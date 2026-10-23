# Graph Report - admitflow  (2026-10-24)

## Corpus Check
- 230 files · ~122,319 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 3, .example 2, .ini 1)

## Summary
- 2084 nodes · 5477 edges · 145 communities (128 shown, 17 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 346 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a6fe22ab`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ADR-008: System-1 Decision Layer (Laya / Jev)
- Conversation Engine (hand-rolled dispatcher)
- AdmitFlow Complete Specification
- Finalized Production Stack
- engine/applications.py
- guardrails.py
- Code Owns the Money
- LeadStatus
- RedisMutex
- journey.py
- WhatsAppSender
- tasks/processing.py
- get_redis
- core/rag.py
- PII Encryption & Audit Log
- Razorpay Payment Integration
- get_settings
- admissions.tsx
- dispatcher.py
- Settings
- AIBoomi Startup Weekend Kochi: fresh-session context
- Reply
- TestClient
- sqlalchemy
- EngineState
- Stages
- test_telegram_journey.py
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
- typing
- main.py
- auth.py
- operations.py
- Hackathon resources for AdmitFlow
- manifest.json
- test_workspace_limits.py
- AdmitFlow: current state and planning baseline
- AdmitFlow: AIBoomi submission plan
- AdmitFlow — Complete Specification
- 13. Dashboard Features
- PaymentLink
- ADR-011: Advanced RAG Strategy (Latency vs Precision)
- Testing
- get_engine
- AdmitFlow project handoff
- detect_intent
- hash_phone
- knowledge/processing.py
- test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment
- copilot.py
- ADR-010: Triage Fallback Routing (Anti-Spam)
- ADR-012: Telegram and OpenAI for the first complete admissions MVP
- test_staff_operations.py
- 2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md
- compilerOptions
- institution.py
- 11. Human-in-the-Loop (Full Workflow)
- test_escalation.py
- api.py
- AdmitFlow Backend
- identity_database
- RazorpayClient
- Official source snapshots
- telegram/service.py
- 10. Observability & Tracing
- 2. Boundaries & Invariants
- adapter.py
- management.tsx
- 8. RAG (Retrieval-Augmented Generation)
- AdmitFlow execution and demonstration checklist
- test_dispatcher.py
- verify.sh
- db/__init__.py
- src/__init__.py
- tasks/__init__.py
- receiver.py
- whatsapp/__init__.py
- integration/__init__.py
- admitflow-backend
- encrypt_pii
- AdmitFlow
- models/__init__.py
- test_payment_contracts.py
- test_webhook.py
- handle_turn
- evaluate_faq.py
- Git & GitHub Workflow
- package.json
- write_audit_log
- record-demo.mjs
- AGENTS.md
- Security & Production Readiness
- pydantic
- next-env.d.ts
- payments/webhook.py
- scripts/__init__.py
- layout.tsx
- frontend/AGENTS.md
- scripts
- Local Telegram/OpenAI runtime
- AdmitFlow pitch deck copy
- decrypt_bytes
- EncryptionKeyNotConfiguredError
- timeline.py
- Quality Gates — Definition of Done
- phone.py
- devDependencies
- applications.tsx
- dependencies
- hashlib
- .__call__
- AdmitFlow submission requirements
- send_outbound
- Alternatives Considered
- reconcile
- review
- budget.py
- payments/service.py
- payments.tsx
- Language review packet
- react
- Knowledge
- pytest
- env.py
- test_shared_budget_preserves_queues_and_settings_wake_deliveries
- test_failure_retry_and_delete_during_indexing
- test_every_tenant_scoped_table_has_tenant_id_fk_to_institutions
- page.tsx
- One final WhatsApp check with Postman
- 5. Code Style
- signin
- add_institution_knowledge_workspace_b627da2f7e11.py
- add_conversation_runtime_714f092da3b8.py
- durable_payments_outbound_f129a064c5e8.py
- 20261008_add_knowledge_models_for_rag_c470f1ebc811.py

## God Nodes (most connected - your core abstractions)
1. `encrypt_pii()` - 82 edges
2. `get_settings()` - 79 edges
3. `LeadStatus` - 67 edges
4. `Reply` - 66 edges
5. `write_audit_log()` - 61 edges
6. `TelegramBot` - 60 edges
7. `decrypt_pii()` - 59 edges
8. `Lead` - 53 edges
9. `Settings` - 44 edges
10. `get_sessionmaker()` - 43 edges

## Surprising Connections (you probably didn't know these)
- `Task 4: PII encryption utilities and audit log infrastructure` --references--> `write_audit_log()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/db/audit.py
- `17.1 Conversation engine — DECIDED: hand-rolled dispatcher` --references--> `handle_turn()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/SPEC.md → backend/src/engine/dispatcher.py
- `Missing-reply investigation (approximately 22:59 IST)` --references--> `process_inbound_message()`  [INFERRED]
  docs/event/READINESS_CHECK.md → backend/src/tasks/processing.py
- `Task 42.3: Pluggable Reranker (Cohere API vs Local)` --references--> `search_chunks()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/core/rag.py
- `Consequences` --references--> `EncryptionKeyNotConfiguredError`  [INFERRED]
  docs/decisions/ADR-009-pii-encryption-and-audit.md → backend/src/core/security.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Finalized Production Stack Components** — docs_decisions_adr_007_finalized_stack_finalized_stack, docs_decisions_adr_007_finalized_stack_fly_io, docs_decisions_adr_007_finalized_stack_neon, docs_decisions_adr_007_finalized_stack_redis, docs_decisions_adr_007_finalized_stack_langfuse [EXTRACTED 1.00]
- **handle_turn() Per-Turn Pipeline** — spec_hand_rolled_dispatcher, docs_decisions_adr_008_system_1_decision_layer_decide, docs_decisions_adr_005_three_layer_guardrails_three_layer_guardrails, docs_decisions_adr_004_memory_architecture_episodic_memory, spec_code_owns_the_money [EXTRACTED 1.00]
- **System-1 Decision Engine (decide + primitives + models)** — docs_decisions_adr_008_system_1_decision_layer_system_1_decision_layer, docs_decisions_adr_008_system_1_decision_layer_decide, docs_research_system_1_decision_models_laya_jev_choice, docs_research_system_1_decision_models_laya_jev_score, docs_research_system_1_decision_models_laya_jev_noul, docs_research_system_1_decision_models_laya_jev_laya [EXTRACTED 1.00]
- **AdmitFlow AI Core Architecture** — tasks_plan_conversation_engine, tasks_plan_decide_decision_layer, tasks_plan_three_layer_guardrails, tasks_plan_rag_pipeline [INFERRED 0.85]
- **WhatsApp Ingress → Worker → Engine Flow** — tasks_plan_fastapi_webhook, tasks_plan_redis, tasks_plan_taskiq, tasks_plan_conversation_engine [INFERRED 0.85]

## Communities (145 total, 17 thin omitted)

### Community 0 - "ADR-008: System-1 Decision Layer (Laya / Jev)"
Cohesion: 0.18
Nodes (17): ADR-001: Hybrid Architecture, ADR-004: Dual Memory Architecture, Episodic Memory (messages table), Semantic Memory (lead_facts table), ADR-005: Three-Layer Guardrails and RAG, Three-Layer Guardrails, ADR-007: Finalized Production Stack, ADR-008: System-1 Decision Layer (Laya / Jev) (+9 more)

### Community 1 - "Conversation Engine (hand-rolled dispatcher)"
Cohesion: 0.25
Nodes (8): Conversation Engine (hand-rolled dispatcher), System-1 decide() Decision Layer, FastAPI WhatsApp Webhook, Langfuse LLM Tracing, pgvector RAG Pipeline, Redis (mutex / dedup / rate-limit), TaskIQ Background Worker, Three-Layer Guardrails

### Community 2 - "AdmitFlow Complete Specification"
Cohesion: 0.17
Nodes (10): AI Impact Statement, Student-to-staff demonstration, Prior-work disclosure draft, AdmitFlow necessary resources, Planning baseline before Telegram alignment, AdmitFlow institution knowledge workspace, AdmitFlow Complete Specification, AdmitFlow Platform (+2 more)

### Community 3 - "Finalized Production Stack"
Cohesion: 0.18
Nodes (11): ADR-002: Webhook Concurrency and Deduplication, Per-Phone Redis Mutex, Webhook Deduplication (Redis SETNX), ADR-003: Multi-Tenancy Strategy, Multi-Tenancy (Row-Level Isolation), Finalized Production Stack, Fly.io (Backend + Worker + Scheduler), Langfuse Cloud (LLM Tracing) (+3 more)

### Community 4 - "engine/applications.py"
Cohesion: 0.16
Nodes (19): action(), application_action(), collect_application(), prompt(), Any, AsyncSession, Explicit, encrypted, deterministic application collection in a private…, Button (+11 more)

### Community 5 - "guardrails.py"
Cohesion: 0.09
Nodes (34): apply_whatsapp_formatting(), check_input_safety(), check_output_safety(), _deterministic_check(), InputGuardrailResult, LLMGuardrailResponse, LLMOutputGuardrailResponse, OutputGuardrailResult (+26 more)

### Community 6 - "Code Owns the Money"
Cohesion: 0.50
Nodes (5): ADR-006: Code-Owned Qualification and Payments, Intent: Admissions Flow and Discounts, Discount Codes, Code Owns Eligibility, Code Owns the Money

### Community 7 - "LeadStatus"
Cohesion: 0.20
Nodes (28): LeadStatus, Lead lifecycle states (SPEC §7.3). Where a lead *stands*, not a fixed track —…, Lead, A prospective applicant with optional phone contact and channel identities.…, resumed_status(), Event, answer_question(), build_reply() (+20 more)

### Community 8 - "RedisMutex"
Cohesion: 0.08
Nodes (26): MutexAcquireError, Redis, RuntimeError, Background loop that extends the TTL while the lock is held., Raised when the mutex cannot be acquired after all retries., Async context-manager mutex backed by Redis ``SET NX``. Parameters: redis: An…, Attempt to acquire the lock, retrying up to ``retry_count`` times., Release the lock using the Lua CAS script (owner-safe). (+18 more)

### Community 9 - "journey.py"
Cohesion: 0.09
Nodes (32): ExtractedFact, Extraction, GroundedQuote, Interpretation, BaseModel, Persistent Telegram admissions journey with code-owned outcomes and quoted…, AllProvidersFailedError, generate_completion() (+24 more)

### Community 10 - "WhatsAppSender"
Cohesion: 0.06
Nodes (32): Five bounded live embedding searches through the real authenticated staff API., Hash the tested code/configuration without reading secrets or runtime data., Any, RuntimeError, WhatsApp message sending service (Task 6). Uses httpx2 to call the Meta Graph…, Send an interactive list message. `sections` is a list of section dicts…, Send a pre-approved template message., Raised when the Meta Cloud API returns an error response. (+24 more)

### Community 11 - "tasks/processing.py"
Cohesion: 0.12
Nodes (15): ping(), process_inbound_message(), Any, task, Background tasks for message processing. For now this module holds only the…, Smoke-test task: returns ``{"result": payload}``. Enqueued from the…, Process an inbound WhatsApp message (Task 17). This is a placeholder for the…, Tests for the TaskIQ broker setup and task execution (Task 3). All tests run… (+7 more)

### Community 12 - "get_redis"
Cohesion: 0.12
Nodes (18): get_redis(), Redis, RuntimeError, Shared async Redis client for application code. Carry-over prerequisite #1: the…, Raised when Redis is needed but ``REDIS_URL`` is unset in settings., Return the process-wide async Redis client singleton. The client is created…, RedisNotConfiguredError, post (+10 more)

### Community 13 - "core/rag.py"
Cohesion: 0.06
Nodes (43): chunk_text(), embed_text(), ingest_document(), Any, AsyncSession, UUID, RAG pipeline core logic (Task 13). Handles ingestion (chunking, embedding),…, Hybrid search (dense + lexical with RRF). (+35 more)

### Community 16 - "get_settings"
Cohesion: 0.09
Nodes (25): AsyncBroker, get_settings(), Application settings singleton. Loads configuration from the environment (and…, Return the process-wide :class:`Settings` singleton., Bounded OpenAI-only model roles; provider details never escape in errors., _build_broker(), TaskIQ broker singleton. In production (and local dev with Redis running) the…, Construct the right broker based on the current settings. This is a plain… (+17 more)

### Community 17 - "admissions.tsx"
Cohesion: 0.14
Nodes (13): Admissions(), Detail, Human, Inquiry, labels, Request, RuleEvidence, statusLabel() (+5 more)

### Community 18 - "dispatcher.py"
Cohesion: 0.16
Nodes (12): Redis distributed mutex with owner-safe release and keepalive (Task 7). Ensures…, MessageDirection, Direction of a WhatsApp message row (episodic memory, ADR-004)., _flush_engine_state(), _load_engine_state(), AsyncSession, Engine Dispatcher (Task 8 & 17). This module contains the main entry point for…, Load EngineState from DB records. (+4 more)

### Community 19 - "Settings"
Cohesion: 0.11
Nodes (22): Environment-backed application configuration., Settings, hash_telegram_identifier(), UUID, Private Telegram identity lookup without storing raw identifiers in indexes., Hash an identifier in its tenant/bot/type domain using the lookup secret. This…, configured_keys(), fixture (+14 more)

### Community 20 - "AIBoomi Startup Weekend Kochi: fresh-session context"
Cohesion: 0.11
Nodes (19): AIBoomi Startup Weekend Kochi: fresh-session context, Assessment and next decision, Current readiness session (October 22), Event sources and local copies, Existing prototype rule and surprise element, Existing working-tree changes, Fresh-message prompt, Handoff status (+11 more)

### Community 21 - "Reply"
Cohesion: 0.20
Nodes (22): Trusted bot-to-institution mapping; token is application-encrypted., TelegramBot, BaseModel, Reply, discount_action(), order_reply(), payment_action(), preview() (+14 more)

### Community 22 - "TestClient"
Cohesion: 0.19
Nodes (8): Any, TestClient, Statuses (read/delivered) have no 'messages' array., GET /api/webhook challenge verification., POST /api/webhook payload processing., sign_payload(), TestWebhookProcessing, TestWebhookVerification

### Community 23 - "sqlalchemy"
Cohesion: 0.09
Nodes (21): alembic, alembic_config, Application-layer PII protection: symmetric encryption + deterministic hashing.…, ConversationEvent, Human-readable callback summaries without exposing routing or signature details., Institution document extraction, durable ingestion and retrieval., Authenticated, audited lead/conversation access and explicit human-request…, Durable deliveries for explicit staff replies, payment events and consented… (+13 more)

### Community 24 - "EngineState"
Cohesion: 0.07
Nodes (48): Qualification-rule comparison operators (SPEC §7.4). Evaluated…, RuleOperator, ExtractionResponse, AsyncSession, BaseModel, Qualification Node (Task 15). Extracts rule fields using the LLM and runs…, Structured output expected from the LLM when extracting fields., Run the qualification loop. (+40 more)

### Community 25 - "Stages"
Cohesion: 0.13
Nodes (15): 10. Reflect & learn, 1. Understand & spec  (`/spec`), 2. Plan & pick a task  (`/plan`), 3. Branch, 4. Build with TDD  (`/build`, `/test`), 5. Verify (the quality gate), 6. Self-review, then adversarial review  (`/review`), 7. Commit & open the PR (+7 more)

### Community 26 - "test_telegram_journey.py"
Cohesion: 0.10
Nodes (20): QualificationRule, A structured eligibility rule evaluated in code, not by the LLM (ADR-006).…, Any, Encrypted explicit application collection, replay safety and tenant-scoped…, test_concurrent_reviews_allocate_one_seat_and_repeated_approval_is_idempotent(), send(), completion(), journey() (+12 more)

### Community 28 - "run_postman_check.cjs"
Cohesion: 0.18
Nodes (9): collection, config, crypto, fs, keys, newman, path, root (+1 more)

### Community 29 - "Task List"
Cohesion: 0.15
Nodes (13): Checkpoint: Advanced Features, Checkpoint: AI Core, Checkpoint: Dashboard Complete, Checkpoint: Foundation, Checkpoint: Production Ready, Checkpoint: WhatsApp Ingress, Phase 1: Foundation, Phase 2: WhatsApp Ingress (+5 more)

### Community 30 - "TelegramClient"
Cohesion: 0.14
Nodes (16): Any, RuntimeError, TelegramAPIError, TelegramClient, Any, MonkeyPatch, test_outbound_dedup_claims_order_and_uncertainty(), deliver() (+8 more)

### Community 31 - "test_migrations.py"
Cohesion: 0.23
Nodes (11): _alembic_config(), monkeypatch_session(), pg_url(), fixture, MonkeyPatch, Migration + schema integration tests against real Postgres. Spins up…, Start Postgres, point settings at it, yield the asyncpg URL., The tier requirement: alembic upgrade head then downgrade base, both clean. (+3 more)

### Community 32 - "Phase 5: Dashboard Frontend (Next.js)"
Cohesion: 0.05
Nodes (44): AdmitFlow — Task List, AIBoomi Startup Weekend session handoff (2026-10-22), Current direction and hackathon resources (2026-10-23), Final Postman diagnostic (October 23, executed; delivery blocked), Phase 1: Foundation, Phase 3–4 addition (see ADR-008), Phase 4: Advanced Bot Features, Phase 5: Dashboard Frontend (Next.js) (+36 more)

### Community 33 - "management.py"
Cohesion: 0.14
Nodes (37): require_admin(), archive_course(), archive_discount(), BatchInput, catalog(), catalog_detail(), course_view(), CourseInput (+29 more)

### Community 34 - "Code Standards"
Cohesion: 0.18
Nodes (11): Async & I/O, Code Standards, Configuration — settings, not literals, Dependencies, Errors, Formatting, LLM calls, Logging & observability (+3 more)

### Community 35 - "normalize_e164"
Cohesion: 0.19
Nodes (5): normalize_e164(), Normalize *raw* into canonical E.164 (``+<digits>``). Strips whitespace,…, normalize_e164 → canonical E.164 string., Meta's ``wa_id`` format: digits-only, no ``+``., TestNormalizeE164

### Community 36 - "Event preparation and execution plan"
Cohesion: 0.18
Nodes (11): Business and mentor preparation, Evaluation and demo evidence, Event preparation and execution plan, Kickoff disclosure draft, Latest direction (October 23), Minimum demonstrable product, Next action: one-hour v1 readiness check, Submission checklist (+3 more)

### Community 37 - "7. Core Feature Specifications"
Cohesion: 0.18
Nodes (11): 7.10 Payment Integration & Discounts (Razorpay), 7.1 WhatsApp Number Architecture, 7.2 Multi-Tenancy (Row-Level Isolation), 7.3 Lead Lifecycle States, 7.4 Course Qualification Rules (Structured), 7.5 Batch & Intake Management, 7.6 Cold Lead Re-engagement, 7.7 Language Support (+3 more)

### Community 38 - "typing"
Cohesion: 0.10
Nodes (30): asyncio, DiscountType, PaymentStatus, Enumerated types used across the schema. These are Python ``str`` enums mapped…, How a discount code reduces the fee., Payment order lifecycle (SPEC §7.10)., PaymentOrder, A Razorpay order for an application fee (SPEC §7.10). Amount is DB-sourced… (+22 more)

### Community 39 - "main.py"
Cohesion: 0.10
Nodes (17): create_app(), ready(), lifespan(), FastAPI, FastAPI application entry point. Boots the API, manages the TaskIQ broker…, Start / stop the TaskIQ broker alongside the FastAPI process. The…, Application factory — builds and configures the FastAPI instance., Tests for the /debug endpoints (Task 3 verification). (+9 more)

### Community 40 - "auth.py"
Cohesion: 0.16
Nodes (20): Login, logout(), me(), BaseModel, Db, get, post, Request (+12 more)

### Community 41 - "operations.py"
Cohesion: 0.14
Nodes (27): course_options(), get_lead(), human_requests(), lead_detail(), leads(), Any, Db, get (+19 more)

### Community 42 - "Hackathon resources for AdmitFlow"
Cohesion: 0.20
Nodes (10): Acceptance before using a resource, Event and release boundaries, Goal, Hackathon resources for AdmitFlow, October 23 Downloads guide: hosted inference access, Participant credits and other support, Suggested allocation and activation order, Useful resources mapped to the plan (+2 more)

### Community 43 - "manifest.json"
Cohesion: 0.20
Nodes (9): SPEC.md, bytes, sha256, tasks/plan.md, bytes, sha256, tasks/todo.md, bytes (+1 more)

### Community 44 - "test_workspace_limits.py"
Cohesion: 0.08
Nodes (23): ASGIApp, Reject oversized multipart streams before they can fill temporary storage., UploadBodyLimit, Staff authentication and institution-scoped access., check_login_limit(), Request, Bounded login throttling; shared Redis when configured, development fallback., isolated_local_login_windows() (+15 more)

### Community 45 - "AdmitFlow: current state and planning baseline"
Cohesion: 0.22
Nodes (9): AdmitFlow: current state and planning baseline, Confirmed user direction, Feature status and integration gaps, Features to finalize next, How to reconcile the planning documents, Proposed architecture for the next plan, Stack inventory, Verification evidence and its limits (+1 more)

### Community 46 - "AdmitFlow: AIBoomi submission plan"
Cohesion: 0.22
Nodes (9): AdmitFlow: AIBoomi submission plan, Deck and presentation, Open decisions, Proposed schedule from Friday evening, Submission outcome, The journey to demonstrate, Use the provided resources, What must be handed in (+1 more)

### Community 47 - "AdmitFlow — Complete Specification"
Cohesion: 0.12
Nodes (16): 12. Edge Cases & Error Handling, 14. Data Privacy (DPDPA-Ready), 15. Memory Architecture, 16. Success Criteria, 17.1 Conversation engine — DECIDED: hand-rolled dispatcher, 17.2 Still open, 17. Decisions & Open Questions, 1. Objective (+8 more)

### Community 48 - "13. Dashboard Features"
Cohesion: 0.22
Nodes (9): 13.1 Authentication, 13.2 Roles & Permissions, 13.3 UI Aesthetic, 13.4 Real-Time Notifications, 13.5 Funnel Analytics, 13.6 Data Export & Integration, 13.7 Document Management (RAG), 13.8 Onboarding (MVP) (+1 more)

### Community 49 - "PaymentLink"
Cohesion: 0.36
Nodes (7): PaymentLink, field_validator, Any, MonkeyPatch, test_ambiguous_creation_is_not_repeated(), test_immutable_request_and_concurrent_jobs_create_one_link(), create()

### Community 50 - "ADR-011: Advanced RAG Strategy (Latency vs Precision)"
Cohesion: 0.25
Nodes (7): 1. Complex Document Ingestion (`docling` or `unstructured`), 2. Pluggable Reranking Architecture (Cohere API over Local CPU), 3. Contextual Query Rewriting, ADR-011: Advanced RAG Strategy (Latency vs Precision), Consequences, Context, Decision

### Community 51 - "Testing"
Cohesion: 0.25
Nodes (8): Coverage, LLM and decision-layer tests, Philosophy — pragmatic TDD, Running tests, Test layout, Testing, The two patterns, Unit vs integration

### Community 52 - "get_engine"
Cohesion: 0.16
Nodes (14): AsyncEngine, get_engine(), Return the process-wide async engine (one pool for the app)., main(), run(), migrated_db(), fixture, Start Postgres, point settings at it, migrate to head; tear down after. (+6 more)

### Community 53 - "AdmitFlow project handoff"
Cohesion: 0.25
Nodes (8): AdmitFlow project handoff, Current direction, Development rules, Event submission, Execution checkpoint, First usable release, Historical evidence, Resume prompt

### Community 54 - "detect_intent"
Cohesion: 0.20
Nodes (15): detect_intent(), Classify the user's intent to route to the correct node. Design Decision: If a…, asyncio, Test routing for course discovery., Test routing for knowledge questions., Test routing for qualification answers., Test routing for human handoff., Test routing for empty messages without calling LLM defaults to discovery. (+7 more)

### Community 55 - "hash_phone"
Cohesion: 0.14
Nodes (14): hash_phone(), Return a deterministic keyed hash of a phone number for lookup/dedup. Keyed…, DatabaseNotConfiguredError, RuntimeError, Raised when a DB session is requested but ``DATABASE_URL`` is unset., test_hash_phone_differs_per_number(), test_hash_phone_is_deterministic(), test_hash_phone_is_not_plaintext_and_fits_column() (+6 more)

### Community 56 - "knowledge/processing.py"
Cohesion: 0.13
Nodes (26): extract_file(), ExtractionError, ValueError, Bounded extraction of institution reference documents; never execute uploads., A safe, public error code rather than parser output containing document text., validate_path(), dispatch_pending(), process_upload() (+18 more)

### Community 57 - "test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment"
Cohesion: 0.19
Nodes (10): payments(), Any, get, Any, MonkeyPatch, test_absent_link_does_not_clear_uncertainty_or_authorize_retry(), test_known_configuration_failure_can_only_requeue_same_bounded_invoice(), test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment() (+2 more)

### Community 58 - "copilot.py"
Cohesion: 0.19
Nodes (16): content(), decide(), DraftContent, DraftDecision, DraftRequest, generate(), latest(), Any (+8 more)

### Community 59 - "ADR-010: Triage Fallback Routing (Anti-Spam)"
Cohesion: 0.33
Nodes (5): ADR-010: Triage Fallback Routing (Anti-Spam), Consequences, Context, Decision, Status

### Community 60 - "ADR-012: Telegram and OpenAI for the first complete admissions MVP"
Cohesion: 0.29
Nodes (7): ADR-012: Telegram and OpenAI for the first complete admissions MVP, Consequences, Context, Decision, Implemented runtime boundaries, References and verification, Supersession and preserved decisions

### Community 61 - "test_staff_operations.py"
Cohesion: 0.16
Nodes (17): inbound(), prepare(), Any, MonkeyPatch, parametrize, UUID, Staff takeover pauses bot replies; explicit sends are scoped, durable and…, test_clear_escalation_records_request_outside_hours_without_a_model() (+9 more)

### Community 62 - "2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md"
Cohesion: 0.25
Nodes (4): Architecture Decisions, Implementation Plan: AdmitFlow, Overview, Risks and Mitigations

### Community 63 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 64 - "institution.py"
Cohesion: 0.10
Nodes (33): argparse, Dashboard access role (SPEC — admin vs agent)., StaffRole, Batch, Course, A program a lead can be qualified for and pay to apply to., A dated intake of a course with finite seats (SPEC §7.5)., Institution (+25 more)

### Community 65 - "11. Human-in-the-Loop (Full Workflow)"
Cohesion: 0.40
Nodes (5): 11.1 Auto-Escalation Triggers, 11.2 Co-pilot Mode, 11.3 Business Hours, 11.4 Never Escalate, 11. Human-in-the-Loop (Full Workflow)

### Community 66 - "test_escalation.py"
Cohesion: 0.23
Nodes (10): escalation_reason(), office_open(), datetime, Reason, Deterministic clear support signals and institution-local office hours., parametrize, Clear support signals escalate; office hours never promise an immediate reply., test_clear_escalation_signals() (+2 more)

### Community 67 - "api.py"
Cohesion: 0.18
Nodes (20): documents(), get_upload(), Any, BaseModel, Db, delete, get, post (+12 more)

### Community 68 - "AdmitFlow Backend"
Cohesion: 0.20
Nodes (10): AdmitFlow Backend, Application payments, Configuration, Current implementation and verification, Institution knowledge workspace, Local development, Stack, Staff takeover and reviewed co-pilot (+2 more)

### Community 69 - "identity_database"
Cohesion: 0.36
Nodes (8): identity_database(), fixture, Use a disposable pgvector database; never mutate the demo database., test_downgrade_preserves_legacy_rows_and_refuses_to_destroy_telegram_data(), insert_rows(), inspect_and_clean(), remove_test_bot(), verify_legacy()

### Community 70 - "RazorpayClient"
Cohesion: 0.14
Nodes (16): AsyncBaseTransport, Credentials, PaymentProviderError, BaseModel, Exception, Read an existing exact reference; absence never authorizes another creation., RazorpayClient, provision() (+8 more)

### Community 71 - "Official source snapshots"
Cohesion: 0.50
Nodes (4): Conflicts to confirm, October 23 planning refresh, Official source snapshots, Sources

### Community 72 - "telegram/service.py"
Cohesion: 0.17
Nodes (22): async_sessionmaker, get_session(), get_sessionmaker(), AsyncSession, Async engine and session factory. Built lazily from ``settings.database_url``…, Return the process-wide async session factory., FastAPI dependency yielding a session that closes after the request., recover_payments() (+14 more)

### Community 73 - "10. Observability & Tracing"
Cohesion: 0.50
Nodes (4): 10.1 LLM Tracing (Langfuse), 10.2 Structured Logging, 10.3 Error Monitoring (Sentry), 10. Observability & Tracing

### Community 74 - "2. Boundaries & Invariants"
Cohesion: 0.50
Nodes (4): 2. Boundaries & Invariants, Always Do, Ask First, Never Do

### Community 75 - "adapter.py"
Cohesion: 0.20
Nodes (9): normalize_update(), protect_logs(), Strict private-chat normalization and token-safe Telegram HTTP transport., TaskIQ changes log levels; redact before either HTTP client or root handlers…, TokenSafeFilter, test_callback_actor_and_origin(), test_http_logs_redact_bot_credentials(), test_private_normalization_and_media() (+1 more)

### Community 76 - "management.tsx"
Cohesion: 0.14
Nodes (10): Batch, Course, empty, Management(), operators, parseValue(), Rule, Settings (+2 more)

### Community 77 - "8. RAG (Retrieval-Augmented Generation)"
Cohesion: 0.50
Nodes (4): 8.1 Per-Institution Knowledge Base, 8.2 Retrieval Pipeline, 8.3 RAG Guardrail, 8. RAG (Retrieval-Augmented Generation)

### Community 78 - "AdmitFlow execution and demonstration checklist"
Cohesion: 0.67
Nodes (3): AdmitFlow execution and demonstration checklist, Build and verify, Demonstrate and submit

### Community 79 - "test_dispatcher.py"
Cohesion: 0.29
Nodes (6): Any, asyncio, fixture, patch, sample_whatsapp_payload(), test_handle_turn_basic_flow()

### Community 84 - "receiver.py"
Cohesion: 0.31
Nodes (9): main(), provision_bot(), UUID, One advisory-locked long poller per bot, with durable offsets and queue…, recovery(), run(), accept_update(), Any (+1 more)

### Community 89 - "encrypt_pii"
Cohesion: 0.14
Nodes (24): Core cross-cutting concerns: settings, security, schemas, guardrails, tracing., decrypt_pii(), encrypt_pii(), Encrypt a PII string, returning a url-safe base64 Fernet token. Fernet is…, Decrypt a token produced by :func:`encrypt_pii`. Raises…, change_then_reply(), expire(), cancel_then_fail() (+16 more)

### Community 90 - "AdmitFlow"
Cohesion: 0.33
Nodes (6): AdmitFlow, Current status, Demonstration and submission, Development, Product scope, Stack

### Community 91 - "models/__init__.py"
Cohesion: 0.11
Nodes (45): Base, IdMixin, Declarative base, metadata naming convention, and shared column mixins. Every…, Declarative base shared by every AdmitFlow model., UUID primary key with an application-side default. UUIDs avoid cross-tenant…, Server-side created/updated timestamps., Row-level tenant scoping (ADR-003). Mixed into every tenant-scoped table., TenantMixin (+37 more)

### Community 92 - "test_payment_contracts.py"
Cohesion: 0.23
Nodes (10): Bounded Razorpay requests; ambiguous link creation is never blindly retried., discounted_amount(), Integer monetary arithmetic and exact-byte webhook authentication., verify_webhook(), Money stays integer/code-owned; signatures use exact bytes; creation never…, test_discounts_use_minor_units_and_boundaries(), test_webhook_signature_uses_raw_body_and_rejects_tampering(), hmac (+2 more)

### Community 93 - "test_webhook.py"
Cohesion: 0.29
Nodes (7): test_tunnel_app_keeps_webhook_verification(), app(), client(), mock_settings(), FastAPI, fixture, Tests for the Meta WhatsApp webhook endpoints (Task 5).

### Community 94 - "handle_turn"
Cohesion: 0.15
Nodes (14): handle_turn(), Any, Process a single turn of conversation., Phase 3: AI Core (Engine + RAG), Task 10: Input guardrail node, Task 11: Triage node (intent detection), Task 12: Discovery node, Task 13: RAG pipeline (+6 more)

### Community 95 - "evaluate_faq.py"
Cohesion: 0.33
Nodes (10): Case, cases(), evaluate(), main(), BaseModel, Bounded live FAQ evaluation on the fictional demo tenant; no messages or writes., score_answer(), Evaluation rejects irrelevant quotations and does not count provider errors as… (+2 more)

### Community 96 - "Git & GitHub Workflow"
Cohesion: 0.22
Nodes (9): Branching model — feature branch → PR → `main`, Commits — Conventional Commits, small and coherent, Git & GitHub Workflow, Merging, No AI attribution — the human is the sole author  ⚠️, Pull Requests, Review gate — adversarial, before merge, What never gets committed (+1 more)

### Community 97 - "package.json"
Cohesion: 0.22
Nodes (8): name, private, version, react-dom, @types/node, @types/react, @types/react-dom, typescript

### Community 98 - "write_audit_log"
Cohesion: 0.23
Nodes (10): Any, AsyncSession, UUID, Audit-log write helper. :func:`write_audit_log` is the one path significant…, Append one entry to ``audit_logs`` on ``session``; return it flushed, not…, write_audit_log(), Unit test for the audit-log write helper. The real INSERT path (JSONB, server-…, test_write_audit_log_defaults_optional_fields() (+2 more)

### Community 99 - "record-demo.mjs"
Cohesion: 0.18
Nodes (7): credentials, headers, journey, target, ref_node_fs, ref_node_path, @playwright/test

### Community 100 - "AGENTS.md"
Cohesion: 0.25
Nodes (7): AIBoomi Startup Weekend handoff, How we build — read the handbook, Knowledge graph, Quick commands (from `backend/`), The rules you cannot skip, What this project is, Workflow triggers

### Community 101 - "Security & Production Readiness"
Cohesion: 0.18
Nodes (11): Dependency & secret scanning, Deploy & rollback, External surfaces, Guardrails & money, Local full-stack (docker-compose), Multi-tenancy — isolation is a correctness bug if wrong, Observability, PII & data protection (DPDPA) (+3 more)

### Community 102 - "pydantic"
Cohesion: 0.28
Nodes (8): embed_chunks(), Use the configured OpenAI model with the database's explicit 1536 dimensions., main(), Probe, BaseModel, Bounded live checks; print sanitized results without credentials or update…, validate(), pydantic

### Community 103 - "next-env.d.ts"
Cohesion: 0.50
Nodes (3): NOTE: This file should not be edited, frontend_next_types_root_params_d, frontend_next_types_routes_d

### Community 104 - "payments/webhook.py"
Cohesion: 0.18
Nodes (15): OutboundMessage, PaymentEvent, LinkEntity, LinkEnvelope, PaidEvent, PaidPayload, PaymentEntity, PaymentEnvelope (+7 more)

### Community 106 - "layout.tsx"
Cohesion: 0.25
Nodes (5): frontend_app_globals, metadata, config, @fontsource-variable/dm-sans, next

### Community 108 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, lint, record:demo, start, test:e2e:live, typecheck

### Community 109 - "Local Telegram/OpenAI runtime"
Cohesion: 0.25
Nodes (7): Configuration and data services, Delivery budget operation, Local Telegram/OpenAI runtime, Migrate and seed, Packaging and release limits, Run the processes, Validate and recover

### Community 110 - "AdmitFlow pitch deck copy"
Cohesion: 0.25
Nodes (7): AdmitFlow pitch deck copy, Slide 1: AdmitFlow, Slide 2: The admissions inquiry, Slide 3: A working student journey, Slide 4: Institution knowledge and control, Slide 5: Technology and verification, Slide 6: Pilot and next steps

### Community 111 - "decrypt_bytes"
Cohesion: 0.29
Nodes (8): decrypt_bytes(), encrypt_bytes(), _fernet(), Encrypt uploaded source bytes before persistence, without lossy text decoding., Authenticate and decrypt source bytes for an authorized ingestion task., readable_pdf(), test_upload_formats_search_duplicates_and_tenant_isolation(), index()

### Community 112 - "EncryptionKeyNotConfiguredError"
Cohesion: 0.25
Nodes (8): EncryptionKeyNotConfiguredError, RuntimeError, Raised when a PII helper is used but its key is unset in settings., payment_webhook(), Db, post, Request, UUID

### Community 113 - "timeline.py"
Cohesion: 0.17
Nodes (13): Cursor, Any, AsyncSession, BaseModel, datetime, field_validator, UUID, Bounded chronological transcript across inbound, replies and standalone… (+5 more)

### Community 114 - "Quality Gates — Definition of Done"
Cohesion: 0.33
Nodes (6): CI mirrors this exactly, Fast iteration vs the gate, Quality Gates — Definition of Done, The baseline gate (every change), The enforced-numbers ledger, The tiers — add gates by what the change touches

### Community 115 - "phone.py"
Cohesion: 0.33
Nodes (5): InvalidPhoneError, ValueError, E.164 phone-number normalization. Carry-over prerequisite #3: un-normalized…, Raised when a phone string cannot be normalized to E.164., Tests for E.164 phone normalization (carry-over prerequisite #3). The…

### Community 116 - "devDependencies"
Cohesion: 0.33
Nodes (6): devDependencies, @playwright/test, @types/node, @types/react, @types/react-dom, typescript

### Community 117 - "applications.tsx"
Cohesion: 0.25
Nodes (5): Applications(), Detail, fields, statuses, Summary

### Community 118 - "dependencies"
Cohesion: 0.40
Nodes (5): dependencies, @fontsource-variable/dm-sans, next, react, react-dom

### Community 119 - "hashlib"
Cohesion: 0.11
Nodes (18): log_delivery_status(), Request, Response, Expose only the existing Meta webhook through the temporary demo tunnel., Observe only authenticated status events, without recipient or error text., get, Response, WhatsApp Webhook routing (Task 5). Handles GET (challenge) and POST (incoming… (+10 more)

### Community 120 - ".__call__"
Cohesion: 0.33
Nodes (4): private_send(), Receive, Scope, Send

### Community 121 - "AdmitFlow submission requirements"
Cohesion: 0.50
Nodes (4): AdmitFlow submission requirements, Demonstration, Required artifacts, Truthful claims

### Community 122 - "send_outbound"
Cohesion: 0.40
Nodes (5): task, Encrypted outbound-message delivery jobs carry only internal identifiers., send_outbound_message(), UUID, send_outbound()

### Community 123 - "Alternatives Considered"
Cohesion: 0.50
Nodes (4): Alternatives Considered, Deterministic encryption of the phone number (so it is both stored and searchable), Full envelope encryption (per-tenant data keys wrapped by a master key), Rely on the provider's at-rest encryption only

### Community 124 - "reconcile"
Cohesion: 0.61
Nodes (8): locked(), owned(), provider(), Db, post, UUID, reconcile(), retry()

### Community 125 - "review"
Cohesion: 0.39
Nodes (9): applications(), detail(), owned(), Any, Db, get, post, UUID (+1 more)

### Community 126 - "budget.py"
Cohesion: 0.15
Nodes (23): day_window(), local_counts(), Any, datetime, UUID, Atomic daily send-attempt budgets shared by every Telegram delivery path., Count confirmed deliveries once; a stats failure must not repeat a sent message., record_sent() (+15 more)

### Community 127 - "payments/service.py"
Cohesion: 0.14
Nodes (20): ApplicationStatus, Application review status (SPEC §7.9 / lifecycle)., fee_details(), PaymentRequestError, process_payment(), AsyncSession, Course, UUID (+12 more)

### Community 128 - "payments.tsx"
Cohesion: 0.32
Nodes (6): label(), money(), outcomes, Payment, Payments(), statuses

### Community 129 - "Language review packet"
Cohesion: 0.67
Nodes (3): Current templates, Language review packet, Live exercise

### Community 130 - "react"
Cohesion: 0.29
Nodes (4): blank, Discount, Discounts(), react

### Community 131 - "Knowledge"
Cohesion: 0.46
Nodes (8): refresh(), api(), Knowledge(), action(), login(), search(), upload(), send()

### Community 132 - "pytest"
Cohesion: 0.13
Nodes (10): Telegram transport and tenant-scoped identity helpers., Both Telegram outboxes share the cap, defer durably and honor provider delays., Actual Redis Lua reservations must remain bounded under concurrent workers., test_budget_migration_preserves_existing_institution(), MonkeyPatch, Translate retrieval queries without weakening the relevance floor., test_english_query_does_not_call_model(), test_non_ascii_query_uses_validated_translation() (+2 more)

### Community 133 - "env.py"
Cohesion: 0.22
Nodes (9): do_run_migrations(), Alembic migration environment (async). Reads the database URL from application…, Emit SQL to stdout without a live DB connection., Run migrations against a live database via an async engine., run_migrations_offline(), run_migrations_online(), Connection, logging_config (+1 more)

### Community 135 - "test_failure_retry_and_delete_during_indexing"
Cohesion: 0.19
Nodes (11): fake_embeddings(), Any, MonkeyPatch, test_duplicate_claim_and_abandoned_attempt_recovery(), claims(), paused(), recover(), test_expired_session_rejected() (+3 more)

### Community 137 - "page.tsx"
Cohesion: 0.25
Nodes (6): DeliveryBudget(), Usage, Doc, errors, Match, Staff

### Community 139 - "5. Code Style"
Cohesion: 0.50
Nodes (4): 5. Code Style, Python (Backend), Separation of Concerns, TypeScript (Frontend)

### Community 143 - "signin"
Cohesion: 0.43
Nodes (7): Any, Real database management: administrator writes, role/tenant boundaries and…, test_catalog_writes_validate_rules_capacity_and_ownership(), test_discount_management_rejects_invalid_values_duplicates_and_foreign_writes(), test_settings_validate_timezone_hours_and_tenant_scope(), TestClient, signin()

### Community 144 - "add_institution_knowledge_workspace_b627da2f7e11.py"
Cohesion: 0.40
Nodes (4): Column, DateTime, _timestamps(), upgrade()

### Community 146 - "add_conversation_runtime_714f092da3b8.py"
Cohesion: 0.50
Nodes (3): columns(), Column, upgrade()

### Community 147 - "durable_payments_outbound_f129a064c5e8.py"
Cohesion: 0.50
Nodes (3): common(), Column, upgrade()

## Knowledge Gaps
- **398 isolated node(s):** `admitflow-backend`, `fs`, `path`, `crypto`, `root` (+393 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 965 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `get_settings()` connect `get_settings` to `engine/applications.py`, `env.py`, `pytest`, `LeadStatus`, `journey.py`, `WhatsAppSender`, `get_redis`, `core/rag.py`, `Settings`, `sqlalchemy`, `test_migrations.py`, `typing`, `main.py`, `auth.py`, `test_workspace_limits.py`, `get_engine`, `hash_phone`, `knowledge/processing.py`, `institution.py`, `api.py`, `RazorpayClient`, `telegram/service.py`, `receiver.py`, `evaluate_faq.py`, `pydantic`, `decrypt_bytes`, `hashlib`, `.__call__`, `reconcile`, `budget.py`, `payments/service.py`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Why does `handle_turn()` connect `handle_turn` to `institution.py`, `normalize_e164`, `guardrails.py`, `LeadStatus`, `RedisMutex`, `telegram/service.py`, `WhatsAppSender`, `tasks/processing.py`, `get_redis`, `core/rag.py`, `test_dispatcher.py`, `AdmitFlow — Complete Specification`, `dispatcher.py`, `detect_intent`, `hash_phone`, `EngineState`, `encrypt_pii`, `models/__init__.py`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Why does `WhatsApp readiness check — October 22, 2026` connect `core/rag.py` to `AdmitFlow Complete Specification`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `encrypt_pii()` (e.g. with `Consequences` and `Decision`) actually correct?**
  _`encrypt_pii()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 41 inferred relationships involving `LeadStatus` (e.g. with `Lead` and `application_action()`) actually correct?**
  _`LeadStatus` has 41 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Reply` (e.g. with `request_staff()` and `timeline()`) actually correct?**
  _`Reply` has 17 INFERRED edges - model-reasoned connections that need verification._
- **What connects `admitflow-backend`, `fs`, `path` to the rest of the system?**
  _398 weakly-connected nodes found - possible documentation gaps or missing edges._