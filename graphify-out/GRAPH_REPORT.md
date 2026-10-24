# Graph Report - admitflow  (2026-10-24)

## Corpus Check
- 337 files · ~187,571 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 7, .example 2, .css 2)

## Summary
- 2953 nodes · 8671 edges · 187 communities (167 shown, 20 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 554 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `83eef0cf`
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
- journey.py
- RedisMutex
- review
- pdf_parser.py
- transport.py
- WhatsAppSender
- core/rag.py
- PII Encryption & Audit Log
- Razorpay Payment Integration
- get_settings
- admissions.tsx
- contextual_query
- GuidanceMemory
- AIBoomi Startup Weekend Kochi: fresh-session context
- test_telegram_contracts.py
- get_engine
- test_expired_lease_recovery_cap_and_configuration_cancellation
- LeadStatus
- Stages
- alembic
- TestClient
- run_postman_check.cjs
- Task List
- sqlalchemy
- test_crm_search.py
- Phase 5: Dashboard Frontend (Next.js)
- management.py
- Code Standards
- outreach/followups.py
- Event preparation and execution plan
- 7. Core Feature Specifications
- send
- main.py
- route
- re
- Hackathon resources for AdmitFlow
- manifest.json
- knowledge/processing.py
- AdmitFlow: current state and planning baseline
- AdmitFlow: AIBoomi submission plan
- AdmitFlow — Complete Specification
- normalize_e164
- DocumentChunk
- ADR-011: Required OpenAI passage reranking
- Testing
- check_input_safety
- AdmitFlow project handoff
- detect_intent
- EncryptionKeyNotConfiguredError
- GuidanceDecision
- RazorpayClient
- Phase 3: AI Core (Engine + RAG)
- ADR-010: Triage Fallback Routing (Anti-Spam)
- ADR-012: Telegram and OpenAI for the first complete admissions MVP
- collections_abc
- 2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md
- compilerOptions
- hash_password
- age
- test_payment_and_webhook_claims_wait_for_erasure_lock
- api.py
- extraction.py
- generate_completion
- evaluate
- Official source snapshots
- 13. Dashboard Features
- ExtractionError
- Course
- budget.py
- management.tsx
- prepare_document_models.py
- guidance_interaction.py
- hashlib
- verify.sh
- db/__init__.py
- src/__init__.py
- tasks/__init__.py
- analytics.tsx
- whatsapp/__init__.py
- integration/__init__.py
- admitflow-backend
- pg_url
- AdmitFlow
- pathlib
- retrieval.py
- test_decision_reranking.py
- Local Telegram/OpenAI runtime
- AllProvidersFailedError
- Git & GitHub Workflow
- package.json
- inbound
- @playwright/test
- AGENTS.md
- Security & Production Readiness
- fake_embeddings
- next-env.d.ts
- encrypt_pii
- ADR-009: Application-Layer PII Encryption and Audit Logging
- layout.tsx
- frontend/AGENTS.md
- scripts
- backend/README.md
- text
- payments/conversation.py
- test_knowledge_workspace.py
- models/__init__.py
- Quality Gates — Definition of Done
- TelegramClient
- devDependencies
- applications.tsx
- dependencies
- dispatcher.py
- Settings
- parse_callback
- Detail
- signin
- WhatsApp readiness check — October 22, 2026
- Reply
- pytest
- DraftContent
- payments.tsx
- download
- ADAPTIVE_GUIDANCE_RESEARCH.md
- Knowledge
- send_reply
- env.py
- verify_document_pipeline.py
- write_audit_log
- prepare
- page.tsx
- AdmitFlow Backend
- 20260929_initial_schema_64cfce85009d.py
- RuleOperator
- identity_database
- verify_compose.py
- add_institution_knowledge_workspace_b627da2f7e11.py
- exports.py
- test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment
- get_sessionmaker
- notifications.tsx
- AdmitFlow — Task List
- index_known_name
- test_webhook.py
- test_qualification.py
- test_crm_exports.py
- record-demo.mjs
- scheduler.py
- add_conversation_runtime_714f092da3b8.py
- fixture
- payment_webhook
- durable_payments_outbound_f129a064c5e8.py
- deliver
- reconcile
- Phase 3–4 addition (see ADR-008)
- Phase 4: Advanced Bot Features
- erase_inquiry
- docs/event/SUBMISSION_PLAN.md
- Language review packet
- 11. Human-in-the-Loop (Full Workflow)
- Phase 6: Production Hardening
- Cursor
- Phase 1: Foundation
- .__call__
- test_workspace_limits.py
- integration/conftest.py
- PaymentProviderError
- process_payment
- Q: What you need to do is i need to present the this project before the jury. First explain the overall structure the stack what things used where used . From A to Z things. that i can answer anything if they question.
- 20261008_add_knowledge_models_for_rag_c470f1ebc811.py
- record_stage_changes
- ADR-014: Natural collection, context reset and responsive replies
- 2. Boundaries & Invariants
- 3. Tech Stack & Commands
- 8. RAG (Retrieval-Augmented Generation)
- tasks/processing.py
- evaluate_live.py
- AdmitFlow execution and demonstration checklist
- DOCUMENT_REVIEW.md

## God Nodes (most connected - your core abstractions)
1. `encrypt_pii()` - 110 edges
2. `Reply` - 105 edges
3. `write_audit_log()` - 100 edges
4. `LeadStatus` - 100 edges
5. `Lead` - 94 edges
6. `get_settings()` - 93 edges
7. `TelegramBot` - 88 edges
8. `decrypt_pii()` - 85 edges
9. `route()` - 80 edges
10. `Course` - 71 edges

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

## Communities (187 total, 20 thin omitted)

### Community 0 - "AdmitFlow Complete Specification"
Cohesion: 0.20
Nodes (18): ADR-001: Hybrid Architecture, ADR-004: Dual Memory Architecture, Episodic Memory (messages table), Semantic Memory (lead_facts table), ADR-005: Three-Layer Guardrails and RAG, Three-Layer Guardrails, ADR-007: Finalized Production Stack, ADR-008: System-1 Decision Layer (Laya / Jev) (+10 more)

### Community 1 - "Conversation Engine (hand-rolled dispatcher)"
Cohesion: 0.25
Nodes (8): Conversation Engine (hand-rolled dispatcher), System-1 decide() Decision Layer, FastAPI WhatsApp Webhook, Langfuse LLM Tracing, pgvector RAG Pipeline, Redis (mutex / dedup / rate-limit), TaskIQ Background Worker, Three-Layer Guardrails

### Community 2 - "README.md"
Cohesion: 0.22
Nodes (7): Executed final check, One final WhatsApp check with Postman, AdmitFlow necessary resources, Planning baseline before Telegram alignment, AdmitFlow Platform, AdmitFlow Implementation Plan, AdmitFlow Task List

### Community 3 - "Finalized Production Stack"
Cohesion: 0.18
Nodes (11): ADR-002: Webhook Concurrency and Deduplication, Per-Phone Redis Mutex, Webhook Deduplication (Redis SETNX), ADR-003: Multi-Tenancy Strategy, Multi-Tenancy (Row-Level Isolation), Finalized Production Stack, Fly.io (Backend + Worker + Scheduler), Langfuse Cloud (LLM Tracing) (+3 more)

### Community 4 - "lead_statement"
Cohesion: 0.18
Nodes (17): lead_statement(), lead_summary(), LeadFilters, LeadSearch, Any, BaseModel, Select, UUID (+9 more)

### Community 5 - "analytics"
Cohesion: 0.14
Nodes (21): alias, analytics(), bucket_dates(), count(), percent(), Period, period_window(), Any (+13 more)

### Community 6 - "Code Owns the Money"
Cohesion: 0.50
Nodes (5): ADR-006: Code-Owned Qualification and Payments, Intent: Admissions Flow and Discounts, Discount Codes, Code Owns Eligibility, Code Owns the Money

### Community 7 - "journey.py"
Cohesion: 0.12
Nodes (48): Lead, A prospective applicant with optional phone contact and channel identities.…, catalog(), commit_guidance(), guide(), load_guidance(), Any, AsyncSession (+40 more)

### Community 8 - "RedisMutex"
Cohesion: 0.07
Nodes (28): MutexAcquireError, Redis, RuntimeError, Redis distributed mutex with owner-safe release and keepalive (Task 7). Ensures…, Background loop that extends the TTL while the lock is held., Raised when the mutex cannot be acquired after all retries., Async context-manager mutex backed by Redis ``SET NX``. Parameters: redis: An…, Attempt to acquire the lock, retrying up to ``retry_count`` times. (+20 more)

### Community 9 - "review"
Cohesion: 0.33
Nodes (10): CRM search and institution downloads, applications(), detail(), owned(), Any, Db, get, post (+2 more)

### Community 10 - "pdf_parser.py"
Cohesion: 0.13
Nodes (16): kill_descendants(), parse_pdf(), Offline PDF child process with per-loop backpressure, memory and time limits., Include Windows venv redirector children and any parser subprocesses., resident_memory(), watch_memory(), Process, parametrize (+8 more)

### Community 11 - "transport.py"
Cohesion: 0.10
Nodes (31): destination(), post_event(), PrivateTransportLogs, protect_logs(), public_ip(), LogRecord, HTTPS delivery pins a public resolved address while retaining TLS host…, resolve_public() (+23 more)

### Community 12 - "WhatsAppSender"
Cohesion: 0.07
Nodes (30): Sanitizer to prevent RAG poisoning. Blocks chunks that contain obvious prompt…, sanitize_chunks(), RAG Node (Task 14). Graph node that retrieves from the knowledge base and…, Any, RuntimeError, WhatsApp message sending service (Task 6). Uses httpx2 to call the Meta Graph…, Send an interactive list message. `sections` is a list of section dicts…, Send a pre-approved template message. (+22 more)

### Community 13 - "core/rag.py"
Cohesion: 0.13
Nodes (19): chunk_text(), embed_text(), ingest_document(), Any, AsyncSession, UUID, RAG pipeline core logic (Task 13). Handles ingestion (chunking, embedding),…, Generate embedding for text using configured model. (+11 more)

### Community 16 - "get_settings"
Cohesion: 0.10
Nodes (22): AsyncBroker, get_settings(), Application settings singleton. Loads configuration from the environment (and…, Return the process-wide :class:`Settings` singleton., Reject oversized multipart streams before they can fill temporary storage., _build_broker(), TaskIQ broker singleton. In production (and local dev with Redis running) the…, Construct the right broker based on the current settings. This is a plain… (+14 more)

### Community 17 - "admissions.tsx"
Cohesion: 0.10
Nodes (19): Admissions(), Detail, Human, Inquiry, labels, Request, RuleEvidence, statusLabel() (+11 more)

### Community 18 - "contextual_query"
Cohesion: 0.13
Nodes (17): contextual_query(), Resolve pronouns/slang using bounded recent turns; uncertainty asks the…, retrieval_query(), evaluate(), main(), Bounded synthetic OpenAI reference resolution; no database writes or sends., MonkeyPatch, parametrize (+9 more)

### Community 19 - "GuidanceMemory"
Cohesion: 0.10
Nodes (58): QualificationRule, A structured eligibility rule evaluated in code, not by the LLM (ADR-006).…, academic_number_supported(), catalog_status(), GuidanceMemory, Note, interpret_turn(), merge_evidence() (+50 more)

### Community 20 - "AIBoomi Startup Weekend Kochi: fresh-session context"
Cohesion: 0.11
Nodes (19): AIBoomi Startup Weekend Kochi: fresh-session context, Assessment and next decision, Current readiness session (October 22), Event sources and local copies, Existing prototype rule and surprise element, Existing working-tree changes, Fresh-message prompt, Handoff status (+11 more)

### Community 21 - "test_telegram_contracts.py"
Cohesion: 0.17
Nodes (14): normalize_update(), protect_logs(), LogRecord, TaskIQ changes log levels; redact before either HTTP client or root handlers…, TokenSafeFilter, MonkeyPatch, Private-chat normalization, callback ownership and validated reply limits., test_callback_actor_and_origin() (+6 more)

### Community 22 - "get_engine"
Cohesion: 0.15
Nodes (16): AsyncEngine, get_engine(), Return the process-wide async engine (one pool for the app)., main(), run(), main(), provision(), Manually provision an institution administrator without printing credentials. (+8 more)

### Community 23 - "test_expired_lease_recovery_cap_and_configuration_cancellation"
Cohesion: 0.13
Nodes (13): configure(), event_for(), test_configuration_roles_encryption_and_tenant_ownership(), inspect(), test_delivery_claim_retry_and_minimal_payload(), exercise(), test_expired_lease_recovery_cap_and_configuration_cancellation(), exercise() (+5 more)

### Community 24 - "LeadStatus"
Cohesion: 0.08
Nodes (42): LeadStatus, Lead lifecycle states (SPEC §7.3). Where a lead *stands*, not a fixed track —…, present_courses(), AsyncSession, Discovery Node (Task 12). Presents available courses as WhatsApp interactive…, Fetch active courses with available batches and present to user. Only shows…, process_rag_node(), AsyncSession (+34 more)

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

### Community 30 - "sqlalchemy"
Cohesion: 0.11
Nodes (34): ApplicationStatus, DiscountType, PaymentStatus, Enumerated types used across the schema. These are Python ``str`` enums mapped…, How a discount code reduces the fee., Payment order lifecycle (SPEC §7.10)., Application review status (SPEC §7.9 / lifecycle)., PaymentOrder (+26 more)

### Community 31 - "test_crm_search.py"
Cohesion: 0.22
Nodes (14): Core cross-cutting concerns: settings, security, schemas, guardrails, tracing., name_tokens(), normalized_phone(), UUID, query_tokens(), Tenant-keyed blind name prefixes; plaintext remains in encrypted columns only., token(), words() (+6 more)

### Community 32 - "Phase 5: Dashboard Frontend (Next.js)"
Cohesion: 0.17
Nodes (12): Phase 5: Dashboard Frontend (Next.js), Task 24: Initialize Next.js + dark mode + glassmorphism, Task 25: Authentication (email + password), Task 26: Dashboard home (funnel analytics), Task 27: Leads CRM page, Task 28: Course & batch management, Task 29: Chat takeover + co-pilot UI, Task 30: Document management (RAG) (+4 more)

### Community 33 - "management.py"
Cohesion: 0.08
Nodes (62): Dashboard access role (SPEC — admin vs agent)., StaffRole, admin_scope(), create_user(), CreateUser, edit_user(), EditUser, Any (+54 more)

### Community 34 - "Code Standards"
Cohesion: 0.18
Nodes (11): Async & I/O, Code Standards, Configuration — settings, not literals, Dependencies, Errors, Formatting, LLM calls, Logging & observability (+3 more)

### Community 35 - "outreach/followups.py"
Cohesion: 0.13
Nodes (27): OutboundMessage, activity(), after_send(), before_send(), Check, course_available(), Hook, pending() (+19 more)

### Community 36 - "Event preparation and execution plan"
Cohesion: 0.18
Nodes (11): Business and mentor preparation, Evaluation and demo evidence, Event preparation and execution plan, Kickoff disclosure draft, Latest direction (October 23), Minimum demonstrable product, Next action: one-hour v1 readiness check, Submission checklist (+3 more)

### Community 37 - "7. Core Feature Specifications"
Cohesion: 0.20
Nodes (10): 7.10 Payment Integration & Discounts (Razorpay), 7.1 WhatsApp Number Architecture, 7.2 Multi-Tenancy (Row-Level Isolation), 7.3 Lead Lifecycle States, 7.5 Batch & Intake Management, 7.6 Cold Lead Re-engagement, 7.7 Language Support, 7.8 Lead Sources & Outbound (+2 more)

### Community 38 - "send"
Cohesion: 0.15
Nodes (11): decrypt_bytes(), _fernet(), Authenticate and decrypt source bytes for an authorized ingestion task., TestClient, readable_pdf(), send(), test_complex_pdf_upload_preserves_table_and_programme_context(), test_upload_formats_search_duplicates_and_tenant_isolation() (+3 more)

### Community 39 - "main.py"
Cohesion: 0.08
Nodes (23): ASGIApp, UploadBodyLimit, recovery_loop(), create_app(), lifespan(), FastAPI, FastAPI application entry point. Boots the API, manages the TaskIQ broker…, Start / stop the TaskIQ broker alongside the FastAPI process. The… (+15 more)

### Community 40 - "route"
Cohesion: 0.11
Nodes (43): Event, route(), callback_data(), test_english_start_has_no_language_or_forced_course_menu(), exercise(), test_foreign_or_changed_availability_cannot_be_selected(), exercise(), test_known_failed_rule_cannot_be_bypassed_by_a_direct_name() (+35 more)

### Community 41 - "re"
Cohesion: 0.18
Nodes (13): AmbiguousCourseReference, AsyncSession, Course, UUID, ValueError, question_courses(), Code-owned course scopes for approved institution references., More than one active course has the requested name without a selected owner. (+5 more)

### Community 42 - "Hackathon resources for AdmitFlow"
Cohesion: 0.20
Nodes (10): Acceptance before using a resource, Event and release boundaries, Goal, Hackathon resources for AdmitFlow, October 23 Downloads guide: hosted inference access, Participant credits and other support, Suggested allocation and activation order, Useful resources mapped to the plan (+2 more)

### Community 43 - "manifest.json"
Cohesion: 0.20
Nodes (9): SPEC.md, bytes, sha256, tasks/plan.md, bytes, sha256, tasks/todo.md, bytes (+1 more)

### Community 44 - "knowledge/processing.py"
Cohesion: 0.15
Nodes (14): Document, An uploaded document in the institution's knowledge base., process_upload(), UUID, Durable upload claims, bounded embedding and atomic publication of ready…, Claim once, process outside the transaction, then publish only the current…, ingest_upload(), task (+6 more)

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

### Community 49 - "DocumentChunk"
Cohesion: 0.24
Nodes (11): DocumentChunk, A chunk of a document, with its embedding for vector search., PassageRanking, BaseModel, UUID, Bounded OpenAI evidence reranking with a validated baseline fallback., Reorder only original, safe tenant candidates; never invent text or sources.…, rerank() (+3 more)

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
Cohesion: 0.20
Nodes (10): AdmitFlow project handoff, Current conversation work: Task 61, Current direction, Current work: Task 62 conversation continuity, Development rules, Event submission, Execution checkpoint, First usable release (+2 more)

### Community 54 - "detect_intent"
Cohesion: 0.20
Nodes (15): detect_intent(), Classify the user's intent to route to the correct node. Design Decision: If a…, asyncio, Test routing for course discovery., Test routing for knowledge questions., Test routing for qualification answers., Test routing for human handoff., Test routing for empty messages without calling LLM defaults to discovery. (+7 more)

### Community 55 - "EncryptionKeyNotConfiguredError"
Cohesion: 0.17
Nodes (13): EncryptionKeyNotConfiguredError, RuntimeError, Raised when a PII helper is used but its key is unset in settings., hash_telegram_identifier(), UUID, Private Telegram identity lookup without storing raw identifiers in indexes., Hash an identifier in its tenant/bot/type domain using the lookup secret. This…, MonkeyPatch (+5 more)

### Community 56 - "GuidanceDecision"
Cohesion: 0.09
Nodes (41): CourseMatch, GuidanceDecision, GuidanceInterpretation, InterestTheme, ProfileUpdate, BaseModel, Bounded exploratory guidance; evidence notes are not psychometric measurements., StrictModel (+33 more)

### Community 57 - "RazorpayClient"
Cohesion: 0.17
Nodes (16): Credentials, Bounded Razorpay requests; ambiguous link creation is never blindly retried., RazorpayClient, discounted_amount(), provision(), Read-only credential probe, then encrypted institution-owned Razorpay…, MonkeyPatch, parametrize (+8 more)

### Community 58 - "Phase 3: AI Core (Engine + RAG)"
Cohesion: 0.18
Nodes (11): Phase 3: AI Core (Engine + RAG), Task 10: Input guardrail node, Task 11: Triage node (intent detection), Task 12: Discovery node, Task 13: RAG pipeline, Task 14: RAG node, Task 15: Qualification node, Task 16: Output guardrail (+3 more)

### Community 59 - "ADR-010: Triage Fallback Routing (Anti-Spam)"
Cohesion: 0.33
Nodes (5): ADR-010: Triage Fallback Routing (Anti-Spam), Consequences, Context, Decision, Status

### Community 60 - "ADR-012: Telegram and OpenAI for the first complete admissions MVP"
Cohesion: 0.29
Nodes (7): ADR-012: Telegram and OpenAI for the first complete admissions MVP, Consequences, Context, Decision, Implemented runtime boundaries, References and verification, Supersession and preserved decisions

### Community 62 - "2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md"
Cohesion: 0.25
Nodes (4): Architecture Decisions, Implementation Plan: AdmitFlow, Overview, Risks and Mitigations

### Community 63 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 64 - "hash_password"
Cohesion: 0.08
Nodes (38): change_password(), hash_password(), issue_session(), Login, logout(), me(), PasswordChange, AsyncSession (+30 more)

### Community 65 - "age"
Cohesion: 0.13
Nodes (18): age(), outreach(), parametrize, seed(), test_exactly_two_reminders_then_cold_without_duplicate_delivery(), exercise(), test_hours_and_opt_out_are_checked_again_before_the_network(), exercise() (+10 more)

### Community 67 - "api.py"
Cohesion: 0.14
Nodes (27): encrypt_bytes(), Encrypt uploaded source bytes before persistence, without lossy text decoding., assign_scope(), documents(), get_upload(), Any, BaseModel, Db (+19 more)

### Community 68 - "extraction.py"
Cohesion: 0.18
Nodes (15): blocks(), Markdown sections and table rows stay together within bounded evidence chunks., Keep section ancestry; repeat table headers instead of breaking row…, semantic_chunks(), table_parts(), table_start(), text_parts(), Bounded extraction of institution reference documents; never execute uploads. (+7 more)

### Community 69 - "generate_completion"
Cohesion: 0.15
Nodes (18): generate_completion(), Any, Bounded OpenAI-only model roles; provider details never escape in errors., Generate a completion with automatic provider fallback. Tries the fast model,…, asyncio, parametrize, Test that it returns successfully on the primary model., Test that it falls back to OpenAI if primary OpenAI model fails. (+10 more)

### Community 70 - "evaluate"
Cohesion: 0.50
Nodes (3): evaluate(), main(), Any

### Community 71 - "Official source snapshots"
Cohesion: 0.50
Nodes (4): Conflicts to confirm, October 23 planning refresh, Official source snapshots, Sources

### Community 72 - "13. Dashboard Features"
Cohesion: 0.22
Nodes (9): 13.1 Authentication, 13.2 Roles & Permissions, 13.3 UI Aesthetic, 13.4 Real-Time Notifications, 13.5 Funnel Analytics, 13.6 Data Export & Integration, 13.7 Document Management (RAG), 13.8 Onboarding (MVP) (+1 more)

### Community 73 - "ExtractionError"
Cohesion: 0.22
Nodes (18): extract_file(), ExtractionError, ValueError, A safe, public error code rather than parser output containing document text., validate_path(), preflight_pdf(), basic_pdf(), parametrize (+10 more)

### Community 74 - "Course"
Cohesion: 0.09
Nodes (25): Batch, Course, A program a lead can be qualified for and pay to apply to., A dated intake of a course with finite seats (SPEC §7.5)., Human-readable callback summaries without exposing routing or signature details., seed(), test_concurrent_reviews_allocate_one_seat_and_repeated_approval_is_idempotent(), seed() (+17 more)

### Community 75 - "budget.py"
Cohesion: 0.07
Nodes (42): escalation_reason(), office_open(), datetime, Reason, Deterministic clear support signals and institution-local office hours., eligible(), safe_hook(), Explicitly consented, bounded student outreach. (+34 more)

### Community 76 - "management.tsx"
Cohesion: 0.09
Nodes (16): blank, Discount, Discounts(), Batch, Course, empty, Management(), operators (+8 more)

### Community 77 - "prepare_document_models.py"
Cohesion: 0.13
Nodes (14): configure(), main(), Path, Create private isolated local Compose configuration without copying live…, main(), prepare(), Path, Download only local PDF layout/table assets; no OCR, generation or document… (+6 more)

### Community 78 - "guidance_interaction.py"
Cohesion: 0.15
Nodes (22): checked_text(), add_response_controls(), answer_labels(), compose_reply(), consume_answer(), needs_progress(), Any, Low-effort answers and a bounded escape from interview-style discovery. (+14 more)

### Community 79 - "hashlib"
Cohesion: 0.09
Nodes (24): log_delivery_status(), Request, Response, Expose only the existing Meta webhook through the temporary demo tunnel., Observe only authenticated status events, without recipient or error text., Integer monetary arithmetic and exact-byte webhook authentication., get, post (+16 more)

### Community 84 - "analytics.tsx"
Cohesion: 0.28
Nodes (7): Analytics(), Conversion, labels, frontend_app_analytics_module, rate(), Report, shortDate()

### Community 89 - "pg_url"
Cohesion: 0.19
Nodes (13): _alembic_config(), monkeypatch_session(), pg_url(), MonkeyPatch, Start Postgres, point settings at it, yield the asyncpg URL., The tier requirement: alembic upgrade head then downgrade base, both clean., test_migration_applies_up_and_down(), _tables() (+5 more)

### Community 90 - "AdmitFlow"
Cohesion: 0.29
Nodes (7): AdmitFlow, Current status, Demonstration and submission, Development, Product scope, Stack, Student-first course guidance

### Community 91 - "pathlib"
Cohesion: 0.18
Nodes (9): convert_pdf(), main(), Path, Single-use PDF parser. Reads stdin; emits bounded JSON, never raw diagnostics., Hash the tested code/configuration without reading secrets or runtime data., math, pathlib, pypdf (+1 more)

### Community 92 - "retrieval.py"
Cohesion: 0.32
Nodes (7): numeric_values(), BaseModel, Bounded query resolution for approved evidence; never turn queries into facts., ResolvedQuestion, RetrievalQuery, Decimal, unicodedata

### Community 93 - "test_decision_reranking.py"
Cohesion: 0.24
Nodes (15): chunks(), Intent, asyncio, BaseModel, MonkeyPatch, parametrize, UUID, Typed OpenAI decisions and bounded, tenant-safe evidence ranking. (+7 more)

### Community 94 - "Local Telegram/OpenAI runtime"
Cohesion: 0.25
Nodes (8): Configuration and data services, Delivery budget operation, Local Telegram/OpenAI runtime, Migrate and seed, Optional reminders and scheduler, Packaging and release limits, Run the processes, Validate and recover

### Community 95 - "AllProvidersFailedError"
Cohesion: 0.09
Nodes (27): decide(), Any, Typed decisions through the existing OpenAI-only provider boundary., Validate structured model output; refusal/malformed output is never a decision.…, AllProvidersFailedError, Exception, Raised when the entire LLM fallback chain is exhausted., _deterministic_check() (+19 more)

### Community 96 - "Git & GitHub Workflow"
Cohesion: 0.12
Nodes (15): build(), Rebuild the committed, fictional digital-PDF fixture with reportlab., Branching model — feature branch → PR → `main`, Commits — Conventional Commits, small and coherent, Git & GitHub Workflow, Merging, No AI attribution — the human is the sole author  ⚠️, Pull Requests (+7 more)

### Community 97 - "package.json"
Cohesion: 0.22
Nodes (8): name, private, version, react-dom, @types/node, @types/react, @types/react-dom, typescript

### Community 98 - "inbound"
Cohesion: 0.28
Nodes (8): callback(), test_budget_pause_does_not_spend_a_reminder_and_stop_cancels_it(), exercise(), test_explicit_consent_and_stop_during_staff_takeover(), exercise(), inbound(), UUID, exercise()

### Community 99 - "@playwright/test"
Cohesion: 0.18
Nodes (5): ref_node_child_process, ref_node_crypto, ref_node_fs, ref_node_path, @playwright/test

### Community 100 - "AGENTS.md"
Cohesion: 0.25
Nodes (7): AIBoomi Startup Weekend handoff, How we build — read the handbook, Knowledge graph, Quick commands (from `backend/`), The rules you cannot skip, What this project is, Workflow triggers

### Community 101 - "Security & Production Readiness"
Cohesion: 0.18
Nodes (11): Dependency & secret scanning, Deploy & rollback, External surfaces, Guardrails & money, Local full-stack (docker-compose), Multi-tenancy — isolation is a correctness bug if wrong, Observability, PII & data protection (DPDPA) (+3 more)

### Community 102 - "fake_embeddings"
Cohesion: 0.19
Nodes (11): fake_embeddings(), Any, MonkeyPatch, test_duplicate_claim_and_abandoned_attempt_recovery(), claims(), paused(), recover(), test_expired_session_rejected() (+3 more)

### Community 103 - "next-env.d.ts"
Cohesion: 0.50
Nodes (3): NOTE: This file should not be edited, frontend_next_types_root_params_d, frontend_next_types_routes_d

### Community 104 - "encrypt_pii"
Cohesion: 0.06
Nodes (69): decrypt_pii(), encrypt_pii(), Encrypt a PII string, returning a url-safe base64 Fernet token. Fernet is…, Decrypt a token produced by :func:`encrypt_pii`. Raises…, Trusted bot-to-institution mapping; token is application-encrypted., TelegramBot, resumed_status(), load_memory() (+61 more)

### Community 105 - "ADR-009: Application-Layer PII Encryption and Audit Logging"
Cohesion: 0.15
Nodes (12): DatabaseNotConfiguredError, RuntimeError, Raised when a DB session is requested but ``DATABASE_URL`` is unset., ADR-009: Application-Layer PII Encryption and Audit Logging, Alternatives Considered, Consequences, Context, Decision (+4 more)

### Community 106 - "layout.tsx"
Cohesion: 0.25
Nodes (5): frontend_app_globals, metadata, config, @fontsource-variable/dm-sans, next

### Community 108 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, lint, record:demo, start, test:e2e:live, typecheck

### Community 109 - "backend/README.md"
Cohesion: 0.13
Nodes (14): Contextual retrieval and reference scope, Isolated full-stack Compose, Outbound integrations and live notifications, Staff access and privacy operations, Typed OpenAI decisions and required reranking, Explicit Telegram receiver, Isolated local full-stack runtime, Stop and recover (+6 more)

### Community 110 - "text"
Cohesion: 0.29
Nodes (6): Staff takeover and reviewed co-pilot, ready(), text(), old(), test_budget_migration_preserves_existing_institution(), before()

### Community 111 - "payments/conversation.py"
Cohesion: 0.16
Nodes (23): button(), discount_action(), order_reply(), payment_action(), preview(), Any, AsyncSession, UUID (+15 more)

### Community 112 - "test_knowledge_workspace.py"
Cohesion: 0.09
Nodes (40): asyncio, Application-layer PII protection: symmetric encryption + deterministic hashing.…, ConversationEvent, ConversationReply, Bounded bulk model context; reset boundaries preserve the staff audit trail., Bounded chronological transcript across inbound, replies and standalone…, Institution document extraction, durable ingestion and retrieval., Bounded live FAQ evaluation on the fictional demo tenant; no messages or writes. (+32 more)

### Community 113 - "models/__init__.py"
Cohesion: 0.08
Nodes (64): Base, IdMixin, Declarative base, metadata naming convention, and shared column mixins. Every…, Declarative base shared by every AdmitFlow model., UUID primary key with an application-side default. UUIDs avoid cross-tenant…, Server-side created/updated timestamps., Row-level tenant scoping (ADR-003). Mixed into every tenant-scoped table., TenantMixin (+56 more)

### Community 114 - "Quality Gates — Definition of Done"
Cohesion: 0.33
Nodes (6): CI mirrors this exactly, Fast iteration vs the gate, Quality Gates — Definition of Done, The baseline gate (every change), The enforced-numbers ledger, The tiers — add gates by what the change touches

### Community 115 - "TelegramClient"
Cohesion: 0.11
Nodes (21): private_send(), Any, RuntimeError, Ephemeral feedback never delays, retries or fails the durable conversation., TelegramAPIError, TelegramClient, pulse(), Any (+13 more)

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
Nodes (16): _flush_engine_state(), handle_turn(), _load_engine_state(), Any, AsyncSession, Engine Dispatcher (Task 8 & 17). This module contains the main entry point for…, Load EngineState from DB records., Flush mutations back to DB records. (+8 more)

### Community 120 - "Settings"
Cohesion: 0.14
Nodes (25): hash_phone(), Return a deterministic keyed hash of a phone number for lookup/dedup. Keyed…, Environment-backed application configuration., Settings, configured_keys(), MonkeyPatch, Unit tests for application-layer PII protection (encrypt/decrypt + phone hash)., Point ``security.get_settings`` at settings with the crypto keys set. (+17 more)

### Community 121 - "parse_callback"
Cohesion: 0.21
Nodes (14): is_reset_event(), Any, AsyncSession, reset_reply(), cancel_queued(), note_inbound(), preference_reply(), Any (+6 more)

### Community 122 - "Detail"
Cohesion: 0.26
Nodes (11): Detail, BaseModel, Only explicitly supplied application details may be reused in an encrypted…, validated_details(), ApplicationTurn, BaseModel, test_multiple_details_and_corrections_fill_only_evidenced_fields(), interpret() (+3 more)

### Community 123 - "signin"
Cohesion: 0.10
Nodes (19): test_local_cohort_counts_conversions_and_observed_stages(), test_tenant_is_derived_from_session_and_period_is_bounded(), test_zero_filled_weekly_buckets_and_empty_rates(), test_downloads_roles_datasets_limits_and_tenants(), test_search_pages_are_bounded_and_do_not_drop_or_repeat_records(), seed(), test_search_scope_validation_and_audit(), Any (+11 more)

### Community 124 - "WhatsApp readiness check — October 22, 2026"
Cohesion: 0.15
Nodes (13): Decision so far, Delivery diagnosis and configuration repair (October 23, approximately 00:16 IST), Evidence collected before configuration, Final Postman retry (October 23), Live checkpoint (approximately 22:54 IST), Missing-reply investigation (approximately 22:59 IST), New test account configuration (October 23, approximately 09:45 IST), Next live checks and evidence required (+5 more)

### Community 125 - "Reply"
Cohesion: 0.11
Nodes (28): action(), application_action(), collect_application(), prompt(), Any, AsyncSession, Button, GroundingSource (+20 more)

### Community 126 - "pytest"
Cohesion: 0.12
Nodes (16): get_redis(), Redis, RuntimeError, Shared async Redis client for application code. Carry-over prerequisite #1: the…, Raised when Redis is needed but ``REDIS_URL`` is unset in settings., Return the process-wide async Redis client singleton. The client is created…, RedisNotConfiguredError, Local operational commands with secrets entered through protected prompts. (+8 more)

### Community 127 - "DraftContent"
Cohesion: 0.47
Nodes (4): DraftContent, DraftDecision, BaseModel, field_validator

### Community 128 - "payments.tsx"
Cohesion: 0.32
Nodes (6): label(), money(), outcomes, Payment, Payments(), statuses

### Community 129 - "download"
Cohesion: 0.47
Nodes (6): download(), export_rows(), ExportRequest, Db, post, Response

### Community 130 - "ADAPTIVE_GUIDANCE_RESEARCH.md"
Cohesion: 0.11
Nodes (15): ADR-013: Adaptive, student-first course guidance, Consequences, Context, Decision, ADR-015: Supportive guidance and contextual answer controls, Consequences and limits, Context, Decision (+7 more)

### Community 131 - "Knowledge"
Cohesion: 0.44
Nodes (9): refresh(), api(), Knowledge(), action(), assignScope(), login(), search(), upload() (+1 more)

### Community 132 - "send_reply"
Cohesion: 0.17
Nodes (6): process_telegram_event(), task, send_telegram_reply(), send_reply(), test_shared_budget_preserves_queues_and_settings_wake_deliveries(), second()

### Community 133 - "env.py"
Cohesion: 0.22
Nodes (9): do_run_migrations(), Connection, Alembic migration environment (async). Reads the database URL from application…, Emit SQL to stdout without a live DB connection., Run migrations against a live database via an async engine., run_migrations_offline(), run_migrations_online(), logging_config (+1 more)

### Community 135 - "write_audit_log"
Cohesion: 0.08
Nodes (33): alembic_config, AsyncSession, UUID, Audit-log write helper. :func:`write_audit_log` is the one path significant…, Append one entry to ``audit_logs`` on ``session``; return it flushed, not…, write_audit_log(), AuditLog, One recorded significant action (state change, payment, deletion, takeover).… (+25 more)

### Community 136 - "prepare"
Cohesion: 0.16
Nodes (13): prepare(), Any, MonkeyPatch, parametrize, test_clear_escalation_records_request_outside_hours_without_a_model(), unavailable(), test_copilot_provider_failure_never_queues_a_message(), test_copilot_requires_review_rejects_stale_and_deduplicates_approval() (+5 more)

### Community 137 - "page.tsx"
Cohesion: 0.12
Nodes (13): DeliveryBudget(), Usage, Exports(), Configuration, Integrations(), Request, Doc, errors (+5 more)

### Community 138 - "AdmitFlow Backend"
Cohesion: 0.18
Nodes (11): Admissions analytics, AdmitFlow Backend, Application payments, Configuration, Consented follow-up reminders, Current implementation and verification, Institution knowledge workspace, Local development (+3 more)

### Community 140 - "RuleOperator"
Cohesion: 0.18
Nodes (17): Qualification-rule comparison operators (SPEC §7.4). Evaluated…, RuleOperator, ExtractionResponse, BaseModel, Qualification Node (Task 15). Extracts rule fields using the LLM and runs…, Structured output expected from the LLM when extracting fields., _coerce_values(), evaluate_rule() (+9 more)

### Community 141 - "identity_database"
Cohesion: 0.43
Nodes (7): identity_database(), Use a disposable pgvector database; never mutate the demo database., test_downgrade_preserves_legacy_rows_and_refuses_to_destroy_telegram_data(), insert_rows(), inspect_and_clean(), remove_test_bot(), verify_legacy()

### Community 142 - "verify_compose.py"
Cohesion: 0.36
Nodes (7): argparse, compose(), Verify the isolated local Compose stack without external API calls or sends., seed_credentials(), verify(), subprocess, websockets_asyncio_client

### Community 143 - "add_institution_knowledge_workspace_b627da2f7e11.py"
Cohesion: 0.40
Nodes (4): Column, DateTime, _timestamps(), upgrade()

### Community 144 - "exports.py"
Cohesion: 0.33
Nodes (9): clean(), Audited institution exports, with explicit limits and spreadsheet-safe text., render_csv(), render_xlsx(), Download encoding prevents formulas while preserving international phone…, test_downloads_never_treat_user_text_as_formulas(), csv, openpyxl (+1 more)

### Community 145 - "test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment"
Cohesion: 0.19
Nodes (10): payments(), Any, get, Any, MonkeyPatch, test_absent_link_does_not_clear_uncertainty_or_authorize_retry(), test_known_configuration_failure_can_only_requeue_same_bounded_invoice(), test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment() (+2 more)

### Community 146 - "get_sessionmaker"
Cohesion: 0.16
Nodes (20): async_sessionmaker, get_session(), get_sessionmaker(), AsyncSession, Return the process-wide async session factory., FastAPI dependency yielding a session that closes after the request., recover_payments(), main() (+12 more)

### Community 147 - "notifications.tsx"
Cohesion: 0.33
Nodes (4): labels, Notice, Notifications(), Snapshot

### Community 148 - "AdmitFlow — Task List"
Cohesion: 0.25
Nodes (8): AdmitFlow — Task List, AIBoomi Startup Weekend session handoff (2026-10-22), Current direction and hackathon resources (2026-10-23), Final Postman diagnostic (October 23, executed; delivery blocked), Readiness blocker: idle Redis worker restart (in progress), Readiness tunnel setup (in progress), Test-number delivery diagnosis (October 23, blocked on Meta account restriction), WhatsApp readiness check (2026-10-22, in progress)

### Community 149 - "index_known_name"
Cohesion: 0.40
Nodes (5): index_known_name(), Connection, Mapper, Keep index updates atomic with encrypted names, including name removal., listens_for

### Community 150 - "test_webhook.py"
Cohesion: 0.38
Nodes (6): test_tunnel_app_keeps_webhook_verification(), app(), client(), mock_settings(), FastAPI, Tests for the Meta WhatsApp webhook endpoints (Task 5).

### Community 151 - "test_qualification.py"
Cohesion: 0.27
Nodes (11): AsyncSession, Run the qualification loop., run_qualification(), MockResult, Any, asyncio, test_qualification_extracts_and_fails(), test_qualification_extracts_and_passes() (+3 more)

### Community 152 - "test_crm_exports.py"
Cohesion: 0.31
Nodes (8): main(), AsyncSession, UUID, Backfill encrypted lead names from latest submitted forms and rebuild blind…, reindex_batch(), Real database CRM lookup, index maintenance, export roles and isolation., test_index_rename_clear_and_legacy_backfill(), exercise()

### Community 153 - "record-demo.mjs"
Cohesion: 0.40
Nodes (4): credentials, headers, journey, target

### Community 154 - "scheduler.py"
Cohesion: 0.21
Nodes (12): dispatch_pending(), recovery_loop(), dispatch_due(), main(), Produce due reminder jobs and recover queued deliveries; safe to run after…, run(), purge_retained(), datetime (+4 more)

### Community 155 - "add_conversation_runtime_714f092da3b8.py"
Cohesion: 0.50
Nodes (3): columns(), Column, upgrade()

### Community 156 - "fixture"
Cohesion: 0.20
Nodes (9): fixture(), Course, crm_data(), event_dependencies(), privacy_dependencies(), mock_settings(), MonkeyPatch, Ensure all three models are configured for fallback testing. (+1 more)

### Community 157 - "payment_webhook"
Cohesion: 0.29
Nodes (7): verify_webhook(), payment_webhook(), Db, post, Request, UUID, test_webhook_signature_uses_raw_body_and_rejects_tampering()

### Community 158 - "durable_payments_outbound_f129a064c5e8.py"
Cohesion: 0.50
Nodes (3): common(), Column, upgrade()

### Community 159 - "deliver"
Cohesion: 0.40
Nodes (5): deliver(), UUID, task, Integration queue messages contain identifiers only., send_webhook()

### Community 160 - "reconcile"
Cohesion: 0.61
Nodes (8): locked(), owned(), provider(), Db, post, UUID, reconcile(), retry()

### Community 161 - "Phase 3–4 addition (see ADR-008)"
Cohesion: 0.29
Nodes (7): Phase 3–4 addition (see ADR-008), Task 40: `decide()` System-1 decision-layer abstraction, Task 41: Distill decisions into self-hosted Laya (post-demo), Task 42.1: Complex Document Parsing & Semantic Chunking, Task 42.2: Contextual Query Rewriting, Task 42.3: Pluggable Reranker (Cohere API vs Local), Task 42: Advanced RAG Strategy (ADR-011)

### Community 162 - "Phase 4: Advanced Bot Features"
Cohesion: 0.29
Nodes (7): Phase 4: Advanced Bot Features, Task 18: Application form collection node, Task 19: Razorpay integration, Task 20: Human handoff + co-pilot mode, Task 21: Cold lead re-engagement worker, Task 22: WhatsApp rate-limit tracking, Task 23: Langfuse tracing integration

### Community 163 - "erase_inquiry"
Cohesion: 0.27
Nodes (10): erase(), erase_inquiry(), EraseRequest, in_flight(), AsyncSession, BaseModel, Db, delete (+2 more)

### Community 164 - "docs/event/SUBMISSION_PLAN.md"
Cohesion: 0.10
Nodes (15): AI Impact Statement, Data, model and asset provenance, Student-to-staff demonstration, AdmitFlow pitch deck, Slide 1: AdmitFlow, Slide 2: The admissions handoff, Slide 3: A working institution workspace, Slide 4: Answers from approved documents (+7 more)

### Community 165 - "Language review packet"
Cohesion: 0.40
Nodes (5): Current templates, Language review packet, Live exercise, Reference clarification, Reminder consent and outreach copy

### Community 166 - "11. Human-in-the-Loop (Full Workflow)"
Cohesion: 0.40
Nodes (5): 11.1 Auto-Escalation Triggers, 11.2 Co-pilot Mode, 11.3 Business Hours, 11.4 Never Escalate, 11. Human-in-the-Loop (Full Workflow)

### Community 167 - "Phase 6: Production Hardening"
Cohesion: 0.33
Nodes (6): Phase 6: Production Hardening, Task 35: Sentry error monitoring, Task 36: Delete My Data endpoint, Task 37: Data retention auto-cleanup, Task 38: Docker Compose for local development, Task 39: Production deployment

### Community 168 - "Cursor"
Cohesion: 0.40
Nodes (4): Cursor, BaseModel, datetime, field_validator

### Community 169 - "Phase 1: Foundation"
Cohesion: 0.40
Nodes (5): Phase 1: Foundation, Task 1: Initialize Python project, FastAPI, settings, and Docker, Task 2: PostgreSQL schema (SQLAlchemy + Alembic), Task 3: TaskIQ + Redis broker setup, Task 4: PII encryption utilities and audit log infrastructure

### Community 170 - ".__call__"
Cohesion: 0.40
Nodes (3): Receive, Scope, Send

### Community 171 - "test_workspace_limits.py"
Cohesion: 0.11
Nodes (19): embed_chunks(), Use the configured OpenAI model with the database's explicit 1536 dimensions., main(), Probe, BaseModel, Bounded live checks; print sanitized results without credentials or update…, validate(), check_login_limit() (+11 more)

### Community 172 - "integration/conftest.py"
Cohesion: 0.50
Nodes (3): isolated_local_login_windows(), MonkeyPatch, Keep development-only throttle state independent across database test cases.

### Community 173 - "PaymentProviderError"
Cohesion: 0.15
Nodes (13): AsyncBaseTransport, PaymentLink, PaymentProviderError, BaseModel, Exception, field_validator, Read an existing exact reference; absence never authorizes another creation., Any (+5 more)

### Community 174 - "process_payment"
Cohesion: 0.50
Nodes (4): process_payment(), create_payment_link(), task, Payment-link creation runs after the requesting conversation transaction…

### Community 175 - "Q: What you need to do is i need to present the this project before the jury. First explain the overall structure the stack what things used where used . From A to Z things. that i can answer anything if they question."
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: What you need to do is i need to present the this project before the jury. First explain the overall structure the stack what things used where used . From A to Z things. that i can answer anything if they question., Source Nodes

### Community 177 - "record_stage_changes"
Cohesion: 0.50
Nodes (4): Any, Record persisted ORM transitions atomically; never infer an earlier stage., record_stage_changes(), Session

### Community 178 - "ADR-014: Natural collection, context reset and responsive replies"
Cohesion: 0.50
Nodes (3): ADR-014: Natural collection, context reset and responsive replies, Decision, Evidence and limits

### Community 179 - "2. Boundaries & Invariants"
Cohesion: 0.50
Nodes (4): 2. Boundaries & Invariants, Always Do, Ask First, Never Do

### Community 180 - "3. Tech Stack & Commands"
Cohesion: 0.50
Nodes (4): 3. Tech Stack & Commands, Deployment, Hybrid Architecture, Key Commands

### Community 181 - "8. RAG (Retrieval-Augmented Generation)"
Cohesion: 0.50
Nodes (4): 8.1 Per-Institution Knowledge Base, 8.2 Retrieval Pipeline, 8.3 RAG Guardrail, 8. RAG (Retrieval-Augmented Generation)

### Community 183 - "tasks/processing.py"
Cohesion: 0.12
Nodes (15): ping(), process_inbound_message(), Any, task, Background tasks for message processing. For now this module holds only the…, Smoke-test task: returns ``{"result": payload}``. Enqueued from the…, Process an inbound WhatsApp message (Task 17). This is a placeholder for the…, Tests for the TaskIQ broker setup and task execution (Task 3). All tests run… (+7 more)

### Community 185 - "AdmitFlow execution and demonstration checklist"
Cohesion: 0.67
Nodes (3): AdmitFlow execution and demonstration checklist, Build and verify, Demonstrate and submit

## Knowledge Gaps
- **441 isolated node(s):** `admitflow-backend`, `fs`, `path`, `crypto`, `root` (+436 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1232 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CRM search and institution downloads` connect `review` to `test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment`, `lead_statement`, `backend/README.md`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Why does `write_audit_log()` connect `write_audit_log` to `download`, `lead_statement`, `analytics`, `send_reply`, `journey.py`, `review`, `transport.py`, `exports.py`, `test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment`, `get_sessionmaker`, `test_expired_lease_recovery_cap_and_configuration_cancellation`, `scheduler.py`, `payment_webhook`, `sqlalchemy`, `reconcile`, `management.py`, `outreach/followups.py`, `erase_inquiry`, `Phase 1: Foundation`, `knowledge/processing.py`, `process_payment`, `record_stage_changes`, `RazorpayClient`, `hash_password`, `api.py`, `encrypt_pii`, `payments/conversation.py`, `test_knowledge_workspace.py`, `models/__init__.py`, `parse_callback`, `Reply`?**
  _High betweenness centrality (0.088) - this node is a cross-community bridge._
- **Why does `LeadStatus` connect `LeadStatus` to `lead_statement`, `analytics`, `journey.py`, `write_audit_log`, `review`, `RuleOperator`, `get_engine`, `test_qualification.py`, `test_crm_exports.py`, `test_expired_lease_recovery_cap_and_configuration_cancellation`, `fixture`, `payment_webhook`, `sqlalchemy`, `outreach/followups.py`, `route`, `record_stage_changes`, `age`, `Course`, `budget.py`, `encrypt_pii`, `payments/conversation.py`, `test_knowledge_workspace.py`, `models/__init__.py`, `dispatcher.py`, `parse_callback`, `Reply`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `encrypt_pii()` (e.g. with `Consequences` and `Decision`) actually correct?**
  _`encrypt_pii()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 23 inferred relationships involving `Reply` (e.g. with `advance_application()` and `request_staff()`) actually correct?**
  _`Reply` has 23 INFERRED edges - model-reasoned connections that need verification._
- **Are the 60 inferred relationships involving `LeadStatus` (e.g. with `record_stage_changes()` and `Lead`) actually correct?**
  _`LeadStatus` has 60 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `Lead` (e.g. with `record_stage_changes()` and `Institution`) actually correct?**
  _`Lead` has 5 INFERRED edges - model-reasoned connections that need verification._