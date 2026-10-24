# Graph Report - admitflow  (2026-10-24)

## Corpus Check
- 368 files · ~208,197 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 7, .example 2, .css 2)

## Summary
- 3126 nodes · 9216 edges · 183 communities (167 shown, 16 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 584 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6a36962a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ADR-008: System-1 Decision Layer (Laya / Jev)
- Conversation Engine (hand-rolled dispatcher)
- AdmitFlow Complete Specification
- Finalized Production Stack
- journey.py
- analytics.py
- payments/service.py
- deliver
- RedisMutex
- knowledge/processing.py
- replace_demo_catalogue.py
- staff/integrations.py
- WhatsAppSender
- core/rag.py
- PII Encryption & Audit Log
- Razorpay Payment Integration
- Settings
- admissions.tsx
- contextual_query
- GuidanceMemory
- AIBoomi Startup Weekend Kochi: fresh-session context
- GuidanceDecision
- office_open
- text
- hash_phone
- Stages
- signin
- test_webhook.py
- run_postman_check.cjs
- Task List
- scope.py
- leads.py
- test_crm_search.py
- management.py
- Code Standards
- Local Telegram/OpenAI runtime
- Event preparation and execution plan
- 7. Core Feature Specifications
- session.py
- main.py
- Event
- get_settings
- Hackathon resources for AdmitFlow
- manifest.json
- accounts.py
- AdmitFlow: current state and planning baseline
- AdmitFlow: AIBoomi submission plan
- AdmitFlow — Complete Specification
- normalize_e164
- Course
- ADR-011: Required OpenAI passage reranking
- Testing
- check_input_safety
- AdmitFlow project handoff
- detect_intent
- tests/test_telegram_identity.py
- live
- provision_staff.py
- LeadStatus
- ADR-010: Triage Fallback Routing (Anti-Spam)
- ADR-012: Telegram and OpenAI for the first complete admissions MVP
- exports.py
- 2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md
- compilerOptions
- auth.py
- age
- ADR-016: Public programme references and an explicit local demo reset
- api.py
- decide
- AllProvidersFailedError
- ._post
- Official source snapshots
- integration/test_followups.py
- fixture
- ADR-013: Adaptive, student-first course guidance
- tests/test_followups.py
- management.tsx
- ADR-015: Supportive guidance and contextual answer controls
- guidance.py
- PublicCatalogue
- verify.sh
- db/__init__.py
- src/__init__.py
- tasks/__init__.py
- analytics.tsx
- whatsapp/__init__.py
- integration/__init__.py
- admitflow-backend
- get_sessionmaker
- AdmitFlow
- Phase 3: AI Core (Engine + RAG)
- AdmitFlow Backend
- test_decision_reranking.py
- reindex_names.py
- pydantic
- Git & GitHub Workflow
- package.json
- erase_inquiry
- @playwright/test
- AGENTS.md
- Security & Production Readiness
- send
- next-env.d.ts
- identity_database
- send_outbound
- layout.tsx
- frontend/AGENTS.md
- scripts
- backend/README.md
- Reply
- ExtractionError
- sqlalchemy
- models/__init__.py
- Quality Gates — Definition of Done
- test_rag_node.py
- devDependencies
- applications.tsx
- dependencies
- dispatcher.py
- encrypt_pii
- outreach/followups.py
- tests/test_conversation_readiness.py
- hashlib
- WhatsApp readiness check — October 22, 2026
- test_faq_evaluation.py
- unittest_mock
- confirmation.py
- payments.tsx
- evaluate_faq.py
- Adaptive course guidance: evidence and implementation
- Knowledge
- telegram/service.py
- env.py
- timeline
- TelegramBot
- prepare
- page.tsx
- test_shared_budget_preserves_queues_and_settings_wake_deliveries
- BaseModel
- RuleOperator
- pg_url
- generate
- add_institution_knowledge_workspace_b627da2f7e11.py
- Code Owns the Money
- seed
- TelegramClient
- notifications.tsx
- Q: Retrieve relevant passages Rerank supporting evidence Validate supporting quotation Grounded answer or abstention: what are the 3 steps for validate supporting quotation?
- send_message
- Q: What is the validate supporting quotation step for? Explain it.
- Q: How did AdmitFlow validate the supporting quotation?
- integration/conftest.py
- record-demo.mjs
- durable_payments_outbound_f129a064c5e8.py
- Check
- Phase 4: Advanced Bot Features
- staff/payments.py
- One final WhatsApp check with Postman
- Phase 3–4 addition (see ADR-008)
- AdmitFlow — Task List
- index_known_name
- ADR-017: Explicit demo applications for public-reference courses
- WhatsApp readiness check (2026-10-22, in progress)
- AdmitFlow pitch deck
- Workspace colour theme
- Phase 5: Dashboard Frontend (Next.js)
- test_payment_and_webhook_claims_wait_for_erasure_lock
- Language review packet
- Q: what you need to is explain me the webpage build and every feature in it
- Q: what is the outbound webhooks for
- Q: what about observbility
- RazorpayClient
- Q: Prepare a three-minute jury pitch and Q&A using a five-stage story arc, customer pain points, solution and impact.
- Q: What you need to do is i need to present the this project before the jury. First explain the overall structure the stack what things used where used . From A to Z things. that i can answer anything if they question.
- write_audit_log
- ADR-014: Natural collection, context reset and responsive replies
- test_worker_broker.py
- AdmitFlow submission requirements
- AdmitFlow execution and demonstration checklist
- DOCUMENT_REVIEW.md
- ExtractionResponse
- DEMO_SCRIPT.md

## God Nodes (most connected - your core abstractions)
1. `encrypt_pii()` - 120 edges
2. `Reply` - 107 edges
3. `write_audit_log()` - 104 edges
4. `get_settings()` - 102 edges
5. `LeadStatus` - 102 edges
6. `TelegramBot` - 100 edges
7. `Lead` - 98 edges
8. `Course` - 91 edges
9. `decrypt_pii()` - 89 edges
10. `route()` - 82 edges

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

## Communities (183 total, 16 thin omitted)

### Community 0 - "ADR-008: System-1 Decision Layer (Laya / Jev)"
Cohesion: 0.18
Nodes (17): ADR-001: Hybrid Architecture, ADR-004: Dual Memory Architecture, Episodic Memory (messages table), Semantic Memory (lead_facts table), ADR-005: Three-Layer Guardrails and RAG, Three-Layer Guardrails, ADR-007: Finalized Production Stack, ADR-008: System-1 Decision Layer (Laya / Jev) (+9 more)

### Community 1 - "Conversation Engine (hand-rolled dispatcher)"
Cohesion: 0.25
Nodes (8): Conversation Engine (hand-rolled dispatcher), System-1 decide() Decision Layer, FastAPI WhatsApp Webhook, Langfuse LLM Tracing, pgvector RAG Pipeline, Redis (mutex / dedup / rate-limit), TaskIQ Background Worker, Three-Layer Guardrails

### Community 2 - "AdmitFlow Complete Specification"
Cohesion: 0.19
Nodes (9): AI Impact Statement, Data, model and asset provenance, Prior-work disclosure, AdmitFlow necessary resources, Planning baseline before Telegram alignment, AdmitFlow Complete Specification, AdmitFlow Platform, AdmitFlow Implementation Plan (+1 more)

### Community 3 - "Finalized Production Stack"
Cohesion: 0.18
Nodes (11): ADR-002: Webhook Concurrency and Deduplication, Per-Phone Redis Mutex, Webhook Deduplication (Redis SETNX), ADR-003: Multi-Tenancy Strategy, Multi-Tenancy (Row-Level Isolation), Finalized Production Stack, Fly.io (Backend + Worker + Scheduler), Langfuse Cloud (LLM Tracing) (+3 more)

### Community 4 - "journey.py"
Cohesion: 0.13
Nodes (51): Lead, A prospective applicant with optional phone contact and channel identities.…, escalation_reason(), Reason, catalog(), commit_guidance(), guide(), load_guidance() (+43 more)

### Community 5 - "analytics.py"
Cohesion: 0.08
Nodes (44): alias, analytics(), bucket_dates(), count(), percent(), Period, period_window(), Any (+36 more)

### Community 6 - "payments/service.py"
Cohesion: 0.14
Nodes (28): ApplicationStatus, PaymentStatus, Payment order lifecycle (SPEC §7.10)., Application review status (SPEC §7.9 / lifecycle)., discount_action(), order_reply(), payment_action(), preview() (+20 more)

### Community 7 - "deliver"
Cohesion: 0.10
Nodes (18): deliver(), UUID, task, Integration queue messages contain identifiers only., send_webhook(), configure(), event_for(), test_configuration_roles_encryption_and_tenant_ownership() (+10 more)

### Community 8 - "RedisMutex"
Cohesion: 0.07
Nodes (28): MutexAcquireError, Redis, RuntimeError, Redis distributed mutex with owner-safe release and keepalive (Task 7). Ensures…, Background loop that extends the TTL while the lock is held., Raised when the mutex cannot be acquired after all retries., Async context-manager mutex backed by Redis ``SET NX``. Parameters: redis: An…, Attempt to acquire the lock, retrying up to ``retry_count`` times. (+20 more)

### Community 9 - "knowledge/processing.py"
Cohesion: 0.12
Nodes (19): dispatch_pending(), embed_chunks(), process_upload(), UUID, Durable upload claims, bounded embedding and atomic publication of ready…, A database-backed inbox survives enqueue failures and lost worker leases., Use the configured OpenAI model with the database's explicit 1536 dimensions., Claim once, process outside the transaction, then publish only the current… (+11 more)

### Community 10 - "replace_demo_catalogue.py"
Cohesion: 0.14
Nodes (17): argparse, configure(), main(), run(), Opt a local reference catalogue into test-only demo applications without…, main(), run(), provision() (+9 more)

### Community 11 - "staff/integrations.py"
Cohesion: 0.09
Nodes (34): destination(), post_event(), PrivateTransportLogs, protect_logs(), public_ip(), LogRecord, HTTPS delivery pins a public resolved address while retaining TLS host…, resolve_public() (+26 more)

### Community 12 - "WhatsAppSender"
Cohesion: 0.12
Nodes (16): RuntimeError, WhatsApp message sending service (Task 6). Uses httpx2 to call the Meta Graph…, Raised when the Meta Cloud API returns an error response., Service for sending messages via Meta WhatsApp Cloud API., WhatsAppAPIError, WhatsAppSender, asyncio, Tests for the WhatsApp Message Sending Service (Task 6). The sender calls the… (+8 more)

### Community 13 - "core/rag.py"
Cohesion: 0.12
Nodes (22): chunk_text(), embed_text(), ingest_document(), Any, AsyncSession, UUID, RAG pipeline core logic (Task 13). Handles ingestion (chunking, embedding),…, Sanitizer to prevent RAG poisoning. Blocks chunks that contain obvious prompt… (+14 more)

### Community 16 - "Settings"
Cohesion: 0.11
Nodes (23): Environment-backed application configuration., Settings, parametrize, The temporary tunnel must not expose local debug or documentation routes., test_delivery_status_logs_are_authenticated_and_exclude_pii(), test_tunnel_app_exposes_no_other_routes(), test_tunnel_app_keeps_webhook_verification(), Tests for the settings singleton. (+15 more)

### Community 17 - "admissions.tsx"
Cohesion: 0.10
Nodes (19): Admissions(), Detail, Human, Inquiry, labels, Request, RuleEvidence, statusLabel() (+11 more)

### Community 18 - "contextual_query"
Cohesion: 0.13
Nodes (17): contextual_query(), Resolve pronouns/slang using bounded recent turns; uncertainty asks the…, retrieval_query(), evaluate(), main(), Bounded synthetic OpenAI reference resolution; no database writes or sends., MonkeyPatch, parametrize (+9 more)

### Community 19 - "GuidanceMemory"
Cohesion: 0.13
Nodes (42): GuidanceMemory, Note, merge_evidence(), render_decision(), test_optional_exploration_and_failure_do_not_erase_profile(), exercise(), turn(), exercise() (+34 more)

### Community 20 - "AIBoomi Startup Weekend Kochi: fresh-session context"
Cohesion: 0.11
Nodes (19): AIBoomi Startup Weekend Kochi: fresh-session context, Assessment and next decision, Current readiness session (October 22), Event sources and local copies, Existing prototype rule and surprise element, Existing working-tree changes, Fresh-message prompt, Handoff status (+11 more)

### Community 21 - "GuidanceDecision"
Cohesion: 0.09
Nodes (37): CourseMatch, GuidanceDecision, GuidanceInterpretation, InterestTheme, ProfileUpdate, BaseModel, Bounded exploratory guidance; evidence notes are not psychometric measurements., StrictModel (+29 more)

### Community 22 - "office_open"
Cohesion: 0.24
Nodes (8): office_open(), datetime, Deterministic clear support signals and institution-local office hours., parametrize, Clear support signals escalate; office hours never promise an immediate reply., test_clear_escalation_signals(), test_office_hours_use_institution_timezone_and_end_exclusive(), src_engine_escalation

### Community 23 - "text"
Cohesion: 0.20
Nodes (11): Staff takeover and reviewed co-pilot, download(), export_rows(), ExportRequest, Db, post, Response, text() (+3 more)

### Community 24 - "hash_phone"
Cohesion: 0.12
Nodes (19): EncryptionKeyNotConfiguredError, hash_phone(), RuntimeError, Raised when a PII helper is used but its key is unset in settings., Return a deterministic keyed hash of a phone number for lookup/dedup. Keyed…, seed(), test_hash_phone_differs_per_number(), test_hash_phone_is_deterministic() (+11 more)

### Community 25 - "Stages"
Cohesion: 0.13
Nodes (15): 10. Reflect & learn, 1. Understand & spec  (`/spec`), 2. Plan & pick a task  (`/plan`), 3. Branch, 4. Build with TDD  (`/build`, `/test`), 5. Verify (the quality gate), 6. Self-review, then adversarial review  (`/review`), 7. Commit & open the PR (+7 more)

### Community 26 - "signin"
Cohesion: 0.15
Nodes (18): analytics_data(), Analytics preserve tenant scope, local dates, real denominators and…, test_all_aggregates_share_a_snapshot_during_concurrent_arrivals(), interleave(), test_local_cohort_counts_conversions_and_observed_stages(), test_stage_audit_is_atomic_and_noop_updates_do_not_create_history(), exercise(), test_tenant_is_derived_from_session_and_period_is_bounded() (+10 more)

### Community 27 - "test_webhook.py"
Cohesion: 0.13
Nodes (13): app(), client(), mock_settings(), Any, FastAPI, TestClient, Tests for the Meta WhatsApp webhook endpoints (Task 5)., Statuses (read/delivered) have no 'messages' array. (+5 more)

### Community 28 - "run_postman_check.cjs"
Cohesion: 0.20
Nodes (8): collection, config, crypto, fs, keys, newman, path, root

### Community 29 - "Task List"
Cohesion: 0.15
Nodes (13): Checkpoint: Advanced Features, Checkpoint: AI Core, Checkpoint: Dashboard Complete, Checkpoint: Foundation, Checkpoint: Production Ready, Checkpoint: WhatsApp Ingress, Phase 1: Foundation, Phase 2: WhatsApp Ingress (+5 more)

### Community 30 - "scope.py"
Cohesion: 0.14
Nodes (16): AmbiguousCourseReference, AsyncSession, Course, UUID, ValueError, question_courses(), Code-owned course scopes for approved institution references., More than one active course has the requested name without a selected owner. (+8 more)

### Community 31 - "leads.py"
Cohesion: 0.17
Nodes (25): lead_statement(), lead_summary(), LeadFilters, LeadSearch, Any, BaseModel, Select, UUID (+17 more)

### Community 32 - "test_crm_search.py"
Cohesion: 0.20
Nodes (15): Core cross-cutting concerns: settings, security, schemas, guardrails, tracing., name_tokens(), normalized_phone(), UUID, query_tokens(), Tenant-keyed blind name prefixes; plaintext remains in encrypted columns only., token(), words() (+7 more)

### Community 33 - "management.py"
Cohesion: 0.20
Nodes (31): DiscountType, How a discount code reduces the fee., archive_course(), archive_discount(), catalog(), catalog_detail(), course_view(), CourseInput (+23 more)

### Community 34 - "Code Standards"
Cohesion: 0.18
Nodes (11): Async & I/O, Code Standards, Configuration — settings, not literals, Dependencies, Errors, Formatting, LLM calls, Logging & observability (+3 more)

### Community 35 - "Local Telegram/OpenAI runtime"
Cohesion: 0.25
Nodes (8): Configuration and data services, Delivery budget operation, Local Telegram/OpenAI runtime, Migrate and seed, Optional reminders and scheduler, Packaging and release limits, Run the processes, Validate and recover

### Community 36 - "Event preparation and execution plan"
Cohesion: 0.18
Nodes (11): Business and mentor preparation, Evaluation and demo evidence, Event preparation and execution plan, Kickoff disclosure draft, Latest direction (October 23), Minimum demonstrable product, Next action: one-hour v1 readiness check, Submission checklist (+3 more)

### Community 37 - "7. Core Feature Specifications"
Cohesion: 0.18
Nodes (11): 7.10 Payment Integration & Discounts (Razorpay), 7.1 WhatsApp Number Architecture, 7.2 Multi-Tenancy (Row-Level Isolation), 7.3 Lead Lifecycle States, 7.4 Course Qualification Rules (Structured), 7.5 Batch & Intake Management, 7.6 Cold Lead Re-engagement, 7.7 Language Support (+3 more)

### Community 38 - "session.py"
Cohesion: 0.04
Nodes (29): alembic, alembic_config, AsyncEngine, columns(), Column, upgrade(), DatabaseNotConfiguredError, get_engine() (+21 more)

### Community 39 - "main.py"
Cohesion: 0.08
Nodes (22): ASGIApp, recovery_loop(), UploadBodyLimit, private_send(), create_app(), lifespan(), FastAPI, FastAPI application entry point. Boots the API, manages the TaskIQ broker… (+14 more)

### Community 40 - "Event"
Cohesion: 0.09
Nodes (33): ConversationEvent, Event, BaseModel, model_history(), Any, AsyncSession, Bounded bulk model context; reset boundaries preserve the staff audit trail., Student-confirmed context reset is separate from deletion and institutional… (+25 more)

### Community 41 - "get_settings"
Cohesion: 0.06
Nodes (46): AsyncBroker, get_redis(), Redis, RuntimeError, Shared async Redis client for application code. Carry-over prerequisite #1: the…, Raised when Redis is needed but ``REDIS_URL`` is unset in settings., Return the process-wide async Redis client singleton. The client is created…, RedisNotConfiguredError (+38 more)

### Community 42 - "Hackathon resources for AdmitFlow"
Cohesion: 0.20
Nodes (10): Acceptance before using a resource, Event and release boundaries, Goal, Hackathon resources for AdmitFlow, October 23 Downloads guide: hosted inference access, Participant credits and other support, Suggested allocation and activation order, Useful resources mapped to the plan (+2 more)

### Community 43 - "manifest.json"
Cohesion: 0.20
Nodes (9): SPEC.md, bytes, sha256, tasks/plan.md, bytes, sha256, tasks/todo.md, bytes (+1 more)

### Community 44 - "accounts.py"
Cohesion: 0.15
Nodes (25): Dashboard access role (SPEC — admin vs agent)., StaffRole, admin_scope(), create_user(), CreateUser, edit_user(), EditUser, Any (+17 more)

### Community 45 - "AdmitFlow: current state and planning baseline"
Cohesion: 0.22
Nodes (9): AdmitFlow: current state and planning baseline, Confirmed user direction, Feature status and integration gaps, Features to finalize next, How to reconcile the planning documents, Proposed architecture for the next plan, Stack inventory, Verification evidence and its limits (+1 more)

### Community 46 - "AdmitFlow: AIBoomi submission plan"
Cohesion: 0.22
Nodes (9): AdmitFlow: AIBoomi submission plan, Deck and presentation, Open decisions, Proposed schedule from Friday evening, Submission outcome, The journey to demonstrate, Use the provided resources, What must be handed in (+1 more)

### Community 47 - "AdmitFlow — Complete Specification"
Cohesion: 0.04
Nodes (46): 10.1 LLM Tracing (Langfuse), 10.2 Structured Logging, 10.3 Error Monitoring (Sentry), 10. Observability & Tracing, 11.1 Auto-Escalation Triggers, 11.2 Co-pilot Mode, 11.3 Business Hours, 11.4 Never Escalate (+38 more)

### Community 48 - "normalize_e164"
Cohesion: 0.14
Nodes (10): InvalidPhoneError, normalize_e164(), ValueError, E.164 phone-number normalization. Carry-over prerequisite #3: un-normalized…, Raised when a phone string cannot be normalized to E.164., Normalize *raw* into canonical E.164 (``+<digits>``). Strips whitespace,…, Tests for E.164 phone normalization (carry-over prerequisite #3). The…, normalize_e164 → canonical E.164 string. (+2 more)

### Community 49 - "Course"
Cohesion: 0.13
Nodes (25): Batch, Course, QualificationRule, A program a lead can be qualified for and pay to apply to., A dated intake of a course with finite seats (SPEC §7.5)., A structured eligibility rule evaluated in code, not by the LLM (ADR-006).…, main(), Idempotent synthetic institution/catalog/staff seed; no real applicant data. (+17 more)

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
Cohesion: 0.15
Nodes (13): AdmitFlow project handoff, Current conversation work: Task 61, Current direction, Current work: Task 62 conversation continuity, Current work: Task 63 supportive adaptive guidance, Current work: Task 64 assistant-led routine inquiries, Current work: Task 65 JAIN Kochi data replacement, Development rules (+5 more)

### Community 54 - "detect_intent"
Cohesion: 0.20
Nodes (15): detect_intent(), Classify the user's intent to route to the correct node. Design Decision: If a…, asyncio, Test routing for course discovery., Test routing for knowledge questions., Test routing for qualification answers., Test routing for human handoff., Test routing for empty messages without calling LLM defaults to discovery. (+7 more)

### Community 55 - "tests/test_telegram_identity.py"
Cohesion: 0.15
Nodes (12): hash_telegram_identifier(), UUID, Hash an identifier in its tenant/bot/type domain using the lookup secret. This…, test_private_identities_are_encrypted_unique_and_tenant_bound(), exercise(), identity(), MonkeyPatch, parametrize (+4 more)

### Community 56 - "live"
Cohesion: 0.19
Nodes (13): Acknowledge, current(), live(), Any, AsyncSession, BaseModel, Db, get (+5 more)

### Community 57 - "provision_staff.py"
Cohesion: 0.25
Nodes (9): main(), provision(), Manually provision an institution administrator without printing credentials., hash_password(), parametrize, Staff passwords must be salted, bounded and verified in constant time., test_invalid_password_lengths_are_rejected(), test_passwords_are_salted_and_invalid_passwords_fail() (+1 more)

### Community 58 - "LeadStatus"
Cohesion: 0.10
Nodes (35): LeadStatus, Enumerated types used across the schema. These are Python ``str`` enums mapped…, Lead lifecycle states (SPEC §7.3). Where a lead *stands*, not a fixed track —…, Discovery Node (Task 12). Presents available courses as WhatsApp interactive…, AsyncSession, Qualification Node (Task 15). Extracts rule fields using the LLM and runs…, Run the qualification loop., run_qualification() (+27 more)

### Community 59 - "ADR-010: Triage Fallback Routing (Anti-Spam)"
Cohesion: 0.33
Nodes (5): ADR-010: Triage Fallback Routing (Anti-Spam), Consequences, Context, Decision, Status

### Community 60 - "ADR-012: Telegram and OpenAI for the first complete admissions MVP"
Cohesion: 0.29
Nodes (7): ADR-012: Telegram and OpenAI for the first complete admissions MVP, Consequences, Context, Decision, Implemented runtime boundaries, References and verification, Supersession and preserved decisions

### Community 61 - "exports.py"
Cohesion: 0.19
Nodes (14): clean(), Audited institution exports, with explicit limits and spreadsheet-safe text., render_csv(), render_xlsx(), crm_data(), Real database CRM lookup, index maintenance, export roles and isolation., test_downloads_roles_datasets_limits_and_tenants(), test_search_scope_validation_and_audit() (+6 more)

### Community 62 - "2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md"
Cohesion: 0.25
Nodes (4): Architecture Decisions, Implementation Plan: AdmitFlow, Overview, Risks and Mitigations

### Community 63 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 64 - "auth.py"
Cohesion: 0.16
Nodes (25): change_password(), issue_session(), Login, logout(), me(), PasswordChange, AsyncSession, BaseModel (+17 more)

### Community 65 - "age"
Cohesion: 0.14
Nodes (14): age(), outreach(), parametrize, exercise(), exercise(), test_new_activity_during_generation_cannot_publish(), changed(), test_no_generation_without_a_valid_office_window_and_course() (+6 more)

### Community 66 - "ADR-016: Public programme references and an explicit local demo reset"
Cohesion: 0.40
Nodes (4): ADR-016: Public programme references and an explicit local demo reset, Context, Decision, Evidence and limits

### Community 67 - "api.py"
Cohesion: 0.17
Nodes (24): assign_scope(), documents(), get_upload(), Any, BaseModel, Db, delete, get (+16 more)

### Community 68 - "decide"
Cohesion: 0.20
Nodes (10): decide(), Any, Validate structured model output; refusal/malformed output is never a decision.…, evaluate(), main(), Any, Synthetic collection latency evidence; no database writes or Telegram…, src_engine (+2 more)

### Community 69 - "AllProvidersFailedError"
Cohesion: 0.10
Nodes (27): AllProvidersFailedError, generate_completion(), Any, Exception, Bounded OpenAI-only model roles; provider details never escape in errors., Raised when the entire LLM fallback chain is exhausted., Generate a completion with automatic provider fallback. Tries the fast model,…, fail() (+19 more)

### Community 70 - "._post"
Cohesion: 0.17
Nodes (11): Any, Send an interactive list message. `sections` is a list of section dicts…, Send a pre-approved template message., Post the payload to Meta and extract the created message ID., Meta API expects the phone number without the leading '+'., Send a simple text message. Returns the Meta message ID., Send an interactive message with up to 3 buttons. `buttons` should be a list of…, Phase 2: WhatsApp Ingress (+3 more)

### Community 71 - "Official source snapshots"
Cohesion: 0.50
Nodes (4): Conflicts to confirm, October 23 planning refresh, Official source snapshots, Sources

### Community 72 - "integration/test_followups.py"
Cohesion: 0.24
Nodes (12): callback(), Real database consent, reminder leases, freshness, delivery and the two-message…, seed(), test_budget_pause_does_not_spend_a_reminder_and_stop_cancels_it(), exercise(), test_exactly_two_reminders_then_cold_without_duplicate_delivery(), test_explicit_consent_and_stop_during_staff_takeover(), exercise() (+4 more)

### Community 73 - "fixture"
Cohesion: 0.14
Nodes (21): catalog_status(), Course, request_decision(), evaluate(), evaluate_dialogues(), fixture(), main(), Any (+13 more)

### Community 74 - "ADR-013: Adaptive, student-first course guidance"
Cohesion: 0.40
Nodes (4): ADR-013: Adaptive, student-first course guidance, Consequences, Context, Decision

### Community 75 - "tests/test_followups.py"
Cohesion: 0.20
Nodes (9): generate_hook(), Any, safe_hook(), Explicitly consented, bounded student outreach., parametrize, Only consented inactive inquiries may receive bounded outreach., test_eligibility_requires_consent_inactivity_and_an_early_stage(), test_generated_hooks_fall_back_without_inventing_claims() (+1 more)

### Community 76 - "management.tsx"
Cohesion: 0.09
Nodes (16): blank, Discount, Discounts(), Batch, Course, empty, Management(), operators (+8 more)

### Community 77 - "ADR-015: Supportive guidance and contextual answer controls"
Cohesion: 0.40
Nodes (4): ADR-015: Supportive guidance and contextual answer controls, Consequences and limits, Context, Decision

### Community 78 - "guidance.py"
Cohesion: 0.13
Nodes (27): checked_text(), add_response_controls(), answer_labels(), compose_reply(), consume_answer(), needs_progress(), Any, Low-effort answers and a bounded escape from interview-style discovery. (+19 more)

### Community 79 - "PublicCatalogue"
Cohesion: 0.16
Nodes (12): Programme, PublicCatalogue, BaseModel, field_validator, model_validator, Self, dataset(), parametrize (+4 more)

### Community 84 - "analytics.tsx"
Cohesion: 0.28
Nodes (7): Analytics(), Conversion, labels, frontend_app_analytics_module, rate(), Report, shortDate()

### Community 89 - "get_sessionmaker"
Cohesion: 0.08
Nodes (37): async_sessionmaker, get_session(), get_sessionmaker(), AsyncSession, Return the process-wide async session factory., FastAPI dependency yielding a session that closes after the request., dispatch_pending(), dispatch_due() (+29 more)

### Community 90 - "AdmitFlow"
Cohesion: 0.08
Nodes (24): AdmitFlow, Architecture, Configuration, Contributing, Current reference catalogue, Documentation, Features, For institutions (+16 more)

### Community 91 - "Phase 3: AI Core (Engine + RAG)"
Cohesion: 0.20
Nodes (10): Phase 3: AI Core (Engine + RAG), Task 10: Input guardrail node, Task 11: Triage node (intent detection), Task 12: Discovery node, Task 13: RAG pipeline, Task 14: RAG node, Task 15: Qualification node, Task 16: Output guardrail (+2 more)

### Community 92 - "AdmitFlow Backend"
Cohesion: 0.18
Nodes (11): Admissions analytics, AdmitFlow Backend, Application payments, Configuration, Consented follow-up reminders, Current implementation and verification, Institution knowledge workspace, Local development (+3 more)

### Community 93 - "test_decision_reranking.py"
Cohesion: 0.14
Nodes (24): PassageRanking, BaseModel, UUID, Bounded OpenAI evidence reranking with a validated baseline fallback., Reorder only original, safe tenant candidates; never invent text or sources.…, rerank(), evaluate(), main() (+16 more)

### Community 94 - "reindex_names.py"
Cohesion: 0.36
Nodes (7): main(), AsyncSession, UUID, Backfill encrypted lead names from latest submitted forms and rebuild blind…, reindex_batch(), test_index_rename_clear_and_legacy_backfill(), exercise()

### Community 95 - "pydantic"
Cohesion: 0.10
Nodes (26): Typed decisions through the existing OpenAI-only provider boundary., _deterministic_check(), InputGuardrailResult, LLMGuardrailResponse, LLMOutputGuardrailResponse, OutputGuardrailResult, BaseModel, Input Guardrail Node (Task 10). Detects prompt injection, profanity, and abuse… (+18 more)

### Community 96 - "Git & GitHub Workflow"
Cohesion: 0.12
Nodes (15): build(), Rebuild the committed, fictional digital-PDF fixture with reportlab., Branching model — feature branch → PR → `main`, Commits — Conventional Commits, small and coherent, Git & GitHub Workflow, Merging, No AI attribution — the human is the sole author  ⚠️, Pull Requests (+7 more)

### Community 97 - "package.json"
Cohesion: 0.22
Nodes (8): name, private, version, react-dom, @types/node, @types/react, @types/react-dom, typescript

### Community 98 - "erase_inquiry"
Cohesion: 0.27
Nodes (10): erase(), erase_inquiry(), EraseRequest, in_flight(), AsyncSession, BaseModel, Db, delete (+2 more)

### Community 99 - "@playwright/test"
Cohesion: 0.18
Nodes (5): ref_node_child_process, ref_node_crypto, ref_node_fs, ref_node_path, @playwright/test

### Community 100 - "AGENTS.md"
Cohesion: 0.25
Nodes (7): AIBoomi Startup Weekend handoff, How we build — read the handbook, Knowledge graph, Quick commands (from `backend/`), The rules you cannot skip, What this project is, Workflow triggers

### Community 101 - "Security & Production Readiness"
Cohesion: 0.18
Nodes (11): Dependency & secret scanning, Deploy & rollback, External surfaces, Guardrails & money, Local full-stack (docker-compose), Multi-tenancy — isolation is a correctness bug if wrong, Observability, PII & data protection (DPDPA) (+3 more)

### Community 102 - "send"
Cohesion: 0.08
Nodes (23): decrypt_bytes(), encrypt_bytes(), _fernet(), Encrypt uploaded source bytes before persistence, without lossy text decoding., Authenticate and decrypt source bytes for an authorized ingestion task., Any, MonkeyPatch, TestClient (+15 more)

### Community 103 - "next-env.d.ts"
Cohesion: 0.50
Nodes (3): NOTE: This file should not be edited, frontend_next_types_root_params_d, frontend_next_types_routes_d

### Community 104 - "identity_database"
Cohesion: 0.43
Nodes (7): identity_database(), Use a disposable pgvector database; never mutate the demo database., test_downgrade_preserves_legacy_rows_and_refuses_to_destroy_telegram_data(), insert_rows(), inspect_and_clean(), remove_test_bot(), verify_legacy()

### Community 105 - "send_outbound"
Cohesion: 0.28
Nodes (7): task, Follow-up jobs carry only tenant and lead identifiers, never student content., send_followup(), task, Encrypted outbound-message delivery jobs carry only internal identifiers., send_outbound_message(), send_outbound()

### Community 106 - "layout.tsx"
Cohesion: 0.25
Nodes (5): frontend_app_globals, metadata, config, @fontsource-variable/dm-sans, next

### Community 108 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, lint, record:demo, start, test:e2e:live, typecheck

### Community 109 - "backend/README.md"
Cohesion: 0.12
Nodes (15): Contextual retrieval and reference scope, Isolated full-stack Compose, Local reference-catalogue demo applications, Outbound integrations and live notifications, Staff access and privacy operations, Typed OpenAI decisions and required reranking, Explicit Telegram receiver, Isolated local full-stack runtime (+7 more)

### Community 110 - "Reply"
Cohesion: 0.08
Nodes (35): Audit-log write helper. :func:`write_audit_log` is the one path significant…, PaymentOrder, A Razorpay order for an application fee (SPEC §7.10). Amount is DB-sourced…, OutboundMessage, Reply, capture_event(), Connection, Mapper (+27 more)

### Community 111 - "ExtractionError"
Cohesion: 0.05
Nodes (63): compose(), Verify the isolated local Compose stack without external API calls or sends., seed_credentials(), verify(), blocks(), Markdown sections and table rows stay together within bounded evidence chunks., Keep section ancestry; repeat table headers instead of breaking row…, semantic_chunks() (+55 more)

### Community 112 - "sqlalchemy"
Cohesion: 0.10
Nodes (42): asyncio, Application-layer PII protection: symmetric encryption + deterministic hashing.…, Lead, its semantic facts (lead_facts), and episodic messages (ADR-004)., Institution document extraction, durable ingestion and retrieval., Code-owned application fees and authenticated Razorpay payment processing., Strict private-chat normalization and token-safe Telegram HTTP transport., Telegram transport and tenant-scoped identity helpers., Adaptive Telegram guidance persists safely through the real encrypted inbox. (+34 more)

### Community 113 - "models/__init__.py"
Cohesion: 0.07
Nodes (74): Base, IdMixin, Declarative base, metadata naming convention, and shared column mixins. Every…, Declarative base shared by every AdmitFlow model., UUID primary key with an application-side default. UUIDs avoid cross-tenant…, Server-side created/updated timestamps., Row-level tenant scoping (ADR-003). Mixed into every tenant-scoped table., TenantMixin (+66 more)

### Community 114 - "Quality Gates — Definition of Done"
Cohesion: 0.33
Nodes (6): CI mirrors this exactly, Fast iteration vs the gate, Quality Gates — Definition of Done, The baseline gate (every change), The enforced-numbers ledger, The tiers — add gates by what the change touches

### Community 115 - "test_rag_node.py"
Cohesion: 0.25
Nodes (10): process_rag_node(), AsyncSession, Retrieve context and answer knowledge questions., mock_state(), asyncio, patch, Unit tests for the RAG node., test_process_rag_node_no_chunks() (+2 more)

### Community 116 - "devDependencies"
Cohesion: 0.33
Nodes (6): devDependencies, @playwright/test, @types/node, @types/react, @types/react-dom, typescript

### Community 117 - "applications.tsx"
Cohesion: 0.25
Nodes (5): Applications(), Detail, fields, statuses, Summary

### Community 118 - "dependencies"
Cohesion: 0.40
Nodes (5): dependencies, @fontsource-variable/dm-sans, next, react, react-dom

### Community 119 - "dispatcher.py"
Cohesion: 0.13
Nodes (19): MessageDirection, Direction of a WhatsApp message row (episodic memory, ADR-004)., _flush_engine_state(), handle_turn(), _load_engine_state(), Any, AsyncSession, Engine Dispatcher (Task 8 & 17). This module contains the main entry point for… (+11 more)

### Community 120 - "encrypt_pii"
Cohesion: 0.08
Nodes (38): decrypt_pii(), encrypt_pii(), Encrypt a PII string, returning a url-safe base64 Fernet token. Fernet is…, Decrypt a token produced by :func:`encrypt_pii`. Raises…, test_profile_and_facts_survive_encryption_without_selecting_a_course(), exercise(), parametrize, test_reset_needs_confirmation_and_preserves_business_ownership() (+30 more)

### Community 121 - "outreach/followups.py"
Cohesion: 0.41
Nodes (12): activity(), after_send(), before_send(), course_available(), eligible(), pending(), process_followup(), AsyncSession (+4 more)

### Community 122 - "tests/test_conversation_readiness.py"
Cohesion: 0.13
Nodes (21): Detail, BaseModel, Only explicitly supplied application details may be reused in an encrypted…, validated_details(), ApplicationTurn, BaseModel, academic_number_supported(), interpret_turn() (+13 more)

### Community 123 - "hashlib"
Cohesion: 0.10
Nodes (16): log_delivery_status(), Request, Response, Expose only the existing Meta webhook through the temporary demo tunnel., Observe only authenticated status events, without recipient or error text., main(), prepare(), Path (+8 more)

### Community 124 - "WhatsApp readiness check — October 22, 2026"
Cohesion: 0.15
Nodes (13): Decision so far, Delivery diagnosis and configuration repair (October 23, approximately 00:16 IST), Evidence collected before configuration, Final Postman retry (October 23), Live checkpoint (approximately 22:54 IST), Missing-reply investigation (approximately 22:59 IST), New test account configuration (October 23, approximately 09:45 IST), Next live checks and evidence required (+5 more)

### Community 125 - "test_faq_evaluation.py"
Cohesion: 0.29
Nodes (10): GroundingSource, Channel-neutral input and validated plain-text reply boundary., Internal evidence persisted in encrypted replies, excluded from channel…, Case, BaseModel, score_answer(), Scoring checks internal evidence, plain answers and language-specific…, source() (+2 more)

### Community 126 - "unittest_mock"
Cohesion: 0.25
Nodes (7): Any, asyncio, patch, sample_whatsapp_payload(), test_handle_turn_basic_flow(), src_engine_dispatcher, unittest_mock

### Community 127 - "confirmation.py"
Cohesion: 0.11
Nodes (24): LinkEntity, LinkEnvelope, PaidEvent, PaidPayload, PaymentEntity, PaymentEnvelope, AsyncSession, BaseModel (+16 more)

### Community 128 - "payments.tsx"
Cohesion: 0.32
Nodes (6): label(), money(), outcomes, Payment, Payments(), statuses

### Community 129 - "evaluate_faq.py"
Cohesion: 0.15
Nodes (16): configure(), main(), Path, Create private isolated local Compose configuration without copying live…, cases(), evaluate(), main(), Bounded live FAQ evaluation on the fictional demo tenant; no messages or writes. (+8 more)

### Community 130 - "Adaptive course guidance: evidence and implementation"
Cohesion: 0.29
Nodes (7): Adaptive course guidance: evidence and implementation, Adaptive method, not a required sequence, Asking useful questions, Boundaries and verification, Primary-source research and limits, Product decision, Text, buttons and respectful pacing

### Community 131 - "Knowledge"
Cohesion: 0.44
Nodes (9): refresh(), api(), Knowledge(), action(), assignScope(), login(), search(), upload() (+1 more)

### Community 132 - "telegram/service.py"
Cohesion: 0.20
Nodes (18): ConversationReply, is_reset_event(), cancel_queued(), note_inbound(), preference_reply(), Any, AsyncSession, datetime (+10 more)

### Community 133 - "env.py"
Cohesion: 0.22
Nodes (9): do_run_migrations(), Connection, Alembic migration environment (async). Reads the database URL from application…, Emit SQL to stdout without a live DB connection., Run migrations against a live database via an async engine., run_migrations_offline(), run_migrations_online(), logging_config (+1 more)

### Community 134 - "timeline"
Cohesion: 0.20
Nodes (9): Cursor, Any, AsyncSession, BaseModel, datetime, field_validator, UUID, timeline() (+1 more)

### Community 135 - "TelegramBot"
Cohesion: 0.12
Nodes (29): Trusted bot-to-institution mapping; token is application-encrypted., TelegramBot, action(), application_action(), collect_application(), prompt(), Any, AsyncSession (+21 more)

### Community 136 - "prepare"
Cohesion: 0.15
Nodes (14): prepare(), Any, MonkeyPatch, parametrize, test_clear_escalation_records_request_outside_hours_without_a_model(), unavailable(), test_copilot_provider_failure_never_queues_a_message(), test_copilot_requires_review_rejects_stale_and_deduplicates_approval() (+6 more)

### Community 137 - "page.tsx"
Cohesion: 0.12
Nodes (13): DeliveryBudget(), Usage, Exports(), Configuration, Integrations(), Request, Doc, errors (+5 more)

### Community 139 - "BaseModel"
Cohesion: 0.23
Nodes (7): BatchInput, Hours, BaseModel, model_validator, Self, RuleInput, SettingsInput

### Community 140 - "RuleOperator"
Cohesion: 0.30
Nodes (12): Qualification-rule comparison operators (SPEC §7.4). Evaluated…, RuleOperator, _coerce_values(), evaluate_rule(), Any, Evaluate a qualification rule deterministically. Args: operator: The…, test_evaluate_rule_in_list(), test_evaluate_rule_missing_extracted_value() (+4 more)

### Community 141 - "pg_url"
Cohesion: 0.19
Nodes (13): _alembic_config(), monkeypatch_session(), pg_url(), MonkeyPatch, Start Postgres, point settings at it, yield the asyncpg URL., The tier requirement: alembic upgrade head then downgrade base, both clean., test_migration_applies_up_and_down(), _tables() (+5 more)

### Community 142 - "generate"
Cohesion: 0.36
Nodes (9): content(), decide(), generate(), latest(), Any, AsyncSession, Db, post (+1 more)

### Community 143 - "add_institution_knowledge_workspace_b627da2f7e11.py"
Cohesion: 0.40
Nodes (4): Column, DateTime, _timestamps(), upgrade()

### Community 144 - "Code Owns the Money"
Cohesion: 0.50
Nodes (5): ADR-006: Code-Owned Qualification and Payments, Intent: Admissions Flow and Discounts, Discount Codes, Code Owns Eligibility, Code Owns the Money

### Community 145 - "seed"
Cohesion: 0.08
Nodes (34): PaymentLink, BaseModel, field_validator, payments(), Any, get, create(), Any (+26 more)

### Community 146 - "TelegramClient"
Cohesion: 0.07
Nodes (34): protect_logs(), Any, LogRecord, RuntimeError, TaskIQ changes log levels; redact before either HTTP client or root handlers…, Ephemeral feedback never delays, retries or fails the durable conversation., TelegramAPIError, TelegramClient (+26 more)

### Community 147 - "notifications.tsx"
Cohesion: 0.33
Nodes (4): labels, Notice, Notifications(), Snapshot

### Community 148 - "Q: Retrieve relevant passages Rerank supporting evidence Validate supporting quotation Grounded answer or abstention: what are the 3 steps for validate supporting quotation?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Retrieve relevant passages Rerank supporting evidence Validate supporting quotation Grounded answer or abstention: what are the 3 steps for validate supporting quotation?, Source Nodes

### Community 149 - "send_message"
Cohesion: 0.36
Nodes (10): active_request(), Any, AsyncSession, Db, post, UUID, require_takeover(), resume() (+2 more)

### Community 150 - "Q: What is the validate supporting quotation step for? Explain it."
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: What is the validate supporting quotation step for? Explain it., Source Nodes

### Community 151 - "Q: How did AdmitFlow validate the supporting quotation?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: How did AdmitFlow validate the supporting quotation?, Source Nodes

### Community 152 - "integration/conftest.py"
Cohesion: 0.50
Nodes (3): isolated_local_login_windows(), MonkeyPatch, Keep development-only throttle state independent across database test cases.

### Community 153 - "record-demo.mjs"
Cohesion: 0.40
Nodes (4): credentials, headers, journey, target

### Community 154 - "durable_payments_outbound_f129a064c5e8.py"
Cohesion: 0.50
Nodes (3): common(), Column, upgrade()

### Community 155 - "Check"
Cohesion: 0.67
Nodes (3): Check, Hook, BaseModel

### Community 156 - "Phase 4: Advanced Bot Features"
Cohesion: 0.29
Nodes (7): Phase 4: Advanced Bot Features, Task 18: Application form collection node, Task 19: Razorpay integration, Task 20: Human handoff + co-pilot mode, Task 21: Cold lead re-engagement worker, Task 22: WhatsApp rate-limit tracking, Task 23: Langfuse tracing integration

### Community 157 - "staff/payments.py"
Cohesion: 0.19
Nodes (19): demo_fee(), AsyncSession, Course, Explicit, institution-scoped development demos never authorise real admissions., check_demo_payment(), check_demo_payments(), check(), UUID (+11 more)

### Community 159 - "Phase 3–4 addition (see ADR-008)"
Cohesion: 0.29
Nodes (7): Phase 3–4 addition (see ADR-008), Task 40: `decide()` System-1 decision-layer abstraction, Task 41: Distill decisions into self-hosted Laya (post-demo), Task 42.1: Complex Document Parsing & Semantic Chunking, Task 42.2: Contextual Query Rewriting, Task 42.3: Pluggable Reranker (Cohere API vs Local), Task 42: Advanced RAG Strategy (ADR-011)

### Community 160 - "AdmitFlow — Task List"
Cohesion: 0.14
Nodes (14): AdmitFlow — Task List, AIBoomi Startup Weekend session handoff (2026-10-22), Current direction and hackathon resources (2026-10-23), Phase 1: Foundation, Phase 6: Production Hardening, Task 1: Initialize Python project, FastAPI, settings, and Docker, Task 2: PostgreSQL schema (SQLAlchemy + Alembic), Task 35: Sentry error monitoring (+6 more)

### Community 161 - "index_known_name"
Cohesion: 0.40
Nodes (5): index_known_name(), Connection, Mapper, Keep index updates atomic with encrypted names, including name removal., listens_for

### Community 162 - "ADR-017: Explicit demo applications for public-reference courses"
Cohesion: 0.40
Nodes (4): ADR-017: Explicit demo applications for public-reference courses, Decision, Local activation and evidence, Verification

### Community 163 - "WhatsApp readiness check (2026-10-22, in progress)"
Cohesion: 0.40
Nodes (5): Final Postman diagnostic (October 23, executed; delivery blocked), Readiness blocker: idle Redis worker restart (in progress), Readiness tunnel setup (in progress), Test-number delivery diagnosis (October 23, blocked on Meta account restriction), WhatsApp readiness check (2026-10-22, in progress)

### Community 164 - "AdmitFlow pitch deck"
Cohesion: 0.25
Nodes (7): AdmitFlow pitch deck, Slide 1: AdmitFlow, Slide 2: The admissions handoff, Slide 3: A working institution workspace, Slide 4: Answers from approved documents, Slide 5: AI with institution control, Slide 6: An institution pilot

### Community 165 - "Workspace colour theme"
Cohesion: 0.50
Nodes (3): Roles, Verification, Workspace colour theme

### Community 167 - "Phase 5: Dashboard Frontend (Next.js)"
Cohesion: 0.17
Nodes (12): Phase 5: Dashboard Frontend (Next.js), Task 24: Initialize Next.js + dark mode + glassmorphism, Task 25: Authentication (email + password), Task 26: Dashboard home (funnel analytics), Task 27: Leads CRM page, Task 28: Course & batch management, Task 29: Chat takeover + co-pilot UI, Task 30: Document management (RAG) (+4 more)

### Community 169 - "Language review packet"
Cohesion: 0.40
Nodes (5): Current templates, Language review packet, Live exercise, Reference clarification, Reminder consent and outreach copy

### Community 170 - "Q: what you need to is explain me the webpage build and every feature in it"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: what you need to is explain me the webpage build and every feature in it, Source Nodes

### Community 171 - "Q: what is the outbound webhooks for"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: what is the outbound webhooks for, Source Nodes

### Community 172 - "Q: what about observbility"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: what about observbility, Source Nodes

### Community 173 - "RazorpayClient"
Cohesion: 0.09
Nodes (24): AsyncBaseTransport, Bounded synthetic PDF upload/queue/OpenAI/search check; removes its own upload., Credentials, PaymentProviderError, Exception, Bounded Razorpay requests; ambiguous link creation is never blindly retried., Read an existing exact reference; absence never authorizes another creation., Read only: verify the exact paid link and its captured, unrefunded test payment. (+16 more)

### Community 174 - "Q: Prepare a three-minute jury pitch and Q&A using a five-stage story arc, customer pain points, solution and impact."
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Prepare a three-minute jury pitch and Q&A using a five-stage story arc, customer pain points, solution and impact., Source Nodes

### Community 175 - "Q: What you need to do is i need to present the this project before the jury. First explain the overall structure the stack what things used where used . From A to Z things. that i can answer anything if they question."
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: What you need to do is i need to present the this project before the jury. First explain the overall structure the stack what things used where used . From A to Z things. that i can answer anything if they question., Source Nodes

### Community 177 - "write_audit_log"
Cohesion: 0.13
Nodes (21): CRM search and institution downloads, Any, AsyncSession, UUID, Record persisted ORM transitions atomically; never infer an earlier stage., Append one entry to ``audit_logs`` on ``session``; return it flushed, not…, record_stage_changes(), write_audit_log() (+13 more)

### Community 178 - "ADR-014: Natural collection, context reset and responsive replies"
Cohesion: 0.50
Nodes (3): ADR-014: Natural collection, context reset and responsive replies, Decision, Evidence and limits

### Community 183 - "test_worker_broker.py"
Cohesion: 0.18
Nodes (10): ping(), task, Smoke-test task: returns ``{"result": payload}``. Enqueued from the…, Tests for the TaskIQ broker setup and task execution (Task 3). All tests run…, When REDIS_URL is unset the factory should yield an InMemoryBroker., The ping task should run and return the expected payload., Ping without an explicit payload should default to 'pong'., test_broker_is_in_memory_without_redis_url() (+2 more)

### Community 184 - "AdmitFlow submission requirements"
Cohesion: 0.50
Nodes (4): AdmitFlow submission requirements, Demonstration, Required artifacts, Truthful claims

### Community 185 - "AdmitFlow execution and demonstration checklist"
Cohesion: 0.67
Nodes (3): AdmitFlow execution and demonstration checklist, Build and verify, Demonstrate and submit

### Community 193 - "ExtractionResponse"
Cohesion: 0.67
Nodes (3): ExtractionResponse, BaseModel, Structured output expected from the LLM when extracting fields.

## Knowledge Gaps
- **486 isolated node(s):** `admitflow-backend`, `fs`, `path`, `crypto`, `root` (+481 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1319 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Work-memory lessons

**Preferred sources** — corroborated by past sessions; start here.
- `answer_question()` (3× useful, score=2.99774848)
- `GroundedQuote` (3× useful, score=2.99774848)
- `WebhookDelivery` (2× useful, score=1.995671698)
- `Admissions()` (2× useful, score=1.995521132)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CRM search and institution downloads` connect `write_audit_log` to `seed`, `backend/README.md`, `PublicCatalogue`, `leads.py`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Why does `write_audit_log()` connect `write_audit_log` to `journey.py`, `telegram/service.py`, `payments/service.py`, `TelegramBot`, `analytics.py`, `knowledge/processing.py`, `replace_demo_catalogue.py`, `staff/integrations.py`, `deliver`, `generate`, `seed`, `send_message`, `text`, `staff/payments.py`, `leads.py`, `AdmitFlow — Task List`, `management.py`, `session.py`, `Event`, `accounts.py`, `Course`, `live`, `exports.py`, `auth.py`, `api.py`, `guidance.py`, `get_sessionmaker`, `erase_inquiry`, `send_outbound`, `Reply`, `models/__init__.py`, `outreach/followups.py`, `confirmation.py`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Why does `LeadStatus` connect `LeadStatus` to `journey.py`, `analytics.py`, `payments/service.py`, `TelegramBot`, `deliver`, `seed`, `GuidanceMemory`, `send_message`, `signin`, `leads.py`, `session.py`, `Event`, `write_audit_log`, `Course`, `tests/test_telegram_identity.py`, `exports.py`, `age`, `integration/test_followups.py`, `tests/test_followups.py`, `guidance.py`, `Reply`, `sqlalchemy`, `models/__init__.py`, `test_rag_node.py`, `dispatcher.py`, `encrypt_pii`, `outreach/followups.py`, `confirmation.py`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `encrypt_pii()` (e.g. with `Consequences` and `Decision`) actually correct?**
  _`encrypt_pii()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 23 inferred relationships involving `Reply` (e.g. with `advance_application()` and `request_staff()`) actually correct?**
  _`Reply` has 23 INFERRED edges - model-reasoned connections that need verification._
- **Are the 61 inferred relationships involving `LeadStatus` (e.g. with `record_stage_changes()` and `Lead`) actually correct?**
  _`LeadStatus` has 61 INFERRED edges - model-reasoned connections that need verification._
- **What connects `admitflow-backend`, `fs`, `path` to the rest of the system?**
  _486 weakly-connected nodes found - possible documentation gaps or missing edges._
Task 70: code AST refreshed. New ADR and verification documents have not received
a separate semantic extraction; source files and test evidence determine readiness.
