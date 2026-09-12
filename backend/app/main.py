from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.document_loader import load_document
from app.chunker import create_chunks
from app.vector_db import (
    save_chunks_to_db, 
    search_similar_chunks, 
    get_all_documents, 
    delete_document_by_name
)
from app.llm_service import generate_rag_answer

app = FastAPI(title="Simple RAG Backend", version="1.0")

# CORS middleware taake React frontend se requests seamlessly aa sakein
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema


class AskRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "RAG Backend is running successfully!"}


@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    User se PDF, DOCX ya TXT file leta hai, usay chunk karta hai aur Vector DB mein save karta hai.
    """
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing or invalid."
        )
    filename = file.filename
    file_bytes = await file.read()

    # 1. Document se text aur pages extract karein
    pages = load_document(file_bytes, filename)
    if not pages:
        raise HTTPException(
            status_code=400, 
            detail="Document empty hai ya is format se text extract nahi ho saka."
        )

    # 2. Text ko chunks mein todhein with overlap
    chunks = create_chunks(pages, chunk_size=600, overlap=100)

    # Agar ye file pehle se mojood thi, to purani chunks replace karein
    delete_document_by_name(filename)

    # 3. Chunks ko Vector DB (ChromaDB) mein save karein
    save_chunks_to_db(chunks)

    return {
        "status": "success",
        "message": f"'{filename}' successfully processed and stored!",
        "filename": filename,
        "total_pages": len(pages),
        "total_chunks": len(chunks)
    }


@app.post("/api/ask")
def ask_question(body: AskRequest):
    """
    User ke sawal ka jawab nikaalta hai using RAG:
    1. Query Vector Search (ChromaDB)
    2. Context + Prompt to Groq LLM
    """
    query = body.question.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Top 3 ya 4 sabse relevant chunks dhoondein
    retrieved_chunks = search_similar_chunks(query, n_results=4)

    # Groq LLM se answer generate karein
    answer = generate_rag_answer(query, retrieved_chunks)

    return {
        "question": query,
        "answer": answer,
        "sources": retrieved_chunks
    }


@app.get("/api/documents")
def list_documents():
    """
    Vector DB mein mojood tamam documents ki list wapis karta hai.
    """
    return get_all_documents()


@app.delete("/api/documents/{filename}")
def delete_document(filename: str):
    """
    Kisi document ko database se delete karne ke liye.
    """
    delete_document_by_name(filename)
    return {"message": f"Document '{filename}' deleted successfully."}
