# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

Weight loss information is spread across medical websites, health organizations,
nutrition resources, and fitness articles. Many people receive conflicting advice
from social media, influencers, and fad diets. This project creates a searchable
knowledge base using evidence-based weight loss information so users can ask
questions and receive grounded answers with source citations.

This knowledge is valuable because it is scattered across dozens of sources and
difficult to search precisely. A user searching "how much protein should I eat"
gets millions of results with no way to filter for quality. Official channels like
government health websites are often too broad or too technical. This system
surfaces verified, evidence-based answers with citations from trusted medical and
wellness sources.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Cleveland Clinic | Medical website | https://health.clevelandclinic.org/calorie-deficit |
| 2 | Mayo Clinic | Medical website | https://www.mayoclinic.org/healthy-lifestyle/weight-loss/in-depth/weight-loss/art-20047752 |
| 3 | Healthline | Health media | https://www.healthline.com/nutrition/weight-loss-plateau |
| 4 | Sleep Foundation | Health organization | https://www.sleepfoundation.org/physical-health/weight-loss-and-sleep |
| 5 | Northside Hospital | Medical website | https://www.northside.com/about/news-center/article-details/why-weight-loss-is-hard-metabolism-sleep-stress-and-hormones |
| 6 | Ubie Health | Health platform | https://ubiehealth.com/doctors-note/weight-loss-science-caloric-deficit-metabo-macro-71e10 |
| 7 | Sezarro Overseas | Health & Wellness | https://sezarroverseas.com/weight-loss-science-2025-evidence-based-strategies/ |
| 8 | Apollo Pharmacy | Health media | https://www.apollopharmacy.in/blog/article/strength-training-or-cardio-exercise-which |
| 9 | &you Digital Wellness | Wellness platform | https://andyou.ph/blogs/weight-loss/the-impact-of-sleep-and-stress-on-weight-loss-results |
| 10 | News Medical | Medical news | https://www.news-medical.net/health/The-Science-Behind-Sustainable-Weight-Loss-and-Weight-Maintenance.aspx |

---

## Chunking Strategy

**Chunk size:** 500 words

**Overlap:** 100 words

**Why these choices fit your documents:**
The source documents are long-form educational articles that each cover multiple
subtopics such as calorie deficits, protein intake, metabolism, sleep, and
exercise. A chunk size of 500 words preserves enough context for the retrieval
system to understand complete concepts without diluting the semantic signal. A
100-word overlap prevents important information from being split across chunk
boundaries — for example, a key fact about protein intake that spans two adjacent
paragraphs will appear fully in at least one chunk. Fixed-size chunking was also
chosen because it is computationally efficient and straightforward to implement
and verify. Before chunking, documents were preprocessed by collapsing all
whitespace and newlines into single spaces to ensure consistent word splitting.

**Final chunk count:** 28 chunks across 10 documents

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API
key required, no rate limits)

**Production tradeoff reflection:**
For a production deployment serving real users, I would consider switching to a
larger model such as text-embedding-3-large (OpenAI) or embed-english-v3.0
(Cohere). The tradeoffs I would weigh are accuracy on domain-specific text —
all-MiniLM-L6-v2 is general-purpose and may not fully understand health-specific
terms like "adaptive thermogenesis" or "GLP-1 agonists," whereas a domain-tuned
model would return more precise results. Context length is also a concern —
all-MiniLM-L6-v2 supports only 256 tokens, meaning longer chunks may be
truncated during embedding and lose information. A model with a longer context
window (such as text-embedding-3-large at 8,191 tokens) would handle larger
chunks without truncation. On latency, the local model adds no network cost but
cloud-hosted models offer higher accuracy at the cost of API latency and per-call
pricing. Finally, the current model is English-only — a multilingual model such
as paraphrase-multilingual-MiniLM-L12-v2 would be needed if the system needed to
serve non-English speakers.

---

## Grounded Generation

**System prompt grounding instruction:**
The following instruction is passed to the LLM in generate.py on every query:

