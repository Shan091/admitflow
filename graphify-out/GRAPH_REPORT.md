# Graph Report - admitflow  (2026-10-24)

## Corpus Check
- 309 files · ~161,031 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 7, .example 2, .css 2)

## Summary
- 2708 nodes · 7480 edges · 173 communities (152 shown, 21 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 472 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2dfaa0c7`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ADR-008: System-1 Decision Layer (Laya / Jev)
- Conversation Engine (hand-rolled dispatcher)
- AdmitFlow Complete Specification
- Finalized Production Stack
- leads.py
- exports.py
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
- encrypt_pii
- AIBoomi Startup Weekend Kochi: fresh-session context
- payments/service.py
- Course
- test_telegram_contracts.py
- LeadStatus
- Stages
- institution.py
- TestClient
- run_postman_check.cjs
- Task List
- pg_url
- test_crm_search.py
- Phase 5: Dashboard Frontend (Next.js)
- management.py
- Code Standards
- outreach/followups.py
- Event preparation and execution plan
- 7. Core Feature Specifications
- Lead
- main.py
- Document
- operations.py
- Hackathon resources for AdmitFlow
- manifest.json
- knowledge/processing.py
- AdmitFlow: current state and planning baseline
- AdmitFlow: AIBoomi submission plan
- AdmitFlow — Complete Specification
- normalize_e164
- age
- ADR-011: Required OpenAI passage reranking
- Testing
- test_guardrails.py
- AdmitFlow project handoff
- detect_intent
- tests/test_telegram_identity.py
- RuleOperator
- test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment
- copilot.py
- ADR-010: Triage Fallback Routing (Anti-Spam)
- ADR-012: Telegram and OpenAI for the first complete admissions MVP
- prepare
- 2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md
- compilerOptions
- auth.py
- send
- test_knowledge_workspace.py
- api.py
- enums.py
- decide
- RazorpayClient
- Official source snapshots
- discovery.py
- get_redis
- get_sessionmaker
- budget.py
- management.tsx
- security.py
- TelegramBot
- dispatcher.py
- verify.sh
- db/__init__.py
- src/__init__.py
- tasks/__init__.py
- analytics.tsx
- whatsapp/__init__.py
- integration/__init__.py
- admitflow-backend
- accounts.py
- AdmitFlow
- ExtractionError
- PaymentProviderError
- json
- hash_phone
- identity_database
- Git & GitHub Workflow
- package.json
- 13. Dashboard Features
- @playwright/test
- AGENTS.md
- Security & Production Readiness
- test_failure_retry_and_delete_during_indexing
- next-env.d.ts
- payments/webhook.py
- reindex_names.py
- layout.tsx
- frontend/AGENTS.md
- scripts
- backend/README.md
- AdmitFlow pitch deck
- TestWhatsAppSender
- TelegramClient
- models/__init__.py
- Quality Gates — Definition of Done
- telegram/service.py
- devDependencies
- applications.tsx
- dependencies
- scheduler.py
- Settings
- test_rag_node.py
- broker.py
- test_course_scope_authority_search_and_faq
- WhatsApp readiness check — October 22, 2026
- Reply
- live
- alembic
- payments.tsx
- office_open
- StaffAccounts
- Knowledge
- test_local_runtime.py
- env.py
- test_shared_budget_preserves_queues_and_settings_wake_deliveries
- verify_document_pipeline.py
- event_dependencies
- page.tsx
- AdmitFlow execution and demonstration checklist
- add_institution_knowledge_workspace_b627da2f7e11.py
- validate_services.py
- test_worker_broker.py
- verify_compose.py
- hashlib
- retrieval.py
- test_handle_turn_basic_flow
- staff/__init__.py
- notifications.tsx
- types
- Phase 3: AI Core (Engine + RAG)
- test_workspace_limits.py
- 11. Human-in-the-Loop (Full Workflow)
- staff/payments.py
- record-demo.mjs
- Local Telegram/OpenAI runtime
- pydantic
- test_existing_inquiries_upgrade_without_invented_consent
- 2. Boundaries & Invariants
- .__init__
- evaluate_live.py
- 8. RAG (Retrieval-Augmented Generation)
- test_explicit_consent_and_stop_during_staff_takeover
- privacy_dependencies
- README.md
- signin
- timeline
- log_delivery_status
- index_known_name
- whatsapp/webhook.py
- 3. Tech Stack & Commands
- isolated_local_login_windows
- test_payment_and_webhook_claims_wait_for_erasure_lock
- DOCUMENT_REVIEW.md

## God Nodes (most connected - your core abstractions)
1. `encrypt_pii()` - 104 edges
2. `write_audit_log()` - 96 edges
3. `get_settings()` - 93 edges
4. `LeadStatus` - 90 edges
5. `Reply` - 80 edges
6. `Lead` - 79 edges
7. `decrypt_pii()` - 75 edges
8. `TelegramBot` - 66 edges
9. `signin()` - 60 edges
10. `Course` - 56 edges

## Surprising Connections (you probably didn't know these)
- `Task 42.3: Pluggable Reranker (Cohere API vs Local)` --references--> `search_chunks()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/core/rag.py
- `Task 4: PII encryption utilities and audit log infrastructure` --references--> `write_audit_log()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/db/audit.py
- `17.1 Conversation engine — DECIDED: hand-rolled dispatcher` --references--> `handle_turn()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/SPEC.md → backend/src/engine/dispatcher.py
- `Task 17: Wire webhook → TaskIQ → engine dispatcher → WhatsApp` --references--> `handle_turn()`  [INFERRED]
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

## Communities (173 total, 21 thin omitted)

### Community 0 - "ADR-008: System-1 Decision Layer (Laya / Jev)"
Cohesion: 0.16
Nodes (17): ADR-001: Hybrid Architecture, ADR-004: Dual Memory Architecture, Episodic Memory (messages table), Semantic Memory (lead_facts table), ADR-005: Three-Layer Guardrails and RAG, Three-Layer Guardrails, ADR-007: Finalized Production Stack, ADR-008: System-1 Decision Layer (Laya / Jev) (+9 more)

### Community 1 - "Conversation Engine (hand-rolled dispatcher)"
Cohesion: 0.25
Nodes (8): Conversation Engine (hand-rolled dispatcher), System-1 decide() Decision Layer, FastAPI WhatsApp Webhook, Langfuse LLM Tracing, pgvector RAG Pipeline, Redis (mutex / dedup / rate-limit), TaskIQ Background Worker, Three-Layer Guardrails

### Community 2 - "AdmitFlow Complete Specification"
Cohesion: 0.26
Nodes (8): Executed final check, One final WhatsApp check with Postman, AdmitFlow necessary resources, Planning baseline before Telegram alignment, AdmitFlow Complete Specification, AdmitFlow Platform, AdmitFlow Implementation Plan, AdmitFlow Task List

### Community 3 - "Finalized Production Stack"
Cohesion: 0.18
Nodes (11): ADR-002: Webhook Concurrency and Deduplication, Per-Phone Redis Mutex, Webhook Deduplication (Redis SETNX), ADR-003: Multi-Tenancy Strategy, Multi-Tenancy (Row-Level Isolation), Finalized Production Stack, Fly.io (Backend + Worker + Scheduler), Langfuse Cloud (LLM Tracing) (+3 more)

### Community 4 - "leads.py"
Cohesion: 0.17
Nodes (25): lead_statement(), lead_summary(), LeadFilters, LeadSearch, Any, BaseModel, Select, UUID (+17 more)

### Community 5 - "exports.py"
Cohesion: 0.05
Nodes (52): alias, Admissions analytics, AdmitFlow Backend, Application payments, Configuration, Consented follow-up reminders, Current implementation and verification, Institution knowledge workspace (+44 more)

### Community 6 - "Code Owns the Money"
Cohesion: 0.50
Nodes (5): ADR-006: Code-Owned Qualification and Payments, Intent: Admissions Flow and Discounts, Discount Codes, Code Owns Eligibility, Code Owns the Money

### Community 7 - "journey.py"
Cohesion: 0.22
Nodes (23): escalation_reason(), Reason, answer_question(), build_reply(), copy(), courses(), ExtractedFact, Extraction (+15 more)

### Community 8 - "RedisMutex"
Cohesion: 0.08
Nodes (26): MutexAcquireError, Redis, RuntimeError, Background loop that extends the TTL while the lock is held., Raised when the mutex cannot be acquired after all retries., Async context-manager mutex backed by Redis ``SET NX``. Parameters: redis: An…, Attempt to acquire the lock, retrying up to ``retry_count`` times., Release the lock using the Lua CAS script (owner-safe). (+18 more)

### Community 9 - "write_audit_log"
Cohesion: 0.13
Nodes (24): CRM search and institution downloads, Any, AsyncSession, UUID, Record persisted ORM transitions atomically; never infer an earlier stage., Append one entry to ``audit_logs`` on ``session``; return it flushed, not…, record_stage_changes(), write_audit_log() (+16 more)

### Community 10 - "pdf_parser.py"
Cohesion: 0.12
Nodes (19): kill_descendants(), parse_pdf(), Offline PDF child process with per-loop backpressure, memory and time limits., Include Windows venv redirector children and any parser subprocesses., resident_memory(), watch_memory(), Process, fixture (+11 more)

### Community 11 - "transport.py"
Cohesion: 0.05
Nodes (49): deliver(), UUID, destination(), post_event(), PrivateTransportLogs, protect_logs(), public_ip(), LogRecord (+41 more)

### Community 12 - "WhatsAppSender"
Cohesion: 0.18
Nodes (13): Any, Send an interactive list message. `sections` is a list of section dicts…, Send a pre-approved template message., Service for sending messages via Meta WhatsApp Cloud API., Post the payload to Meta and extract the created message ID., Meta API expects the phone number without the leading '+'., Send a simple text message. Returns the Meta message ID., Send an interactive message with up to 3 buttons. `buttons` should be a list of… (+5 more)

### Community 13 - "core/rag.py"
Cohesion: 0.13
Nodes (19): chunk_text(), embed_text(), ingest_document(), Any, AsyncSession, UUID, RAG pipeline core logic (Task 13). Handles ingestion (chunking, embedding),…, Generate embedding for text using configured model. (+11 more)

### Community 16 - "get_settings"
Cohesion: 0.18
Nodes (12): AsyncBroker, get_settings(), Return the process-wide :class:`Settings` singleton., _build_broker(), Construct the right broker based on the current settings. This is a plain…, A real Redis worker must stay listening while its queue is idle., test_idle_queue_listener_receives_a_later_message(), mock_settings() (+4 more)

### Community 17 - "admissions.tsx"
Cohesion: 0.12
Nodes (15): Admissions(), Detail, Human, Inquiry, labels, Request, RuleEvidence, statusLabel() (+7 more)

### Community 18 - "contextual_query"
Cohesion: 0.13
Nodes (17): contextual_query(), Resolve pronouns/slang using bounded recent turns; uncertainty asks the…, retrieval_query(), evaluate(), main(), Bounded synthetic OpenAI reference resolution; no database writes or sends., MonkeyPatch, parametrize (+9 more)

### Community 19 - "encrypt_pii"
Cohesion: 0.11
Nodes (31): decrypt_pii(), encrypt_pii(), Encrypt a PII string, returning a url-safe base64 Fernet token. Fernet is…, Decrypt a token produced by :func:`encrypt_pii`. Raises…, test_all_aggregates_share_a_snapshot_during_concurrent_arrivals(), interleave(), test_search_pages_are_bounded_and_do_not_drop_or_repeat_records(), seed() (+23 more)

### Community 20 - "AIBoomi Startup Weekend Kochi: fresh-session context"
Cohesion: 0.11
Nodes (19): AIBoomi Startup Weekend Kochi: fresh-session context, Assessment and next decision, Current readiness session (October 22), Event sources and local copies, Existing prototype rule and surprise element, Existing working-tree changes, Fresh-message prompt, Handoff status (+11 more)

### Community 21 - "payments/service.py"
Cohesion: 0.12
Nodes (32): ApplicationStatus, PaymentStatus, Payment order lifecycle (SPEC §7.10)., Application review status (SPEC §7.9 / lifecycle)., discount_action(), order_reply(), payment_action(), preview() (+24 more)

### Community 22 - "Course"
Cohesion: 0.08
Nodes (28): Application, PaymentOrder, Structured application data collected from an admission-ready lead (SPEC §7.9).…, A Razorpay order for an application fee (SPEC §7.10). Amount is DB-sourced…, Batch, Course, QualificationRule, A program a lead can be qualified for and pay to apply to. (+20 more)

### Community 23 - "test_telegram_contracts.py"
Cohesion: 0.13
Nodes (21): normalize_update(), protect_logs(), LogRecord, TaskIQ changes log levels; redact before either HTTP client or root handlers…, TokenSafeFilter, callback_data(), parse_callback(), UUID (+13 more)

### Community 24 - "LeadStatus"
Cohesion: 0.10
Nodes (34): LeadStatus, Lead lifecycle states (SPEC §7.3). Where a lead *stands*, not a fixed track —…, AsyncSession, Run the qualification loop., run_qualification(), EngineState, InvalidTransitionError, BaseModel (+26 more)

### Community 25 - "Stages"
Cohesion: 0.13
Nodes (15): 10. Reflect & learn, 1. Understand & spec  (`/spec`), 2. Plan & pick a task  (`/plan`), 3. Branch, 4. Build with TDD  (`/build`, `/test`), 5. Verify (the quality gate), 6. Self-review, then adversarial review  (`/review`), 7. Commit & open the PR (+7 more)

### Community 26 - "institution.py"
Cohesion: 0.08
Nodes (35): alembic_config, AsyncEngine, Dashboard access role (SPEC — admin vs agent)., StaffRole, Institution, Institution (the tenant root) and its staff users., An institution, optionally connected to a legacy WhatsApp number. The tenant…, A dashboard user (admin or agent) belonging to one institution. (+27 more)

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

### Community 32 - "Phase 5: Dashboard Frontend (Next.js)"
Cohesion: 0.04
Nodes (45): AdmitFlow — Task List, AIBoomi Startup Weekend session handoff (2026-10-22), Current direction and hackathon resources (2026-10-23), Final Postman diagnostic (October 23, executed; delivery blocked), Phase 1: Foundation, Phase 3–4 addition (see ADR-008), Phase 4: Advanced Bot Features, Phase 5: Dashboard Frontend (Next.js) (+37 more)

### Community 33 - "management.py"
Cohesion: 0.10
Nodes (47): require_admin(), archive_course(), archive_discount(), BatchInput, catalog(), catalog_detail(), course_view(), CourseInput (+39 more)

### Community 34 - "Code Standards"
Cohesion: 0.18
Nodes (11): Async & I/O, Code Standards, Configuration — settings, not literals, Dependencies, Errors, Formatting, LLM calls, Logging & observability (+3 more)

### Community 35 - "outreach/followups.py"
Cohesion: 0.12
Nodes (27): activity(), after_send(), before_send(), Check, course_available(), eligible(), generate_hook(), Hook (+19 more)

### Community 36 - "Event preparation and execution plan"
Cohesion: 0.18
Nodes (11): Business and mentor preparation, Evaluation and demo evidence, Event preparation and execution plan, Kickoff disclosure draft, Latest direction (October 23), Minimum demonstrable product, Next action: one-hour v1 readiness check, Submission checklist (+3 more)

### Community 37 - "7. Core Feature Specifications"
Cohesion: 0.20
Nodes (10): 7.10 Payment Integration & Discounts (Razorpay), 7.1 WhatsApp Number Architecture, 7.2 Multi-Tenancy (Row-Level Isolation), 7.3 Lead Lifecycle States, 7.5 Batch & Intake Management, 7.6 Cold Lead Re-engagement, 7.7 Language Support, 7.8 Lead Sources & Outbound (+2 more)

### Community 38 - "Lead"
Cohesion: 0.20
Nodes (17): Lead, A prospective applicant with optional phone contact and channel identities.…, Event, button(), submitted_reply(), cancel_queued(), note_inbound(), preference_reply() (+9 more)

### Community 39 - "main.py"
Cohesion: 0.11
Nodes (16): create_app(), lifespan(), FastAPI, FastAPI application entry point. Boots the API, manages the TaskIQ broker…, Start / stop the TaskIQ broker alongside the FastAPI process. The…, Application factory — builds and configures the FastAPI instance., Tests for the /debug endpoints (Task 3 verification)., GET /debug/enqueue-ping should enqueue a ping task and return its ID. (+8 more)

### Community 40 - "Document"
Cohesion: 0.23
Nodes (14): Document, An uploaded document in the institution's knowledge base., extract_file(), Bounded extraction of institution reference documents; never execute uploads., validate_path(), parametrize, Untrusted institutional files must extract safely or fail explicitly., test_compressed_docx_bombs_are_rejected() (+6 more)

### Community 41 - "operations.py"
Cohesion: 0.17
Nodes (18): active_request(), ManualMessage, Any, AsyncSession, BaseModel, Db, field_validator, post (+10 more)

### Community 42 - "Hackathon resources for AdmitFlow"
Cohesion: 0.20
Nodes (10): Acceptance before using a resource, Event and release boundaries, Goal, Hackathon resources for AdmitFlow, October 23 Downloads guide: hosted inference access, Participant credits and other support, Suggested allocation and activation order, Useful resources mapped to the plan (+2 more)

### Community 43 - "manifest.json"
Cohesion: 0.20
Nodes (9): SPEC.md, bytes, sha256, tasks/plan.md, bytes, sha256, tasks/todo.md, bytes (+1 more)

### Community 44 - "knowledge/processing.py"
Cohesion: 0.14
Nodes (16): decrypt_bytes(), Authenticate and decrypt source bytes for an authorized ingestion task., dispatch_pending(), process_upload(), UUID, Durable upload claims, bounded embedding and atomic publication of ready…, A database-backed inbox survives enqueue failures and lost worker leases., Claim once, process outside the transaction, then publish only the current… (+8 more)

### Community 45 - "AdmitFlow: current state and planning baseline"
Cohesion: 0.22
Nodes (9): AdmitFlow: current state and planning baseline, Confirmed user direction, Feature status and integration gaps, Features to finalize next, How to reconcile the planning documents, Proposed architecture for the next plan, Stack inventory, Verification evidence and its limits (+1 more)

### Community 46 - "AdmitFlow: AIBoomi submission plan"
Cohesion: 0.22
Nodes (9): AdmitFlow: AIBoomi submission plan, Deck and presentation, Open decisions, Proposed schedule from Friday evening, Submission outcome, The journey to demonstrate, Use the provided resources, What must be handed in (+1 more)

### Community 47 - "AdmitFlow — Complete Specification"
Cohesion: 0.10
Nodes (20): 10.1 LLM Tracing (Langfuse), 10.2 Structured Logging, 10.3 Error Monitoring (Sentry), 10. Observability & Tracing, 12. Edge Cases & Error Handling, 14. Data Privacy (DPDPA-Ready), 15. Memory Architecture, 16. Success Criteria (+12 more)

### Community 48 - "normalize_e164"
Cohesion: 0.14
Nodes (10): InvalidPhoneError, normalize_e164(), ValueError, E.164 phone-number normalization. Carry-over prerequisite #3: un-normalized…, Raised when a phone string cannot be normalized to E.164., Normalize *raw* into canonical E.164 (``+<digits>``). Strips whitespace,…, Tests for E.164 phone normalization (carry-over prerequisite #3). The…, normalize_e164 → canonical E.164 string. (+2 more)

### Community 49 - "age"
Cohesion: 0.13
Nodes (20): age(), outreach(), fixture, parametrize, seed(), test_budget_pause_does_not_spend_a_reminder_and_stop_cancels_it(), exercise(), test_exactly_two_reminders_then_cold_without_duplicate_delivery() (+12 more)

### Community 50 - "ADR-011: Required OpenAI passage reranking"
Cohesion: 0.40
Nodes (4): ADR-011: Required OpenAI passage reranking, Decision, Separate retrieval work, Verification and tradeoffs

### Community 51 - "Testing"
Cohesion: 0.22
Nodes (9): Browser announcement regions, Coverage, LLM and decision-layer tests, Philosophy — pragmatic TDD, Running tests, Test layout, Testing, The two patterns (+1 more)

### Community 52 - "test_guardrails.py"
Cohesion: 0.15
Nodes (16): asyncio, Test output guardrail with safe content., Test output guardrail blocks hallucinated fee., Test that a clean message passes through., Test that profanity is blocked deterministically without calling the LLM., Test that simple injection heuristics are blocked deterministically., Test that complex prompt injection is caught by the LLM., Test that Markdown formatting is converted to WhatsApp formatting. (+8 more)

### Community 53 - "AdmitFlow project handoff"
Cohesion: 0.25
Nodes (8): AdmitFlow project handoff, Current direction, Development rules, Event submission, Execution checkpoint, First usable release, Historical evidence, Resume prompt

### Community 54 - "detect_intent"
Cohesion: 0.20
Nodes (15): detect_intent(), Classify the user's intent to route to the correct node. Design Decision: If a…, asyncio, Test routing for course discovery., Test routing for knowledge questions., Test routing for qualification answers., Test routing for human handoff., Test routing for empty messages without calling LLM defaults to discovery. (+7 more)

### Community 55 - "tests/test_telegram_identity.py"
Cohesion: 0.23
Nodes (8): hash_telegram_identifier(), Hash an identifier in its tenant/bot/type domain using the lookup secret. This…, MonkeyPatch, parametrize, Telegram identities must be independent of phone numbers and tenant-bound., test_lookup_hash_is_stable_scoped_and_does_not_reveal_identifiers(), test_lookup_requires_a_configured_secret(), test_private_chat_identity_rejects_invalid_identifiers()

### Community 56 - "RuleOperator"
Cohesion: 0.18
Nodes (17): Qualification-rule comparison operators (SPEC §7.4). Evaluated…, RuleOperator, ExtractionResponse, BaseModel, Qualification Node (Task 15). Extracts rule fields using the LLM and runs…, Structured output expected from the LLM when extracting fields., _coerce_values(), evaluate_rule() (+9 more)

### Community 57 - "test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment"
Cohesion: 0.19
Nodes (10): payments(), Any, get, Any, MonkeyPatch, test_absent_link_does_not_clear_uncertainty_or_authorize_retry(), test_known_configuration_failure_can_only_requeue_same_bounded_invoice(), test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment() (+2 more)

### Community 58 - "copilot.py"
Cohesion: 0.13
Nodes (24): load_memory(), event_text(), AsyncSession, content(), decide(), DraftContent, DraftDecision, DraftRequest (+16 more)

### Community 59 - "ADR-010: Triage Fallback Routing (Anti-Spam)"
Cohesion: 0.33
Nodes (5): ADR-010: Triage Fallback Routing (Anti-Spam), Consequences, Context, Decision, Status

### Community 60 - "ADR-012: Telegram and OpenAI for the first complete admissions MVP"
Cohesion: 0.29
Nodes (7): ADR-012: Telegram and OpenAI for the first complete admissions MVP, Consequences, Context, Decision, Implemented runtime boundaries, References and verification, Supersession and preserved decisions

### Community 61 - "prepare"
Cohesion: 0.15
Nodes (16): inbound(), prepare(), Any, MonkeyPatch, parametrize, UUID, test_clear_escalation_records_request_outside_hours_without_a_model(), exercise() (+8 more)

### Community 62 - "2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md"
Cohesion: 0.25
Nodes (4): Architecture Decisions, Implementation Plan: AdmitFlow, Overview, Risks and Mitigations

### Community 63 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 64 - "auth.py"
Cohesion: 0.14
Nodes (28): change_password(), hash_password(), issue_session(), Login, logout(), me(), PasswordChange, AsyncSession (+20 more)

### Community 65 - "send"
Cohesion: 0.15
Nodes (12): test_ambiguous_context_asks_without_search_or_fact_mutation(), exercise(), send(), Any, MonkeyPatch, test_multilingual_quote_selection_uses_translated_question(), exercise(), test_provider_outage_refusal_and_bad_schema_preserve_facts_and_allow_handoff() (+4 more)

### Community 66 - "test_knowledge_workspace.py"
Cohesion: 0.12
Nodes (32): asyncio, ConversationEvent, ConversationReply, OutboundMessage, Bounded chronological transcript across inbound, replies and standalone…, Institution document extraction, durable ingestion and retrieval., Strict private-chat normalization and token-safe Telegram HTTP transport., Telegram transport and tenant-scoped identity helpers. (+24 more)

### Community 67 - "api.py"
Cohesion: 0.18
Nodes (21): assign_scope(), documents(), get_upload(), Any, BaseModel, Db, delete, get (+13 more)

### Community 68 - "enums.py"
Cohesion: 0.11
Nodes (21): DiscountType, Enumerated types used across the schema. These are Python ``str`` enums mapped…, How a discount code reduces the fee., DiscountCode, A staff-defined discount the backend (never the LLM) applies to a fee., Code-owned application fees and authenticated Razorpay payment processing., fixture, workspace() (+13 more)

### Community 69 - "decide"
Cohesion: 0.12
Nodes (21): decide(), Any, Validate structured model output; refusal/malformed output is never a decision.…, apply_whatsapp_formatting(), check_output_safety(), _deterministic_check(), InputGuardrailResult, LLMGuardrailResponse (+13 more)

### Community 70 - "RazorpayClient"
Cohesion: 0.14
Nodes (19): Credentials, Bounded Razorpay requests; ambiguous link creation is never blindly retried., RazorpayClient, Integer monetary arithmetic and exact-byte webhook authentication., verify_webhook(), main(), run(), provision() (+11 more)

### Community 71 - "Official source snapshots"
Cohesion: 0.50
Nodes (4): Conflicts to confirm, October 23 planning refresh, Official source snapshots, Sources

### Community 72 - "discovery.py"
Cohesion: 0.18
Nodes (9): Sanitizer to prevent RAG poisoning. Blocks chunks that contain obvious prompt…, sanitize_chunks(), Discovery Node (Task 12). Presents available courses as WhatsApp interactive…, RAG Node (Task 14). Graph node that retrieves from the knowledge base and…, RuntimeError, WhatsApp message sending service (Task 6). Uses httpx2 to call the Meta Graph…, Raised when the Meta Cloud API returns an error response., WhatsAppAPIError (+1 more)

### Community 73 - "get_redis"
Cohesion: 0.17
Nodes (12): get_redis(), Redis, RuntimeError, Shared async Redis client for application code. Carry-over prerequisite #1: the…, Raised when Redis is needed but ``REDIS_URL`` is unset in settings., Return the process-wide async Redis client singleton. The client is created…, RedisNotConfiguredError, Tests for the shared async Redis client helper (carry-over prerequisite #1).… (+4 more)

### Community 74 - "get_sessionmaker"
Cohesion: 0.13
Nodes (22): async_sessionmaker, DatabaseNotConfiguredError, get_session(), get_sessionmaker(), AsyncSession, RuntimeError, Async engine and session factory. Built lazily from ``settings.database_url``…, Raised when a DB session is requested but ``DATABASE_URL`` is unset. (+14 more)

### Community 75 - "budget.py"
Cohesion: 0.16
Nodes (22): day_window(), local_counts(), Any, datetime, UUID, Atomic daily send-attempt budgets shared by every Telegram delivery path., Count confirmed deliveries once; a stats failure must not repeat a sent message., record_sent() (+14 more)

### Community 76 - "management.tsx"
Cohesion: 0.10
Nodes (13): blank, Discount, Discounts(), Batch, Course, empty, Management(), operators (+5 more)

### Community 77 - "security.py"
Cohesion: 0.19
Nodes (11): encrypt_bytes(), _fernet(), Application-layer PII protection: symmetric encryption + deterministic hashing.…, Encrypt uploaded source bytes before persistence, without lossy text decoding., Application settings singleton. Loads configuration from the environment (and…, UUID, Private Telegram identity lookup without storing raw identifiers in indexes., Exercise Telegram tenant/identity constraints and safe migration rollback. (+3 more)

### Community 78 - "TelegramBot"
Cohesion: 0.21
Nodes (15): Trusted bot-to-institution mapping; token is application-encrypted., TelegramBot, action(), application_action(), collect_application(), prompt(), Any, AsyncSession (+7 more)

### Community 79 - "dispatcher.py"
Cohesion: 0.15
Nodes (18): MessageDirection, Direction of a WhatsApp message row (episodic memory, ADR-004)., _flush_engine_state(), handle_turn(), _load_engine_state(), Any, AsyncSession, Engine Dispatcher (Task 8 & 17). This module contains the main entry point for… (+10 more)

### Community 84 - "analytics.tsx"
Cohesion: 0.28
Nodes (7): Analytics(), Conversion, labels, frontend_app_analytics_module, rate(), Report, shortDate()

### Community 89 - "accounts.py"
Cohesion: 0.19
Nodes (21): admin_scope(), create_user(), CreateUser, edit_user(), EditUser, Any, BaseModel, Db (+13 more)

### Community 90 - "AdmitFlow"
Cohesion: 0.33
Nodes (6): AdmitFlow, Current status, Demonstration and submission, Development, Product scope, Stack

### Community 91 - "ExtractionError"
Cohesion: 0.11
Nodes (28): blocks(), Markdown sections and table rows stay together within bounded evidence chunks., Keep section ancestry; repeat table headers instead of breaking row…, semantic_chunks(), table_parts(), table_start(), text_parts(), ExtractionError (+20 more)

### Community 92 - "PaymentProviderError"
Cohesion: 0.19
Nodes (12): PaymentLink, PaymentProviderError, BaseModel, Exception, field_validator, Read an existing exact reference; absence never authorizes another creation., Any, MonkeyPatch (+4 more)

### Community 93 - "json"
Cohesion: 0.13
Nodes (27): DocumentChunk, A chunk of a document, with its embedding for vector search., PassageRanking, BaseModel, UUID, Bounded OpenAI evidence reranking with a validated baseline fallback., Reorder only original, safe tenant candidates; never invent text or sources.…, rerank() (+19 more)

### Community 94 - "hash_phone"
Cohesion: 0.10
Nodes (21): EncryptionKeyNotConfiguredError, hash_phone(), RuntimeError, Raised when a PII helper is used but its key is unset in settings., Return a deterministic keyed hash of a phone number for lookup/dedup. Keyed…, crm_data(), seed(), fixture (+13 more)

### Community 95 - "identity_database"
Cohesion: 0.38
Nodes (7): identity_database(), fixture, Use a disposable pgvector database; never mutate the demo database., test_downgrade_preserves_legacy_rows_and_refuses_to_destroy_telegram_data(), inspect_and_clean(), remove_test_bot(), verify_legacy()

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

### Community 102 - "test_failure_retry_and_delete_during_indexing"
Cohesion: 0.17
Nodes (10): Any, MonkeyPatch, test_duplicate_claim_and_abandoned_attempt_recovery(), claims(), paused(), recover(), test_expired_session_rejected(), expire() (+2 more)

### Community 103 - "next-env.d.ts"
Cohesion: 0.50
Nodes (3): NOTE: This file should not be edited, frontend_next_types_root_params_d, frontend_next_types_routes_d

### Community 104 - "payments/webhook.py"
Cohesion: 0.19
Nodes (14): LinkEntity, LinkEnvelope, PaidEvent, PaidPayload, payment_webhook(), PaymentEntity, PaymentEnvelope, BaseModel (+6 more)

### Community 105 - "reindex_names.py"
Cohesion: 0.36
Nodes (7): main(), AsyncSession, UUID, Backfill encrypted lead names from latest submitted forms and rebuild blind…, reindex_batch(), test_index_rename_clear_and_legacy_backfill(), exercise()

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

### Community 111 - "TestWhatsAppSender"
Cohesion: 0.15
Nodes (10): asyncio, fixture, Successfully sending a template message., API errors (non-200) raise WhatsAppAPIError., Fails loud if access token or phone ID are missing., WhatsApp sender operations., Successfully sending a text message., Successfully sending an interactive buttons message. (+2 more)

### Community 112 - "TelegramClient"
Cohesion: 0.15
Nodes (15): Any, RuntimeError, TelegramAPIError, TelegramClient, Any, MonkeyPatch, test_outbound_dedup_claims_order_and_uncertainty(), deliver() (+7 more)

### Community 113 - "models/__init__.py"
Cohesion: 0.08
Nodes (62): Audit-log write helper. :func:`write_audit_log` is the one path significant…, Base, IdMixin, Declarative base, metadata naming convention, and shared column mixins. Every…, Declarative base shared by every AdmitFlow model., UUID primary key with an application-side default. UUIDs avoid cross-tenant…, Server-side created/updated timestamps., Row-level tenant scoping (ADR-003). Mixed into every tenant-scoped table. (+54 more)

### Community 114 - "Quality Gates — Definition of Done"
Cohesion: 0.33
Nodes (6): CI mirrors this exactly, Fast iteration vs the gate, Quality Gates — Definition of Done, The baseline gate (every change), The enforced-numbers ledger, The tiers — add gates by what the change touches

### Community 115 - "telegram/service.py"
Cohesion: 0.25
Nodes (13): process_telegram_event(), task, Telegram inbox and outbox jobs contain only internal identifiers., send_telegram_reply(), accept_update(), process_event(), Any, UUID (+5 more)

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
Cohesion: 0.15
Nodes (14): dispatch_pending(), recovery_loop(), dispatch_due(), Local operational commands with secrets entered through protected prompts., main(), Produce due reminder jobs and recover queued deliveries; safe to run after…, run(), purge_retained() (+6 more)

### Community 120 - "Settings"
Cohesion: 0.13
Nodes (18): Environment-backed application configuration., Settings, Tests use explicit configuration and never implicitly load developer…, configured_keys(), fixture, MonkeyPatch, Point ``security.get_settings`` at settings with the crypto keys set., Point ``security.get_settings`` at settings with no crypto keys. (+10 more)

### Community 121 - "test_rag_node.py"
Cohesion: 0.23
Nodes (11): process_rag_node(), AsyncSession, Retrieve context and answer knowledge questions., mock_state(), asyncio, fixture, patch, Unit tests for the RAG node. (+3 more)

### Community 122 - "broker.py"
Cohesion: 0.24
Nodes (8): TaskIQ broker singleton. In production (and local dev with Redis running) the…, task, Encrypted outbound-message delivery jobs carry only internal identifiers., send_outbound_message(), Payment-link creation runs after the requesting conversation transaction…, UUID, send_outbound(), taskiq

### Community 123 - "test_course_scope_authority_search_and_faq"
Cohesion: 0.13
Nodes (15): AmbiguousCourseReference, AsyncSession, Course, UUID, ValueError, question_courses(), More than one active course has the requested name without a selected owner., Explicit catalog names take precedence over selection; no model invents IDs. (+7 more)

### Community 124 - "WhatsApp readiness check — October 22, 2026"
Cohesion: 0.15
Nodes (13): Decision so far, Delivery diagnosis and configuration repair (October 23, approximately 00:16 IST), Evidence collected before configuration, Final Postman retry (October 23), Live checkpoint (approximately 22:54 IST), Missing-reply investigation (approximately 22:59 IST), New test account configuration (October 23, approximately 09:45 IST), Next live checks and evidence required (+5 more)

### Community 125 - "Reply"
Cohesion: 0.18
Nodes (19): GroundingSource, BaseModel, Channel-neutral input and validated plain-text reply boundary., Internal evidence persisted in encrypted replies, excluded from channel…, Reply, Case, cases(), evaluate() (+11 more)

### Community 126 - "live"
Cohesion: 0.22
Nodes (11): current(), live(), Any, AsyncSession, Db, get, post, Response (+3 more)

### Community 127 - "alembic"
Cohesion: 0.05
Nodes (10): alembic, columns(), Column, upgrade(), common(), Column, upgrade(), collections_abc (+2 more)

### Community 128 - "payments.tsx"
Cohesion: 0.32
Nodes (6): label(), money(), outcomes, Payment, Payments(), statuses

### Community 129 - "office_open"
Cohesion: 0.24
Nodes (8): office_open(), datetime, Deterministic clear support signals and institution-local office hours., parametrize, Clear support signals escalate; office hours never promise an immediate reply., test_clear_escalation_signals(), test_office_hours_use_institution_timezone_and_end_exclusive(), src_engine_escalation

### Community 130 - "StaffAccounts"
Cohesion: 1.00
Nodes (3): StaffAccounts(), create(), mutate()

### Community 131 - "Knowledge"
Cohesion: 0.44
Nodes (9): refresh(), api(), Knowledge(), action(), assignScope(), login(), search(), upload() (+1 more)

### Community 132 - "test_local_runtime.py"
Cohesion: 0.19
Nodes (12): configure(), main(), Path, Create private isolated local Compose configuration without copying live…, asyncio, MonkeyPatch, Path, Local bootstrap preserves secrets and legacy ingress stays explicitly opt-in. (+4 more)

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

### Community 140 - "validate_services.py"
Cohesion: 0.32
Nodes (7): embed_chunks(), Use the configured OpenAI model with the database's explicit 1536 dimensions., main(), Probe, BaseModel, Bounded live checks; print sanitized results without credentials or update…, validate()

### Community 141 - "test_worker_broker.py"
Cohesion: 0.25
Nodes (7): Tests for the TaskIQ broker setup and task execution (Task 3). All tests run…, When REDIS_URL is unset the factory should yield an InMemoryBroker., The ping task should run and return the expected payload., Ping without an explicit payload should default to 'pong'., test_broker_is_in_memory_without_redis_url(), test_ping_task_default_payload(), test_ping_task_returns_result()

### Community 142 - "verify_compose.py"
Cohesion: 0.17
Nodes (13): argparse, compose(), Verify the isolated local Compose stack without external API calls or sends., seed_credentials(), verify(), main(), prepare(), Path (+5 more)

### Community 143 - "hashlib"
Cohesion: 0.11
Nodes (18): Expose only the existing Meta webhook through the temporary demo tunnel., Hash the tested code/configuration without reading secrets or runtime data., parametrize, The temporary tunnel must not expose local debug or documentation routes., test_delivery_status_logs_are_authenticated_and_exclude_pii(), test_tunnel_app_exposes_no_other_routes(), test_tunnel_app_keeps_webhook_verification(), app() (+10 more)

### Community 144 - "retrieval.py"
Cohesion: 0.38
Nodes (6): numeric_values(), BaseModel, Bounded query resolution for approved evidence; never turn queries into facts., ResolvedQuestion, RetrievalQuery, Decimal

### Community 145 - "test_handle_turn_basic_flow"
Cohesion: 0.29
Nodes (6): Any, asyncio, fixture, patch, sample_whatsapp_payload(), test_handle_turn_basic_flow()

### Community 147 - "notifications.tsx"
Cohesion: 0.33
Nodes (4): labels, Notice, Notifications(), Snapshot

### Community 148 - "types"
Cohesion: 0.40
Nodes (4): Redis distributed mutex with owner-safe release and keepalive (Task 7). Ensures…, Actual Redis Lua reservations must remain bounded under concurrent workers., redis_asyncio, types

### Community 149 - "Phase 3: AI Core (Engine + RAG)"
Cohesion: 0.20
Nodes (10): Phase 3: AI Core (Engine + RAG), Task 10: Input guardrail node, Task 11: Triage node (intent detection), Task 12: Discovery node, Task 13: RAG pipeline, Task 14: RAG node, Task 15: Qualification node, Task 16: Output guardrail (+2 more)

### Community 150 - "test_workspace_limits.py"
Cohesion: 0.09
Nodes (19): ASGIApp, Reject oversized multipart streams before they can fill temporary storage., UploadBodyLimit, private_send(), check_login_limit(), Request, MonkeyPatch, Bound resource use and reject browser cross-origin mutations before database… (+11 more)

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

### Community 155 - "pydantic"
Cohesion: 0.11
Nodes (25): Typed decisions through the existing OpenAI-only provider boundary., AllProvidersFailedError, generate_completion(), Any, Exception, Bounded OpenAI-only model roles; provider details never escape in errors., Raised when the entire LLM fallback chain is exhausted., Generate a completion with automatic provider fallback. Tries the fast model,… (+17 more)

### Community 156 - "test_existing_inquiries_upgrade_without_invented_consent"
Cohesion: 0.50
Nodes (3): test_existing_inquiries_upgrade_without_invented_consent(), in_flight(), old()

### Community 157 - "2. Boundaries & Invariants"
Cohesion: 0.50
Nodes (4): 2. Boundaries & Invariants, Always Do, Ask First, Never Do

### Community 160 - "8. RAG (Retrieval-Augmented Generation)"
Cohesion: 0.50
Nodes (4): 8.1 Per-Institution Knowledge Base, 8.2 Retrieval Pipeline, 8.3 RAG Guardrail, 8. RAG (Retrieval-Augmented Generation)

### Community 164 - "README.md"
Cohesion: 0.13
Nodes (13): AI Impact Statement, Data, model and asset provenance, Student-to-staff demonstration, Current templates, Language review packet, Live exercise, Reference clarification, Reminder consent and outreach copy (+5 more)

### Community 167 - "signin"
Cohesion: 0.11
Nodes (18): test_local_cohort_counts_conversions_and_observed_stages(), test_tenant_is_derived_from_session_and_period_is_bounded(), test_zero_filled_weekly_buckets_and_empty_rates(), test_downloads_roles_datasets_limits_and_tenants(), test_search_scope_validation_and_audit(), Any, Real database management: administrator writes, role/tenant boundaries and…, test_catalog_writes_validate_rules_capacity_and_ownership() (+10 more)

### Community 168 - "timeline"
Cohesion: 0.22
Nodes (8): Cursor, Any, AsyncSession, BaseModel, datetime, field_validator, UUID, timeline()

### Community 177 - "log_delivery_status"
Cohesion: 0.40
Nodes (5): log_delivery_status(), Request, Response, Observe only authenticated status events, without recipient or error text., middleware

### Community 178 - "index_known_name"
Cohesion: 0.40
Nodes (5): index_known_name(), Connection, Mapper, Keep index updates atomic with encrypted names, including name removal., listens_for

### Community 183 - "whatsapp/webhook.py"
Cohesion: 0.12
Nodes (17): ping(), process_inbound_message(), Any, task, Background tasks for message processing. For now this module holds only the…, Smoke-test task: returns ``{"result": payload}``. Enqueued from the…, Process an inbound WhatsApp message (Task 17). This is a placeholder for the…, get (+9 more)

### Community 184 - "3. Tech Stack & Commands"
Cohesion: 0.50
Nodes (4): 3. Tech Stack & Commands, Deployment, Hybrid Architecture, Key Commands

### Community 187 - "isolated_local_login_windows"
Cohesion: 0.67
Nodes (3): isolated_local_login_windows(), fixture, MonkeyPatch

## Knowledge Gaps
- **420 isolated node(s):** `admitflow-backend`, `fs`, `path`, `crypto`, `root` (+415 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1180 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CRM search and institution downloads` connect `write_audit_log` to `test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment`, `leads.py`, `backend/README.md`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Why does `write_audit_log()` connect `write_audit_log` to `leads.py`, `exports.py`, `journey.py`, `transport.py`, `payments/service.py`, `staff/payments.py`, `institution.py`, `Phase 5: Dashboard Frontend (Next.js)`, `management.py`, `outreach/followups.py`, `Lead`, `operations.py`, `knowledge/processing.py`, `test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment`, `copilot.py`, `auth.py`, `test_knowledge_workspace.py`, `api.py`, `RazorpayClient`, `get_sessionmaker`, `TelegramBot`, `accounts.py`, `payments/webhook.py`, `models/__init__.py`, `telegram/service.py`, `scheduler.py`, `broker.py`, `live`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Why does `LeadStatus` connect `LeadStatus` to `leads.py`, `exports.py`, `journey.py`, `write_audit_log`, `transport.py`, `encrypt_pii`, `payments/service.py`, `Course`, `institution.py`, `outreach/followups.py`, `Lead`, `operations.py`, `age`, `RuleOperator`, `send`, `test_knowledge_workspace.py`, `enums.py`, `discovery.py`, `get_sessionmaker`, `security.py`, `TelegramBot`, `dispatcher.py`, `hash_phone`, `payments/webhook.py`, `models/__init__.py`, `test_rag_node.py`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `encrypt_pii()` (e.g. with `Consequences` and `Decision`) actually correct?**
  _`encrypt_pii()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 54 inferred relationships involving `LeadStatus` (e.g. with `record_stage_changes()` and `Lead`) actually correct?**
  _`LeadStatus` has 54 INFERRED edges - model-reasoned connections that need verification._
- **What connects `admitflow-backend`, `fs`, `path` to the rest of the system?**
  _420 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `exports.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0512987012987013 - nodes in this community are weakly interconnected._