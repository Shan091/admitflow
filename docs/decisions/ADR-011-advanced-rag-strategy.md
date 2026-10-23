# ADR-011: Advanced RAG Strategy (Latency vs Precision)

**Status:** Accepted

## Context
AdmitFlow utilizes a RAG (Retrieval-Augmented Generation) pipeline to answer complex knowledge questions from institution documents. The baseline pipeline (Task 13) implemented a pgvector HNSW index with hybrid search + Reciprocal Rank Fusion (RRF). 

However, standard RAG has three critical blindspots for a WhatsApp admissions bot:
1. **Latency Sensitivity:** WhatsApp users expect near-instant responses. A heavy local cross-encoder for reranking would add 500ms to 2.5s of latency per turn, risking race conditions and degraded UX.
2. **Complex Document Formatting:** Institutions upload PDFs heavily formatted with tables, multi-column layouts, and bulleted lists. A naive sliding-window text chunker destroys this structural context.
3. **Conversational Drift & Slang:** WhatsApp queries are often informal ("fee 4 btech?") or rely on conversational memory ("what about hostel?"), making dense vector similarity matching highly erratic without query resolution.

## Decision
We are upgrading to an "Advanced RAG" pipeline governed by strict latency budgets and structural awareness.

### 1. Complex Document Ingestion (`docling` or `unstructured`)
Instead of directly extracting raw text and applying a sliding window, we will integrate a specialized document parsing library (`docling` or `unstructured`).
- **Action:** Documents will be converted to structured Markdown.
- **Chunking:** We will use semantic chunking (e.g., splitting by Markdown headers) to retain parent-child context. Tables will be preserved in Markdown format.

### 2. Pluggable Reranking Architecture (Cohere API over Local CPU)
To achieve state-of-the-art precision without breaking the per-turn latency budget on our self-hosted CPU infrastructure:
- **Production:** We will integrate the Cohere Rerank API via LiteLLM. It offloads compute and only incurs a ~150-300ms network roundtrip penalty.
- **Development/Testing:** A lightweight local model (e.g., `cross-encoder/ms-marco-MiniLM-L-2-v2`) or a no-op passthrough will be used to keep local testing fast and free.

### 3. Contextual Query Rewriting
Before executing the hybrid search, the user's raw WhatsApp message will be passed through the fast Gemini Flash model to rewrite it into a well-formed query, resolving pronouns and slang based on conversational history.

## Consequences

**Positive:**
- Complex tables and layouts in institution PDFs survive the chunking process.
- High precision retrieval via Cohere Reranker without massive local compute requirements.
- WhatsApp slang and fragmented follow-ups are successfully matched against formal PDFs.
- Latency is carefully managed.

**Negative:**
- `docling` / `unstructured` adds ingestion time complexity and memory overhead to the background TaskIQ worker (though it doesn't affect user latency).
- Cohere API introduces a vendor dependency and marginal per-query cost (vs. a purely self-hosted approach).
