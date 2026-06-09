# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

Weight Loss and Healthy Living: The Unofficial Guide

Weight loss information is spread across medical websites, health organizations, nutrition resources, and fitness articles. Many people receive conflicting advice from social media, influencers, and fad diets. This project creates a searchable knowledge base using evidence-based weight loss information so users can ask questions and receive grounded answers with source citations.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 |Cleveland Clinic|Calorie deficit and safe weight loss|documents/article1.txt
| 2 |Mayo Clinic|Weight loss strategies for long-term success|documents/article2.txt
| 3 |Healthline|Breaking through a weight loss plateau|documents/article3.txt
| 4 |Sleep Foundation|Relationsh between sleep & weight loss| documents/article4.txt
| 5 |Northside Hospital|Metabolism, sleep, stress|documents/article5.txt
| 6 |Ubie Health|Caloric deficits, metabolism|documents/article6.txt
| 7 |Sezarro Overseas|Evidence-based weight loss strategies|documents/article7.txt
| 8 |Apollo Pharmacy|Cardio versus strength training|documents/article8.txt
| 9 |You Wellness|weight management|documents/article9.txt
| 10|News Medical|Sustainable weight loss|documents/article10.txt

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
500 words
**Overlap:**
100 words
**Reasoning:**
I selected fixed-size chunking because the source documents are long-form educational articles that contain multiple topics and subtopics. A chunk size of 500 words preserves enough context for the retrieval system to understand complete concepts such as calorie deficits, protein intake, metabolism, sleep, and exercise. A 100-word overlap helps prevent important information from being split across chunk boundaries, improving retrieval quality. Fixed-size chunking is also computationally efficient and straightforward to implement using Python.---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
all-MiniLM-L6-v2 via sentence-transformers
**Top-k:**
3
**Production tradeoff reflection:**
For a production deployment serving real users, I would consider switching to a
larger, more powerful embedding model such as text-embedding-3-large from OpenAI
or embed-english-v3.0 from Cohere. The tradeoffs I would weigh are:

- Accuracy on domain-specific text: all-MiniLM-L6-v2 is a general-purpose model
  trained on broad web text. A production health and wellness system would benefit
  from a model fine-tuned on medical or nutritional content, which would better
  understand domain-specific terms like "adaptive thermogenesis", "caloric deficit",
  or "GLP-1 agonists" and return more precise retrieval results.

- Context length: all-MiniLM-L6-v2 has a maximum input length of 256 tokens, which
  is why a 500-word chunk size can cause truncation on longer chunks. A model with
  a longer context window (such as text-embedding-3-large at 8,191 tokens) would
  allow larger, more coherent chunks without losing information.

- Latency: all-MiniLM-L6-v2 runs locally with no API calls, making it fast and
  free. A cloud-based model like OpenAI's embeddings adds network latency and API
  cost per request — a real tradeoff at scale.

- Multilingual support: if the system needed to serve non-English speakers,
  a multilingual model such as paraphrase-multilingual-MiniLM-L12-v2 would be
  necessary. The current model is English-only.
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |What is a calorie deficit and why is it important for weight loss? | A calorie deficit occurs when a person consumes fewer calories than they burn. It is the fundamental requirement for weight loss because the body must use stored energy to make up the difference.|
| 2 |How much weight loss per week is generally considered safe and sustainable? |Most sources recommend approximately 1–2 pounds (0.5–1 kg) per week through a moderate calorie deficit and healthy lifestyle changes. |
| 3 |Why is protein important during weight loss? |Protein helps preserve muscle mass, increases satiety (fullness), and may increase calorie burn through digestion, making weight loss easier to sustain. |
| 4 | How does sleep affect weight loss?|Poor sleep can increase hunger hormones, decrease fullness signals, lower metabolism, increase cravings, and make it more difficult to maintain a calorie deficit. |
| 5 | What causes a weight loss plateau and how can it be overcome?| Weight loss plateaus can occur due to metabolic adaptation, reduced calorie expenditure, inaccurate calorie tracking, insufficient protein intake, lack of exercise progression, poor sleep, or stress. Adjusting nutrition, activity, sleep, and tracking habits may help restart progress.|

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Some documents may provide slightly different recommendations about weight loss, nutrition, exercise, or calorie intake. These inconsistencies could make it difficult for the system to generate a single clear answer and may result in responses that combine conflicting information.
2. Relevant information may be split across multiple chunks or documents. If the retrieval system fails to retrieve all necessary chunks, the generated response may be incomplete or miss important context, reducing answer accuracy.


---

## Architecture

+------------------------------------------------------------------+
|  STAGE 1: Document Ingestion                                     |
|  Tool: Python (open, os.listdir)                                 |
|  - Load 10 .txt files from documents/                            |
|  - Parse metadata header (SOURCE URL, TITLE, SOURCE)            |
|  - Output: list of {text, source, url, filename} dicts          |
+------------------------------------------------------------------+
                              |
                              | raw text + metadata
                              v
+------------------------------------------------------------------+
|  STAGE 2: Chunking                                               |
|  Tool: Python (custom chunk_text() function)                     |
|  - Fixed-size: 500 words per chunk                               |
|  - Overlap: 100 words                                            |
|  - Output: list of {text, source, url, filename, chunk_index}   |
+------------------------------------------------------------------+
                              |
                              | chunk dicts with metadata
                              v
