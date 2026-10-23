# AdmitFlow — Complete Specification

> **What AdmitFlow is** (the product definition) lives in [PRODUCT.md](PRODUCT.md) — the canonical source for the product concept. This file is the **technical** specification. Where the two conflict on *what the product is*, PRODUCT.md governs.

## 1. Objective

**AdmitFlow** is an AI-native admissions engagement platform — a multi-tenant SaaS product institutions can onboard to. It runs on WhatsApp, the channel parents and institutions already use daily in India, removing any adoption friction. Using simple tap-based options instead of long typed answers, it understands each inquirer's interest area, level, and timeline, and guides them toward the most suitable course or batch the institution already offers.

It remembers the full history of each conversation, so nothing gets repeated or forgotten, and treats an admission-ready lead differently from a browsing parent, and differently again from a cold lead re-engaged days later. Complex or sensitive cases are handed to staff with full conversation context.

**Target Users:**
- **Parents/Students** interacting via WhatsApp (English, Hindi, Hinglish, Malayalam).
- **Institution Staff** managing courses and leads via a web-based Admin Dashboard.

**Revenue Model:** Base monthly subscription per institution, tiered by qualified leads or active engagements.

**Differentiator:** Most existing tools only auto-reply to the first message; AdmitFlow manages the full lead relationship — from first inquiry through qualification, application form collection, fee payment, and enrollment.

---

## 2. Boundaries & Invariants

### Always Do
- **Readiness-Aware, Adaptive Flow**: There is **no single fixed script** every inquirer follows. The bot adapts to each inquirer's readiness to enroll — an admission-ready lead is guided toward next steps, a browsing parent gets no-pressure information, a cold lead gets a timely follow-up. Lifecycle states (§7.3) record *where a lead stands*, not a rigid track they must march through. Guidance is scoped to the institution's **own** courses — never general career counselling. See [PRODUCT.md](PRODUCT.md).
- **Code Owns Eligibility**: The institution's **hard** eligibility rules are verified deterministically in code. The LLM only extracts field values from the conversation and never marks a lead "Admission-Ready" — code does. (Enrollment *readiness* is AI-assessed and soft; hard eligibility is code-gated.)
- **Code Owns the Money**: The LLM never decides fee amounts. Application fees come from the `course.application_fee` database field. The LLM may only reference the fee in conversational context; all payment link amounts are code-derived.
- **Decisions vs Generation**: Bounded decisions (intent routing, guardrail triage, readiness scoring, escalation) run on a fast **System-1 decision layer** with calibrated probabilities; only user-facing text is produced by a frontier LLM. Field extraction stays on the LLM + code. See ADR-008.
- **Zero-LLM Fast Paths**: Taps on WhatsApp interactive menus update state instantly in code, skipping LLM calls where possible.
- **Per-Message Mutex**: Redis distributed lock keyed by `wa_mutex:{phone_number}` ensures only one worker processes a message from a given phone number at a time.
- **PII Encryption**: Phone numbers, names, and emails are encrypted at application level in the database.
- **Three-Layer Guardrails**: Input sanitization, RAG chunk sanitization, and output validation run on every message.
- **Webhook Dedup**: Redis `SETNX` on `message.id` with 5-minute TTL prevents duplicate processing.
- **Audit Everything**: Every significant action writes to the `audit_log` table.

### Ask First
- Database schema changes
- Adding new external dependencies
- Changing LLM provider configuration
- Modifying qualification rule evaluation logic
- Changing guardrail detection patterns

### Never Do
- Store institution API keys or WhatsApp tokens in plain text
- Let the AI send un-sanitized markdown in WhatsApp (WhatsApp uses different formatting)
- Let the LLM directly determine if a lead is qualified (code must verify)
- Let the LLM decide or invent a fee amount (code owns the money)
- Process messages concurrently for the same phone number without the mutex
- Send messages exceeding the institution's WhatsApp rate-limit tier

---

## 3. Tech Stack & Commands

