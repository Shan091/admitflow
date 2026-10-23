# AdmitFlow — Task List

## Current direction and hackathon resources (2026-10-23)

The user selected this AdmitFlow repository and its **full institutional MVP roadmap**.
Preserve all tasks and existing completion evidence. Keep active planning self-contained.
See [EVENT_CONTEXT.md](../EVENT_CONTEXT.md) and the
[resource plan](../docs/event/RESOURCE_PLAN.md) before starting implementation.

- [ ] Record and verify hackathon credit activation, eligible services, quotas, expiry and
  post-credit costs. No grant redemption, spending or cloud provisioning is authorized by a
  planning checklist alone.
- [ ] Select a bounded event milestone from the full roadmap after confirming prior-work
  disclosure and the announced surprise requirement. Define acceptance and verification first.
- [ ] Prioritize resources that improve the admissions journey: structured extraction and
  evaluation, supported hosting, approved institution knowledge and pilot/mentor feedback.

---

## Phase 1: Foundation

### Task 1: Initialize Python project, FastAPI, settings, and Docker
**Description:** Create the `backend/` directory, `requirements.txt`, FastAPI app entry, settings singleton, and Dockerfile.
**Acceptance criteria:**
- [x] FastAPI boots on localhost:8000
- [x] `/docs` shows Swagger UI
- [x] Settings loaded from `.env`
**Verification:** `uvicorn src.main:app --reload` starts successfully
**Dependencies:** None
**Estimated scope:** Small

### Task 2: PostgreSQL schema (SQLAlchemy + Alembic)
**Description:** Define all core SQLAlchemy models: Institution, StaffUser, Course, Batch, QualificationRule, DiscountCode, Lead, LeadFact, Message, Application, PaymentOrder, AuditLog. Every table has `tenant_id`.
**Acceptance criteria:**
- [x] All models defined with proper relationships
- [x] Alembic migration runs cleanly
- [x] `tenant_id` on every tenant-scoped table
**Verification:** `alembic upgrade head` succeeds
**Dependencies:** Task 1
**Estimated scope:** Large

### Task 3: TaskIQ + Redis broker setup
**Description:** Configure TaskIQ with Redis as the message broker for background processing.
**Acceptance criteria:**
- [x] TaskIQ broker boots successfully
- [x] A dummy task can be enqueued and processed
**Verification:** Trigger a test task from a `/debug` endpoint
**Dependencies:** Task 1
**Estimated scope:** Small

### Task 4: PII encryption utilities and audit log infrastructure
**Description:** Build `security.py` (encrypt/decrypt PII fields) and the audit log write utility.
**Acceptance criteria:**
- [x] Phone numbers and names can be encrypted/decrypted transparently
- [x] `write_audit_log()` function writes to the `audit_log` table
**Verification:** Unit tests for encryption roundtrip and audit log writes
**Dependencies:** Task 2
**Estimated scope:** Small

---

## Phase 2: WhatsApp Ingress

