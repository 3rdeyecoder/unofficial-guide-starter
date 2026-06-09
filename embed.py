# embed.py
# Milestone 4 — Embedding and Retrieval
# Embeds chunks from ingest.py using all-MiniLM-L6-v2
# and stores them in a ChromaDB vector store.

import chromadb
from sentence_transformers import SentenceTransformer
from ingest import main as load_chunks

# Load embedding model
MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

# Initialize ChromaDB in-memory client and collection
client = chromadb.Client()
collection = client.get_or_create_collection(name="weight_loss")


def embed_chunks(chunks):
    """
    Takes the list of chunk dicts from ingest.py,
    embeds each chunk's text, and stores vectors
    plus metadata in ChromaDB.
    """
    print("=" * 60)
    print("STAGE 3: Embedding + Vector Store")
    print("=" * 60)

    texts = [c["text"] for c in chunks]
    ids = [f"{c['filename']}_{c['chunk_index']}" for c in chunks]
    metadatas = [
        {
            "source": c["source"],
            "url": c["url"],
            "filename": c["filename"],
            "chunk_index": c["chunk_index"]
        }
        for c in chunks
    ]

    print(f"  Embedding {len(chunks)} chunks with {MODEL_NAME}...")
    embeddings = model.encode(texts, show_progress_bar=True)

    collection.add(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=texts,
        metadatas=metadatas
    )

    print(f"  Stored {collection.count()} chunks in ChromaDB")
    return collection


def retrieve(query, k=3):
    """
    Embeds the user query and returns the top-k
    most similar chunks with their metadata.
    """
    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "url": results["metadatas"][0][i]["url"],
            "filename": results["metadatas"][0][i]["filename"],
            "chunk_index": results["metadatas"][0][i]["chunk_index"]
        })

    return chunks


def main():
    # Load and embed all chunks
    all_chunks = load_chunks()
    collection = embed_chunks(all_chunks)

    # Test retrieval with all 5 evaluation questions
    print("\n" + "=" * 60)
    print("STAGE 4: Retrieval — Evaluation Questions")
    print("=" * 60)

    test_questions = [
        "What is a calorie deficit and why is it important for weight loss?",
        "How much weight loss per week is generally considered safe and sustainable?",
        "Why is protein important during weight loss?",
        "How does sleep affect weight loss?",
        "What causes a weight loss plateau and how can it be overcome?"
    ]

    for question in test_questions:
        print(f"\nQ: {question}")
        results = retrieve(question)
        for r in results:
            print(f"  → [{r['source']}] {r['filename']} chunk {r['chunk_index']}")
            print(f"     {r['text'][:80]}...")


if __name__ == "__main__":
    main()
