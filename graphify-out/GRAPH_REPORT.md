# Graph Report - admitflow  (2026-10-24)

## Corpus Check
- 306 files · ~159,240 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: (none) 6, .example 2, .css 2)

## Summary
- 2701 nodes · 7450 edges · 191 communities (168 shown, 23 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 469 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `148af194`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ADR-008: System-1 Decision Layer (Laya / Jev)
- Conversation Engine (hand-rolled dispatcher)
- AdmitFlow Complete Specification
- Finalized Production Stack
- get_lead
- analytics
- Code Owns the Money
- journey.py
- RedisMutex
- review
- pdf_parser.py
- test_integration_security.py
- WhatsAppSender
- core/rag.py
- PII Encryption & Audit Log
- Razorpay Payment Integration
- get_settings
- admissions.tsx
- contextual_query
- encrypt_pii
- AIBoomi Startup Weekend Kochi: fresh-session context
- Lead
- test_exports.py
- test_telegram_contracts.py
- LeadStatus
- Stages
- Course
- TestClient
- run_postman_check.cjs
- Task List
- pg_url
- test_crm_search.py
- AdmitFlow — Task List
- management.py
- Code Standards
- outreach/followups.py
- Event preparation and execution plan
- 7. Core Feature Specifications
- consent.py
- main.py
- ExtractionError
- send_message
- Hackathon resources for AdmitFlow
- manifest.json
- write_audit_log
- AdmitFlow: current state and planning baseline
- AdmitFlow: AIBoomi submission plan
- AdmitFlow — Complete Specification
- normalize_e164
- accept_update
- ADR-011: Required OpenAI passage reranking
- Testing
- check_input_safety
- AdmitFlow project handoff
- detect_intent
- tests/test_telegram_identity.py
- RuleOperator
- seed
- generate
- ADR-010: Triage Fallback Routing (Anti-Spam)
- ADR-012: Telegram and OpenAI for the first complete admissions MVP
- prepare
- compilerOptions
- change_password
- TelegramBot
- test_knowledge_workspace.py
- require_admin
- process_upload
- RazorpayClient
- Official source snapshots
- test_discovery.py
- get_redis
- get_sessionmaker
- budget.py
- management.tsx
- hashlib
- deliver
- dispatcher.py
- verify.sh
- db/__init__.py
- src/__init__.py
- tasks/__init__.py
- analytics.tsx
- whatsapp/__init__.py
- integration/__init__.py
- admitflow-backend
- edit_user
- AdmitFlow
- test_structured_documents.py
- PaymentProviderError
- test_decision_reranking.py
- hash_phone
- identity_database
- Git & GitHub Workflow
- package.json
- 13. Dashboard Features
- @playwright/test
- AGENTS.md
- Security & Production Readiness
- send
- next-env.d.ts
- sqlalchemy
- reindex_batch
- layout.tsx
- frontend/AGENTS.md
- scripts
- backend/README.md
- AdmitFlow pitch deck copy
- BaseModel
- TelegramClient
- models/__init__.py
- Quality Gates — Definition of Done
- AdmitFlow Backend
- devDependencies
- applications.tsx
- dependencies
- update
- Settings
- test_rag_node.py
- broker.py
- question_courses
- WhatsApp readiness check — October 22, 2026
- evaluate
- get_engine
- alembic
- payments.tsx
- test_expired_lease_recovery_cap_and_configuration_cancellation
- StaffAccounts
- Knowledge
- test_local_runtime.py
- env.py
- send_reply
- pathlib
- event_dependencies
- page.tsx
- AdmitFlow execution and demonstration checklist
- add_institution_knowledge_workspace_b627da2f7e11.py
- enqueue_outbound
- test_worker_broker.py
- prepare_document_models.py
- test_webhook.py
- lead_statement
- verify_compose.py
- test_integrations_notifications.py
- notifications.tsx
- Phase 5: Dashboard Frontend (Next.js)
- Phase 3: AI Core (Engine + RAG)
- limits.py
- 11. Human-in-the-Loop (Full Workflow)
- staff/payments.py
- record-demo.mjs
- Local Telegram/OpenAI runtime
- generate_completion
- 10. Observability & Tracing
- 2. Boundaries & Invariants
- 20260929_initial_schema_64cfce85009d.py
- 5. Code Style
- 8. RAG (Retrieval-Augmented Generation)
- transport.py
- add_conversation_runtime_714f092da3b8.py
- durable_payments_outbound_f129a064c5e8.py
- Language review packet
- 20261008_add_knowledge_models_for_rag_c470f1ebc811.py
- configure
- signin
- Cursor
- configured_keys
- AdmitFlow submission requirements
- Phase 4: Advanced Bot Features
- test_ingest_document
- One final WhatsApp check with Postman
- Phase 3–4 addition (see ADR-008)
- Phase 6: Production Hardening
- log_delivery_status
- index_known_name
- Implementation Plan: AdmitFlow
- record_stage_changes
- evaluate_reranking.py
- users
- verify_webhook
- 3. Tech Stack & Commands
- isolated_local_login_windows
- test_payment_and_webhook_claims_wait_for_erasure_lock
- 17. Decisions & Open Questions
- DOCUMENT_REVIEW.md

## God Nodes (most connected - your core abstractions)
1. `encrypt_pii()` - 104 edges
2. `write_audit_log()` - 96 edges
3. `get_settings()` - 93 edges
4. `LeadStatus` - 90 edges
5. `Lead` - 79 edges
6. `decrypt_pii()` - 75 edges
7. `Reply` - 74 edges
8. `TelegramBot` - 66 edges
9. `signin()` - 60 edges
10. `Course` - 56 edges

## Surprising Connections (you probably didn't know these)
- `Task 4: PII encryption utilities and audit log infrastructure` --references--> `write_audit_log()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/db/audit.py
- `17.1 Conversation engine — DECIDED: hand-rolled dispatcher` --references--> `handle_turn()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/SPEC.md → backend/src/engine/dispatcher.py
- `Task 17: Wire webhook → TaskIQ → engine dispatcher → WhatsApp` --references--> `handle_turn()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/engine/dispatcher.py
- `Task 8: Engine state definition and lifecycle` --references--> `handle_turn()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/engine/dispatcher.py
- `Missing-reply investigation (approximately 22:59 IST)` --references--> `process_inbound_message()`  [INFERRED]
  docs/event/READINESS_CHECK.md → backend/src/tasks/processing.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Finalized Production Stack Components** — docs_decisions_adr_007_finalized_stack_finalized_stack, docs_decisions_adr_007_finalized_stack_fly_io, docs_decisions_adr_007_finalized_stack_neon, docs_decisions_adr_007_finalized_stack_redis, docs_decisions_adr_007_finalized_stack_langfuse [EXTRACTED 1.00]
- **handle_turn() Per-Turn Pipeline** — spec_hand_rolled_dispatcher, docs_decisions_adr_008_system_1_decision_layer_decide, docs_decisions_adr_005_three_layer_guardrails_three_layer_guardrails, docs_decisions_adr_004_memory_architecture_episodic_memory, spec_code_owns_the_money [EXTRACTED 1.00]
- **System-1 Decision Engine (decide + primitives + models)** — docs_decisions_adr_008_system_1_decision_layer_system_1_decision_layer, docs_decisions_adr_008_system_1_decision_layer_decide, docs_research_system_1_decision_models_laya_jev_choice, docs_research_system_1_decision_models_laya_jev_score, docs_research_system_1_decision_models_laya_jev_noul, docs_research_system_1_decision_models_laya_jev_laya [EXTRACTED 1.00]
- **AdmitFlow AI Core Architecture** — tasks_plan_conversation_engine, tasks_plan_decide_decision_layer, tasks_plan_three_layer_guardrails, tasks_plan_rag_pipeline [INFERRED 0.85]
- **WhatsApp Ingress → Worker → Engine Flow** — tasks_plan_fastapi_webhook, tasks_plan_redis, tasks_plan_taskiq, tasks_plan_conversation_engine [INFERRED 0.85]

## Communities (191 total, 23 thin omitted)

### Community 0 - "ADR-008: System-1 Decision Layer (Laya / Jev)"
Cohesion: 0.16
Nodes (17): ADR-001: Hybrid Architecture, ADR-004: Dual Memory Architecture, Episodic Memory (messages table), Semantic Memory (lead_facts table), ADR-005: Three-Layer Guardrails and RAG, Three-Layer Guardrails, ADR-007: Finalized Production Stack, ADR-008: System-1 Decision Layer (Laya / Jev) (+9 more)

### Community 1 - "Conversation Engine (hand-rolled dispatcher)"
Cohesion: 0.25
Nodes (8): Conversation Engine (hand-rolled dispatcher), System-1 decide() Decision Layer, FastAPI WhatsApp Webhook, Langfuse LLM Tracing, pgvector RAG Pipeline, Redis (mutex / dedup / rate-limit), TaskIQ Background Worker, Three-Layer Guardrails

### Community 2 - "AdmitFlow Complete Specification"
Cohesion: 0.20
Nodes (9): AI Impact Statement, Student-to-staff demonstration, Prior-work disclosure draft, AdmitFlow necessary resources, Planning baseline before Telegram alignment, AdmitFlow Complete Specification, AdmitFlow Platform, AdmitFlow Implementation Plan (+1 more)

### Community 3 - "Finalized Production Stack"
Cohesion: 0.18
Nodes (11): ADR-002: Webhook Concurrency and Deduplication, Per-Phone Redis Mutex, Webhook Deduplication (Redis SETNX), ADR-003: Multi-Tenancy Strategy, Multi-Tenancy (Row-Level Isolation), Finalized Production Stack, Fly.io (Backend + Worker + Scheduler), Langfuse Cloud (LLM Tracing) (+3 more)

### Community 4 - "get_lead"
Cohesion: 0.26
Nodes (15): lead_summary(), Any, course_options(), get_lead(), human_requests(), lead_detail(), leads(), Any (+7 more)

### Community 5 - "analytics"
Cohesion: 0.14
Nodes (21): alias, analytics(), bucket_dates(), count(), percent(), Period, period_window(), Any (+13 more)

### Community 6 - "Code Owns the Money"
Cohesion: 0.50
Nodes (5): ADR-006: Code-Owned Qualification and Payments, Intent: Admissions Flow and Discounts, Discount Codes, Code Owns Eligibility, Code Owns the Money

### Community 7 - "journey.py"
Cohesion: 0.11
Nodes (43): action(), application_action(), collect_application(), prompt(), Any, AsyncSession, Button, Event (+35 more)

### Community 8 - "RedisMutex"
Cohesion: 0.07
Nodes (28): MutexAcquireError, Redis, RuntimeError, Redis distributed mutex with owner-safe release and keepalive (Task 7). Ensures…, Background loop that extends the TTL while the lock is held., Raised when the mutex cannot be acquired after all retries., Async context-manager mutex backed by Redis ``SET NX``. Parameters: redis: An…, Attempt to acquire the lock, retrying up to ``retry_count`` times. (+20 more)

### Community 9 - "review"
Cohesion: 0.33
Nodes (10): CRM search and institution downloads, applications(), detail(), owned(), Any, Db, get, post (+2 more)

### Community 10 - "pdf_parser.py"
Cohesion: 0.13
Nodes (17): kill_descendants(), parse_pdf(), Offline PDF child process with per-loop backpressure, memory and time limits., Include Windows venv redirector children and any parser subprocesses., resident_memory(), watch_memory(), Process, fixture (+9 more)

### Community 11 - "test_integration_security.py"
Cohesion: 0.17
Nodes (17): Durable, minimal institution events and signed outbound integrations., destination(), post_event(), public_ip(), resolve_public(), signature(), parametrize, Outbound integrations reject unsafe destinations and sign exact delivery bytes. (+9 more)

### Community 12 - "WhatsAppSender"
Cohesion: 0.09
Nodes (23): Any, Send an interactive list message. `sections` is a list of section dicts…, Send a pre-approved template message., Service for sending messages via Meta WhatsApp Cloud API., Post the payload to Meta and extract the created message ID., Meta API expects the phone number without the leading '+'., Send a simple text message. Returns the Meta message ID., Send an interactive message with up to 3 buttons. `buttons` should be a list of… (+15 more)

### Community 13 - "core/rag.py"
Cohesion: 0.16
Nodes (16): chunk_text(), embed_text(), ingest_document(), Any, AsyncSession, UUID, RAG pipeline core logic (Task 13). Handles ingestion (chunking, embedding),…, Generate embedding for text using configured model. (+8 more)

### Community 16 - "get_settings"
Cohesion: 0.11
Nodes (21): AsyncBroker, get_settings(), Return the process-wide :class:`Settings` singleton., embed_chunks(), Use the configured OpenAI model with the database's explicit 1536 dimensions., main(), Probe, BaseModel (+13 more)

### Community 17 - "admissions.tsx"
Cohesion: 0.12
Nodes (15): Admissions(), Detail, Human, Inquiry, labels, Request, RuleEvidence, statusLabel() (+7 more)

### Community 18 - "contextual_query"
Cohesion: 0.13
Nodes (17): contextual_query(), Resolve pronouns/slang using bounded recent turns; uncertainty asks the…, retrieval_query(), evaluate(), main(), Bounded synthetic OpenAI reference resolution; no database writes or sends., MonkeyPatch, parametrize (+9 more)

### Community 19 - "encrypt_pii"
Cohesion: 0.12
Nodes (29): decrypt_pii(), encrypt_pii(), Encrypt a PII string, returning a url-safe base64 Fernet token. Fernet is…, Decrypt a token produced by :func:`encrypt_pii`. Raises…, test_all_aggregates_share_a_snapshot_during_concurrent_arrivals(), interleave(), test_application_collection_is_explicit_encrypted_and_replay_safe(), exercise() (+21 more)

### Community 20 - "AIBoomi Startup Weekend Kochi: fresh-session context"
Cohesion: 0.11
Nodes (19): AIBoomi Startup Weekend Kochi: fresh-session context, Assessment and next decision, Current readiness session (October 22), Event sources and local copies, Existing prototype rule and surprise element, Existing working-tree changes, Fresh-message prompt, Handoff status (+11 more)

### Community 21 - "Lead"
Cohesion: 0.19
Nodes (23): Lead, A prospective applicant with optional phone contact and channel identities.…, button(), discount_action(), order_reply(), payment_action(), preview(), Any (+15 more)

### Community 22 - "test_exports.py"
Cohesion: 0.43
Nodes (6): clean(), render_csv(), render_xlsx(), Download encoding prevents formulas while preserving international phone…, test_downloads_never_treat_user_text_as_formulas(), io

### Community 23 - "test_telegram_contracts.py"
Cohesion: 0.24
Nodes (9): normalize_update(), protect_logs(), LogRecord, TaskIQ changes log levels; redact before either HTTP client or root handlers…, TokenSafeFilter, Private-chat normalization, callback ownership and validated reply limits., test_callback_actor_and_origin(), test_http_logs_redact_bot_credentials() (+1 more)

### Community 24 - "LeadStatus"
Cohesion: 0.10
Nodes (36): LeadStatus, Lead lifecycle states (SPEC §7.3). Where a lead *stands*, not a fixed track —…, QualificationRule, A structured eligibility rule evaluated in code, not by the LLM (ADR-006).…, AsyncSession, Run the qualification loop., run_qualification(), EngineState (+28 more)

### Community 25 - "Stages"
Cohesion: 0.13
Nodes (15): 10. Reflect & learn, 1. Understand & spec  (`/spec`), 2. Plan & pick a task  (`/plan`), 3. Branch, 4. Build with TDD  (`/build`, `/test`), 5. Verify (the quality gate), 6. Self-review, then adversarial review  (`/review`), 7. Commit & open the PR (+7 more)

### Community 26 - "Course"
Cohesion: 0.10
Nodes (28): alembic_config, Dashboard access role (SPEC — admin vs agent)., StaffRole, Course, A program a lead can be qualified for and pay to apply to., Institution, Institution (the tenant root) and its staff users., An institution, optionally connected to a legacy WhatsApp number. The tenant… (+20 more)

### Community 27 - "TestClient"
Cohesion: 0.19
Nodes (8): Any, TestClient, Statuses (read/delivered) have no 'messages' array., GET /api/webhook challenge verification., POST /api/webhook payload processing., sign_payload(), TestWebhookProcessing, TestWebhookVerification

### Community 28 - "run_postman_check.cjs"
Cohesion: 0.20
Nodes (8): collection, config, crypto, fs, keys, newman, path, root

### Community 29 - "Task List"
Cohesion: 0.15
Nodes (13): Checkpoint: Advanced Features, Checkpoint: AI Core, Checkpoint: Dashboard Complete, Checkpoint: Foundation, Checkpoint: Production Ready, Checkpoint: WhatsApp Ingress, Phase 1: Foundation, Phase 2: WhatsApp Ingress (+5 more)

### Community 30 - "pg_url"
Cohesion: 0.19
Nodes (14): _alembic_config(), monkeypatch_session(), pg_url(), fixture, MonkeyPatch, Start Postgres, point settings at it, yield the asyncpg URL., The tier requirement: alembic upgrade head then downgrade base, both clean., test_migration_applies_up_and_down() (+6 more)

### Community 31 - "test_crm_search.py"
Cohesion: 0.19
Nodes (16): Core cross-cutting concerns: settings, security, schemas, guardrails, tracing., name_tokens(), normalized_phone(), UUID, query_tokens(), Tenant-keyed blind name prefixes; plaintext remains in encrypted columns only., token(), words() (+8 more)

### Community 32 - "AdmitFlow — Task List"
Cohesion: 0.15
Nodes (13): AdmitFlow — Task List, AIBoomi Startup Weekend session handoff (2026-10-22), Current direction and hackathon resources (2026-10-23), Final Postman diagnostic (October 23, executed; delivery blocked), Phase 1: Foundation, Readiness blocker: idle Redis worker restart (in progress), Readiness tunnel setup (in progress), Task 1: Initialize Python project, FastAPI, settings, and Docker (+5 more)

### Community 33 - "management.py"
Cohesion: 0.20
Nodes (31): DiscountType, How a discount code reduces the fee., archive_course(), archive_discount(), catalog(), catalog_detail(), course_view(), CourseInput (+23 more)

### Community 34 - "Code Standards"
Cohesion: 0.18
Nodes (11): Async & I/O, Code Standards, Configuration — settings, not literals, Dependencies, Errors, Formatting, LLM calls, Logging & observability (+3 more)

### Community 35 - "outreach/followups.py"
Cohesion: 0.08
Nodes (39): escalation_reason(), office_open(), datetime, Reason, Deterministic clear support signals and institution-local office hours., load_memory(), activity(), after_send() (+31 more)

### Community 36 - "Event preparation and execution plan"
Cohesion: 0.18
Nodes (11): Business and mentor preparation, Evaluation and demo evidence, Event preparation and execution plan, Kickoff disclosure draft, Latest direction (October 23), Minimum demonstrable product, Next action: one-hour v1 readiness check, Submission checklist (+3 more)

### Community 37 - "7. Core Feature Specifications"
Cohesion: 0.18
Nodes (11): 7.10 Payment Integration & Discounts (Razorpay), 7.1 WhatsApp Number Architecture, 7.2 Multi-Tenancy (Row-Level Isolation), 7.3 Lead Lifecycle States, 7.4 Course Qualification Rules (Structured), 7.5 Batch & Intake Management, 7.6 Cold Lead Re-engagement, 7.7 Language Support (+3 more)

### Community 38 - "consent.py"
Cohesion: 0.24
Nodes (14): cancel_queued(), note_inbound(), preference_reply(), Any, AsyncSession, datetime, Student-owned reminder preferences apply even while staff has paused the bot., callback_data() (+6 more)

### Community 39 - "main.py"
Cohesion: 0.11
Nodes (16): create_app(), lifespan(), FastAPI, FastAPI application entry point. Boots the API, manages the TaskIQ broker…, Start / stop the TaskIQ broker alongside the FastAPI process. The…, Application factory — builds and configures the FastAPI instance., Tests for the /debug endpoints (Task 3 verification)., GET /debug/enqueue-ping should enqueue a ping task and return its ID. (+8 more)

### Community 40 - "ExtractionError"
Cohesion: 0.19
Nodes (21): extract_file(), ExtractionError, ValueError, Bounded extraction of institution reference documents; never execute uploads., A safe, public error code rather than parser output containing document text., validate_path(), convert_pdf(), main() (+13 more)

### Community 41 - "send_message"
Cohesion: 0.36
Nodes (10): active_request(), Any, AsyncSession, Db, post, UUID, require_takeover(), resume() (+2 more)

### Community 42 - "Hackathon resources for AdmitFlow"
Cohesion: 0.20
Nodes (10): Acceptance before using a resource, Event and release boundaries, Goal, Hackathon resources for AdmitFlow, October 23 Downloads guide: hosted inference access, Participant credits and other support, Suggested allocation and activation order, Useful resources mapped to the plan (+2 more)

### Community 43 - "manifest.json"
Cohesion: 0.20
Nodes (9): SPEC.md, bytes, sha256, tasks/plan.md, bytes, sha256, tasks/todo.md, bytes (+1 more)

### Community 44 - "write_audit_log"
Cohesion: 0.08
Nodes (47): Application settings singleton. Loads configuration from the environment (and…, AsyncSession, UUID, Audit-log write helper. :func:`write_audit_log` is the one path significant…, Append one entry to ``audit_logs`` on ``session``; return it flushed, not…, write_audit_log(), Async engine and session factory. Built lazily from ``settings.database_url``…, Authenticated institution file/folder uploads, status, retry, deletion and… (+39 more)

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

### Community 49 - "accept_update"
Cohesion: 0.08
Nodes (30): accept_update(), Any, Commit the encrypted inbox and offset in the same transaction, before…, age(), callback(), outreach(), fixture, parametrize (+22 more)

### Community 50 - "ADR-011: Required OpenAI passage reranking"
Cohesion: 0.40
Nodes (4): ADR-011: Required OpenAI passage reranking, Decision, Separate retrieval work, Verification and tradeoffs

### Community 51 - "Testing"
Cohesion: 0.22
Nodes (9): Browser announcement regions, Coverage, LLM and decision-layer tests, Philosophy — pragmatic TDD, Running tests, Test layout, Testing, The two patterns (+1 more)

### Community 52 - "check_input_safety"
Cohesion: 0.16
Nodes (18): check_input_safety(), Check if the user input is safe to process. 1. Deterministic checks…, asyncio, Test output guardrail with safe content., Test output guardrail blocks hallucinated fee., Test that a clean message passes through., Test that profanity is blocked deterministically without calling the LLM., Test that simple injection heuristics are blocked deterministically. (+10 more)

### Community 53 - "AdmitFlow project handoff"
Cohesion: 0.25
Nodes (8): AdmitFlow project handoff, Current direction, Development rules, Event submission, Execution checkpoint, First usable release, Historical evidence, Resume prompt

### Community 54 - "detect_intent"
Cohesion: 0.20
Nodes (15): detect_intent(), Classify the user's intent to route to the correct node. Design Decision: If a…, asyncio, Test routing for course discovery., Test routing for knowledge questions., Test routing for qualification answers., Test routing for human handoff., Test routing for empty messages without calling LLM defaults to discovery. (+7 more)

### Community 55 - "tests/test_telegram_identity.py"
Cohesion: 0.19
Nodes (10): hash_telegram_identifier(), UUID, Private Telegram identity lookup without storing raw identifiers in indexes., Hash an identifier in its tenant/bot/type domain using the lookup secret. This…, MonkeyPatch, parametrize, Telegram identities must be independent of phone numbers and tenant-bound., test_lookup_hash_is_stable_scoped_and_does_not_reveal_identifiers() (+2 more)

### Community 56 - "RuleOperator"
Cohesion: 0.18
Nodes (17): Qualification-rule comparison operators (SPEC §7.4). Evaluated…, RuleOperator, ExtractionResponse, BaseModel, Qualification Node (Task 15). Extracts rule fields using the LLM and runs…, Structured output expected from the LLM when extracting fields., _coerce_values(), evaluate_rule() (+9 more)

### Community 57 - "seed"
Cohesion: 0.15
Nodes (16): payments(), Any, get, UUID, seed(), exercise(), Any, MonkeyPatch (+8 more)

### Community 58 - "generate"
Cohesion: 0.14
Nodes (17): content(), decide(), DraftContent, DraftDecision, DraftRequest, generate(), latest(), Any (+9 more)

### Community 59 - "ADR-010: Triage Fallback Routing (Anti-Spam)"
Cohesion: 0.33
Nodes (5): ADR-010: Triage Fallback Routing (Anti-Spam), Consequences, Context, Decision, Status

### Community 60 - "ADR-012: Telegram and OpenAI for the first complete admissions MVP"
Cohesion: 0.29
Nodes (7): ADR-012: Telegram and OpenAI for the first complete admissions MVP, Consequences, Context, Decision, Implemented runtime boundaries, References and verification, Supersession and preserved decisions

### Community 61 - "prepare"
Cohesion: 0.16
Nodes (13): prepare(), Any, MonkeyPatch, parametrize, test_clear_escalation_records_request_outside_hours_without_a_model(), unavailable(), test_copilot_provider_failure_never_queues_a_message(), test_copilot_requires_review_rejects_stale_and_deduplicates_approval() (+5 more)

### Community 63 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 64 - "change_password"
Cohesion: 0.06
Nodes (47): change_password(), issue_session(), Login, logout(), me(), PasswordChange, AsyncSession, BaseModel (+39 more)

### Community 65 - "TelegramBot"
Cohesion: 0.12
Nodes (21): Trusted bot-to-institution mapping; token is application-encrypted., TelegramBot, exercise(), Any, test_fee_changes_require_another_tap_and_legacy_paid_orders_are_not_charged_again(), exercise(), Any, test_transcript_paginates_inbound_bot_and_standalone_deliveries() (+13 more)

### Community 66 - "test_knowledge_workspace.py"
Cohesion: 0.09
Nodes (40): asyncio, ConversationEvent, ConversationReply, OutboundMessage, Bounded chronological transcript across inbound, replies and standalone…, event_text(), AsyncSession, Human-readable callback summaries without exposing routing or signature details. (+32 more)

### Community 67 - "require_admin"
Cohesion: 0.16
Nodes (22): encrypt_bytes(), Encrypt uploaded source bytes before persistence, without lossy text decoding., assign_scope(), documents(), get_upload(), Any, BaseModel, Db (+14 more)

### Community 68 - "process_upload"
Cohesion: 0.29
Nodes (7): process_upload(), UUID, Claim once, process outside the transaction, then publish only the current…, Any, test_course_scope_authority_search_and_faq(), index(), seed()

### Community 70 - "RazorpayClient"
Cohesion: 0.14
Nodes (18): AsyncBaseTransport, Credentials, Bounded Razorpay requests; ambiguous link creation is never blindly retried., RazorpayClient, discounted_amount(), process_payment(), provision(), Read-only credential probe, then encrypted institution-owned Razorpay… (+10 more)

### Community 71 - "Official source snapshots"
Cohesion: 0.50
Nodes (4): Conflicts to confirm, October 23 planning refresh, Official source snapshots, Sources

### Community 72 - "test_discovery.py"
Cohesion: 0.13
Nodes (16): present_courses(), AsyncSession, Discovery Node (Task 12). Presents available courses as WhatsApp interactive…, Fetch active courses with available batches and present to user. Only shows…, RuntimeError, WhatsApp message sending service (Task 6). Uses httpx2 to call the Meta Graph…, Raised when the Meta Cloud API returns an error response., WhatsAppAPIError (+8 more)

### Community 73 - "get_redis"
Cohesion: 0.13
Nodes (16): get_redis(), Redis, RuntimeError, Shared async Redis client for application code. Carry-over prerequisite #1: the…, Raised when Redis is needed but ``REDIS_URL`` is unset in settings., Return the process-wide async Redis client singleton. The client is created…, RedisNotConfiguredError, post (+8 more)

### Community 74 - "get_sessionmaker"
Cohesion: 0.21
Nodes (16): async_sessionmaker, get_session(), get_sessionmaker(), AsyncSession, Return the process-wide async session factory., FastAPI dependency yielding a session that closes after the request., recover_payments(), main() (+8 more)

### Community 75 - "budget.py"
Cohesion: 0.15
Nodes (24): day_window(), local_counts(), Any, datetime, UUID, Atomic daily send-attempt budgets shared by every Telegram delivery path., Count confirmed deliveries once; a stats failure must not repeat a sent message., record_sent() (+16 more)

### Community 76 - "management.tsx"
Cohesion: 0.10
Nodes (13): blank, Discount, Discounts(), Batch, Course, empty, Management(), operators (+5 more)

### Community 77 - "hashlib"
Cohesion: 0.18
Nodes (9): Expose only the existing Meta webhook through the temporary demo tunnel., Integer monetary arithmetic and exact-byte webhook authentication., Hash the tested code/configuration without reading secrets or runtime data., WhatsApp Webhook routing (Task 5). Handles GET (challenge) and POST (incoming…, The temporary tunnel must not expose local debug or documentation routes., test_tunnel_app_keeps_webhook_verification(), hashlib, hmac (+1 more)

### Community 78 - "deliver"
Cohesion: 0.40
Nodes (5): deliver(), UUID, task, Integration queue messages contain identifiers only., send_webhook()

### Community 79 - "dispatcher.py"
Cohesion: 0.09
Nodes (24): _flush_engine_state(), handle_turn(), _load_engine_state(), Any, AsyncSession, Engine Dispatcher (Task 8 & 17). This module contains the main entry point for…, Load EngineState from DB records., Flush mutations back to DB records. (+16 more)

### Community 84 - "analytics.tsx"
Cohesion: 0.28
Nodes (7): Analytics(), Conversion, labels, frontend_app_analytics_module, rate(), Report, shortDate()

### Community 89 - "edit_user"
Cohesion: 0.23
Nodes (16): admin_scope(), create_user(), CreateUser, edit_user(), EditUser, BaseModel, Db, post (+8 more)

### Community 90 - "AdmitFlow"
Cohesion: 0.33
Nodes (6): AdmitFlow, Current status, Demonstration and submission, Development, Product scope, Stack

### Community 91 - "test_structured_documents.py"
Cohesion: 0.19
Nodes (14): blocks(), Markdown sections and table rows stay together within bounded evidence chunks., Keep section ancestry; repeat table headers instead of breaking row…, semantic_chunks(), table_parts(), table_start(), text_parts(), parametrize (+6 more)

### Community 92 - "PaymentProviderError"
Cohesion: 0.15
Nodes (15): PaymentLink, PaymentProviderError, BaseModel, Exception, field_validator, Read an existing exact reference; absence never authorizes another creation., Any, MonkeyPatch (+7 more)

### Community 93 - "test_decision_reranking.py"
Cohesion: 0.21
Nodes (18): UUID, Reorder only original, safe tenant candidates; never invent text or sources.…, rerank(), chunks(), Intent, asyncio, BaseModel, MonkeyPatch (+10 more)

### Community 94 - "hash_phone"
Cohesion: 0.11
Nodes (18): hash_phone(), Return a deterministic keyed hash of a phone number for lookup/dedup. Keyed…, crm_data(), seed(), fixture, test_hash_phone_differs_per_number(), test_hash_phone_is_deterministic(), test_hash_phone_is_not_plaintext_and_fits_column() (+10 more)

### Community 95 - "identity_database"
Cohesion: 0.36
Nodes (8): identity_database(), fixture, Use a disposable pgvector database; never mutate the demo database., test_downgrade_preserves_legacy_rows_and_refuses_to_destroy_telegram_data(), insert_rows(), inspect_and_clean(), remove_test_bot(), verify_legacy()

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
Cohesion: 0.20
Nodes (5): ref_node_child_process, ref_node_crypto, ref_node_fs, ref_node_path, @playwright/test

### Community 100 - "AGENTS.md"
Cohesion: 0.25
Nodes (7): AIBoomi Startup Weekend handoff, How we build — read the handbook, Knowledge graph, Quick commands (from `backend/`), The rules you cannot skip, What this project is, Workflow triggers

### Community 101 - "Security & Production Readiness"
Cohesion: 0.18
Nodes (11): Dependency & secret scanning, Deploy & rollback, External surfaces, Guardrails & money, Local full-stack (docker-compose), Multi-tenancy — isolation is a correctness bug if wrong, Observability, PII & data protection (DPDPA) (+3 more)

### Community 102 - "send"
Cohesion: 0.10
Nodes (20): decrypt_bytes(), _fernet(), Authenticate and decrypt source bytes for an authorized ingestion task., Any, MonkeyPatch, TestClient, readable_pdf(), send() (+12 more)

### Community 103 - "next-env.d.ts"
Cohesion: 0.50
Nodes (3): NOTE: This file should not be edited, frontend_next_types_root_params_d, frontend_next_types_routes_d

### Community 104 - "sqlalchemy"
Cohesion: 0.09
Nodes (44): Application-layer PII protection: symmetric encryption + deterministic hashing.…, ApplicationStatus, PaymentStatus, Enumerated types used across the schema. These are Python ``str`` enums mapped…, Payment order lifecycle (SPEC §7.10)., Application review status (SPEC §7.9 / lifecycle)., PaymentOrder, Application form submissions and their payment orders. (+36 more)

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

### Community 110 - "AdmitFlow pitch deck copy"
Cohesion: 0.25
Nodes (7): AdmitFlow pitch deck copy, Slide 1: AdmitFlow, Slide 2: The admissions inquiry, Slide 3: A working student journey, Slide 4: Institution knowledge and control, Slide 5: Technology and verification, Slide 6: Pilot and next steps

### Community 111 - "BaseModel"
Cohesion: 0.23
Nodes (7): BatchInput, Hours, BaseModel, RuleInput, SettingsInput, model_validator, Self

### Community 112 - "TelegramClient"
Cohesion: 0.13
Nodes (19): Any, RuntimeError, TelegramAPIError, TelegramClient, test_uncertain_delivery_does_not_schedule_more_outreach(), exercise(), uncertain(), Any (+11 more)

### Community 113 - "models/__init__.py"
Cohesion: 0.08
Nodes (66): Base, IdMixin, Declarative base, metadata naming convention, and shared column mixins. Every…, Declarative base shared by every AdmitFlow model., UUID primary key with an application-side default. UUIDs avoid cross-tenant…, Server-side created/updated timestamps., Row-level tenant scoping (ADR-003). Mixed into every tenant-scoped table., TenantMixin (+58 more)

### Community 114 - "Quality Gates — Definition of Done"
Cohesion: 0.33
Nodes (6): CI mirrors this exactly, Fast iteration vs the gate, Quality Gates — Definition of Done, The baseline gate (every change), The enforced-numbers ledger, The tiers — add gates by what the change touches

### Community 115 - "AdmitFlow Backend"
Cohesion: 0.12
Nodes (16): Admissions analytics, AdmitFlow Backend, Application payments, Configuration, Consented follow-up reminders, Current implementation and verification, Institution knowledge workspace, Local development (+8 more)

### Community 116 - "devDependencies"
Cohesion: 0.33
Nodes (6): devDependencies, @playwright/test, @types/node, @types/react, @types/react-dom, typescript

### Community 117 - "applications.tsx"
Cohesion: 0.25
Nodes (5): Applications(), Detail, fields, statuses, Summary

### Community 118 - "dependencies"
Cohesion: 0.40
Nodes (5): dependencies, @fontsource-variable/dm-sans, next, react, react-dom

### Community 119 - "update"
Cohesion: 0.16
Nodes (15): dispatch_pending(), recovery_loop(), dispatch_due(), Local operational commands with secrets entered through protected prompts., main(), Produce due reminder jobs and recover queued deliveries; safe to run after…, run(), purge_retained() (+7 more)

### Community 120 - "Settings"
Cohesion: 0.15
Nodes (15): Environment-backed application configuration., Settings, check_login_limit(), Request, Tests for the settings singleton., test_dotenv_is_explicit_in_tests(), test_env_overrides_defaults(), test_get_settings_returns_settings_instance() (+7 more)

### Community 121 - "test_rag_node.py"
Cohesion: 0.17
Nodes (14): Sanitizer to prevent RAG poisoning. Blocks chunks that contain obvious prompt…, sanitize_chunks(), process_rag_node(), AsyncSession, RAG Node (Task 14). Graph node that retrieves from the knowledge base and…, Retrieve context and answer knowledge questions., mock_state(), asyncio (+6 more)

### Community 122 - "broker.py"
Cohesion: 0.14
Nodes (12): TaskIQ broker singleton. In production (and local dev with Redis running) the…, ingest_upload(), task, TaskIQ entry point for institution document indexing., task, Encrypted outbound-message delivery jobs carry only internal identifiers., send_outbound_message(), create_payment_link() (+4 more)

### Community 123 - "question_courses"
Cohesion: 0.18
Nodes (11): AmbiguousCourseReference, AsyncSession, Course, UUID, ValueError, question_courses(), More than one active course has the requested name without a selected owner., Explicit catalog names take precedence over selection; no model invents IDs. (+3 more)

### Community 124 - "WhatsApp readiness check — October 22, 2026"
Cohesion: 0.15
Nodes (13): Decision so far, Delivery diagnosis and configuration repair (October 23, approximately 00:16 IST), Evidence collected before configuration, Final Postman retry (October 23), Live checkpoint (approximately 22:54 IST), Missing-reply investigation (approximately 22:59 IST), New test account configuration (October 23, approximately 09:45 IST), Next live checks and evidence required (+5 more)

### Community 125 - "evaluate"
Cohesion: 0.33
Nodes (9): Case, cases(), evaluate(), main(), BaseModel, score_answer(), Evaluation rejects irrelevant quotations and does not count provider errors as…, test_supported_answer_requires_expected_fact_and_reference() (+1 more)

### Community 126 - "get_engine"
Cohesion: 0.13
Nodes (17): AsyncEngine, DatabaseNotConfiguredError, get_engine(), RuntimeError, Raised when a DB session is requested but ``DATABASE_URL`` is unset., Return the process-wide async engine (one pool for the app)., main(), run() (+9 more)

### Community 128 - "payments.tsx"
Cohesion: 0.32
Nodes (6): label(), money(), outcomes, Payment, Payments(), statuses

### Community 129 - "test_expired_lease_recovery_cap_and_configuration_cancellation"
Cohesion: 0.22
Nodes (6): configure(), test_delivery_claim_retry_and_minimal_payload(), test_expired_lease_recovery_cap_and_configuration_cancellation(), inspect(), test_source_transaction_rolls_back_event_and_outbox(), exercise()

### Community 130 - "StaffAccounts"
Cohesion: 1.00
Nodes (3): StaffAccounts(), create(), mutate()

### Community 131 - "Knowledge"
Cohesion: 0.44
Nodes (9): refresh(), api(), Knowledge(), action(), assignScope(), login(), search(), upload() (+1 more)

### Community 132 - "test_local_runtime.py"
Cohesion: 0.19
Nodes (12): argparse, configure(), main(), Path, Create private isolated local Compose configuration without copying live…, asyncio, MonkeyPatch, Path (+4 more)

### Community 133 - "env.py"
Cohesion: 0.22
Nodes (9): do_run_migrations(), Connection, Alembic migration environment (async). Reads the database URL from application…, Emit SQL to stdout without a live DB connection., Run migrations against a live database via an async engine., run_migrations_offline(), run_migrations_online(), logging_config (+1 more)

### Community 134 - "send_reply"
Cohesion: 0.15
Nodes (7): process_telegram_event(), task, send_telegram_reply(), UUID, send_reply(), test_shared_budget_preserves_queues_and_settings_wake_deliveries(), second()

### Community 135 - "pathlib"
Cohesion: 0.15
Nodes (8): Bounded synthetic PDF upload/queue/OpenAI/search check; removes its own upload., Single-use PDF parser. Reads stdin; emits bounded JSON, never raw diagnostics., Five bounded live embedding searches through the real authenticated staff API., math, pathlib, pypdf, sys, warnings

### Community 137 - "page.tsx"
Cohesion: 0.12
Nodes (13): DeliveryBudget(), Usage, Exports(), Configuration, Integrations(), Request, Doc, errors (+5 more)

### Community 138 - "AdmitFlow execution and demonstration checklist"
Cohesion: 0.67
Nodes (3): AdmitFlow execution and demonstration checklist, Build and verify, Demonstrate and submit

### Community 139 - "add_institution_knowledge_workspace_b627da2f7e11.py"
Cohesion: 0.40
Nodes (4): Column, DateTime, _timestamps(), upgrade()

### Community 140 - "enqueue_outbound"
Cohesion: 0.14
Nodes (12): verify_webhook(), payment_webhook(), Db, post, Request, UUID, enqueue_outbound(), AsyncSession (+4 more)

### Community 141 - "test_worker_broker.py"
Cohesion: 0.25
Nodes (7): Tests for the TaskIQ broker setup and task execution (Task 3). All tests run…, When REDIS_URL is unset the factory should yield an InMemoryBroker., The ping task should run and return the expected payload., Ping without an explicit payload should default to 'pong'., test_broker_is_in_memory_without_redis_url(), test_ping_task_default_payload(), test_ping_task_returns_result()

### Community 142 - "prepare_document_models.py"
Cohesion: 0.22
Nodes (8): main(), prepare(), Path, Download only local PDF layout/table assets; no OCR, generation or document…, Tests use explicit configuration and never implicitly load developer…, importlib, importlib_metadata, os

### Community 143 - "test_webhook.py"
Cohesion: 0.22
Nodes (10): parametrize, test_delivery_status_logs_are_authenticated_and_exclude_pii(), test_tunnel_app_exposes_no_other_routes(), app(), client(), mock_settings(), FastAPI, fixture (+2 more)

### Community 144 - "lead_statement"
Cohesion: 0.21
Nodes (12): lead_statement(), LeadFilters, LeadSearch, BaseModel, Select, UUID, download(), export_rows() (+4 more)

### Community 145 - "verify_compose.py"
Cohesion: 0.43
Nodes (6): compose(), Verify the isolated local Compose stack without external API calls or sends., seed_credentials(), verify(), subprocess, websockets_asyncio_client

### Community 146 - "test_integrations_notifications.py"
Cohesion: 0.18
Nodes (9): Staff authentication and institution-scoped access., Keep development-only throttle state independent across database test cases., event_for(), Committed event delivery, signed destination configuration and live staff…, exercise(), exercise(), test_more_than_one_page_of_unread_events_remains_accessible(), seed() (+1 more)

### Community 147 - "notifications.tsx"
Cohesion: 0.33
Nodes (4): labels, Notice, Notifications(), Snapshot

### Community 148 - "Phase 5: Dashboard Frontend (Next.js)"
Cohesion: 0.17
Nodes (12): Phase 5: Dashboard Frontend (Next.js), Task 24: Initialize Next.js + dark mode + glassmorphism, Task 25: Authentication (email + password), Task 26: Dashboard home (funnel analytics), Task 27: Leads CRM page, Task 28: Course & batch management, Task 29: Chat takeover + co-pilot UI, Task 30: Document management (RAG) (+4 more)

### Community 149 - "Phase 3: AI Core (Engine + RAG)"
Cohesion: 0.18
Nodes (11): Phase 3: AI Core (Engine + RAG), Task 10: Input guardrail node, Task 11: Triage node (intent detection), Task 12: Discovery node, Task 13: RAG pipeline, Task 14: RAG node, Task 15: Qualification node, Task 16: Output guardrail (+3 more)

### Community 150 - "limits.py"
Cohesion: 0.15
Nodes (9): ASGIApp, Reject oversized multipart streams before they can fill temporary storage., UploadBodyLimit, private_send(), Receive, Scope, Send, starlette_responses (+1 more)

### Community 151 - "11. Human-in-the-Loop (Full Workflow)"
Cohesion: 0.40
Nodes (5): 11.1 Auto-Escalation Triggers, 11.2 Co-pilot Mode, 11.3 Business Hours, 11.4 Never Escalate, 11. Human-in-the-Loop (Full Workflow)

### Community 152 - "staff/payments.py"
Cohesion: 0.36
Nodes (12): EncryptionKeyNotConfiguredError, RuntimeError, Raised when a PII helper is used but its key is unset in settings., locked(), owned(), provider(), Db, post (+4 more)

### Community 153 - "record-demo.mjs"
Cohesion: 0.40
Nodes (4): credentials, headers, journey, target

### Community 154 - "Local Telegram/OpenAI runtime"
Cohesion: 0.25
Nodes (8): Configuration and data services, Delivery budget operation, Local Telegram/OpenAI runtime, Migrate and seed, Optional reminders and scheduler, Packaging and release limits, Run the processes, Validate and recover

### Community 155 - "generate_completion"
Cohesion: 0.06
Nodes (51): decide(), Any, Typed decisions through the existing OpenAI-only provider boundary., Validate structured model output; refusal/malformed output is never a decision.…, AllProvidersFailedError, generate_completion(), Any, Exception (+43 more)

### Community 156 - "10. Observability & Tracing"
Cohesion: 0.50
Nodes (4): 10.1 LLM Tracing (Langfuse), 10.2 Structured Logging, 10.3 Error Monitoring (Sentry), 10. Observability & Tracing

### Community 157 - "2. Boundaries & Invariants"
Cohesion: 0.50
Nodes (4): 2. Boundaries & Invariants, Always Do, Ask First, Never Do

### Community 159 - "5. Code Style"
Cohesion: 0.50
Nodes (4): 5. Code Style, Python (Backend), Separation of Concerns, TypeScript (Frontend)

### Community 160 - "8. RAG (Retrieval-Augmented Generation)"
Cohesion: 0.50
Nodes (4): 8.1 Per-Institution Knowledge Base, 8.2 Retrieval Pipeline, 8.3 RAG Guardrail, 8. RAG (Retrieval-Augmented Generation)

### Community 161 - "transport.py"
Cohesion: 0.22
Nodes (8): PrivateTransportLogs, protect_logs(), LogRecord, HTTPS delivery pins a public resolved address while retaining TLS host…, contextvars, ipaddress, socket, urllib_parse

### Community 162 - "add_conversation_runtime_714f092da3b8.py"
Cohesion: 0.50
Nodes (3): columns(), Column, upgrade()

### Community 163 - "durable_payments_outbound_f129a064c5e8.py"
Cohesion: 0.50
Nodes (3): common(), Column, upgrade()

### Community 164 - "Language review packet"
Cohesion: 0.40
Nodes (5): Current templates, Language review packet, Live exercise, Reference clarification, Reminder consent and outreach copy

### Community 166 - "configure"
Cohesion: 0.28
Nodes (9): configuration(), configure(), EndpointInput, Any, BaseModel, Db, get, put (+1 more)

### Community 167 - "signin"
Cohesion: 0.09
Nodes (19): test_local_cohort_counts_conversions_and_observed_stages(), test_tenant_is_derived_from_session_and_period_is_bounded(), test_zero_filled_weekly_buckets_and_empty_rates(), Any, test_concurrent_reviews_allocate_one_seat_and_repeated_approval_is_idempotent(), test_downloads_roles_datasets_limits_and_tenants(), test_search_scope_validation_and_audit(), Any (+11 more)

### Community 168 - "Cursor"
Cohesion: 0.40
Nodes (4): Cursor, BaseModel, datetime, field_validator

### Community 169 - "configured_keys"
Cohesion: 0.33
Nodes (7): configured_keys(), fixture, MonkeyPatch, Point ``security.get_settings`` at settings with the crypto keys set., Point ``security.get_settings`` at settings with no crypto keys., test_hash_phone_differs_per_pepper_key(), unset_keys()

### Community 170 - "AdmitFlow submission requirements"
Cohesion: 0.50
Nodes (4): AdmitFlow submission requirements, Demonstration, Required artifacts, Truthful claims

### Community 172 - "Phase 4: Advanced Bot Features"
Cohesion: 0.29
Nodes (7): Phase 4: Advanced Bot Features, Task 18: Application form collection node, Task 19: Razorpay integration, Task 20: Human handoff + co-pilot mode, Task 21: Cold lead re-engagement worker, Task 22: WhatsApp rate-limit tracking, Task 23: Langfuse tracing integration

### Community 173 - "test_ingest_document"
Cohesion: 0.33
Nodes (5): asyncio, patch, test_ingest_document(), test_sanitize_chunks(), Fresh baseline quality gate

### Community 175 - "Phase 3–4 addition (see ADR-008)"
Cohesion: 0.33
Nodes (6): Phase 3–4 addition (see ADR-008), Task 40: `decide()` System-1 decision-layer abstraction, Task 41: Distill decisions into self-hosted Laya (post-demo), Task 42.1: Complex Document Parsing & Semantic Chunking, Task 42.2: Contextual Query Rewriting, Task 42: Advanced RAG Strategy (ADR-011)

### Community 176 - "Phase 6: Production Hardening"
Cohesion: 0.33
Nodes (6): Phase 6: Production Hardening, Task 35: Sentry error monitoring, Task 36: Delete My Data endpoint, Task 37: Data retention auto-cleanup, Task 38: Docker Compose for local development, Task 39: Production deployment

### Community 177 - "log_delivery_status"
Cohesion: 0.40
Nodes (5): log_delivery_status(), Request, Response, Observe only authenticated status events, without recipient or error text., middleware

### Community 178 - "index_known_name"
Cohesion: 0.40
Nodes (5): index_known_name(), Connection, Mapper, Keep index updates atomic with encrypted names, including name removal., listens_for

### Community 179 - "Implementation Plan: AdmitFlow"
Cohesion: 0.40
Nodes (4): Architecture Decisions, Implementation Plan: AdmitFlow, Overview, Risks and Mitigations

### Community 180 - "record_stage_changes"
Cohesion: 0.50
Nodes (4): Any, Record persisted ORM transitions atomically; never infer an earlier stage., record_stage_changes(), Session

### Community 181 - "evaluate_reranking.py"
Cohesion: 0.67
Nodes (3): evaluate(), main(), Live synthetic OpenAI ranking check; no database writes or message delivery.

### Community 182 - "users"
Cohesion: 0.50
Nodes (4): Any, get, Response, users()

### Community 183 - "verify_webhook"
Cohesion: 0.50
Nodes (4): get, Response, Handle Meta's webhook challenge., verify_webhook()

### Community 184 - "3. Tech Stack & Commands"
Cohesion: 0.50
Nodes (4): 3. Tech Stack & Commands, Deployment, Hybrid Architecture, Key Commands

### Community 187 - "isolated_local_login_windows"
Cohesion: 0.67
Nodes (3): isolated_local_login_windows(), fixture, MonkeyPatch

### Community 189 - "17. Decisions & Open Questions"
Cohesion: 0.67
Nodes (3): 17.1 Conversation engine — DECIDED: hand-rolled dispatcher, 17.2 Still open, 17. Decisions & Open Questions

## Knowledge Gaps
- **419 isolated node(s):** `admitflow-backend`, `fs`, `path`, `crypto`, `root` (+414 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1177 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CRM search and institution downloads` connect `review` to `seed`, `get_lead`, `backend/README.md`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Why does `LeadStatus` connect `LeadStatus` to `test_expired_lease_recovery_cap_and_configuration_cancellation`, `get_lead`, `analytics`, `journey.py`, `review`, `enqueue_outbound`, `lead_statement`, `test_integrations_notifications.py`, `encrypt_pii`, `Lead`, `Course`, `outreach/followups.py`, `send_message`, `write_audit_log`, `accept_update`, `record_stage_changes`, `RuleOperator`, `seed`, `TelegramBot`, `test_knowledge_workspace.py`, `test_discovery.py`, `dispatcher.py`, `PaymentProviderError`, `hash_phone`, `sqlalchemy`, `models/__init__.py`, `test_rag_node.py`, `get_engine`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `write_audit_log()` connect `write_audit_log` to `get_lead`, `analytics`, `send_reply`, `journey.py`, `review`, `enqueue_outbound`, `lead_statement`, `test_integrations_notifications.py`, `Lead`, `staff/payments.py`, `Course`, `AdmitFlow — Task List`, `management.py`, `outreach/followups.py`, `consent.py`, `configure`, `send_message`, `record_stage_changes`, `users`, `seed`, `generate`, `change_password`, `test_knowledge_workspace.py`, `require_admin`, `process_upload`, `RazorpayClient`, `get_sessionmaker`, `budget.py`, `edit_user`, `sqlalchemy`, `models/__init__.py`, `update`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `encrypt_pii()` (e.g. with `Consequences` and `Decision`) actually correct?**
  _`encrypt_pii()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 54 inferred relationships involving `LeadStatus` (e.g. with `record_stage_changes()` and `Lead`) actually correct?**
  _`LeadStatus` has 54 INFERRED edges - model-reasoned connections that need verification._
- **What connects `admitflow-backend`, `fs`, `path` to the rest of the system?**
  _419 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `analytics` be split into smaller, more focused modules?**
  _Cohesion score 0.13852813852813853 - nodes in this community are weakly interconnected._