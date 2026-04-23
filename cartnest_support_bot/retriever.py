import chromadb
from embeddings import get_embedder
from config import CHROMA_DB_PATH, TOP_K_RESULTS, CONFIDENCE_THRESHOLD


class Retriever:
    def __init__(self):
        self.embedder = get_embedder()
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        self.collection = self.client.get_collection("cartnest_support")
        print(f"Retriever ready. KB size: {self.collection.count()} chunks")

    def retrieve(self, query, top_k=TOP_K_RESULTS):
        query_vec = self.embedder.embed_one(query)
        results = self.collection.query(
            query_embeddings=[query_vec],
            n_results=min(top_k, self.collection.count()),
            include=["documents", "metadatas", "distances"]
        )
        chunks = []
        for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
            chunks.append({
                "text"  : doc,
                "score" : round(max(0.0, 1.0 - dist), 4),
                "page"  : meta.get("page", "?"),
                "source": meta.get("source", "?")
            })
        chunks.sort(key=lambda x: x["score"], reverse=True)
        return chunks

    def retrieve_with_confidence(self, query):
        chunks = self.retrieve(query)
        if not chunks:
            return [], "LOW"
        top_score = chunks[0]["score"]
        if top_score >= 0.6:
            confidence = "HIGH"
        elif top_score >= CONFIDENCE_THRESHOLD:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"
        return chunks, confidence

    def format_context(self, chunks):
        if not chunks:
            return "No relevant information found in the knowledge base."
        parts = []
        for i, c in enumerate(chunks, 1):
            parts.append(f"[Source {i} | Page {c['page']} | Score: {c['score']:.2f}]\n{c['text']}")
        return "\n\n---\n\n".join(parts)


_retriever_instance = None

def get_retriever():
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = Retriever()
    return _retriever_instance


if __name__ == "__main__":
    r = Retriever()
    queries = [
        "How do I track my order?",
        "I was charged twice",
        "What is the return policy?",
        "My account was hacked",
    ]
    for q in queries:
        chunks, conf = r.retrieve_with_confidence(q)
        print(f"\nQuery : {q}")
        print(f"Conf  : {conf} | Top score: {chunks[0]['score'] if chunks else 0}")
        print(f"Chunk : {chunks[0]['text'][:100] if chunks else 'None'}...")