### Hybrid Architecture
| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Backend API** | Python, FastAPI | Lightning-fast webhook ingestion, mature AI ecosystem |
| **Background Workers** | TaskIQ + Redis | Async processing to meet WhatsApp's 5s webhook timeout |
| **Conversation Engine** | Hand-rolled async dispatcher (decided — see §17, ADR-001/ADR-007) | Each WhatsApp turn is a cold reload: load lead + readiness + facts, run the decision layer, dispatch to one handler, generate, persist. Routing lives in the `decide()` layer, so no graph framework is needed. `messages` is the single source of truth. |
| **Decision Layer (System-1)** | Laya (self-hosted, Apache-2.0, Jev-compatible); demo runs on Gemini Flash behind a `decide()` interface | Typed, calibrated decisions — routing, guardrail triage, readiness `score`, escalation — in one forward pass, ~100–400x cheaper/faster than an LLM per decision. See ADR-008. |
| **Database** | PostgreSQL + pgvector (Neon) | Managed Postgres: automatic backups, point-in-time restore, DB branching for dev/staging. Provider-independent. |
| **Vector Store (RAG)** | pgvector (PostgreSQL extension) | Per-institution knowledge base for course FAQs, prospectus, fee info |
| **Embeddings** | Pluggable: `bge-m3` (self-hosted, dev) / OpenAI `text-embedding-3-small` (prod) | Multilingual (English + Malayalam) RAG. Each chunk is tagged with its model + dimension; switching providers triggers a clean per-tenant re-index (1024-dim vs 1536-dim are not interchangeable). |
| **Episodic Memory** | `messages` table (PostgreSQL) | Turn-by-turn conversation persisted as queryable rows — one source of truth for the engine, the dashboard, and Laya training labels. Recent N turns (or a rolling summary) reloaded per message. |
| **Semantic Memory** | Custom `lead_facts` table in PostgreSQL | Extracted key facts injected as `{memory_block}` |
| **Concurrency** | Redis distributed mutex (Redis on Fly, persistence on) | Per-phone-number locking to prevent state corruption. Flat-cost Redis co-located with the app — better fit than per-command pricing for a constantly-polling broker. |
| **Webhook Dedup** | Redis SETNX | Prevent duplicate message processing from Meta retries |
| **Frontend Dashboard** | Next.js (TypeScript, React, Tailwind CSS) | Premium glassmorphism dark-mode UI |
| **Real-time Notifications** | SSE (Server-Sent Events) | One-way server→client dashboard updates; auto-reconnects, passes cleanly through Fly/Vercel. |
| **AI Providers** | Multi-provider with fallback (Gemini → OpenAI → Anthropic) | Gemini Flash primary: best Malayalam/Indic coverage + lowest cost for high-frequency nodes. OpenAI fallback for reliability + strongest structured-output extraction. Anthropic for co-pilot nuance. Model IDs are config-driven (versions churn monthly; current fast tier `gemini-3.7-flash`). |
| **WhatsApp** | Meta WhatsApp Business Cloud API | Official API for sending/receiving messages |
| **Payments** | Razorpay Payment Links (raw `httpx` + stdlib `hmac`) | Application fee collection, gated by explicit user confirmation |
| **Observability** | Langfuse Cloud (free tier) | LLM call tracing: input/output, latency, token cost, execution path. Scrub PII before logging traces. |
| **Error Monitoring** | Sentry | Crash monitoring, exception tracking |
| **Structured Logging** | Python `logging` with `[tenant_id\|phone\|request_id]` | Correlated log lines across webhook → worker → graph |
| **Task Scheduler** | TaskIQ scheduler (cron source) | Cold-lead re-engagement + data-retention jobs; failed messages retry with backoff → dead-letter list |
| **Object Storage** | Cloudflare R2 (S3-compatible) | Durable storage for uploaded RAG documents (prospectus, FAQ, fee sheets) |
| **Transactional Email** | Resend | Password resets, staff invites, admission-ready alerts |
| **Secrets & Keys** | Fly secrets + app-level envelope encryption | API keys and per-tenant WhatsApp/Razorpay creds; a master data-encryption key encrypts PII columns |
| **Tooling & CI** | uv, ruff, mypy --strict, pytest, GitHub Actions | Reproducible deps, lint/format, type-safety, tests on every push |

### Key Commands
```bash
# Backend
uvicorn src.main:app --reload
taskiq worker src.tasks.broker:broker

# Frontend
npm run dev

# Database
alembic upgrade head

# RAG Ingestion
python -m src.scripts.ingest_docs --tenant-id <id> --input-dir ./docs/<tenant>

# Webhook Testing
ngrok http 8000

# Tests
pytest
pytest tests/test_rules.py          # qualification rule engine
pytest tests/test_guardrails.py     # three-layer guardrails
pytest tests/test_payments.py       # payment flow, HMAC, gating
```

