# Graph Report - admitflow  (2026-10-24)

## Corpus Check
- 288 files · ~150,578 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 5, .example 2, .css 2)

## Summary
- 2568 nodes · 7099 edges · 172 communities (157 shown, 15 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 445 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d4971d1b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AdmitFlow Complete Specification
- Conversation Engine (hand-rolled dispatcher)
- AdmitFlow Task List
- Finalized Production Stack
- leads.py
- pydantic
- Code Owns the Money
- journey.py
- RedisMutex
- settings.py
- WhatsAppSender
- transport.py
- get_redis
- core/rag.py
- PII Encryption & Audit Log
- Razorpay Payment Integration
- get_settings
- admissions.tsx
- test_handle_turn_basic_flow
- Settings
- AIBoomi Startup Weekend Kochi: fresh-session context
- payments/service.py
- exports.py
- Course
- LeadStatus
- Stages
- decrypt_pii
- test_webhook.py
- run_postman_check.cjs
- Task List
- telegram/service.py
- test_crm_search.py
- Phase 5: Dashboard Frontend (Next.js)
- management.py
- Code Standards
- outreach/followups.py
- Event preparation and execution plan
- 7. Core Feature Specifications
- analytics
- main.py
- StaffUser
- operations.py
- Hackathon resources for AdmitFlow
- manifest.json
- test_workspace_limits.py
- AdmitFlow: current state and planning baseline
- AdmitFlow: AIBoomi submission plan
- AdmitFlow — Complete Specification
- normalize_e164
- age
- ADR-011: Required OpenAI passage reranking
- Testing
- check_input_safety
- AdmitFlow project handoff
- detect_intent
- EncryptionKeyNotConfiguredError
- RuleOperator
- seed
- generate
- ADR-010: Triage Fallback Routing (Anti-Spam)
- ADR-012: Telegram and OpenAI for the first complete admissions MVP
- prepare
- compilerOptions
- change_password
- TelegramBot
- reconcile
- api.py
- ExtractionError
- alembic
- RazorpayClient
- Official source snapshots
- get_engine
- test_telegram_contracts.py
- TelegramClient
- budget.py
- management.tsx
- sqlalchemy
- AdmitFlow Backend
- dispatcher.py
- verify.sh
- db/__init__.py
- src/__init__.py
- tasks/__init__.py
- analytics.tsx
- whatsapp/__init__.py
- integration/__init__.py
- admitflow-backend
- signin
- AdmitFlow
- models/__init__.py
- Reply
- test_decision_reranking.py
- crm.py
- evaluate
- Git & GitHub Workflow
- package.json
- encrypt_pii
- @playwright/test
- AGENTS.md
- Security & Production Readiness
- knowledge/processing.py
- next-env.d.ts
- payments/webhook.py
- process_rag_node
- layout.tsx
- frontend/AGENTS.md
- scripts
- backend/README.md
- AdmitFlow pitch deck copy
- test_qualification.py
- typing
- uuid
- Quality Gates — Definition of Done
- reranking.py
- devDependencies
- applications.tsx
- dependencies
- scheduler.py
- live
- README.md
- InputGuardrailResult
- reindex_names.py
- WhatsApp readiness check — October 22, 2026
- write_audit_log
- erase_inquiry
- Phase 3: AI Core (Engine + RAG)
- payments.tsx
- test_expired_lease_recovery_cap_and_configuration_cancellation
- react
- Knowledge
- test_local_runtime.py
- env.py
- test_shared_budget_preserves_queues_and_settings_wake_deliveries
- test_failure_retry_and_delete_during_indexing
- send_outbound
- page.tsx
- index_known_name
- process_inbound_message
- 13. Dashboard Features
- test_worker_broker.py
- AuditLog
- Phase 3–4 addition (see ADR-008)
- decrypt_bytes
- unittest_mock
- notifications.tsx
- AdmitFlow — Task List
- Implementation Plan: AdmitFlow
- staff/__init__.py
- inbound
- 11. Human-in-the-Loop (Full Workflow)
- record-demo.mjs
- event_for
- generate_completion
- 10. Observability & Tracing
- 2. Boundaries & Invariants
- 3. Tech Stack & Commands
- 5. Code Style
- 8. RAG (Retrieval-Augmented Generation)
- Phase 4: Advanced Bot Features
- test_ingest_document
- Phase 6: Production Hardening
- log_delivery_status
- 17. Decisions & Open Questions
- ConversationEvent
- test_schema_metadata.py
- Cursor
- WhatsApp readiness check (2026-10-22, in progress)
- TriageResponse
- event_dependencies

## God Nodes (most connected - your core abstractions)
1. `encrypt_pii()` - 104 edges
2. `write_audit_log()` - 95 edges
3. `get_settings()` - 91 edges
4. `LeadStatus` - 90 edges
5. `Lead` - 76 edges
6. `decrypt_pii()` - 75 edges
7. `Reply` - 73 edges
8. `TelegramBot` - 66 edges
9. `signin()` - 56 edges
10. `get_sessionmaker()` - 53 edges

## Surprising Connections (you probably didn't know these)
- `Task 4: PII encryption utilities and audit log infrastructure` --references--> `write_audit_log()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/db/audit.py
- `17.1 Conversation engine — DECIDED: hand-rolled dispatcher` --references--> `handle_turn()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/SPEC.md → backend/src/engine/dispatcher.py
- `Task 17: Wire webhook → TaskIQ → engine dispatcher → WhatsApp` --references--> `handle_turn()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/engine/dispatcher.py
- `Task 8: Engine state definition and lifecycle` --references--> `handle_turn()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/engine/dispatcher.py
- `7.4 Course Qualification Rules (Structured)` --references--> `age()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/SPEC.md → backend/tests/integration/test_followups.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Finalized Production Stack Components** — docs_decisions_adr_007_finalized_stack_finalized_stack, docs_decisions_adr_007_finalized_stack_fly_io, docs_decisions_adr_007_finalized_stack_neon, docs_decisions_adr_007_finalized_stack_redis, docs_decisions_adr_007_finalized_stack_langfuse [EXTRACTED 1.00]
- **handle_turn() Per-Turn Pipeline** — spec_hand_rolled_dispatcher, docs_decisions_adr_008_system_1_decision_layer_decide, docs_decisions_adr_005_three_layer_guardrails_three_layer_guardrails, docs_decisions_adr_004_memory_architecture_episodic_memory, spec_code_owns_the_money [EXTRACTED 1.00]
- **System-1 Decision Engine (decide + primitives + models)** — docs_decisions_adr_008_system_1_decision_layer_system_1_decision_layer, docs_decisions_adr_008_system_1_decision_layer_decide, docs_research_system_1_decision_models_laya_jev_choice, docs_research_system_1_decision_models_laya_jev_score, docs_research_system_1_decision_models_laya_jev_noul, docs_research_system_1_decision_models_laya_jev_laya [EXTRACTED 1.00]
- **AdmitFlow AI Core Architecture** — tasks_plan_conversation_engine, tasks_plan_decide_decision_layer, tasks_plan_three_layer_guardrails, tasks_plan_rag_pipeline [INFERRED 0.85]
- **WhatsApp Ingress → Worker → Engine Flow** — tasks_plan_fastapi_webhook, tasks_plan_redis, tasks_plan_taskiq, tasks_plan_conversation_engine [INFERRED 0.85]

## Communities (172 total, 15 thin omitted)

### Community 0 - "AdmitFlow Complete Specification"
Cohesion: 0.20
Nodes (18): ADR-001: Hybrid Architecture, ADR-004: Dual Memory Architecture, Episodic Memory (messages table), Semantic Memory (lead_facts table), ADR-005: Three-Layer Guardrails and RAG, Three-Layer Guardrails, ADR-007: Finalized Production Stack, ADR-008: System-1 Decision Layer (Laya / Jev) (+10 more)

### Community 1 - "Conversation Engine (hand-rolled dispatcher)"
Cohesion: 0.25
Nodes (8): Conversation Engine (hand-rolled dispatcher), System-1 decide() Decision Layer, FastAPI WhatsApp Webhook, Langfuse LLM Tracing, pgvector RAG Pipeline, Redis (mutex / dedup / rate-limit), TaskIQ Background Worker, Three-Layer Guardrails

### Community 2 - "AdmitFlow Task List"
Cohesion: 0.22
Nodes (10): Executed final check, One final WhatsApp check with Postman, AdmitFlow execution and demonstration checklist, Build and verify, Demonstrate and submit, AdmitFlow necessary resources, Planning baseline before Telegram alignment, AdmitFlow Platform (+2 more)

### Community 3 - "Finalized Production Stack"
Cohesion: 0.18
Nodes (11): ADR-002: Webhook Concurrency and Deduplication, Per-Phone Redis Mutex, Webhook Deduplication (Redis SETNX), ADR-003: Multi-Tenancy Strategy, Multi-Tenancy (Row-Level Isolation), Finalized Production Stack, Fly.io (Backend + Worker + Scheduler), Langfuse Cloud (LLM Tracing) (+3 more)

### Community 4 - "leads.py"
Cohesion: 0.25
Nodes (17): lead_summary(), Any, course_options(), get_lead(), human_requests(), lead_detail(), leads(), Any (+9 more)

### Community 5 - "pydantic"
Cohesion: 0.14
Nodes (19): decide(), Any, Typed decisions through the existing OpenAI-only provider boundary., Validate structured model output; refusal/malformed output is never a decision.…, AllProvidersFailedError, Exception, Raised when the entire LLM fallback chain is exhausted., apply_whatsapp_formatting() (+11 more)

### Community 6 - "Code Owns the Money"
Cohesion: 0.50
Nodes (5): ADR-006: Code-Owned Qualification and Payments, Intent: Admissions Flow and Discounts, Discount Codes, Code Owns Eligibility, Code Owns the Money

### Community 7 - "journey.py"
Cohesion: 0.14
Nodes (37): Lead, A prospective applicant with optional phone contact and channel identities.…, Event, escalation_reason(), Reason, answer_question(), build_reply(), button() (+29 more)

### Community 8 - "RedisMutex"
Cohesion: 0.08
Nodes (26): MutexAcquireError, Redis, RuntimeError, Background loop that extends the TTL while the lock is held., Raised when the mutex cannot be acquired after all retries., Async context-manager mutex backed by Redis ``SET NX``. Parameters: redis: An…, Attempt to acquire the lock, retrying up to ``retry_count`` times., Release the lock using the Lua CAS script (owner-safe). (+18 more)

### Community 9 - "settings.py"
Cohesion: 0.09
Nodes (24): alembic_config, Expose only the existing Meta webhook through the temporary demo tunnel., Application settings singleton. Loads configuration from the environment (and…, get_session(), Async engine and session factory. Built lazily from ``settings.database_url``…, FastAPI dependency yielding a session that closes after the request., Bounded live FAQ evaluation on the fictional demo tenant; no messages or writes., Background tasks for message processing. For now this module holds only the… (+16 more)

### Community 10 - "WhatsAppSender"
Cohesion: 0.09
Nodes (23): Any, Send an interactive list message. `sections` is a list of section dicts…, Send a pre-approved template message., Service for sending messages via Meta WhatsApp Cloud API., Post the payload to Meta and extract the created message ID., Meta API expects the phone number without the leading '+'., Send a simple text message. Returns the Meta message ID., Send an interactive message with up to 3 buttons. `buttons` should be a list of… (+15 more)

### Community 11 - "transport.py"
Cohesion: 0.08
Nodes (34): Durable, minimal institution events and signed outbound integrations., destination(), post_event(), PrivateTransportLogs, protect_logs(), public_ip(), LogRecord, HTTPS delivery pins a public resolved address while retaining TLS host… (+26 more)

### Community 12 - "get_redis"
Cohesion: 0.13
Nodes (16): get_redis(), Redis, RuntimeError, Shared async Redis client for application code. Carry-over prerequisite #1: the…, Raised when Redis is needed but ``REDIS_URL`` is unset in settings., Return the process-wide async Redis client singleton. The client is created…, RedisNotConfiguredError, post (+8 more)

### Community 13 - "core/rag.py"
Cohesion: 0.18
Nodes (15): chunk_text(), embed_text(), ingest_document(), Any, AsyncSession, UUID, RAG pipeline core logic (Task 13). Handles ingestion (chunking, embedding),…, Hybrid search (dense + lexical with RRF). (+7 more)

### Community 16 - "get_settings"
Cohesion: 0.11
Nodes (20): AsyncBroker, get_settings(), Return the process-wide :class:`Settings` singleton., _build_broker(), Construct the right broker based on the current settings. This is a plain…, get, Response, Handle Meta's webhook challenge. (+12 more)

### Community 17 - "admissions.tsx"
Cohesion: 0.12
Nodes (15): Admissions(), Detail, Human, Inquiry, labels, Request, RuleEvidence, statusLabel() (+7 more)

### Community 18 - "test_handle_turn_basic_flow"
Cohesion: 0.29
Nodes (6): Any, asyncio, fixture, patch, sample_whatsapp_payload(), test_handle_turn_basic_flow()

### Community 19 - "Settings"
Cohesion: 0.13
Nodes (26): hash_phone(), Return a deterministic keyed hash of a phone number for lookup/dedup. Keyed…, Environment-backed application configuration., Settings, configured_keys(), fixture, MonkeyPatch, Unit tests for application-layer PII protection (encrypt/decrypt + phone hash). (+18 more)

### Community 20 - "AIBoomi Startup Weekend Kochi: fresh-session context"
Cohesion: 0.11
Nodes (19): AIBoomi Startup Weekend Kochi: fresh-session context, Assessment and next decision, Current readiness session (October 22), Event sources and local copies, Existing prototype rule and surprise element, Existing working-tree changes, Fresh-message prompt, Handoff status (+11 more)

### Community 21 - "payments/service.py"
Cohesion: 0.20
Nodes (24): ApplicationStatus, PaymentStatus, Payment order lifecycle (SPEC §7.10)., Application review status (SPEC §7.9 / lifecycle)., discount_action(), order_reply(), payment_action(), preview() (+16 more)

### Community 22 - "exports.py"
Cohesion: 0.19
Nodes (14): clean(), Audited institution exports, with explicit limits and spreadsheet-safe text., render_csv(), render_xlsx(), crm_data(), fixture, Real database CRM lookup, index maintenance, export roles and isolation., test_search_scope_validation_and_audit() (+6 more)

### Community 23 - "Course"
Cohesion: 0.14
Nodes (19): Application, Structured application data collected from an admission-ready lead (SPEC §7.9).…, Batch, Course, QualificationRule, A program a lead can be qualified for and pay to apply to., A dated intake of a course with finite seats (SPEC §7.5)., A structured eligibility rule evaluated in code, not by the LLM (ADR-006).… (+11 more)

### Community 24 - "LeadStatus"
Cohesion: 0.11
Nodes (28): LeadStatus, Lead lifecycle states (SPEC §7.3). Where a lead *stands*, not a fixed track —…, EngineState, InvalidTransitionError, BaseModel, ValueError, Engine state definition (Task 8). Defines the plain dataclass/Pydantic model…, Safely transition the lead to a new lifecycle status. Raises:… (+20 more)

### Community 25 - "Stages"
Cohesion: 0.13
Nodes (15): 10. Reflect & learn, 1. Understand & spec  (`/spec`), 2. Plan & pick a task  (`/plan`), 3. Branch, 4. Build with TDD  (`/build`, `/test`), 5. Verify (the quality gate), 6. Self-review, then adversarial review  (`/review`), 7. Commit & open the PR (+7 more)

### Community 26 - "decrypt_pii"
Cohesion: 0.21
Nodes (12): decrypt_pii(), Decrypt a token produced by :func:`encrypt_pii`. Raises…, deliver(), dispatch_pending(), UUID, Leased at-least-once webhook delivery with stable recipient deduplication IDs., recovery_loop(), task (+4 more)

### Community 27 - "test_webhook.py"
Cohesion: 0.11
Nodes (19): parametrize, test_delivery_status_logs_are_authenticated_and_exclude_pii(), test_tunnel_app_exposes_no_other_routes(), test_tunnel_app_keeps_webhook_verification(), app(), client(), mock_settings(), Any (+11 more)

### Community 28 - "run_postman_check.cjs"
Cohesion: 0.20
Nodes (8): collection, config, crypto, fs, keys, newman, path, root

### Community 29 - "Task List"
Cohesion: 0.15
Nodes (13): Checkpoint: Advanced Features, Checkpoint: AI Core, Checkpoint: Dashboard Complete, Checkpoint: Foundation, Checkpoint: Production Ready, Checkpoint: WhatsApp Ingress, Phase 1: Foundation, Phase 2: WhatsApp Ingress (+5 more)

### Community 30 - "telegram/service.py"
Cohesion: 0.15
Nodes (27): async_sessionmaker, get_sessionmaker(), AsyncSession, Return the process-wide async session factory., recover_payments(), process_telegram_event(), task, Telegram inbox and outbox jobs contain only internal identifiers. (+19 more)

### Community 31 - "test_crm_search.py"
Cohesion: 0.19
Nodes (16): Core cross-cutting concerns: settings, security, schemas, guardrails, tracing., name_tokens(), normalized_phone(), UUID, query_tokens(), Tenant-keyed blind name prefixes; plaintext remains in encrypted columns only., token(), words() (+8 more)

### Community 32 - "Phase 5: Dashboard Frontend (Next.js)"
Cohesion: 0.17
Nodes (12): Phase 5: Dashboard Frontend (Next.js), Task 24: Initialize Next.js + dark mode + glassmorphism, Task 25: Authentication (email + password), Task 26: Dashboard home (funnel analytics), Task 27: Leads CRM page, Task 28: Course & batch management, Task 29: Chat takeover + co-pilot UI, Task 30: Document management (RAG) (+4 more)

### Community 33 - "management.py"
Cohesion: 0.12
Nodes (41): Any, get, Response, users(), require_admin(), archive_course(), archive_discount(), BatchInput (+33 more)

### Community 34 - "Code Standards"
Cohesion: 0.18
Nodes (11): Async & I/O, Code Standards, Configuration — settings, not literals, Dependencies, Errors, Formatting, LLM calls, Logging & observability (+3 more)

### Community 35 - "outreach/followups.py"
Cohesion: 0.06
Nodes (50): office_open(), datetime, Deterministic clear support signals and institution-local office hours., activity(), after_send(), before_send(), Check, course_available() (+42 more)

### Community 36 - "Event preparation and execution plan"
Cohesion: 0.18
Nodes (11): Business and mentor preparation, Evaluation and demo evidence, Event preparation and execution plan, Kickoff disclosure draft, Latest direction (October 23), Minimum demonstrable product, Next action: one-hour v1 readiness check, Submission checklist (+3 more)

### Community 37 - "7. Core Feature Specifications"
Cohesion: 0.18
Nodes (11): 7.10 Payment Integration & Discounts (Razorpay), 7.1 WhatsApp Number Architecture, 7.2 Multi-Tenancy (Row-Level Isolation), 7.3 Lead Lifecycle States, 7.4 Course Qualification Rules (Structured), 7.5 Batch & Intake Management, 7.6 Cold Lead Re-engagement, 7.7 Language Support (+3 more)

### Community 38 - "analytics"
Cohesion: 0.14
Nodes (21): alias, analytics(), bucket_dates(), count(), percent(), Period, period_window(), Any (+13 more)

### Community 39 - "main.py"
Cohesion: 0.10
Nodes (17): recovery_loop(), create_app(), lifespan(), FastAPI, FastAPI application entry point. Boots the API, manages the TaskIQ broker…, Start / stop the TaskIQ broker alongside the FastAPI process. The…, Application factory — builds and configures the FastAPI instance., Tests for the /debug endpoints (Task 3 verification). (+9 more)

### Community 40 - "StaffUser"
Cohesion: 0.16
Nodes (28): Dashboard access role (SPEC — admin vs agent)., StaffRole, A dashboard user (admin or agent) belonging to one institution., StaffUser, main(), provision(), Manually provision an institution administrator without printing credentials., admin_scope() (+20 more)

### Community 41 - "operations.py"
Cohesion: 0.21
Nodes (16): active_request(), finish_takeover(), ManualMessage, Any, AsyncSession, BaseModel, Db, field_validator (+8 more)

### Community 42 - "Hackathon resources for AdmitFlow"
Cohesion: 0.20
Nodes (10): Acceptance before using a resource, Event and release boundaries, Goal, Hackathon resources for AdmitFlow, October 23 Downloads guide: hosted inference access, Participant credits and other support, Suggested allocation and activation order, Useful resources mapped to the plan (+2 more)

### Community 43 - "manifest.json"
Cohesion: 0.20
Nodes (9): SPEC.md, bytes, sha256, tasks/plan.md, bytes, sha256, tasks/todo.md, bytes (+1 more)

### Community 44 - "test_workspace_limits.py"
Cohesion: 0.09
Nodes (19): ASGIApp, Reject oversized multipart streams before they can fill temporary storage., UploadBodyLimit, private_send(), check_login_limit(), Request, MonkeyPatch, Bound resource use and reject browser cross-origin mutations before database… (+11 more)

### Community 45 - "AdmitFlow: current state and planning baseline"
Cohesion: 0.22
Nodes (9): AdmitFlow: current state and planning baseline, Confirmed user direction, Feature status and integration gaps, Features to finalize next, How to reconcile the planning documents, Proposed architecture for the next plan, Stack inventory, Verification evidence and its limits (+1 more)

### Community 46 - "AdmitFlow: AIBoomi submission plan"
Cohesion: 0.22
Nodes (9): AdmitFlow: AIBoomi submission plan, Deck and presentation, Open decisions, Proposed schedule from Friday evening, Submission outcome, The journey to demonstrate, Use the provided resources, What must be handed in (+1 more)

### Community 47 - "AdmitFlow — Complete Specification"
Cohesion: 0.22
Nodes (9): 12. Edge Cases & Error Handling, 14. Data Privacy (DPDPA-Ready), 15. Memory Architecture, 16. Success Criteria, 1. Objective, 4. Project Structure, 6. Testing Strategy, 9. Guardrails (Three-Layer) (+1 more)

### Community 48 - "normalize_e164"
Cohesion: 0.14
Nodes (10): InvalidPhoneError, normalize_e164(), ValueError, E.164 phone-number normalization. Carry-over prerequisite #3: un-normalized…, Raised when a phone string cannot be normalized to E.164., Normalize *raw* into canonical E.164 (``+<digits>``). Strips whitespace,…, Tests for E.164 phone normalization (carry-over prerequisite #3). The…, normalize_e164 → canonical E.164 string. (+2 more)

### Community 49 - "age"
Cohesion: 0.11
Nodes (21): age(), outreach(), fixture, parametrize, seed(), test_exactly_two_reminders_then_cold_without_duplicate_delivery(), exercise(), test_existing_inquiries_upgrade_without_invented_consent() (+13 more)

### Community 50 - "ADR-011: Required OpenAI passage reranking"
Cohesion: 0.40
Nodes (4): ADR-011: Required OpenAI passage reranking, Decision, Separate retrieval work, Verification and tradeoffs

### Community 51 - "Testing"
Cohesion: 0.22
Nodes (9): Browser announcement regions, Coverage, LLM and decision-layer tests, Philosophy — pragmatic TDD, Running tests, Test layout, Testing, The two patterns (+1 more)

### Community 52 - "check_input_safety"
Cohesion: 0.18
Nodes (16): check_input_safety(), Check if the user input is safe to process. 1. Deterministic checks…, asyncio, Test output guardrail with safe content., Test output guardrail blocks hallucinated fee., Test that a clean message passes through., Test that profanity is blocked deterministically without calling the LLM., Test that simple injection heuristics are blocked deterministically. (+8 more)

### Community 53 - "AdmitFlow project handoff"
Cohesion: 0.25
Nodes (8): AdmitFlow project handoff, Current direction, Development rules, Event submission, Execution checkpoint, First usable release, Historical evidence, Resume prompt

### Community 54 - "detect_intent"
Cohesion: 0.20
Nodes (15): detect_intent(), Classify the user's intent to route to the correct node. Design Decision: If a…, asyncio, Test routing for course discovery., Test routing for knowledge questions., Test routing for qualification answers., Test routing for human handoff., Test routing for empty messages without calling LLM defaults to discovery. (+7 more)

### Community 55 - "EncryptionKeyNotConfiguredError"
Cohesion: 0.10
Nodes (21): EncryptionKeyNotConfiguredError, RuntimeError, Raised when a PII helper is used but its key is unset in settings., hash_telegram_identifier(), UUID, Hash an identifier in its tenant/bot/type domain using the lookup secret. This…, MonkeyPatch, parametrize (+13 more)

### Community 56 - "RuleOperator"
Cohesion: 0.19
Nodes (16): Qualification-rule comparison operators (SPEC §7.4). Evaluated…, RuleOperator, ExtractionResponse, BaseModel, Qualification Node (Task 15). Extracts rule fields using the LLM and runs…, Structured output expected from the LLM when extracting fields., _coerce_values(), evaluate_rule() (+8 more)

### Community 57 - "seed"
Cohesion: 0.09
Nodes (30): DiscountType, How a discount code reduces the fee., PaymentLink, BaseModel, field_validator, payments(), Any, get (+22 more)

### Community 58 - "generate"
Cohesion: 0.19
Nodes (14): content(), decide(), DraftContent, DraftDecision, DraftRequest, generate(), latest(), Any (+6 more)

### Community 59 - "ADR-010: Triage Fallback Routing (Anti-Spam)"
Cohesion: 0.33
Nodes (5): ADR-010: Triage Fallback Routing (Anti-Spam), Consequences, Context, Decision, Status

### Community 60 - "ADR-012: Telegram and OpenAI for the first complete admissions MVP"
Cohesion: 0.29
Nodes (7): ADR-012: Telegram and OpenAI for the first complete admissions MVP, Consequences, Context, Decision, Implemented runtime boundaries, References and verification, Supersession and preserved decisions

### Community 61 - "prepare"
Cohesion: 0.13
Nodes (17): prepare(), Any, MonkeyPatch, parametrize, test_clear_escalation_records_request_outside_hours_without_a_model(), exercise(), unavailable(), test_copilot_provider_failure_never_queues_a_message() (+9 more)

### Community 63 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 64 - "change_password"
Cohesion: 0.13
Nodes (24): change_password(), issue_session(), Login, logout(), me(), PasswordChange, AsyncSession, BaseModel (+16 more)

### Community 65 - "TelegramBot"
Cohesion: 0.17
Nodes (19): Trusted bot-to-institution mapping; token is application-encrypted., TelegramBot, action(), application_action(), collect_application(), prompt(), Any, AsyncSession (+11 more)

### Community 66 - "reconcile"
Cohesion: 0.61
Nodes (8): locked(), owned(), provider(), Db, post, UUID, reconcile(), retry()

### Community 67 - "api.py"
Cohesion: 0.10
Nodes (30): documents(), get_upload(), Any, BaseModel, Db, delete, get, post (+22 more)

### Community 68 - "ExtractionError"
Cohesion: 0.26
Nodes (15): extract_file(), ExtractionError, ValueError, Bounded extraction of institution reference documents; never execute uploads., A safe, public error code rather than parser output containing document text., validate_path(), parametrize, Untrusted institutional files must extract safely or fail explicitly. (+7 more)

### Community 69 - "alembic"
Cohesion: 0.05
Nodes (14): alembic, columns(), Column, upgrade(), Column, DateTime, _timestamps(), upgrade() (+6 more)

### Community 70 - "RazorpayClient"
Cohesion: 0.11
Nodes (23): AsyncBaseTransport, Credentials, PaymentProviderError, Exception, Bounded Razorpay requests; ambiguous link creation is never blindly retried., Read an existing exact reference; absence never authorizes another creation., RazorpayClient, discounted_amount() (+15 more)

### Community 71 - "Official source snapshots"
Cohesion: 0.50
Nodes (4): Conflicts to confirm, October 23 planning refresh, Official source snapshots, Sources

### Community 72 - "get_engine"
Cohesion: 0.13
Nodes (17): AsyncEngine, DatabaseNotConfiguredError, get_engine(), RuntimeError, Raised when a DB session is requested but ``DATABASE_URL`` is unset., Return the process-wide async engine (one pool for the app)., main(), run() (+9 more)

### Community 73 - "test_telegram_contracts.py"
Cohesion: 0.14
Nodes (22): cancel_queued(), note_inbound(), preference_reply(), Any, AsyncSession, datetime, Student-owned reminder preferences apply even while staff has paused the bot., normalize_update() (+14 more)

### Community 74 - "TelegramClient"
Cohesion: 0.13
Nodes (19): Any, RuntimeError, TelegramAPIError, TelegramClient, Any, MonkeyPatch, test_outbound_dedup_claims_order_and_uncertainty(), deliver() (+11 more)

### Community 75 - "budget.py"
Cohesion: 0.16
Nodes (22): day_window(), local_counts(), Any, datetime, UUID, Atomic daily send-attempt budgets shared by every Telegram delivery path., Count confirmed deliveries once; a stats failure must not repeat a sent message., record_sent() (+14 more)

### Community 76 - "management.tsx"
Cohesion: 0.10
Nodes (13): blank, Discount, Discounts(), Batch, Course, empty, Management(), operators (+5 more)

### Community 77 - "sqlalchemy"
Cohesion: 0.14
Nodes (23): Audit-log write helper. :func:`write_audit_log` is the one path significant…, Enumerated types used across the schema. These are Python ``str`` enums mapped…, Institution (the tenant root) and its staff users., Bounded chronological transcript across inbound, replies and standalone…, Idempotent synthetic institution/catalog/staff seed; no real applicant data., Tenant-scoped creation cohorts with explicit, observed conversion evidence., Audited application inspection and deterministic administrative review., Opaque database-backed staff sessions; no client-provided tenant authority. (+15 more)

### Community 78 - "AdmitFlow Backend"
Cohesion: 0.11
Nodes (17): Admissions analytics, AdmitFlow Backend, Application payments, Configuration, Consented follow-up reminders, Current implementation and verification, Institution knowledge workspace, Local development (+9 more)

### Community 79 - "dispatcher.py"
Cohesion: 0.13
Nodes (19): _flush_engine_state(), handle_turn(), _load_engine_state(), Any, AsyncSession, Engine Dispatcher (Task 8 & 17). This module contains the main entry point for…, Load EngineState from DB records., Flush mutations back to DB records. (+11 more)

### Community 84 - "analytics.tsx"
Cohesion: 0.28
Nodes (7): Analytics(), Conversion, labels, frontend_app_analytics_module, rate(), Report, shortDate()

### Community 89 - "signin"
Cohesion: 0.14
Nodes (18): Analytics preserve tenant scope, local dates, real denominators and…, test_all_aggregates_share_a_snapshot_during_concurrent_arrivals(), test_local_cohort_counts_conversions_and_observed_stages(), test_stage_audit_is_atomic_and_noop_updates_do_not_create_history(), exercise(), test_tenant_is_derived_from_session_and_period_is_bounded(), test_zero_filled_weekly_buckets_and_empty_rates(), test_downloads_roles_datasets_limits_and_tenants() (+10 more)

### Community 90 - "AdmitFlow"
Cohesion: 0.33
Nodes (6): AdmitFlow, Current status, Demonstration and submission, Development, Product scope, Stack

### Community 91 - "models/__init__.py"
Cohesion: 0.10
Nodes (29): MessageDirection, Direction of a WhatsApp message row (episodic memory, ADR-004)., PaymentOrder, A Razorpay order for an application fee (SPEC §7.10). Amount is DB-sourced…, ConversationMemory, OutboundMessage, PaymentEvent, ORM models package. Importing this package registers every model on… (+21 more)

### Community 92 - "Reply"
Cohesion: 0.13
Nodes (13): BaseModel, field_validator, Channel-neutral input and validated plain-text reply boundary., Reply, enqueue_outbound(), AsyncSession, UUID, Any (+5 more)

### Community 93 - "test_decision_reranking.py"
Cohesion: 0.22
Nodes (17): Reorder only original, safe tenant candidates; never invent text or sources.…, rerank(), chunks(), Intent, asyncio, BaseModel, MonkeyPatch, parametrize (+9 more)

### Community 94 - "crm.py"
Cohesion: 0.21
Nodes (13): lead_statement(), LeadFilters, LeadSearch, BaseModel, Select, UUID, Shared bounded CRM filters; search values never belong in URLs or audit details., download() (+5 more)

### Community 95 - "evaluate"
Cohesion: 0.33
Nodes (9): Case, cases(), evaluate(), main(), BaseModel, score_answer(), Evaluation rejects irrelevant quotations and does not count provider errors as…, test_supported_answer_requires_expected_fact_and_reference() (+1 more)

### Community 96 - "Git & GitHub Workflow"
Cohesion: 0.22
Nodes (9): Branching model — feature branch → PR → `main`, Commits — Conventional Commits, small and coherent, Git & GitHub Workflow, Merging, No AI attribution — the human is the sole author  ⚠️, Pull Requests, Review gate — adversarial, before merge, What never gets committed (+1 more)

### Community 97 - "package.json"
Cohesion: 0.22
Nodes (8): name, private, version, react-dom, @types/node, @types/react, @types/react-dom, typescript

### Community 98 - "encrypt_pii"
Cohesion: 0.15
Nodes (19): encrypt_pii(), Encrypt a PII string, returning a url-safe base64 Fernet token. Fernet is…, interleave(), test_search_pages_are_bounded_and_do_not_drop_or_repeat_records(), seed(), Any, test_fee_changes_require_another_tap_and_legacy_paid_orders_are_not_charged_again(), exercise() (+11 more)

### Community 99 - "@playwright/test"
Cohesion: 0.21
Nodes (5): ref_node_child_process, ref_node_crypto, ref_node_fs, ref_node_path, @playwright/test

### Community 100 - "AGENTS.md"
Cohesion: 0.25
Nodes (7): AIBoomi Startup Weekend handoff, How we build — read the handbook, Knowledge graph, Quick commands (from `backend/`), The rules you cannot skip, What this project is, Workflow triggers

### Community 101 - "Security & Production Readiness"
Cohesion: 0.18
Nodes (11): Dependency & secret scanning, Deploy & rollback, External surfaces, Guardrails & money, Local full-stack (docker-compose), Multi-tenancy — isolation is a correctness bug if wrong, Observability, PII & data protection (DPDPA) (+3 more)

### Community 102 - "knowledge/processing.py"
Cohesion: 0.16
Nodes (15): embed_chunks(), process_upload(), UUID, Durable upload claims, bounded embedding and atomic publication of ready…, Use the configured OpenAI model with the database's explicit 1536 dimensions., Claim once, process outside the transaction, then publish only the current…, main(), Probe (+7 more)

### Community 103 - "next-env.d.ts"
Cohesion: 0.50
Nodes (3): NOTE: This file should not be edited, frontend_next_types_root_params_d, frontend_next_types_routes_d

### Community 104 - "payments/webhook.py"
Cohesion: 0.27
Nodes (10): LinkEntity, LinkEnvelope, PaidEvent, PaidPayload, PaymentEntity, PaymentEnvelope, BaseModel, UUID (+2 more)

### Community 105 - "process_rag_node"
Cohesion: 0.33
Nodes (6): Sanitizer to prevent RAG poisoning. Blocks chunks that contain obvious prompt…, sanitize_chunks(), process_rag_node(), AsyncSession, RAG Node (Task 14). Graph node that retrieves from the knowledge base and…, Retrieve context and answer knowledge questions.

### Community 106 - "layout.tsx"
Cohesion: 0.25
Nodes (5): frontend_app_globals, metadata, config, @fontsource-variable/dm-sans, next

### Community 108 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, lint, record:demo, start, test:e2e:live, typecheck

### Community 109 - "backend/README.md"
Cohesion: 0.10
Nodes (17): Isolated full-stack Compose, Outbound integrations and live notifications, Staff access and privacy operations, Typed OpenAI decisions and required reranking, Explicit Telegram receiver, Isolated local full-stack runtime, Stop and recover, Verification without provider calls (+9 more)

### Community 110 - "AdmitFlow pitch deck copy"
Cohesion: 0.29
Nodes (7): AdmitFlow pitch deck copy, Slide 1: AdmitFlow, Slide 2: The admissions inquiry, Slide 3: A working student journey, Slide 4: Institution knowledge and control, Slide 5: Technology and verification, Slide 6: Pilot and next steps

### Community 111 - "test_qualification.py"
Cohesion: 0.27
Nodes (11): AsyncSession, Run the qualification loop., run_qualification(), MockResult, Any, asyncio, test_qualification_extracts_and_fails(), test_qualification_extracts_and_passes() (+3 more)

### Community 112 - "typing"
Cohesion: 0.08
Nodes (41): asyncio, Redis distributed mutex with owner-safe release and keepalive (Task 7). Ensures…, Application-layer PII protection: symmetric encryption + deterministic hashing.…, Lead, its semantic facts (lead_facts), and episodic messages (ADR-004)., Institution document extraction, durable ingestion and retrieval., Code-owned application fees and authenticated Razorpay payment processing., Strict private-chat normalization and token-safe Telegram HTTP transport., Telegram transport and tenant-scoped identity helpers. (+33 more)

### Community 113 - "uuid"
Cohesion: 0.15
Nodes (33): Base, IdMixin, Declarative base, metadata naming convention, and shared column mixins. Every…, Declarative base shared by every AdmitFlow model., UUID primary key with an application-side default. UUIDs avoid cross-tenant…, Server-side created/updated timestamps., Row-level tenant scoping (ADR-003). Mixed into every tenant-scoped table., TenantMixin (+25 more)

### Community 114 - "Quality Gates — Definition of Done"
Cohesion: 0.33
Nodes (6): CI mirrors this exactly, Fast iteration vs the gate, Quality Gates — Definition of Done, The baseline gate (every change), The enforced-numbers ledger, The tiers — add gates by what the change touches

### Community 115 - "reranking.py"
Cohesion: 0.15
Nodes (11): Bounded OpenAI-only model roles; provider details never escape in errors., PassageRanking, BaseModel, UUID, Bounded OpenAI evidence reranking with a validated baseline fallback., evaluate(), main(), Live synthetic OpenAI ranking check; no database writes or message delivery. (+3 more)

### Community 116 - "devDependencies"
Cohesion: 0.33
Nodes (6): devDependencies, @playwright/test, @types/node, @types/react, @types/react-dom, typescript

### Community 117 - "applications.tsx"
Cohesion: 0.25
Nodes (5): Applications(), Detail, fields, statuses, Summary

### Community 118 - "dependencies"
Cohesion: 0.40
Nodes (5): dependencies, @fontsource-variable/dm-sans, next, react, react-dom

### Community 119 - "scheduler.py"
Cohesion: 0.19
Nodes (11): dispatch_due(), Local operational commands with secrets entered through protected prompts., main(), Produce due reminder jobs and recover queued deliveries; safe to run after…, run(), purge_retained(), datetime, Expire inactive dialogue; applications, payments and CRM records survive. (+3 more)

### Community 120 - "live"
Cohesion: 0.19
Nodes (13): Acknowledge, current(), live(), Any, AsyncSession, BaseModel, Db, get (+5 more)

### Community 121 - "README.md"
Cohesion: 0.14
Nodes (11): AI Impact Statement, Student-to-staff demonstration, Current templates, Language review packet, Live exercise, Reminder consent and outreach copy, Prior-work disclosure draft, AdmitFlow submission requirements (+3 more)

### Community 122 - "InputGuardrailResult"
Cohesion: 0.18
Nodes (11): _deterministic_check(), InputGuardrailResult, LLMGuardrailResponse, LLMOutputGuardrailResponse, OutputGuardrailResult, BaseModel, Result of the input guardrail check., Result of the output guardrail check. (+3 more)

### Community 123 - "reindex_names.py"
Cohesion: 0.36
Nodes (7): main(), AsyncSession, UUID, Backfill encrypted lead names from latest submitted forms and rebuild blind…, reindex_batch(), test_index_rename_clear_and_legacy_backfill(), exercise()

### Community 124 - "WhatsApp readiness check — October 22, 2026"
Cohesion: 0.20
Nodes (10): Decision so far, Delivery diagnosis and configuration repair (October 23, approximately 00:16 IST), Evidence collected before configuration, Final Postman retry (October 23), Live checkpoint (approximately 22:54 IST), New test account configuration (October 23, approximately 09:45 IST), Prior-work disclosure draft, Setup and bounded repair checkpoint (approximately 22:52 IST) (+2 more)

### Community 125 - "write_audit_log"
Cohesion: 0.12
Nodes (24): CRM search and institution downloads, Any, AsyncSession, UUID, Record persisted ORM transitions atomically; never infer an earlier stage., Append one entry to ``audit_logs`` on ``session``; return it flushed, not…, record_stage_changes(), write_audit_log() (+16 more)

### Community 126 - "erase_inquiry"
Cohesion: 0.27
Nodes (10): erase(), erase_inquiry(), EraseRequest, in_flight(), AsyncSession, BaseModel, Db, delete (+2 more)

### Community 127 - "Phase 3: AI Core (Engine + RAG)"
Cohesion: 0.18
Nodes (11): Phase 3: AI Core (Engine + RAG), Task 10: Input guardrail node, Task 11: Triage node (intent detection), Task 12: Discovery node, Task 13: RAG pipeline, Task 14: RAG node, Task 15: Qualification node, Task 16: Output guardrail (+3 more)

### Community 128 - "payments.tsx"
Cohesion: 0.32
Nodes (6): label(), money(), outcomes, Payment, Payments(), statuses

### Community 129 - "test_expired_lease_recovery_cap_and_configuration_cancellation"
Cohesion: 0.22
Nodes (7): configure(), test_configuration_roles_encryption_and_tenant_ownership(), inspect(), test_expired_lease_recovery_cap_and_configuration_cancellation(), inspect(), test_source_transaction_rolls_back_event_and_outbox(), exercise()

### Community 130 - "react"
Cohesion: 0.40
Nodes (5): StaffAccounts(), create(), mutate(), User, react

### Community 131 - "Knowledge"
Cohesion: 0.46
Nodes (8): refresh(), api(), Knowledge(), action(), login(), search(), upload(), send()

### Community 132 - "test_local_runtime.py"
Cohesion: 0.11
Nodes (17): argparse, compose(), Verify the isolated local Compose stack without external API calls or sends., seed_credentials(), verify(), configure(), main(), Path (+9 more)

### Community 133 - "env.py"
Cohesion: 0.22
Nodes (9): do_run_migrations(), Connection, Alembic migration environment (async). Reads the database URL from application…, Emit SQL to stdout without a live DB connection., Run migrations against a live database via an async engine., run_migrations_offline(), run_migrations_online(), logging_config (+1 more)

### Community 135 - "test_failure_retry_and_delete_during_indexing"
Cohesion: 0.16
Nodes (12): Any, MonkeyPatch, TestClient, send(), test_duplicate_claim_and_abandoned_attempt_recovery(), claims(), paused(), recover() (+4 more)

### Community 136 - "send_outbound"
Cohesion: 0.21
Nodes (10): process_payment(), TaskIQ broker singleton. In production (and local dev with Redis running) the…, task, Encrypted outbound-message delivery jobs carry only internal identifiers., send_outbound_message(), create_payment_link(), task, Payment-link creation runs after the requesting conversation transaction… (+2 more)

### Community 137 - "page.tsx"
Cohesion: 0.12
Nodes (11): DeliveryBudget(), Usage, Exports(), Configuration, Integrations(), Request, Doc, errors (+3 more)

### Community 138 - "index_known_name"
Cohesion: 0.40
Nodes (5): index_known_name(), Connection, Mapper, Keep index updates atomic with encrypted names, including name removal., listens_for

### Community 139 - "process_inbound_message"
Cohesion: 0.20
Nodes (10): process_inbound_message(), Any, Process an inbound WhatsApp message (Task 17). This is a placeholder for the…, asyncio, MonkeyPatch, test_legacy_webhook_is_absent_and_nondev_debug_is_disabled(), test_preexisting_legacy_job_cannot_dispatch_by_default(), Missing-reply investigation (approximately 22:59 IST) (+2 more)

### Community 140 - "13. Dashboard Features"
Cohesion: 0.22
Nodes (9): 13.1 Authentication, 13.2 Roles & Permissions, 13.3 UI Aesthetic, 13.4 Real-Time Notifications, 13.5 Funnel Analytics, 13.6 Data Export & Integration, 13.7 Document Management (RAG), 13.8 Onboarding (MVP) (+1 more)

### Community 141 - "test_worker_broker.py"
Cohesion: 0.18
Nodes (10): ping(), task, Smoke-test task: returns ``{"result": payload}``. Enqueued from the…, Tests for the TaskIQ broker setup and task execution (Task 3). All tests run…, When REDIS_URL is unset the factory should yield an InMemoryBroker., The ping task should run and return the expected payload., Ping without an explicit payload should default to 'pong'., test_broker_is_in_memory_without_redis_url() (+2 more)

### Community 142 - "AuditLog"
Cohesion: 0.25
Nodes (8): AuditLog, One recorded significant action (state change, payment, deletion, takeover).…, capture_event(), Connection, Mapper, Unit test for the audit-log write helper. The real INSERT path (JSONB, server-…, test_write_audit_log_defaults_optional_fields(), test_write_audit_log_stages_and_flushes_entry()

### Community 144 - "Phase 3–4 addition (see ADR-008)"
Cohesion: 0.33
Nodes (6): Phase 3–4 addition (see ADR-008), Task 40: `decide()` System-1 decision-layer abstraction, Task 41: Distill decisions into self-hosted Laya (post-demo), Task 42.1: Complex Document Parsing & Semantic Chunking, Task 42.2: Contextual Query Rewriting, Task 42: Advanced RAG Strategy (ADR-011)

### Community 145 - "decrypt_bytes"
Cohesion: 0.29
Nodes (8): decrypt_bytes(), encrypt_bytes(), _fernet(), Encrypt uploaded source bytes before persistence, without lossy text decoding., Authenticate and decrypt source bytes for an authorized ingestion task., readable_pdf(), test_upload_formats_search_duplicates_and_tenant_isolation(), index()

### Community 146 - "unittest_mock"
Cohesion: 0.29
Nodes (6): RuntimeError, WhatsApp message sending service (Task 6). Uses httpx2 to call the Meta Graph…, Raised when the Meta Cloud API returns an error response., WhatsAppAPIError, Tests for the WhatsApp Message Sending Service (Task 6). The sender calls the…, unittest_mock

### Community 147 - "notifications.tsx"
Cohesion: 0.33
Nodes (4): labels, Notice, Notifications(), Snapshot

### Community 148 - "AdmitFlow — Task List"
Cohesion: 0.25
Nodes (8): AdmitFlow — Task List, AIBoomi Startup Weekend session handoff (2026-10-22), Current direction and hackathon resources (2026-10-23), Phase 1: Foundation, Task 1: Initialize Python project, FastAPI, settings, and Docker, Task 2: PostgreSQL schema (SQLAlchemy + Alembic), Task 3: TaskIQ + Redis broker setup, Task 4: PII encryption utilities and audit log infrastructure

### Community 149 - "Implementation Plan: AdmitFlow"
Cohesion: 0.40
Nodes (4): Architecture Decisions, Implementation Plan: AdmitFlow, Overview, Risks and Mitigations

### Community 150 - "staff/__init__.py"
Cohesion: 0.29
Nodes (5): Staff authentication and institution-scoped access., isolated_local_login_windows(), fixture, MonkeyPatch, Keep development-only throttle state independent across database test cases.

### Community 151 - "inbound"
Cohesion: 0.38
Nodes (6): test_budget_pause_does_not_spend_a_reminder_and_stop_cancels_it(), exercise(), test_explicit_consent_and_stop_during_staff_takeover(), exercise(), inbound(), UUID

### Community 152 - "11. Human-in-the-Loop (Full Workflow)"
Cohesion: 0.40
Nodes (5): 11.1 Auto-Escalation Triggers, 11.2 Co-pilot Mode, 11.3 Business Hours, 11.4 Never Escalate, 11. Human-in-the-Loop (Full Workflow)

### Community 153 - "record-demo.mjs"
Cohesion: 0.40
Nodes (4): credentials, headers, journey, target

### Community 154 - "event_for"
Cohesion: 0.29
Nodes (6): event_for(), test_delivery_claim_retry_and_minimal_payload(), exercise(), exercise(), test_more_than_one_page_of_unread_events_remains_accessible(), seed()

### Community 155 - "generate_completion"
Cohesion: 0.17
Nodes (16): generate_completion(), Any, Generate a completion with automatic provider fallback. Tries the fast model,…, mock_settings(), asyncio, fixture, MonkeyPatch, Ensure all three models are configured for fallback testing. (+8 more)

### Community 156 - "10. Observability & Tracing"
Cohesion: 0.50
Nodes (4): 10.1 LLM Tracing (Langfuse), 10.2 Structured Logging, 10.3 Error Monitoring (Sentry), 10. Observability & Tracing

### Community 157 - "2. Boundaries & Invariants"
Cohesion: 0.50
Nodes (4): 2. Boundaries & Invariants, Always Do, Ask First, Never Do

### Community 158 - "3. Tech Stack & Commands"
Cohesion: 0.50
Nodes (4): 3. Tech Stack & Commands, Deployment, Hybrid Architecture, Key Commands

### Community 159 - "5. Code Style"
Cohesion: 0.50
Nodes (4): 5. Code Style, Python (Backend), Separation of Concerns, TypeScript (Frontend)

### Community 160 - "8. RAG (Retrieval-Augmented Generation)"
Cohesion: 0.50
Nodes (4): 8.1 Per-Institution Knowledge Base, 8.2 Retrieval Pipeline, 8.3 RAG Guardrail, 8. RAG (Retrieval-Augmented Generation)

### Community 161 - "Phase 4: Advanced Bot Features"
Cohesion: 0.29
Nodes (7): Phase 4: Advanced Bot Features, Task 18: Application form collection node, Task 19: Razorpay integration, Task 20: Human handoff + co-pilot mode, Task 21: Cold lead re-engagement worker, Task 22: WhatsApp rate-limit tracking, Task 23: Langfuse tracing integration

### Community 162 - "test_ingest_document"
Cohesion: 0.33
Nodes (5): asyncio, patch, test_ingest_document(), test_sanitize_chunks(), Fresh baseline quality gate

### Community 163 - "Phase 6: Production Hardening"
Cohesion: 0.33
Nodes (6): Phase 6: Production Hardening, Task 35: Sentry error monitoring, Task 36: Delete My Data endpoint, Task 37: Data retention auto-cleanup, Task 38: Docker Compose for local development, Task 39: Production deployment

### Community 164 - "log_delivery_status"
Cohesion: 0.40
Nodes (5): log_delivery_status(), Request, Response, Observe only authenticated status events, without recipient or error text., middleware

### Community 165 - "17. Decisions & Open Questions"
Cohesion: 0.67
Nodes (3): 17.1 Conversation engine — DECIDED: hand-rolled dispatcher, 17.2 Still open, 17. Decisions & Open Questions

### Community 166 - "ConversationEvent"
Cohesion: 0.50
Nodes (4): ConversationEvent, event_text(), AsyncSession, Human-readable callback summaries without exposing routing or signature details.

### Community 167 - "test_schema_metadata.py"
Cohesion: 0.17
Nodes (7): A private-chat identity whose bot and lead must belong to its tenant., TelegramIdentity, Schema invariants — pure metadata assertions, no database required. These…, ADR-003: every tenant-scoped table carries tenant_id -> institutions.id., test_every_tenant_scoped_table_has_tenant_id_fk_to_institutions(), test_lead_status_covers_all_spec_lifecycle_states(), test_rule_operator_covers_spec_operator_set()

### Community 168 - "Cursor"
Cohesion: 0.40
Nodes (4): Cursor, BaseModel, datetime, field_validator

### Community 169 - "WhatsApp readiness check (2026-10-22, in progress)"
Cohesion: 0.40
Nodes (5): Final Postman diagnostic (October 23, executed; delivery blocked), Readiness blocker: idle Redis worker restart (in progress), Readiness tunnel setup (in progress), Test-number delivery diagnosis (October 23, blocked on Meta account restriction), WhatsApp readiness check (2026-10-22, in progress)

### Community 170 - "TriageResponse"
Cohesion: 0.67
Nodes (3): BaseModel, Structured output expected from the LLM triage classifier., TriageResponse

## Knowledge Gaps
- **414 isolated node(s):** `admitflow-backend`, `fs`, `path`, `crypto`, `root` (+409 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1121 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CRM search and institution downloads` connect `write_audit_log` to `seed`, `leads.py`, `backend/README.md`?**
  _High betweenness centrality (0.087) - this node is a cross-community bridge._
- **Why does `AdmitFlow — Task List` connect `AdmitFlow — Task List` to `Phase 5: Dashboard Frontend (Next.js)`, `Phase 4: Advanced Bot Features`, `Phase 6: Production Hardening`, `WhatsApp readiness check (2026-10-22, in progress)`, `WhatsAppSender`, `Phase 3–4 addition (see ADR-008)`, `2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md`, `Phase 3: AI Core (Engine + RAG)`?**
  _High betweenness centrality (0.077) - this node is a cross-community bridge._
- **Why does `write_audit_log()` connect `write_audit_log` to `leads.py`, `journey.py`, `send_outbound`, `settings.py`, `transport.py`, `AuditLog`, `AdmitFlow — Task List`, `payments/service.py`, `exports.py`, `Course`, `event_for`, `telegram/service.py`, `management.py`, `outreach/followups.py`, `analytics`, `StaffUser`, `operations.py`, `seed`, `generate`, `change_password`, `TelegramBot`, `reconcile`, `api.py`, `RazorpayClient`, `test_telegram_contracts.py`, `sqlalchemy`, `models/__init__.py`, `crm.py`, `knowledge/processing.py`, `payments/webhook.py`, `typing`, `scheduler.py`, `live`, `erase_inquiry`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `encrypt_pii()` (e.g. with `Consequences` and `Decision`) actually correct?**
  _`encrypt_pii()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 54 inferred relationships involving `LeadStatus` (e.g. with `record_stage_changes()` and `Lead`) actually correct?**
  _`LeadStatus` has 54 INFERRED edges - model-reasoned connections that need verification._
- **What connects `admitflow-backend`, `fs`, `path` to the rest of the system?**
  _414 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `pydantic` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._