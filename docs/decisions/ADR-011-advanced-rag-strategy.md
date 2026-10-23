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

Digital PDF, DOCX and text ingestion remains supported. Complex table/layout parsing,
semantic chunking and full conversational rewriting remain separate tasks. Existing
bounded non-ASCII query translation remains in place. The active candidate search is
pgvector similarity; the compatibility hybrid-search helper is not this runtime path.

## Verification and tradeoffs

Unit checks cover ranking order, original-source preservation, tenant/injection
filtering and invalid/outage fallback. PostgreSQL document and journey checks verify
integration. Synthetic live multilingual ranking/FAQ reports are kept in docs/event.
This adds model-call cost and latency. No fixed latency or broad accuracy claim is
made; baseline fallback protects availability, not equivalent ranking quality.