### Deployment
- **Frontend**: Vercel (optimized for Next.js)
- **Backend API + Worker**: Fly.io (always-on machines — no sleep, so webhooks and the re-engagement scheduler stay live)
- **Database**: Neon (managed PostgreSQL + pgvector)
- **Redis**: Redis on Fly (persistence enabled to protect the job queue)
- **DB connections**: app uses Neon's pooled endpoint; long-running jobs (migrations, ingestion) use the direct (session-mode) endpoint
- **Langfuse**: Langfuse Cloud (Free Tier)
- **Estimated cost**: near-$0 at pilot scale; a small always-on cost as volume grows

---

## 4. Project Structure

```text
admitflow/
├── backend/                            # Python (FastAPI + hand-rolled engine)
│   ├── src/
│   │   ├── main.py                     # FastAPI application entry
│   │   ├── api/
│   │   │   ├── webhooks.py             # Meta WhatsApp webhook (HMAC, dedup, enqueue)
│   │   │   ├── razorpay_webhook.py     # Razorpay payment webhook (HMAC, confirm)
│   │   │   └── routes/                 # REST endpoints for dashboard frontend
│   │   │       ├── leads.py
│   │   │       ├── courses.py
│   │   │       ├── batches.py
│   │   │       ├── applications.py
│   │   │       ├── analytics.py
│   │   │       ├── documents.py        # RAG document upload/manage
│   │   │       ├── auth.py
│   │   │       └── export.py           # CSV/Excel export + webhook config
│   │   ├── engine/
│   │   │   ├── dispatcher.py          # handle_turn(): mutex → load → decide → dispatch → generate → guard → persist
│   │   │   ├── state.py               # Lead lifecycle states & transitions
│   │   │   └── handlers/
│   │   │       ├── guardrail.py       # INPUT guardrail (abuse, injection, profanity)
│   │   │       ├── triage.py          # Intent detection & routing (via decide())
│   │   │       ├── discovery.py       # Course exploration handler
│   │   │       ├── rag_node.py        # RAG retrieval for knowledge questions
│   │   │       ├── qualification.py   # Rule-based qualification verification
│   │   │       ├── form_collection.py # Structured application data collection
│   │   │       ├── payment.py         # Payment link generation & confirmation
│   │   │       └── handoff.py         # Human escalation handler
│   │   ├── tasks/
│   │   │   ├── broker.py             # TaskIQ broker config
│   │   │   ├── processing.py         # Message processing worker
│   │   │   └── reengagement.py       # Scheduled cold-lead follow-up worker
│   │   ├── services/
│   │   │   ├── whatsapp.py           # Meta API send (text, interactive, templates)
│   │   │   ├── razorpay_service.py   # Razorpay Payment Link creation (raw httpx)
│   │   │   └── llm_factory.py        # Multi-provider LLM with fallback chain
│   │   ├── logic/
│   │   │   ├── rules.py             # Deterministic qualification rule engine
│   │   │   ├── pricing.py           # Application fee resolution (code-owned)
│   │   │   └── rate_limiter.py      # WhatsApp send-rate tracking per tenant
│   │   ├── decision/
│   │   │   ├── engine.py            # decide() abstraction: choice / score / noul
│   │   │   ├── llm_backend.py       # demo backend: Gemini Flash structured outputs
│   │   │   └── laya_backend.py      # post-demo: self-hosted Laya (Jev-compatible /v1/systemone)
│   │   ├── rag/
│   │   │   ├── ingestion.py         # Document chunking & embedding pipeline
│   │   │   ├── search.py            # Hybrid dense+lexical retrieval with RRF
│   │   │   └── sanitizer.py         # RAG chunk guardrail (sanitize before injection)
│   │   ├── core/
│   │   │   ├── schemas.py           # Pydantic models for all payloads
│   │   │   ├── guardrails.py        # OUTPUT guardrail (validate AI response before send)
│   │   │   ├── security.py          # PII encryption/decryption utilities
│   │   │   ├── tracing.py           # Langfuse integration
│   │   │   └── settings.py          # Environment config singleton
│   │   ├── models/
│   │   │   └── db.py                # SQLAlchemy models
│   │   └── scripts/
│   │       ├── init_db.py           # Database initialization
│   │       ├── ingest_docs.py       # RAG document ingestion CLI
│   │       └── reset_thread.py      # Clear a phone number's conversation
│   ├── alembic/                      # Database migrations
│   ├── tests/
│   │   ├── test_rules.py            # Qualification rule engine
│   │   ├── test_guardrails.py       # Three-layer guardrail tests
│   │   ├── test_payments.py         # Payment gating, HMAC, fee resolution
│   │   ├── test_rag.py              # Retrieval accuracy
│   │   ├── test_dedup.py            # Webhook deduplication
│   │   └── test_rate_limiter.py     # WhatsApp rate limit enforcement
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                         # Next.js (TypeScript)
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/login/        # Email + password login
│   │   │   ├── (dashboard)/
│   │   │   │   ├── page.tsx         # Dashboard home (funnel analytics)
│   │   │   │   ├── leads/           # Leads CRM view
│   │   │   │   ├── courses/         # Course, batch & rule management
│   │   │   │   ├── applications/    # Application form submissions view
│   │   │   │   ├── chat/            # Chat takeover + co-pilot UI
│   │   │   │   ├── documents/       # RAG document upload/manage
│   │   │   │   ├── analytics/       # Funnel analytics & charts
│   │   │   │   ├── export/          # CSV/Excel export + webhook config
│   │   │   │   └── settings/        # Institution settings, business hours
│   │   │   └── layout.tsx
│   │   ├── components/              # Shared UI components
│   │   └── lib/                     # API client, auth utilities
│   ├── package.json
│   └── Dockerfile
├── SPEC.md
├── CONSTRAINTS.md
└── tasks/
    ├── plan.md
    └── todo.md
```

