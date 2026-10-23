# Graph Report - admitflow  (2026-10-24)

## Corpus Check
- 253 files · ~134,734 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 3, .example 2, .css 2)

## Summary
- 2301 nodes · 6239 edges · 150 communities (134 shown, 16 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 396 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ab516b1a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ADR-008: System-1 Decision Layer (Laya / Jev)
- Conversation Engine (hand-rolled dispatcher)
- AdmitFlow Complete Specification
- Finalized Production Stack
- leads.py
- guardrails.py
- Code Owns the Money
- journey.py
- RedisMutex
- verify_webhook
- WhatsAppSender
- test_worker_broker.py
- get_redis
- core/rag.py
- PII Encryption & Audit Log
- Razorpay Payment Integration
- get_settings
- admissions.tsx
- dispatcher.py
- encrypt_pii
- AIBoomi Startup Weekend Kochi: fresh-session context
- payments/conversation.py
- exports.py
- enums.py
- LeadStatus
- Stages
- test_concurrent_reviews_allocate_one_seat_and_repeated_approval_is_idempotent
- test_webhook.py
- run_postman_check.cjs
- Task List
- test_telegram_journey.py
- test_crm_search.py
- Phase 5: Dashboard Frontend (Next.js)
- management.py
- Code Standards
- process_followup
- Event preparation and execution plan
- 7. Core Feature Specifications
- analytics
- main.py
- institution.py
- operations.py
- Hackathon resources for AdmitFlow
- manifest.json
- test_workspace_limits.py
- AdmitFlow: current state and planning baseline
- AdmitFlow: AIBoomi submission plan
- AdmitFlow — Complete Specification
- 13. Dashboard Features
- send_outbound
- ADR-011: Advanced RAG Strategy (Latency vs Precision)
- Testing
- test_rag_node.py
- AdmitFlow project handoff
- detect_intent
- ADR-009: Application-Layer PII Encryption and Audit Logging
- RuleOperator
- workspace
- copilot.py
- ADR-010: Triage Fallback Routing (Anti-Spam)
- ADR-012: Telegram and OpenAI for the first complete admissions MVP
- test_staff_operations.py
- 2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md
- compilerOptions
- Login
- 11. Human-in-the-Loop (Full Workflow)
- enqueue_outbound
- api.py
- AdmitFlow Backend
- test_knowledge_workspace.py
- provision_payments.py
- Official source snapshots
- get_sessionmaker
- 10. Observability & Tracing
- 2. Boundaries & Invariants
- test_institution_management.py
- management.tsx
- write_audit_log
- AdmitFlow execution and demonstration checklist
- pytest
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
- EncryptionKeyNotConfiguredError
- crm.py
- Phase 3: AI Core (Engine + RAG)
- fastapi_testclient
- Git & GitHub Workflow
- package.json
- identity_database
- @playwright/test
- AGENTS.md
- Security & Production Readiness
- generate_completion
- next-env.d.ts
- payments/webhook.py
- scripts/__init__.py
- layout.tsx
- frontend/AGENTS.md
- scripts
- Local Telegram/OpenAI runtime
- AdmitFlow pitch deck copy
- add_institution_knowledge_workspace_b627da2f7e11.py
- test_send_budget_redis.py
- sqlalchemy
- Quality Gates — Definition of Done
- integration/conftest.py
- devDependencies
- applications.tsx
- dependencies
- test_payment_contracts.py
- .__call__
- README.md
- uuid
- reindex_batch
- reconcile
- review
- budget.py
- add_conversation_runtime_714f092da3b8.py
- payments.tsx
- durable_payments_outbound_f129a064c5e8.py
- react
- Knowledge
- log_delivery_status
- env.py
- test_shared_budget_preserves_queues_and_settings_wake_deliveries
- process_upload
- 8. RAG (Retrieval-Augmented Generation)
- page.tsx
- index_known_name
- 5. Code Style
- Cursor
- Phase 1: Foundation
- AdmitFlow — Task List
- Phase 3–4 addition (see ADR-008)
- Phase 4: Advanced Bot Features
- Phase 6: Production Hardening
- limits.py
- ExtractionResponse
- tests/conftest.py

## God Nodes (most connected - your core abstractions)
1. `encrypt_pii()` - 100 edges
2. `LeadStatus` - 86 edges
3. `get_settings()` - 85 edges
4. `Lead` - 72 edges
5. `write_audit_log()` - 71 edges
6. `Reply` - 71 edges
7. `decrypt_pii()` - 70 edges
8. `TelegramBot` - 64 edges
9. `Course` - 50 edges
10. `get_sessionmaker()` - 48 edges

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

## Communities (150 total, 16 thin omitted)

### Community 0 - "ADR-008: System-1 Decision Layer (Laya / Jev)"
Cohesion: 0.18
Nodes (17): ADR-001: Hybrid Architecture, ADR-004: Dual Memory Architecture, Episodic Memory (messages table), Semantic Memory (lead_facts table), ADR-005: Three-Layer Guardrails and RAG, Three-Layer Guardrails, ADR-007: Finalized Production Stack, ADR-008: System-1 Decision Layer (Laya / Jev) (+9 more)

### Community 1 - "Conversation Engine (hand-rolled dispatcher)"
Cohesion: 0.25
Nodes (8): Conversation Engine (hand-rolled dispatcher), System-1 decide() Decision Layer, FastAPI WhatsApp Webhook, Langfuse LLM Tracing, pgvector RAG Pipeline, Redis (mutex / dedup / rate-limit), TaskIQ Background Worker, Three-Layer Guardrails

### Community 2 - "AdmitFlow Complete Specification"
Cohesion: 0.25
Nodes (9): Executed final check, One final WhatsApp check with Postman, AdmitFlow necessary resources, Planning baseline before Telegram alignment, AdmitFlow institution knowledge workspace, AdmitFlow Complete Specification, AdmitFlow Platform, AdmitFlow Implementation Plan (+1 more)

### Community 3 - "Finalized Production Stack"
Cohesion: 0.18
Nodes (11): ADR-002: Webhook Concurrency and Deduplication, Per-Phone Redis Mutex, Webhook Deduplication (Redis SETNX), ADR-003: Multi-Tenancy Strategy, Multi-Tenancy (Row-Level Isolation), Finalized Production Stack, Fly.io (Backend + Worker + Scheduler), Langfuse Cloud (LLM Tracing) (+3 more)

### Community 4 - "leads.py"
Cohesion: 0.25
Nodes (17): lead_summary(), Any, course_options(), get_lead(), human_requests(), lead_detail(), leads(), Any (+9 more)

### Community 5 - "guardrails.py"
Cohesion: 0.09
Nodes (34): apply_whatsapp_formatting(), check_input_safety(), check_output_safety(), _deterministic_check(), InputGuardrailResult, LLMGuardrailResponse, LLMOutputGuardrailResponse, OutputGuardrailResult (+26 more)

### Community 6 - "Code Owns the Money"
Cohesion: 0.50
Nodes (5): ADR-006: Code-Owned Qualification and Payments, Intent: Admissions Flow and Discounts, Discount Codes, Code Owns Eligibility, Code Owns the Money

### Community 7 - "journey.py"
Cohesion: 0.10
Nodes (59): Lead, A prospective applicant with optional phone contact and channel identities.…, Trusted bot-to-institution mapping; token is application-encrypted., TelegramBot, action(), application_action(), collect_application(), prompt() (+51 more)

### Community 8 - "RedisMutex"
Cohesion: 0.08
Nodes (25): MutexAcquireError, Redis, RuntimeError, Background loop that extends the TTL while the lock is held., Raised when the mutex cannot be acquired after all retries., Async context-manager mutex backed by Redis ``SET NX``. Parameters: redis: An…, Attempt to acquire the lock, retrying up to ``retry_count`` times., Release the lock using the Lua CAS script (owner-safe). (+17 more)

### Community 9 - "verify_webhook"
Cohesion: 0.21
Nodes (8): get, Response, Handle Meta's webhook challenge., verify_webhook(), mock_settings(), fixture, MonkeyPatch, Ensure all three models are configured for fallback testing.

### Community 10 - "WhatsAppSender"
Cohesion: 0.09
Nodes (23): Any, Send an interactive list message. `sections` is a list of section dicts…, Send a pre-approved template message., Service for sending messages via Meta WhatsApp Cloud API., Post the payload to Meta and extract the created message ID., Meta API expects the phone number without the leading '+'., Send a simple text message. Returns the Meta message ID., Send an interactive message with up to 3 buttons. `buttons` should be a list of… (+15 more)

### Community 11 - "test_worker_broker.py"
Cohesion: 0.25
Nodes (7): Tests for the TaskIQ broker setup and task execution (Task 3). All tests run…, When REDIS_URL is unset the factory should yield an InMemoryBroker., The ping task should run and return the expected payload., Ping without an explicit payload should default to 'pong'., test_broker_is_in_memory_without_redis_url(), test_ping_task_default_payload(), test_ping_task_returns_result()

### Community 12 - "get_redis"
Cohesion: 0.13
Nodes (16): get_redis(), Redis, RuntimeError, Shared async Redis client for application code. Carry-over prerequisite #1: the…, Raised when Redis is needed but ``REDIS_URL`` is unset in settings., Return the process-wide async Redis client singleton. The client is created…, RedisNotConfiguredError, post (+8 more)

### Community 13 - "core/rag.py"
Cohesion: 0.06
Nodes (35): chunk_text(), embed_text(), ingest_document(), Any, AsyncSession, UUID, RAG pipeline core logic (Task 13). Handles ingestion (chunking, embedding),…, Hybrid search (dense + lexical with RRF). (+27 more)

### Community 16 - "get_settings"
Cohesion: 0.14
Nodes (16): AsyncBroker, get_settings(), Return the process-wide :class:`Settings` singleton., _build_broker(), TaskIQ broker singleton. In production (and local dev with Redis running) the…, Construct the right broker based on the current settings. This is a plain…, A real Redis worker must stay listening while its queue is idle., test_idle_queue_listener_receives_a_later_message() (+8 more)

### Community 17 - "admissions.tsx"
Cohesion: 0.13
Nodes (14): Admissions(), Detail, Human, Inquiry, labels, Request, RuleEvidence, statusLabel() (+6 more)

### Community 18 - "dispatcher.py"
Cohesion: 0.10
Nodes (24): MessageDirection, Direction of a WhatsApp message row (episodic memory, ADR-004)., _flush_engine_state(), handle_turn(), _load_engine_state(), Any, AsyncSession, Engine Dispatcher (Task 8 & 17). This module contains the main entry point for… (+16 more)

### Community 19 - "encrypt_pii"
Cohesion: 0.06
Nodes (45): decrypt_pii(), encrypt_bytes(), encrypt_pii(), _fernet(), Encrypt a PII string, returning a url-safe base64 Fernet token. Fernet is…, Encrypt uploaded source bytes before persistence, without lossy text decoding., Decrypt a token produced by :func:`encrypt_pii`. Raises…, AllProvidersFailedError (+37 more)

### Community 20 - "AIBoomi Startup Weekend Kochi: fresh-session context"
Cohesion: 0.11
Nodes (19): AIBoomi Startup Weekend Kochi: fresh-session context, Assessment and next decision, Current readiness session (October 22), Event sources and local copies, Existing prototype rule and surprise element, Existing working-tree changes, Fresh-message prompt, Handoff status (+11 more)

### Community 21 - "payments/conversation.py"
Cohesion: 0.24
Nodes (19): discount_action(), order_reply(), payment_action(), preview(), Any, AsyncSession, UUID, Code-owned fee previews and explicit, conversation-bound payment requests. (+11 more)

### Community 22 - "exports.py"
Cohesion: 0.20
Nodes (16): clean(), download(), export_rows(), ExportRequest, Db, post, Response, Audited institution exports, with explicit limits and spreadsheet-safe text. (+8 more)

### Community 23 - "enums.py"
Cohesion: 0.09
Nodes (41): asyncio, Application-layer PII protection: symmetric encryption + deterministic hashing.…, ApplicationStatus, DiscountType, PaymentStatus, Enumerated types used across the schema. These are Python ``str`` enums mapped…, How a discount code reduces the fee., Payment order lifecycle (SPEC §7.10). (+33 more)

### Community 24 - "LeadStatus"
Cohesion: 0.10
Nodes (36): LeadStatus, Lead lifecycle states (SPEC §7.3). Where a lead *stands*, not a fixed track —…, QualificationRule, A structured eligibility rule evaluated in code, not by the LLM (ADR-006).…, Discovery Node (Task 12). Presents available courses as WhatsApp interactive…, AsyncSession, Qualification Node (Task 15). Extracts rule fields using the LLM and runs…, Run the qualification loop. (+28 more)

### Community 25 - "Stages"
Cohesion: 0.13
Nodes (15): 10. Reflect & learn, 1. Understand & spec  (`/spec`), 2. Plan & pick a task  (`/plan`), 3. Branch, 4. Build with TDD  (`/build`, `/test`), 5. Verify (the quality gate), 6. Self-review, then adversarial review  (`/review`), 7. Commit & open the PR (+7 more)

### Community 27 - "test_webhook.py"
Cohesion: 0.13
Nodes (15): test_tunnel_app_keeps_webhook_verification(), app(), client(), mock_settings(), Any, FastAPI, fixture, TestClient (+7 more)

### Community 28 - "run_postman_check.cjs"
Cohesion: 0.18
Nodes (9): collection, config, crypto, fs, keys, newman, path, root (+1 more)

### Community 29 - "Task List"
Cohesion: 0.15
Nodes (13): Checkpoint: Advanced Features, Checkpoint: AI Core, Checkpoint: Dashboard Complete, Checkpoint: Foundation, Checkpoint: Production Ready, Checkpoint: WhatsApp Ingress, Phase 1: Foundation, Phase 2: WhatsApp Ingress (+5 more)

### Community 30 - "test_telegram_journey.py"
Cohesion: 0.07
Nodes (51): ConversationEvent, process_telegram_event(), task, send_telegram_reply(), normalize_update(), protect_logs(), Any, RuntimeError (+43 more)

### Community 31 - "test_crm_search.py"
Cohesion: 0.21
Nodes (14): Core cross-cutting concerns: settings, security, schemas, guardrails, tracing., name_tokens(), UUID, query_tokens(), Tenant-keyed blind name prefixes; plaintext remains in encrypted columns only., token(), words(), keys() (+6 more)

### Community 32 - "Phase 5: Dashboard Frontend (Next.js)"
Cohesion: 0.17
Nodes (12): Phase 5: Dashboard Frontend (Next.js), Task 24: Initialize Next.js + dark mode + glassmorphism, Task 25: Authentication (email + password), Task 26: Dashboard home (funnel analytics), Task 27: Leads CRM page, Task 28: Course & batch management, Task 29: Chat takeover + co-pilot UI, Task 30: Document management (RAG) (+4 more)

### Community 33 - "management.py"
Cohesion: 0.14
Nodes (37): require_admin(), archive_course(), archive_discount(), BatchInput, catalog(), catalog_detail(), course_view(), CourseInput (+29 more)

### Community 34 - "Code Standards"
Cohesion: 0.18
Nodes (11): Async & I/O, Code Standards, Configuration — settings, not literals, Dependencies, Errors, Formatting, LLM calls, Logging & observability (+3 more)

### Community 35 - "process_followup"
Cohesion: 0.05
Nodes (41): InvalidPhoneError, normalize_e164(), ValueError, E.164 phone-number normalization. Carry-over prerequisite #3: un-normalized…, Raised when a phone string cannot be normalized to E.164., Normalize *raw* into canonical E.164 (``+<digits>``). Strips whitespace,…, escalation_reason(), office_open() (+33 more)

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
Cohesion: 0.16
Nodes (13): ASGIApp, UploadBodyLimit, create_app(), lifespan(), FastAPI, FastAPI application entry point. Boots the API, manages the TaskIQ broker…, Start / stop the TaskIQ broker alongside the FastAPI process. The…, Application factory — builds and configures the FastAPI instance. (+5 more)

### Community 40 - "institution.py"
Cohesion: 0.15
Nodes (23): Dashboard access role (SPEC — admin vs agent)., StaffRole, Institution, Institution (the tenant root) and its staff users., An institution, optionally connected to a legacy WhatsApp number. The tenant…, A dashboard user (admin or agent) belonging to one institution., StaffUser, main() (+15 more)

### Community 41 - "operations.py"
Cohesion: 0.28
Nodes (14): resumed_status(), active_request(), finish_takeover(), Any, AsyncSession, Db, post, UUID (+6 more)

### Community 42 - "Hackathon resources for AdmitFlow"
Cohesion: 0.20
Nodes (10): Acceptance before using a resource, Event and release boundaries, Goal, Hackathon resources for AdmitFlow, October 23 Downloads guide: hosted inference access, Participant credits and other support, Suggested allocation and activation order, Useful resources mapped to the plan (+2 more)

### Community 43 - "manifest.json"
Cohesion: 0.20
Nodes (9): SPEC.md, bytes, sha256, tasks/plan.md, bytes, sha256, tasks/todo.md, bytes (+1 more)

### Community 44 - "test_workspace_limits.py"
Cohesion: 0.17
Nodes (12): Custom header + strict cookies prevent cross-origin simple-request CSRF., require_browser_write(), check_login_limit(), Request, MonkeyPatch, Bound resource use and reject browser cross-origin mutations before database…, test_custom_header_and_origin_required(), test_embedding_key_loaded_from_settings() (+4 more)

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

### Community 49 - "send_outbound"
Cohesion: 0.11
Nodes (23): send_outbound(), age(), outreach(), fixture, parametrize, seed(), test_budget_pause_does_not_spend_a_reminder_and_stop_cancels_it(), exercise() (+15 more)

### Community 50 - "ADR-011: Advanced RAG Strategy (Latency vs Precision)"
Cohesion: 0.25
Nodes (7): 1. Complex Document Ingestion (`docling` or `unstructured`), 2. Pluggable Reranking Architecture (Cohere API over Local CPU), 3. Contextual Query Rewriting, ADR-011: Advanced RAG Strategy (Latency vs Precision), Consequences, Context, Decision

### Community 51 - "Testing"
Cohesion: 0.22
Nodes (9): Browser announcement regions, Coverage, LLM and decision-layer tests, Philosophy — pragmatic TDD, Running tests, Test layout, Testing, The two patterns (+1 more)

### Community 52 - "test_rag_node.py"
Cohesion: 0.17
Nodes (14): Sanitizer to prevent RAG poisoning. Blocks chunks that contain obvious prompt…, sanitize_chunks(), process_rag_node(), AsyncSession, RAG Node (Task 14). Graph node that retrieves from the knowledge base and…, Retrieve context and answer knowledge questions., mock_state(), asyncio (+6 more)

### Community 53 - "AdmitFlow project handoff"
Cohesion: 0.25
Nodes (8): AdmitFlow project handoff, Current direction, Development rules, Event submission, Execution checkpoint, First usable release, Historical evidence, Resume prompt

### Community 54 - "detect_intent"
Cohesion: 0.20
Nodes (15): detect_intent(), Classify the user's intent to route to the correct node. Design Decision: If a…, asyncio, Test routing for course discovery., Test routing for knowledge questions., Test routing for qualification answers., Test routing for human handoff., Test routing for empty messages without calling LLM defaults to discovery. (+7 more)

### Community 55 - "ADR-009: Application-Layer PII Encryption and Audit Logging"
Cohesion: 0.15
Nodes (12): DatabaseNotConfiguredError, RuntimeError, Raised when a DB session is requested but ``DATABASE_URL`` is unset., ADR-009: Application-Layer PII Encryption and Audit Logging, Alternatives Considered, Consequences, Context, Decision (+4 more)

### Community 56 - "RuleOperator"
Cohesion: 0.27
Nodes (13): Qualification-rule comparison operators (SPEC §7.4). Evaluated…, RuleOperator, _coerce_values(), evaluate_rule(), Any, Evaluate a qualification rule deterministically. Args: operator: The…, test_evaluate_rule_in_list(), test_evaluate_rule_missing_extracted_value() (+5 more)

### Community 57 - "workspace"
Cohesion: 0.12
Nodes (19): payments(), Any, get, fixture, workspace(), UUID, seed(), exercise() (+11 more)

### Community 58 - "copilot.py"
Cohesion: 0.09
Nodes (30): load_memory(), Any, AsyncSession, UUID, timeline(), event_text(), AsyncSession, content() (+22 more)

### Community 59 - "ADR-010: Triage Fallback Routing (Anti-Spam)"
Cohesion: 0.33
Nodes (5): ADR-010: Triage Fallback Routing (Anti-Spam), Consequences, Context, Decision, Status

### Community 60 - "ADR-012: Telegram and OpenAI for the first complete admissions MVP"
Cohesion: 0.29
Nodes (7): ADR-012: Telegram and OpenAI for the first complete admissions MVP, Consequences, Context, Decision, Implemented runtime boundaries, References and verification, Supersession and preserved decisions

### Community 61 - "test_staff_operations.py"
Cohesion: 0.11
Nodes (26): recent_history(), test_local_cohort_counts_conversions_and_observed_stages(), test_tenant_is_derived_from_session_and_period_is_bounded(), test_zero_filled_weekly_buckets_and_empty_rates(), test_downloads_roles_datasets_limits_and_tenants(), test_search_scope_validation_and_audit(), test_explicit_consent_and_stop_during_staff_takeover(), exercise() (+18 more)

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

### Community 66 - "enqueue_outbound"
Cohesion: 0.14
Nodes (12): process_payment(), payment_webhook(), Db, post, Request, UUID, enqueue_outbound(), AsyncSession (+4 more)

### Community 67 - "api.py"
Cohesion: 0.06
Nodes (47): documents(), get_upload(), Any, BaseModel, Db, delete, get, post (+39 more)

### Community 68 - "AdmitFlow Backend"
Cohesion: 0.12
Nodes (16): Admissions analytics, AdmitFlow Backend, Application payments, Configuration, Consented follow-up reminders, Current implementation and verification, Institution knowledge workspace, Local development (+8 more)

### Community 69 - "test_knowledge_workspace.py"
Cohesion: 0.06
Nodes (26): alembic, alembic_config, Application settings singleton. Loads configuration from the environment (and…, Batch, A dated intake of a course with finite seats (SPEC §7.5)., Async engine and session factory. Built lazily from ``settings.database_url``…, Institution document extraction, durable ingestion and retrieval., Durable upload claims, bounded embedding and atomic publication of ready… (+18 more)

### Community 70 - "provision_payments.py"
Cohesion: 0.09
Nodes (30): AsyncBaseTransport, Credentials, PaymentLink, PaymentProviderError, BaseModel, Exception, field_validator, Bounded Razorpay requests; ambiguous link creation is never blindly retried. (+22 more)

### Community 71 - "Official source snapshots"
Cohesion: 0.50
Nodes (4): Conflicts to confirm, October 23 planning refresh, Official source snapshots, Sources

### Community 72 - "get_sessionmaker"
Cohesion: 0.06
Nodes (53): argparse, async_sessionmaker, AsyncEngine, get_engine(), get_session(), get_sessionmaker(), AsyncSession, Return the process-wide async engine (one pool for the app). (+45 more)

### Community 73 - "10. Observability & Tracing"
Cohesion: 0.50
Nodes (4): 10.1 LLM Tracing (Langfuse), 10.2 Structured Logging, 10.3 Error Monitoring (Sentry), 10. Observability & Tracing

### Community 74 - "2. Boundaries & Invariants"
Cohesion: 0.50
Nodes (4): 2. Boundaries & Invariants, Always Do, Ask First, Never Do

### Community 75 - "test_institution_management.py"
Cohesion: 0.47
Nodes (5): Any, Real database management: administrator writes, role/tenant boundaries and…, test_catalog_writes_validate_rules_capacity_and_ownership(), test_discount_management_rejects_invalid_values_duplicates_and_foreign_writes(), test_settings_validate_timezone_hours_and_tenant_scope()

### Community 76 - "management.tsx"
Cohesion: 0.14
Nodes (10): Batch, Course, empty, Management(), operators, parseValue(), Rule, Settings (+2 more)

### Community 77 - "write_audit_log"
Cohesion: 0.20
Nodes (11): Any, AsyncSession, UUID, Record persisted ORM transitions atomically; never infer an earlier stage., Append one entry to ``audit_logs`` on ``session``; return it flushed, not…, record_stage_changes(), write_audit_log(), Unit test for the audit-log write helper. The real INSERT path (JSONB, server-… (+3 more)

### Community 78 - "AdmitFlow execution and demonstration checklist"
Cohesion: 0.67
Nodes (3): AdmitFlow execution and demonstration checklist, Build and verify, Demonstrate and submit

### Community 79 - "pytest"
Cohesion: 0.13
Nodes (14): RuntimeError, WhatsApp message sending service (Task 6). Uses httpx2 to call the Meta Graph…, Raised when the Meta Cloud API returns an error response., WhatsAppAPIError, Any, asyncio, fixture, patch (+6 more)

### Community 84 - "analytics.tsx"
Cohesion: 0.28
Nodes (7): Analytics(), Conversion, labels, frontend_app_analytics_module, rate(), Report, shortDate()

### Community 89 - "Settings"
Cohesion: 0.13
Nodes (26): hash_phone(), Return a deterministic keyed hash of a phone number for lookup/dedup. Keyed…, Environment-backed application configuration., Settings, configured_keys(), fixture, MonkeyPatch, Unit tests for application-layer PII protection (encrypt/decrypt + phone hash). (+18 more)

### Community 90 - "AdmitFlow"
Cohesion: 0.33
Nodes (6): AdmitFlow, Current status, Demonstration and submission, Development, Product scope, Stack

### Community 91 - "models/__init__.py"
Cohesion: 0.11
Nodes (44): Base, IdMixin, Declarative base, metadata naming convention, and shared column mixins. Every…, Declarative base shared by every AdmitFlow model., UUID primary key with an application-side default. UUIDs avoid cross-tenant…, Server-side created/updated timestamps., Row-level tenant scoping (ADR-003). Mixed into every tenant-scoped table., TenantMixin (+36 more)

### Community 92 - "EncryptionKeyNotConfiguredError"
Cohesion: 0.17
Nodes (13): EncryptionKeyNotConfiguredError, RuntimeError, Raised when a PII helper is used but its key is unset in settings., hash_telegram_identifier(), UUID, Private Telegram identity lookup without storing raw identifiers in indexes., Hash an identifier in its tenant/bot/type domain using the lookup secret. This…, MonkeyPatch (+5 more)

### Community 93 - "crm.py"
Cohesion: 0.29
Nodes (9): normalized_phone(), lead_statement(), LeadFilters, LeadSearch, BaseModel, Select, UUID, Shared bounded CRM filters; search values never belong in URLs or audit details. (+1 more)

### Community 94 - "Phase 3: AI Core (Engine + RAG)"
Cohesion: 0.18
Nodes (11): Phase 3: AI Core (Engine + RAG), Task 10: Input guardrail node, Task 11: Triage node (intent detection), Task 12: Discovery node, Task 13: RAG pipeline, Task 14: RAG node, Task 15: Qualification node, Task 16: Output guardrail (+3 more)

### Community 95 - "fastapi_testclient"
Cohesion: 0.20
Nodes (5): Tests for the /debug endpoints (Task 3 verification)., GET /debug/enqueue-ping should enqueue a ping task and return its ID., test_enqueue_ping_returns_task_id(), Tests for the FastAPI app: health check and Swagger UI., fastapi_testclient

### Community 96 - "Git & GitHub Workflow"
Cohesion: 0.22
Nodes (9): Branching model — feature branch → PR → `main`, Commits — Conventional Commits, small and coherent, Git & GitHub Workflow, Merging, No AI attribution — the human is the sole author  ⚠️, Pull Requests, Review gate — adversarial, before merge, What never gets committed (+1 more)

### Community 97 - "package.json"
Cohesion: 0.22
Nodes (8): name, private, version, react-dom, @types/node, @types/react, @types/react-dom, typescript

### Community 98 - "identity_database"
Cohesion: 0.36
Nodes (8): identity_database(), fixture, Use a disposable pgvector database; never mutate the demo database., test_downgrade_preserves_legacy_rows_and_refuses_to_destroy_telegram_data(), insert_rows(), inspect_and_clean(), remove_test_bot(), verify_legacy()

### Community 99 - "@playwright/test"
Cohesion: 0.16
Nodes (7): credentials, headers, journey, target, ref_node_fs, ref_node_path, @playwright/test

### Community 100 - "AGENTS.md"
Cohesion: 0.25
Nodes (7): AIBoomi Startup Weekend handoff, How we build — read the handbook, Knowledge graph, Quick commands (from `backend/`), The rules you cannot skip, What this project is, Workflow triggers

### Community 101 - "Security & Production Readiness"
Cohesion: 0.18
Nodes (11): Dependency & secret scanning, Deploy & rollback, External surfaces, Guardrails & money, Local full-stack (docker-compose), Multi-tenancy — isolation is a correctness bug if wrong, Observability, PII & data protection (DPDPA) (+3 more)

### Community 102 - "generate_completion"
Cohesion: 0.10
Nodes (26): generate_completion(), Any, Generate a completion with automatic provider fallback. Tries the fast model,…, BaseModel, Triage Node (Task 11). Routes incoming messages to the appropriate downstream…, Structured output expected from the LLM triage classifier., TriageResponse, Engine state definition (Task 8). Defines the plain dataclass/Pydantic model… (+18 more)

### Community 103 - "next-env.d.ts"
Cohesion: 0.50
Nodes (3): NOTE: This file should not be edited, frontend_next_types_root_params_d, frontend_next_types_routes_d

### Community 104 - "payments/webhook.py"
Cohesion: 0.31
Nodes (9): LinkEntity, LinkEnvelope, PaidEvent, PaidPayload, PaymentEntity, PaymentEnvelope, BaseModel, Raw-body authenticated, amount-checked and replay-safe payment confirmation. (+1 more)

### Community 106 - "layout.tsx"
Cohesion: 0.25
Nodes (5): frontend_app_globals, metadata, config, @fontsource-variable/dm-sans, next

### Community 108 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, lint, record:demo, start, test:e2e:live, typecheck

### Community 109 - "Local Telegram/OpenAI runtime"
Cohesion: 0.22
Nodes (8): Configuration and data services, Delivery budget operation, Local Telegram/OpenAI runtime, Migrate and seed, Optional reminders and scheduler, Packaging and release limits, Run the processes, Validate and recover

### Community 110 - "AdmitFlow pitch deck copy"
Cohesion: 0.29
Nodes (7): AdmitFlow pitch deck copy, Slide 1: AdmitFlow, Slide 2: The admissions inquiry, Slide 3: A working student journey, Slide 4: Institution knowledge and control, Slide 5: Technology and verification, Slide 6: Pilot and next steps

### Community 111 - "add_institution_knowledge_workspace_b627da2f7e11.py"
Cohesion: 0.40
Nodes (4): Column, DateTime, _timestamps(), upgrade()

### Community 112 - "test_send_budget_redis.py"
Cohesion: 0.40
Nodes (4): Redis distributed mutex with owner-safe release and keepalive (Task 7). Ensures…, Actual Redis Lua reservations must remain bounded under concurrent workers., redis_asyncio, types

### Community 113 - "sqlalchemy"
Cohesion: 0.15
Nodes (18): Audit-log write helper. :func:`write_audit_log` is the one path significant…, Lead, its semantic facts (lead_facts), and episodic messages (ADR-004)., Bounded chronological transcript across inbound, replies and standalone…, Human-readable callback summaries without exposing routing or signature details., Check, Hook, BaseModel, Lease-backed, consented reminders with fresh-state checks before generation and… (+10 more)

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

### Community 119 - "test_payment_contracts.py"
Cohesion: 0.15
Nodes (16): Expose only the existing Meta webhook through the temporary demo tunnel., discounted_amount(), Integer monetary arithmetic and exact-byte webhook authentication., verify_webhook(), WhatsApp Webhook routing (Task 5). Handles GET (challenge) and POST (incoming…, Money stays integer/code-owned; signatures use exact bytes; creation never…, test_discounts_use_minor_units_and_boundaries(), test_webhook_signature_uses_raw_body_and_rejects_tampering() (+8 more)

### Community 120 - ".__call__"
Cohesion: 0.33
Nodes (4): private_send(), Receive, Scope, Send

### Community 121 - "README.md"
Cohesion: 0.14
Nodes (11): AI Impact Statement, Student-to-staff demonstration, Current templates, Language review packet, Live exercise, Reminder consent and outreach copy, Prior-work disclosure draft, AdmitFlow submission requirements (+3 more)

### Community 122 - "uuid"
Cohesion: 0.19
Nodes (11): task, Follow-up jobs carry only tenant and lead identifiers, never student content., send_followup(), task, Encrypted outbound-message delivery jobs carry only internal identifiers., send_outbound_message(), create_payment_link(), task (+3 more)

### Community 123 - "reindex_batch"
Cohesion: 0.40
Nodes (6): main(), AsyncSession, UUID, reindex_batch(), test_index_rename_clear_and_legacy_backfill(), exercise()

### Community 124 - "reconcile"
Cohesion: 0.61
Nodes (8): locked(), owned(), provider(), Db, post, UUID, reconcile(), retry()

### Community 125 - "review"
Cohesion: 0.33
Nodes (10): CRM search and institution downloads, applications(), detail(), owned(), Any, Db, get, post (+2 more)

### Community 126 - "budget.py"
Cohesion: 0.15
Nodes (23): day_window(), local_counts(), Any, datetime, UUID, Atomic daily send-attempt budgets shared by every Telegram delivery path., Count confirmed deliveries once; a stats failure must not repeat a sent message., record_sent() (+15 more)

### Community 127 - "add_conversation_runtime_714f092da3b8.py"
Cohesion: 0.50
Nodes (3): columns(), Column, upgrade()

### Community 128 - "payments.tsx"
Cohesion: 0.32
Nodes (6): label(), money(), outcomes, Payment, Payments(), statuses

### Community 129 - "durable_payments_outbound_f129a064c5e8.py"
Cohesion: 0.50
Nodes (3): common(), Column, upgrade()

### Community 130 - "react"
Cohesion: 0.29
Nodes (4): blank, Discount, Discounts(), react

### Community 131 - "Knowledge"
Cohesion: 0.46
Nodes (8): refresh(), api(), Knowledge(), action(), login(), search(), upload(), send()

### Community 132 - "log_delivery_status"
Cohesion: 0.40
Nodes (5): log_delivery_status(), Request, Response, Observe only authenticated status events, without recipient or error text., middleware

### Community 133 - "env.py"
Cohesion: 0.22
Nodes (9): do_run_migrations(), Connection, Alembic migration environment (async). Reads the database URL from application…, Emit SQL to stdout without a live DB connection., Run migrations against a live database via an async engine., run_migrations_offline(), run_migrations_online(), logging_config (+1 more)

### Community 135 - "process_upload"
Cohesion: 0.10
Nodes (22): decrypt_bytes(), Authenticate and decrypt source bytes for an authorized ingestion task., process_upload(), UUID, Claim once, process outside the transaction, then publish only the current…, ingest_upload(), task, TaskIQ entry point for institution document indexing. (+14 more)

### Community 136 - "8. RAG (Retrieval-Augmented Generation)"
Cohesion: 0.50
Nodes (4): 8.1 Per-Institution Knowledge Base, 8.2 Retrieval Pipeline, 8.3 RAG Guardrail, 8. RAG (Retrieval-Augmented Generation)

### Community 137 - "page.tsx"
Cohesion: 0.20
Nodes (7): DeliveryBudget(), Usage, Exports(), Doc, errors, Match, Staff

### Community 138 - "index_known_name"
Cohesion: 0.40
Nodes (5): index_known_name(), Connection, Keep index updates atomic with encrypted names, including name removal., listens_for, Mapper

### Community 139 - "5. Code Style"
Cohesion: 0.50
Nodes (4): 5. Code Style, Python (Backend), Separation of Concerns, TypeScript (Frontend)

### Community 140 - "Cursor"
Cohesion: 0.40
Nodes (4): Cursor, BaseModel, datetime, field_validator

### Community 141 - "Phase 1: Foundation"
Cohesion: 0.40
Nodes (5): Phase 1: Foundation, Task 1: Initialize Python project, FastAPI, settings, and Docker, Task 2: PostgreSQL schema (SQLAlchemy + Alembic), Task 3: TaskIQ + Redis broker setup, Task 4: PII encryption utilities and audit log infrastructure

### Community 142 - "AdmitFlow — Task List"
Cohesion: 0.25
Nodes (8): AdmitFlow — Task List, AIBoomi Startup Weekend session handoff (2026-10-22), Current direction and hackathon resources (2026-10-23), Final Postman diagnostic (October 23, executed; delivery blocked), Readiness blocker: idle Redis worker restart (in progress), Readiness tunnel setup (in progress), Test-number delivery diagnosis (October 23, blocked on Meta account restriction), WhatsApp readiness check (2026-10-22, in progress)

### Community 144 - "Phase 3–4 addition (see ADR-008)"
Cohesion: 0.29
Nodes (7): Phase 3–4 addition (see ADR-008), Task 40: `decide()` System-1 decision-layer abstraction, Task 41: Distill decisions into self-hosted Laya (post-demo), Task 42.1: Complex Document Parsing & Semantic Chunking, Task 42.2: Contextual Query Rewriting, Task 42.3: Pluggable Reranker (Cohere API vs Local), Task 42: Advanced RAG Strategy (ADR-011)

### Community 145 - "Phase 4: Advanced Bot Features"
Cohesion: 0.29
Nodes (7): Phase 4: Advanced Bot Features, Task 18: Application form collection node, Task 19: Razorpay integration, Task 20: Human handoff + co-pilot mode, Task 21: Cold lead re-engagement worker, Task 22: WhatsApp rate-limit tracking, Task 23: Langfuse tracing integration

### Community 146 - "Phase 6: Production Hardening"
Cohesion: 0.33
Nodes (6): Phase 6: Production Hardening, Task 35: Sentry error monitoring, Task 36: Delete My Data endpoint, Task 37: Data retention auto-cleanup, Task 38: Docker Compose for local development, Task 39: Production deployment

### Community 147 - "limits.py"
Cohesion: 0.50
Nodes (3): Reject oversized multipart streams before they can fill temporary storage., starlette_responses, starlette_types

### Community 148 - "ExtractionResponse"
Cohesion: 0.67
Nodes (3): ExtractionResponse, BaseModel, Structured output expected from the LLM when extracting fields.

## Knowledge Gaps
- **403 isolated node(s):** `admitflow-backend`, `fs`, `path`, `crypto`, `root` (+398 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1026 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CRM search and institution downloads` connect `review` to `workspace`, `AdmitFlow Complete Specification`, `leads.py`?**
  _High betweenness centrality (0.117) - this node is a cross-community bridge._
- **Why does `LeadStatus` connect `LeadStatus` to `leads.py`, `journey.py`, `dispatcher.py`, `encrypt_pii`, `payments/conversation.py`, `enums.py`, `test_telegram_journey.py`, `process_followup`, `analytics`, `operations.py`, `send_outbound`, `test_rag_node.py`, `workspace`, `enqueue_outbound`, `test_knowledge_workspace.py`, `get_sessionmaker`, `write_audit_log`, `models/__init__.py`, `crm.py`, `generate_completion`, `payments/webhook.py`, `sqlalchemy`, `review`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Why does `handle_turn()` connect `dispatcher.py` to `process_followup`, `guardrails.py`, `journey.py`, `RedisMutex`, `institution.py`, `get_sessionmaker`, `WhatsAppSender`, `get_redis`, `pytest`, `AdmitFlow — Complete Specification`, `encrypt_pii`, `test_rag_node.py`, `detect_intent`, `LeadStatus`, `Settings`, `models/__init__.py`, `Phase 3: AI Core (Engine + RAG)`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `encrypt_pii()` (e.g. with `Consequences` and `Decision`) actually correct?**
  _`encrypt_pii()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 52 inferred relationships involving `LeadStatus` (e.g. with `record_stage_changes()` and `Lead`) actually correct?**
  _`LeadStatus` has 52 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `Lead` (e.g. with `record_stage_changes()` and `Institution`) actually correct?**
  _`Lead` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `admitflow-backend`, `fs`, `path` to the rest of the system?**
  _403 weakly-connected nodes found - possible documentation gaps or missing edges._