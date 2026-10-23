# Graph Report - admitflow  (2026-10-24)

## Corpus Check
- 243 files · ~131,128 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 3, .example 2, .css 2)

## Summary
- 2222 nodes · 5977 edges · 146 communities (132 shown, 14 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 381 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `91f4370b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ADR-008: System-1 Decision Layer (Laya / Jev)
- Conversation Engine (hand-rolled dispatcher)
- AdmitFlow Complete Specification
- Finalized Production Stack
- application_action
- guardrails.py
- Code Owns the Money
- journey.py
- RedisMutex
- generate_completion
- WhatsAppSender
- tasks/processing.py
- get_redis
- core/rag.py
- PII Encryption & Audit Log
- Razorpay Payment Integration
- get_settings
- admissions.tsx
- Lead
- encrypt_pii
- AIBoomi Startup Weekend Kochi: fresh-session context
- payments/conversation.py
- sqlalchemy
- pytest
- LeadStatus
- Stages
- TelegramBot
- collections_abc
- run_postman_check.cjs
- Task List
- TelegramClient
- test_migrations.py
- Phase 5: Dashboard Frontend (Next.js)
- management.py
- Code Standards
- normalize_e164
- Event preparation and execution plan
- 7. Core Feature Specifications
- analytics.py
- main.py
- provision_staff.py
- write_audit_log
- Hackathon resources for AdmitFlow
- manifest.json
- test_workspace_limits.py
- AdmitFlow: current state and planning baseline
- AdmitFlow: AIBoomi submission plan
- AdmitFlow — Complete Specification
- 13. Dashboard Features
- integration/test_followups.py
- ADR-011: Advanced RAG Strategy (Latency vs Precision)
- Testing
- get_engine
- AdmitFlow project handoff
- detect_intent
- ADR-009: Application-Layer PII Encryption and Audit Logging
- retrieval.py
- test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment
- generate
- ADR-010: Triage Fallback Routing (Anti-Spam)
- ADR-012: Telegram and OpenAI for the first complete admissions MVP
- test_staff_operations.py
- 2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md
- compilerOptions
- Login
- 11. Human-in-the-Loop (Full Workflow)
- re
- api.py
- AdmitFlow Backend
- test_knowledge_workspace.py
- payments/service.py
- Official source snapshots
- get_sessionmaker
- 10. Observability & Tracing
- 2. Boundaries & Invariants
- signin
- management.tsx
- ._post
- AdmitFlow execution and demonstration checklist
- test_handle_turn_basic_flow
- verify.sh
- db/__init__.py
- src/__init__.py
- tasks/__init__.py
- analytics.tsx
- whatsapp/__init__.py
- integration/__init__.py
- admitflow-backend
- Settings
- AdmitFlow
- models/__init__.py
- hash_telegram_identifier
- receiver.py
- Phase 3: AI Core (Engine + RAG)
- evaluate_faq.py
- Git & GitHub Workflow
- package.json
- journey
- record-demo.mjs
- AGENTS.md
- Security & Production Readiness
- validate_services.py
- next-env.d.ts
- payments/webhook.py
- scripts/__init__.py
- layout.tsx
- frontend/AGENTS.md
- scripts
- Local Telegram/OpenAI runtime
- AdmitFlow pitch deck copy
- WhatsApp readiness check — October 22, 2026
- scheduler.py
- Reply
- Quality Gates — Definition of Done
- integration/conftest.py
- devDependencies
- applications.tsx
- dependencies
- test_readiness_webhook.py
- accept_update
- AdmitFlow submission requirements
- outreach/followups.py
- sender.py
- telegram/outbound.py
- staff/applications.py
- budget.py
- @playwright/test
- payments.tsx
- Language review packet
- react
- Knowledge
- test_ingest_document
- env.py
- integration/test_send_budget.py
- knowledge/processing.py
- 8. RAG (Retrieval-Augmented Generation)
- page.tsx
- 17. Decisions & Open Questions
- 5. Code Style
- AdmitFlow — Task List
- Phase 3–4 addition (see ADR-008)
- Phase 4: Advanced Bot Features
- Phase 6: Production Hardening
- 3. Tech Stack & Commands

## God Nodes (most connected - your core abstractions)
1. `encrypt_pii()` - 94 edges
2. `get_settings()` - 83 edges
3. `LeadStatus` - 82 edges
4. `Reply` - 71 edges
5. `write_audit_log()` - 68 edges
6. `Lead` - 67 edges
7. `TelegramBot` - 64 edges
8. `decrypt_pii()` - 62 edges
9. `Course` - 46 edges
10. `get_sessionmaker()` - 46 edges

## Surprising Connections (you probably didn't know these)
- `Task 42.3: Pluggable Reranker (Cohere API vs Local)` --references--> `search_chunks()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/core/rag.py
- `Task 4: PII encryption utilities and audit log infrastructure` --references--> `write_audit_log()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/db/audit.py
- `17.1 Conversation engine — DECIDED: hand-rolled dispatcher` --references--> `handle_turn()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/SPEC.md → backend/src/engine/dispatcher.py
- `Task 17: Wire webhook → TaskIQ → engine dispatcher → WhatsApp` --references--> `handle_turn()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/engine/dispatcher.py
- `Task 8: Engine state definition and lifecycle` --references--> `handle_turn()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/engine/dispatcher.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Finalized Production Stack Components** — docs_decisions_adr_007_finalized_stack_finalized_stack, docs_decisions_adr_007_finalized_stack_fly_io, docs_decisions_adr_007_finalized_stack_neon, docs_decisions_adr_007_finalized_stack_redis, docs_decisions_adr_007_finalized_stack_langfuse [EXTRACTED 1.00]
- **handle_turn() Per-Turn Pipeline** — spec_hand_rolled_dispatcher, docs_decisions_adr_008_system_1_decision_layer_decide, docs_decisions_adr_005_three_layer_guardrails_three_layer_guardrails, docs_decisions_adr_004_memory_architecture_episodic_memory, spec_code_owns_the_money [EXTRACTED 1.00]
- **System-1 Decision Engine (decide + primitives + models)** — docs_decisions_adr_008_system_1_decision_layer_system_1_decision_layer, docs_decisions_adr_008_system_1_decision_layer_decide, docs_research_system_1_decision_models_laya_jev_choice, docs_research_system_1_decision_models_laya_jev_score, docs_research_system_1_decision_models_laya_jev_noul, docs_research_system_1_decision_models_laya_jev_laya [EXTRACTED 1.00]
- **AdmitFlow AI Core Architecture** — tasks_plan_conversation_engine, tasks_plan_decide_decision_layer, tasks_plan_three_layer_guardrails, tasks_plan_rag_pipeline [INFERRED 0.85]
- **WhatsApp Ingress → Worker → Engine Flow** — tasks_plan_fastapi_webhook, tasks_plan_redis, tasks_plan_taskiq, tasks_plan_conversation_engine [INFERRED 0.85]

## Communities (146 total, 14 thin omitted)

### Community 0 - "ADR-008: System-1 Decision Layer (Laya / Jev)"
Cohesion: 0.18
Nodes (17): ADR-001: Hybrid Architecture, ADR-004: Dual Memory Architecture, Episodic Memory (messages table), Semantic Memory (lead_facts table), ADR-005: Three-Layer Guardrails and RAG, Three-Layer Guardrails, ADR-007: Finalized Production Stack, ADR-008: System-1 Decision Layer (Laya / Jev) (+9 more)

### Community 1 - "Conversation Engine (hand-rolled dispatcher)"
Cohesion: 0.25
Nodes (8): Conversation Engine (hand-rolled dispatcher), System-1 decide() Decision Layer, FastAPI WhatsApp Webhook, Langfuse LLM Tracing, pgvector RAG Pipeline, Redis (mutex / dedup / rate-limit), TaskIQ Background Worker, Three-Layer Guardrails

### Community 2 - "AdmitFlow Complete Specification"
Cohesion: 0.16
Nodes (12): AI Impact Statement, Student-to-staff demonstration, Executed final check, One final WhatsApp check with Postman, Prior-work disclosure draft, AdmitFlow necessary resources, Planning baseline before Telegram alignment, AdmitFlow institution knowledge workspace (+4 more)

### Community 3 - "Finalized Production Stack"
Cohesion: 0.18
Nodes (11): ADR-002: Webhook Concurrency and Deduplication, Per-Phone Redis Mutex, Webhook Deduplication (Redis SETNX), ADR-003: Multi-Tenancy Strategy, Multi-Tenancy (Row-Level Isolation), Finalized Production Stack, Fly.io (Backend + Worker + Scheduler), Langfuse Cloud (LLM Tracing) (+3 more)

### Community 4 - "application_action"
Cohesion: 0.60
Nodes (6): action(), application_action(), collect_application(), prompt(), Any, AsyncSession

### Community 5 - "guardrails.py"
Cohesion: 0.09
Nodes (34): apply_whatsapp_formatting(), check_input_safety(), check_output_safety(), _deterministic_check(), InputGuardrailResult, LLMGuardrailResponse, LLMOutputGuardrailResponse, OutputGuardrailResult (+26 more)

### Community 6 - "Code Owns the Money"
Cohesion: 0.50
Nodes (5): ADR-006: Code-Owned Qualification and Payments, Intent: Admissions Flow and Discounts, Discount Codes, Code Owns Eligibility, Code Owns the Money

### Community 7 - "journey.py"
Cohesion: 0.21
Nodes (23): answer_question(), build_reply(), button(), copy(), courses(), ExtractedFact, Extraction, GroundedQuote (+15 more)

### Community 8 - "RedisMutex"
Cohesion: 0.07
Nodes (28): MutexAcquireError, Redis, RuntimeError, Redis distributed mutex with owner-safe release and keepalive (Task 7). Ensures…, Background loop that extends the TTL while the lock is held., Raised when the mutex cannot be acquired after all retries., Async context-manager mutex backed by Redis ``SET NX``. Parameters: redis: An…, Attempt to acquire the lock, retrying up to ``retry_count`` times. (+20 more)

### Community 9 - "generate_completion"
Cohesion: 0.12
Nodes (22): AllProvidersFailedError, generate_completion(), Any, Exception, Bounded OpenAI-only model roles; provider details never escape in errors., Raised when the entire LLM fallback chain is exhausted., Generate a completion with automatic provider fallback. Tries the fast model,…, mock_settings() (+14 more)

### Community 10 - "WhatsAppSender"
Cohesion: 0.15
Nodes (12): Service for sending messages via Meta WhatsApp Cloud API., WhatsAppSender, asyncio, fixture, Successfully sending a template message., API errors (non-200) raise WhatsAppAPIError., Fails loud if access token or phone ID are missing., WhatsApp sender operations. (+4 more)

### Community 11 - "tasks/processing.py"
Cohesion: 0.12
Nodes (15): ping(), process_inbound_message(), Any, task, Background tasks for message processing. For now this module holds only the…, Smoke-test task: returns ``{"result": payload}``. Enqueued from the…, Process an inbound WhatsApp message (Task 17). This is a placeholder for the…, Tests for the TaskIQ broker setup and task execution (Task 3). All tests run… (+7 more)

### Community 12 - "get_redis"
Cohesion: 0.13
Nodes (16): get_redis(), Redis, RuntimeError, Raised when Redis is needed but ``REDIS_URL`` is unset in settings., Return the process-wide async Redis client singleton. The client is created…, RedisNotConfiguredError, post, Request (+8 more)

### Community 13 - "core/rag.py"
Cohesion: 0.13
Nodes (21): chunk_text(), embed_text(), ingest_document(), Any, AsyncSession, UUID, RAG pipeline core logic (Task 13). Handles ingestion (chunking, embedding),…, Hybrid search (dense + lexical with RRF). (+13 more)

### Community 16 - "get_settings"
Cohesion: 0.09
Nodes (28): AsyncBroker, Shared async Redis client for application code. Carry-over prerequisite #1: the…, get_settings(), Application settings singleton. Loads configuration from the environment (and…, Return the process-wide :class:`Settings` singleton., Async engine and session factory. Built lazily from ``settings.database_url``…, _build_broker(), TaskIQ broker singleton. In production (and local dev with Redis running) the… (+20 more)

### Community 17 - "admissions.tsx"
Cohesion: 0.14
Nodes (13): Admissions(), Detail, Human, Inquiry, labels, Request, RuleEvidence, statusLabel() (+5 more)

### Community 18 - "Lead"
Cohesion: 0.07
Nodes (37): MessageDirection, Enumerated types used across the schema. These are Python ``str`` enums mapped…, Direction of a WhatsApp message row (episodic memory, ADR-004)., Institution, An institution, optionally connected to a legacy WhatsApp number. The tenant…, Lead, A prospective applicant with optional phone contact and channel identities.…, _flush_engine_state() (+29 more)

### Community 19 - "encrypt_pii"
Cohesion: 0.12
Nodes (25): decrypt_pii(), encrypt_bytes(), encrypt_pii(), EncryptionKeyNotConfiguredError, _fernet(), RuntimeError, Application-layer PII protection: symmetric encryption + deterministic hashing.…, Raised when a PII helper is used but its key is unset in settings. (+17 more)

### Community 20 - "AIBoomi Startup Weekend Kochi: fresh-session context"
Cohesion: 0.11
Nodes (19): AIBoomi Startup Weekend Kochi: fresh-session context, Assessment and next decision, Current readiness session (October 22), Event sources and local copies, Existing prototype rule and surprise element, Existing working-tree changes, Fresh-message prompt, Handoff status (+11 more)

### Community 21 - "payments/conversation.py"
Cohesion: 0.08
Nodes (42): Button, field_validator, button(), discount_action(), order_reply(), payment_action(), preview(), Any (+34 more)

### Community 22 - "sqlalchemy"
Cohesion: 0.17
Nodes (15): Declarative base, metadata naming convention, and shared column mixins. Every…, Application form submissions and their payment orders., Append-only audit trail (SPEC §12 / security-and-production.md)., Course catalog: courses, batches, qualification rules, discount codes., Encrypted durable non-conversation deliveries and payment-event deduplication., Institution (the tenant root) and its staff users., Lead, its semantic facts (lead_facts), and episodic messages (ADR-004)., Durable, institution-scoped upload jobs and hashed staff sessions. (+7 more)

### Community 23 - "pytest"
Cohesion: 0.10
Nodes (33): asyncio, DiscountType, How a discount code reduces the fee., PaymentOrder, A Razorpay order for an application fee (SPEC §7.10). Amount is DB-sourced…, OutboundMessage, PaymentEvent, Code-owned application fees and authenticated Razorpay payment processing. (+25 more)

### Community 24 - "LeadStatus"
Cohesion: 0.06
Nodes (60): Any, Record persisted ORM transitions atomically; never infer an earlier stage., record_stage_changes(), LeadStatus, Lead lifecycle states (SPEC §7.3). Where a lead *stands*, not a fixed track —…, Qualification-rule comparison operators (SPEC §7.4). Evaluated…, RuleOperator, ExtractionResponse (+52 more)

### Community 25 - "Stages"
Cohesion: 0.13
Nodes (15): 10. Reflect & learn, 1. Understand & spec  (`/spec`), 2. Plan & pick a task  (`/plan`), 3. Branch, 4. Build with TDD  (`/build`, `/test`), 5. Verify (the quality gate), 6. Self-review, then adversarial review  (`/review`), 7. Commit & open the PR (+7 more)

### Community 26 - "TelegramBot"
Cohesion: 0.14
Nodes (26): Dashboard access role (SPEC — admin vs agent)., StaffRole, Batch, Course, QualificationRule, A program a lead can be qualified for and pay to apply to., A dated intake of a course with finite seats (SPEC §7.5)., A structured eligibility rule evaluated in code, not by the LLM (ADR-006).… (+18 more)

### Community 27 - "collections_abc"
Cohesion: 0.05
Nodes (27): columns(), Column, upgrade(), Column, DateTime, _timestamps(), upgrade(), common() (+19 more)

### Community 28 - "run_postman_check.cjs"
Cohesion: 0.18
Nodes (9): collection, config, crypto, fs, keys, newman, path, root (+1 more)

### Community 29 - "Task List"
Cohesion: 0.15
Nodes (13): Checkpoint: Advanced Features, Checkpoint: AI Core, Checkpoint: Dashboard Complete, Checkpoint: Foundation, Checkpoint: Production Ready, Checkpoint: WhatsApp Ingress, Phase 1: Foundation, Phase 2: WhatsApp Ingress (+5 more)

### Community 30 - "TelegramClient"
Cohesion: 0.14
Nodes (16): private_send(), Any, RuntimeError, TelegramAPIError, TelegramClient, Any, MonkeyPatch, test_outbound_dedup_claims_order_and_uncertainty() (+8 more)

### Community 31 - "test_migrations.py"
Cohesion: 0.23
Nodes (11): _alembic_config(), monkeypatch_session(), pg_url(), fixture, MonkeyPatch, Migration + schema integration tests against real Postgres. Spins up…, Start Postgres, point settings at it, yield the asyncpg URL., The tier requirement: alembic upgrade head then downgrade base, both clean. (+3 more)

### Community 32 - "Phase 5: Dashboard Frontend (Next.js)"
Cohesion: 0.17
Nodes (12): Phase 5: Dashboard Frontend (Next.js), Task 24: Initialize Next.js + dark mode + glassmorphism, Task 25: Authentication (email + password), Task 26: Dashboard home (funnel analytics), Task 27: Leads CRM page, Task 28: Course & batch management, Task 29: Chat takeover + co-pilot UI, Task 30: Document management (RAG) (+4 more)

### Community 33 - "management.py"
Cohesion: 0.13
Nodes (38): require_admin(), archive_course(), archive_discount(), BatchInput, catalog(), catalog_detail(), course_view(), CourseInput (+30 more)

### Community 34 - "Code Standards"
Cohesion: 0.18
Nodes (11): Async & I/O, Code Standards, Configuration — settings, not literals, Dependencies, Errors, Formatting, LLM calls, Logging & observability (+3 more)

### Community 35 - "normalize_e164"
Cohesion: 0.14
Nodes (10): InvalidPhoneError, normalize_e164(), ValueError, E.164 phone-number normalization. Carry-over prerequisite #3: un-normalized…, Raised when a phone string cannot be normalized to E.164., Normalize *raw* into canonical E.164 (``+<digits>``). Strips whitespace,…, Tests for E.164 phone normalization (carry-over prerequisite #3). The…, normalize_e164 → canonical E.164 string. (+2 more)

### Community 36 - "Event preparation and execution plan"
Cohesion: 0.18
Nodes (11): Business and mentor preparation, Evaluation and demo evidence, Event preparation and execution plan, Kickoff disclosure draft, Latest direction (October 23), Minimum demonstrable product, Next action: one-hour v1 readiness check, Submission checklist (+3 more)

### Community 37 - "7. Core Feature Specifications"
Cohesion: 0.18
Nodes (11): 7.10 Payment Integration & Discounts (Razorpay), 7.1 WhatsApp Number Architecture, 7.2 Multi-Tenancy (Row-Level Isolation), 7.3 Lead Lifecycle States, 7.4 Course Qualification Rules (Structured), 7.5 Batch & Intake Management, 7.6 Cold Lead Re-engagement, 7.7 Language Support (+3 more)

### Community 38 - "analytics.py"
Cohesion: 0.14
Nodes (22): alias, analytics(), bucket_dates(), count(), percent(), Period, period_window(), Any (+14 more)

### Community 39 - "main.py"
Cohesion: 0.10
Nodes (18): recovery_loop(), create_app(), ready(), lifespan(), FastAPI, FastAPI application entry point. Boots the API, manages the TaskIQ broker…, Start / stop the TaskIQ broker alongside the FastAPI process. The…, Application factory — builds and configures the FastAPI instance. (+10 more)

### Community 40 - "provision_staff.py"
Cohesion: 0.24
Nodes (10): main(), provision(), Manually provision an institution administrator without printing credentials., hash_password(), verify_password(), parametrize, Staff passwords must be salted, bounded and verified in constant time., test_invalid_password_lengths_are_rejected() (+2 more)

### Community 41 - "write_audit_log"
Cohesion: 0.09
Nodes (49): AsyncSession, UUID, Audit-log write helper. :func:`write_audit_log` is the one path significant…, Append one entry to ``audit_logs`` on ``session``; return it flushed, not…, write_audit_log(), Explicit, encrypted, deterministic application collection in a private…, resumed_status(), load_memory() (+41 more)

### Community 42 - "Hackathon resources for AdmitFlow"
Cohesion: 0.20
Nodes (10): Acceptance before using a resource, Event and release boundaries, Goal, Hackathon resources for AdmitFlow, October 23 Downloads guide: hosted inference access, Participant credits and other support, Suggested allocation and activation order, Useful resources mapped to the plan (+2 more)

### Community 43 - "manifest.json"
Cohesion: 0.20
Nodes (9): SPEC.md, bytes, sha256, tasks/plan.md, bytes, sha256, tasks/todo.md, bytes (+1 more)

### Community 44 - "test_workspace_limits.py"
Cohesion: 0.10
Nodes (18): ASGIApp, Reject oversized multipart streams before they can fill temporary storage., UploadBodyLimit, check_login_limit(), Request, MonkeyPatch, Bound resource use and reject browser cross-origin mutations before database…, test_custom_header_and_origin_required() (+10 more)

### Community 45 - "AdmitFlow: current state and planning baseline"
Cohesion: 0.22
Nodes (9): AdmitFlow: current state and planning baseline, Confirmed user direction, Feature status and integration gaps, Features to finalize next, How to reconcile the planning documents, Proposed architecture for the next plan, Stack inventory, Verification evidence and its limits (+1 more)

### Community 46 - "AdmitFlow: AIBoomi submission plan"
Cohesion: 0.22
Nodes (9): AdmitFlow: AIBoomi submission plan, Deck and presentation, Open decisions, Proposed schedule from Friday evening, Submission outcome, The journey to demonstrate, Use the provided resources, What must be handed in (+1 more)

### Community 47 - "AdmitFlow — Complete Specification"
Cohesion: 0.22
Nodes (9): 12. Edge Cases & Error Handling, 14. Data Privacy (DPDPA-Ready), 15. Memory Architecture, 16. Success Criteria, 1. Objective, 4. Project Structure, 6. Testing Strategy, 9. Guardrails (Three-Layer) (+1 more)

### Community 48 - "13. Dashboard Features"
Cohesion: 0.22
Nodes (9): 13.1 Authentication, 13.2 Roles & Permissions, 13.3 UI Aesthetic, 13.4 Real-Time Notifications, 13.5 Funnel Analytics, 13.6 Data Export & Integration, 13.7 Document Management (RAG), 13.8 Onboarding (MVP) (+1 more)

### Community 49 - "integration/test_followups.py"
Cohesion: 0.11
Nodes (26): age(), outreach(), fixture, parametrize, Real database consent, reminder leases, freshness, delivery and the two-message…, seed(), test_budget_pause_does_not_spend_a_reminder_and_stop_cancels_it(), exercise() (+18 more)

### Community 50 - "ADR-011: Advanced RAG Strategy (Latency vs Precision)"
Cohesion: 0.25
Nodes (7): 1. Complex Document Ingestion (`docling` or `unstructured`), 2. Pluggable Reranking Architecture (Cohere API over Local CPU), 3. Contextual Query Rewriting, ADR-011: Advanced RAG Strategy (Latency vs Precision), Consequences, Context, Decision

### Community 51 - "Testing"
Cohesion: 0.22
Nodes (9): Browser announcement regions, Coverage, LLM and decision-layer tests, Philosophy — pragmatic TDD, Running tests, Test layout, Testing, The two patterns (+1 more)

### Community 52 - "get_engine"
Cohesion: 0.15
Nodes (14): AsyncEngine, DatabaseNotConfiguredError, get_engine(), RuntimeError, Raised when a DB session is requested but ``DATABASE_URL`` is unset., Return the process-wide async engine (one pool for the app)., main(), run() (+6 more)

### Community 53 - "AdmitFlow project handoff"
Cohesion: 0.25
Nodes (8): AdmitFlow project handoff, Current direction, Development rules, Event submission, Execution checkpoint, First usable release, Historical evidence, Resume prompt

### Community 54 - "detect_intent"
Cohesion: 0.20
Nodes (15): detect_intent(), Classify the user's intent to route to the correct node. Design Decision: If a…, asyncio, Test routing for course discovery., Test routing for knowledge questions., Test routing for qualification answers., Test routing for human handoff., Test routing for empty messages without calling LLM defaults to discovery. (+7 more)

### Community 55 - "ADR-009: Application-Layer PII Encryption and Audit Logging"
Cohesion: 0.25
Nodes (7): ADR-009: Application-Layer PII Encryption and Audit Logging, Alternatives Considered, Context, Deterministic encryption of the phone number (so it is both stored and searchable), Full envelope encryption (per-tenant data keys wrapped by a master key), Rely on the provider's at-rest encryption only, Status

### Community 56 - "retrieval.py"
Cohesion: 0.23
Nodes (8): BaseModel, Translate non-ASCII questions for English reference material without lowering…, retrieval_query(), RetrievalQuery, MonkeyPatch, Translate retrieval queries without weakening the relevance floor., test_english_query_does_not_call_model(), test_non_ascii_query_uses_validated_translation()

### Community 57 - "test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment"
Cohesion: 0.13
Nodes (14): PaymentLink, BaseModel, field_validator, payments(), Any, get, create(), Any (+6 more)

### Community 58 - "generate"
Cohesion: 0.19
Nodes (14): content(), decide(), DraftContent, DraftDecision, DraftRequest, generate(), latest(), Any (+6 more)

### Community 59 - "ADR-010: Triage Fallback Routing (Anti-Spam)"
Cohesion: 0.33
Nodes (5): ADR-010: Triage Fallback Routing (Anti-Spam), Consequences, Context, Decision, Status

### Community 60 - "ADR-012: Telegram and OpenAI for the first complete admissions MVP"
Cohesion: 0.29
Nodes (7): ADR-012: Telegram and OpenAI for the first complete admissions MVP, Consequences, Context, Decision, Implemented runtime boundaries, References and verification, Supersession and preserved decisions

### Community 61 - "test_staff_operations.py"
Cohesion: 0.17
Nodes (16): inbound(), prepare(), Any, MonkeyPatch, parametrize, UUID, Staff takeover pauses bot replies; explicit sends are scoped, durable and…, test_clear_escalation_records_request_outside_hours_without_a_model() (+8 more)

### Community 62 - "2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md"
Cohesion: 0.25
Nodes (4): Architecture Decisions, Implementation Plan: AdmitFlow, Overview, Risks and Mitigations

### Community 63 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 64 - "Login"
Cohesion: 0.31
Nodes (11): Login, logout(), me(), BaseModel, Db, get, post, Request (+3 more)

### Community 65 - "11. Human-in-the-Loop (Full Workflow)"
Cohesion: 0.40
Nodes (5): 11.1 Auto-Escalation Triggers, 11.2 Co-pilot Mode, 11.3 Business Hours, 11.4 Never Escalate, 11. Human-in-the-Loop (Full Workflow)

### Community 66 - "re"
Cohesion: 0.21
Nodes (11): escalation_reason(), office_open(), datetime, Reason, Deterministic clear support signals and institution-local office hours., parametrize, Clear support signals escalate; office hours never promise an immediate reply., test_clear_escalation_signals() (+3 more)

### Community 67 - "api.py"
Cohesion: 0.17
Nodes (22): documents(), get_upload(), Any, BaseModel, Db, delete, get, post (+14 more)

### Community 68 - "AdmitFlow Backend"
Cohesion: 0.17
Nodes (12): Admissions analytics, AdmitFlow Backend, Application payments, Configuration, Consented follow-up reminders, Current implementation and verification, Institution knowledge workspace, Local development (+4 more)

### Community 69 - "test_knowledge_workspace.py"
Cohesion: 0.08
Nodes (20): alembic, alembic_config, Institution document extraction, durable ingestion and retrieval., Integration test: ``write_audit_log`` persists to real Postgres and reads back.…, Real PostgreSQL acceptance for authenticated uploads and atomic semantic…, identity_database(), fixture, Exercise Telegram tenant/identity constraints and safe migration rollback. (+12 more)

### Community 70 - "payments/service.py"
Cohesion: 0.10
Nodes (29): AsyncBaseTransport, Credentials, PaymentProviderError, Exception, Bounded Razorpay requests; ambiguous link creation is never blindly retried., Read an existing exact reference; absence never authorizes another creation., RazorpayClient, discounted_amount() (+21 more)

### Community 71 - "Official source snapshots"
Cohesion: 0.50
Nodes (4): Conflicts to confirm, October 23 planning refresh, Official source snapshots, Sources

### Community 72 - "get_sessionmaker"
Cohesion: 0.24
Nodes (11): async_sessionmaker, get_session(), get_sessionmaker(), AsyncSession, Return the process-wide async session factory., FastAPI dependency yielding a session that closes after the request., test_write_audit_log_persists_and_reads_back(), _run() (+3 more)

### Community 73 - "10. Observability & Tracing"
Cohesion: 0.50
Nodes (4): 10.1 LLM Tracing (Langfuse), 10.2 Structured Logging, 10.3 Error Monitoring (Sentry), 10. Observability & Tracing

### Community 74 - "2. Boundaries & Invariants"
Cohesion: 0.50
Nodes (4): 2. Boundaries & Invariants, Always Do, Ask First, Never Do

### Community 75 - "signin"
Cohesion: 0.27
Nodes (10): test_local_cohort_counts_conversions_and_observed_stages(), test_tenant_is_derived_from_session_and_period_is_bounded(), test_zero_filled_weekly_buckets_and_empty_rates(), Any, Real database management: administrator writes, role/tenant boundaries and…, test_catalog_writes_validate_rules_capacity_and_ownership(), test_discount_management_rejects_invalid_values_duplicates_and_foreign_writes(), test_settings_validate_timezone_hours_and_tenant_scope() (+2 more)

### Community 76 - "management.tsx"
Cohesion: 0.14
Nodes (10): Batch, Course, empty, Management(), operators, parseValue(), Rule, Settings (+2 more)

### Community 77 - "._post"
Cohesion: 0.17
Nodes (11): Any, Send an interactive list message. `sections` is a list of section dicts…, Send a pre-approved template message., Post the payload to Meta and extract the created message ID., Meta API expects the phone number without the leading '+'., Send a simple text message. Returns the Meta message ID., Send an interactive message with up to 3 buttons. `buttons` should be a list of…, Phase 2: WhatsApp Ingress (+3 more)

### Community 78 - "AdmitFlow execution and demonstration checklist"
Cohesion: 0.67
Nodes (3): AdmitFlow execution and demonstration checklist, Build and verify, Demonstrate and submit

### Community 79 - "test_handle_turn_basic_flow"
Cohesion: 0.29
Nodes (6): Any, asyncio, fixture, patch, sample_whatsapp_payload(), test_handle_turn_basic_flow()

### Community 84 - "analytics.tsx"
Cohesion: 0.28
Nodes (7): Analytics(), Conversion, labels, frontend_app_analytics_module, rate(), Report, shortDate()

### Community 89 - "Settings"
Cohesion: 0.12
Nodes (27): Core cross-cutting concerns: settings, security, schemas, guardrails, tracing., hash_phone(), Return a deterministic keyed hash of a phone number for lookup/dedup. Keyed…, Environment-backed application configuration., Settings, configured_keys(), fixture, MonkeyPatch (+19 more)

### Community 90 - "AdmitFlow"
Cohesion: 0.33
Nodes (6): AdmitFlow, Current status, Demonstration and submission, Development, Product scope, Stack

### Community 91 - "models/__init__.py"
Cohesion: 0.11
Nodes (39): Base, IdMixin, Declarative base shared by every AdmitFlow model., UUID primary key with an application-side default. UUIDs avoid cross-tenant…, Server-side created/updated timestamps., Row-level tenant scoping (ADR-003). Mixed into every tenant-scoped table., TenantMixin, TimestampMixin (+31 more)

### Community 92 - "hash_telegram_identifier"
Cohesion: 0.29
Nodes (8): hash_telegram_identifier(), UUID, Hash an identifier in its tenant/bot/type domain using the lookup secret. This…, MonkeyPatch, parametrize, test_lookup_hash_is_stable_scoped_and_does_not_reveal_identifiers(), test_lookup_requires_a_configured_secret(), test_private_chat_identity_rejects_invalid_identifiers()

### Community 93 - "receiver.py"
Cohesion: 0.46
Nodes (7): main(), provision_bot(), UUID, One advisory-locked long poller per bot, with durable offsets and queue…, recovery(), run(), recover_pending()

### Community 94 - "Phase 3: AI Core (Engine + RAG)"
Cohesion: 0.18
Nodes (11): Phase 3: AI Core (Engine + RAG), Task 10: Input guardrail node, Task 11: Triage node (intent detection), Task 12: Discovery node, Task 13: RAG pipeline, Task 14: RAG node, Task 15: Qualification node, Task 16: Output guardrail (+3 more)

### Community 95 - "evaluate_faq.py"
Cohesion: 0.29
Nodes (11): Case, cases(), evaluate(), main(), BaseModel, Bounded live FAQ evaluation on the fictional demo tenant; no messages or writes., score_answer(), Evaluation rejects irrelevant quotations and does not count provider errors as… (+3 more)

### Community 96 - "Git & GitHub Workflow"
Cohesion: 0.22
Nodes (9): Branching model — feature branch → PR → `main`, Commits — Conventional Commits, small and coherent, Git & GitHub Workflow, Merging, No AI attribution — the human is the sole author  ⚠️, Pull Requests, Review gate — adversarial, before merge, What never gets committed (+1 more)

### Community 97 - "package.json"
Cohesion: 0.22
Nodes (8): name, private, version, react-dom, @types/node, @types/react, @types/react-dom, typescript

### Community 98 - "journey"
Cohesion: 0.16
Nodes (12): completion(), journey(), Any, fixture, MonkeyPatch, test_multilingual_quote_selection_uses_translated_question(), exercise(), test_replies_wait_for_earlier_pending_reply() (+4 more)

### Community 99 - "record-demo.mjs"
Cohesion: 0.29
Nodes (6): credentials, headers, journey, target, ref_node_fs, ref_node_path

### Community 100 - "AGENTS.md"
Cohesion: 0.25
Nodes (7): AIBoomi Startup Weekend handoff, How we build — read the handbook, Knowledge graph, Quick commands (from `backend/`), The rules you cannot skip, What this project is, Workflow triggers

### Community 101 - "Security & Production Readiness"
Cohesion: 0.18
Nodes (11): Dependency & secret scanning, Deploy & rollback, External surfaces, Guardrails & money, Local full-stack (docker-compose), Multi-tenancy — isolation is a correctness bug if wrong, Observability, PII & data protection (DPDPA) (+3 more)

### Community 102 - "validate_services.py"
Cohesion: 0.16
Nodes (12): BaseModel, Triage Node (Task 11). Routes incoming messages to the appropriate downstream…, Structured output expected from the LLM triage classifier., TriageResponse, embed_chunks(), Use the configured OpenAI model with the database's explicit 1536 dimensions., main(), Probe (+4 more)

### Community 103 - "next-env.d.ts"
Cohesion: 0.50
Nodes (3): NOTE: This file should not be edited, frontend_next_types_root_params_d, frontend_next_types_routes_d

### Community 104 - "payments/webhook.py"
Cohesion: 0.21
Nodes (13): LinkEntity, LinkEnvelope, PaidEvent, PaidPayload, payment_webhook(), PaymentEntity, PaymentEnvelope, BaseModel (+5 more)

### Community 106 - "layout.tsx"
Cohesion: 0.25
Nodes (5): frontend_app_globals, metadata, config, @fontsource-variable/dm-sans, next

### Community 108 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, lint, record:demo, start, test:e2e:live, typecheck

### Community 109 - "Local Telegram/OpenAI runtime"
Cohesion: 0.25
Nodes (8): Configuration and data services, Delivery budget operation, Local Telegram/OpenAI runtime, Migrate and seed, Optional reminders and scheduler, Packaging and release limits, Run the processes, Validate and recover

### Community 110 - "AdmitFlow pitch deck copy"
Cohesion: 0.29
Nodes (7): AdmitFlow pitch deck copy, Slide 1: AdmitFlow, Slide 2: The admissions inquiry, Slide 3: A working student journey, Slide 4: Institution knowledge and control, Slide 5: Technology and verification, Slide 6: Pilot and next steps

### Community 111 - "WhatsApp readiness check — October 22, 2026"
Cohesion: 0.15
Nodes (13): Decision so far, Delivery diagnosis and configuration repair (October 23, approximately 00:16 IST), Evidence collected before configuration, Final Postman retry (October 23), Live checkpoint (approximately 22:54 IST), Missing-reply investigation (approximately 22:59 IST), New test account configuration (October 23, approximately 09:45 IST), Next live checks and evidence required (+5 more)

### Community 112 - "scheduler.py"
Cohesion: 0.43
Nodes (6): argparse, dispatch_due(), main(), Produce due reminder jobs and recover queued deliveries; safe to run after…, run(), recover_outbound()

### Community 113 - "Reply"
Cohesion: 0.07
Nodes (48): ConversationEvent, Event, BaseModel, Channel-neutral input and validated plain-text reply boundary., Reply, Cursor, Any, AsyncSession (+40 more)

### Community 114 - "Quality Gates — Definition of Done"
Cohesion: 0.33
Nodes (6): CI mirrors this exactly, Fast iteration vs the gate, Quality Gates — Definition of Done, The baseline gate (every change), The enforced-numbers ledger, The tiers — add gates by what the change touches

### Community 115 - "integration/conftest.py"
Cohesion: 0.29
Nodes (5): Staff authentication and institution-scoped access., isolated_local_login_windows(), fixture, MonkeyPatch, Keep development-only throttle state independent across database test cases.

### Community 116 - "devDependencies"
Cohesion: 0.33
Nodes (6): devDependencies, @playwright/test, @types/node, @types/react, @types/react-dom, typescript

### Community 117 - "applications.tsx"
Cohesion: 0.25
Nodes (5): Applications(), Detail, fields, statuses, Summary

### Community 118 - "dependencies"
Cohesion: 0.40
Nodes (5): dependencies, @fontsource-variable/dm-sans, next, react, react-dom

### Community 119 - "test_readiness_webhook.py"
Cohesion: 0.16
Nodes (12): log_delivery_status(), Request, Response, Expose only the existing Meta webhook through the temporary demo tunnel., Observe only authenticated status events, without recipient or error text., parametrize, The temporary tunnel must not expose local debug or documentation routes., test_delivery_status_logs_are_authenticated_and_exclude_pii() (+4 more)

### Community 120 - "accept_update"
Cohesion: 0.29
Nodes (6): accept_update(), Any, Commit the encrypted inbox and offset in the same transaction, before…, callback(), test_explicit_consent_and_stop_during_staff_takeover(), exercise()

### Community 121 - "AdmitFlow submission requirements"
Cohesion: 0.50
Nodes (4): AdmitFlow submission requirements, Demonstration, Required artifacts, Truthful claims

### Community 122 - "outreach/followups.py"
Cohesion: 0.12
Nodes (27): activity(), after_send(), before_send(), Check, course_available(), eligible(), generate_hook(), Hook (+19 more)

### Community 123 - "sender.py"
Cohesion: 0.33
Nodes (5): RuntimeError, WhatsApp message sending service (Task 6). Uses httpx2 to call the Meta Graph…, Raised when the Meta Cloud API returns an error response., WhatsAppAPIError, Tests for the WhatsApp Message Sending Service (Task 6). The sender calls the…

### Community 124 - "telegram/outbound.py"
Cohesion: 0.20
Nodes (19): PaymentStatus, Payment order lifecycle (SPEC §7.10)., locked(), owned(), provider(), Db, post, UUID (+11 more)

### Community 125 - "staff/applications.py"
Cohesion: 0.25
Nodes (14): ApplicationStatus, Application review status (SPEC §7.9 / lifecycle)., applications(), detail(), owned(), Any, Db, get (+6 more)

### Community 126 - "budget.py"
Cohesion: 0.14
Nodes (24): day_window(), local_counts(), Any, datetime, UUID, Atomic daily send-attempt budgets shared by every Telegram delivery path., Count confirmed deliveries once; a stats failure must not repeat a sent message., record_sent() (+16 more)

### Community 128 - "payments.tsx"
Cohesion: 0.32
Nodes (6): label(), money(), outcomes, Payment, Payments(), statuses

### Community 129 - "Language review packet"
Cohesion: 0.50
Nodes (4): Current templates, Language review packet, Live exercise, Reminder consent and outreach copy

### Community 130 - "react"
Cohesion: 0.29
Nodes (4): blank, Discount, Discounts(), react

### Community 131 - "Knowledge"
Cohesion: 0.46
Nodes (8): refresh(), api(), Knowledge(), action(), login(), search(), upload(), send()

### Community 132 - "test_ingest_document"
Cohesion: 0.40
Nodes (4): asyncio, patch, test_ingest_document(), Fresh baseline quality gate

### Community 133 - "env.py"
Cohesion: 0.22
Nodes (9): do_run_migrations(), Alembic migration environment (async). Reads the database URL from application…, Emit SQL to stdout without a live DB connection., Run migrations against a live database via an async engine., run_migrations_offline(), run_migrations_online(), Connection, logging_config (+1 more)

### Community 134 - "integration/test_send_budget.py"
Cohesion: 0.14
Nodes (4): Both Telegram outboxes share the cap, defer durably and honor provider delays., test_budget_migration_preserves_existing_institution(), test_shared_budget_preserves_queues_and_settings_wake_deliveries(), second()

### Community 135 - "knowledge/processing.py"
Cohesion: 0.06
Nodes (42): decrypt_bytes(), Authenticate and decrypt source bytes for an authorized ingestion task., extract_file(), ExtractionError, ValueError, Bounded extraction of institution reference documents; never execute uploads., A safe, public error code rather than parser output containing document text., validate_path() (+34 more)

### Community 136 - "8. RAG (Retrieval-Augmented Generation)"
Cohesion: 0.50
Nodes (4): 8.1 Per-Institution Knowledge Base, 8.2 Retrieval Pipeline, 8.3 RAG Guardrail, 8. RAG (Retrieval-Augmented Generation)

### Community 137 - "page.tsx"
Cohesion: 0.25
Nodes (6): DeliveryBudget(), Usage, Doc, errors, Match, Staff

### Community 138 - "17. Decisions & Open Questions"
Cohesion: 0.67
Nodes (3): 17.1 Conversation engine — DECIDED: hand-rolled dispatcher, 17.2 Still open, 17. Decisions & Open Questions

### Community 139 - "5. Code Style"
Cohesion: 0.50
Nodes (4): 5. Code Style, Python (Backend), Separation of Concerns, TypeScript (Frontend)

### Community 142 - "AdmitFlow — Task List"
Cohesion: 0.15
Nodes (13): AdmitFlow — Task List, AIBoomi Startup Weekend session handoff (2026-10-22), Current direction and hackathon resources (2026-10-23), Final Postman diagnostic (October 23, executed; delivery blocked), Phase 1: Foundation, Readiness blocker: idle Redis worker restart (in progress), Readiness tunnel setup (in progress), Task 1: Initialize Python project, FastAPI, settings, and Docker (+5 more)

### Community 144 - "Phase 3–4 addition (see ADR-008)"
Cohesion: 0.29
Nodes (7): Phase 3–4 addition (see ADR-008), Task 40: `decide()` System-1 decision-layer abstraction, Task 41: Distill decisions into self-hosted Laya (post-demo), Task 42.1: Complex Document Parsing & Semantic Chunking, Task 42.2: Contextual Query Rewriting, Task 42.3: Pluggable Reranker (Cohere API vs Local), Task 42: Advanced RAG Strategy (ADR-011)

### Community 145 - "Phase 4: Advanced Bot Features"
Cohesion: 0.29
Nodes (7): Phase 4: Advanced Bot Features, Task 18: Application form collection node, Task 19: Razorpay integration, Task 20: Human handoff + co-pilot mode, Task 21: Cold lead re-engagement worker, Task 22: WhatsApp rate-limit tracking, Task 23: Langfuse tracing integration

### Community 146 - "Phase 6: Production Hardening"
Cohesion: 0.33
Nodes (6): Phase 6: Production Hardening, Task 35: Sentry error monitoring, Task 36: Delete My Data endpoint, Task 37: Data retention auto-cleanup, Task 38: Docker Compose for local development, Task 39: Production deployment

### Community 149 - "3. Tech Stack & Commands"
Cohesion: 0.50
Nodes (4): 3. Tech Stack & Commands, Deployment, Hybrid Architecture, Key Commands

## Knowledge Gaps
- **404 isolated node(s):** `admitflow-backend`, `fs`, `path`, `crypto`, `root` (+399 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1006 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_settings()` connect `get_settings` to `env.py`, `journey.py`, `knowledge/processing.py`, `generate_completion`, `WhatsAppSender`, `get_redis`, `core/rag.py`, `Lead`, `encrypt_pii`, `payments/conversation.py`, `TelegramBot`, `test_migrations.py`, `main.py`, `write_audit_log`, `test_workspace_limits.py`, `get_engine`, `Login`, `api.py`, `test_knowledge_workspace.py`, `payments/service.py`, `Settings`, `hash_telegram_identifier`, `receiver.py`, `evaluate_faq.py`, `validate_services.py`, `scheduler.py`, `outreach/followups.py`, `sender.py`, `telegram/outbound.py`, `budget.py`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Why does `handle_turn()` connect `Lead` to `normalize_e164`, `guardrails.py`, `RedisMutex`, `get_sessionmaker`, `WhatsAppSender`, `tasks/processing.py`, `get_redis`, `core/rag.py`, `17. Decisions & Open Questions`, `test_handle_turn_basic_flow`, `encrypt_pii`, `detect_intent`, `LeadStatus`, `Settings`, `models/__init__.py`, `Phase 3: AI Core (Engine + RAG)`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Why does `WhatsApp readiness check — October 22, 2026` connect `WhatsApp readiness check — October 22, 2026` to `AdmitFlow Complete Specification`, `test_ingest_document`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `encrypt_pii()` (e.g. with `Consequences` and `Decision`) actually correct?**
  _`encrypt_pii()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 50 inferred relationships involving `LeadStatus` (e.g. with `record_stage_changes()` and `Lead`) actually correct?**
  _`LeadStatus` has 50 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Reply` (e.g. with `request_staff()` and `timeline()`) actually correct?**
  _`Reply` has 17 INFERRED edges - model-reasoned connections that need verification._
- **What connects `admitflow-backend`, `fs`, `path` to the rest of the system?**
  _404 weakly-connected nodes found - possible documentation gaps or missing edges._