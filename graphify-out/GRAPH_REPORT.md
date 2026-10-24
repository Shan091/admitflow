# Graph Report - admitflow  (2026-10-24)

## Corpus Check
- 351 files · ~201,923 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 7, .example 2, .css 2)

## Summary
- 3033 nodes · 8905 edges · 179 communities (166 shown, 13 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 562 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `69492e8d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ADR-008: System-1 Decision Layer (Laya / Jev)
- Conversation Engine (hand-rolled dispatcher)
- AdmitFlow Complete Specification
- Finalized Production Stack
- answer_question
- analytics
- payments/conversation.py
- test_workspace_limits.py
- RedisMutex
- parse_callback
- pdf_parser.py
- staff/integrations.py
- WhatsAppSender
- test_rag.py
- PII Encryption & Audit Log
- Razorpay Payment Integration
- get_settings
- admissions.tsx
- retrieval.py
- GuidanceMemory
- AIBoomi Startup Weekend Kochi: fresh-session context
- test_telegram_contracts.py
- office_open
- AdmitFlow Backend
- LeadStatus
- Stages
- outreach/followups.py
- fixture
- run_postman_check.cjs
- Task List
- Reply
- leads.py
- test_crm_search.py
- management.py
- Code Standards
- Local Telegram/OpenAI runtime
- Event preparation and execution plan
- 7. Core Feature Specifications
- get_engine
- main.py
- route
- budget.py
- Hackathon resources for AdmitFlow
- manifest.json
- accounts.py
- AdmitFlow: current state and planning baseline
- AdmitFlow: AIBoomi submission plan
- AdmitFlow — Complete Specification
- normalize_e164
- QualificationRule
- ADR-011: Required OpenAI passage reranking
- Testing
- check_input_safety
- AdmitFlow project handoff
- unittest_mock
- EncryptionKeyNotConfiguredError
- GuidanceInterpretation
- Cursor
- EngineState
- ADR-010: Triage Fallback Routing (Anti-Spam)
- ADR-012: Telegram and OpenAI for the first complete admissions MVP
- alembic
- 2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md
- compilerOptions
- change_password
- age
- ADR-016: Public programme references and an explicit local demo reset
- api.py
- evaluate_conversation.py
- generate_completion
- journey.py
- Official source snapshots
- 13. Dashboard Features
- integration/conftest.py
- ADR-013: Adaptive, student-first course guidance
- process_followup
- management.tsx
- ADR-015: Supportive guidance and contextual answer controls
- guidance_interaction.py
- PublicCatalogue
- verify.sh
- db/__init__.py
- src/__init__.py
- tasks/__init__.py
- analytics.tsx
- whatsapp/__init__.py
- integration/__init__.py
- admitflow-backend
- auth.py
- AdmitFlow
- pathlib
- GuidanceDecision
- test_decision_reranking.py
- signin
- pydantic
- Git & GitHub Workflow
- package.json
- InputGuardrailResult
- @playwright/test
- AGENTS.md
- Security & Production Readiness
- process_upload
- next-env.d.ts
- encrypt_pii
- broker.py
- layout.tsx
- frontend/AGENTS.md
- scripts
- backend/README.md
- copilot.py
- ExtractionError
- test_knowledge_workspace.py
- models/__init__.py
- Quality Gates — Definition of Done
- PaymentProviderError
- devDependencies
- applications.tsx
- dependencies
- dispatcher.py
- decrypt_pii
- Lead
- tests/test_conversation_readiness.py
- pdf_worker.py
- WhatsApp readiness check — October 22, 2026
- test_faq_evaluation.py
- test_handle_turn_basic_flow
- payment_webhook
- payments.tsx
- test_local_runtime.py
- Adaptive course guidance: evidence and implementation
- Knowledge
- process_event
- env.py
- ._post
- TelegramBot
- prepare
- page.tsx
- test_structured_documents.py
- BaseModel
- RuleOperator
- pg_url
- exports.py
- add_institution_knowledge_workspace_b627da2f7e11.py
- test_redis_client.py
- seed
- TelegramAPIError
- notifications.tsx
- ingest_document
- send_message
- crm.py
- reconcile
- AdmitFlow — Task List
- record-demo.mjs
- verify_compose.py
- .__call__
- Phase 4: Advanced Bot Features
- sqlalchemy
- download
- Phase 3–4 addition (see ADR-008)
- Phase 6: Production Hardening
- index_known_name
- Code Owns the Money
- WhatsApp readiness check (2026-10-22, in progress)
- docs/event/SUBMISSION_PLAN.md
- Workspace colour theme
- 11. Human-in-the-Loop (Full Workflow)
- Phase 5: Dashboard Frontend (Next.js)
- test_payment_and_webhook_claims_wait_for_erasure_lock
- RazorpayClient
- Q: What you need to do is i need to present the this project before the jury. First explain the overall structure the stack what things used where used . From A to Z things. that i can answer anything if they question.
- write_audit_log
- ADR-014: Natural collection, context reset and responsive replies
- 2. Boundaries & Invariants
- 3. Tech Stack & Commands
- 8. RAG (Retrieval-Augmented Generation)
- test_worker_broker.py
- AdmitFlow execution and demonstration checklist
- DOCUMENT_REVIEW.md

## God Nodes (most connected - your core abstractions)
1. `encrypt_pii()` - 113 edges
2. `Reply` - 105 edges
3. `write_audit_log()` - 102 edges
4. `LeadStatus` - 100 edges
5. `get_settings()` - 96 edges
6. `Lead` - 95 edges
7. `TelegramBot` - 94 edges
8. `decrypt_pii()` - 85 edges
9. `route()` - 82 edges
10. `Course` - 80 edges

## Surprising Connections (you probably didn't know these)
- `Task 4: PII encryption utilities and audit log infrastructure` --references--> `write_audit_log()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/db/audit.py
- `17.1 Conversation engine — DECIDED: hand-rolled dispatcher` --references--> `handle_turn()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/SPEC.md → backend/src/engine/dispatcher.py
- `Missing-reply investigation (approximately 22:59 IST)` --references--> `process_inbound_message()`  [INFERRED]
  docs/event/READINESS_CHECK.md → backend/src/tasks/processing.py
- `Task 42.3: Pluggable Reranker (Cohere API vs Local)` --references--> `search_chunks()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/core/rag.py
- `Consequences` --references--> `encrypt_pii()`  [INFERRED]
  docs/decisions/ADR-009-pii-encryption-and-audit.md → backend/src/core/security.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Finalized Production Stack Components** — docs_decisions_adr_007_finalized_stack_finalized_stack, docs_decisions_adr_007_finalized_stack_fly_io, docs_decisions_adr_007_finalized_stack_neon, docs_decisions_adr_007_finalized_stack_redis, docs_decisions_adr_007_finalized_stack_langfuse [EXTRACTED 1.00]
- **handle_turn() Per-Turn Pipeline** — spec_hand_rolled_dispatcher, docs_decisions_adr_008_system_1_decision_layer_decide, docs_decisions_adr_005_three_layer_guardrails_three_layer_guardrails, docs_decisions_adr_004_memory_architecture_episodic_memory, spec_code_owns_the_money [EXTRACTED 1.00]
- **System-1 Decision Engine (decide + primitives + models)** — docs_decisions_adr_008_system_1_decision_layer_system_1_decision_layer, docs_decisions_adr_008_system_1_decision_layer_decide, docs_research_system_1_decision_models_laya_jev_choice, docs_research_system_1_decision_models_laya_jev_score, docs_research_system_1_decision_models_laya_jev_noul, docs_research_system_1_decision_models_laya_jev_laya [EXTRACTED 1.00]
- **AdmitFlow AI Core Architecture** — tasks_plan_conversation_engine, tasks_plan_decide_decision_layer, tasks_plan_three_layer_guardrails, tasks_plan_rag_pipeline [INFERRED 0.85]
- **WhatsApp Ingress → Worker → Engine Flow** — tasks_plan_fastapi_webhook, tasks_plan_redis, tasks_plan_taskiq, tasks_plan_conversation_engine [INFERRED 0.85]

## Communities (179 total, 13 thin omitted)

### Community 0 - "ADR-008: System-1 Decision Layer (Laya / Jev)"
Cohesion: 0.16
Nodes (17): ADR-001: Hybrid Architecture, ADR-004: Dual Memory Architecture, Episodic Memory (messages table), Semantic Memory (lead_facts table), ADR-005: Three-Layer Guardrails and RAG, Three-Layer Guardrails, ADR-007: Finalized Production Stack, ADR-008: System-1 Decision Layer (Laya / Jev) (+9 more)

### Community 1 - "Conversation Engine (hand-rolled dispatcher)"
Cohesion: 0.25
Nodes (8): Conversation Engine (hand-rolled dispatcher), System-1 decide() Decision Layer, FastAPI WhatsApp Webhook, Langfuse LLM Tracing, pgvector RAG Pipeline, Redis (mutex / dedup / rate-limit), TaskIQ Background Worker, Three-Layer Guardrails

### Community 2 - "AdmitFlow Complete Specification"
Cohesion: 0.25
Nodes (8): Executed final check, One final WhatsApp check with Postman, AdmitFlow necessary resources, Planning baseline before Telegram alignment, AdmitFlow Complete Specification, AdmitFlow Platform, AdmitFlow Implementation Plan, AdmitFlow Task List

### Community 3 - "Finalized Production Stack"
Cohesion: 0.18
Nodes (11): ADR-002: Webhook Concurrency and Deduplication, Per-Phone Redis Mutex, Webhook Deduplication (Redis SETNX), ADR-003: Multi-Tenancy Strategy, Multi-Tenancy (Row-Level Isolation), Finalized Production Stack, Fly.io (Backend + Worker + Scheduler), Langfuse Cloud (LLM Tracing) (+3 more)

### Community 4 - "answer_question"
Cohesion: 0.19
Nodes (23): answer_question(), build_reply(), copy(), courses(), fee_information(), held_reply(), load_memory(), Any (+15 more)

### Community 5 - "analytics"
Cohesion: 0.14
Nodes (21): alias, analytics(), bucket_dates(), count(), percent(), Period, period_window(), Any (+13 more)

### Community 6 - "payments/conversation.py"
Cohesion: 0.29
Nodes (17): discount_action(), order_reply(), payment_action(), preview(), Any, AsyncSession, UUID, Code-owned fee previews and explicit, conversation-bound payment requests. (+9 more)

### Community 7 - "test_workspace_limits.py"
Cohesion: 0.09
Nodes (22): ASGIApp, Reject oversized multipart streams before they can fill temporary storage., UploadBodyLimit, embed_chunks(), Use the configured OpenAI model with the database's explicit 1536 dimensions., main(), Probe, BaseModel (+14 more)

### Community 8 - "RedisMutex"
Cohesion: 0.07
Nodes (28): MutexAcquireError, Redis, RuntimeError, Redis distributed mutex with owner-safe release and keepalive (Task 7). Ensures…, Background loop that extends the TTL while the lock is held., Raised when the mutex cannot be acquired after all retries., Async context-manager mutex backed by Redis ``SET NX``. Parameters: redis: An…, Attempt to acquire the lock, retrying up to ``retry_count`` times. (+20 more)

### Community 9 - "parse_callback"
Cohesion: 0.18
Nodes (15): is_reset_event(), Any, AsyncSession, reset_reply(), cancel_queued(), note_inbound(), preference_reply(), Any (+7 more)

### Community 10 - "pdf_parser.py"
Cohesion: 0.14
Nodes (15): kill_descendants(), parse_pdf(), Offline PDF child process with per-loop backpressure, memory and time limits., Include Windows venv redirector children and any parser subprocesses., resident_memory(), watch_memory(), Process, parametrize (+7 more)

### Community 11 - "staff/integrations.py"
Cohesion: 0.05
Nodes (51): deliver(), UUID, Durable, minimal institution events and signed outbound integrations., destination(), post_event(), PrivateTransportLogs, protect_logs(), public_ip() (+43 more)

### Community 12 - "WhatsAppSender"
Cohesion: 0.10
Nodes (21): Discovery Node (Task 12). Presents available courses as WhatsApp interactive…, ExtractionResponse, BaseModel, Qualification Node (Task 15). Extracts rule fields using the LLM and runs…, Structured output expected from the LLM when extracting fields., RuntimeError, WhatsApp message sending service (Task 6). Uses httpx2 to call the Meta Graph…, Raised when the Meta Cloud API returns an error response. (+13 more)

### Community 13 - "test_rag.py"
Cohesion: 0.19
Nodes (11): chunk_text(), Sanitizer to prevent RAG poisoning. Blocks chunks that contain obvious prompt…, Section-aware chunks; table rows retain their column and section headers., sanitize_chunks(), asyncio, patch, Unit tests for the RAG pipeline., test_chunk_text() (+3 more)

### Community 16 - "get_settings"
Cohesion: 0.08
Nodes (30): Shared async Redis client for application code. Carry-over prerequisite #1: the…, get_settings(), Application settings singleton. Loads configuration from the environment (and…, Return the process-wide :class:`Settings` singleton., Bounded login throttling; shared Redis when configured, development fallback., process_inbound_message(), Any, Background tasks for message processing. For now this module holds only the… (+22 more)

### Community 17 - "admissions.tsx"
Cohesion: 0.10
Nodes (19): Admissions(), Detail, Human, Inquiry, labels, Request, RuleEvidence, statusLabel() (+11 more)

### Community 18 - "retrieval.py"
Cohesion: 0.11
Nodes (23): contextual_query(), numeric_values(), BaseModel, Bounded query resolution for approved evidence; never turn queries into facts., Resolve pronouns/slang using bounded recent turns; uncertainty asks the…, ResolvedQuestion, retrieval_query(), RetrievalQuery (+15 more)

### Community 19 - "GuidanceMemory"
Cohesion: 0.17
Nodes (35): GuidanceMemory, InterestTheme, Note, ProfileUpdate, BaseModel, Bounded exploratory guidance; evidence notes are not psychometric measurements., StrictModel, StudyFact (+27 more)

### Community 20 - "AIBoomi Startup Weekend Kochi: fresh-session context"
Cohesion: 0.11
Nodes (19): AIBoomi Startup Weekend Kochi: fresh-session context, Assessment and next decision, Current readiness session (October 22), Event sources and local copies, Existing prototype rule and surprise element, Existing working-tree changes, Fresh-message prompt, Handoff status (+11 more)

### Community 21 - "test_telegram_contracts.py"
Cohesion: 0.05
Nodes (43): dispatch_pending(), recovery_loop(), dispatch_due(), Local operational commands with secrets entered through protected prompts., main(), Produce due reminder jobs and recover queued deliveries; safe to run after…, run(), erase() (+35 more)

### Community 22 - "office_open"
Cohesion: 0.23
Nodes (10): escalation_reason(), office_open(), datetime, Reason, Deterministic clear support signals and institution-local office hours., parametrize, Clear support signals escalate; office hours never promise an immediate reply., test_clear_escalation_signals() (+2 more)

### Community 23 - "AdmitFlow Backend"
Cohesion: 0.12
Nodes (16): Admissions analytics, AdmitFlow Backend, Application payments, Configuration, Consented follow-up reminders, Current implementation and verification, Institution knowledge workspace, Local development (+8 more)

### Community 24 - "LeadStatus"
Cohesion: 0.20
Nodes (17): LeadStatus, Lead lifecycle states (SPEC §7.3). Where a lead *stands*, not a fixed track —…, AsyncSession, Run the qualification loop., run_qualification(), parametrize, test_reset_needs_confirmation_and_preserves_business_ownership(), base_state() (+9 more)

### Community 25 - "Stages"
Cohesion: 0.13
Nodes (15): 10. Reflect & learn, 1. Understand & spec  (`/spec`), 2. Plan & pick a task  (`/plan`), 3. Branch, 4. Build with TDD  (`/build`, `/test`), 5. Verify (the quality gate), 6. Self-review, then adversarial review  (`/review`), 7. Commit & open the PR (+7 more)

### Community 26 - "outreach/followups.py"
Cohesion: 0.15
Nodes (13): OutboundMessage, Bounded chronological transcript across inbound, replies and standalone…, Check, Hook, BaseModel, Lease-backed, consented reminders with fresh-state checks before generation and…, Any, test_payment_and_delivery_ownership_dedup_and_safe_downgrade() (+5 more)

### Community 27 - "fixture"
Cohesion: 0.08
Nodes (24): fixture(), Course, crm_data(), event_dependencies(), privacy_dependencies(), settings(), parametrize, test_delivery_status_logs_are_authenticated_and_exclude_pii() (+16 more)

### Community 28 - "run_postman_check.cjs"
Cohesion: 0.20
Nodes (8): collection, config, crypto, fs, keys, newman, path, root

### Community 29 - "Task List"
Cohesion: 0.15
Nodes (13): Checkpoint: Advanced Features, Checkpoint: AI Core, Checkpoint: Dashboard Complete, Checkpoint: Foundation, Checkpoint: Production Ready, Checkpoint: WhatsApp Ingress, Phase 1: Foundation, Phase 2: WhatsApp Ingress (+5 more)

### Community 30 - "Reply"
Cohesion: 0.10
Nodes (18): field_validator, Reply, model_history(), Any, AsyncSession, field_validator, test_greeting_question_pause_and_resume_do_not_become_form_values(), faq() (+10 more)

### Community 31 - "leads.py"
Cohesion: 0.25
Nodes (17): lead_summary(), Any, course_options(), get_lead(), human_requests(), lead_detail(), leads(), Any (+9 more)

### Community 32 - "test_crm_search.py"
Cohesion: 0.20
Nodes (15): Core cross-cutting concerns: settings, security, schemas, guardrails, tracing., name_tokens(), normalized_phone(), UUID, query_tokens(), Tenant-keyed blind name prefixes; plaintext remains in encrypted columns only., token(), words() (+7 more)

### Community 33 - "management.py"
Cohesion: 0.22
Nodes (29): archive_course(), archive_discount(), catalog(), catalog_detail(), course_view(), CourseInput, create_course(), create_discount() (+21 more)

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
Cohesion: 0.20
Nodes (10): 7.10 Payment Integration & Discounts (Razorpay), 7.1 WhatsApp Number Architecture, 7.2 Multi-Tenancy (Row-Level Isolation), 7.3 Lead Lifecycle States, 7.5 Batch & Intake Management, 7.6 Cold Lead Re-engagement, 7.7 Language Support, 7.8 Lead Sources & Outbound (+2 more)

### Community 38 - "get_engine"
Cohesion: 0.15
Nodes (15): AsyncEngine, DatabaseNotConfiguredError, get_engine(), RuntimeError, Raised when a DB session is requested but ``DATABASE_URL`` is unset., Return the process-wide async engine (one pool for the app)., main(), execute() (+7 more)

### Community 39 - "main.py"
Cohesion: 0.08
Nodes (23): log_delivery_status(), Request, Response, Expose only the existing Meta webhook through the temporary demo tunnel., Observe only authenticated status events, without recipient or error text., recovery_loop(), create_app(), lifespan() (+15 more)

### Community 40 - "route"
Cohesion: 0.11
Nodes (42): Event, advance_application(), A confirmed choice may start a draft; submission remains explicitly confirmed., route(), callback_data(), test_english_start_has_no_language_or_forced_course_menu(), exercise(), test_foreign_or_changed_availability_cannot_be_selected() (+34 more)

### Community 41 - "budget.py"
Cohesion: 0.14
Nodes (26): get_redis(), Redis, Return the process-wide async Redis client singleton. The client is created…, day_window(), local_counts(), Any, datetime, UUID (+18 more)

### Community 42 - "Hackathon resources for AdmitFlow"
Cohesion: 0.20
Nodes (10): Acceptance before using a resource, Event and release boundaries, Goal, Hackathon resources for AdmitFlow, October 23 Downloads guide: hosted inference access, Participant credits and other support, Suggested allocation and activation order, Useful resources mapped to the plan (+2 more)

### Community 43 - "manifest.json"
Cohesion: 0.20
Nodes (9): SPEC.md, bytes, sha256, tasks/plan.md, bytes, sha256, tasks/todo.md, bytes (+1 more)

### Community 44 - "accounts.py"
Cohesion: 0.15
Nodes (24): admin_scope(), create_user(), CreateUser, edit_user(), EditUser, Any, BaseModel, Db (+16 more)

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

### Community 49 - "QualificationRule"
Cohesion: 0.15
Nodes (25): QualificationRule, A structured eligibility rule evaluated in code, not by the LLM (ADR-006).…, catalog_status(), interpret_turn(), Course, Interpret first; planning must see corrected facts and recomputed eligibility., request_decision(), evaluate() (+17 more)

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

### Community 54 - "unittest_mock"
Cohesion: 0.18
Nodes (16): detect_intent(), Classify the user's intent to route to the correct node. Design Decision: If a…, asyncio, Test routing for course discovery., Test routing for knowledge questions., Test routing for qualification answers., Test routing for human handoff., Test routing for empty messages without calling LLM defaults to discovery. (+8 more)

### Community 55 - "EncryptionKeyNotConfiguredError"
Cohesion: 0.10
Nodes (22): EncryptionKeyNotConfiguredError, RuntimeError, Raised when a PII helper is used but its key is unset in settings., hash_telegram_identifier(), UUID, Private Telegram identity lookup without storing raw identifiers in indexes., Hash an identifier in its tenant/bot/type domain using the lookup secret. This…, MonkeyPatch (+14 more)

### Community 56 - "GuidanceInterpretation"
Cohesion: 0.21
Nodes (13): GuidanceInterpretation, Any, AsyncSession, UUID, timeline(), interpreted(), test_new_background_information_keeps_useful_discovery_open(), exercise() (+5 more)

### Community 57 - "Cursor"
Cohesion: 0.40
Nodes (4): Cursor, BaseModel, datetime, field_validator

### Community 58 - "EngineState"
Cohesion: 0.10
Nodes (27): process_rag_node(), AsyncSession, RAG Node (Task 14). Graph node that retrieves from the knowledge base and…, Retrieve context and answer knowledge questions., EngineState, InvalidTransitionError, BaseModel, ValueError (+19 more)

### Community 59 - "ADR-010: Triage Fallback Routing (Anti-Spam)"
Cohesion: 0.33
Nodes (5): ADR-010: Triage Fallback Routing (Anti-Spam), Consequences, Context, Decision, Status

### Community 60 - "ADR-012: Telegram and OpenAI for the first complete admissions MVP"
Cohesion: 0.29
Nodes (7): ADR-012: Telegram and OpenAI for the first complete admissions MVP, Consequences, Context, Decision, Implemented runtime boundaries, References and verification, Supersession and preserved decisions

### Community 61 - "alembic"
Cohesion: 0.05
Nodes (9): alembic, columns(), Column, upgrade(), common(), Column, upgrade(), pgvector_sqlalchemy (+1 more)

### Community 62 - "2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md"
Cohesion: 0.25
Nodes (4): Architecture Decisions, Implementation Plan: AdmitFlow, Overview, Risks and Mitigations

### Community 63 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 64 - "change_password"
Cohesion: 0.08
Nodes (37): change_password(), issue_session(), Login, logout(), me(), PasswordChange, AsyncSession, BaseModel (+29 more)

### Community 65 - "age"
Cohesion: 0.13
Nodes (18): age(), parametrize, seed(), test_exactly_two_reminders_then_cold_without_duplicate_delivery(), exercise(), test_existing_inquiries_upgrade_without_invented_consent(), in_flight(), old() (+10 more)

### Community 66 - "ADR-016: Public programme references and an explicit local demo reset"
Cohesion: 0.40
Nodes (4): ADR-016: Public programme references and an explicit local demo reset, Context, Decision, Evidence and limits

### Community 67 - "api.py"
Cohesion: 0.13
Nodes (31): encrypt_bytes(), Encrypt uploaded source bytes before persistence, without lossy text decoding., assign_scope(), documents(), get_upload(), Any, BaseModel, Db (+23 more)

### Community 68 - "evaluate_conversation.py"
Cohesion: 0.50
Nodes (3): Synthetic collection latency evidence; no database writes or Telegram…, src_engine, statistics

### Community 69 - "generate_completion"
Cohesion: 0.20
Nodes (15): generate_completion(), Any, Generate a completion with automatic provider fallback. Tries the fast model,…, asyncio, parametrize, Test that it returns successfully on the primary model., Test that it falls back to OpenAI if primary OpenAI model fails., Test that AllProvidersFailedError is raised if everything fails. (+7 more)

### Community 70 - "journey.py"
Cohesion: 0.15
Nodes (26): RAG pipeline core logic (Task 13). Handles ingestion (chunking, embedding),…, Only explicitly supplied application details may be reused in an encrypted…, catalog(), commit_guidance(), guide(), load_guidance(), Any, AsyncSession (+18 more)

### Community 71 - "Official source snapshots"
Cohesion: 0.50
Nodes (4): Conflicts to confirm, October 23 planning refresh, Official source snapshots, Sources

### Community 72 - "13. Dashboard Features"
Cohesion: 0.22
Nodes (9): 13.1 Authentication, 13.2 Roles & Permissions, 13.3 UI Aesthetic, 13.4 Real-Time Notifications, 13.5 Funnel Analytics, 13.6 Data Export & Integration, 13.7 Document Management (RAG), 13.8 Onboarding (MVP) (+1 more)

### Community 73 - "integration/conftest.py"
Cohesion: 0.50
Nodes (3): isolated_local_login_windows(), MonkeyPatch, Keep development-only throttle state independent across database test cases.

### Community 74 - "ADR-013: Adaptive, student-first course guidance"
Cohesion: 0.40
Nodes (4): ADR-013: Adaptive, student-first course guidance, Consequences, Context, Decision

### Community 75 - "process_followup"
Cohesion: 0.15
Nodes (20): activity(), after_send(), before_send(), course_available(), eligible(), generate_hook(), pending(), process_followup() (+12 more)

### Community 76 - "management.tsx"
Cohesion: 0.09
Nodes (16): blank, Discount, Discounts(), Batch, Course, empty, Management(), operators (+8 more)

### Community 77 - "ADR-015: Supportive guidance and contextual answer controls"
Cohesion: 0.40
Nodes (4): ADR-015: Supportive guidance and contextual answer controls, Consequences and limits, Context, Decision

### Community 78 - "guidance_interaction.py"
Cohesion: 0.12
Nodes (28): checked_text(), CourseMatch, add_response_controls(), answer_labels(), compose_reply(), consume_answer(), needs_progress(), Any (+20 more)

### Community 79 - "PublicCatalogue"
Cohesion: 0.16
Nodes (12): Programme, PublicCatalogue, BaseModel, field_validator, model_validator, Self, dataset(), parametrize (+4 more)

### Community 84 - "analytics.tsx"
Cohesion: 0.28
Nodes (7): Analytics(), Conversion, labels, frontend_app_analytics_module, rate(), Report, shortDate()

### Community 89 - "auth.py"
Cohesion: 0.08
Nodes (40): alembic_config, async_sessionmaker, Dashboard access role (SPEC — admin vs agent)., StaffRole, Institution, Institution (the tenant root) and its staff users., An institution, optionally connected to a legacy WhatsApp number. The tenant…, A dashboard user (admin or agent) belonging to one institution. (+32 more)

### Community 90 - "AdmitFlow"
Cohesion: 0.08
Nodes (24): AdmitFlow, Architecture, Configuration, Contributing, Current reference catalogue, Documentation, Features, For institutions (+16 more)

### Community 91 - "pathlib"
Cohesion: 0.20
Nodes (4): Bounded synthetic PDF upload/queue/OpenAI/search check; removes its own upload., Five bounded live embedding searches through the real authenticated staff API., Hash the tested code/configuration without reading secrets or runtime data., pathlib

### Community 92 - "GuidanceDecision"
Cohesion: 0.13
Nodes (24): GuidanceDecision, test_profile_and_facts_survive_encryption_without_selecting_a_course(), exercise(), plan(), test_recommend_confirm_text_then_batch_and_eligibility(), plan(), parametrize, test_interview_probe_is_replaced_without_an_extra_model_request() (+16 more)

### Community 93 - "test_decision_reranking.py"
Cohesion: 0.16
Nodes (21): PassageRanking, BaseModel, UUID, Bounded OpenAI evidence reranking with a validated baseline fallback., Reorder only original, safe tenant candidates; never invent text or sources.…, rerank(), chunks(), Intent (+13 more)

### Community 94 - "signin"
Cohesion: 0.10
Nodes (18): test_local_cohort_counts_conversions_and_observed_stages(), test_tenant_is_derived_from_session_and_period_is_bounded(), test_zero_filled_weekly_buckets_and_empty_rates(), Any, test_concurrent_reviews_allocate_one_seat_and_repeated_approval_is_idempotent(), test_downloads_roles_datasets_limits_and_tenants(), test_search_scope_validation_and_audit(), Any (+10 more)

### Community 95 - "pydantic"
Cohesion: 0.12
Nodes (20): decide(), Any, Typed decisions through the existing OpenAI-only provider boundary., Validate structured model output; refusal/malformed output is never a decision.…, AllProvidersFailedError, Exception, Bounded OpenAI-only model roles; provider details never escape in errors., Raised when the entire LLM fallback chain is exhausted. (+12 more)

### Community 96 - "Git & GitHub Workflow"
Cohesion: 0.12
Nodes (15): build(), Rebuild the committed, fictional digital-PDF fixture with reportlab., Branching model — feature branch → PR → `main`, Commits — Conventional Commits, small and coherent, Git & GitHub Workflow, Merging, No AI attribution — the human is the sole author  ⚠️, Pull Requests (+7 more)

### Community 97 - "package.json"
Cohesion: 0.22
Nodes (8): name, private, version, react-dom, @types/node, @types/react, @types/react-dom, typescript

### Community 98 - "InputGuardrailResult"
Cohesion: 0.18
Nodes (11): _deterministic_check(), InputGuardrailResult, LLMGuardrailResponse, LLMOutputGuardrailResponse, OutputGuardrailResult, BaseModel, Result of the input guardrail check., Result of the output guardrail check. (+3 more)

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
Nodes (35): decrypt_bytes(), _fernet(), Authenticate and decrypt source bytes for an authorized ingestion task., process_upload(), UUID, Claim once, process outside the transaction, then publish only the current…, ingest_upload(), task (+27 more)

### Community 103 - "next-env.d.ts"
Cohesion: 0.50
Nodes (3): NOTE: This file should not be edited, frontend_next_types_root_params_d, frontend_next_types_routes_d

### Community 104 - "encrypt_pii"
Cohesion: 0.09
Nodes (30): encrypt_pii(), Encrypt a PII string, returning a url-safe base64 Fernet token. Fernet is…, AsyncSession, UUID, reindex_batch(), test_all_aggregates_share_a_snapshot_during_concurrent_arrivals(), interleave(), test_index_rename_clear_and_legacy_backfill() (+22 more)

### Community 105 - "broker.py"
Cohesion: 0.12
Nodes (17): AsyncBroker, _build_broker(), TaskIQ broker singleton. In production (and local dev with Redis running) the…, Construct the right broker based on the current settings. This is a plain…, task, Follow-up jobs carry only tenant and lead identifiers, never student content., send_followup(), task (+9 more)

### Community 106 - "layout.tsx"
Cohesion: 0.25
Nodes (5): frontend_app_globals, metadata, config, @fontsource-variable/dm-sans, next

### Community 108 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, lint, record:demo, start, test:e2e:live, typecheck

### Community 109 - "backend/README.md"
Cohesion: 0.13
Nodes (14): Contextual retrieval and reference scope, Isolated full-stack Compose, Outbound integrations and live notifications, Staff access and privacy operations, Typed OpenAI decisions and required reranking, Explicit Telegram receiver, Isolated local full-stack runtime, Stop and recover (+6 more)

### Community 110 - "copilot.py"
Cohesion: 0.15
Nodes (21): event_text(), AsyncSession, content(), decide(), DraftContent, DraftDecision, DraftRequest, generate() (+13 more)

### Community 111 - "ExtractionError"
Cohesion: 0.22
Nodes (18): extract_file(), ExtractionError, ValueError, Bounded extraction of institution reference documents; never execute uploads., A safe, public error code rather than parser output containing document text., validate_path(), preflight_pdf(), basic_pdf() (+10 more)

### Community 112 - "test_knowledge_workspace.py"
Cohesion: 0.10
Nodes (41): asyncio, ConversationEvent, ConversationReply, Institution document extraction, durable ingestion and retrieval., Durable upload claims, bounded embedding and atomic publication of ready…, Bounded live FAQ evaluation on the fictional demo tenant; no messages or writes., Strict private-chat normalization and token-safe Telegram HTTP transport., TelegramClient (+33 more)

### Community 113 - "models/__init__.py"
Cohesion: 0.07
Nodes (68): Base, IdMixin, Declarative base, metadata naming convention, and shared column mixins. Every…, Declarative base shared by every AdmitFlow model., UUID primary key with an application-side default. UUIDs avoid cross-tenant…, Server-side created/updated timestamps., Row-level tenant scoping (ADR-003). Mixed into every tenant-scoped table., TenantMixin (+60 more)

### Community 114 - "Quality Gates — Definition of Done"
Cohesion: 0.33
Nodes (6): CI mirrors this exactly, Fast iteration vs the gate, Quality Gates — Definition of Done, The baseline gate (every change), The enforced-numbers ledger, The tiers — add gates by what the change touches

### Community 115 - "PaymentProviderError"
Cohesion: 0.15
Nodes (15): PaymentLink, PaymentProviderError, BaseModel, Exception, field_validator, Read an existing exact reference; absence never authorizes another creation., Any, MonkeyPatch (+7 more)

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
Cohesion: 0.09
Nodes (26): _flush_engine_state(), handle_turn(), _load_engine_state(), Any, AsyncSession, Engine Dispatcher (Task 8 & 17). This module contains the main entry point for…, Load EngineState from DB records., Flush mutations back to DB records. (+18 more)

### Community 120 - "decrypt_pii"
Cohesion: 0.13
Nodes (29): decrypt_pii(), hash_phone(), Decrypt a token produced by :func:`encrypt_pii`. Raises…, Return a deterministic keyed hash of a phone number for lookup/dedup. Keyed…, Environment-backed application configuration., Settings, seed(), test_configuration_roles_encryption_and_tenant_ownership() (+21 more)

### Community 121 - "Lead"
Cohesion: 0.21
Nodes (16): Lead, A prospective applicant with optional phone contact and channel identities.…, action(), application_action(), collect_application(), prompt(), Any, AsyncSession (+8 more)

### Community 122 - "tests/test_conversation_readiness.py"
Cohesion: 0.18
Nodes (16): Detail, BaseModel, validated_details(), ApplicationTurn, BaseModel, academic_number_supported(), An interest score, phone number or unrelated number is not an academic fact., test_multiple_details_and_corrections_fill_only_evidenced_fields() (+8 more)

### Community 123 - "pdf_worker.py"
Cohesion: 0.14
Nodes (15): argparse, convert_pdf(), main(), Path, Single-use PDF parser. Reads stdin; emits bounded JSON, never raw diagnostics., main(), prepare(), Path (+7 more)

### Community 124 - "WhatsApp readiness check — October 22, 2026"
Cohesion: 0.15
Nodes (13): Decision so far, Delivery diagnosis and configuration repair (October 23, approximately 00:16 IST), Evidence collected before configuration, Final Postman retry (October 23), Live checkpoint (approximately 22:54 IST), Missing-reply investigation (approximately 22:59 IST), New test account configuration (October 23, approximately 09:45 IST), Next live checks and evidence required (+5 more)

### Community 125 - "test_faq_evaluation.py"
Cohesion: 0.20
Nodes (14): GroundingSource, BaseModel, Channel-neutral input and validated plain-text reply boundary., Internal evidence persisted in encrypted replies, excluded from channel…, Case, cases(), evaluate(), main() (+6 more)

### Community 126 - "test_handle_turn_basic_flow"
Cohesion: 0.33
Nodes (5): Any, asyncio, patch, sample_whatsapp_payload(), test_handle_turn_basic_flow()

### Community 127 - "payment_webhook"
Cohesion: 0.40
Nodes (5): payment_webhook(), Db, post, Request, UUID

### Community 128 - "payments.tsx"
Cohesion: 0.32
Nodes (6): label(), money(), outcomes, Payment, Payments(), statuses

### Community 129 - "test_local_runtime.py"
Cohesion: 0.15
Nodes (14): configure(), main(), Path, Create private isolated local Compose configuration without copying live…, Tests use explicit configuration and never implicitly load developer…, asyncio, MonkeyPatch, Path (+6 more)

### Community 130 - "Adaptive course guidance: evidence and implementation"
Cohesion: 0.29
Nodes (7): Adaptive course guidance: evidence and implementation, Adaptive method, not a required sequence, Asking useful questions, Boundaries and verification, Primary-source research and limits, Product decision, Text, buttons and respectful pacing

### Community 131 - "Knowledge"
Cohesion: 0.44
Nodes (9): refresh(), api(), Knowledge(), action(), assignScope(), login(), search(), upload() (+1 more)

### Community 132 - "process_event"
Cohesion: 0.11
Nodes (13): process_telegram_event(), task, Telegram inbox and outbox jobs contain only internal identifiers., send_telegram_reply(), process_event(), UUID, Serialize by locked lead, then atomically commit memory, result and one reply., send_reply() (+5 more)

### Community 133 - "env.py"
Cohesion: 0.25
Nodes (8): do_run_migrations(), Connection, Alembic migration environment (async). Reads the database URL from application…, Emit SQL to stdout without a live DB connection., Run migrations against a live database via an async engine., run_migrations_offline(), run_migrations_online(), logging_config

### Community 134 - "._post"
Cohesion: 0.17
Nodes (11): Any, Send an interactive list message. `sections` is a list of section dicts…, Send a pre-approved template message., Post the payload to Meta and extract the created message ID., Meta API expects the phone number without the leading '+'., Send a simple text message. Returns the Meta message ID., Send an interactive message with up to 3 buttons. `buttons` should be a list of…, Phase 2: WhatsApp Ingress (+3 more)

### Community 135 - "TelegramBot"
Cohesion: 0.10
Nodes (28): Batch, Course, A program a lead can be qualified for and pay to apply to., A dated intake of a course with finite seats (SPEC §7.5)., Trusted bot-to-institution mapping; token is application-encrypted., TelegramBot, Human-readable callback summaries without exposing routing or signature details., Code-owned course scopes for approved institution references. (+20 more)

### Community 136 - "prepare"
Cohesion: 0.12
Nodes (20): test_budget_pause_does_not_spend_a_reminder_and_stop_cancels_it(), exercise(), inbound(), prepare(), Any, MonkeyPatch, parametrize, UUID (+12 more)

### Community 137 - "page.tsx"
Cohesion: 0.12
Nodes (13): DeliveryBudget(), Usage, Exports(), Configuration, Integrations(), Request, Doc, errors (+5 more)

### Community 138 - "test_structured_documents.py"
Cohesion: 0.19
Nodes (14): blocks(), Markdown sections and table rows stay together within bounded evidence chunks., Keep section ancestry; repeat table headers instead of breaking row…, semantic_chunks(), table_parts(), table_start(), text_parts(), parametrize (+6 more)

### Community 139 - "BaseModel"
Cohesion: 0.23
Nodes (7): BatchInput, Hours, BaseModel, model_validator, Self, RuleInput, SettingsInput

### Community 140 - "RuleOperator"
Cohesion: 0.30
Nodes (12): Qualification-rule comparison operators (SPEC §7.4). Evaluated…, RuleOperator, _coerce_values(), evaluate_rule(), Any, Evaluate a qualification rule deterministically. Args: operator: The…, test_evaluate_rule_in_list(), test_evaluate_rule_missing_extracted_value() (+4 more)

### Community 141 - "pg_url"
Cohesion: 0.19
Nodes (13): _alembic_config(), monkeypatch_session(), pg_url(), MonkeyPatch, Start Postgres, point settings at it, yield the asyncpg URL., The tier requirement: alembic upgrade head then downgrade base, both clean., test_migration_applies_up_and_down(), _tables() (+5 more)

### Community 142 - "exports.py"
Cohesion: 0.30
Nodes (10): clean(), Audited institution exports, with explicit limits and spreadsheet-safe text., render_csv(), render_xlsx(), Download encoding prevents formulas while preserving international phone…, test_downloads_never_treat_user_text_as_formulas(), csv, io (+2 more)

### Community 143 - "add_institution_knowledge_workspace_b627da2f7e11.py"
Cohesion: 0.40
Nodes (4): Column, DateTime, _timestamps(), upgrade()

### Community 144 - "test_redis_client.py"
Cohesion: 0.20
Nodes (8): RuntimeError, Raised when Redis is needed but ``REDIS_URL`` is unset in settings., RedisNotConfiguredError, Tests for the shared async Redis client helper (carry-over prerequisite #1).…, get_redis() singleton behaviour., Calling get_redis() with no REDIS_URL must fail loud., When REDIS_URL is set, get_redis() returns a Redis client., TestGetRedis

### Community 145 - "seed"
Cohesion: 0.13
Nodes (18): payments(), Any, get, test_unconfigured_payments_do_not_offer_a_payment_request_or_staff_handoff(), exercise(), UUID, seed(), exercise() (+10 more)

### Community 146 - "TelegramAPIError"
Cohesion: 0.10
Nodes (24): recover_payments(), RuntimeError, TelegramAPIError, main(), provision_bot(), UUID, One advisory-locked long poller per bot, with durable offsets and queue…, recovery() (+16 more)

### Community 147 - "notifications.tsx"
Cohesion: 0.33
Nodes (4): labels, Notice, Notifications(), Snapshot

### Community 148 - "ingest_document"
Cohesion: 0.22
Nodes (10): embed_text(), ingest_document(), Any, AsyncSession, UUID, Generate embedding for text using configured model., Chunk, embed, and store a document in pgvector., Hybrid search (dense + lexical with RRF). (+2 more)

### Community 149 - "send_message"
Cohesion: 0.33
Nodes (10): active_request(), finish_takeover(), Any, AsyncSession, Db, post, UUID, resume() (+2 more)

### Community 150 - "crm.py"
Cohesion: 0.36
Nodes (7): lead_statement(), LeadFilters, LeadSearch, BaseModel, Select, UUID, Shared bounded CRM filters; search values never belong in URLs or audit details.

### Community 151 - "reconcile"
Cohesion: 0.61
Nodes (8): locked(), owned(), provider(), Db, post, UUID, reconcile(), retry()

### Community 152 - "AdmitFlow — Task List"
Cohesion: 0.25
Nodes (8): AdmitFlow — Task List, AIBoomi Startup Weekend session handoff (2026-10-22), Current direction and hackathon resources (2026-10-23), Phase 1: Foundation, Task 1: Initialize Python project, FastAPI, settings, and Docker, Task 2: PostgreSQL schema (SQLAlchemy + Alembic), Task 3: TaskIQ + Redis broker setup, Task 4: PII encryption utilities and audit log infrastructure

### Community 153 - "record-demo.mjs"
Cohesion: 0.40
Nodes (4): credentials, headers, journey, target

### Community 154 - "verify_compose.py"
Cohesion: 0.43
Nodes (6): compose(), Verify the isolated local Compose stack without external API calls or sends., seed_credentials(), verify(), subprocess, websockets_asyncio_client

### Community 155 - ".__call__"
Cohesion: 0.29
Nodes (4): private_send(), Receive, Scope, Send

### Community 156 - "Phase 4: Advanced Bot Features"
Cohesion: 0.29
Nodes (7): Phase 4: Advanced Bot Features, Task 18: Application form collection node, Task 19: Razorpay integration, Task 20: Human handoff + co-pilot mode, Task 21: Cold lead re-engagement worker, Task 22: WhatsApp rate-limit tracking, Task 23: Langfuse tracing integration

### Community 157 - "sqlalchemy"
Cohesion: 0.08
Nodes (54): Application-layer PII protection: symmetric encryption + deterministic hashing.…, Audit-log write helper. :func:`write_audit_log` is the one path significant…, ApplicationStatus, DiscountType, PaymentStatus, Enumerated types used across the schema. These are Python ``str`` enums mapped…, How a discount code reduces the fee., Payment order lifecycle (SPEC §7.10). (+46 more)

### Community 158 - "download"
Cohesion: 0.47
Nodes (6): download(), export_rows(), ExportRequest, Db, post, Response

### Community 159 - "Phase 3–4 addition (see ADR-008)"
Cohesion: 0.33
Nodes (6): Phase 3–4 addition (see ADR-008), Task 40: `decide()` System-1 decision-layer abstraction, Task 41: Distill decisions into self-hosted Laya (post-demo), Task 42.1: Complex Document Parsing & Semantic Chunking, Task 42.2: Contextual Query Rewriting, Task 42: Advanced RAG Strategy (ADR-011)

### Community 160 - "Phase 6: Production Hardening"
Cohesion: 0.33
Nodes (6): Phase 6: Production Hardening, Task 35: Sentry error monitoring, Task 36: Delete My Data endpoint, Task 37: Data retention auto-cleanup, Task 38: Docker Compose for local development, Task 39: Production deployment

### Community 161 - "index_known_name"
Cohesion: 0.40
Nodes (5): index_known_name(), Connection, Mapper, Keep index updates atomic with encrypted names, including name removal., listens_for

### Community 162 - "Code Owns the Money"
Cohesion: 0.50
Nodes (5): ADR-006: Code-Owned Qualification and Payments, Intent: Admissions Flow and Discounts, Discount Codes, Code Owns Eligibility, Code Owns the Money

### Community 163 - "WhatsApp readiness check (2026-10-22, in progress)"
Cohesion: 0.40
Nodes (5): Final Postman diagnostic (October 23, executed; delivery blocked), Readiness blocker: idle Redis worker restart (in progress), Readiness tunnel setup (in progress), Test-number delivery diagnosis (October 23, blocked on Meta account restriction), WhatsApp readiness check (2026-10-22, in progress)

### Community 164 - "docs/event/SUBMISSION_PLAN.md"
Cohesion: 0.08
Nodes (20): AI Impact Statement, Data, model and asset provenance, Student-to-staff demonstration, Current templates, Language review packet, Live exercise, Reference clarification, Reminder consent and outreach copy (+12 more)

### Community 165 - "Workspace colour theme"
Cohesion: 0.50
Nodes (3): Roles, Verification, Workspace colour theme

### Community 166 - "11. Human-in-the-Loop (Full Workflow)"
Cohesion: 0.40
Nodes (5): 11.1 Auto-Escalation Triggers, 11.2 Co-pilot Mode, 11.3 Business Hours, 11.4 Never Escalate, 11. Human-in-the-Loop (Full Workflow)

### Community 167 - "Phase 5: Dashboard Frontend (Next.js)"
Cohesion: 0.17
Nodes (12): Phase 5: Dashboard Frontend (Next.js), Task 24: Initialize Next.js + dark mode + glassmorphism, Task 25: Authentication (email + password), Task 26: Dashboard home (funnel analytics), Task 27: Leads CRM page, Task 28: Course & batch management, Task 29: Chat takeover + co-pilot UI, Task 30: Document management (RAG) (+4 more)

### Community 173 - "RazorpayClient"
Cohesion: 0.12
Nodes (22): AsyncBaseTransport, Credentials, Bounded Razorpay requests; ambiguous link creation is never blindly retried., RazorpayClient, discounted_amount(), verify_webhook(), process_payment(), main() (+14 more)

### Community 175 - "Q: What you need to do is i need to present the this project before the jury. First explain the overall structure the stack what things used where used . From A to Z things. that i can answer anything if they question."
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: What you need to do is i need to present the this project before the jury. First explain the overall structure the stack what things used where used . From A to Z things. that i can answer anything if they question., Source Nodes

### Community 177 - "write_audit_log"
Cohesion: 0.13
Nodes (21): CRM search and institution downloads, Any, AsyncSession, UUID, Record persisted ORM transitions atomically; never infer an earlier stage., Append one entry to ``audit_logs`` on ``session``; return it flushed, not…, record_stage_changes(), write_audit_log() (+13 more)

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

### Community 183 - "test_worker_broker.py"
Cohesion: 0.18
Nodes (10): ping(), task, Smoke-test task: returns ``{"result": payload}``. Enqueued from the…, Tests for the TaskIQ broker setup and task execution (Task 3). All tests run…, When REDIS_URL is unset the factory should yield an InMemoryBroker., The ping task should run and return the expected payload., Ping without an explicit payload should default to 'pong'., test_broker_is_in_memory_without_redis_url() (+2 more)

### Community 185 - "AdmitFlow execution and demonstration checklist"
Cohesion: 0.67
Nodes (3): AdmitFlow execution and demonstration checklist, Build and verify, Demonstrate and submit

## Knowledge Gaps
- **462 isolated node(s):** `admitflow-backend`, `fs`, `path`, `crypto`, `root` (+457 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1269 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CRM search and institution downloads` connect `write_audit_log` to `seed`, `backend/README.md`, `PublicCatalogue`, `leads.py`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Why does `write_audit_log()` connect `write_audit_log` to `process_event`, `analytics`, `payments/conversation.py`, `TelegramBot`, `parse_callback`, `staff/integrations.py`, `exports.py`, `seed`, `TelegramAPIError`, `send_message`, `test_telegram_contracts.py`, `reconcile`, `AdmitFlow — Task List`, `outreach/followups.py`, `sqlalchemy`, `download`, `leads.py`, `management.py`, `budget.py`, `accounts.py`, `RazorpayClient`, `change_password`, `api.py`, `journey.py`, `process_followup`, `auth.py`, `process_upload`, `copilot.py`, `test_knowledge_workspace.py`, `models/__init__.py`, `Lead`, `payment_webhook`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Why does `get_settings()` connect `get_settings` to `test_local_runtime.py`, `answer_question`, `env.py`, `test_workspace_limits.py`, `TelegramBot`, `pdf_parser.py`, `WhatsAppSender`, `exports.py`, `TelegramAPIError`, `ingest_document`, `test_telegram_contracts.py`, `reconcile`, `outreach/followups.py`, `.__call__`, `sqlalchemy`, `download`, `get_engine`, `main.py`, `route`, `budget.py`, `accounts.py`, `RazorpayClient`, `EncryptionKeyNotConfiguredError`, `change_password`, `api.py`, `generate_completion`, `journey.py`, `process_followup`, `auth.py`, `test_decision_reranking.py`, `pydantic`, `process_upload`, `broker.py`, `test_knowledge_workspace.py`, `decrypt_pii`, `test_faq_evaluation.py`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `encrypt_pii()` (e.g. with `Consequences` and `Decision`) actually correct?**
  _`encrypt_pii()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 23 inferred relationships involving `Reply` (e.g. with `advance_application()` and `request_staff()`) actually correct?**
  _`Reply` has 23 INFERRED edges - model-reasoned connections that need verification._
- **Are the 60 inferred relationships involving `LeadStatus` (e.g. with `record_stage_changes()` and `Lead`) actually correct?**
  _`LeadStatus` has 60 INFERRED edges - model-reasoned connections that need verification._
- **What connects `admitflow-backend`, `fs`, `path` to the rest of the system?**
  _462 weakly-connected nodes found - possible documentation gaps or missing edges._