+------------------------------------------------------------------+
|  STAGE 3: Embedding + Vector Store                               |
|  Embedding: sentence-transformers (all-MiniLM-L6-v2)            |
|  Vector Store: ChromaDB or FAISS                                 |
|  - Embed each chunk text into a vector                           |
|  - Store vector + metadata in index                              |
|  - Output: persistent vector index                               |
+------------------------------------------------------------------+
                              |
                    +---------+---------+
                    |                   |
               user query          vector index
                    |                   |
                    v                   v
+------------------------------------------------------------------+
|  STAGE 4: Retrieval                                              |
|  Tool: ChromaDB or FAISS similarity search                       |
|  - Embed user query with same model (all-MiniLM-L6-v2)          |
|  - Cosine similarity search against index                        |
|  - Return top-k = 3 chunks with metadata                         |
+------------------------------------------------------------------+
                              |
                              | top-3 chunks + user query
                              v
+------------------------------------------------------------------+
|  STAGE 5: Generation                                             |
|  Tool: Claude API (claude-sonnet-4-20250514)                    |
|  - Build prompt: system message + retrieved chunks + question    |
|  - Send to Claude API                                            |
|  - Output: grounded answer with source citations                 |
+------------------------------------------------------------------+
                              |
                              | answer + citations
                              v
                       [ User Interface ]
                       Python CLI or
                       Gradio/Streamlit

---

## AI Tool Plan

---

### Milestone 3 — Ingestion and Chunking

**AI tool:** Claude (claude.ai)

**Input to Claude:**
- The Documents table from this planning.md (the 10 sources and filenames)
- The Chunking Strategy section (500 words, 100-word overlap, fixed-size)
- The Architecture stage 1 and stage 2 boxes from the ASCII diagram
- The .txt file format (SOURCE URL, TITLE, SOURCE header structure)

**What I expect it to produce:**
- A load_documents() function that reads all 10 .txt files from documents/,
  parses the SOURCE URL, TITLE, and SOURCE metadata headers at the top of
  each file, and returns a list of dicts with keys: text, source, url, filename
- A chunk_text(text, metadata, chunk_size=500, overlap=100) function that
  splits text by word count, applies 100-word overlap, and returns a list of
  dicts with keys: text, source, url, filename, chunk_index
- A main ingestion script that calls both functions and prints a summary
  (number of documents loaded, total chunks produced)

**How I will verify the output:**
- Run the script and confirm it loads exactly 10 documents with no errors
- Print the first 3 chunks and confirm each one is a dict containing text,
  source, url, filename, and chunk_index — not a plain string
- Confirm chunk word counts are close to 500 words using len(chunk["text"].split())
- Confirm overlap by checking that the last 100 words of chunk 0 appear at
  the start of chunk 1

---

### Milestone 4 — Embedding and Retrieval

**AI tool:** Claude (claude.ai)

**Input to Claude:**
- The Retrieval Approach section (all-MiniLM-L6-v2, top-k = 3)
- The Architecture stage 3 and stage 4 boxes from the ASCII diagram
- The output format from Milestone 3 (list of chunk dicts with metadata)
- The 5 test questions from the Evaluation Plan section

**What I expect it to produce:**
- An embed_chunks() function that takes the list of chunk dicts from Milestone 3,
  uses sentence-transformers with all-MiniLM-L6-v2 to embed each chunk's text
  field, and stores the vectors plus metadata in ChromaDB or FAISS
- A retrieve(query, k=3) function that embeds a user query with the same model,
  runs cosine similarity search against the index, and returns the top-3 chunk
  dicts including their text, source, url, and filename
- A test script that runs all 5 evaluation questions through retrieve() and
  prints the top-3 results for each

**How I will verify the output:**
- Run the 5 test questions and confirm each returns exactly 3 chunks
- Confirm every returned chunk is a dict with text, source, url, and filename
  (not just a text string — metadata must survive embedding)
- Manually check that results for "How does sleep affect weight loss?" return
  chunks from article4.txt or article5.txt, not unrelated articles
- Confirm no chunk appears in results without a source field (would break citations)

---

### Milestone 5 — Generation and Interface

**AI tool:** Claude (claude.ai)

**Input to Claude:**
- The Architecture stage 5 box from the ASCII diagram
- The output format from Milestone 4 (top-3 chunk dicts with metadata)
- The Evaluation Plan section (5 test questions and expected answers)
- The Domain section (evidence-based weight loss, source citations required)

**What I expect it to produce:**
- A build_prompt(query, chunks) function that formats a system message instructing
  the model to answer only from the retrieved chunks and cite sources by name,
  concatenates the 3 chunk texts with their source labels, and appends the
  user query
- A generate(query) function that calls retrieve() to get the top-3 chunks,
  calls build_prompt(), sends the prompt to the Claude API, and returns the
  response text
- A simple CLI or Gradio interface that accepts a user question, calls generate(),
  and prints or displays the answer with citations
- Error handling for empty retrieval results and API failures

**How I will verify the output:**
- Run all 5 evaluation questions and compare answers against the expected answers
  in the Evaluation Plan
- Confirm every answer includes at least one source citation (e.g. "According to
  Cleveland Clinic..." or "[Source: Mayo Clinic]")
- Confirm the model does not answer from outside knowledge — test with an
  off-topic question like "What is the capital of France?" and verify it responds
  that it can only answer weight loss questions from the provided sources
- Confirm the interface accepts typed input and displays a readable response
