import os
import json
import hashlib
from datetime import datetime
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END

from retriever import get_retriever
from config import CONFIDENCE_THRESHOLD, ESCALATION_KEYWORDS, GROQ_API_KEY


class GraphState(TypedDict):
    query            : str
    intent           : str
    chunks           : list
    confidence       : str
    route            : str
    llm_response     : str
    final_answer     : str
    escalated        : bool
    escalation_reason: str
    human_response   : str
    sources          : list


def get_llm_response(prompt):
    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        return _demo_response(prompt)
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"[LLM Error: {e}] {_extract_context(prompt)}"


def _extract_context(prompt):
    if "KNOWLEDGE BASE:" in prompt and "QUERY:" in prompt:
        start = prompt.find("KNOWLEDGE BASE:") + len("KNOWLEDGE BASE:")
        end = prompt.find("QUERY:")
        ctx = prompt[start:end].strip()
        return ctx[:300] + "..." if len(ctx) > 300 else ctx
    return "Please contact support for assistance."


def _demo_response(prompt):
    ctx = _extract_context(prompt)
    return (
        f"Based on CartNest support documentation:\n\n{ctx}\n\n"
        f"[Demo mode — add GROQ_API_KEY in .env for full AI responses.]"
    )


def build_prompt(query, context):
    return f"""You are a helpful customer support agent for CartNest, an e-commerce platform.
Answer the customer's question using ONLY the information from the knowledge base below.
If the context does not have enough information, say so and suggest contacting support.
Be concise, friendly, and actionable. Use bullet points where it helps clarity.

KNOWLEDGE BASE:
{context}

QUERY:
{query}

RESPONSE:"""


def detect_intent(query):
    q = query.lower()
    if any(kw in q for kw in [k.lower() for k in ESCALATION_KEYWORDS]):
        return "escalation"
    if any(w in q for w in ["track", "order", "delivered", "dispatch", "shipment"]):
        return "order_tracking"
    if any(w in q for w in ["charged", "payment", "refund", "invoice", "emi", "bill"]):
        return "payment_issue"
    if any(w in q for w in ["return", "exchange", "replace", "wrong product"]):
        return "returns"
    if any(w in q for w in ["account", "password", "login", "email", "phone", "delete"]):
        return "account"
    if any(w in q for w in ["product", "review", "authentic", "seller", "counterfeit"]):
        return "product"
    if any(w in q for w in ["deliver", "shipping", "address", "pin code", "international"]):
        return "shipping"
    return "general"


def input_node(state: GraphState) -> GraphState:
    query = state["query"].strip()
    intent = detect_intent(query)
    print(f"\n[INPUT] Query: {query}")
    print(f"[INPUT] Intent: {intent}")
    return {**state, "query": query, "intent": intent}


def rag_node(state: GraphState) -> GraphState:
    print("\n[RAG] Retrieving context...")
    retriever = get_retriever()
    chunks, confidence = retriever.retrieve_with_confidence(state["query"])
    print(f"[RAG] {len(chunks)} chunks | Confidence: {confidence} | Top score: {chunks[0]['score'] if chunks else 0:.3f}")
    context = retriever.format_context(chunks)
    prompt = build_prompt(state["query"], context)
    response = get_llm_response(prompt)
    sources = [f"Page {c['page']} (score: {c['score']:.2f})" for c in chunks]
    return {**state, "chunks": chunks, "confidence": confidence,
            "llm_response": response, "sources": sources, "escalated": False}


def hitl_node(state: GraphState) -> GraphState:
    print(f"\n[HITL] Escalating — {state.get('escalation_reason', '')}")
    _log_escalation(state)
    ticket = _ticket_id(state["query"])
    response = (
        f"Thank you for contacting CartNest Support.\n\n"
        f"Your query requires attention from one of our specialist agents.\n\n"
        f"What happens next:\n"
        f"- Case escalated (Ticket: {ticket})\n"
        f"- A senior agent will reach you within 2-4 hours\n"
        f"- Updates sent via email and SMS\n\n"
        f"For urgent help, call 1800-XXX-XXXX (Mon-Sat, 9AM-7PM).\n\n"
        f"We apologise for the inconvenience."
    )
    return {**state, "llm_response": response, "escalated": True,
            "human_response": "", "chunks": [], "sources": []}


def output_node(state: GraphState) -> GraphState:
    answer = state["llm_response"]
    if state.get("sources") and not state.get("escalated"):
        src = "\n".join(f"  - {s}" for s in state["sources"][:3])
        answer += f"\n\nSources:\n{src}"
    print("\n[OUTPUT] Response ready.")
    return {**state, "final_answer": answer}


def route_query(state: GraphState) -> Literal["rag_node", "hitl_node"]:
    intent = state.get("intent", "general")
    if intent == "escalation":
        state["escalation_reason"] = f"High-risk intent: {intent}"
        state["route"] = "escalate"
        print("[ROUTER] -> HITL (escalation intent)")
        return "hitl_node"

    retriever = get_retriever()
    _, confidence = retriever.retrieve_with_confidence(state.get("query", ""))
    if confidence == "LOW":
        state["escalation_reason"] = "Low retrieval confidence"
        state["route"] = "escalate"
        print("[ROUTER] -> HITL (low confidence)")
        return "hitl_node"

    state["route"] = "rag"
    print(f"[ROUTER] -> RAG (confidence: {confidence})")
    return "rag_node"


def _ticket_id(query):
    h = hashlib.md5(query.encode()).hexdigest()[:6].upper()
    return f"CN-{h}"


def _log_escalation(state: GraphState):
    os.makedirs("logs", exist_ok=True)
    entry = {
        "timestamp"         : datetime.now().isoformat(),
        "ticket_id"         : _ticket_id(state["query"]),
        "query"             : state["query"],
        "intent"            : state.get("intent", ""),
        "escalation_reason" : state.get("escalation_reason", ""),
        "confidence"        : state.get("confidence", "")
    }
    with open("logs/escalations.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")


def build_graph():
    graph = StateGraph(GraphState)
    graph.add_node("input_node",  input_node)
    graph.add_node("rag_node",    rag_node)
    graph.add_node("hitl_node",   hitl_node)
    graph.add_node("output_node", output_node)
    graph.set_entry_point("input_node")
    graph.add_conditional_edges("input_node", route_query,
                                {"rag_node": "rag_node", "hitl_node": "hitl_node"})
    graph.add_edge("rag_node",  "output_node")
    graph.add_edge("hitl_node", "output_node")
    graph.add_edge("output_node", END)
    return graph.compile()


_graph = None

def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


def run_query(query):
    graph = get_graph()
    initial_state: GraphState = {
        "query": query, "intent": "", "chunks": [],
        "confidence": "", "route": "", "llm_response": "",
        "final_answer": "", "escalated": False,
        "escalation_reason": "", "human_response": "", "sources": []
    }
    return graph.invoke(initial_state)


if __name__ == "__main__":
    tests = [
        "How do I track my order?",
        "I was charged twice for my order",
        "My account was hacked and I see unauthorized orders!",
        "What is the return policy for electronics?",
        "Do you deliver internationally?",
    ]
    for q in tests:
        print(f"\n{'='*50}")
        result = run_query(q)
        print(f"Query    : {result['query']}")
        print(f"Intent   : {result['intent']}")
        print(f"Route    : {result['route']}")
        print(f"Escalated: {result['escalated']}")
        print(f"Answer   :\n{result['final_answer'][:300]}")
