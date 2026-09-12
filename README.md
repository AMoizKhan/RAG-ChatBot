# Multi-Document RAG Application

A lightweight, human-readable Full-Stack RAG (Retrieval-Augmented Generation) application built with **Python (FastAPI + ChromaDB + Groq LLM)** and **React + TypeScript**.

## Architecture & Features
- **Multi-Document Parser**: Handles `.pdf`, `.docx` (Word), `.txt`, and `.md` files cleanly.
- **Smart Chunking**: 600 characters per chunk with 100 characters overlap (preserves sentence & word boundaries).
- **Persistent Vector DB**: Uses `ChromaDB` stored locally in `backend/chroma_db/` (persists on restart).
- **Fast Free Inference**: Uses Groq's `qwen/qwen3.8-27b` with strict zero-hallucination grounding.
- **Source Citations**: Every AI response shows exact chunk excerpts and page numbers.
- **Automated QA Suite**: 100% verified test coverage (`backend/test_suite.py`).
- **Comprehensive Docs**: Includes complete specifications in `PROJECT_DOCUMENTATION.md` and `RAG_Project_Documentation_and_Test_Cases.docx`.
- **Clean UI**: Responsive interface built with React 18, TypeScript, and Vite.

---

## How to Run

### 1. Backend Setup (Python)
Open a terminal in `backend/`:
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Start the server (runs on http://localhost:8000)
python run.py
```

### 2. Frontend Setup (React + TypeScript)
Open a second terminal in `frontend/`:
```bash
cd frontend

# Install dependencies
npm install

# Start Vite dev server (runs on http://localhost:3000)
npm run dev
```

Open your browser at `http://localhost:3000`.
