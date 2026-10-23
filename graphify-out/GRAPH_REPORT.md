# Graph Report - admitflow  (2026-10-24)

## Corpus Check
- 283 files · ~148,232 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 3, .example 2, .css 2)

## Summary
- 2542 nodes · 7040 edges · 168 communities (145 shown, 23 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 442 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2b3dd6eb`
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
- test_payment_contracts.py
- WhatsAppSender
- transport.py
- get_redis
- core/rag.py
- PII Encryption & Audit Log
- Razorpay Payment Integration
- get_settings
- admissions.tsx
- test_dispatcher.py
- encrypt_pii
- AIBoomi Startup Weekend Kochi: fresh-session context
- PaymentStatus
- exports.py
- Course
- LeadStatus
- Stages
- test_integrations_notifications.py
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
- send_message
- Hackathon resources for AdmitFlow
- manifest.json
- test_workspace_limits.py
- AdmitFlow: current state and planning baseline
- AdmitFlow: AIBoomi submission plan
- AdmitFlow — Complete Specification
- normalize_e164
- integration/test_followups.py
- ADR-011: Required OpenAI passage reranking
- Testing
- guardrails.py
- AdmitFlow project handoff
- unittest_mock
- hash_phone
- RuleOperator
- test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment
- copilot.py
- ADR-010: Triage Fallback Routing (Anti-Spam)
- ADR-012: Telegram and OpenAI for the first complete admissions MVP
- signin
- compilerOptions
- auth.py
- Lead
- staff/payments.py
- api.py
- process_upload
- alembic
- RazorpayClient
- Official source snapshots
- get_sessionmaker
- test_application_journey.py
- Reply
- budget.py
- management.tsx
- pg_url
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
- configured_keys
- AdmitFlow
- models/__init__.py
- tests/test_telegram_identity.py
- test_decision_reranking.py
- crm.py
- evaluate_faq.py
- Git & GitHub Workflow
- package.json
- identity_database
- @playwright/test
- AGENTS.md
- Security & Production Readiness
- validate_services.py
- next-env.d.ts
- payments/webhook.py
- test_rag_node.py
- layout.tsx
- frontend/AGENTS.md
- scripts
- backend/README.md
- AdmitFlow pitch deck copy
- add_institution_knowledge_workspace_b627da2f7e11.py
- typing
- sqlalchemy
- Quality Gates — Definition of Done
- DocumentChunk
- devDependencies
- applications.tsx
- dependencies
- update
- re
- README.md
- knowledge/processing.py
- reindex_names.py
- WhatsApp readiness check — October 22, 2026
- write_audit_log
- erase_inquiry
- test_english_query_does_not_call_model
- payments.tsx
- test_expired_lease_recovery_cap_and_configuration_cancellation
- react
- Knowledge
- json
- env.py
- test_shared_budget_preserves_queues_and_settings_wake_deliveries
- test_knowledge_workspace.py
- process_payment
- page.tsx
- index_known_name
- configure
- 13. Dashboard Features
- test_worker_broker.py
- 20260929_initial_schema_64cfce85009d.py
- Phase 3–4 addition (see ADR-008)
- collections_abc
- .__call__
- notifications.tsx
- hash_telegram_identifier
- Implementation Plan: AdmitFlow
- add_conversation_runtime_714f092da3b8.py
- durable_payments_outbound_f129a064c5e8.py
- 11. Human-in-the-Loop (Full Workflow)
- record-demo.mjs
- 20261008_add_knowledge_models_for_rag_c470f1ebc811.py
- mock_settings
- 10. Observability & Tracing
- 2. Boundaries & Invariants
- 3. Tech Stack & Commands
- 5. Code Style
- 8. RAG (Retrieval-Augmented Generation)
- migrated_db
- test_payment_and_webhook_claims_wait_for_erasure_lock
- 17. Decisions & Open Questions
- privacy_dependencies
- test_every_tenant_scoped_table_has_tenant_id_fk_to_institutions

## God Nodes (most connected - your core abstractions)
1. `encrypt_pii()` - 104 edges
2. `write_audit_log()` - 95 edges
3. `LeadStatus` - 90 edges
4. `get_settings()` - 89 edges
5. `Lead` - 76 edges
6. `decrypt_pii()` - 75 edges
7. `Reply` - 73 edges
8. `TelegramBot` - 66 edges
9. `signin()` - 56 edges
10. `get_sessionmaker()` - 53 edges

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

## Communities (168 total, 23 thin omitted)

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
Cohesion: 0.23
Nodes (18): lead_summary(), Any, course_options(), get_lead(), human_requests(), lead_detail(), leads(), Any (+10 more)

### Community 5 - "pydantic"
Cohesion: 0.08
Nodes (35): decide(), Any, Typed decisions through the existing OpenAI-only provider boundary., Validate structured model output; refusal/malformed output is never a decision.…, AllProvidersFailedError, generate_completion(), Any, Exception (+27 more)

### Community 6 - "Code Owns the Money"
Cohesion: 0.50
Nodes (5): ADR-006: Code-Owned Qualification and Payments, Intent: Admissions Flow and Discounts, Discount Codes, Code Owns Eligibility, Code Owns the Money

### Community 7 - "journey.py"
Cohesion: 0.23
Nodes (22): answer_question(), build_reply(), button(), copy(), courses(), ExtractedFact, Extraction, GroundedQuote (+14 more)

### Community 8 - "RedisMutex"
Cohesion: 0.07
Nodes (28): MutexAcquireError, Redis, RuntimeError, Redis distributed mutex with owner-safe release and keepalive (Task 7). Ensures…, Background loop that extends the TTL while the lock is held., Raised when the mutex cannot be acquired after all retries., Async context-manager mutex backed by Redis ``SET NX``. Parameters: redis: An…, Attempt to acquire the lock, retrying up to ``retry_count`` times. (+20 more)

### Community 9 - "test_payment_contracts.py"
Cohesion: 0.18
Nodes (13): discounted_amount(), Integer monetary arithmetic and exact-byte webhook authentication., verify_webhook(), get, Response, WhatsApp Webhook routing (Task 5). Handles GET (challenge) and POST (incoming…, Handle Meta's webhook challenge., verify_webhook() (+5 more)

### Community 10 - "WhatsAppSender"
Cohesion: 0.07
Nodes (29): Any, RuntimeError, WhatsApp message sending service (Task 6). Uses httpx2 to call the Meta Graph…, Send an interactive list message. `sections` is a list of section dicts…, Send a pre-approved template message., Raised when the Meta Cloud API returns an error response., Service for sending messages via Meta WhatsApp Cloud API., Post the payload to Meta and extract the created message ID. (+21 more)

### Community 11 - "transport.py"
Cohesion: 0.13
Nodes (23): destination(), post_event(), PrivateTransportLogs, protect_logs(), public_ip(), LogRecord, HTTPS delivery pins a public resolved address while retaining TLS host…, resolve_public() (+15 more)

### Community 12 - "get_redis"
Cohesion: 0.12
Nodes (17): get_redis(), Redis, RuntimeError, Shared async Redis client for application code. Carry-over prerequisite #1: the…, Raised when Redis is needed but ``REDIS_URL`` is unset in settings., Return the process-wide async Redis client singleton. The client is created…, RedisNotConfiguredError, post (+9 more)

### Community 13 - "core/rag.py"
Cohesion: 0.13
Nodes (19): chunk_text(), embed_text(), ingest_document(), Any, AsyncSession, UUID, RAG pipeline core logic (Task 13). Handles ingestion (chunking, embedding),…, Hybrid search (dense + lexical with RRF). (+11 more)

### Community 16 - "get_settings"
Cohesion: 0.10
Nodes (26): AsyncBroker, get_settings(), Application settings singleton. Loads configuration from the environment (and…, Environment-backed application configuration., Return the process-wide :class:`Settings` singleton., Settings, _build_broker(), TaskIQ broker singleton. In production (and local dev with Redis running) the… (+18 more)

### Community 17 - "admissions.tsx"
Cohesion: 0.12
Nodes (15): Admissions(), Detail, Human, Inquiry, labels, Request, RuleEvidence, statusLabel() (+7 more)

### Community 18 - "test_dispatcher.py"
Cohesion: 0.13
Nodes (14): ping(), process_inbound_message(), Any, task, Background tasks for message processing. For now this module holds only the…, Smoke-test task: returns ``{"result": payload}``. Enqueued from the…, Process an inbound WhatsApp message (Task 17). This is a placeholder for the…, Any (+6 more)

### Community 19 - "encrypt_pii"
Cohesion: 0.11
Nodes (31): decrypt_pii(), encrypt_bytes(), encrypt_pii(), _fernet(), Application-layer PII protection: symmetric encryption + deterministic hashing.…, Encrypt a PII string, returning a url-safe base64 Fernet token. Fernet is…, Encrypt uploaded source bytes before persistence, without lossy text decoding., Decrypt a token produced by :func:`encrypt_pii`. Raises… (+23 more)

### Community 20 - "AIBoomi Startup Weekend Kochi: fresh-session context"
Cohesion: 0.11
Nodes (19): AIBoomi Startup Weekend Kochi: fresh-session context, Assessment and next decision, Current readiness session (October 22), Event sources and local copies, Existing prototype rule and surprise element, Existing working-tree changes, Fresh-message prompt, Handoff status (+11 more)

### Community 21 - "PaymentStatus"
Cohesion: 0.26
Nodes (19): PaymentStatus, Payment order lifecycle (SPEC §7.10)., discount_action(), order_reply(), payment_action(), preview(), Any, AsyncSession (+11 more)

### Community 22 - "exports.py"
Cohesion: 0.16
Nodes (16): clean(), Audited institution exports, with explicit limits and spreadsheet-safe text., render_csv(), render_xlsx(), crm_data(), fixture, Real database CRM lookup, index maintenance, export roles and isolation., test_search_pages_are_bounded_and_do_not_drop_or_repeat_records() (+8 more)

### Community 23 - "Course"
Cohesion: 0.12
Nodes (22): Application, PaymentOrder, Structured application data collected from an admission-ready lead (SPEC §7.9).…, A Razorpay order for an application fee (SPEC §7.10). Amount is DB-sourced…, Batch, Course, A program a lead can be qualified for and pay to apply to., A dated intake of a course with finite seats (SPEC §7.5). (+14 more)

### Community 24 - "LeadStatus"
Cohesion: 0.11
Nodes (32): LeadStatus, Lead lifecycle states (SPEC §7.3). Where a lead *stands*, not a fixed track —…, AsyncSession, Run the qualification loop., run_qualification(), EngineState, InvalidTransitionError, BaseModel (+24 more)

### Community 25 - "Stages"
Cohesion: 0.13
Nodes (15): 10. Reflect & learn, 1. Understand & spec  (`/spec`), 2. Plan & pick a task  (`/plan`), 3. Branch, 4. Build with TDD  (`/build`, `/test`), 5. Verify (the quality gate), 6. Self-review, then adversarial review  (`/review`), 7. Commit & open the PR (+7 more)

### Community 26 - "test_integrations_notifications.py"
Cohesion: 0.14
Nodes (12): deliver(), UUID, Leased at-least-once webhook delivery with stable recipient deduplication IDs., Durable, minimal institution events and signed outbound integrations., Staff authentication and institution-scoped access., task, Integration queue messages contain identifiers only., send_webhook() (+4 more)

### Community 27 - "test_webhook.py"
Cohesion: 0.13
Nodes (15): test_tunnel_app_keeps_webhook_verification(), app(), client(), mock_settings(), Any, FastAPI, fixture, TestClient (+7 more)

### Community 28 - "run_postman_check.cjs"
Cohesion: 0.20
Nodes (8): collection, config, crypto, fs, keys, newman, path, root

### Community 29 - "Task List"
Cohesion: 0.15
Nodes (13): Checkpoint: Advanced Features, Checkpoint: AI Core, Checkpoint: Dashboard Complete, Checkpoint: Foundation, Checkpoint: Production Ready, Checkpoint: WhatsApp Ingress, Phase 1: Foundation, Phase 2: WhatsApp Ingress (+5 more)

### Community 30 - "telegram/service.py"
Cohesion: 0.08
Nodes (41): process_telegram_event(), task, send_telegram_reply(), normalize_update(), protect_logs(), Any, LogRecord, RuntimeError (+33 more)

### Community 31 - "test_crm_search.py"
Cohesion: 0.21
Nodes (14): Core cross-cutting concerns: settings, security, schemas, guardrails, tracing., name_tokens(), UUID, query_tokens(), Tenant-keyed blind name prefixes; plaintext remains in encrypted columns only., token(), words(), keys() (+6 more)

### Community 32 - "Phase 5: Dashboard Frontend (Next.js)"
Cohesion: 0.04
Nodes (49): AdmitFlow — Task List, AIBoomi Startup Weekend session handoff (2026-10-22), Current direction and hackathon resources (2026-10-23), Final Postman diagnostic (October 23, executed; delivery blocked), Phase 1: Foundation, Phase 3: AI Core (Engine + RAG), Phase 4: Advanced Bot Features, Phase 5: Dashboard Frontend (Next.js) (+41 more)

### Community 33 - "management.py"
Cohesion: 0.12
Nodes (41): Any, get, Response, users(), require_admin(), archive_course(), archive_discount(), BatchInput (+33 more)

### Community 34 - "Code Standards"
Cohesion: 0.18
Nodes (11): Async & I/O, Code Standards, Configuration — settings, not literals, Dependencies, Errors, Formatting, LLM calls, Logging & observability (+3 more)

### Community 35 - "outreach/followups.py"
Cohesion: 0.12
Nodes (28): load_memory(), activity(), after_send(), before_send(), Check, course_available(), eligible(), generate_hook() (+20 more)

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
Nodes (27): Dashboard access role (SPEC — admin vs agent)., StaffRole, A dashboard user (admin or agent) belonging to one institution., StaffUser, main(), provision(), Manually provision an institution administrator without printing credentials., admin_scope() (+19 more)

### Community 41 - "send_message"
Cohesion: 0.36
Nodes (10): active_request(), Any, AsyncSession, Db, post, UUID, require_takeover(), resume() (+2 more)

### Community 42 - "Hackathon resources for AdmitFlow"
Cohesion: 0.20
Nodes (10): Acceptance before using a resource, Event and release boundaries, Goal, Hackathon resources for AdmitFlow, October 23 Downloads guide: hosted inference access, Participant credits and other support, Suggested allocation and activation order, Useful resources mapped to the plan (+2 more)

### Community 43 - "manifest.json"
Cohesion: 0.20
Nodes (9): SPEC.md, bytes, sha256, tasks/plan.md, bytes, sha256, tasks/todo.md, bytes (+1 more)

### Community 44 - "test_workspace_limits.py"
Cohesion: 0.12
Nodes (15): ASGIApp, Reject oversized multipart streams before they can fill temporary storage., UploadBodyLimit, check_login_limit(), Request, MonkeyPatch, Bound resource use and reject browser cross-origin mutations before database…, test_custom_header_and_origin_required() (+7 more)

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

### Community 49 - "integration/test_followups.py"
Cohesion: 0.13
Nodes (23): age(), callback(), outreach(), fixture, parametrize, Real database consent, reminder leases, freshness, delivery and the two-message…, seed(), test_budget_pause_does_not_spend_a_reminder_and_stop_cancels_it() (+15 more)

### Community 50 - "ADR-011: Required OpenAI passage reranking"
Cohesion: 0.40
Nodes (4): ADR-011: Required OpenAI passage reranking, Decision, Separate retrieval work, Verification and tradeoffs

### Community 51 - "Testing"
Cohesion: 0.22
Nodes (9): Browser announcement regions, Coverage, LLM and decision-layer tests, Philosophy — pragmatic TDD, Running tests, Test layout, Testing, The two patterns (+1 more)

### Community 52 - "guardrails.py"
Cohesion: 0.09
Nodes (34): apply_whatsapp_formatting(), check_input_safety(), check_output_safety(), _deterministic_check(), InputGuardrailResult, LLMGuardrailResponse, LLMOutputGuardrailResponse, OutputGuardrailResult (+26 more)

### Community 53 - "AdmitFlow project handoff"
Cohesion: 0.25
Nodes (8): AdmitFlow project handoff, Current direction, Development rules, Event submission, Execution checkpoint, First usable release, Historical evidence, Resume prompt

### Community 54 - "unittest_mock"
Cohesion: 0.18
Nodes (16): detect_intent(), Classify the user's intent to route to the correct node. Design Decision: If a…, asyncio, Test routing for course discovery., Test routing for knowledge questions., Test routing for qualification answers., Test routing for human handoff., Test routing for empty messages without calling LLM defaults to discovery. (+8 more)

### Community 55 - "hash_phone"
Cohesion: 0.10
Nodes (21): EncryptionKeyNotConfiguredError, hash_phone(), RuntimeError, Raised when a PII helper is used but its key is unset in settings., Return a deterministic keyed hash of a phone number for lookup/dedup. Keyed…, DatabaseNotConfiguredError, RuntimeError, Raised when a DB session is requested but ``DATABASE_URL`` is unset. (+13 more)

### Community 56 - "RuleOperator"
Cohesion: 0.18
Nodes (17): Qualification-rule comparison operators (SPEC §7.4). Evaluated…, RuleOperator, ExtractionResponse, BaseModel, Qualification Node (Task 15). Extracts rule fields using the LLM and runs…, Structured output expected from the LLM when extracting fields., _coerce_values(), evaluate_rule() (+9 more)

### Community 57 - "test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment"
Cohesion: 0.19
Nodes (10): payments(), Any, get, Any, MonkeyPatch, test_absent_link_does_not_clear_uncertainty_or_authorize_retry(), test_known_configuration_failure_can_only_requeue_same_bounded_invoice(), test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment() (+2 more)

### Community 58 - "copilot.py"
Cohesion: 0.07
Nodes (38): Cursor, Any, AsyncSession, BaseModel, datetime, field_validator, UUID, Bounded chronological transcript across inbound, replies and standalone… (+30 more)

### Community 59 - "ADR-010: Triage Fallback Routing (Anti-Spam)"
Cohesion: 0.33
Nodes (5): ADR-010: Triage Fallback Routing (Anti-Spam), Consequences, Context, Decision, Status

### Community 60 - "ADR-012: Telegram and OpenAI for the first complete admissions MVP"
Cohesion: 0.29
Nodes (7): ADR-012: Telegram and OpenAI for the first complete admissions MVP, Consequences, Context, Decision, Implemented runtime boundaries, References and verification, Supersession and preserved decisions

### Community 61 - "signin"
Cohesion: 0.09
Nodes (33): test_local_cohort_counts_conversions_and_observed_stages(), test_tenant_is_derived_from_session_and_period_is_bounded(), test_zero_filled_weekly_buckets_and_empty_rates(), test_downloads_roles_datasets_limits_and_tenants(), changed(), Any, Real database management: administrator writes, role/tenant boundaries and…, test_catalog_writes_validate_rules_capacity_and_ownership() (+25 more)

### Community 63 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 64 - "auth.py"
Cohesion: 0.08
Nodes (44): change_password(), hash_password(), issue_session(), Login, logout(), me(), PasswordChange, AsyncSession (+36 more)

### Community 65 - "Lead"
Cohesion: 0.19
Nodes (16): Lead, A prospective applicant with optional phone contact and channel identities.…, action(), application_action(), collect_application(), prompt(), Any, AsyncSession (+8 more)

### Community 66 - "staff/payments.py"
Cohesion: 0.53
Nodes (9): locked(), owned(), provider(), Db, post, UUID, Scoped payment monitoring and explicit, read-only provider reconciliation., reconcile() (+1 more)

### Community 67 - "api.py"
Cohesion: 0.19
Nodes (18): documents(), get_upload(), Any, BaseModel, Db, delete, get, post (+10 more)

### Community 68 - "process_upload"
Cohesion: 0.20
Nodes (19): Document, An uploaded document in the institution's knowledge base., extract_file(), ExtractionError, ValueError, Bounded extraction of institution reference documents; never execute uploads., A safe, public error code rather than parser output containing document text., validate_path() (+11 more)

### Community 70 - "RazorpayClient"
Cohesion: 0.11
Nodes (21): AsyncBaseTransport, PaymentLink, PaymentProviderError, Exception, field_validator, Bounded Razorpay requests; ambiguous link creation is never blindly retried., Read an existing exact reference; absence never authorizes another creation., RazorpayClient (+13 more)

### Community 71 - "Official source snapshots"
Cohesion: 0.50
Nodes (4): Conflicts to confirm, October 23 planning refresh, Official source snapshots, Sources

### Community 72 - "get_sessionmaker"
Cohesion: 0.12
Nodes (23): async_sessionmaker, AsyncEngine, get_engine(), get_session(), get_sessionmaker(), AsyncSession, Return the process-wide async engine (one pool for the app)., Return the process-wide async session factory. (+15 more)

### Community 73 - "test_application_journey.py"
Cohesion: 0.11
Nodes (25): Event, BaseModel, Channel-neutral input and validated plain-text reply boundary., cancel_queued(), note_inbound(), preference_reply(), Any, AsyncSession (+17 more)

### Community 74 - "Reply"
Cohesion: 0.08
Nodes (36): Trusted bot-to-institution mapping; token is application-encrypted., TelegramBot, Reply, Telegram transport and tenant-scoped identity helpers., Any, MonkeyPatch, test_outbound_dedup_claims_order_and_uncertainty(), deliver() (+28 more)

### Community 75 - "budget.py"
Cohesion: 0.15
Nodes (23): day_window(), local_counts(), Any, datetime, UUID, Atomic daily send-attempt budgets shared by every Telegram delivery path., Count confirmed deliveries once; a stats failure must not repeat a sent message., record_sent() (+15 more)

### Community 76 - "management.tsx"
Cohesion: 0.10
Nodes (13): blank, Discount, Discounts(), Batch, Course, empty, Management(), operators (+5 more)

### Community 77 - "pg_url"
Cohesion: 0.19
Nodes (14): _alembic_config(), monkeypatch_session(), pg_url(), fixture, MonkeyPatch, Start Postgres, point settings at it, yield the asyncpg URL., The tier requirement: alembic upgrade head then downgrade base, both clean., test_migration_applies_up_and_down() (+6 more)

### Community 78 - "AdmitFlow Backend"
Cohesion: 0.11
Nodes (17): Admissions analytics, AdmitFlow Backend, Application payments, Configuration, Consented follow-up reminders, Current implementation and verification, Institution knowledge workspace, Local development (+9 more)

### Community 79 - "dispatcher.py"
Cohesion: 0.13
Nodes (19): _flush_engine_state(), handle_turn(), _load_engine_state(), Any, AsyncSession, Engine Dispatcher (Task 8 & 17). This module contains the main entry point for…, Load EngineState from DB records., Flush mutations back to DB records. (+11 more)

### Community 84 - "analytics.tsx"
Cohesion: 0.28
Nodes (7): Analytics(), Conversion, labels, frontend_app_analytics_module, rate(), Report, shortDate()

### Community 89 - "configured_keys"
Cohesion: 0.33
Nodes (7): configured_keys(), fixture, MonkeyPatch, Point ``security.get_settings`` at settings with the crypto keys set., Point ``security.get_settings`` at settings with no crypto keys., test_hash_phone_differs_per_pepper_key(), unset_keys()

### Community 90 - "AdmitFlow"
Cohesion: 0.33
Nodes (6): AdmitFlow, Current status, Demonstration and submission, Development, Product scope, Stack

### Community 91 - "models/__init__.py"
Cohesion: 0.10
Nodes (49): Base, IdMixin, Declarative base shared by every AdmitFlow model., UUID primary key with an application-side default. UUIDs avoid cross-tenant…, Server-side created/updated timestamps., Row-level tenant scoping (ADR-003). Mixed into every tenant-scoped table., TenantMixin, TimestampMixin (+41 more)

### Community 92 - "tests/test_telegram_identity.py"
Cohesion: 0.29
Nodes (3): parametrize, Telegram identities must be independent of phone numbers and tenant-bound., test_private_chat_identity_rejects_invalid_identifiers()

### Community 93 - "test_decision_reranking.py"
Cohesion: 0.24
Nodes (15): chunks(), Intent, asyncio, BaseModel, MonkeyPatch, parametrize, UUID, Typed OpenAI decisions and bounded, tenant-safe evidence ranking. (+7 more)

### Community 94 - "crm.py"
Cohesion: 0.18
Nodes (15): normalized_phone(), lead_statement(), LeadFilters, LeadSearch, BaseModel, Select, UUID, Shared bounded CRM filters; search values never belong in URLs or audit details. (+7 more)

### Community 95 - "evaluate_faq.py"
Cohesion: 0.29
Nodes (11): Case, cases(), evaluate(), main(), BaseModel, Bounded live FAQ evaluation on the fictional demo tenant; no messages or writes., score_answer(), Evaluation rejects irrelevant quotations and does not count provider errors as… (+3 more)

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
Cohesion: 0.21
Nodes (5): ref_node_child_process, ref_node_crypto, ref_node_fs, ref_node_path, @playwright/test

### Community 100 - "AGENTS.md"
Cohesion: 0.25
Nodes (7): AIBoomi Startup Weekend handoff, How we build — read the handbook, Knowledge graph, Quick commands (from `backend/`), The rules you cannot skip, What this project is, Workflow triggers

### Community 101 - "Security & Production Readiness"
Cohesion: 0.18
Nodes (11): Dependency & secret scanning, Deploy & rollback, External surfaces, Guardrails & money, Local full-stack (docker-compose), Multi-tenancy — isolation is a correctness bug if wrong, Observability, PII & data protection (DPDPA) (+3 more)

### Community 102 - "validate_services.py"
Cohesion: 0.28
Nodes (8): argparse, embed_chunks(), Use the configured OpenAI model with the database's explicit 1536 dimensions., main(), Probe, BaseModel, Bounded live checks; print sanitized results without credentials or update…, validate()

### Community 103 - "next-env.d.ts"
Cohesion: 0.50
Nodes (3): NOTE: This file should not be edited, frontend_next_types_root_params_d, frontend_next_types_routes_d

### Community 104 - "payments/webhook.py"
Cohesion: 0.19
Nodes (14): LinkEntity, LinkEnvelope, PaidEvent, PaidPayload, payment_webhook(), PaymentEntity, PaymentEnvelope, BaseModel (+6 more)

### Community 105 - "test_rag_node.py"
Cohesion: 0.20
Nodes (12): Sanitizer to prevent RAG poisoning. Blocks chunks that contain obvious prompt…, sanitize_chunks(), process_rag_node(), AsyncSession, RAG Node (Task 14). Graph node that retrieves from the knowledge base and…, Retrieve context and answer knowledge questions., asyncio, patch (+4 more)

### Community 106 - "layout.tsx"
Cohesion: 0.25
Nodes (5): frontend_app_globals, metadata, config, @fontsource-variable/dm-sans, next

### Community 108 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, lint, record:demo, start, test:e2e:live, typecheck

### Community 109 - "backend/README.md"
Cohesion: 0.13
Nodes (12): Outbound integrations and live notifications, Staff access and privacy operations, Typed OpenAI decisions and required reranking, Configuration and data services, Delivery budget operation, Local Telegram/OpenAI runtime, Migrate and seed, Optional reminders and scheduler (+4 more)

### Community 110 - "AdmitFlow pitch deck copy"
Cohesion: 0.29
Nodes (7): AdmitFlow pitch deck copy, Slide 1: AdmitFlow, Slide 2: The admissions inquiry, Slide 3: A working student journey, Slide 4: Institution knowledge and control, Slide 5: Technology and verification, Slide 6: Pilot and next steps

### Community 111 - "add_institution_knowledge_workspace_b627da2f7e11.py"
Cohesion: 0.40
Nodes (4): Column, DateTime, _timestamps(), upgrade()

### Community 112 - "typing"
Cohesion: 0.08
Nodes (30): asyncio, OutboundMessage, Code-owned application fees and authenticated Razorpay payment processing., enqueue_outbound(), AsyncSession, fixture, workspace(), A student must confirm a fresh code-owned fee quote; retries cannot create… (+22 more)

### Community 113 - "sqlalchemy"
Cohesion: 0.10
Nodes (37): alembic_config, Audit-log write helper. :func:`write_audit_log` is the one path significant…, Declarative base, metadata naming convention, and shared column mixins. Every…, ApplicationStatus, DiscountType, Enumerated types used across the schema. These are Python ``str`` enums mapped…, How a discount code reduces the fee., Application review status (SPEC §7.9 / lifecycle). (+29 more)

### Community 114 - "Quality Gates — Definition of Done"
Cohesion: 0.33
Nodes (6): CI mirrors this exactly, Fast iteration vs the gate, Quality Gates — Definition of Done, The baseline gate (every change), The enforced-numbers ledger, The tiers — add gates by what the change touches

### Community 115 - "DocumentChunk"
Cohesion: 0.24
Nodes (11): DocumentChunk, A chunk of a document, with its embedding for vector search., PassageRanking, BaseModel, UUID, Bounded OpenAI evidence reranking with a validated baseline fallback., Reorder only original, safe tenant candidates; never invent text or sources.…, rerank() (+3 more)

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
Nodes (16): dispatch_pending(), dispatch_due(), recover_payments(), Local operational commands with secrets entered through protected prompts., main(), Produce due reminder jobs and recover queued deliveries; safe to run after…, run(), purge_retained() (+8 more)

### Community 120 - "re"
Cohesion: 0.21
Nodes (11): escalation_reason(), office_open(), datetime, Reason, Deterministic clear support signals and institution-local office hours., parametrize, Clear support signals escalate; office hours never promise an immediate reply., test_clear_escalation_signals() (+3 more)

### Community 121 - "README.md"
Cohesion: 0.14
Nodes (11): AI Impact Statement, Student-to-staff demonstration, Current templates, Language review packet, Live exercise, Reminder consent and outreach copy, Prior-work disclosure draft, AdmitFlow submission requirements (+3 more)

### Community 122 - "knowledge/processing.py"
Cohesion: 0.24
Nodes (8): dispatch_pending(), UUID, Durable upload claims, bounded embedding and atomic publication of ready…, A database-backed inbox survives enqueue failures and lost worker leases., recovery_loop(), ingest_upload(), task, TaskIQ entry point for institution document indexing.

### Community 123 - "reindex_names.py"
Cohesion: 0.36
Nodes (7): main(), AsyncSession, UUID, Backfill encrypted lead names from latest submitted forms and rebuild blind…, reindex_batch(), test_index_rename_clear_and_legacy_backfill(), exercise()

### Community 124 - "WhatsApp readiness check — October 22, 2026"
Cohesion: 0.15
Nodes (13): Decision so far, Delivery diagnosis and configuration repair (October 23, approximately 00:16 IST), Evidence collected before configuration, Final Postman retry (October 23), Live checkpoint (approximately 22:54 IST), Missing-reply investigation (approximately 22:59 IST), New test account configuration (October 23, approximately 09:45 IST), Next live checks and evidence required (+5 more)

### Community 125 - "write_audit_log"
Cohesion: 0.13
Nodes (21): CRM search and institution downloads, Any, AsyncSession, UUID, Record persisted ORM transitions atomically; never infer an earlier stage., Append one entry to ``audit_logs`` on ``session``; return it flushed, not…, record_stage_changes(), write_audit_log() (+13 more)

### Community 126 - "erase_inquiry"
Cohesion: 0.27
Nodes (10): erase(), erase_inquiry(), EraseRequest, in_flight(), AsyncSession, BaseModel, Db, delete (+2 more)

### Community 127 - "test_english_query_does_not_call_model"
Cohesion: 0.40
Nodes (3): MonkeyPatch, test_english_query_does_not_call_model(), test_non_ascii_query_uses_validated_translation()

### Community 128 - "payments.tsx"
Cohesion: 0.32
Nodes (6): label(), money(), outcomes, Payment, Payments(), statuses

### Community 129 - "test_expired_lease_recovery_cap_and_configuration_cancellation"
Cohesion: 0.13
Nodes (13): configure(), event_for(), test_configuration_roles_encryption_and_tenant_ownership(), inspect(), test_delivery_claim_retry_and_minimal_payload(), exercise(), test_expired_lease_recovery_cap_and_configuration_cancellation(), exercise() (+5 more)

### Community 130 - "react"
Cohesion: 0.40
Nodes (5): StaffAccounts(), create(), mutate(), User, react

### Community 131 - "Knowledge"
Cohesion: 0.46
Nodes (8): refresh(), api(), Knowledge(), action(), login(), search(), upload(), send()

### Community 132 - "json"
Cohesion: 0.11
Nodes (16): log_delivery_status(), Request, Response, Expose only the existing Meta webhook through the temporary demo tunnel., Observe only authenticated status events, without recipient or error text., Five bounded live embedding searches through the real authenticated staff API., Hash the tested code/configuration without reading secrets or runtime data., parametrize (+8 more)

### Community 133 - "env.py"
Cohesion: 0.22
Nodes (9): do_run_migrations(), Connection, Alembic migration environment (async). Reads the database URL from application…, Emit SQL to stdout without a live DB connection., Run migrations against a live database via an async engine., run_migrations_offline(), run_migrations_online(), logging_config (+1 more)

### Community 135 - "test_knowledge_workspace.py"
Cohesion: 0.11
Nodes (23): decrypt_bytes(), Authenticate and decrypt source bytes for an authorized ingestion task., Institution document extraction, durable ingestion and retrieval., fake_embeddings(), Any, MonkeyPatch, Real PostgreSQL acceptance for authenticated uploads and atomic semantic…, readable_pdf() (+15 more)

### Community 136 - "process_payment"
Cohesion: 0.28
Nodes (7): process_payment(), task, Encrypted outbound-message delivery jobs carry only internal identifiers., send_outbound_message(), create_payment_link(), task, Payment-link creation runs after the requesting conversation transaction…

### Community 137 - "page.tsx"
Cohesion: 0.12
Nodes (11): DeliveryBudget(), Usage, Exports(), Configuration, Integrations(), Request, Doc, errors (+3 more)

### Community 138 - "index_known_name"
Cohesion: 0.40
Nodes (5): index_known_name(), Connection, Mapper, Keep index updates atomic with encrypted names, including name removal., listens_for

### Community 139 - "configure"
Cohesion: 0.28
Nodes (9): configuration(), configure(), EndpointInput, Any, BaseModel, Db, get, put (+1 more)

### Community 140 - "13. Dashboard Features"
Cohesion: 0.22
Nodes (9): 13.1 Authentication, 13.2 Roles & Permissions, 13.3 UI Aesthetic, 13.4 Real-Time Notifications, 13.5 Funnel Analytics, 13.6 Data Export & Integration, 13.7 Document Management (RAG), 13.8 Onboarding (MVP) (+1 more)

### Community 141 - "test_worker_broker.py"
Cohesion: 0.25
Nodes (7): Tests for the TaskIQ broker setup and task execution (Task 3). All tests run…, When REDIS_URL is unset the factory should yield an InMemoryBroker., The ping task should run and return the expected payload., Ping without an explicit payload should default to 'pong'., test_broker_is_in_memory_without_redis_url(), test_ping_task_default_payload(), test_ping_task_returns_result()

### Community 144 - "Phase 3–4 addition (see ADR-008)"
Cohesion: 0.29
Nodes (7): Phase 3–4 addition (see ADR-008), Task 40: `decide()` System-1 decision-layer abstraction, Task 41: Distill decisions into self-hosted Laya (post-demo), Task 42.1: Complex Document Parsing & Semantic Chunking, Task 42.2: Contextual Query Rewriting, Task 42.3: Pluggable Reranker (Cohere API vs Local), Task 42: Advanced RAG Strategy (ADR-011)

### Community 146 - ".__call__"
Cohesion: 0.33
Nodes (4): private_send(), Receive, Scope, Send

### Community 147 - "notifications.tsx"
Cohesion: 0.33
Nodes (4): labels, Notice, Notifications(), Snapshot

### Community 148 - "hash_telegram_identifier"
Cohesion: 0.40
Nodes (5): hash_telegram_identifier(), UUID, Private Telegram identity lookup without storing raw identifiers in indexes., Hash an identifier in its tenant/bot/type domain using the lookup secret. This…, identity()

### Community 149 - "Implementation Plan: AdmitFlow"
Cohesion: 0.40
Nodes (4): Architecture Decisions, Implementation Plan: AdmitFlow, Overview, Risks and Mitigations

### Community 150 - "add_conversation_runtime_714f092da3b8.py"
Cohesion: 0.50
Nodes (3): columns(), Column, upgrade()

### Community 151 - "durable_payments_outbound_f129a064c5e8.py"
Cohesion: 0.50
Nodes (3): common(), Column, upgrade()

### Community 152 - "11. Human-in-the-Loop (Full Workflow)"
Cohesion: 0.40
Nodes (5): 11.1 Auto-Escalation Triggers, 11.2 Co-pilot Mode, 11.3 Business Hours, 11.4 Never Escalate, 11. Human-in-the-Loop (Full Workflow)

### Community 153 - "record-demo.mjs"
Cohesion: 0.40
Nodes (4): credentials, headers, journey, target

### Community 155 - "mock_settings"
Cohesion: 0.50
Nodes (4): mock_settings(), fixture, MonkeyPatch, Ensure all three models are configured for fallback testing.

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

### Community 163 - "migrated_db"
Cohesion: 0.67
Nodes (3): migrated_db(), fixture, Start Postgres, point settings at it, migrate to head; tear down after.

### Community 165 - "17. Decisions & Open Questions"
Cohesion: 0.67
Nodes (3): 17.1 Conversation engine — DECIDED: hand-rolled dispatcher, 17.2 Still open, 17. Decisions & Open Questions

## Knowledge Gaps
- **410 isolated node(s):** `admitflow-backend`, `fs`, `path`, `crypto`, `root` (+405 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1109 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CRM search and institution downloads` connect `write_audit_log` to `test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment`, `leads.py`, `backend/README.md`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Why does `LeadStatus` connect `LeadStatus` to `test_expired_lease_recovery_cap_and_configuration_cancellation`, `leads.py`, `pydantic`, `journey.py`, `encrypt_pii`, `PaymentStatus`, `exports.py`, `test_integrations_notifications.py`, `outreach/followups.py`, `analytics`, `send_message`, `integration/test_followups.py`, `RuleOperator`, `Lead`, `get_sessionmaker`, `test_application_journey.py`, `Reply`, `dispatcher.py`, `models/__init__.py`, `crm.py`, `payments/webhook.py`, `test_rag_node.py`, `typing`, `sqlalchemy`, `write_audit_log`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `write_audit_log()` connect `write_audit_log` to `test_expired_lease_recovery_cap_and_configuration_cancellation`, `leads.py`, `journey.py`, `process_payment`, `configure`, `PaymentStatus`, `exports.py`, `Course`, `test_integrations_notifications.py`, `telegram/service.py`, `Phase 5: Dashboard Frontend (Next.js)`, `management.py`, `outreach/followups.py`, `analytics`, `StaffUser`, `send_message`, `test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment`, `copilot.py`, `auth.py`, `Lead`, `staff/payments.py`, `api.py`, `process_upload`, `get_sessionmaker`, `test_application_journey.py`, `models/__init__.py`, `crm.py`, `payments/webhook.py`, `sqlalchemy`, `update`, `knowledge/processing.py`, `erase_inquiry`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `encrypt_pii()` (e.g. with `Consequences` and `Decision`) actually correct?**
  _`encrypt_pii()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 54 inferred relationships involving `LeadStatus` (e.g. with `record_stage_changes()` and `Lead`) actually correct?**
  _`LeadStatus` has 54 INFERRED edges - model-reasoned connections that need verification._
- **What connects `admitflow-backend`, `fs`, `path` to the rest of the system?**
  _410 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `pydantic` be split into smaller, more focused modules?**
  _Cohesion score 0.07682926829268293 - nodes in this community are weakly interconnected._