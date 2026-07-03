import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(question: str, context_chunks: list[str]) -> str:
    context = "\n\n".join(context_chunks)

    if context.strip():
        prompt = f"""You are RAG Doc Q&A, an intelligent assistant that answers questions based on uploaded documents.

You have been provided with relevant excerpts from the user's documents as context below.
Answer the user's question using ONLY this context. If the answer is not found in the context, say "I could not find the answer in the uploaded documents."

Context:
{context}

Question: {question}
"""
    else:
        prompt = f"""You are RAG Doc Q&A, an intelligent document assistant. Here is what you can do:
- Users can upload PDF documents
- You analyze and understand the content of those documents
- Users can then ask any question about the uploaded documents and you answer based on the content

Respond naturally and helpfully to the user's message. If they ask what you can do or how to use you, explain the above clearly and in a friendly tone.

User message: {question}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024
    )

    return response.choices[0].message.content
