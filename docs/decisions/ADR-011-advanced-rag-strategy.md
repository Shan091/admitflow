# ADR-011: Required OpenAI passage reranking

Status: Accepted; revised by user decision. Reranking is current release scope.

## Decision

Use the existing OpenAI provider configuration to rerank evidence in active Telegram
FAQ answers and authenticated staff document search. No extra API vendor, local
cross-encoder, model training or serving infrastructure is required.

Retrieve at most 12 candidates from approved, ready uploads in the requesting tenant
with the configured embedding model. Preserve the existing similarity floor and
injection filter before ranking. Send only bounded question/reference text, never the
applicant profile or conversation history. Zero or one candidate needs no ranking call.

The structured output must be a complete permutation of supplied candidate IDs.
Reject duplicates, missing IDs and invented IDs. Return original database objects,
preserving text, source paths and chunk references; select the top five.

An additional configurable timeout bounds the ranking operation across provider
retries. Refusal, timeout, provider error and invalid output retain the safe baseline
retrieval order. Logs record outcome/count only. Ranking does not establish support:
FAQ answers still require an exact quotation from a supplied source or abstain.

## Separate retrieval work

Digital PDF, DOCX and text ingestion remains supported. Complex table/layout parsing
and semantic chunking remain Task 42.1. Task 42.2 now resolves follow-ups through typed
OpenAI decisions over six bounded recent completed/sent turns. Uncertain references
ask for clarification. Standalone questions retain bounded non-ASCII translation and
the ASCII fast path. Numeric rewrites are compared by normalized decimal value.

Administrators can mark an indexed document as shared or assign it to a tenant-owned
course. Student retrieval includes shared references plus explicitly named active
catalog courses, falling back to the selected course. With no course, only shared
references are eligible. Staff can explicitly filter by course. These metadata
filters run before candidate ranking; model output never supplies authoritative IDs.
Application/registration fees use matching database course rows, including explicit
questions about a different course, without altering the student selection.

The active candidate search is pgvector similarity; the compatibility hybrid-search
helper is not this runtime path.

## Verification and tradeoffs

Unit checks cover ranking order, original-source preservation, tenant/injection
filtering and invalid/outage fallback. PostgreSQL document and journey checks verify
integration. Synthetic live multilingual ranking/FAQ reports are kept in docs/event.
This adds model-call cost and latency. No fixed latency or broad accuracy claim is
made; baseline fallback protects availability, not equivalent ranking quality.
