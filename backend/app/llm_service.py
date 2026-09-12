import os
from dotenv import load_dotenv
from groq import Groq

# Load .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")
# Groq Client Initialization
groq_client = Groq(api_key=GROQ_API_KEY)


def generate_rag_answer(query: str, retrieved_chunks: list[dict]) -> str:
    """
    Retrieved chunks ko context bana kar Groq LLM ko bhejta hai aur grounded answer hasil karta hai.
    """
    if not retrieved_chunks:
        return "Abhi koi document upload nahi kiya gaya ya is sawal se related koi data nahi mila."

    # Context text taiyar karna (Page number aur Source ke sath)
    formatted_context = ""
    for idx, chunk in enumerate(retrieved_chunks, 1):
        formatted_context += f"--- Chunk {idx} (File: {chunk['source']}, Page: {chunk['page']}) ---\n"
        formatted_context += f"{chunk['text']}\n\n"

    # Strict Grounding Prompt taake model hallucinate na kare
    system_prompt = (
        "You are an accurate AI document assistant. "
        "Your task is to answer the user's question using ONLY the provided context below. "
        "If the answer is NOT present in the context, explicitly say: "
        "'I could not find information about this in the uploaded document(s).' "
        "Do not invent facts or assume anything beyond the context. Be concise and direct."
    )

    user_prompt = f"Context:\n{formatted_context}\nQuestion:\n{query}\n\nAnswer:"

    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,  # Low temperature = High accuracy, no creative guessing
            max_tokens=600    # Prevents exceeding Groq on-demand OTPM limit (1000)
        )
        content = response.choices[0].message.content
        return content if content is not None else ""
    except Exception as e:
        return f"Groq API Error: {str(e)}"
