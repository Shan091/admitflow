# AdmitFlow: current state and planning baseline

This is the starting source/document audit. New implementation evidence is recorded in tasks/todo.md.
Read before rewriting [the implementation plan](../../tasks/plan.md) or
[the task list](../../tasks/todo.md).

## Confirmed user direction

- Continue in this repository and preserve existing changes/deletions.
- Use **Telegram as the active student channel**, replacing WhatsApp for the
  current build. Telegram is no longer merely a suggested fallback.
- Use **OpenAI as the AI provider**. Neysa and other sponsor resources are optional
  and should be used only if necessary. A provider comparison is not a requirement.
- Explain the current approach, stack, implemented behavior and gaps before
  finalizing features and rewriting the plan/task list.
- Retain the full institutional product roadmap. Separate a demonstrable milestone
  from later releases without silently deleting the broader product scope.

These decisions supersede older active-planning references to WhatsApp as the
required current channel, Gemini-first inference, or mandatory Neysa experiments.
Historical readiness evidence and existing WhatsApp code should remain intact.

## What the existing approach does

The implemented entry path is Meta webhook -> Redis/TaskIQ -> Python dispatcher ->
WhatsApp sender. The dispatcher resolves the institution from Meta's phone-number
ID and the lead from a normalized phone number. It stores the inbound message,
loads conversation history/facts, runs input checks and intent classification,
then calls discovery, retrieval, qualification or a basic handoff branch.

The intended design is sound in its main boundaries: PostgreSQL holds persistent
state; each message reloads that state; AI interprets language and drafts replies;
code owns eligibility, prices and consequential transitions. The staff dashboard
would consume the same data. A separate autonomous-agent framework is unnecessary
for this turn-by-turn interaction.

However, several descriptions in SPEC/tasks state intended behavior more strongly
than the current implementation or tests establish.

## Stack inventory

| Area | Present in the repository | Status/implication |
| --- | --- | --- |
| Backend | Python >=3.12, uv, FastAPI, Uvicorn, Pydantic | Existing application foundation; observed local interpreter in prior checks is newer than the declared minimum |
| Database | SQLAlchemy async, Alembic, asyncpg, PostgreSQL models | Models and migrations exist; prior local migration/seed evidence exists |
| Background processing | TaskIQ and Redis; mutex/dedup helpers | Existing code; prior real-Redis worker smoke/regression evidence exists |
| Student channel | Meta WhatsApp webhook and sender | Implemented transport code; actual delivery remained blocked; no Telegram source found |
| AI calls | LiteLLM completion wrapper with configurable model roles/fallbacks | Can target OpenAI; default settings still name Gemini, while ignored local config was previously set to OpenAI; secrets were not inspected for this audit |
| Knowledge retrieval | pgvector, embeddings, dense/English lexical rank fusion, simple text chunking | Core code exists; no complete document-management product or calibrated relevance gate |
| Business rules | Python qualification-rule evaluator and lifecycle transitions | Implemented; integration, typed-value validation and correction behavior need work |
| Data protection | Fernet encryption helpers, keyed phone lookup, audit utility | Building blocks exist; full PII handling, authorization, tenant isolation and deletion/retention are not established by their presence |
| Staff frontend | Next.js/Tailwind described in the plan | No frontend application found; no implemented login, CRM or staff management API |
| Payments | Application/payment/discount database models | No implemented Razorpay service or payment journey found |
| Observability | Python logging; Langfuse/Sentry described in roadmap | Langfuse/Sentry integration not found |
| Deployment | Backend Dockerfile, CI quality gate, local readiness Compose | Prior Fly.io/Vercel/Neon/R2 choices are plans, not deployment evidence |

Source locations: [dependencies](../../backend/pyproject.toml),
[settings](../../backend/src/core/settings.py),
[app routes](../../backend/src/main.py),
[dispatcher](../../backend/src/engine/dispatcher.py),
[database models](../../backend/src/db/models),
[earlier stack decision](../decisions/ADR-007-finalized-stack.md).

## Feature status and integration gaps

| Feature | Actual state |
| --- | --- |
| Course browsing | Queries active courses/batches with seats and renders WhatsApp buttons/lists; does not complete the selection loop |
| Course/batch selection | Dispatcher reads text only; no interactive callback branch sets the selected course/batch |
| Conversation history | Inbound messages are inserted; history query loads oldest 20, and normal outbound replies are not persisted |
| Student facts | Facts are loaded/upserted; qualification extracts missing fields; general memory and corrections are not complete |
| Eligibility | Code evaluates rule operators; selected course, validating extracted values, corrections and reliable state transitions need integration |
| Knowledge answers | Retrieval and generation exist; no confidence threshold is actually enforced; lexical search is English-specific |
| Output safety | Classifier helper and mocked tests exist, but it is not called by the active dispatcher/RAG send path |
| Human handoff | Sets a status and sends a promise of counselor contact; no verified staff inbox, assignment, notification or response path |
| Co-pilot | A flag exists; no implemented behavior that suppresses bot replies and offers staff-only suggestions |
| Readiness-aware decisions | Status enum and readiness database field exist; planned `decide()`/calibrated readiness layer is absent |
| Applications/payments | Data models exist; collection, validation, review and payment orchestration remain unbuilt |
| Staff operations | Authentication, leads UI, conversation view, course/rule editor, uploads, exports and analytics remain unbuilt |
| Multi-tenancy | Tenant fields and some tenant-filtered queries exist; full end-to-end isolation/authorization is not proven |
| Multilingual support | Product intention; no demonstrated language selection/localized flow or evaluation establishing all promised languages |
| Telegram | No bot adapter, sender, identity mapping or live journey established |