---

## 5. Code Style

### Python (Backend)
```python
# Strict type hints everywhere
async def handle_turn(
    tenant_id: str,
    phone_number: str,
    inbound: InboundMessage,
) -> None:
    """Process one incoming WhatsApp message: decide → dispatch → generate → persist."""
    async with redis_mutex(f"wa_mutex:{phone_number}"):
        lead   = await load_lead(tenant_id, phone_number)
        facts  = await load_facts(tenant_id, lead.id)
        recent = await recent_messages(lead.id, n=20)        # episodic memory = our own rows

        if (await decide.noul(inbound, "abuse or injection?")).p > 0.8:
            return await send_canned_refusal(phone_number)
        route = await decide.choice(inbound, recent, ROUTES) # triage via System-1 layer
        await update_readiness(lead, await decide.score(inbound, recent, facts))

        reply = await HANDLERS[route.label](lead, inbound, facts, recent)
        safe  = output_guardrail(reply, db=lead)             # code owns money & eligibility
        await send_whatsapp(phone_number, safe)
        await persist(lead, inbound, safe)                   # messages = single source of truth
        await update_facts_async(lead.id, inbound)           # semantic memory
```

- Strict type hints (`mypy --strict`)
- Async/await for all IO-bound operations
- Pydantic models for all request/response schemas
- f-string structured logging with `[tenant_id|phone_number|request_id]` context
- Langfuse `@observe()` decorators on all LLM-calling functions

### TypeScript (Frontend)
- Server Components where possible
- Strict TypeScript (`strict: true` in tsconfig)
- API calls go through a typed client layer

### Separation of Concerns
- Python backend handles ALL business logic, AI, and database state
- Next.js frontend ONLY consumes FastAPI REST endpoints
- No business logic in the frontend

---

## 6. Testing Strategy

- **Webhook Mocking**: Python test scripts to simulate incoming Meta WhatsApp JSON payloads
- **Engine Testing**: Unit test the dispatcher — each `lead.status` / route dispatches to the right handler, with mocked `decide()` and LLM responses
- **Rule Engine Testing**: Deterministic tests for the qualification rule evaluator (field/operator/value checks)
- **Guardrail Testing**: Tests for all three layers — input sanitization, RAG chunk sanitization, output validation
- **Payment Testing**: Fee resolution from DB (not LLM), HMAC webhook verification, payment gating (no link without explicit tap)
- **RAG Testing**: Retrieval accuracy tests (golden questions ≥80% hit rate)
- **Mutex Testing**: Verify that concurrent messages for the same phone number are serialized
- **Dedup Testing**: Verify duplicate `message.id` is silently dropped
- **PII Testing**: Verify encryption at rest and that the 'Delete My Data' endpoint purges all user data
- **CI**: GitHub Actions runs `ruff`, `mypy --strict`, and `pytest` on every push; dependencies managed with `uv`.

---

