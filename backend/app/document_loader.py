import io
from pypdf import PdfReader
from docx import Document

def load_document(file_bytes: bytes, filename: str) -> list[dict]:
    """
    Kisi bhi document (PDF, Word, Text) se text aur page number extract karta hai.
    Returns: [{"text": "...", "page": 1, "source": "abc.pdf"}, ...]
    """
    file_lower = filename.lower()
    extracted_pages = []

    # 1. Agar PDF file ho
    if file_lower.endswith(".pdf"):
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            for page_idx, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""
                if page_text.strip():
                    extracted_pages.append({
                        "text": page_text.strip(),
                        "page": page_idx + 1,
                        "source": filename
                    })
        except Exception:
            return []

    # 2. Agar Word Document (.docx) ho
    elif file_lower.endswith(".docx"):
        try:
            doc = Document(io.BytesIO(file_bytes))
            full_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            if full_text.strip():
                extracted_pages.append({
                    "text": full_text.strip(),
                    "page": 1,
                    "source": filename
                })
        except Exception:
            return []

    # 3. Agar Plain Text (.txt ya .md) ho
    elif file_lower.endswith(".txt") or file_lower.endswith(".md"):
        text = file_bytes.decode("utf-8", errors="ignore")
        if text.strip():
            extracted_pages.append({
                "text": text.strip(),
                "page": 1,
                "source": filename
            })

    return extracted_pages
