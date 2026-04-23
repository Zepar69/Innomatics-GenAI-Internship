import os
import sys
from ingest import run_ingestion
from graph import run_query

BANNER = """
╔══════════════════════════════════════════════╗
║       CartNest AI Customer Support Bot       ║
║       Powered by RAG + LangGraph + HITL      ║
╚══════════════════════════════════════════════╝
Type your question and press Enter.
Commands: /quit  /reset  /help
"""

EXAMPLES = """
Try these queries:
  - How do I track my order?
  - What is the return policy for electronics?
  - I was charged twice, what do I do?
  - Do you deliver internationally?
  - How do I reset my password?
  - My account was hacked!          (triggers HITL escalation)
  - I want to report a fraud        (triggers HITL escalation)
"""


def format_response(result):
    lines = ["\n" + "-"*52]
    label = "ESCALATED TO HUMAN" if result["escalated"] else "AI RESPONSE"
    conf  = f"[{result.get('confidence', '')} confidence]" if not result["escalated"] else ""
    lines.append(f"{label}  |  Intent: {result.get('intent', 'general')}  {conf}")
    lines.append("-"*52)
    lines.append(result["final_answer"])
    if result["escalated"] and result.get("escalation_reason"):
        lines.append(f"\nEscalation reason: {result['escalation_reason']}")
    lines.append("-"*52 + "\n")
    return "\n".join(lines)


def main():
    print(BANNER)
    print("Initializing knowledge base...")
    try:
        run_ingestion()
    except Exception as e:
        print(f"Failed to initialize: {e}")
        sys.exit(1)

    print("System ready.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("/quit", "/exit", "quit", "exit"):
            print("Goodbye!")
            break
        if user_input.lower() == "/reset":
            os.system("clear" if os.name == "posix" else "cls")
            print(BANNER)
            continue
        if user_input.lower() == "/help":
            print(EXAMPLES)
            continue

        print("\nProcessing...")
        try:
            result = run_query(user_input)
            print(format_response(result))
        except Exception as e:
            print(f"\nError: {e}\nPlease try again.\n")


if __name__ == "__main__":
    main()
