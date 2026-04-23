import os
import shutil
import pypdf
import chromadb

from embeddings import get_embedder
from config import PDF_PATH, CHROMA_DB_PATH, CHUNK_SIZE, CHUNK_OVERLAP


def load_pdf(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"PDF not found: {path}")
    reader = pypdf.PdfReader(path)
    pages = [p.extract_text() or "" for p in reader.pages]
    pages = [p.strip() for p in pages if p.strip()]
    print(f"Loaded {len(pages)} pages from {path}")
    return pages


def chunk_text(text, chunk_size, overlap):
    chunks, start = [], 0
    while start < len(text):
        chunk = text[start:start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def chunk_documents(pages):
    all_chunks = []
    for page_num, page_text in enumerate(pages):
        for chunk in chunk_text(page_text, CHUNK_SIZE, CHUNK_OVERLAP):
            all_chunks.append({"text": chunk, "page": page_num + 1, "source": PDF_PATH})
    print(f"Created {len(all_chunks)} chunks")
    return all_chunks


def build_vector_store(chunks, reset=False):
    if reset and os.path.exists(CHROMA_DB_PATH):
        shutil.rmtree(CHROMA_DB_PATH)

    os.makedirs(CHROMA_DB_PATH, exist_ok=True)
    corpus = [c["text"] for c in chunks]

    embedder = get_embedder(corpus=corpus, force_refit=True)
    embeddings = embedder.embed_batch(corpus)

    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(
        name="cartnest_support",
        metadata={"hnsw:space": "cosine"}
    )
    collection.add(
        documents=[c["text"] for c in chunks],
        embeddings=embeddings,
        metadatas=[{"page": c["page"], "source": c["source"]} for c in chunks],
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )
    print(f"{collection.count()} vectors stored in ChromaDB at {CHROMA_DB_PATH}")
    return client, collection


def load_vector_store():
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_collection("cartnest_support")
    return client, collection


def run_ingestion(reset=False):
    print("\n--- CartNest RAG Ingestion Pipeline ---")
    if not reset and os.path.exists(CHROMA_DB_PATH):
        print("ChromaDB already exists, loading...")
        client, collection = load_vector_store()
        print(f"{collection.count()} vectors ready.\n")
        return client, collection

    pages = load_pdf(PDF_PATH)
    chunks = chunk_documents(pages)
    client, collection = build_vector_store(chunks, reset=reset)
    print("Ingestion complete.\n")
    return client, collection


if __name__ == "__main__":
    run_ingestion(reset=True)