> **Phase 1 → Phase 2 carry-over (from the 2026-10-01 Phase 1 readiness audit).**
> Phase 1 (Tasks 1–4) is complete and green — no defects. These are *forward-looking
> prerequisites* the Phase 2 webhook needs; none existed yet at end of Phase 1. Do them
> as the opening moves of the tasks noted, not as afterthoughts:
>
> 1. **Shared async Redis client/helper** — a `redis.asyncio` client for app code (the
>    TaskIQ broker's internal Redis is separate). Needed by **Task 5** (`SETNX` dedup) and
>    **Task 7** (Lua CAS mutex). The `redis[hiredis]` dep is already installed; this is
>    net-new code, no mutex/dedup foundation exists today.
> 2. **Meta webhook config in `Settings` + `.env.example`** — `meta_app_secret` (HMAC body
>    verify), `whatsapp_verify_token` (GET challenge), Meta access token, and Graph API
>    version. None exist yet. Owned by **Task 5** (and reused by Task 6 sending).
> 3. **E.164 phone-normalization helper feeding `hash_phone`** — deliberately deferred from
>    Task 4 to its first caller. Un-normalized input (`+91 98765…` vs `919876…`) defeats the
>    `(tenant_id, phone_hash)` unique constraint and creates duplicate leads. Owned by
>    **Task 5** (lead creation / lookup by phone).
> 4. **Decision: UNIQUE/partial index on `messages.wa_message_id`?** Today it is indexed but
>    *not* UNIQUE — dedup is Redis-`SETNX`-only by design (ADR-002). Make a conscious call in
>    **Task 5** on whether to add a DB-level backstop for when the Redis layer is bypassed.
>
> Naming note: acceptance text below says "`audit_log`"; the real table is `audit_logs`
> (code + migration agree) — cosmetic, no change needed.

### Task 5: Meta WhatsApp webhook (HMAC + dedup + enqueue)
**Description:** Build `GET` (challenge verification) and `POST` (HMAC verify body, Redis SETNX dedup on `message.id`, extract payload, enqueue to TaskIQ).
**Acceptance criteria:**
- [x] `GET /api/webhook` passes Meta challenge
- [x] `POST /api/webhook` returns 200 OK immediately
- [x] Duplicate `message.id` silently dropped
- [x] Valid messages enqueued to TaskIQ
**Verification:** Test with ngrok + Meta test tool
**Dependencies:** Task 3
**Estimated scope:** Medium

### Task 6: WhatsApp message sending service
**Description:** Build `whatsapp.py` service with functions to send: text, interactive buttons, interactive lists, and template messages via Meta Cloud API.
**Acceptance criteria:**
- [x] `send_text()`, `send_buttons()`, `send_list()`, `send_template()` all work
**Verification:** Send a test message to a verified number
**Dependencies:** Task 1
**Estimated scope:** Medium

### Task 7: Redis distributed mutex
**Description:** Implement `redis_mutex(key)` async context manager using Redis Lua CAS for owner-safe release, with keepalive TTL extension.
**Acceptance criteria:**
- [x] Only one worker processes a message per phone number at a time
- [x] Lock auto-releases after TTL if worker crashes
**Verification:** Unit test with simulated concurrent access
**Dependencies:** Task 3
**Estimated scope:** Small

---

## Phase 3: AI Core (Engine + RAG)

### Task 8: Engine state definition and lifecycle
**Description:** Define the conversation state schema (a plain dataclass/Pydantic model loaded per turn, not a graph state) including: `lead_status`, `conversation_history`, `current_course`, `extracted_facts`, `pending_order`, `applied_discount`, `co_pilot_mode`, `consult_stage`. Build `engine/state.py` (lifecycle states + allowed transitions) and the `engine/dispatcher.py` skeleton (`handle_turn()`).
**Acceptance criteria:**
- [x] State schema defined with all required fields
- [x] Lead lifecycle transitions enforced in code
**Verification:** Unit test state transitions
**Dependencies:** Task 2
**Estimated scope:** Medium

### Task 9: Multi-provider LLM factory with fallback
**Description:** Build `llm_factory.py` that tries Gemini → OpenAI → Anthropic with automatic fallback on API errors (chain per ADR-007; model IDs config-driven).
**Acceptance criteria:**
- [x] Primary provider used when healthy
- [x] Automatic fallback to next provider on error
- [x] All providers return the same interface
**Verification:** Mock primary provider failure, verify fallback triggers
**Dependencies:** Task 1
**Estimated scope:** Medium

### Task 10: Input guardrail node
**Description:** First node in the graph. Detects prompt injection, profanity, and abuse patterns. Issues canned refusal and halts processing.
**Acceptance criteria:**
- [x] Injection attempts detected and blocked
- [x] Profanity detected and blocked
- [x] Clean messages pass through unchanged
**Verification:** Unit tests with adversarial inputs
**Dependencies:** Task 8
**Estimated scope:** Medium

### Task 11: Triage node (intent detection)
**Description:** Routes incoming messages to the appropriate downstream node: Discovery, RAG, Qualification, Handoff.
**Acceptance criteria:**
- [x] Correct routing for course exploration, knowledge questions, qualification answers, and human requests
**Verification:** Unit tests with representative message types
**Dependencies:** Task 8, 9
**Estimated scope:** Medium

### Task 12: Discovery node
**Description:** Presents available courses as WhatsApp interactive lists/buttons. Handles course selection and batch routing.
**Acceptance criteria:**
- [x] Courses fetched from DB filtered by `tenant_id`
- [x] Only batches with `seats_remaining > 0` shown
- [x] Tap-based selection updates lead state to `discovering`
**Verification:** Integration test with seeded course data
**Dependencies:** Task 8, 6
**Estimated scope:** Medium

### Task 13: RAG pipeline
**Description:** Build document ingestion (chunk, embed, store in pgvector), hybrid search (dense + lexical with RRF), and RAG chunk sanitizer.
**Acceptance criteria:**
- [x] Documents chunked and embedded per tenant
- [x] Search returns relevant chunks above confidence threshold
- [x] Chunks sanitized before injection
**Verification:** Golden question retrieval test (≥80% hit rate)
**Dependencies:** Task 2
**Estimated scope:** Large

### Task 14: RAG node
**Description:** Graph node that retrieves from the knowledge base and generates an answer. Fail-closed below confidence threshold.
**Acceptance criteria:**
- [x] Answers knowledge questions from institution documents
- [x] Says "I don't have that information" below threshold (no hallucination)
**Verification:** Test with institution FAQ documents
**Dependencies:** Task 13, 9
**Estimated scope:** Medium

### Task 15: Qualification node
**Description:** Asks the user questions to extract field values, then verifies against structured course rules in code. Extraction uses native structured outputs (JSON-schema / function calling), not free-text parsing — extracted fields feed deterministic rule eval (ADR-007 LLM efficiency).
**Acceptance criteria:**
- [x] AI asks the right questions to fill rule fields
- [x] Field values extracted via structured output into a typed schema (no regex/free-text parsing)
- [x] Code evaluates field/operator/value rules deterministically
- [x] Lead marked `admission_ready` only when ALL rules pass
**Verification:** Unit tests for rule engine + integration test with mocked LLM
**Dependencies:** Task 8, 9, 12
**Estimated scope:** Large

### Task 16: Output guardrail
**Description:** Validates AI response before sending to WhatsApp. Blocks hallucinated fees, made-up course names, PII leakage, and ensures WhatsApp-safe formatting.
**Acceptance criteria:**
- [x] Monetary figures not from DB are blocked
- [x] Course names not in the DB are flagged
- [x] WhatsApp formatting applied correctly
**Verification:** Unit tests with adversarial AI outputs
**Dependencies:** Task 8
**Estimated scope:** Medium

### Task 17: Wire webhook → TaskIQ → engine dispatcher → WhatsApp
**Description:** Connect all the pieces: TaskIQ worker picks up the message, runs it through the full `handle_turn()` dispatcher (decide → dispatch → generate → guard), and sends the response.
**Acceptance criteria:**
- [ ] Full loop works end-to-end
- [ ] Episodic memory (`messages` table) persists conversation between turns; recent turns reloaded each message
- [ ] Semantic memory (`lead_facts`) updated after each turn
**Verification:** End-to-end test on a real WhatsApp device
**Dependencies:** Task 5, 6, 7, 8–16
**Estimated scope:** Medium

---

## Phase 4: Advanced Bot Features

### Task 18: Application form collection node
**Description:** Collects structured application data (name, DOB, parent name, address, previous school) via sequential WhatsApp prompts.
**Acceptance criteria:**
- [ ] All required fields collected via tap/type prompts
- [ ] Data saved to `application` table
- [ ] Lead state transitions to `form_collecting` → `payment_pending`
**Verification:** Integration test collecting a full application
**Dependencies:** Task 15, 17
**Estimated scope:** Medium

### Task 19: Razorpay integration
**Description:** Build discount code validation, payment link creation (raw httpx), HMAC webhook verification, and in-chat confirmation.
**Acceptance criteria:**
- [ ] Payment link generated with correct amount from DB
- [ ] Link sent only after explicit user tap
- [ ] `payment_link_sent` flag prevents duplicate links
- [ ] Razorpay webhook (HMAC verified) updates payment status
- [ ] Bot confirms payment in chat
**Verification:** End-to-end test with Razorpay test mode + test card
**Dependencies:** Task 17, 6
**Estimated scope:** Large

### Task 20: Human handoff + co-pilot mode
**Description:** Handoff node for escalation. Co-pilot mode: AI generates suggested replies visible in dashboard.
**Acceptance criteria:**
- [ ] Auto-escalation triggers work (anger, human request, safety topics)
- [ ] Co-pilot mode generates suggestions without sending to user
- [ ] "Resume AI" re-activates the bot with context continuity
- [ ] Business hours respected for escalation
**Verification:** Integration test with escalation triggers
**Dependencies:** Task 17
**Estimated scope:** Large

### Task 21: Cold lead re-engagement worker
**Description:** Scheduled TaskIQ task that finds stale leads and sends AI-generated, context-aware follow-up hooks.
**Acceptance criteria:**
- [ ] Stale leads identified (no reply in X days)
- [ ] AI generates personalized hook with urgency + tap button
- [ ] Max 2 follow-ups, then mark `cold`
**Verification:** Test with artificially aged leads
**Dependencies:** Task 17, 6
**Estimated scope:** Medium

### Task 22: WhatsApp rate-limit tracking
**Description:** Track outbound message counts per institution per day. Queue messages if approaching Meta tier limits.
**Acceptance criteria:**
- [ ] Outbound count tracked in Redis per tenant per day
- [ ] Warning surfaced when approaching limit
- [ ] Messages queued instead of dropped when limit reached
**Verification:** Unit test with simulated high volume
**Dependencies:** Task 6
**Estimated scope:** Small

### Task 23: Langfuse tracing integration
**Description:** Add `@observe()` decorators to all LLM-calling functions. Configure Langfuse client in `tracing.py`.
**Acceptance criteria:**
- [ ] Every LLM call visible in Langfuse with input/output/latency/cost
- [ ] Graph execution path traceable per conversation
**Verification:** Run a conversation and verify traces appear in Langfuse dashboard
**Dependencies:** Task 17
**Estimated scope:** Small

---

## Phase 5: Dashboard Frontend (Next.js)

### Task 24: Initialize Next.js + dark mode + glassmorphism
**Description:** Create `frontend/` with Next.js, Tailwind CSS configured for dark mode and premium glassmorphism aesthetic.
**Acceptance criteria:**
- [ ] Next.js app runs on localhost:3000
- [ ] Dark mode + glassmorphism tokens configured
**Verification:** Visual inspection of a test page
**Dependencies:** None
**Estimated scope:** Small

### Task 25: Authentication (email + password)
**Description:** Login page, JWT-based auth, role-based access control (`admin` vs `agent`).
**Acceptance criteria:**
- [ ] Staff can register and log in
- [ ] JWT token stored securely
- [ ] Route guards based on role
**Verification:** Login flow + unauthorized access blocked
**Dependencies:** Task 24, Task 2 (backend auth endpoints)
**Estimated scope:** Medium

### Task 26: Dashboard home (funnel analytics)
**Description:** Main dashboard page with funnel visualization and time-series lead charts.
**Acceptance criteria:**
- [ ] Funnel shows counts and conversion rates for each lifecycle state
- [ ] Time-series chart shows leads per day/week
**Verification:** Load with seeded data, verify charts render
**Dependencies:** Task 25
**Estimated scope:** Medium

### Task 27: Leads CRM page
**Description:** Table/grid of all leads with status filters, search, and click-to-view detail.
**Acceptance criteria:**
- [ ] Leads fetched from FastAPI, filtered by tenant
- [ ] Status indicators (color-coded by lifecycle state)
- [ ] Search by name/phone
**Verification:** Load with seeded leads
**Dependencies:** Task 25
**Estimated scope:** Medium

### Task 28: Course & batch management
**Description:** CRUD pages for courses, batches, discount codes, and qualification rules builder.
**Acceptance criteria:**
- [ ] Create/edit/delete courses and batches
- [ ] Qualification rules builder (field/operator/value)
- [ ] Batch capacity and seat tracking visible
**Verification:** Create a course with rules, verify in DB
**Dependencies:** Task 25
**Estimated scope:** Large

### Task 29: Chat takeover + co-pilot UI
**Description:** Messaging interface showing chat history, AI suggested replies, and manual send.
**Acceptance criteria:**
- [ ] Chat history rendered (AI messages vs user messages)
- [ ] AI-suggested replies shown with approve/edit/ignore buttons
- [ ] Manual text input sends message via WhatsApp
- [ ] "Take Over" and "Resume AI" buttons
**Verification:** Take over a chat and send a manual message
**Dependencies:** Task 25, 20
**Estimated scope:** Large

### Task 30: Document management (RAG)
**Description:** Upload/delete institution documents for the RAG knowledge base.
**Acceptance criteria:**
- [ ] File upload triggers backend ingestion
- [ ] Document list shows indexed files
- [ ] Delete removes chunks from pgvector
**Verification:** Upload a PDF, ask the bot a question, verify RAG answer
**Dependencies:** Task 25, 13
**Estimated scope:** Medium

### Task 31: Application submissions view
**Description:** Table of submitted application forms with detail view and manual review actions (Approve, Waitlist, Reject).
**Acceptance criteria:**
- [ ] Application data displayed (name, DOB, address, etc.)
- [ ] Linked to lead record
**Verification:** Submit an application via bot, verify it appears in dashboard
**Dependencies:** Task 25, 18
**Estimated scope:** Small

### Task 32: Data export + webhook config
**Description:** CSV/Excel export for leads, applications, payments. Outbound webhook URL configuration.
**Acceptance criteria:**
- [ ] Export buttons generate downloadable CSV/Excel
- [ ] Webhook URL configurable per institution
- [ ] Events pushed to webhook URL in real-time
**Verification:** Export data + configure a test webhook URL
**Dependencies:** Task 25
**Estimated scope:** Medium

### Task 33: Real-time WebSocket notifications
**Description:** Notification bell with live badge count for new events.
**Acceptance criteria:**
- [ ] WebSocket connection established on dashboard load
- [ ] Badge increments on: new qualified lead, dead-letter message, co-pilot suggestion, payment received
**Verification:** Trigger an event from the bot, verify badge updates
**Dependencies:** Task 25
**Estimated scope:** Medium

### Task 34: Institution settings
**Description:** Settings page for business hours, re-engagement timing, and general config.
**Acceptance criteria:**
- [ ] Business hours configurable (start/end time, timezone)
- [ ] Re-engagement delay configurable (days)
**Verification:** Update settings, verify they affect bot behavior
**Dependencies:** Task 25
**Estimated scope:** Small

---

## Phase 6: Production Hardening

### Task 35: Sentry error monitoring
**Description:** Integrate Sentry SDK in both FastAPI and TaskIQ worker.
**Acceptance criteria:**
- [ ] Unhandled exceptions reported to Sentry with full context
**Verification:** Trigger a test error, verify it appears in Sentry
**Dependencies:** Task 17
**Estimated scope:** Small

### Task 36: Delete My Data endpoint
**Description:** API endpoint that purges all data for a given phone number: conversation state, lead facts, messages, application, payment orders.
**Acceptance criteria:**
- [ ] All user data deleted across all tables
- [ ] Deletion logged in audit trail
**Verification:** Delete a test user, verify no data remains
**Dependencies:** Task 4
**Estimated scope:** Small

### Task 37: Data retention auto-cleanup
**Description:** Scheduled job that deletes conversations older than the configured retention period.
**Acceptance criteria:**
- [ ] Conversations beyond retention period auto-deleted
- [ ] Configurable per tenant
**Verification:** Test with artificially aged data
**Dependencies:** Task 4
**Estimated scope:** Small

### Task 38: Docker Compose for local development
**Description:** `docker-compose.yml` with all services: FastAPI, TaskIQ worker, PostgreSQL+pgvector, Redis, Langfuse.
**Acceptance criteria:**
- [ ] `docker compose up --build` starts everything
**Verification:** Full stack boots from clean state
**Dependencies:** All previous tasks
**Estimated scope:** Medium

### Task 39: Production deployment
**Description:** Deploy Next.js to Vercel; backend API + TaskIQ worker + scheduler to Fly.io (always-on machines); Neon (managed Postgres + pgvector); Redis on Fly; Langfuse Cloud. Per ADR-007.
**Acceptance criteria:**
- [ ] Frontend accessible on production URL
- [ ] Backend API accessible on production URL
- [ ] Webhooks configured with production URLs
**Verification:** End-to-end test on production
**Dependencies:** All previous tasks
**Estimated scope:** Medium

---

## Phase 3–4 addition (see ADR-008)

### Task 40: `decide()` System-1 decision-layer abstraction
**Description:** Build `src/decision/` — a `decide()` interface exposing choice/score/noul primitives with calibrated probabilities. Demo backend uses Gemini Flash structured outputs; the interface is backend-agnostic so a self-hosted Laya backend can drop in later (ADR-008). Used by input guardrail, triage, readiness scoring, and escalation detection.
**Acceptance criteria:**
- [ ] `decide()` returns typed answers (label+prob / score / yes-no prob) via Gemini Flash structured output
- [ ] Guardrail, triage, readiness, and escalation call `decide()` (no ad-hoc LLM calls)
- [ ] Backend is swappable behind the interface (config-selected)
**Verification:** Unit tests with a mocked backend; each decision site covered
**Dependencies:** Task 9, 10, 11, 15
**Estimated scope:** Medium

### Task 41: Distill decisions into self-hosted Laya (post-demo)
**Description:** Stand up self-hosted Laya (Jev-compatible `/v1/systemone`) as a `decide()` backend. Use labels collected during the demo to fine-tune/calibrate the high-frequency decisions (triage, guardrail-triage, readiness, escalation). Switch per decision only after evaluating Malayalam/Hinglish accuracy and fitting calibration.
**Acceptance criteria:**
- [ ] Laya backend implements the `decide()` interface
- [ ] Malayalam/Hinglish accuracy measured per decision vs the LLM backend
- [ ] Calibration (temperature) fitted; over-confidence checked (ECE)
- [ ] OTHER/ESCALATE option present on all choice decisions
**Verification:** Offline eval set per decision; shadow-run against live LLM decisions before cutover
**Dependencies:** Task 40, 17
**Estimated scope:** Large

### Task 42: Advanced RAG Strategy (ADR-011)
**Description:** Implement the advanced RAG pipeline to handle complex document parsing, latency-optimized reranking, and contextual query rewriting.
This epic is broken down into sub-tasks for focused implementation.

### Task 42.1: Complex Document Parsing & Semantic Chunking
**Description:** Integrate `docling` (or `unstructured`) to parse uploaded PDFs into Markdown, preserving tables and structure. Replace the naive sliding window chunker in `rag.py` with a semantic, Markdown-header-aware chunker.
**Acceptance criteria:**
- [ ] Document ingestion pipeline uses `docling`/`unstructured` for PDFs
- [ ] Tables and multi-column layouts are preserved in Markdown
- [ ] Semantic chunking implemented (retains parent-child headers)
**Verification:**
- [ ] Unit tests uploading a complex PDF and verifying structural chunks
**Dependencies:** Task 13
**Files likely touched:** `backend/pyproject.toml`, `backend/src/core/rag.py`
**Estimated scope:** Medium

### Task 42.2: Contextual Query Rewriting
**Description:** Add a query resolution step before vector search. Use Gemini Flash to rewrite the raw WhatsApp message into a standalone query (resolving slang and pronouns using conversation history).
**Acceptance criteria:**
- [ ] Query rewriter LLM chain implemented
- [ ] Uses previous conversation turns to resolve ambiguous intent
- [ ] Pre-filters search space using metadata tags if a specific course is identified
**Verification:**
- [ ] Unit tests for query resolution given ambiguous user inputs
**Dependencies:** Task 13
**Files likely touched:** `backend/src/core/rag.py`
**Estimated scope:** Medium

### Task 42.3: Pluggable Reranker (Cohere API vs Local)
**Description:** Add a config-driven reranker layer to `search_chunks`. In dev mode, use a fast/free pass-through or tiny local cross-encoder. In prod mode, use Cohere's Rerank API via LiteLLM for high precision without CPU bloat.
**Acceptance criteria:**
- [ ] Reranking logic implemented after hybrid search
- [ ] `use_reranker` and `reranker_provider` (local vs cohere) added to settings
- [ ] Latency stays well within budget (since compute is offloaded)
**Verification:**
- [ ] Unit tests mock the reranker and verify correct top-N sorting
**Dependencies:** Task 42.2
**Files likely touched:** `backend/src/core/rag.py`, `backend/src/core/settings.py`
**Estimated scope:** Medium

---

## AIBoomi Startup Weekend session handoff (2026-10-22)

**Scope:** Preserve context in this repository; no new repository, product changes, or deployment.
**Dependencies:** Public event/handbook snapshots and repository inspection.
**Acceptance criteria:**
- [ ] Root EVENT_CONTEXT.md records the latest user direction, event rules, baseline facts, unknowns, and restart prompt.
- [ ] docs/event/ holds the preparation plan, source snapshots, and discrepancies.
- [ ] AGENTS.md links the handoff and local links/content have been checked.
- [ ] Follow the existing completion/commit workflow before marking this milestone complete.

Start at [../EVENT_CONTEXT.md](../EVENT_CONTEXT.md). Next implementation step proposed: bounded real WhatsApp readiness check, after the user resumes.

## WhatsApp readiness check (2026-10-22, in progress)

**Scope:** One-hour evidence check in the renamed admitflow repository; preserve the dirty baseline. Local configuration authorized by the user. No broad implementation.
**Evidence:** [../docs/event/READINESS_CHECK.md](../docs/event/READINESS_CHECK.md).
**Acceptance criteria:**
- [ ] Real demo-phone ingress -> Redis queue -> registered worker -> delivered WhatsApp reply evidenced with latency.
- [ ] Seeded course selection, next-turn memory, and tenant-scoped persisted lead inspected.
- [ ] Pass/fail/blocker and smallest repair scope recorded at the timebox boundary.
- [ ] Prior-work disclosure updated from actual evidence; surprise requirement remains unclaimed until announced and implemented.

Fresh default baseline gate: 106 passed, 4 integration tests deselected, 2 warnings. This is not a live readiness pass.

### Readiness blocker: idle Redis worker restart (in progress)

**Evidence:** Actual TaskIQ worker raised Redis TimeoutError after five idle seconds, then restarted. Credentials validated separately using read-only Meta/OpenAI requests.
**Acceptance:** A real Redis listener remains alive beyond five seconds and consumes subsequent work; configure the blocking broker read timeout without changing normal Redis calls. Regression test first, then full gate and actual queue/worker smoke check.

### Readiness tunnel setup (in progress)

**Scope:** Expose only the existing signed Meta webhook via a temporary tunnel; keep local debug/docs routes private. Verify handshake, invalid signature rejection, and other-route 404s. No production deployment or dashboard claim.

### Test-number delivery diagnosis (October 23, blocked on Meta account restriction)

**Scope:** Correct the existing app callback and missing account subscription; observe signed delivery statuses without PII. Preserve other app subscriptions and existing webhook fields.
**Evidence:** READINESS_CHECK.md records successful subscription repair and a real failure webhook (131031). Meta health API reports the test account banned (141014), sending BLOCKED. Appeal in Meta Business Support Home is the next required user action; local configuration cannot lift the restriction.
**Verification:** Missing-status regression reproduced; focused tests cover signed status logs, invalid-signature rejection, PII exclusion, and tunnel route restrictions. Full gate result recorded in the readiness report when completed. No phone-delivery or complete learner-journey claim.

### Final Postman diagnostic (October 23, executed; delivery blocked)

User authorized executing the Postman setup and one final send. Imported collection ran via isolated temporary Newman, using ignored local credentials in memory. Health BLOCKED; send accepted HTTP 200; signed failure event 131031 confirmed (`f3fc27bca826` hashed reference). Safe local runner added; syntax checked. Corrected sandbox variable declarations, then read-only execution produced 2 assertions with 1 expected restriction failure. No subsequent send. Details: [../docs/event/POSTMAN_CHECK.md](../docs/event/POSTMAN_CHECK.md). Further delivery depends on Meta account access, not another client or API retry.
