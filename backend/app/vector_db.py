import os
from typing import Any, cast
import chromadb
from sentence_transformers import SentenceTransformer

# Storage directory jahan database disk par save hogi
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
os.makedirs(DB_DIR, exist_ok=True)

# ChromaDB Persistent Client (Server restart hone par bhi data delete nahi hota)
client = chromadb.PersistentClient(path=DB_DIR)
collection = client.get_or_create_collection(name="rag_documents")

# Free local embedding model (384 dimensions)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def save_chunks_to_db(chunks: list[dict]):
    """
    Chunks ko embed kar ke Vector DB (ChromaDB) mein save karta hai.
    """
    if not chunks:
        return

    texts = [c["text"] for c in chunks]
    ids = [c["chunk_id"] for c in chunks]
    metadatas = [{"source": c["source"], "page": c["page"]} for c in chunks]

    # Generate Embeddings
    embeddings = embedding_model.encode(texts).tolist()

    # Store in ChromaDB
    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=cast(Any, metadatas)
    )


def search_similar_chunks(query: str, n_results: int = 4) -> list[dict]:
    """
    User query ki embedding banata hai aur sabse relevant chunks dhoondta hai.
    """
    query_vector = embedding_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_vector,
        n_results=n_results
    )

    retrieved = []
    if results:
        documents = results.get("documents")
        metadatas = results.get("metadatas")

        if documents and metadatas and documents[0] and metadatas[0]:
            docs = documents[0]
            metas = metadatas[0]

            for text, meta in zip(docs, metas):
                meta_dict = meta if isinstance(meta, dict) else {}
                retrieved.append({
                    "text": text,
                    "source": meta_dict.get("source", "Unknown"),
                    "page": meta_dict.get("page", 1)
                })

    return retrieved


def get_all_documents() -> list[dict]:
    """
    Pata lagata hai ke database mein kon kon se documents mojood hain.
    """
    data = collection.get()
    unique_sources: dict[str, int] = {}
    
    metadatas = data.get("metadatas") if data else None
    if metadatas:
        for meta in metadatas:
            if meta and isinstance(meta, dict):
                source = str(meta.get("source", "Unknown"))
                unique_sources[source] = unique_sources.get(source, 0) + 1

    return [{"name": name, "chunk_count": count} for name, count in unique_sources.items()]


def delete_document_by_name(filename: str):
    """
    Specific document ko Vector DB se delete karta hai.
    """
    collection.delete(where={"source": filename})
