# ADR-012: Telegram and OpenAI for the first complete admissions MVP

Status: Accepted; core implementation and local/live checks complete. Release and extended device/language acceptance remain tracked in tasks/todo.md.

## Context

The user selected Telegram instead of WhatsApp and OpenAI as the AI provider, with
only necessary services. The existing backend has reusable data/queue/engine modules,
but no verified complete admissions journey or staff dashboard. Meta delivery remains
historically blocked. The user approved a first release covering a Telegram inquiry
and a minimal staff workflow while retaining the full institutional roadmap.

## Decision

1. Use Telegram private chats, manually provisioned one bot per institution. Add
   explicit channel identities and trusted bot-to-tenant mapping; phone contact is
   optional. Preserve existing WhatsApp rows/code/evidence without claiming migration.
2. Use long polling for the initial local/event receiver. Durable intake and startup
   recovery protect accepted work before advancing offsets. A hosted webhook is an
   alternative requiring authenticated HTTPS and the same durable acceptance contract.
3. Normalize inbound events and route all replies through a validation/persistence/
   transport boundary. Handlers should not construct a WhatsApp sender directly.
4. Keep FastAPI, PostgreSQL/pgvector, SQLAlchemy/Alembic, Redis/TaskIQ and the plain async
   dispatcher. Keep the current AI wrapper with OpenAI-only configuration initially.
   Do not add a graph framework or change SDK merely for the channel migration.
5. Use OpenAI for language interpretation, typed extraction, grounded answers and
   embeddings. Keep configured model IDs and bounded timeouts/retries. Explicit code
   owns prices, eligibility, authorization and consequential changes. Preserve state
   and give safe failure behavior when OpenAI is unavailable.
6. Build a minimal Next.js/TypeScript/Tailwind staff surface over authenticated Python
   APIs. Login, leads, conversation/eligibility detail and human-request controls are
   in scope; broad CRUD, analytics, applications/payments and co-pilot are later work.
7. Use correlated redacted telemetry for model role, usage, latency and errors from
   the start. Langfuse and Sentry are optional implementations; no external telemetry
   vendor or raw-prompt logging is required for this MVP. Keep security/audit controls.
8. Use OpenAI itself for typed decisions and required passage reranking. No fine-tuning,
   distillation or self-hosted decision model is planned. Neysa, SerpAPI, Gemini/Anthropic
   fallback and external reranker services are not dependencies. Hosting is verified
   at release planning rather than inferred from credits or prior design documents.

## Supersession and preserved decisions

For this first release, this ADR supersedes WhatsApp-specific ingress/identity/sender
assumptions in ADR-001/002/003/007; the Gemini-first/multi-provider/self-hosted mandates
in ADR-007/008; and vendor-specific observability requirements. The corresponding
historical engineering text remains context, not an instruction to add unused services.
ADR-004 persistence, ADR-005 three-layer validation, ADR-006 code-owned decisions and
ADR-009 PII/audit principles remain applicable. ADR-010's anti-spam intent remains;
current-state-aware handling takes precedence over resetting every unknown reply to
discovery. ADR-008 and ADR-011 now reflect the required OpenAI decision/reranking path. Complex
parsing and full conversational rewriting remain separately tracked; reranking does
not depend on either.

## Consequences

The first release avoids Meta reinstatement as a dependency, but must implement a new
adapter, identity migration and live verification. Telegram IDs are not phone numbers
or verified identities. OpenAI-only operation trades cross-provider fallback for less
configuration and requires graceful outages. Polling requires a running single receiver
per bot and durable offsets; it does not imply zero operational requirements.

Staff human-request acknowledgment/resolution is distinct from live takeover. The
first release must communicate this truthfully. The selected languages and any AI
quality claims remain subject to evaluation and fluent-speaker review.

## References and verification

- [Active specification](../../SPEC.md), [plan](../../tasks/plan.md), [tasks](../../tasks/todo.md).
- [Current source audit](../event/CURRENT_STATE.md) and [historical baseline](../planning/archive/2026-10-23-before-telegram-alignment/README.md).
- [Telegram Bot API](https://core.telegram.org/bots/api): receiving modes, identifiers and callbacks.
- [OpenAI structured outputs](https://developers.openai.com/api/docs/guides/structured-outputs): structured output is not factual validation.

No new API calls, bot provisioning, credits, deployment or product readiness is
established by accepting this decision. Tasks 43-60 define implementation evidence.
## Implemented runtime boundaries

Telegram uses its own encrypted event inbox, reply outbox and conversation memory;
the historical WhatsApp dispatcher remains compatibility code. An institution-owned
bot and scoped identity resolve tenant/lead authority. The poller commits accepted
events and its checkpoint together and holds one PostgreSQL advisory receiver lock.
Workers serialize on the tenant-owned lead row, then atomically commit memory and a
validated reply. The reply outbox preserves conversation send order, records uncertain
delivery, and never blindly retries an ambiguous send. Redis/TaskIQ transports jobs;
database recovery makes publication failures recoverable.

Staff use opaque hashed server-side sessions. Inquiry/detail/history and human-request
actions derive tenant authority from those sessions. Conversation facts and messages
remain encrypted at rest in application storage. Approved reference text is separate
from applicant data and remains tenant scoped. The active AI path is OpenAI only.
Non-ASCII document queries use bounded translation while preserving the relevance
floor; quoted answers must match an approved source passage exactly.