"You are a helpful weight loss assistant. Answer the user's question using ONLY
the context provided below. Always cite your sources by name (e.g. 'According to
Cleveland Clinic...'). If the context does not contain enough information to
answer the question, say 'I don't have enough information on that topic in my
knowledge base.'"

The retrieved chunks are formatted and labeled before being passed to the model:

"[Source 1: Cleveland Clinic]
{chunk text}

[Source 2: Ubie Health]
{chunk text}"

This labeling makes it easy for the model to cite sources by name in its response.

**How source attribution is surfaced in the response:**
Source attribution is enforced in two ways. First, the system prompt explicitly
instructs the model to cite sources by name in every answer using the format
"According to [Source]...". Second, app.py programmatically extracts the source
name and URL from each retrieved chunk's metadata and displays them in a separate
Sources box below the answer, regardless of what the model produces. This ensures
citations are always visible even if the model omits them in the answer text.
Additionally, app.py implements a keyword filter that blocks out-of-scope queries
before they reach the LLM, returning a refusal message directly.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What is a calorie deficit and why is it important for weight loss? | A calorie deficit occurs when a person consumes fewer calories than they burn. It is the fundamental requirement for weight loss. | Correctly defined calorie deficit and cited Ubie Health, Cleveland Clinic, and Sezarro Overseas. Explained the body uses stored fat to make up the energy difference. | Relevant | Accurate |
| 2 | How much weight loss per week is generally considered safe and sustainable? | Approximately 1–2 pounds per week through a moderate calorie deficit and healthy lifestyle changes. | Cited Cleveland Clinic (1 lb/week from 500-cal deficit) and Sezarro Overseas (no more than 2 lbs/week). Correctly identified 1–1.5 lbs/week as the sustainable target. | Relevant | Accurate |
| 3 | Why is protein important during weight loss? | Protein helps preserve muscle mass, increases satiety, and increases calorie burn through digestion. | Cited Sezarro Overseas and Ubie Health covering thermic effect of food, satiety hormone increases, ghrelin reduction, and muscle preservation. | Partially relevant | Accurate |
| 4 | How does sleep affect weight loss? | Poor sleep increases hunger hormones, decreases fullness signals, lowers metabolism, and increases cravings. | Cited &you and Sleep Foundation. Covered ghrelin and leptin disruption, insulin sensitivity, cortisol, and the 7–9 hour recommendation. | Relevant | Accurate |
| 5 | What causes a weight loss plateau and how can it be overcome? | Plateaus occur due to metabolic adaptation, calorie creep, and reduced activity. Adjust nutrition, activity, and sleep. | Cited Ubie Health, Healthline, and Sezarro. Covered metabolic adaptation, diet breaks, stress management, and sustainable rate of loss. | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:**
"Why is protein important during weight loss?"

**What the system returned:**
The system returned a chunk from article8.txt (Apollo Pharmacy — cardio vs.
strength training) as one of the top-3 retrieved results. While the answer was
still accurate because the other two chunks covered protein well, one of the three
retrieved chunks was not primarily about protein.

**Root cause (tied to a specific pipeline stage):**
The root cause is in the embedding stage. The all-MiniLM-L6-v2 model has a
maximum context length of 256 tokens. The article8.txt chunks are derived from
500-word chunks, which exceed this limit and get truncated during embedding. The
truncated embedding carries less semantic signal and becomes more generic — it
matched the query on surface-level terms like "muscle" and "weight loss" rather
than the specific concept of protein's thermic effect and satiety benefits. This
is a retrieval failure caused by embedding truncation at Stage 3.

**What you would change to fix it:**
Reduce chunk size to 200–250 words to stay within the 256-token context limit of
all-MiniLM-L6-v2, or switch to an embedding model with a longer context window
such as text-embedding-3-large. Either change would produce more accurate
embeddings and reduce off-topic retrieval.

---

## Spec Reflection

**One way the spec helped you during implementation:**
Writing the chunking strategy in planning.md before coding forced a deliberate
decision about chunk size and overlap before any code was written. When the
overlap verification check initially failed during Milestone 3, having the spec
as a reference made it clear that the chunking logic itself was correct — the
issue was that the test was comparing chunks from two different documents (article1
is only 445 words and produces a single chunk). The spec prevented unnecessary
changes to working code by providing a clear standard to check against.

**One way your implementation diverged from the spec, and why:**
The spec and AI Tool Plan both specified using the Anthropic Claude API for Stage
5 generation. The actual implementation used the Groq API with
llama-3.3-70b-versatile instead. This change was made because a Groq API key was
already configured in the project's .env file and Groq's free tier has no usage
limits or credit requirements. The grounding prompt structure, source citation
format, and overall generation logic remained identical to what the spec described
— only the API client and model name changed.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* My planning.md Documents section, Chunking Strategy
  section, Architecture diagram, and the .txt file header format (SOURCE URL,
  TITLE, SOURCE). I asked Claude to implement load_documents() and chunk_text()
  matching my spec.
- *What it produced:* A working ingestion script with both functions. However,
  chunk_text() returned a list of plain text strings with no metadata attached —
  just the raw chunk text, no source, URL, or filename.
- *What I changed or overrode:* I identified the missing metadata issue and
  directed Claude to add a metadata parameter to chunk_text() and wrap each chunk
  in a dict containing text, source, url, filename, and chunk_index. I also
  identified and corrected an indentation error in the generated code where the
  body assignment was placed outside the for loop.

**Instance 2**

- *What I gave the AI:* The failing overlap verification output showing FAIL and
  an explanation that article1.txt is only 445 words and produces a single chunk,
  meaning chunk 0 and chunk 1 were from two different documents.
- *What it produced:* A fix that changed the verification check to filter for
  chunks from article7.txt (the longest article at 1,730 words, guaranteed to
  produce multiple chunks) before comparing overlap.
- *What I changed or overrode:* I verified the fix was logically correct before
  applying it — confirming that article7.txt would always produce at least 2
  chunks at a 500-word chunk size, making the overlap test valid. I also confirmed
  the rest of the verification block (key checks, word count) remained unchanged.

**Instance 3**

- *What I gave the AI:* The Groq API error message showing that llama3-8b-8192
  had been decommissioned, along with the generate.py file.
- *What it produced:* A one-line fix replacing the model name with
  llama-3.3-70b-versatile.
- *What I changed or overrode:* I verified the new model name was current and
  available on Groq's free tier before applying the change. I also confirmed the
  rest of the API call structure (temperature, max_tokens, message format)
  remained valid for the new model.