Additional reliability findings relevant to the plan:

- The webhook acknowledges some queue/dedup exceptions with HTTP 200, potentially
  losing work. Acceptance criteria must distinguish receipt from durable enqueue.
- A send can happen before database commit; retries, outbound state and duplicate
  effects need an explicit design rather than an exactly-once claim.
- Several handlers swallow invalid-transition exceptions and still send success
  messages. User-visible outcomes must agree with persisted state.
- The qualification extractor only runs for missing fields, so correcting an
  already-known value needs explicit handling.
- Triage sees only the incoming text, rather than the active question/state. A
  short answer such as a number needs conversation-aware routing.

Key sources: [discovery](../../backend/src/engine/nodes/discovery.py),
[qualification](../../backend/src/engine/nodes/qualification.py),
[triage](../../backend/src/engine/nodes/triage.py),
[retrieval](../../backend/src/core/rag.py),
[RAG replies](../../backend/src/engine/nodes/rag.py),
[guardrails](../../backend/src/engine/nodes/guardrails.py),
[webhook](../../backend/src/whatsapp/webhook.py).

## Verification evidence and its limits

The last recorded default gate passed 114 tests, with five integration tests
deselected and two existing RAG AsyncMock warnings. A real-Redis idle-worker
regression and separate worker ping were also recorded. These are historical
results in [READINESS_CHECK.md](READINESS_CHECK.md), not results rerun for this audit.

The latest [Postman check](POSTMAN_CHECK.md) records HTTP acceptance followed by
Meta delivery failure 131031. No successful phone-to-engine-to-phone learner
journey was established. Telegram has not been verified either.

The dispatcher test mocks the database, Redis, sender and discovery handler. The
discovery integration test checks menu presentation, not a tap selecting a course.
The RAG tests mock retrieval/model output. Passing these tests does not establish
the complete product journey or advertised retrieval/language quality.

The knowledge graph CLI still fails with a missing `graphify` module. Its existing
JSON graph was traversed as historical navigation, then checked against source.
Graph facts cannot establish runtime readiness.

## Proposed architecture for the next plan

Telegram private chat -> Telegram adapter -> normalized inbound event -> existing
TaskIQ/Redis worker -> conversation engine -> validated reply -> Telegram sender.
PostgreSQL stores leads, both directions of messages, facts, courses and knowledge.
A Next.js staff application reads/writes through authenticated FastAPI endpoints.
OpenAI provides language interpretation, grounded generation and embeddings.

Keep the existing Python/data/worker foundation. Use the existing LLM wrapper with
OpenAI-only configuration initially; swapping to the direct OpenAI SDK is a
separate simplification decision, not necessary for the channel migration. Keep
model IDs in configuration and evaluate the selected model on actual cases.

Telegram work is more than a new send URL:

1. Add trusted bot-to-institution routing and a tenant-scoped channel identity for
   Telegram user/chat IDs; make phone contact optional rather than fabricating one.
2. Normalize text, `/start` and button callbacks into engine events; separate reply
   content from channel-specific rendering/sending.
3. Persist inbound/outbound IDs and processing/send status with scoped dedup keys;
   lock processing per tenant/bot/conversation.
4. Validate callback ownership and course availability, acknowledge callbacks,
   and reject stale or cross-tenant selections.
5. Choose one receiving mode for a running bot. Long polling can simplify local
   development; a hosted webhook requires HTTPS and secret-token validation.
   Polling offsets must advance only after durable acceptance.
6. Restrict the first journey to private chats; handle unsupported content and
   failures explicitly. A Telegram ID is not a verified phone number or identity.

See [Telegram Bot API](https://core.telegram.org/bots/api) for receiving modes,
identifiers and callbacks. Telegram Bot API calls can use the existing HTTP client;
a new bot framework is not required for the initial adapter.

OpenAI structured outputs help constrain extraction format; values still need
domain validation. See [official guidance](https://developers.openai.com/api/docs/guides/structured-outputs).

## Features to finalize next

Proposed first complete milestone: Telegram onboarding, course/batch selection,
short adaptive qualification questions, reliable memory/corrections, approved
knowledge answers with abstention, persisted inquiry, minimal authenticated staff
lead/conversation view, and honest human-request handling.

Keep the broader roadmap for application forms, application review, Razorpay,
co-pilot, follow-ups, catalog/document management, analytics/exports and production
hardening. Decide which belong in the first usable release versus later phases;
do not mark them removed or completed based on this proposal.

Neysa, SerpAPI, self-hosted models, distillation, external rerankers, LangGraph and
additional AI providers are unnecessary for this first proposed milestone.
Langfuse/Sentry can be evaluated later; basic sanitized logs and request/error/
latency/usage evidence are needed from the beginning. Hosting remains to be chosen
against actual runtime, persistence and budget needs; no new service was provisioned.

## How to reconcile the planning documents

1. Finalize product scope, student/staff journeys and release acceptance criteria.
2. Update SPEC with Telegram, OpenAI, identity/data flow and truthful feature scope.
3. Record the channel/provider decision in an ADR, superseding only affected parts
   of previous decisions; preserve historical ADRs and evidence.
4. Rewrite plan.md into ordered, complete milestones with explicit dependencies.
5. Reconcile todo.md task by task: preserve IDs/history; distinguish implemented
   modules, unfinished integration, verified journeys and deferred work.
6. Update event submission/resource documents and backend README to match.

Plan.md currently marks schema/security work incomplete where todo.md marks it
complete, and both contain stronger messaging/guardrail claims than current live
evidence supports. Resolve those differences explicitly. Avoid a global rename of
WhatsApp or blanket resetting all task checkboxes.