## 7. Core Feature Specifications

### 7.1 WhatsApp Number Architecture
- **One WhatsApp Business number per institution.** Each institution connects their own Meta Business Account.
- Tenant identification: The webhook payload's `phone_number_id` maps to a `tenant_id` in our database.

### 7.2 Multi-Tenancy (Row-Level Isolation)
- All institutions share one PostgreSQL database.
- Every table has a `tenant_id` column.
- All queries are ALWAYS filtered by `tenant_id`.

### 7.3 Lead Lifecycle States
> These states record **where a lead stands**, not a fixed track. The bot moves a lead between them **adaptively, based on readiness** — a browsing parent may sit in `discovering` for weeks; an eager one may reach `admission_ready` in a single session. Only the money and hard-eligibility transitions are code-decided; the rest is readiness-driven. Readiness itself is a calibrated `score` from the System-1 decision layer (ADR-008), surfaced to staff as a numeric signal beside the stage.
```
new → discovering → qualifying → admission_ready → form_collecting → payment_pending → under_review → enrolled
                                        ↓                                                       ↓
                                   handed_off                                          rejected / waitlisted
                                   cold (after 2 unanswered attempts)
```
- `new`: First message received, no interaction yet.
- `discovering`: Actively exploring courses via tap menus.
- `qualifying`: AI is asking verification questions based on course rules.
- `admission_ready`: All qualification criteria passed. Flagged for institution.
- `form_collecting`: Bot is collecting structured application form data.
- `payment_pending`: Application form complete, Razorpay payment link sent.
- `under_review`: Payment confirmed. Application is awaiting manual staff review.
- `enrolled`: Staff manually approved the application in the dashboard.
- `rejected`: Staff manually rejected the application. Automated WhatsApp template sent.
- `waitlisted`: Staff manually waitlisted the application. Automated WhatsApp template sent.
- `handed_off`: A human staff member has taken over (co-pilot mode active).
- `cold`: Lead went silent after 2 re-engagement attempts.

### 7.4 Course Qualification Rules (Structured)
Staff define rules through a Dashboard form. Each course has a list of qualification criteria:

| Field | Operator | Value | Example |
|-------|----------|-------|---------|
| `age` | `>=` | `16` | Student must be 16 or older |
| `previous_grade` | `=` | `10th Pass` | Must have passed 10th grade |
| `location` | `in` | `["Kerala", "Karnataka"]` | Must be from these states |

- **Code verifies these rules deterministically.**
- **The AI's only job is to extract the field values from the conversation.**

### 7.5 Batch & Intake Management
- Each course has multiple batches (e.g., "Oct 2026 Morning", "Jan 2027 Evening").
- Each batch has: `capacity`, `start_date`, `end_date`, `seats_remaining`.
- The AI routes students to the nearest batch with available seats.
- When `seats_remaining` hits 0, the course stops accepting for that batch.
- Staff manage batches in the dashboard.

### 7.6 Cold Lead Re-engagement
- If a lead in `discovering` or `qualifying` state hasn't replied in X days (configurable per institution), the system sends an AI-generated, **context-aware follow-up hook**.
- The hook combines urgency + personalization + a tap button to resume.
- Maximum 2 follow-ups. After that, the lead is marked `cold`.

### 7.7 Language Support
- **LLM-Native Multilingual**: The system prompt instructs the LLM to detect the user's language (English, Hindi, Hinglish, or Malayalam) and reply in the same language.
- **RAG Embeddings**: We explicitly use `text-embedding-3-small` to ensure Malayalam queries successfully retrieve English institutional documents and vice versa.
- WhatsApp button/list labels will be bilingual where character limits allow.

### 7.8 Lead Sources & Outbound
- **WhatsApp Template Messages**: Institutions can trigger approved Meta Message Templates from the dashboard to initiate first contact with phone numbers collected at events.
- After the user replies, the 24-hour session window opens and the AI takes over.

### 7.9 Application Form Collection
- Once a lead is `admission_ready`, the bot collects structured application data via a series of tap/type prompts in WhatsApp.
- Fields: full name, DOB, parent/guardian name, address, previous school, ID proof number.
- Data stored in a structured `application` table, visible to staff in the dashboard.

