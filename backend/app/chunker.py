def create_chunks(pages: list[dict], chunk_size: int = 600, overlap: int = 100) -> list[dict]:
    """
    Bari text ko chhotay tukron (chunks) mein todta hai with overlap.
    Overlap is liye zaroori hai taake do chunks ke beech context break na ho.
    """
    chunks = []
    chunk_counter = 0

    for page_data in pages:
        text = page_data["text"]
        page_num = page_data["page"]
        source_name = page_data["source"]

        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + chunk_size
            chunk_slice = text[start:end]

            if chunk_slice.strip():
                chunk_counter += 1
                chunks.append({
                    "chunk_id": f"{source_name}_p{page_num}_c{chunk_counter}",
                    "text": chunk_slice.strip(),
                    "page": page_num,
                    "source": source_name
                })

            # Agla chunk start karne ke liye overlap minus karte hain
            start += (chunk_size - overlap)

    return chunks
