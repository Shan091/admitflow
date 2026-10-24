# Graph Report - admitflow  (2026-10-24)

## Corpus Check
- 321 files · ~176,115 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 7, .example 2, .css 2)

## Summary
- 2822 nodes · 8083 edges · 169 communities (154 shown, 15 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 509 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `56074f12`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ADR-008: System-1 Decision Layer (Laya / Jev)
- Conversation Engine (hand-rolled dispatcher)
- AdmitFlow Complete Specification
- Finalized Production Stack
- leads.py
- analytics
- Code Owns the Money
- journey.py
- RedisMutex
- write_audit_log
- pdf_parser.py
- transport.py
- WhatsAppSender
- core/rag.py
- PII Encryption & Audit Log
- Razorpay Payment Integration
- get_settings
- admissions.tsx
- contextual_query
- guidance.py
- AIBoomi Startup Weekend Kochi: fresh-session context
- LeadStatus
- require_admin
- ._post
- RuleOperator
- Stages
- test_knowledge_workspace.py
- fixture
- run_postman_check.cjs
- Task List
- payments/webhook.py
- test_crm_search.py
- Phase 5: Dashboard Frontend (Next.js)
- management.py
- Code Standards
- outreach/followups.py
- Event preparation and execution plan
- 7. Core Feature Specifications
- BaseModel
- main.py
- Event
- operations.py
- Hackathon resources for AdmitFlow
- manifest.json
- knowledge/processing.py
- AdmitFlow: current state and planning baseline
- AdmitFlow: AIBoomi submission plan
- AdmitFlow — Complete Specification
- handle_turn
- integration/test_followups.py
- ADR-011: Required OpenAI passage reranking
- Testing
- test_guardrails.py
- AdmitFlow project handoff
- unittest_mock
- EncryptionKeyNotConfiguredError
- GuidanceMemory
- test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment
- copilot.py
- ADR-010: Triage Fallback Routing (Anti-Spam)
- ADR-012: Telegram and OpenAI for the first complete admissions MVP
- decrypt_pii
- compilerOptions
- auth.py
- encrypt_pii
- pdf_worker.py
- api.py
- test_structured_documents.py
- AllProvidersFailedError
- RazorpayClient
- Official source snapshots
- Batch
- get_redis
- validate_services.py
- budget.py
- management.tsx
- prepare_document_models.py
- test_whatsapp_sender.py
- test_privacy.py
- verify.sh
- db/__init__.py
- src/__init__.py
- tasks/__init__.py
- analytics.tsx
- whatsapp/__init__.py
- integration/__init__.py
- admitflow-backend
- Implementation Plan: AdmitFlow
- AdmitFlow
- ExtractionError
- PaymentLink
- json
- ADR-009: Application-Layer PII Encryption and Audit Logging
- 3. Tech Stack & Commands
- Git & GitHub Workflow
- package.json
- 13. Dashboard Features
- @playwright/test
- AGENTS.md
- Security & Production Readiness
- process_upload
- next-env.d.ts
- sqlalchemy
- reindex_batch
- layout.tsx
- frontend/AGENTS.md
- scripts
- backend/README.md
- AdmitFlow pitch deck
- test_payment_contracts.py
- test_telegram_journey.py
- models/__init__.py
- AGENTS.md
- telegram/service.py
- devDependencies
- applications.tsx
- dependencies
- ExtractionResponse
- Settings
- TriageResponse
- telegram/outbound.py
- question_courses
- WhatsApp readiness check — October 22, 2026
- evaluate_faq.py
- live
- 17. Decisions & Open Questions
- payments.tsx
- Adaptive course guidance: evidence and implementation
- Knowledge
- test_local_runtime.py
- env.py
- test_shared_budget_preserves_queues_and_settings_wake_deliveries
- page.tsx
- AdmitFlow execution and demonstration checklist
- add_institution_knowledge_workspace_b627da2f7e11.py
- review
- scheduler.py
- verify_compose.py
- test_readiness_webhook.py
- get_engine
- workspace
- notifications.tsx
- AdmitFlow — Task List
- settings.py
- 11. Human-in-the-Loop (Full Workflow)
- staff/payments.py
- record-demo.mjs
- Local Telegram/OpenAI runtime
- generate_completion
- 2. Boundaries & Invariants
- 8. RAG (Retrieval-Augmented Generation)
- Phase 3–4 addition (see ADR-008)
- Phase 4: Advanced Bot Features
- Language review packet
- exports.py
- Phase 6: Production Hardening
- timeline.py
- add_conversation_runtime_714f092da3b8.py
- UploadBodyLimit
- enqueue_outbound
- AdmitFlow submission requirements
- index_known_name
- 10. Observability & Tracing
- 5. Code Style
- tasks/processing.py
- test_payment_and_webhook_claims_wait_for_erasure_lock
- DOCUMENT_REVIEW.md

## God Nodes (most connected - your core abstractions)
1. `encrypt_pii()` - 106 edges
2. `write_audit_log()` - 98 edges
3. `LeadStatus` - 96 edges
4. `get_settings()` - 93 edges
5. `Reply` - 88 edges
6. `Lead` - 86 edges
7. `decrypt_pii()` - 78 edges
8. `TelegramBot` - 74 edges
9. `Course` - 64 edges
10. `signin()` - 62 edges

## Surprising Connections (you probably didn't know these)
- `Task 42.3: Pluggable Reranker (Cohere API vs Local)` --references--> `search_chunks()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/core/rag.py
- `Task 4: PII encryption utilities and audit log infrastructure` --references--> `write_audit_log()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/db/audit.py
- `17.1 Conversation engine — DECIDED: hand-rolled dispatcher` --references--> `handle_turn()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/SPEC.md → backend/src/engine/dispatcher.py
- `Missing-reply investigation (approximately 22:59 IST)` --references--> `process_inbound_message()`  [INFERRED]
  docs/event/READINESS_CHECK.md → backend/src/tasks/processing.py
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

## Communities (169 total, 15 thin omitted)

### Community 0 - "ADR-008: System-1 Decision Layer (Laya / Jev)"
Cohesion: 0.18
Nodes (17): ADR-001: Hybrid Architecture, ADR-004: Dual Memory Architecture, Episodic Memory (messages table), Semantic Memory (lead_facts table), ADR-005: Three-Layer Guardrails and RAG, Three-Layer Guardrails, ADR-007: Finalized Production Stack, ADR-008: System-1 Decision Layer (Laya / Jev) (+9 more)

### Community 1 - "Conversation Engine (hand-rolled dispatcher)"
Cohesion: 0.25
Nodes (8): Conversation Engine (hand-rolled dispatcher), System-1 decide() Decision Layer, FastAPI WhatsApp Webhook, Langfuse LLM Tracing, pgvector RAG Pipeline, Redis (mutex / dedup / rate-limit), TaskIQ Background Worker, Three-Layer Guardrails

### Community 2 - "AdmitFlow Complete Specification"
Cohesion: 0.17
Nodes (12): AI Impact Statement, Data, model and asset provenance, Student-to-staff demonstration, Executed final check, One final WhatsApp check with Postman, Prior-work disclosure, AdmitFlow necessary resources, Planning baseline before Telegram alignment (+4 more)

### Community 3 - "Finalized Production Stack"
Cohesion: 0.18
Nodes (11): ADR-002: Webhook Concurrency and Deduplication, Per-Phone Redis Mutex, Webhook Deduplication (Redis SETNX), ADR-003: Multi-Tenancy Strategy, Multi-Tenancy (Row-Level Isolation), Finalized Production Stack, Fly.io (Backend + Worker + Scheduler), Langfuse Cloud (LLM Tracing) (+3 more)

### Community 4 - "leads.py"
Cohesion: 0.19
Nodes (21): lead_statement(), lead_summary(), LeadFilters, LeadSearch, Any, BaseModel, Select, UUID (+13 more)

### Community 5 - "analytics"
Cohesion: 0.06
Nodes (38): alias, Admissions analytics, AdmitFlow Backend, Application payments, Configuration, Consented follow-up reminders, Current implementation and verification, Institution knowledge workspace (+30 more)

### Community 6 - "Code Owns the Money"
Cohesion: 0.50
Nodes (5): ADR-006: Code-Owned Qualification and Payments, Intent: Admissions Flow and Discounts, Discount Codes, Code Owns Eligibility, Code Owns the Money

### Community 7 - "journey.py"
Cohesion: 0.10
Nodes (55): Lead, A prospective applicant with optional phone contact and channel identities.…, action(), application_action(), collect_application(), prompt(), Any, AsyncSession (+47 more)

### Community 8 - "RedisMutex"
Cohesion: 0.07
Nodes (28): MutexAcquireError, Redis, RuntimeError, Redis distributed mutex with owner-safe release and keepalive (Task 7). Ensures…, Background loop that extends the TTL while the lock is held., Raised when the mutex cannot be acquired after all retries., Async context-manager mutex backed by Redis ``SET NX``. Parameters: redis: An…, Attempt to acquire the lock, retrying up to ``retry_count`` times. (+20 more)

### Community 9 - "write_audit_log"
Cohesion: 0.18
Nodes (13): Any, AsyncSession, UUID, Record persisted ORM transitions atomically; never infer an earlier stage., Append one entry to ``audit_logs`` on ``session``; return it flushed, not…, record_stage_changes(), write_audit_log(), test_write_audit_log_persists_and_reads_back() (+5 more)

### Community 10 - "pdf_parser.py"
Cohesion: 0.14
Nodes (15): kill_descendants(), parse_pdf(), Offline PDF child process with per-loop backpressure, memory and time limits., Include Windows venv redirector children and any parser subprocesses., resident_memory(), watch_memory(), Process, parametrize (+7 more)

### Community 11 - "transport.py"
Cohesion: 0.09
Nodes (33): destination(), post_event(), PrivateTransportLogs, protect_logs(), public_ip(), LogRecord, HTTPS delivery pins a public resolved address while retaining TLS host…, resolve_public() (+25 more)

### Community 12 - "WhatsAppSender"
Cohesion: 0.16
Nodes (11): Service for sending messages via Meta WhatsApp Cloud API., WhatsAppSender, asyncio, Successfully sending a template message., API errors (non-200) raise WhatsAppAPIError., Fails loud if access token or phone ID are missing., WhatsApp sender operations., Successfully sending a text message. (+3 more)

### Community 13 - "core/rag.py"
Cohesion: 0.09
Nodes (29): chunk_text(), embed_text(), ingest_document(), Any, AsyncSession, UUID, RAG pipeline core logic (Task 13). Handles ingestion (chunking, embedding),…, Sanitizer to prevent RAG poisoning. Blocks chunks that contain obvious prompt… (+21 more)

### Community 16 - "get_settings"
Cohesion: 0.12
Nodes (20): AsyncBroker, get_settings(), Return the process-wide :class:`Settings` singleton., _build_broker(), TaskIQ broker singleton. In production (and local dev with Redis running) the…, Construct the right broker based on the current settings. This is a plain…, get, Response (+12 more)

### Community 17 - "admissions.tsx"
Cohesion: 0.10
Nodes (19): Admissions(), Detail, Human, Inquiry, labels, Request, RuleEvidence, statusLabel() (+11 more)

### Community 18 - "contextual_query"
Cohesion: 0.13
Nodes (17): contextual_query(), Resolve pronouns/slang using bounded recent turns; uncertainty asks the…, retrieval_query(), evaluate(), main(), Bounded synthetic OpenAI reference resolution; no database writes or sends., MonkeyPatch, parametrize (+9 more)

### Community 19 - "guidance.py"
Cohesion: 0.13
Nodes (38): QualificationRule, A structured eligibility rule evaluated in code, not by the LLM (ADR-006).…, academic_number_supported(), catalog(), catalog_status(), checked_text(), commit_guidance(), guide() (+30 more)

### Community 20 - "AIBoomi Startup Weekend Kochi: fresh-session context"
Cohesion: 0.11
Nodes (19): AIBoomi Startup Weekend Kochi: fresh-session context, Assessment and next decision, Current readiness session (October 22), Event sources and local copies, Existing prototype rule and surprise element, Existing working-tree changes, Fresh-message prompt, Handoff status (+11 more)

### Community 21 - "LeadStatus"
Cohesion: 0.09
Nodes (49): Application-layer PII protection: symmetric encryption + deterministic hashing.…, ApplicationStatus, DiscountType, LeadStatus, PaymentStatus, Enumerated types used across the schema. These are Python ``str`` enums mapped…, Lead lifecycle states (SPEC §7.3). Where a lead *stands*, not a fixed track —…, How a discount code reduces the fee. (+41 more)

### Community 22 - "require_admin"
Cohesion: 0.19
Nodes (22): admin_scope(), create_user(), CreateUser, edit_user(), EditUser, Any, BaseModel, Db (+14 more)

### Community 23 - "._post"
Cohesion: 0.17
Nodes (11): Any, Send an interactive list message. `sections` is a list of section dicts…, Send a pre-approved template message., Post the payload to Meta and extract the created message ID., Meta API expects the phone number without the leading '+'., Send a simple text message. Returns the Meta message ID., Send an interactive message with up to 3 buttons. `buttons` should be a list of…, Phase 2: WhatsApp Ingress (+3 more)

### Community 24 - "RuleOperator"
Cohesion: 0.08
Nodes (41): Qualification-rule comparison operators (SPEC §7.4). Evaluated…, RuleOperator, AsyncSession, Run the qualification loop., run_qualification(), EngineState, InvalidTransitionError, BaseModel (+33 more)

### Community 25 - "Stages"
Cohesion: 0.13
Nodes (15): 10. Reflect & learn, 1. Understand & spec  (`/spec`), 2. Plan & pick a task  (`/plan`), 3. Branch, 4. Build with TDD  (`/build`, `/test`), 5. Verify (the quality gate), 6. Self-review, then adversarial review  (`/review`), 7. Commit & open the PR (+7 more)

### Community 26 - "test_knowledge_workspace.py"
Cohesion: 0.05
Nodes (39): alembic, alembic_config, asyncio, common(), Column, upgrade(), Dashboard access role (SPEC — admin vs agent)., StaffRole (+31 more)

### Community 27 - "fixture"
Cohesion: 0.05
Nodes (42): fixture(), Course, isolated_local_login_windows(), MonkeyPatch, Keep development-only throttle state independent across database test cases., migrated_db(), Start Postgres, point settings at it, migrate to head; tear down after., migrated_db() (+34 more)

### Community 28 - "run_postman_check.cjs"
Cohesion: 0.20
Nodes (8): collection, config, crypto, fs, keys, newman, path, root

### Community 29 - "Task List"
Cohesion: 0.15
Nodes (13): Checkpoint: Advanced Features, Checkpoint: AI Core, Checkpoint: Dashboard Complete, Checkpoint: Foundation, Checkpoint: Production Ready, Checkpoint: WhatsApp Ingress, Phase 1: Foundation, Phase 2: WhatsApp Ingress (+5 more)

### Community 30 - "payments/webhook.py"
Cohesion: 0.18
Nodes (13): Integer monetary arithmetic and exact-byte webhook authentication., LinkEntity, LinkEnvelope, PaidEvent, PaidPayload, PaymentEntity, PaymentEnvelope, BaseModel (+5 more)

### Community 31 - "test_crm_search.py"
Cohesion: 0.22
Nodes (14): Core cross-cutting concerns: settings, security, schemas, guardrails, tracing., name_tokens(), normalized_phone(), UUID, query_tokens(), Tenant-keyed blind name prefixes; plaintext remains in encrypted columns only., token(), words() (+6 more)

### Community 32 - "Phase 5: Dashboard Frontend (Next.js)"
Cohesion: 0.17
Nodes (12): Phase 5: Dashboard Frontend (Next.js), Task 24: Initialize Next.js + dark mode + glassmorphism, Task 25: Authentication (email + password), Task 26: Dashboard home (funnel analytics), Task 27: Leads CRM page, Task 28: Course & batch management, Task 29: Chat takeover + co-pilot UI, Task 30: Document management (RAG) (+4 more)

### Community 33 - "management.py"
Cohesion: 0.22
Nodes (29): archive_course(), archive_discount(), catalog(), catalog_detail(), course_view(), CourseInput, create_course(), create_discount() (+21 more)

### Community 34 - "Code Standards"
Cohesion: 0.18
Nodes (11): Async & I/O, Code Standards, Configuration — settings, not literals, Dependencies, Errors, Formatting, LLM calls, Logging & observability (+3 more)

### Community 35 - "outreach/followups.py"
Cohesion: 0.09
Nodes (38): escalation_reason(), office_open(), datetime, Reason, Deterministic clear support signals and institution-local office hours., load_memory(), activity(), after_send() (+30 more)

### Community 36 - "Event preparation and execution plan"
Cohesion: 0.18
Nodes (11): Business and mentor preparation, Evaluation and demo evidence, Event preparation and execution plan, Kickoff disclosure draft, Latest direction (October 23), Minimum demonstrable product, Next action: one-hour v1 readiness check, Submission checklist (+3 more)

### Community 37 - "7. Core Feature Specifications"
Cohesion: 0.18
Nodes (11): 7.10 Payment Integration & Discounts (Razorpay), 7.1 WhatsApp Number Architecture, 7.2 Multi-Tenancy (Row-Level Isolation), 7.3 Lead Lifecycle States, 7.4 Course Qualification Rules (Structured), 7.5 Batch & Intake Management, 7.6 Cold Lead Re-engagement, 7.7 Language Support (+3 more)

### Community 38 - "BaseModel"
Cohesion: 0.23
Nodes (7): BatchInput, Hours, BaseModel, RuleInput, SettingsInput, model_validator, Self

### Community 39 - "main.py"
Cohesion: 0.10
Nodes (17): recovery_loop(), create_app(), lifespan(), FastAPI, FastAPI application entry point. Boots the API, manages the TaskIQ broker…, Start / stop the TaskIQ broker alongside the FastAPI process. The…, Application factory — builds and configures the FastAPI instance., Tests for the /debug endpoints (Task 3 verification). (+9 more)

### Community 40 - "Event"
Cohesion: 0.10
Nodes (34): Event, cancel_queued(), note_inbound(), preference_reply(), Any, AsyncSession, datetime, Student-owned reminder preferences apply even while staff has paused the bot. (+26 more)

### Community 41 - "operations.py"
Cohesion: 0.24
Nodes (17): resumed_status(), get_lead(), post, update_request(), active_request(), finish_takeover(), Any, AsyncSession (+9 more)

### Community 42 - "Hackathon resources for AdmitFlow"
Cohesion: 0.20
Nodes (10): Acceptance before using a resource, Event and release boundaries, Goal, Hackathon resources for AdmitFlow, October 23 Downloads guide: hosted inference access, Participant credits and other support, Suggested allocation and activation order, Useful resources mapped to the plan (+2 more)

### Community 43 - "manifest.json"
Cohesion: 0.20
Nodes (9): SPEC.md, bytes, sha256, tasks/plan.md, bytes, sha256, tasks/todo.md, bytes (+1 more)

### Community 44 - "knowledge/processing.py"
Cohesion: 0.14
Nodes (7): Bounded synthetic PDF upload/queue/OpenAI/search check; removes its own upload., UUID, Durable upload claims, bounded embedding and atomic publication of ready…, Five bounded live embedding searches through the real authenticated staff API., Hash the tested code/configuration without reading secrets or runtime data., math, pathlib

### Community 45 - "AdmitFlow: current state and planning baseline"
Cohesion: 0.22
Nodes (9): AdmitFlow: current state and planning baseline, Confirmed user direction, Feature status and integration gaps, Features to finalize next, How to reconcile the planning documents, Proposed architecture for the next plan, Stack inventory, Verification evidence and its limits (+1 more)

### Community 46 - "AdmitFlow: AIBoomi submission plan"
Cohesion: 0.22
Nodes (9): AdmitFlow: AIBoomi submission plan, Deck and presentation, Open decisions, Proposed schedule from Friday evening, Submission outcome, The journey to demonstrate, Use the provided resources, What must be handed in (+1 more)

### Community 47 - "AdmitFlow — Complete Specification"
Cohesion: 0.22
Nodes (9): 12. Edge Cases & Error Handling, 14. Data Privacy (DPDPA-Ready), 15. Memory Architecture, 16. Success Criteria, 1. Objective, 4. Project Structure, 6. Testing Strategy, 9. Guardrails (Three-Layer) (+1 more)

### Community 48 - "handle_turn"
Cohesion: 0.06
Nodes (32): InvalidPhoneError, normalize_e164(), ValueError, E.164 phone-number normalization. Carry-over prerequisite #3: un-normalized…, Raised when a phone string cannot be normalized to E.164., Normalize *raw* into canonical E.164 (``+<digits>``). Strips whitespace,…, _flush_engine_state(), handle_turn() (+24 more)

### Community 49 - "integration/test_followups.py"
Cohesion: 0.12
Nodes (25): age(), callback(), outreach(), parametrize, Real database consent, reminder leases, freshness, delivery and the two-message…, seed(), test_budget_pause_does_not_spend_a_reminder_and_stop_cancels_it(), exercise() (+17 more)

### Community 50 - "ADR-011: Required OpenAI passage reranking"
Cohesion: 0.40
Nodes (4): ADR-011: Required OpenAI passage reranking, Decision, Separate retrieval work, Verification and tradeoffs

### Community 51 - "Testing"
Cohesion: 0.22
Nodes (9): Browser announcement regions, Coverage, LLM and decision-layer tests, Philosophy — pragmatic TDD, Running tests, Test layout, Testing, The two patterns (+1 more)

### Community 52 - "test_guardrails.py"
Cohesion: 0.14
Nodes (18): apply_whatsapp_formatting(), Convert common markdown formatting to WhatsApp formatting., asyncio, Test output guardrail with safe content., Test output guardrail blocks hallucinated fee., Test that a clean message passes through., Test that profanity is blocked deterministically without calling the LLM., Test that simple injection heuristics are blocked deterministically. (+10 more)

### Community 53 - "AdmitFlow project handoff"
Cohesion: 0.22
Nodes (9): AdmitFlow project handoff, Current conversation work: Task 61, Current direction, Development rules, Event submission, Execution checkpoint, First usable release, Historical evidence (+1 more)

### Community 54 - "unittest_mock"
Cohesion: 0.18
Nodes (16): detect_intent(), Classify the user's intent to route to the correct node. Design Decision: If a…, asyncio, Test routing for course discovery., Test routing for knowledge questions., Test routing for qualification answers., Test routing for human handoff., Test routing for empty messages without calling LLM defaults to discovery. (+8 more)

### Community 55 - "EncryptionKeyNotConfiguredError"
Cohesion: 0.17
Nodes (13): EncryptionKeyNotConfiguredError, RuntimeError, Raised when a PII helper is used but its key is unset in settings., hash_telegram_identifier(), UUID, Private Telegram identity lookup without storing raw identifiers in indexes., Hash an identifier in its tenant/bot/type domain using the lookup secret. This…, MonkeyPatch (+5 more)

### Community 56 - "GuidanceMemory"
Cohesion: 0.11
Nodes (49): CourseMatch, GuidanceDecision, GuidanceInterpretation, GuidanceMemory, InterestTheme, Note, ProfileUpdate, BaseModel (+41 more)

### Community 57 - "test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment"
Cohesion: 0.15
Nodes (13): payments(), Any, get, Any, MonkeyPatch, test_absent_link_does_not_clear_uncertainty_or_authorize_retry(), prepare(), test_known_configuration_failure_can_only_requeue_same_bounded_invoice() (+5 more)

### Community 58 - "copilot.py"
Cohesion: 0.14
Nodes (20): event_text(), AsyncSession, content(), decide(), DraftContent, DraftDecision, DraftRequest, generate() (+12 more)

### Community 59 - "ADR-010: Triage Fallback Routing (Anti-Spam)"
Cohesion: 0.33
Nodes (5): ADR-010: Triage Fallback Routing (Anti-Spam), Consequences, Context, Decision, Status

### Community 60 - "ADR-012: Telegram and OpenAI for the first complete admissions MVP"
Cohesion: 0.29
Nodes (7): ADR-012: Telegram and OpenAI for the first complete admissions MVP, Consequences, Context, Decision, Implemented runtime boundaries, References and verification, Supersession and preserved decisions

### Community 61 - "decrypt_pii"
Cohesion: 0.08
Nodes (40): decrypt_pii(), Decrypt a token produced by :func:`encrypt_pii`. Raises…, test_profile_and_facts_survive_encryption_without_selecting_a_course(), exercise(), test_local_cohort_counts_conversions_and_observed_stages(), test_tenant_is_derived_from_session_and_period_is_bounded(), test_zero_filled_weekly_buckets_and_empty_rates(), test_downloads_roles_datasets_limits_and_tenants() (+32 more)

### Community 63 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 64 - "auth.py"
Cohesion: 0.14
Nodes (26): change_password(), issue_session(), Login, logout(), me(), PasswordChange, AsyncSession, BaseModel (+18 more)

### Community 65 - "encrypt_pii"
Cohesion: 0.07
Nodes (46): encrypt_pii(), Encrypt a PII string, returning a url-safe base64 Fernet token. Fernet is…, Trusted bot-to-institution mapping; token is application-encrypted., TelegramBot, seed(), test_all_aggregates_share_a_snapshot_during_concurrent_arrivals(), interleave(), test_search_pages_are_bounded_and_do_not_drop_or_repeat_records() (+38 more)

### Community 66 - "pdf_worker.py"
Cohesion: 0.29
Nodes (7): convert_pdf(), main(), Path, Single-use PDF parser. Reads stdin; emits bounded JSON, never raw diagnostics., pypdf, sys, warnings

### Community 67 - "api.py"
Cohesion: 0.14
Nodes (27): encrypt_bytes(), Encrypt uploaded source bytes before persistence, without lossy text decoding., assign_scope(), documents(), get_upload(), Any, BaseModel, Db (+19 more)

### Community 68 - "test_structured_documents.py"
Cohesion: 0.19
Nodes (14): blocks(), Markdown sections and table rows stay together within bounded evidence chunks., Keep section ancestry; repeat table headers instead of breaking row…, semantic_chunks(), table_parts(), table_start(), text_parts(), parametrize (+6 more)

### Community 69 - "AllProvidersFailedError"
Cohesion: 0.09
Nodes (33): decide(), Any, Typed decisions through the existing OpenAI-only provider boundary., Validate structured model output; refusal/malformed output is never a decision.…, AllProvidersFailedError, Exception, Raised when the entire LLM fallback chain is exhausted., check_input_safety() (+25 more)

### Community 70 - "RazorpayClient"
Cohesion: 0.16
Nodes (13): AsyncBaseTransport, PaymentProviderError, Exception, Read an existing exact reference; absence never authorizes another creation., RazorpayClient, test_ambiguous_creation_is_not_repeated(), exercise(), fail() (+5 more)

### Community 71 - "Official source snapshots"
Cohesion: 0.50
Nodes (4): Conflicts to confirm, October 23 planning refresh, Official source snapshots, Sources

### Community 72 - "Batch"
Cohesion: 0.07
Nodes (22): Batch, A dated intake of a course with finite seats (SPEC §7.5)., present_courses(), AsyncSession, Discovery Node (Task 12). Presents available courses as WhatsApp interactive…, Fetch active courses with available batches and present to user. Only shows…, Qualification Node (Task 15). Extracts rule fields using the LLM and runs…, Human-readable callback summaries without exposing routing or signature details. (+14 more)

### Community 73 - "get_redis"
Cohesion: 0.14
Nodes (15): get_redis(), Redis, RuntimeError, Raised when Redis is needed but ``REDIS_URL`` is unset in settings., Return the process-wide async Redis client singleton. The client is created…, RedisNotConfiguredError, post, Request (+7 more)

### Community 74 - "validate_services.py"
Cohesion: 0.32
Nodes (7): embed_chunks(), Use the configured OpenAI model with the database's explicit 1536 dimensions., main(), Probe, BaseModel, Bounded live checks; print sanitized results without credentials or update…, validate()

### Community 75 - "budget.py"
Cohesion: 0.15
Nodes (23): day_window(), local_counts(), Any, datetime, UUID, Atomic daily send-attempt budgets shared by every Telegram delivery path., Count confirmed deliveries once; a stats failure must not repeat a sent message., record_sent() (+15 more)

### Community 76 - "management.tsx"
Cohesion: 0.09
Nodes (16): blank, Discount, Discounts(), Batch, Course, empty, Management(), operators (+8 more)

### Community 77 - "prepare_document_models.py"
Cohesion: 0.33
Nodes (6): main(), prepare(), Path, Download only local PDF layout/table assets; no OCR, generation or document…, importlib, importlib_metadata

### Community 78 - "test_whatsapp_sender.py"
Cohesion: 0.40
Nodes (4): RuntimeError, Raised when the Meta Cloud API returns an error response., WhatsAppAPIError, Tests for the WhatsApp Message Sending Service (Task 6). The sender calls the…

### Community 79 - "test_privacy.py"
Cohesion: 0.13
Nodes (17): MessageDirection, Direction of a WhatsApp message row (episodic memory, ADR-004)., LeadFact, Message, Semantic memory: a durable key/value fact about a lead (ADR-004). Unique on…, Episodic memory: one WhatsApp turn (ADR-004). The single source of truth for…, _load_engine_state(), Engine Dispatcher (Task 8 & 17). This module contains the main entry point for… (+9 more)

### Community 84 - "analytics.tsx"
Cohesion: 0.28
Nodes (7): Analytics(), Conversion, labels, frontend_app_analytics_module, rate(), Report, shortDate()

### Community 89 - "Implementation Plan: AdmitFlow"
Cohesion: 0.40
Nodes (4): Architecture Decisions, Implementation Plan: AdmitFlow, Overview, Risks and Mitigations

### Community 90 - "AdmitFlow"
Cohesion: 0.29
Nodes (7): AdmitFlow, Current status, Demonstration and submission, Development, Product scope, Stack, Student-first course guidance

### Community 91 - "ExtractionError"
Cohesion: 0.22
Nodes (18): extract_file(), ExtractionError, ValueError, Bounded extraction of institution reference documents; never execute uploads., A safe, public error code rather than parser output containing document text., validate_path(), preflight_pdf(), basic_pdf() (+10 more)

### Community 92 - "PaymentLink"
Cohesion: 0.25
Nodes (7): PaymentLink, BaseModel, field_validator, MonkeyPatch, test_immutable_request_and_concurrent_jobs_create_one_link(), create(), exercise()

### Community 93 - "json"
Cohesion: 0.13
Nodes (27): DocumentChunk, A chunk of a document, with its embedding for vector search., PassageRanking, BaseModel, UUID, Bounded OpenAI evidence reranking with a validated baseline fallback., Reorder only original, safe tenant candidates; never invent text or sources.…, rerank() (+19 more)

### Community 94 - "ADR-009: Application-Layer PII Encryption and Audit Logging"
Cohesion: 0.22
Nodes (8): ADR-009: Application-Layer PII Encryption and Audit Logging, Alternatives Considered, Consequences, Context, Deterministic encryption of the phone number (so it is both stored and searchable), Full envelope encryption (per-tenant data keys wrapped by a master key), Rely on the provider's at-rest encryption only, Status

### Community 95 - "3. Tech Stack & Commands"
Cohesion: 0.50
Nodes (4): 3. Tech Stack & Commands, Deployment, Hybrid Architecture, Key Commands

### Community 96 - "Git & GitHub Workflow"
Cohesion: 0.12
Nodes (15): build(), Rebuild the committed, fictional digital-PDF fixture with reportlab., Branching model — feature branch → PR → `main`, Commits — Conventional Commits, small and coherent, Git & GitHub Workflow, Merging, No AI attribution — the human is the sole author  ⚠️, Pull Requests (+7 more)

### Community 97 - "package.json"
Cohesion: 0.22
Nodes (8): name, private, version, react-dom, @types/node, @types/react, @types/react-dom, typescript

### Community 98 - "13. Dashboard Features"
Cohesion: 0.22
Nodes (9): 13.1 Authentication, 13.2 Roles & Permissions, 13.3 UI Aesthetic, 13.4 Real-Time Notifications, 13.5 Funnel Analytics, 13.6 Data Export & Integration, 13.7 Document Management (RAG), 13.8 Onboarding (MVP) (+1 more)

### Community 99 - "@playwright/test"
Cohesion: 0.18
Nodes (5): ref_node_child_process, ref_node_crypto, ref_node_fs, ref_node_path, @playwright/test

### Community 100 - "AGENTS.md"
Cohesion: 0.25
Nodes (7): AIBoomi Startup Weekend handoff, How we build — read the handbook, Knowledge graph, Quick commands (from `backend/`), The rules you cannot skip, What this project is, Workflow triggers

### Community 101 - "Security & Production Readiness"
Cohesion: 0.18
Nodes (11): Dependency & secret scanning, Deploy & rollback, External surfaces, Guardrails & money, Local full-stack (docker-compose), Multi-tenancy — isolation is a correctness bug if wrong, Observability, PII & data protection (DPDPA) (+3 more)

### Community 102 - "process_upload"
Cohesion: 0.06
Nodes (35): decrypt_bytes(), _fernet(), Authenticate and decrypt source bytes for an authorized ingestion task., process_upload(), Claim once, process outside the transaction, then publish only the current…, ingest_upload(), task, TaskIQ entry point for institution document indexing. (+27 more)

### Community 103 - "next-env.d.ts"
Cohesion: 0.50
Nodes (3): NOTE: This file should not be edited, frontend_next_types_root_params_d, frontend_next_types_routes_d

### Community 104 - "sqlalchemy"
Cohesion: 0.09
Nodes (17): Audit-log write helper. :func:`write_audit_log` is the one path significant…, IntegrationEvent, WebhookDelivery, WebhookEndpoint, Leased at-least-once webhook delivery with stable recipient deduplication IDs., capture_event(), Connection, Mapper (+9 more)

### Community 105 - "reindex_batch"
Cohesion: 0.40
Nodes (6): main(), AsyncSession, UUID, reindex_batch(), test_index_rename_clear_and_legacy_backfill(), exercise()

### Community 106 - "layout.tsx"
Cohesion: 0.25
Nodes (5): frontend_app_globals, metadata, config, @fontsource-variable/dm-sans, next

### Community 108 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, lint, record:demo, start, test:e2e:live, typecheck

### Community 109 - "backend/README.md"
Cohesion: 0.13
Nodes (14): Contextual retrieval and reference scope, Isolated full-stack Compose, Outbound integrations and live notifications, Staff access and privacy operations, Typed OpenAI decisions and required reranking, Explicit Telegram receiver, Isolated local full-stack runtime, Stop and recover (+6 more)

### Community 110 - "AdmitFlow pitch deck"
Cohesion: 0.29
Nodes (7): AdmitFlow pitch deck, Slide 1: AdmitFlow, Slide 2: The admissions handoff, Slide 3: A working institution workspace, Slide 4: Answers from approved documents, Slide 5: AI with institution control, Slide 6: An institution pilot

### Community 111 - "test_payment_contracts.py"
Cohesion: 0.28
Nodes (7): discounted_amount(), verify_webhook(), MonkeyPatch, Money stays integer/code-owned; signatures use exact bytes; creation never…, test_discounts_use_minor_units_and_boundaries(), test_payment_creation_does_not_retry_ambiguous_network_failure(), test_webhook_signature_uses_raw_body_and_rejects_tampering()

### Community 112 - "test_telegram_journey.py"
Cohesion: 0.10
Nodes (27): private_send(), normalize_update(), protect_logs(), Any, LogRecord, RuntimeError, Strict private-chat normalization and token-safe Telegram HTTP transport., TaskIQ changes log levels; redact before either HTTP client or root handlers… (+19 more)

### Community 113 - "models/__init__.py"
Cohesion: 0.10
Nodes (52): Base, IdMixin, Declarative base, metadata naming convention, and shared column mixins. Every…, Declarative base shared by every AdmitFlow model., UUID primary key with an application-side default. UUIDs avoid cross-tenant…, Server-side created/updated timestamps., Row-level tenant scoping (ADR-003). Mixed into every tenant-scoped table., TenantMixin (+44 more)

### Community 114 - "AGENTS.md"
Cohesion: 0.27
Nodes (6): CI mirrors this exactly, Fast iteration vs the gate, Quality Gates — Definition of Done, The baseline gate (every change), The enforced-numbers ledger, The tiers — add gates by what the change touches

### Community 115 - "telegram/service.py"
Cohesion: 0.12
Nodes (32): async_sessionmaker, ConversationEvent, ConversationReply, get_sessionmaker(), Return the process-wide async session factory., deliver(), UUID, recover_payments() (+24 more)

### Community 116 - "devDependencies"
Cohesion: 0.33
Nodes (6): devDependencies, @playwright/test, @types/node, @types/react, @types/react-dom, typescript

### Community 117 - "applications.tsx"
Cohesion: 0.25
Nodes (5): Applications(), Detail, fields, statuses, Summary

### Community 118 - "dependencies"
Cohesion: 0.40
Nodes (5): dependencies, @fontsource-variable/dm-sans, next, react, react-dom

### Community 119 - "ExtractionResponse"
Cohesion: 0.67
Nodes (3): ExtractionResponse, BaseModel, Structured output expected from the LLM when extracting fields.

### Community 120 - "Settings"
Cohesion: 0.10
Nodes (30): hash_phone(), Return a deterministic keyed hash of a phone number for lookup/dedup. Keyed…, Environment-backed application configuration., Settings, configured_keys(), MonkeyPatch, Unit tests for application-layer PII protection (encrypt/decrypt + phone hash)., Point ``security.get_settings`` at settings with the crypto keys set. (+22 more)

### Community 121 - "TriageResponse"
Cohesion: 0.67
Nodes (3): BaseModel, Structured output expected from the LLM triage classifier., TriageResponse

### Community 122 - "telegram/outbound.py"
Cohesion: 0.24
Nodes (9): task, Encrypted outbound-message delivery jobs carry only internal identifiers., send_outbound_message(), create_payment_link(), task, Payment-link creation runs after the requesting conversation transaction…, UUID, Durable deliveries for explicit staff replies, payment events and consented… (+1 more)

### Community 123 - "question_courses"
Cohesion: 0.20
Nodes (10): AmbiguousCourseReference, AsyncSession, Course, UUID, ValueError, question_courses(), More than one active course has the requested name without a selected owner., Explicit catalog names take precedence over selection; no model invents IDs. (+2 more)

### Community 124 - "WhatsApp readiness check — October 22, 2026"
Cohesion: 0.15
Nodes (13): Decision so far, Delivery diagnosis and configuration repair (October 23, approximately 00:16 IST), Evidence collected before configuration, Final Postman retry (October 23), Live checkpoint (approximately 22:54 IST), Missing-reply investigation (approximately 22:59 IST), New test account configuration (October 23, approximately 09:45 IST), Next live checks and evidence required (+5 more)

### Community 125 - "evaluate_faq.py"
Cohesion: 0.20
Nodes (15): GroundingSource, BaseModel, Channel-neutral input and validated plain-text reply boundary., Internal evidence persisted in encrypted replies, excluded from channel…, Case, cases(), evaluate(), main() (+7 more)

### Community 126 - "live"
Cohesion: 0.19
Nodes (13): Acknowledge, current(), live(), Any, AsyncSession, BaseModel, Db, get (+5 more)

### Community 127 - "17. Decisions & Open Questions"
Cohesion: 0.67
Nodes (3): 17.1 Conversation engine — DECIDED: hand-rolled dispatcher, 17.2 Still open, 17. Decisions & Open Questions

### Community 128 - "payments.tsx"
Cohesion: 0.32
Nodes (6): label(), money(), outcomes, Payment, Payments(), statuses

### Community 130 - "Adaptive course guidance: evidence and implementation"
Cohesion: 0.18
Nodes (9): ADR-013: Adaptive, student-first course guidance, Consequences, Context, Decision, Adaptive course guidance: evidence and implementation, Asking useful questions, Boundaries and verification, Primary-source research and limits (+1 more)

### Community 131 - "Knowledge"
Cohesion: 0.44
Nodes (9): refresh(), api(), Knowledge(), action(), assignScope(), login(), search(), upload() (+1 more)

### Community 132 - "test_local_runtime.py"
Cohesion: 0.16
Nodes (13): configure(), main(), Path, Create private isolated local Compose configuration without copying live…, Tests use explicit configuration and never implicitly load developer…, asyncio, MonkeyPatch, Path (+5 more)

### Community 133 - "env.py"
Cohesion: 0.22
Nodes (9): do_run_migrations(), Connection, Alembic migration environment (async). Reads the database URL from application…, Emit SQL to stdout without a live DB connection., Run migrations against a live database via an async engine., run_migrations_offline(), run_migrations_online(), logging_config (+1 more)

### Community 137 - "page.tsx"
Cohesion: 0.12
Nodes (13): DeliveryBudget(), Usage, Exports(), Configuration, Integrations(), Request, Doc, errors (+5 more)

### Community 138 - "AdmitFlow execution and demonstration checklist"
Cohesion: 0.67
Nodes (3): AdmitFlow execution and demonstration checklist, Build and verify, Demonstrate and submit

### Community 139 - "add_institution_knowledge_workspace_b627da2f7e11.py"
Cohesion: 0.40
Nodes (4): Column, DateTime, _timestamps(), upgrade()

### Community 140 - "review"
Cohesion: 0.33
Nodes (10): CRM search and institution downloads, applications(), detail(), owned(), Any, Db, get, post (+2 more)

### Community 141 - "scheduler.py"
Cohesion: 0.10
Nodes (23): dispatch_pending(), recovery_loop(), dispatch_due(), Local operational commands with secrets entered through protected prompts., main(), Produce due reminder jobs and recover queued deliveries; safe to run after…, run(), erase() (+15 more)

### Community 142 - "verify_compose.py"
Cohesion: 0.36
Nodes (7): argparse, compose(), Verify the isolated local Compose stack without external API calls or sends., seed_credentials(), verify(), subprocess, websockets_asyncio_client

### Community 143 - "test_readiness_webhook.py"
Cohesion: 0.33
Nodes (6): parametrize, The temporary tunnel must not expose local debug or documentation routes., test_delivery_status_logs_are_authenticated_and_exclude_pii(), test_tunnel_app_exposes_no_other_routes(), test_tunnel_app_keeps_webhook_verification(), LogCaptureFixture

### Community 144 - "get_engine"
Cohesion: 0.16
Nodes (16): AsyncEngine, DatabaseNotConfiguredError, get_engine(), RuntimeError, Raised when a DB session is requested but ``DATABASE_URL`` is unset., Return the process-wide async engine (one pool for the app)., Credentials, Bounded Razorpay requests; ambiguous link creation is never blindly retried. (+8 more)

### Community 146 - "workspace"
Cohesion: 0.10
Nodes (15): task, Integration queue messages contain identifiers only., send_webhook(), configure(), event_for(), test_delivery_claim_retry_and_minimal_payload(), exercise(), test_expired_lease_recovery_cap_and_configuration_cancellation() (+7 more)

### Community 147 - "notifications.tsx"
Cohesion: 0.33
Nodes (4): labels, Notice, Notifications(), Snapshot

### Community 148 - "AdmitFlow — Task List"
Cohesion: 0.15
Nodes (13): AdmitFlow — Task List, AIBoomi Startup Weekend session handoff (2026-10-22), Current direction and hackathon resources (2026-10-23), Final Postman diagnostic (October 23, executed; delivery blocked), Phase 1: Foundation, Readiness blocker: idle Redis worker restart (in progress), Readiness tunnel setup (in progress), Task 1: Initialize Python project, FastAPI, settings, and Docker (+5 more)

### Community 150 - "settings.py"
Cohesion: 0.10
Nodes (21): log_delivery_status(), Request, Response, Expose only the existing Meta webhook through the temporary demo tunnel., Observe only authenticated status events, without recipient or error text., Shared async Redis client for application code. Carry-over prerequisite #1: the…, Application settings singleton. Loads configuration from the environment (and…, Reject oversized multipart streams before they can fill temporary storage. (+13 more)

### Community 151 - "11. Human-in-the-Loop (Full Workflow)"
Cohesion: 0.40
Nodes (5): 11.1 Auto-Escalation Triggers, 11.2 Co-pilot Mode, 11.3 Business Hours, 11.4 Never Escalate, 11. Human-in-the-Loop (Full Workflow)

### Community 152 - "staff/payments.py"
Cohesion: 0.53
Nodes (9): locked(), owned(), provider(), Db, post, UUID, Scoped payment monitoring and explicit, read-only provider reconciliation., reconcile() (+1 more)

### Community 153 - "record-demo.mjs"
Cohesion: 0.40
Nodes (4): credentials, headers, journey, target

### Community 154 - "Local Telegram/OpenAI runtime"
Cohesion: 0.25
Nodes (8): Configuration and data services, Delivery budget operation, Local Telegram/OpenAI runtime, Migrate and seed, Optional reminders and scheduler, Packaging and release limits, Run the processes, Validate and recover

### Community 155 - "generate_completion"
Cohesion: 0.15
Nodes (18): generate_completion(), Any, Bounded OpenAI-only model roles; provider details never escape in errors., Generate a completion with automatic provider fallback. Tries the fast model,…, asyncio, parametrize, Test that it returns successfully on the primary model., Test that it falls back to OpenAI if primary OpenAI model fails. (+10 more)

### Community 157 - "2. Boundaries & Invariants"
Cohesion: 0.50
Nodes (4): 2. Boundaries & Invariants, Always Do, Ask First, Never Do

### Community 160 - "8. RAG (Retrieval-Augmented Generation)"
Cohesion: 0.50
Nodes (4): 8.1 Per-Institution Knowledge Base, 8.2 Retrieval Pipeline, 8.3 RAG Guardrail, 8. RAG (Retrieval-Augmented Generation)

### Community 161 - "Phase 3–4 addition (see ADR-008)"
Cohesion: 0.29
Nodes (7): Phase 3–4 addition (see ADR-008), Task 40: `decide()` System-1 decision-layer abstraction, Task 41: Distill decisions into self-hosted Laya (post-demo), Task 42.1: Complex Document Parsing & Semantic Chunking, Task 42.2: Contextual Query Rewriting, Task 42.3: Pluggable Reranker (Cohere API vs Local), Task 42: Advanced RAG Strategy (ADR-011)

### Community 162 - "Phase 4: Advanced Bot Features"
Cohesion: 0.29
Nodes (7): Phase 4: Advanced Bot Features, Task 18: Application form collection node, Task 19: Razorpay integration, Task 20: Human handoff + co-pilot mode, Task 21: Cold lead re-engagement worker, Task 22: WhatsApp rate-limit tracking, Task 23: Langfuse tracing integration

### Community 164 - "Language review packet"
Cohesion: 0.40
Nodes (5): Current templates, Language review packet, Live exercise, Reference clarification, Reminder consent and outreach copy

### Community 165 - "exports.py"
Cohesion: 0.20
Nodes (16): clean(), download(), export_rows(), ExportRequest, Db, post, Response, Audited institution exports, with explicit limits and spreadsheet-safe text. (+8 more)

### Community 167 - "Phase 6: Production Hardening"
Cohesion: 0.33
Nodes (6): Phase 6: Production Hardening, Task 35: Sentry error monitoring, Task 36: Delete My Data endpoint, Task 37: Data retention auto-cleanup, Task 38: Docker Compose for local development, Task 39: Production deployment

### Community 168 - "timeline.py"
Cohesion: 0.19
Nodes (11): Cursor, Any, AsyncSession, BaseModel, datetime, field_validator, UUID, Bounded chronological transcript across inbound, replies and standalone… (+3 more)

### Community 169 - "add_conversation_runtime_714f092da3b8.py"
Cohesion: 0.50
Nodes (3): columns(), Column, upgrade()

### Community 171 - "UploadBodyLimit"
Cohesion: 0.25
Nodes (5): ASGIApp, UploadBodyLimit, Receive, Scope, Send

### Community 173 - "enqueue_outbound"
Cohesion: 0.15
Nodes (11): process_payment(), payment_webhook(), Db, post, Request, UUID, enqueue_outbound(), AsyncSession (+3 more)

### Community 177 - "AdmitFlow submission requirements"
Cohesion: 0.50
Nodes (4): AdmitFlow submission requirements, Demonstration, Required artifacts, Truthful claims

### Community 178 - "index_known_name"
Cohesion: 0.40
Nodes (5): index_known_name(), Connection, Mapper, Keep index updates atomic with encrypted names, including name removal., listens_for

### Community 179 - "10. Observability & Tracing"
Cohesion: 0.50
Nodes (4): 10.1 LLM Tracing (Langfuse), 10.2 Structured Logging, 10.3 Error Monitoring (Sentry), 10. Observability & Tracing

### Community 180 - "5. Code Style"
Cohesion: 0.50
Nodes (4): 5. Code Style, Python (Backend), Separation of Concerns, TypeScript (Frontend)

### Community 183 - "tasks/processing.py"
Cohesion: 0.12
Nodes (15): ping(), process_inbound_message(), Any, task, Background tasks for message processing. For now this module holds only the…, Smoke-test task: returns ``{"result": payload}``. Enqueued from the…, Process an inbound WhatsApp message (Task 17). This is a placeholder for the…, Tests for the TaskIQ broker setup and task execution (Task 3). All tests run… (+7 more)

## Knowledge Gaps
- **431 isolated node(s):** `admitflow-backend`, `fs`, `path`, `crypto`, `root` (+426 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1194 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CRM search and institution downloads` connect `review` to `test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment`, `leads.py`, `backend/README.md`?**
  _High betweenness centrality (0.110) - this node is a cross-community bridge._
- **Why does `write_audit_log()` connect `write_audit_log` to `leads.py`, `analytics`, `journey.py`, `transport.py`, `review`, `scheduler.py`, `get_engine`, `workspace`, `guidance.py`, `AdmitFlow — Task List`, `LeadStatus`, `require_admin`, `staff/payments.py`, `test_knowledge_workspace.py`, `payments/webhook.py`, `management.py`, `outreach/followups.py`, `exports.py`, `Event`, `operations.py`, `knowledge/processing.py`, `enqueue_outbound`, `test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment`, `copilot.py`, `auth.py`, `api.py`, `test_privacy.py`, `process_upload`, `sqlalchemy`, `models/__init__.py`, `telegram/service.py`, `telegram/outbound.py`, `live`?**
  _High betweenness centrality (0.095) - this node is a cross-community bridge._
- **Why does `AdmitFlow — Task List` connect `AdmitFlow — Task List` to `Phase 5: Dashboard Frontend (Next.js)`, `Phase 3–4 addition (see ADR-008)`, `Phase 4: Advanced Bot Features`, `Phase 6: Production Hardening`, `handle_turn`, `._post`, `2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `encrypt_pii()` (e.g. with `Consequences` and `Decision`) actually correct?**
  _`encrypt_pii()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 58 inferred relationships involving `LeadStatus` (e.g. with `record_stage_changes()` and `Lead`) actually correct?**
  _`LeadStatus` has 58 INFERRED edges - model-reasoned connections that need verification._
- **What connects `admitflow-backend`, `fs`, `path` to the rest of the system?**
  _431 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `analytics` be split into smaller, more focused modules?**
  _Cohesion score 0.0641025641025641 - nodes in this community are weakly interconnected._