### 7.10 Payment Integration & Discounts (Razorpay)
- Once the application form is complete, the bot can send a Razorpay Payment Link for the application/registration fee.
- **Discounts**: The AI can suggest active discount codes fetched from the DB (e.g., `EARLYBIRD10`). If the user accepts, the AI passes the code to the backend.
- **Code Owns the Money**: The Python backend validates the discount code and calculates the final fee. The LLM NEVER decides the final amount.
- Payment confirmation via Razorpay webhook (HMAC verified).
- After payment, the lead transitions to `under_review`, not `enrolled`.
- Payment link is ONLY generated after an explicit user tap ("Pay Application Fee").
- Payment order tracked with full audit trail (amount, status, webhook event).
- Replay-safe: `payment_link_sent` flag prevents duplicate link generation.

---

## 8. RAG (Retrieval-Augmented Generation)

### 8.1 Per-Institution Knowledge Base
- Each institution uploads documents (prospectus, fee structure, campus info, FAQ sheets) via the dashboard.
- Documents are chunked, embedded (via `bge-m3` or OpenAI embeddings), and stored in pgvector.
- Original uploaded files are kept in Cloudflare R2; chunks + embeddings live in pgvector.
- All chunks are tagged with `tenant_id` for strict multi-tenant isolation.

### 8.2 Retrieval Pipeline
- **Hybrid search**: Dense (vector similarity) + Lexical (keyword matching) with asymmetric RRF fusion.
- **Fail-closed**: If retrieval confidence is below threshold, the bot says "I don't have that information — let me connect you with our team" instead of hallucinating.
- **Indexing**: HNSW index on the pgvector embedding column for fast approximate-nearest-neighbour search.

### 8.3 RAG Guardrail
- Retrieved chunks are sanitized BEFORE injection into the LLM context.
- Prevents poisoned or manipulated documents from hijacking the AI's response.

---

## 9. Guardrails (Three-Layer)

| Layer | Where | What It Blocks |
|-------|-------|---------------|
| **Input** | Before LLM | Prompt injection patterns, profanity, abuse. Strips dangerous patterns, detects trolling → canned refusal. |
| **RAG** | After retrieval, before injection | Sanitizes retrieved document chunks. Prevents poisoned documents from hijacking AI responses. |
| **Output** | After LLM, before WhatsApp send | Validates AI response: blocks hallucinated fees/figures not from DB, blocks made-up course names, blocks PII leakage, ensures WhatsApp-safe formatting. |

**Deterministic-first:** The Input and Output layers run as fast code/regex checks first (injection patterns; matching any monetary figure or course name against the database). A fast System-1 decision model (Laya — calibrated `noul`, not a full LLM; ADR-008) scores only the genuinely ambiguous cases — this keeps per-turn latency and cost low and makes "code owns the money" literally enforced in code.

---

## 10. Observability & Tracing

### 10.1 LLM Tracing (Langfuse)
- Every LLM call traced with: input prompt, output, latency, token count, cost.
- Full engine execution path visible per conversation (decision calls + handler + generation).
- Dashboards: cost per institution, cost per conversation, error rates, slow queries.
- Langfuse Cloud (free tier); scrub PII from prompts/outputs before logging. Self-hosting is a post-MVP option if data-residency requires it.

### 10.2 Structured Logging
- Every log line carries `[tenant_id|phone_number|request_id]` for correlation.
- Log levels: DEBUG for graph transitions, INFO for message flow, ERROR for failures.

### 10.3 Error Monitoring (Sentry)
- Crash monitoring and exception tracking.
- Alerts on unhandled exceptions in webhook or worker processes.

---

## 11. Human-in-the-Loop (Full Workflow)

### 11.1 Auto-Escalation Triggers
The AI automatically hands off to a human when:
- Unresolved anger or frustration detected
- User explicitly requests a human ("I want to talk to someone")
- Safety or legally sensitive topics (binding commitments, special needs accommodations)
- Repeated qualification failures (user keeps failing the same rule)
- Post-payment problems (refund requests, payment disputes)

> Trigger detection runs on the System-1 decision layer (calibrated `noul`/`score`), not a full LLM (ADR-008).

### 11.2 Co-pilot Mode
When a staff member clicks "Take Over" in the dashboard:
- The AI stops sending messages directly to the user.
- The AI continues generating **suggested replies** in the background.
- Suggestions appear in the dashboard for the staff member to approve, edit, or ignore.
- Staff can click "Resume AI" to hand back to the bot. The AI reads the human messages to maintain context continuity.

