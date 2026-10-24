# Graph Report - admitflow  (2026-10-24)

## Corpus Check
- 329 files · ~180,989 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 7, .example 2, .css 2)

## Summary
- 2890 nodes · 8404 edges · 175 communities (155 shown, 20 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 529 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `aa902fbd`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AdmitFlow Complete Specification
- Conversation Engine (hand-rolled dispatcher)
- README.md
- Finalized Production Stack
- lead_statement
- analytics
- Code Owns the Money
- Reply
- RedisMutex
- write_audit_log
- pdf_parser.py
- test_integration_security.py
- WhatsAppSender
- core/rag.py
- PII Encryption & Audit Log
- Razorpay Payment Integration
- get_settings
- admissions.tsx
- contextual_query
- evaluate_guidance.py
- AIBoomi Startup Weekend Kochi: fresh-session context
- LeadStatus
- test_knowledge_workspace.py
- deliver
- RuleOperator
- Stages
- alembic
- TestClient
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
- guidance.py
- main.py
- route
- send_message
- Hackathon resources for AdmitFlow
- manifest.json
- knowledge/processing.py
- AdmitFlow: current state and planning baseline
- AdmitFlow: AIBoomi submission plan
- AdmitFlow — Complete Specification
- normalize_e164
- accounts.py
- ADR-011: Required OpenAI passage reranking
- Testing
- check_input_safety
- AdmitFlow project handoff
- detect_intent
- EncryptionKeyNotConfiguredError
- GuidanceMemory
- test_payment_contracts.py
- generate
- ADR-010: Triage Fallback Routing (Anti-Spam)
- ADR-012: Telegram and OpenAI for the first complete admissions MVP
- decrypt_pii
- 2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md
- compilerOptions
- change_password
- encrypt_pii
- test_privacy.py
- api.py
- test_structured_documents.py
- AllProvidersFailedError
- decide
- Official source snapshots
- handle_turn
- Document
- ._post
- budget.py
- management.tsx
- pathlib
- GuidanceDecision
- tests/test_conversation_readiness.py
- verify.sh
- db/__init__.py
- src/__init__.py
- tasks/__init__.py
- analytics.tsx
- whatsapp/__init__.py
- integration/__init__.py
- admitflow-backend
- fixture
- AdmitFlow
- ExtractionError
- BaseModel
- test_decision_reranking.py
- live
- guardrails.py
- Git & GitHub Workflow
- package.json
- 13. Dashboard Features
- @playwright/test
- AGENTS.md
- Security & Production Readiness
- signin
- next-env.d.ts
- security.py
- DocumentChunk
- layout.tsx
- frontend/AGENTS.md
- scripts
- backend/README.md
- AdmitFlow pitch deck
- payments/conversation.py
- test_telegram_journey.py
- models/__init__.py
- AGENTS.md
- TelegramAPIError
- devDependencies
- applications.tsx
- dependencies
- Phase 3: AI Core (Engine + RAG)
- Settings
- consent.py
- Detail
- Phase 1: Foundation
- WhatsApp readiness check — October 22, 2026
- test_faq_evaluation.py
- ManualMessage
- transport.py
- payments.tsx
- configure
- Adaptive course guidance: evidence and implementation
- Knowledge
- test_shared_budget_preserves_queues_and_settings_wake_deliveries
- env.py
- sender.py
- capture_event
- retrieval.py
- page.tsx
- AdmitFlow execution and demonstration checklist
- 20260929_initial_schema_64cfce85009d.py
- review
- identity_database
- verify_compose.py
- add_institution_knowledge_workspace_b627da2f7e11.py
- test_exports.py
- add_conversation_runtime_714f092da3b8.py
- durable_payments_outbound_f129a064c5e8.py
- notifications.tsx
- AdmitFlow — Task List
- index_known_name
- pytest
- 11. Human-in-the-Loop (Full Workflow)
- reindex_batch
- record-demo.mjs
- Local Telegram/OpenAI runtime
- 20261008_add_knowledge_models_for_rag_c470f1ebc811.py
- ADR-014: Natural collection, context reset and responsive replies
- 2. Boundaries & Invariants
- 8. RAG (Retrieval-Augmented Generation)
- Phase 3–4 addition (see ADR-008)
- Phase 4: Advanced Bot Features
- Language review packet
- ExtractionResponse
- Phase 6: Production Hardening
- timeline
- test_workspace_limits.py
- AdmitFlow submission requirements
- 10. Observability & Tracing
- 5. Code Style
- test_worker_broker.py
- DOCUMENT_REVIEW.md

## God Nodes (most connected - your core abstractions)
1. `encrypt_pii()` - 110 edges
2. `write_audit_log()` - 100 edges
3. `LeadStatus` - 100 edges
4. `Reply` - 98 edges
5. `get_settings()` - 93 edges
6. `Lead` - 90 edges
7. `decrypt_pii()` - 82 edges
8. `TelegramBot` - 80 edges
9. `route()` - 69 edges
10. `Course` - 67 edges

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

## Communities (175 total, 20 thin omitted)

### Community 0 - "AdmitFlow Complete Specification"
Cohesion: 0.20
Nodes (18): ADR-001: Hybrid Architecture, ADR-004: Dual Memory Architecture, Episodic Memory (messages table), Semantic Memory (lead_facts table), ADR-005: Three-Layer Guardrails and RAG, Three-Layer Guardrails, ADR-007: Finalized Production Stack, ADR-008: System-1 Decision Layer (Laya / Jev) (+10 more)

### Community 1 - "Conversation Engine (hand-rolled dispatcher)"
Cohesion: 0.25
Nodes (8): Conversation Engine (hand-rolled dispatcher), System-1 decide() Decision Layer, FastAPI WhatsApp Webhook, Langfuse LLM Tracing, pgvector RAG Pipeline, Redis (mutex / dedup / rate-limit), TaskIQ Background Worker, Three-Layer Guardrails

### Community 2 - "README.md"
Cohesion: 0.16
Nodes (11): AI Impact Statement, Data, model and asset provenance, Student-to-staff demonstration, Executed final check, One final WhatsApp check with Postman, Prior-work disclosure, AdmitFlow necessary resources, Planning baseline before Telegram alignment (+3 more)

### Community 3 - "Finalized Production Stack"
Cohesion: 0.18
Nodes (11): ADR-002: Webhook Concurrency and Deduplication, Per-Phone Redis Mutex, Webhook Deduplication (Redis SETNX), ADR-003: Multi-Tenancy Strategy, Multi-Tenancy (Row-Level Isolation), Finalized Production Stack, Fly.io (Backend + Worker + Scheduler), Langfuse Cloud (LLM Tracing) (+3 more)

### Community 4 - "lead_statement"
Cohesion: 0.20
Nodes (18): lead_statement(), lead_summary(), Any, Select, UUID, course_options(), get_lead(), human_requests() (+10 more)

### Community 5 - "analytics"
Cohesion: 0.06
Nodes (43): alias, Admissions analytics, AdmitFlow Backend, Application payments, Configuration, Consented follow-up reminders, Current implementation and verification, Institution knowledge workspace (+35 more)

### Community 6 - "Code Owns the Money"
Cohesion: 0.50
Nodes (5): ADR-006: Code-Owned Qualification and Payments, Intent: Admissions Flow and Discounts, Discount Codes, Code Owns Eligibility, Code Owns the Money

### Community 7 - "Reply"
Cohesion: 0.08
Nodes (65): Lead, A prospective applicant with optional phone contact and channel identities.…, Trusted bot-to-institution mapping; token is application-encrypted., TelegramBot, action(), application_action(), collect_application(), prompt() (+57 more)

### Community 8 - "RedisMutex"
Cohesion: 0.08
Nodes (25): MutexAcquireError, Redis, RuntimeError, Background loop that extends the TTL while the lock is held., Raised when the mutex cannot be acquired after all retries., Async context-manager mutex backed by Redis ``SET NX``. Parameters: redis: An…, Attempt to acquire the lock, retrying up to ``retry_count`` times., Release the lock using the Lua CAS script (owner-safe). (+17 more)

### Community 9 - "write_audit_log"
Cohesion: 0.17
Nodes (19): Any, AsyncSession, UUID, Record persisted ORM transitions atomically; never infer an earlier stage., Append one entry to ``audit_logs`` on ``session``; return it flushed, not…, record_stage_changes(), write_audit_log(), locked() (+11 more)

### Community 10 - "pdf_parser.py"
Cohesion: 0.13
Nodes (17): kill_descendants(), parse_pdf(), Offline PDF child process with per-loop backpressure, memory and time limits., Include Windows venv redirector children and any parser subprocesses., resident_memory(), watch_memory(), Process, parametrize (+9 more)

### Community 11 - "test_integration_security.py"
Cohesion: 0.20
Nodes (16): destination(), post_event(), public_ip(), resolve_public(), signature(), parametrize, Outbound integrations reject unsafe destinations and sign exact delivery bytes., test_internal_and_nonpublic_addresses_are_rejected() (+8 more)

### Community 12 - "WhatsAppSender"
Cohesion: 0.16
Nodes (11): Service for sending messages via Meta WhatsApp Cloud API., WhatsAppSender, asyncio, Successfully sending a template message., API errors (non-200) raise WhatsAppAPIError., Fails loud if access token or phone ID are missing., WhatsApp sender operations., Successfully sending a text message. (+3 more)

### Community 13 - "core/rag.py"
Cohesion: 0.13
Nodes (21): chunk_text(), embed_text(), ingest_document(), Any, AsyncSession, UUID, RAG pipeline core logic (Task 13). Handles ingestion (chunking, embedding),…, Sanitizer to prevent RAG poisoning. Blocks chunks that contain obvious prompt… (+13 more)

### Community 16 - "get_settings"
Cohesion: 0.10
Nodes (26): AsyncBroker, get_settings(), Application settings singleton. Loads configuration from the environment (and…, Return the process-wide :class:`Settings` singleton., embed_chunks(), Use the configured OpenAI model with the database's explicit 1536 dimensions., main(), Probe (+18 more)

### Community 17 - "admissions.tsx"
Cohesion: 0.10
Nodes (19): Admissions(), Detail, Human, Inquiry, labels, Request, RuleEvidence, statusLabel() (+11 more)

### Community 18 - "contextual_query"
Cohesion: 0.13
Nodes (17): contextual_query(), Resolve pronouns/slang using bounded recent turns; uncertainty asks the…, retrieval_query(), evaluate(), main(), Bounded synthetic OpenAI reference resolution; no database writes or sends., MonkeyPatch, parametrize (+9 more)

### Community 19 - "evaluate_guidance.py"
Cohesion: 0.21
Nodes (12): question_field(), Bind short numerical answers only to a visibly asked academic question., evaluate(), evaluate_dialogues(), main(), Any, Bounded synthetic live course-guidance scenarios; no database writes or sends., Exercise persistent state, not just independent single-message answers. (+4 more)

### Community 20 - "AIBoomi Startup Weekend Kochi: fresh-session context"
Cohesion: 0.11
Nodes (19): AIBoomi Startup Weekend Kochi: fresh-session context, Assessment and next decision, Current readiness session (October 22), Event sources and local copies, Existing prototype rule and surprise element, Existing working-tree changes, Fresh-message prompt, Handoff status (+11 more)

### Community 21 - "LeadStatus"
Cohesion: 0.06
Nodes (63): asyncio, ApplicationStatus, DiscountType, LeadStatus, PaymentStatus, Enumerated types used across the schema. These are Python ``str`` enums mapped…, Lead lifecycle states (SPEC §7.3). Where a lead *stands*, not a fixed track —…, How a discount code reduces the fee. (+55 more)

### Community 22 - "test_knowledge_workspace.py"
Cohesion: 0.05
Nodes (67): alembic_config, async_sessionmaker, AsyncEngine, Dashboard access role (SPEC — admin vs agent)., StaffRole, Institution, Institution (the tenant root) and its staff users., An institution, optionally connected to a legacy WhatsApp number. The tenant… (+59 more)

### Community 23 - "deliver"
Cohesion: 0.11
Nodes (16): deliver(), UUID, task, Integration queue messages contain identifiers only., send_webhook(), configure(), event_for(), test_delivery_claim_retry_and_minimal_payload() (+8 more)

### Community 24 - "RuleOperator"
Cohesion: 0.06
Nodes (54): Qualification-rule comparison operators (SPEC §7.4). Evaluated…, RuleOperator, _flush_engine_state(), AsyncSession, Flush mutations back to DB records., AsyncSession, Run the qualification loop., run_qualification() (+46 more)

### Community 25 - "Stages"
Cohesion: 0.13
Nodes (15): 10. Reflect & learn, 1. Understand & spec  (`/spec`), 2. Plan & pick a task  (`/plan`), 3. Branch, 4. Build with TDD  (`/build`, `/test`), 5. Verify (the quality gate), 6. Self-review, then adversarial review  (`/review`), 7. Commit & open the PR (+7 more)

### Community 27 - "TestClient"
Cohesion: 0.16
Nodes (8): Any, TestClient, Statuses (read/delivered) have no 'messages' array., GET /api/webhook challenge verification., POST /api/webhook payload processing., sign_payload(), TestWebhookProcessing, TestWebhookVerification

### Community 28 - "run_postman_check.cjs"
Cohesion: 0.20
Nodes (8): collection, config, crypto, fs, keys, newman, path, root

### Community 29 - "Task List"
Cohesion: 0.15
Nodes (13): Checkpoint: Advanced Features, Checkpoint: AI Core, Checkpoint: Dashboard Complete, Checkpoint: Foundation, Checkpoint: Production Ready, Checkpoint: WhatsApp Ingress, Phase 1: Foundation, Phase 2: WhatsApp Ingress (+5 more)

### Community 30 - "payments/webhook.py"
Cohesion: 0.19
Nodes (14): LinkEntity, LinkEnvelope, PaidEvent, PaidPayload, payment_webhook(), PaymentEntity, PaymentEnvelope, BaseModel (+6 more)

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
Cohesion: 0.05
Nodes (58): escalation_reason(), office_open(), datetime, Reason, Deterministic clear support signals and institution-local office hours., dispatch_pending(), recovery_loop(), activity() (+50 more)

### Community 36 - "Event preparation and execution plan"
Cohesion: 0.18
Nodes (11): Business and mentor preparation, Evaluation and demo evidence, Event preparation and execution plan, Kickoff disclosure draft, Latest direction (October 23), Minimum demonstrable product, Next action: one-hour v1 readiness check, Submission checklist (+3 more)

### Community 37 - "7. Core Feature Specifications"
Cohesion: 0.18
Nodes (11): 7.10 Payment Integration & Discounts (Razorpay), 7.1 WhatsApp Number Architecture, 7.2 Multi-Tenancy (Row-Level Isolation), 7.3 Lead Lifecycle States, 7.4 Course Qualification Rules (Structured), 7.5 Batch & Intake Management, 7.6 Cold Lead Re-engagement, 7.7 Language Support (+3 more)

### Community 38 - "guidance.py"
Cohesion: 0.21
Nodes (22): QualificationRule, A structured eligibility rule evaluated in code, not by the LLM (ADR-006).…, catalog(), catalog_status(), checked_text(), commit_guidance(), guide(), interpret_turn() (+14 more)

### Community 39 - "main.py"
Cohesion: 0.08
Nodes (23): log_delivery_status(), Request, Response, Expose only the existing Meta webhook through the temporary demo tunnel., Observe only authenticated status events, without recipient or error text., recovery_loop(), create_app(), lifespan() (+15 more)

### Community 40 - "route"
Cohesion: 0.09
Nodes (53): Event, GuidanceInterpretation, advance_application(), A confirmed choice may start a draft; submission remains explicitly confirmed., route(), submitted_reply(), callback_data(), Adaptive Telegram guidance persists safely through the real encrypted inbox. (+45 more)

### Community 41 - "send_message"
Cohesion: 0.36
Nodes (10): active_request(), Any, AsyncSession, Db, post, UUID, require_takeover(), resume() (+2 more)

### Community 42 - "Hackathon resources for AdmitFlow"
Cohesion: 0.20
Nodes (10): Acceptance before using a resource, Event and release boundaries, Goal, Hackathon resources for AdmitFlow, October 23 Downloads guide: hosted inference access, Participant credits and other support, Suggested allocation and activation order, Useful resources mapped to the plan (+2 more)

### Community 43 - "manifest.json"
Cohesion: 0.20
Nodes (9): SPEC.md, bytes, sha256, tasks/plan.md, bytes, sha256, tasks/todo.md, bytes (+1 more)

### Community 44 - "knowledge/processing.py"
Cohesion: 0.10
Nodes (20): decrypt_bytes(), Authenticate and decrypt source bytes for an authorized ingestion task., Bounded OpenAI-only model roles; provider details never escape in errors., process_upload(), UUID, Durable upload claims, bounded embedding and atomic publication of ready…, Claim once, process outside the transaction, then publish only the current…, ingest_upload() (+12 more)

### Community 45 - "AdmitFlow: current state and planning baseline"
Cohesion: 0.22
Nodes (9): AdmitFlow: current state and planning baseline, Confirmed user direction, Feature status and integration gaps, Features to finalize next, How to reconcile the planning documents, Proposed architecture for the next plan, Stack inventory, Verification evidence and its limits (+1 more)

### Community 46 - "AdmitFlow: AIBoomi submission plan"
Cohesion: 0.22
Nodes (9): AdmitFlow: AIBoomi submission plan, Deck and presentation, Open decisions, Proposed schedule from Friday evening, Submission outcome, The journey to demonstrate, Use the provided resources, What must be handed in (+1 more)

### Community 47 - "AdmitFlow — Complete Specification"
Cohesion: 0.12
Nodes (16): 12. Edge Cases & Error Handling, 14. Data Privacy (DPDPA-Ready), 15. Memory Architecture, 16. Success Criteria, 17.1 Conversation engine — DECIDED: hand-rolled dispatcher, 17.2 Still open, 17. Decisions & Open Questions, 1. Objective (+8 more)

### Community 48 - "normalize_e164"
Cohesion: 0.14
Nodes (10): InvalidPhoneError, normalize_e164(), ValueError, E.164 phone-number normalization. Carry-over prerequisite #3: un-normalized…, Raised when a phone string cannot be normalized to E.164., Normalize *raw* into canonical E.164 (``+<digits>``). Strips whitespace,…, Tests for E.164 phone normalization (carry-over prerequisite #3). The…, normalize_e164 → canonical E.164 string. (+2 more)

### Community 49 - "accounts.py"
Cohesion: 0.15
Nodes (24): admin_scope(), create_user(), CreateUser, edit_user(), EditUser, Any, BaseModel, Db (+16 more)

### Community 50 - "ADR-011: Required OpenAI passage reranking"
Cohesion: 0.40
Nodes (4): ADR-011: Required OpenAI passage reranking, Decision, Separate retrieval work, Verification and tradeoffs

### Community 51 - "Testing"
Cohesion: 0.22
Nodes (9): Browser announcement regions, Coverage, LLM and decision-layer tests, Philosophy — pragmatic TDD, Running tests, Test layout, Testing, The two patterns (+1 more)

### Community 52 - "check_input_safety"
Cohesion: 0.14
Nodes (22): apply_whatsapp_formatting(), check_input_safety(), check_output_safety(), Convert common markdown formatting to WhatsApp formatting., Check if the AI output is safe to send to the user. 1. Applies WhatsApp…, Check if the user input is safe to process. 1. Deterministic checks…, asyncio, Test output guardrail with safe content. (+14 more)

### Community 53 - "AdmitFlow project handoff"
Cohesion: 0.22
Nodes (9): AdmitFlow project handoff, Current conversation work: Task 61, Current direction, Development rules, Event submission, Execution checkpoint, First usable release, Historical evidence (+1 more)

### Community 54 - "detect_intent"
Cohesion: 0.20
Nodes (15): detect_intent(), Classify the user's intent to route to the correct node. Design Decision: If a…, asyncio, Test routing for course discovery., Test routing for knowledge questions., Test routing for qualification answers., Test routing for human handoff., Test routing for empty messages without calling LLM defaults to discovery. (+7 more)

### Community 55 - "EncryptionKeyNotConfiguredError"
Cohesion: 0.07
Nodes (29): EncryptionKeyNotConfiguredError, _fernet(), RuntimeError, Raised when a PII helper is used but its key is unset in settings., DatabaseNotConfiguredError, RuntimeError, Raised when a DB session is requested but ``DATABASE_URL`` is unset., hash_telegram_identifier() (+21 more)

### Community 56 - "GuidanceMemory"
Cohesion: 0.26
Nodes (25): GuidanceMemory, Note, ProfileUpdate, render_decision(), exercise(), exercise(), course(), decision() (+17 more)

### Community 57 - "test_payment_contracts.py"
Cohesion: 0.05
Nodes (38): AsyncBaseTransport, PaymentLink, PaymentProviderError, BaseModel, Exception, field_validator, Read an existing exact reference; absence never authorizes another creation., discounted_amount() (+30 more)

### Community 58 - "generate"
Cohesion: 0.19
Nodes (13): decide(), DraftContent, DraftDecision, DraftRequest, generate(), latest(), Any, AsyncSession (+5 more)

### Community 59 - "ADR-010: Triage Fallback Routing (Anti-Spam)"
Cohesion: 0.33
Nodes (5): ADR-010: Triage Fallback Routing (Anti-Spam), Consequences, Context, Decision, Status

### Community 60 - "ADR-012: Telegram and OpenAI for the first complete admissions MVP"
Cohesion: 0.29
Nodes (7): ADR-012: Telegram and OpenAI for the first complete admissions MVP, Consequences, Context, Decision, Implemented runtime boundaries, References and verification, Supersession and preserved decisions

### Community 61 - "decrypt_pii"
Cohesion: 0.13
Nodes (20): decrypt_pii(), Decrypt a token produced by :func:`encrypt_pii`. Raises…, test_configuration_roles_encryption_and_tenant_ownership(), inspect(), Any, MonkeyPatch, parametrize, test_clear_escalation_records_request_outside_hours_without_a_model() (+12 more)

### Community 62 - "2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md"
Cohesion: 0.25
Nodes (4): Architecture Decisions, Implementation Plan: AdmitFlow, Overview, Risks and Mitigations

### Community 63 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 64 - "change_password"
Cohesion: 0.17
Nodes (18): change_password(), issue_session(), Login, logout(), me(), PasswordChange, AsyncSession, BaseModel (+10 more)

### Community 65 - "encrypt_pii"
Cohesion: 0.10
Nodes (21): encrypt_pii(), Encrypt a PII string, returning a url-safe base64 Fernet token. Fernet is…, seed(), test_all_aggregates_share_a_snapshot_during_concurrent_arrivals(), interleave(), Any, Encrypted explicit application collection, replay safety and tenant-scoped…, test_application_collection_is_explicit_encrypted_and_replay_safe() (+13 more)

### Community 66 - "test_privacy.py"
Cohesion: 0.09
Nodes (20): MessageDirection, Direction of a WhatsApp message row (episodic memory, ADR-004)., PaymentOrder, A Razorpay order for an application fee (SPEC §7.10). Amount is DB-sourced…, PaymentEvent, _load_engine_state(), Load EngineState from DB records., Durable, minimal institution events and signed outbound integrations. (+12 more)

### Community 67 - "api.py"
Cohesion: 0.13
Nodes (31): encrypt_bytes(), Encrypt uploaded source bytes before persistence, without lossy text decoding., assign_scope(), documents(), get_upload(), Any, BaseModel, Db (+23 more)

### Community 68 - "test_structured_documents.py"
Cohesion: 0.21
Nodes (13): blocks(), Markdown sections and table rows stay together within bounded evidence chunks., Keep section ancestry; repeat table headers instead of breaking row…, semantic_chunks(), table_parts(), table_start(), text_parts(), parametrize (+5 more)

### Community 69 - "AllProvidersFailedError"
Cohesion: 0.15
Nodes (20): AllProvidersFailedError, generate_completion(), Any, Exception, Raised when the entire LLM fallback chain is exhausted., Generate a completion with automatic provider fallback. Tries the fast model,…, exercise(), unavailable() (+12 more)

### Community 70 - "decide"
Cohesion: 0.12
Nodes (14): decide(), Any, Typed decisions through the existing OpenAI-only provider boundary., Validate structured model output; refusal/malformed output is never a decision.…, RAG Node (Task 14). Graph node that retrieves from the knowledge base and…, BaseModel, Triage Node (Task 11). Routes incoming messages to the appropriate downstream…, Structured output expected from the LLM triage classifier. (+6 more)

### Community 71 - "Official source snapshots"
Cohesion: 0.50
Nodes (4): Conflicts to confirm, October 23 planning refresh, Official source snapshots, Sources

### Community 72 - "handle_turn"
Cohesion: 0.08
Nodes (26): handle_turn(), Any, Process a single turn of conversation., ping(), process_inbound_message(), Any, task, Background tasks for message processing. For now this module holds only the… (+18 more)

### Community 73 - "Document"
Cohesion: 0.22
Nodes (15): Document, An uploaded document in the institution's knowledge base., extract_file(), Bounded extraction of institution reference documents; never execute uploads., validate_path(), parametrize, Untrusted institutional files must extract safely or fail explicitly., test_compressed_docx_bombs_are_rejected() (+7 more)

### Community 74 - "._post"
Cohesion: 0.17
Nodes (11): Any, Send an interactive list message. `sections` is a list of section dicts…, Send a pre-approved template message., Post the payload to Meta and extract the created message ID., Meta API expects the phone number without the leading '+'., Send a simple text message. Returns the Meta message ID., Send an interactive message with up to 3 buttons. `buttons` should be a list of…, Phase 2: WhatsApp Ingress (+3 more)

### Community 75 - "budget.py"
Cohesion: 0.08
Nodes (38): Redis distributed mutex with owner-safe release and keepalive (Task 7). Ensures…, get_redis(), Redis, RuntimeError, Shared async Redis client for application code. Carry-over prerequisite #1: the…, Raised when Redis is needed but ``REDIS_URL`` is unset in settings., Return the process-wide async Redis client singleton. The client is created…, RedisNotConfiguredError (+30 more)

### Community 76 - "management.tsx"
Cohesion: 0.09
Nodes (16): blank, Discount, Discounts(), Batch, Course, empty, Management(), operators (+8 more)

### Community 77 - "pathlib"
Cohesion: 0.12
Nodes (16): argparse, configure(), main(), Path, Create private isolated local Compose configuration without copying live…, main(), prepare(), Path (+8 more)

### Community 78 - "GuidanceDecision"
Cohesion: 0.24
Nodes (12): CourseMatch, GuidanceDecision, InterestTheme, BaseModel, Bounded exploratory guidance; evidence notes are not psychometric measurements., StrictModel, StudyFact, test_profile_and_facts_survive_encryption_without_selecting_a_course() (+4 more)

### Community 79 - "tests/test_conversation_readiness.py"
Cohesion: 0.19
Nodes (12): academic_number_supported(), literal_quote(), merge_evidence(), Recover a literal source span, tolerating capitalization and terminal…, An interest score, phone number or unrelated number is not an academic fact., typed_value(), Natural collection and typing are bounded independently of provider…, test_explicit_keyed_marks_are_not_reasked_when_model_omits_them() (+4 more)

### Community 84 - "analytics.tsx"
Cohesion: 0.28
Nodes (7): Analytics(), Conversion, labels, frontend_app_analytics_module, rate(), Report, shortDate()

### Community 89 - "fixture"
Cohesion: 0.10
Nodes (23): fixture(), Course, isolated_local_login_windows(), MonkeyPatch, event_dependencies(), _alembic_config(), monkeypatch_session(), pg_url() (+15 more)

### Community 90 - "AdmitFlow"
Cohesion: 0.29
Nodes (7): AdmitFlow, Current status, Demonstration and submission, Development, Product scope, Stack, Student-first course guidance

### Community 91 - "ExtractionError"
Cohesion: 0.21
Nodes (14): ExtractionError, ValueError, A safe, public error code rather than parser output containing document text., convert_pdf(), main(), preflight_pdf(), Path, Single-use PDF parser. Reads stdin; emits bounded JSON, never raw diagnostics. (+6 more)

### Community 92 - "BaseModel"
Cohesion: 0.23
Nodes (7): BatchInput, Hours, BaseModel, RuleInput, SettingsInput, model_validator, Self

### Community 93 - "test_decision_reranking.py"
Cohesion: 0.22
Nodes (17): Reorder only original, safe tenant candidates; never invent text or sources.…, rerank(), chunks(), Intent, asyncio, BaseModel, MonkeyPatch, parametrize (+9 more)

### Community 94 - "live"
Cohesion: 0.19
Nodes (13): Acknowledge, current(), live(), Any, AsyncSession, BaseModel, Db, get (+5 more)

### Community 95 - "guardrails.py"
Cohesion: 0.21
Nodes (12): _deterministic_check(), InputGuardrailResult, LLMGuardrailResponse, LLMOutputGuardrailResponse, OutputGuardrailResult, BaseModel, Input Guardrail Node (Task 10). Detects prompt injection, profanity, and abuse…, Result of the input guardrail check. (+4 more)

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

### Community 102 - "signin"
Cohesion: 0.07
Nodes (31): test_local_cohort_counts_conversions_and_observed_stages(), test_tenant_is_derived_from_session_and_period_is_bounded(), test_zero_filled_weekly_buckets_and_empty_rates(), test_downloads_roles_datasets_limits_and_tenants(), test_search_scope_validation_and_audit(), Any, Real database management: administrator writes, role/tenant boundaries and…, test_catalog_writes_validate_rules_capacity_and_ownership() (+23 more)

### Community 103 - "next-env.d.ts"
Cohesion: 0.50
Nodes (3): NOTE: This file should not be edited, frontend_next_types_root_params_d, frontend_next_types_routes_d

### Community 104 - "security.py"
Cohesion: 0.08
Nodes (43): Application-layer PII protection: symmetric encryption + deterministic hashing.…, Audit-log write helper. :func:`write_audit_log` is the one path significant…, Bounded chronological transcript across inbound, replies and standalone…, event_text(), AsyncSession, Synthetic collection latency evidence; no database writes or Telegram…, Opaque database-backed staff sessions; no client-provided tenant authority., Custom header + strict cookies prevent cross-origin simple-request CSRF. (+35 more)

### Community 105 - "DocumentChunk"
Cohesion: 0.24
Nodes (9): DocumentChunk, A chunk of a document, with its embedding for vector search., PassageRanking, BaseModel, UUID, Bounded OpenAI evidence reranking with a validated baseline fallback., evaluate(), main() (+1 more)

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

### Community 111 - "payments/conversation.py"
Cohesion: 0.29
Nodes (17): discount_action(), order_reply(), payment_action(), preview(), Any, AsyncSession, UUID, Code-owned fee previews and explicit, conversation-bound payment requests. (+9 more)

### Community 112 - "test_telegram_journey.py"
Cohesion: 0.06
Nodes (63): is_reset_event(), process_telegram_event(), task, send_telegram_reply(), Strict private-chat normalization and token-safe Telegram HTTP transport., TelegramClient, Telegram transport and tenant-scoped identity helpers., send_outbound() (+55 more)

### Community 113 - "models/__init__.py"
Cohesion: 0.09
Nodes (56): Base, IdMixin, Declarative base, metadata naming convention, and shared column mixins. Every…, Declarative base shared by every AdmitFlow model., UUID primary key with an application-side default. UUIDs avoid cross-tenant…, Server-side created/updated timestamps., Row-level tenant scoping (ADR-003). Mixed into every tenant-scoped table., TenantMixin (+48 more)

### Community 114 - "AGENTS.md"
Cohesion: 0.27
Nodes (6): CI mirrors this exactly, Fast iteration vs the gate, Quality Gates — Definition of Done, The baseline gate (every change), The enforced-numbers ledger, The tiers — add gates by what the change touches

### Community 115 - "TelegramAPIError"
Cohesion: 0.06
Nodes (39): recover_payments(), normalize_update(), protect_logs(), Any, LogRecord, RuntimeError, TaskIQ changes log levels; redact before either HTTP client or root handlers…, Ephemeral feedback never delays, retries or fails the durable conversation. (+31 more)

### Community 116 - "devDependencies"
Cohesion: 0.33
Nodes (6): devDependencies, @playwright/test, @types/node, @types/react, @types/react-dom, typescript

### Community 117 - "applications.tsx"
Cohesion: 0.25
Nodes (5): Applications(), Detail, fields, statuses, Summary

### Community 118 - "dependencies"
Cohesion: 0.40
Nodes (5): dependencies, @fontsource-variable/dm-sans, next, react, react-dom

### Community 119 - "Phase 3: AI Core (Engine + RAG)"
Cohesion: 0.18
Nodes (11): Phase 3: AI Core (Engine + RAG), Task 10: Input guardrail node, Task 11: Triage node (intent detection), Task 12: Discovery node, Task 13: RAG pipeline, Task 14: RAG node, Task 15: Qualification node, Task 16: Output guardrail (+3 more)

### Community 120 - "Settings"
Cohesion: 0.11
Nodes (29): hash_phone(), Return a deterministic keyed hash of a phone number for lookup/dedup. Keyed…, Environment-backed application configuration., Settings, asyncio, MonkeyPatch, Local bootstrap preserves secrets and legacy ingress stays explicitly opt-in., test_legacy_webhook_is_absent_and_nondev_debug_is_disabled() (+21 more)

### Community 121 - "consent.py"
Cohesion: 0.24
Nodes (13): cancel_queued(), note_inbound(), preference_reply(), Any, AsyncSession, datetime, Student-owned reminder preferences apply even while staff has paused the bot., parse_callback() (+5 more)

### Community 122 - "Detail"
Cohesion: 0.25
Nodes (10): Detail, BaseModel, Only explicitly supplied application details may be reused in an encrypted…, validated_details(), ApplicationTurn, BaseModel, interpret(), parametrize (+2 more)

### Community 123 - "Phase 1: Foundation"
Cohesion: 0.40
Nodes (5): Phase 1: Foundation, Task 1: Initialize Python project, FastAPI, settings, and Docker, Task 2: PostgreSQL schema (SQLAlchemy + Alembic), Task 3: TaskIQ + Redis broker setup, Task 4: PII encryption utilities and audit log infrastructure

### Community 124 - "WhatsApp readiness check — October 22, 2026"
Cohesion: 0.15
Nodes (13): Decision so far, Delivery diagnosis and configuration repair (October 23, approximately 00:16 IST), Evidence collected before configuration, Final Postman retry (October 23), Live checkpoint (approximately 22:54 IST), Missing-reply investigation (approximately 22:59 IST), New test account configuration (October 23, approximately 09:45 IST), Next live checks and evidence required (+5 more)

### Community 125 - "test_faq_evaluation.py"
Cohesion: 0.26
Nodes (11): GroundingSource, BaseModel, Channel-neutral input and validated plain-text reply boundary., Internal evidence persisted in encrypted replies, excluded from channel…, Case, BaseModel, score_answer(), Scoring checks internal evidence, plain answers and language-specific… (+3 more)

### Community 126 - "ManualMessage"
Cohesion: 0.50
Nodes (3): ManualMessage, BaseModel, field_validator

### Community 127 - "transport.py"
Cohesion: 0.25
Nodes (7): PrivateTransportLogs, protect_logs(), LogRecord, HTTPS delivery pins a public resolved address while retaining TLS host…, contextvars, ipaddress, socket

### Community 128 - "payments.tsx"
Cohesion: 0.32
Nodes (6): label(), money(), outcomes, Payment, Payments(), statuses

### Community 129 - "configure"
Cohesion: 0.28
Nodes (9): configuration(), configure(), EndpointInput, Any, BaseModel, Db, get, put (+1 more)

### Community 130 - "Adaptive course guidance: evidence and implementation"
Cohesion: 0.18
Nodes (9): ADR-013: Adaptive, student-first course guidance, Consequences, Context, Decision, Adaptive course guidance: evidence and implementation, Asking useful questions, Boundaries and verification, Primary-source research and limits (+1 more)

### Community 131 - "Knowledge"
Cohesion: 0.44
Nodes (9): refresh(), api(), Knowledge(), action(), assignScope(), login(), search(), upload() (+1 more)

### Community 133 - "env.py"
Cohesion: 0.22
Nodes (9): do_run_migrations(), Connection, Alembic migration environment (async). Reads the database URL from application…, Emit SQL to stdout without a live DB connection., Run migrations against a live database via an async engine., run_migrations_offline(), run_migrations_online(), logging_config (+1 more)

### Community 134 - "sender.py"
Cohesion: 0.16
Nodes (8): Bounded synthetic PDF upload/queue/OpenAI/search check; removes its own upload., Five bounded live embedding searches through the real authenticated staff API., RuntimeError, WhatsApp message sending service (Task 6). Uses httpx2 to call the Meta Graph…, Raised when the Meta Cloud API returns an error response., WhatsAppAPIError, Tests for the WhatsApp Message Sending Service (Task 6). The sender calls the…, httpx2

### Community 135 - "capture_event"
Cohesion: 0.67
Nodes (3): capture_event(), Connection, Mapper

### Community 136 - "retrieval.py"
Cohesion: 0.32
Nodes (7): numeric_values(), BaseModel, Bounded query resolution for approved evidence; never turn queries into facts., ResolvedQuestion, RetrievalQuery, Decimal, unicodedata

### Community 137 - "page.tsx"
Cohesion: 0.12
Nodes (13): DeliveryBudget(), Usage, Exports(), Configuration, Integrations(), Request, Doc, errors (+5 more)

### Community 138 - "AdmitFlow execution and demonstration checklist"
Cohesion: 0.67
Nodes (3): AdmitFlow execution and demonstration checklist, Build and verify, Demonstrate and submit

### Community 140 - "review"
Cohesion: 0.33
Nodes (10): CRM search and institution downloads, applications(), detail(), owned(), Any, Db, get, post (+2 more)

### Community 141 - "identity_database"
Cohesion: 0.43
Nodes (7): identity_database(), Use a disposable pgvector database; never mutate the demo database., test_downgrade_preserves_legacy_rows_and_refuses_to_destroy_telegram_data(), insert_rows(), inspect_and_clean(), remove_test_bot(), verify_legacy()

### Community 142 - "verify_compose.py"
Cohesion: 0.43
Nodes (6): compose(), Verify the isolated local Compose stack without external API calls or sends., seed_credentials(), verify(), subprocess, websockets_asyncio_client

### Community 143 - "add_institution_knowledge_workspace_b627da2f7e11.py"
Cohesion: 0.40
Nodes (4): Column, DateTime, _timestamps(), upgrade()

### Community 144 - "test_exports.py"
Cohesion: 0.53
Nodes (5): clean(), render_csv(), render_xlsx(), Download encoding prevents formulas while preserving international phone…, test_downloads_never_treat_user_text_as_formulas()

### Community 145 - "add_conversation_runtime_714f092da3b8.py"
Cohesion: 0.50
Nodes (3): columns(), Column, upgrade()

### Community 146 - "durable_payments_outbound_f129a064c5e8.py"
Cohesion: 0.50
Nodes (3): common(), Column, upgrade()

### Community 147 - "notifications.tsx"
Cohesion: 0.33
Nodes (4): labels, Notice, Notifications(), Snapshot

### Community 148 - "AdmitFlow — Task List"
Cohesion: 0.25
Nodes (8): AdmitFlow — Task List, AIBoomi Startup Weekend session handoff (2026-10-22), Current direction and hackathon resources (2026-10-23), Final Postman diagnostic (October 23, executed; delivery blocked), Readiness blocker: idle Redis worker restart (in progress), Readiness tunnel setup (in progress), Test-number delivery diagnosis (October 23, blocked on Meta account restriction), WhatsApp readiness check (2026-10-22, in progress)

### Community 149 - "index_known_name"
Cohesion: 0.40
Nodes (5): index_known_name(), Connection, Mapper, Keep index updates atomic with encrypted names, including name removal., listens_for

### Community 150 - "pytest"
Cohesion: 0.12
Nodes (18): Local operational commands with secrets entered through protected prompts., Bounded login throttling; shared Redis when configured, development fallback., Keep development-only throttle state independent across database test cases., Tests for the Redis distributed mutex (Task 7). The mutex must guarantee: 1.…, parametrize, The temporary tunnel must not expose local debug or documentation routes., test_delivery_status_logs_are_authenticated_and_exclude_pii(), test_tunnel_app_exposes_no_other_routes() (+10 more)

### Community 151 - "11. Human-in-the-Loop (Full Workflow)"
Cohesion: 0.40
Nodes (5): 11.1 Auto-Escalation Triggers, 11.2 Co-pilot Mode, 11.3 Business Hours, 11.4 Never Escalate, 11. Human-in-the-Loop (Full Workflow)

### Community 152 - "reindex_batch"
Cohesion: 0.50
Nodes (5): AsyncSession, UUID, reindex_batch(), test_index_rename_clear_and_legacy_backfill(), exercise()

### Community 153 - "record-demo.mjs"
Cohesion: 0.40
Nodes (4): credentials, headers, journey, target

### Community 154 - "Local Telegram/OpenAI runtime"
Cohesion: 0.25
Nodes (8): Configuration and data services, Delivery budget operation, Local Telegram/OpenAI runtime, Migrate and seed, Optional reminders and scheduler, Packaging and release limits, Run the processes, Validate and recover

### Community 156 - "ADR-014: Natural collection, context reset and responsive replies"
Cohesion: 0.50
Nodes (3): ADR-014: Natural collection, context reset and responsive replies, Decision, Evidence and limits

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

### Community 166 - "ExtractionResponse"
Cohesion: 0.67
Nodes (3): ExtractionResponse, BaseModel, Structured output expected from the LLM when extracting fields.

### Community 167 - "Phase 6: Production Hardening"
Cohesion: 0.33
Nodes (6): Phase 6: Production Hardening, Task 35: Sentry error monitoring, Task 36: Delete My Data endpoint, Task 37: Data retention auto-cleanup, Task 38: Docker Compose for local development, Task 39: Production deployment

### Community 168 - "timeline"
Cohesion: 0.22
Nodes (8): Cursor, Any, AsyncSession, BaseModel, datetime, field_validator, UUID, timeline()

### Community 171 - "test_workspace_limits.py"
Cohesion: 0.09
Nodes (19): ASGIApp, Reject oversized multipart streams before they can fill temporary storage., UploadBodyLimit, private_send(), check_login_limit(), Request, MonkeyPatch, Bound resource use and reject browser cross-origin mutations before database… (+11 more)

### Community 177 - "AdmitFlow submission requirements"
Cohesion: 0.50
Nodes (4): AdmitFlow submission requirements, Demonstration, Required artifacts, Truthful claims

### Community 179 - "10. Observability & Tracing"
Cohesion: 0.50
Nodes (4): 10.1 LLM Tracing (Langfuse), 10.2 Structured Logging, 10.3 Error Monitoring (Sentry), 10. Observability & Tracing

### Community 180 - "5. Code Style"
Cohesion: 0.50
Nodes (4): 5. Code Style, Python (Backend), Separation of Concerns, TypeScript (Frontend)

### Community 183 - "test_worker_broker.py"
Cohesion: 0.25
Nodes (7): Tests for the TaskIQ broker setup and task execution (Task 3). All tests run…, When REDIS_URL is unset the factory should yield an InMemoryBroker., The ping task should run and return the expected payload., Ping without an explicit payload should default to 'pong'., test_broker_is_in_memory_without_redis_url(), test_ping_task_default_payload(), test_ping_task_returns_result()

## Knowledge Gaps
- **433 isolated node(s):** `admitflow-backend`, `fs`, `path`, `crypto`, `root` (+428 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1216 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CRM search and institution downloads` connect `review` to `test_payment_contracts.py`, `lead_statement`, `backend/README.md`?**
  _High betweenness centrality (0.130) - this node is a cross-community bridge._
- **Why does `write_audit_log()` connect `write_audit_log` to `configure`, `lead_statement`, `analytics`, `Reply`, `review`, `LeadStatus`, `test_knowledge_workspace.py`, `deliver`, `payments/webhook.py`, `management.py`, `outreach/followups.py`, `guidance.py`, `send_message`, `knowledge/processing.py`, `accounts.py`, `test_payment_contracts.py`, `generate`, `change_password`, `test_privacy.py`, `api.py`, `live`, `security.py`, `payments/conversation.py`, `test_telegram_journey.py`, `models/__init__.py`, `TelegramAPIError`, `consent.py`, `Phase 1: Foundation`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Why does `AdmitFlow — Task List` connect `AdmitFlow — Task List` to `Phase 5: Dashboard Frontend (Next.js)`, `Phase 3–4 addition (see ADR-008)`, `Phase 4: Advanced Bot Features`, `Phase 6: Production Hardening`, `._post`, `Phase 3: AI Core (Engine + RAG)`, `Phase 1: Foundation`, `2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `encrypt_pii()` (e.g. with `Consequences` and `Decision`) actually correct?**
  _`encrypt_pii()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 60 inferred relationships involving `LeadStatus` (e.g. with `record_stage_changes()` and `Lead`) actually correct?**
  _`LeadStatus` has 60 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `Reply` (e.g. with `advance_application()` and `request_staff()`) actually correct?**
  _`Reply` has 21 INFERRED edges - model-reasoned connections that need verification._
- **What connects `admitflow-backend`, `fs`, `path` to the rest of the system?**
  _433 weakly-connected nodes found - possible documentation gaps or missing edges._