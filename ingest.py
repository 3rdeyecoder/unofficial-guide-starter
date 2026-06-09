# ingest.py
# Milestone 3 — Document Ingestion and Chunking
# Loads 10 .txt files from documents/, parses metadata headers,
# and produces chunks of 500 words with 100-word overlap.

import os

DOCUMENTS_DIR = "documents"
CHUNK_SIZE = 500
OVERLAP = 100


def load_documents(directory):
    """
    Reads all .txt files from the documents/ folder.
    Parses the SOURCE URL, TITLE, and SOURCE metadata headers
    at the top of each file.
    Returns a list of dicts: {text, source, url, filename}
    """
    documents = []

    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".txt"):
            continue

        filepath = os.path.join(directory, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            raw = f.read()

        # Parse metadata from header lines
        lines = raw.splitlines()
        metadata = {
            "filename": filename,
            "source": "",
            "url": ""
        }

        body_start = 0
        for i, line in enumerate(lines):
            if line.startswith("SOURCE URL:"):
                metadata["url"] = line.replace("SOURCE URL:", "").strip()
            elif line.startswith("SOURCE:"):
                metadata["source"] = line.replace("SOURCE:", "").strip()
            elif line.startswith("=" * 10):
                # The long === divider marks the end of the header block
                body_start = i + 1
                break

        # Everything after the header divider is the article body
        body = " ".join("\n".join(lines[body_start:]).split())
        metadata["text"] = body

        documents.append(metadata)
        print(f"  Loaded: {filename} — source: {metadata['source']}")

    return documents


def chunk_text(text, metadata, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    """
    Splits text into fixed-size chunks of chunk_size words
    with overlap words repeated between consecutive chunks.
    Each chunk is a dict carrying the parent document's metadata.
    Returns a list of dicts: {text, source, url, filename, chunk_index}
    """
    words = text.split()
    chunks = []
    start = 0
    chunk_index = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunk_text_str = " ".join(chunk_words).strip()

        chunks.append({
            "text": chunk_text_str,
            "source": metadata["source"],
            "url": metadata["url"],
            "filename": metadata["filename"],
            "chunk_index": chunk_index
        })

        start += chunk_size - overlap
        chunk_index += 1

    return chunks


def main():
    print("=" * 60)
    print("STAGE 1: Document Ingestion")
    print("=" * 60)

    documents = load_documents(DOCUMENTS_DIR)
    print(f"\nDocuments loaded: {len(documents)}")

    print("\n" + "=" * 60)
    print("STAGE 2: Chunking")
    print("=" * 60)

    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"], doc)
        all_chunks.extend(chunks)
        print(f"  {doc['filename']}: {len(chunks)} chunks")

    print(f"\nTotal chunks produced: {len(all_chunks)}")

    # Verification checks
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)

    # Check 1: first chunk is a dict with all required keys
    first = all_chunks[0]
    required_keys = {"text", "source", "url", "filename", "chunk_index"}
    missing = required_keys - first.keys()
    if missing:
        print(f"  FAIL — missing keys in chunk: {missing}")
    else:
        print(f"  PASS — all required keys present in chunk dict")

    # Check 2: word count close to 500
    word_count = len(first["text"].split())
    print(f"  Chunk 0 word count: {word_count} (target: {CHUNK_SIZE})")

    # Check 3: overlap — last 100 words of chunk 0 should appear at start of chunk 1
    same_doc_chunks = [c for c in all_chunks if c["filename"] == "article7.txt"]
    chunk0_words = same_doc_chunks[0]["text"].split()
    chunk1_words = same_doc_chunks[1]["text"].split()
    overlap_from_0 = chunk0_words[-OVERLAP:]
    start_of_1 = chunk1_words[:OVERLAP]

    if overlap_from_0 == start_of_1:
        print(f"  PASS — 100-word overlap confirmed between chunk 0 and chunk 1")
    else:
        print(f"  FAIL — overlap mismatch between chunk 0 and chunk 1")

    # Print sample chunk for inspection
    print("\n--- Sample chunk (chunk 0) ---")
    print(f"  filename:    {all_chunks[0]['filename']}")
    print(f"  source:      {all_chunks[0]['source']}")
    print(f"  url:         {all_chunks[0]['url']}")
    print(f"  chunk_index: {all_chunks[0]['chunk_index']}")
    print(f"  text[:100]:  {all_chunks[0]['text'][:100]}...")

    return all_chunks


if __name__ == "__main__":
    all_chunks = main()
