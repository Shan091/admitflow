# Institution document ingestion

Authenticated institution staff can upload individual files or a folder containing
digital PDFs, DOCX and UTF-8 text. Each file has an encrypted durable upload record;
only a successfully completed current attempt publishes searchable document chunks.
Tenant authorization, duplicate detection, retry and deletion apply to every format.

## PDF setup and worker

From `backend/`, install the locked dependencies and public layout/table weights:

```bash
uv sync --frozen
uv run python -m src.scripts.prepare_document_models
uv run taskiq worker src.tasks.knowledge:broker src.tasks.knowledge --workers 1 --max-async-tasks 1
```

Run the API and interactive worker separately as documented in
[LOCAL_RUNTIME.md](LOCAL_RUNTIME.md). The API publishes ingestion jobs to Redis list
`admitflow-knowledge`; the interactive queue remains `taskiq`. Existing queued uploads
are recovered from their database records. Start the knowledge worker before accepting
new uploads; a stopped worker leaves queued records recoverable. Do not run ingestion
with unconstrained worker concurrency. Roll back the API and workers together; pending
records can be redispatched by the version's normal recovery loop.

The preparation command downloads only pretrained CPU layout and TableFormer assets,
about 669 MiB for the current versions, and writes an asset inventory. It receives no
institution document. Docling's required conversion, local-model and PDF extras plus
headless OpenCV are locked; CUDA, OCR and additional decision providers are unnecessary.
The Compose backend image includes these assets at `/opt/admitflow/document-models`.
Native assets default to ignored `backend/.runtime/document-models` and can be moved
using `DOCUMENT_MODELS_PATH`. Keep the inventory with the model files when moving them.

## Processing and evidence

Each PDF runs in a single-use child process, with provider credentials excluded from
its environment and Hugging Face offline mode enabled. It preflights native text,
passwords, page count and page dimensions, then Docling reconstructs reading order,
tables and heading hierarchy. All content layers, including footers and caveats, are
exported to Markdown. Scanned/blank pages fail explicitly; OCR is outside this version.
DOCX extraction preserves paragraph/table order and heading styles.

The semantic chunker repeats ancestor headings, splits prose at available boundaries,
and splits tables between complete rows with repeated column headers. A table row or
heading context too large for a chunk fails rather than silently losing associations.
OpenAI embeds the resulting chunks; existing tenant/course filters and OpenAI reranking
apply at search time. These local pretrained parsing models do not train or replace
the OpenAI decision layer.

Defaults: 10 MiB/file, 25 files/30 MiB per batch, 100 PDF pages, 400,000 extracted
characters, 500 chunks, 120 seconds/PDF child and 2 GiB child resident memory.
`DOCUMENT_PARSE_TIMEOUT_SECONDS` and `DOCUMENT_PARSE_MAX_MEMORY_MB` configure bounded
limits; total ingestion has its own 180-second deadline. Cancellation, timeout and
memory exhaustion kill and reap the child before its processing slot is released.
The dedicated worker claims one upload at a time, so waiting folder files remain queued.
The child boundary controls resource use and credentials; it is not an OS security sandbox.

Malformed, encrypted, unsupported, oversized and scanned inputs receive safe error
codes. Missing assets produce `parser_not_ready`. Partial conversion produces
`layout_incomplete`; resource limits and oversized structure produce explicit errors.
No raw parser output or document text is included in a public failure message.

## Verification

```bash
uv run pytest tests/test_structured_documents.py tests/test_pdf_parser_boundary.py tests/test_knowledge_queue.py
uv run pytest -m integration tests/integration/test_knowledge_workspace.py
uv run python scripts/verify_compose.py
# Bounded paid OpenAI check against the local synthetic demo; removes its own upload:
uv run python scripts/verify_document_pipeline.py
```

The real complex-PDF integration case runs only when local assets are prepared; it
must pass, rather than skip, to establish layout acceptance. Its committed synthetic
two-page fixture has two columns, two programmes, tuition/hostel/library tables and
fee caveats. PostgreSQL acceptance exercises authenticated upload, the real offline
parser, fake embeddings and atomic publication. Other database tests use a lightweight
PDF stub to isolate authorization/transaction behavior; they do not establish layout
quality. The fixture's rendered pages are inspected separately. Automated checks cover
row/amount associations, heading ancestry, column text, caveats and sibling separation.
This is bounded fixture evidence, not a guarantee for every possible PDF layout.
