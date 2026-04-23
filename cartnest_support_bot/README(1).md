# CartNest RAG Customer Support Bot

A **Retrieval-Augmented Generation (RAG)** system for e-commerce customer support, built with **LangGraph**, **ChromaDB**, and **Groq LLM**.

## Architecture

```
User Query
    │
    ▼
[INPUT NODE] — Intent Detection
    │
    ▼ (conditional routing)
┌──────────────────────────────┐
│  Normal / High Confidence?   │  Low Confidence / Sensitive?  │
└──────────┬───────────────────┴──────────────┬────────────────┘
           │                                  │
           ▼                                  ▼
     [RAG NODE]                         [HITL NODE]
     Retrieve + LLM Answer              Escalate to Human Agent
           │                                  │
           └─────────────┬────────────────────┘
                         ▼
                  [OUTPUT NODE]
                  Format & Return
```

## Setup

### 1. Clone & Install
```bash
git clone <your-repo-url>
cd cartnest_support_bot
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
# Create a .env file and add:
GROQ_API_KEY=your_key_here   # Free at console.groq.com
```

### 3. Generate Knowledge Base PDF
```bash
python generate_pdf.py
```

### 4. Run
```bash
python main.py
```

> Works without a Groq API key in demo mode — returns context directly from the knowledge base.

## Project Structure

```
cartnest_support_bot/
├── main.py              # CLI entry point
├── graph.py             # LangGraph workflow (nodes + routing)
├── ingest.py            # PDF → ChromaDB ingestion pipeline
├── retriever.py         # ChromaDB similarity search
├── embeddings.py        # TF-IDF + SVD embedding engine
├── config.py            # Centralized configuration
├── generate_pdf.py      # Knowledge base PDF generator
├── requirements.txt
├── .env                 # API keys (never commit this)
├── data/
│   ├── cartnest_support_kb.pdf    # Knowledge base
│   ├── chroma_db/                 # Vector store (auto-created)
│   └── embedding_model.pkl        # Fitted embedder (auto-created)
└── logs/
    └── escalations.jsonl          # HITL escalation log
```

## Key Design Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Embedding | TF-IDF + SVD | Local, no API cost, effective for FAQ-style KB |
| Vector DB | ChromaDB | Persistent, serverless, LangChain-native |
| Workflow | LangGraph | Stateful graph with conditional routing |
| LLM | Groq (llama3) | Free tier, fast inference |
| Chunking | 500 chars + 50 overlap | Balanced context vs retrieval granularity |

## HITL Escalation Triggers

1. **Escalation keywords** — fraud, hacked, scam, unauthorized, legal, lawsuit, etc.
2. **Low retrieval confidence** — similarity score below 0.35
3. All escalations logged to `logs/escalations.jsonl`

## Example Queries

```
How do I track my order?             → RAG answer
What is CartNest's return policy?    → RAG answer
My account was hacked!               → HITL escalation
I want to report a fraud complaint   → HITL escalation
```

## Tech Stack

- **LangGraph** — Graph-based workflow orchestration
- **ChromaDB** — Persistent vector database
- **scikit-learn** — TF-IDF + SVD embeddings
- **Groq** — Fast LLM inference (llama3-70b)
- **pypdf** — PDF text extraction
- **reportlab** — PDF generation

---
*Built as part of Innomatics Research Labs GenAI Internship — Final Project*
