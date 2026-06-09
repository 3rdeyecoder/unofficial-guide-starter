# generate.py
# Milestone 5 — Generation and Interface
# Retrieves relevant chunks and generates answers using Groq API.

import os
from dotenv import load_dotenv
from groq import Groq
from embed import embed_chunks, retrieve
from ingest import main as load_chunks

# Load API key from .env
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load and embed all chunks once at startup
print("Loading and embedding documents...")
all_chunks = load_chunks()
embed_chunks(all_chunks)
print("Ready.\n")


def build_prompt(query, chunks):
    """
    Builds a prompt from the retrieved chunks and user query.
    Instructs the model to answer only from the provided context
    and cite sources by name.
    """
    context = ""
    for i, chunk in enumerate(chunks):
        context += f"[Source {i+1}: {chunk['source']}]\n{chunk['text']}\n\n"

    prompt = f"""You are a helpful weight loss assistant. Answer the user's question 
using ONLY the context provided below. Always cite your sources by name 
(e.g. 'According to Cleveland Clinic...'). If the context does not contain 
enough information to answer the question, say 'I don't have enough information 
on that topic in my knowledge base.'

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""

    return prompt


def generate(query):
    """
    Retrieves top-3 chunks for the query and generates
    a grounded answer with source citations using Groq.
    """
    chunks = retrieve(query, k=3)

    if not chunks:
        return "I could not find any relevant information for that question."

    prompt = build_prompt(query, chunks)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content


def main():
    """
    Simple CLI interface — type a question and get an answer.
    Type 'quit' to exit.
    """
    print("=" * 60)
    print("Weight Loss Unofficial Guide — Q&A")
    print("=" * 60)
    print("Ask any weight loss question. Type 'quit' to exit.\n")

    while True:
        query = input("Your question: ").strip()

        if query.lower() == "quit":
            print("Goodbye!")
            break

        if not query:
            continue

        print("\nSearching knowledge base...\n")
        answer = generate(query)
        print(f"Answer:\n{answer}\n")
        print("-" * 60)


if __name__ == "__main__":
    main()
