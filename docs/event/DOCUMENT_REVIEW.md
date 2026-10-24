# Structured-document review

The primary agent performed the adversarial pass against Task 42.1, focusing on
untrusted uploads, tenant authority, process lifetime, numerical/source fidelity and
interactive-worker availability.

- Upload authorization, encryption and atomic attempt/tenant publication remain in
  the existing durable path; the parser receives raw bytes without a filename or
  application/provider credentials. Native-text preflight rejects scans and bounds
  pages, dimensions, decompressed streams and extracted text.
- Layout parsing uses offline assets, no OCR/remote inference/plugins, accurate table
  reconstruction and heading hierarchy. All content layers retain document caveats.
- Oversized table rows fail explicitly; row splits repeat headers and ancestor
  headings. Sibling programme contamination and amount associations are tested.
- Cancellation and resource limits terminate descendants as well as the Python
  launcher. Review found that Windows venv redirectors needed this treatment; it was
  fixed, tested with child RSS and confirmed against real Windows processes.
- Dedicated serial Redis ingestion prevents folder wait time from consuming claimed
  jobs' processing deadlines or interactive Telegram worker capacity. Pending and
  abandoned jobs remain recoverable through the database inbox.
- The real fixture was rendered and both pages visually inspected. PostgreSQL tests
  exercise real Docling publication; ordinary isolated tests do not claim model quality.
- Staged credentials/private-key scan has no findings. Models, runtime files and
  configuration secrets are excluded from Git and Docker contexts as applicable.

No open Critical or Important finding remains for the reviewed code. Default gate:
251 tests, 117 strictly typed source files. PostgreSQL: 87 passed, including the actual
model fixture. Redis: 2 passed. Frontend lint/build pass. Live OpenAI structured output,
1536-dimensional embeddings and read-only Telegram bot identity checks pass. Live
PDF queue/index/search checks pass and remove their temporary synthetic upload.
The final Linux image passes bounded parsing with networking disabled; nine current
Compose smoke checks pass, including the dedicated worker. The preceding ten-check
restart run confirmed credential persistence. CI exposed a platform-specific typing
issue in the Windows process flag; an explicit guard fixes Linux typing without
changing execution behavior. The final PR gate remains separate; this review does not establish a public
release, payment-card journey, handset receipt or general PDF extraction accuracy.