### 11.3 Business Hours
- The AI operates **24/7**.
- Human escalation respects business hours (configurable per institution, default 9 AM – 6 PM IST).
- If escalated outside hours: bot sends "Our team will get back to you during working hours." The escalation is queued for the next morning.

### 11.4 Never Escalate
- Prompt injection and trolling are deflected locally by the guardrail node.
- A hostile user should NOT become a human's problem.
- **Empty or Unclear Messages**: Accidental media uploads (images without text) or stray greetings ("hello") are routed to the `discovery` node so the AI can ask for clarification. They must never trigger a human escalation (see ADR-010).

---

## 12. Edge Cases & Error Handling

| Scenario | Behavior |
|----------|----------|
| **Media (voice, image, PDF)** | Triage defaults to `discovery` (ADR-010). AI provides graceful refusal: "I can only process text messages and button taps right now." |
| **Unclear / Chit-Chat Intent**| Routed to `discovery` (ADR-010). AI naturally asks "How can I help you today?". |
| **Mid-flow intent shift** | Detect shift, clear qualification state, route back to Discovery. |
| **Human collision** | Co-pilot Mode: AI generates suggestions, staff approves/sends. |
| **Abuse & prompt injection** | Three-layer guardrails: input sanitize, RAG sanitize, output validate. |
| **LLM API outage** | Fallback chain (Gemini → OpenAI → Anthropic). All fail → retry 3x → Dead Letter Queue. |
| **Concurrent messages** | Redis mutex `wa_mutex:{phone_number}` serializes per user. |
| **Duplicate webhooks** | Redis SETNX on `message.id` with 5-min TTL. Duplicates silently dropped. |
| **WhatsApp webhook timeout** | FastAPI returns 200 OK immediately; heavy work in TaskIQ worker. |
| **WhatsApp rate limit** | Track tier per institution. Queue messages if approaching limit. Warn in dashboard. |
| **Batch full** | AI informs user that the current batch is full, offers next available batch. |
| **Payment failure** | Bot nudges once with same live link. Repeated failures → escalate to human. |
| **Payment replay** | `payment_link_sent` flag prevents duplicate link generation. Webhook clears pending order after payment. |
| **Hallucinated fee** | Output guardrail blocks any monetary figure not from the database. |

---

## 13. Dashboard Features

### 13.1 Authentication
- Email + Password for MVP (Google SSO on roadmap).
- Built on `fastapi-users` (password hashing, reset, email verification). Session token stored in an httpOnly cookie so SSE connections authenticate without custom headers.
- Each staff member belongs to one institution (tenant).

### 13.2 Roles & Permissions
| Role | Capabilities |
|------|-------------|
| `admin` | Manage courses, batches, rules, staff accounts, documents, discount codes, view all leads, analytics, export, settings |
| `agent` | View leads, take over chats, approve AI suggestions, review applications (approve/reject/waitlist) |

### 13.3 UI Aesthetic
- **Theme**: Modern & Sleek (Dark Mode)
- **Style**: Glassmorphism, deep dark backgrounds, vibrant neon purple/blue accents
- **Feel**: Premium, state-of-the-art, futuristic

### 13.4 Real-Time Notifications
- SSE-powered notification bell/badge (see §3 — one-way server→client, authenticated via the httpOnly cookie).
- Events: new admission-ready lead, dead-letter message, co-pilot suggestion, payment received.

### 13.5 Funnel Analytics
- Visual funnel with counts and conversion rates across all lifecycle states.
- Time-series chart of leads per day/week.
- Drop-off visibility (where leads are abandoning).

### 13.6 Data Export & Integration
- CSV/Excel export for leads, applications, and payment data.
- Outbound webhook configuration: institutions set a URL to receive real-time events (new lead, qualified lead, payment received) for CRM integration.

### 13.7 Document Management (RAG)
- Upload/delete institution documents (prospectus, FAQ, fee structure).
- View indexed document list and status.

### 13.8 Onboarding (MVP)
- **White-Glove**: We manually provision tenants and link their WhatsApp Business API keys.

---

## 14. Data Privacy (DPDPA-Ready)

- **PII Encryption**: Phone numbers, names, and emails encrypted at application level in PostgreSQL, using a master data-encryption key held in Fly secrets (envelope encryption). Per-tenant WhatsApp/Razorpay credentials are encrypted the same way.
- **Delete My Data**: API endpoint to purge all conversation history, facts, and application data for a given phone number.
- **Data Retention**: Auto-delete conversations older than 12 months (configurable).
- **Audit Trail**: Every significant action (message processed, state change, payment, data deletion, human takeover) logged to `audit_log` table with `tenant_id`, `lead_id`, `action`, `actor`, `timestamp`, `details`.

---

## 15. Memory Architecture

| Layer | Technology | What It Stores |
|-------|-----------|---------------|
| **Episodic** | `messages` table (PostgreSQL) | Turn-by-turn conversation as queryable rows; recent N turns (or a rolling summary) reloaded per message |
| **Semantic** | Custom `lead_facts` table (PostgreSQL) | Extracted key facts (name, age, interests, concerns, language) injected as `{memory_block}` into system prompt |
| **Knowledge** | pgvector (per-tenant document chunks) | Institution-specific information (fees, facilities, policies) retrieved via RAG |

---

## 16. Success Criteria

- [ ] A student can message the bot, explore courses via tap menus, and get qualified — all without typing long answers.
- [ ] The bot remembers the student's name, interests, and progress across sessions (even days later).
- [ ] Course qualification is deterministic: the code verifies rules, not the LLM.
- [ ] When asked "What's the hostel fee?", the bot retrieves the answer from the institution's uploaded documents (RAG), not hallucination.
- [ ] A cold lead gets a personalized, context-aware re-engagement message after X days of inactivity.
- [ ] Staff can view all leads, their funnel stage, and conversation history in the dashboard.
- [ ] Staff can take over a chat; the AI switches to co-pilot mode (suggested replies only).
- [ ] Once qualified, the bot collects application form data via structured WhatsApp prompts.
- [ ] The bot sends a Razorpay payment link for the application fee (amount set by institution, not AI).
- [ ] Payment confirmation arrives via webhook and the bot confirms in-chat.
- [ ] Every LLM call is traced in Langfuse with input, output, latency, and cost.
- [ ] The output guardrail blocks any AI response containing a fee amount not from the database.
- [ ] The system handles LLM outages gracefully via provider fallback.
- [ ] PII is encrypted at rest and can be deleted on request.
- [ ] Full audit trail exists for all significant actions.
- [ ] Duplicate webhooks from Meta are silently dropped (no double replies).
- [ ] Staff can export lead data as CSV and configure outbound webhooks for CRM integration.

---

## 17. Decisions & Open Questions

### 17.1 Conversation engine — DECIDED: hand-rolled dispatcher
The engine is a **hand-rolled async dispatcher**, not LangGraph (supersedes ADR-001's LangGraph mention; see ADR-007). The product is **readiness-aware and adaptive** ([PRODUCT.md](PRODUCT.md)), not a fixed funnel, but the adaptive **routing already lives in the System-1 `decide()` layer** (ADR-008) — so a graph framework's conditional edges add nothing. Each WhatsApp turn is a **cold reload**: `handle_turn()` loads lead + readiness + facts + recent `messages`, runs the decision layer (guardrail `noul` → triage `choice` → readiness `score`), dispatches to exactly one handler, generates the reply, runs the output guardrail, sends, and persists.

Why hand-rolled won:
- **Routing is already solved by `decide()`** — LangGraph's headline feature (conditional-edge routing) is redundant.
- **One queryable source of truth** — conversation lives in the `messages` table (needed by the dashboard *and* to collect Laya training labels), not duplicated in an opaque checkpointer blob.
- **Turn-based, not autonomous** — WhatsApp returns control to the human after each reply, so the real loop spans *messages* (state in the DB), not steps within one message. No in-process agent loop is needed or wanted; more autonomy would only widen the surface for hallucinated fees / off-catalog answers, against "code owns money & eligibility."
- **Solo-dev debuggability** — plain async Python + pytest, no framework version churn.

Bounded retries (e.g. RAG retrieve → grade → one reformulation, else fail-closed) are written as **explicit capped loops in code**, never model-driven control flow. TaskIQ owns retries/DLQ; Redis owns the per-phone mutex. Optionality is preserved: handlers are plain functions, so wrapping them as graph nodes later (if ever needed) is a contained refactor.

### 17.2 Still open
- **Rolling-summary threshold** for episodic memory: at what conversation length do we switch from "recent N turns verbatim" to a summarized block? (Tune during M1.)
- **Per-decision Laya cutover**: which decisions distill to self-hosted Laya first, gated on Malayalam/Hinglish eval + calibration (ADR-008, Task 41).
