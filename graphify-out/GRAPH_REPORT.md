# Graph Report - admitflow  (2026-10-24)

## Corpus Check
- 350 files · ~199,119 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 15 file(s) not represented in the graph (top: (none) 7, .example 2, .css 2)

## Summary
- 3012 nodes · 8889 edges · 164 communities (143 shown, 21 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 562 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `27cf9dca`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ADR-008: System-1 Decision Layer (Laya / Jev)
- Conversation Engine (hand-rolled dispatcher)
- README.md
- Finalized Production Stack
- journey.py
- analytics
- payments/conversation.py
- test_workspace_limits.py
- RedisMutex
- parse_callback
- ExtractionError
- transport.py
- WhatsAppSender
- DocumentChunk
- PII Encryption & Audit Log
- Razorpay Payment Integration
- get_settings
- admissions.tsx
- contextual_query
- GuidanceMemory
- AIBoomi Startup Weekend Kochi: fresh-session context
- test_telegram_contracts.py
- office_open
- AdmitFlow Backend
- LeadStatus
- Stages
- outreach/followups.py
- TestClient
- run_postman_check.cjs
- Task List
- workspace
- leads.py
- retrieval.py
- management.py
- Code Standards
- Local Telegram/OpenAI runtime
- Event preparation and execution plan
- 7. Core Feature Specifications
- knowledge/processing.py
- main.py
- route
- answer_question
- Hackathon resources for AdmitFlow
- manifest.json
- text
- AdmitFlow: current state and planning baseline
- AdmitFlow: AIBoomi submission plan
- AdmitFlow — Complete Specification
- normalize_e164
- evaluate_supportive_guidance.py
- ADR-011: Required OpenAI passage reranking
- Testing
- check_input_safety
- AdmitFlow project handoff
- detect_intent
- tests/test_telegram_identity.py
- GuidanceInterpretation
- Cursor
- test_rag_node.py
- ADR-010: Triage Fallback Routing (Anti-Spam)
- ADR-012: Telegram and OpenAI for the first complete admissions MVP
- alembic
- 2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md
- compilerOptions
- change_password
- age
- ADR-016: Public programme references and an explicit local demo reset
- write_audit_log
- evaluate_conversation.py
- generate_completion
- guidance.py
- Official source snapshots
- 13. Dashboard Features
- integration/conftest.py
- ADR-013: Adaptive, student-first course guidance
- process_followup
- management.tsx
- ADR-015: Supportive guidance and contextual answer controls
- GuidanceDecision
- PublicCatalogue
- verify.sh
- db/__init__.py
- src/__init__.py
- tasks/__init__.py
- analytics.tsx
- whatsapp/__init__.py
- integration/__init__.py
- admitflow-backend
- session.py
- AdmitFlow
- pathlib
- test_decision_reranking.py
- AllProvidersFailedError
- Git & GitHub Workflow
- package.json
- InputGuardrailResult
- @playwright/test
- AGENTS.md
- Security & Production Readiness
- signin
- next-env.d.ts
- encrypt_pii
- layout.tsx
- frontend/AGENTS.md
- scripts
- backend/README.md
- generate
- TelegramBot
- models/__init__.py
- AGENTS.md
- devDependencies
- applications.tsx
- dependencies
- dispatcher.py
- Settings
- Lead
- tests/test_conversation_readiness.py
- WhatsApp readiness check — October 22, 2026
- Reply
- test_handle_turn_basic_flow
- hash_phone
- payments.tsx
- Adaptive course guidance: evidence and implementation
- Knowledge
- test_shared_budget_preserves_queues_and_settings_wake_deliveries
- env.py
- Course
- process_event
- page.tsx
- reindex_batch
- 20260929_initial_schema_64cfce85009d.py
- RuleOperator
- identity_database
- add_institution_knowledge_workspace_b627da2f7e11.py
- log_delivery_status
- test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment
- get_sessionmaker
- notifications.tsx
- record-demo.mjs
- add_conversation_runtime_714f092da3b8.py
- sqlalchemy
- durable_payments_outbound_f129a064c5e8.py
- AdmitFlow pitch deck
- Language review packet
- 11. Human-in-the-Loop (Full Workflow)
- Phase 5: Dashboard Frontend (Next.js)
- AdmitFlow submission requirements
- RazorpayClient
- Q: What you need to do is i need to present the this project before the jury. First explain the overall structure the stack what things used where used . From A to Z things. that i can answer anything if they question.
- 20261008_add_knowledge_models_for_rag_c470f1ebc811.py
- record_stage_changes
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
- `Task 42.3: Pluggable Reranker (Cohere API vs Local)` --references--> `search_chunks()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/core/rag.py
- `Task 4: PII encryption utilities and audit log infrastructure` --references--> `write_audit_log()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/db/audit.py
- `17.1 Conversation engine — DECIDED: hand-rolled dispatcher` --references--> `handle_turn()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/SPEC.md → backend/src/engine/dispatcher.py
- `Missing-reply investigation (approximately 22:59 IST)` --references--> `process_inbound_message()`  [INFERRED]
  docs/event/READINESS_CHECK.md → backend/src/tasks/processing.py
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

## Communities (164 total, 21 thin omitted)

### Community 0 - "ADR-008: System-1 Decision Layer (Laya / Jev)"
Cohesion: 0.13
Nodes (22): ADR-001: Hybrid Architecture, ADR-004: Dual Memory Architecture, Episodic Memory (messages table), Semantic Memory (lead_facts table), ADR-005: Three-Layer Guardrails and RAG, Three-Layer Guardrails, ADR-006: Code-Owned Qualification and Payments, ADR-007: Finalized Production Stack (+14 more)

### Community 1 - "Conversation Engine (hand-rolled dispatcher)"
Cohesion: 0.25
Nodes (8): Conversation Engine (hand-rolled dispatcher), System-1 decide() Decision Layer, FastAPI WhatsApp Webhook, Langfuse LLM Tracing, pgvector RAG Pipeline, Redis (mutex / dedup / rate-limit), TaskIQ Background Worker, Three-Layer Guardrails

### Community 2 - "README.md"
Cohesion: 0.15
Nodes (12): AI Impact Statement, Data, model and asset provenance, Student-to-staff demonstration, Executed final check, One final WhatsApp check with Postman, Prior-work disclosure, AdmitFlow necessary resources, Planning baseline before Telegram alignment (+4 more)

### Community 3 - "Finalized Production Stack"
Cohesion: 0.18
Nodes (11): ADR-002: Webhook Concurrency and Deduplication, Per-Phone Redis Mutex, Webhook Deduplication (Redis SETNX), ADR-003: Multi-Tenancy Strategy, Multi-Tenancy (Row-Level Isolation), Finalized Production Stack, Fly.io (Backend + Worker + Scheduler), Langfuse Cloud (LLM Tracing) (+3 more)

### Community 4 - "journey.py"
Cohesion: 0.19
Nodes (28): Button, advance_application(), build_reply(), button(), copy(), courses(), ExtractedFact, Extraction (+20 more)

### Community 5 - "analytics"
Cohesion: 0.14
Nodes (21): alias, analytics(), bucket_dates(), count(), percent(), Period, period_window(), Any (+13 more)

### Community 6 - "payments/conversation.py"
Cohesion: 0.27
Nodes (18): button(), discount_action(), order_reply(), payment_action(), preview(), Any, AsyncSession, UUID (+10 more)

### Community 7 - "test_workspace_limits.py"
Cohesion: 0.12
Nodes (15): ASGIApp, Reject oversized multipart streams before they can fill temporary storage., UploadBodyLimit, check_login_limit(), Request, MonkeyPatch, Bound resource use and reject browser cross-origin mutations before database…, test_custom_header_and_origin_required() (+7 more)

### Community 8 - "RedisMutex"
Cohesion: 0.07
Nodes (28): MutexAcquireError, Redis, RuntimeError, Redis distributed mutex with owner-safe release and keepalive (Task 7). Ensures…, Background loop that extends the TTL while the lock is held., Raised when the mutex cannot be acquired after all retries., Async context-manager mutex backed by Redis ``SET NX``. Parameters: redis: An…, Attempt to acquire the lock, retrying up to ``retry_count`` times. (+20 more)

### Community 9 - "parse_callback"
Cohesion: 0.18
Nodes (12): model_history(), Any, AsyncSession, Any, AsyncSession, reset_reply(), parse_callback(), test_model_history_excludes_pre_reset_context_in_one_scoped_query() (+4 more)

### Community 10 - "ExtractionError"
Cohesion: 0.05
Nodes (62): compose(), Verify the isolated local Compose stack without external API calls or sends., seed_credentials(), verify(), blocks(), Markdown sections and table rows stay together within bounded evidence chunks., Keep section ancestry; repeat table headers instead of breaking row…, semantic_chunks() (+54 more)

### Community 11 - "transport.py"
Cohesion: 0.09
Nodes (33): Durable, minimal institution events and signed outbound integrations., destination(), post_event(), PrivateTransportLogs, protect_logs(), public_ip(), LogRecord, HTTPS delivery pins a public resolved address while retaining TLS host… (+25 more)

### Community 12 - "WhatsAppSender"
Cohesion: 0.09
Nodes (22): Any, Send an interactive list message. `sections` is a list of section dicts…, Send a pre-approved template message., Service for sending messages via Meta WhatsApp Cloud API., Post the payload to Meta and extract the created message ID., Meta API expects the phone number without the leading '+'., Send a simple text message. Returns the Meta message ID., Send an interactive message with up to 3 buttons. `buttons` should be a list of… (+14 more)

### Community 13 - "DocumentChunk"
Cohesion: 0.09
Nodes (28): chunk_text(), embed_text(), ingest_document(), Any, AsyncSession, UUID, RAG pipeline core logic (Task 13). Handles ingestion (chunking, embedding),…, Generate embedding for text using configured model. (+20 more)

### Community 16 - "get_settings"
Cohesion: 0.05
Nodes (49): AsyncBroker, get_redis(), Redis, RuntimeError, Shared async Redis client for application code. Carry-over prerequisite #1: the…, Raised when Redis is needed but ``REDIS_URL`` is unset in settings., Return the process-wide async Redis client singleton. The client is created…, RedisNotConfiguredError (+41 more)

### Community 17 - "admissions.tsx"
Cohesion: 0.10
Nodes (19): Admissions(), Detail, Human, Inquiry, labels, Request, RuleEvidence, statusLabel() (+11 more)

### Community 18 - "contextual_query"
Cohesion: 0.13
Nodes (17): contextual_query(), Resolve pronouns/slang using bounded recent turns; uncertainty asks the…, retrieval_query(), evaluate(), main(), Bounded synthetic OpenAI reference resolution; no database writes or sends., MonkeyPatch, parametrize (+9 more)

### Community 19 - "GuidanceMemory"
Cohesion: 0.20
Nodes (31): GuidanceMemory, Note, merge_evidence(), render_decision(), test_optional_exploration_and_failure_do_not_erase_profile(), exercise(), turn(), exercise() (+23 more)

### Community 20 - "AIBoomi Startup Weekend Kochi: fresh-session context"
Cohesion: 0.11
Nodes (19): AIBoomi Startup Weekend Kochi: fresh-session context, Assessment and next decision, Current readiness session (October 22), Event sources and local copies, Existing prototype rule and surprise element, Existing working-tree changes, Fresh-message prompt, Handoff status (+11 more)

### Community 21 - "test_telegram_contracts.py"
Cohesion: 0.06
Nodes (35): private_send(), Acknowledge, current(), live(), Any, AsyncSession, BaseModel, Db (+27 more)

### Community 22 - "office_open"
Cohesion: 0.23
Nodes (10): escalation_reason(), office_open(), datetime, Reason, Deterministic clear support signals and institution-local office hours., parametrize, Clear support signals escalate; office hours never promise an immediate reply., test_clear_escalation_signals() (+2 more)

### Community 23 - "AdmitFlow Backend"
Cohesion: 0.18
Nodes (11): Admissions analytics, AdmitFlow Backend, Application payments, Configuration, Consented follow-up reminders, Current implementation and verification, Institution knowledge workspace, Local development (+3 more)

### Community 24 - "LeadStatus"
Cohesion: 0.11
Nodes (33): LeadStatus, Lead lifecycle states (SPEC §7.3). Where a lead *stands*, not a fixed track —…, AsyncSession, Run the qualification loop., run_qualification(), EngineState, InvalidTransitionError, BaseModel (+25 more)

### Community 25 - "Stages"
Cohesion: 0.13
Nodes (15): 10. Reflect & learn, 1. Understand & spec  (`/spec`), 2. Plan & pick a task  (`/plan`), 3. Branch, 4. Build with TDD  (`/build`, `/test`), 5. Verify (the quality gate), 6. Self-review, then adversarial review  (`/review`), 7. Commit & open the PR (+7 more)

### Community 26 - "outreach/followups.py"
Cohesion: 0.24
Nodes (8): Check, Hook, BaseModel, Lease-backed, consented reminders with fresh-state checks before generation and…, safe_hook(), Explicitly consented, bounded student outreach., Only consented inactive inquiries may receive bounded outreach., test_hook_rejects_urgency_prices_and_external_actions()

### Community 27 - "TestClient"
Cohesion: 0.16
Nodes (8): Any, TestClient, Statuses (read/delivered) have no 'messages' array., GET /api/webhook challenge verification., POST /api/webhook payload processing., sign_payload(), TestWebhookProcessing, TestWebhookVerification

### Community 28 - "run_postman_check.cjs"
Cohesion: 0.20
Nodes (8): collection, config, crypto, fs, keys, newman, path, root

### Community 29 - "Task List"
Cohesion: 0.15
Nodes (13): Checkpoint: Advanced Features, Checkpoint: AI Core, Checkpoint: Dashboard Complete, Checkpoint: Foundation, Checkpoint: Production Ready, Checkpoint: WhatsApp Ingress, Phase 1: Foundation, Phase 2: WhatsApp Ingress (+5 more)

### Community 30 - "workspace"
Cohesion: 0.08
Nodes (29): DiscountType, How a discount code reduces the fee., PaymentOrder, A Razorpay order for an application fee (SPEC §7.10). Amount is DB-sourced…, OutboundMessage, Code-owned application fees and authenticated Razorpay payment processing., workspace(), A student must confirm a fresh code-owned fee quote; retries cannot create… (+21 more)

### Community 31 - "leads.py"
Cohesion: 0.05
Nodes (70): Core cross-cutting concerns: settings, security, schemas, guardrails, tracing., name_tokens(), normalized_phone(), UUID, query_tokens(), Tenant-keyed blind name prefixes; plaintext remains in encrypted columns only., token(), words() (+62 more)

### Community 32 - "retrieval.py"
Cohesion: 0.32
Nodes (7): numeric_values(), BaseModel, Bounded query resolution for approved evidence; never turn queries into facts., ResolvedQuestion, RetrievalQuery, Decimal, unicodedata

### Community 33 - "management.py"
Cohesion: 0.05
Nodes (88): admin_scope(), create_user(), CreateUser, edit_user(), EditUser, Any, BaseModel, Db (+80 more)

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

### Community 38 - "knowledge/processing.py"
Cohesion: 0.08
Nodes (30): encrypt_bytes(), Encrypt uploaded source bytes before persistence, without lossy text decoding., dispatch_pending(), embed_chunks(), process_upload(), UUID, Durable upload claims, bounded embedding and atomic publication of ready…, A database-backed inbox survives enqueue failures and lost worker leases. (+22 more)

### Community 39 - "main.py"
Cohesion: 0.07
Nodes (28): argparse, create_app(), lifespan(), FastAPI, FastAPI application entry point. Boots the API, manages the TaskIQ broker…, Start / stop the TaskIQ broker alongside the FastAPI process. The…, Application factory — builds and configures the FastAPI instance., configure() (+20 more)

### Community 40 - "route"
Cohesion: 0.08
Nodes (58): QualificationRule, A structured eligibility rule evaluated in code, not by the LLM (ADR-006).…, Event, route(), submitted_reply(), callback_data(), UUID, test_english_start_has_no_language_or_forced_course_menu() (+50 more)

### Community 41 - "answer_question"
Cohesion: 0.12
Nodes (19): answer_question(), AmbiguousCourseReference, AsyncSession, Course, UUID, ValueError, question_courses(), More than one active course has the requested name without a selected owner. (+11 more)

### Community 42 - "Hackathon resources for AdmitFlow"
Cohesion: 0.20
Nodes (10): Acceptance before using a resource, Event and release boundaries, Goal, Hackathon resources for AdmitFlow, October 23 Downloads guide: hosted inference access, Participant credits and other support, Suggested allocation and activation order, Useful resources mapped to the plan (+2 more)

### Community 43 - "manifest.json"
Cohesion: 0.20
Nodes (9): SPEC.md, bytes, sha256, tasks/plan.md, bytes, sha256, tasks/todo.md, bytes (+1 more)

### Community 44 - "text"
Cohesion: 0.29
Nodes (6): Staff takeover and reviewed co-pilot, ready(), text(), old(), test_budget_migration_preserves_existing_institution(), before()

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

### Community 49 - "evaluate_supportive_guidance.py"
Cohesion: 0.20
Nodes (12): catalog_status(), Course, evaluate(), main(), Any, Synthetic adaptive guidance through the real composer; no database or Telegram…, Published programmes can support exploration without inventing admissions…, test_reference_programme_cannot_grant_eligibility_even_with_a_batch() (+4 more)

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
Cohesion: 0.15
Nodes (13): AdmitFlow project handoff, Current conversation work: Task 61, Current direction, Current work: Task 62 conversation continuity, Current work: Task 63 supportive adaptive guidance, Current work: Task 64 assistant-led routine inquiries, Current work: Task 65 JAIN Kochi data replacement, Development rules (+5 more)

### Community 54 - "detect_intent"
Cohesion: 0.20
Nodes (15): detect_intent(), Classify the user's intent to route to the correct node. Design Decision: If a…, asyncio, Test routing for course discovery., Test routing for knowledge questions., Test routing for qualification answers., Test routing for human handoff., Test routing for empty messages without calling LLM defaults to discovery. (+7 more)

### Community 55 - "tests/test_telegram_identity.py"
Cohesion: 0.19
Nodes (10): hash_telegram_identifier(), UUID, Private Telegram identity lookup without storing raw identifiers in indexes., Hash an identifier in its tenant/bot/type domain using the lookup secret. This…, MonkeyPatch, parametrize, Telegram identities must be independent of phone numbers and tenant-bound., test_lookup_hash_is_stable_scoped_and_does_not_reveal_identifiers() (+2 more)

### Community 56 - "GuidanceInterpretation"
Cohesion: 0.14
Nodes (22): CourseMatch, GuidanceInterpretation, InterestTheme, ProfileUpdate, BaseModel, Bounded exploratory guidance; evidence notes are not psychometric measurements., StrictModel, StudyFact (+14 more)

### Community 57 - "Cursor"
Cohesion: 0.40
Nodes (4): Cursor, BaseModel, datetime, field_validator

### Community 58 - "test_rag_node.py"
Cohesion: 0.11
Nodes (19): Sanitizer to prevent RAG poisoning. Blocks chunks that contain obvious prompt…, sanitize_chunks(), Discovery Node (Task 12). Presents available courses as WhatsApp interactive…, process_rag_node(), AsyncSession, RAG Node (Task 14). Graph node that retrieves from the knowledge base and…, Retrieve context and answer knowledge questions., RuntimeError (+11 more)

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

### Community 64 - "change_password"
Cohesion: 0.06
Nodes (45): change_password(), issue_session(), Login, logout(), me(), PasswordChange, AsyncSession, BaseModel (+37 more)

### Community 65 - "age"
Cohesion: 0.09
Nodes (25): task, send_followup(), age(), outreach(), parametrize, seed(), test_budget_pause_does_not_spend_a_reminder_and_stop_cancels_it(), exercise() (+17 more)

### Community 66 - "ADR-016: Public programme references and an explicit local demo reset"
Cohesion: 0.40
Nodes (4): ADR-016: Public programme references and an explicit local demo reset, Context, Decision, Evidence and limits

### Community 67 - "write_audit_log"
Cohesion: 0.12
Nodes (32): AsyncSession, UUID, Append one entry to ``audit_logs`` on ``session``; return it flushed, not…, write_audit_log(), assign_scope(), documents(), get_upload(), Any (+24 more)

### Community 68 - "evaluate_conversation.py"
Cohesion: 0.50
Nodes (3): Synthetic collection latency evidence; no database writes or Telegram…, src_engine, statistics

### Community 69 - "generate_completion"
Cohesion: 0.16
Nodes (15): generate_completion(), Any, Generate a completion with automatic provider fallback. Tries the fast model,…, asyncio, parametrize, Test that it returns successfully on the primary model., Test that it falls back to OpenAI if primary OpenAI model fails., Test that AllProvidersFailedError is raised if everything fails. (+7 more)

### Community 70 - "guidance.py"
Cohesion: 0.13
Nodes (30): catalog(), commit_guidance(), guide(), interpret_turn(), load_guidance(), Any, AsyncSession, UUID (+22 more)

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
Cohesion: 0.50
Nodes (4): ADR-013: Adaptive, student-first course guidance, Consequences, Context, Decision

### Community 75 - "process_followup"
Cohesion: 0.20
Nodes (16): activity(), after_send(), before_send(), course_available(), eligible(), generate_hook(), pending(), process_followup() (+8 more)

### Community 76 - "management.tsx"
Cohesion: 0.09
Nodes (16): blank, Discount, Discounts(), Batch, Course, empty, Management(), operators (+8 more)

### Community 77 - "ADR-015: Supportive guidance and contextual answer controls"
Cohesion: 0.50
Nodes (4): ADR-015: Supportive guidance and contextual answer controls, Consequences and limits, Context, Decision

### Community 78 - "GuidanceDecision"
Cohesion: 0.16
Nodes (25): checked_text(), GuidanceDecision, add_response_controls(), answer_labels(), compose_reply(), consume_answer(), needs_progress(), Any (+17 more)

### Community 79 - "PublicCatalogue"
Cohesion: 0.11
Nodes (22): CRM search and institution downloads, Programme, PublicCatalogue, BaseModel, field_validator, model_validator, Self, applications() (+14 more)

### Community 84 - "analytics.tsx"
Cohesion: 0.28
Nodes (7): Analytics(), Conversion, labels, frontend_app_analytics_module, rate(), Report, shortDate()

### Community 89 - "session.py"
Cohesion: 0.06
Nodes (52): alembic_config, AsyncEngine, Dashboard access role (SPEC — admin vs agent)., StaffRole, DatabaseNotConfiguredError, get_engine(), RuntimeError, Async engine and session factory. Built lazily from ``settings.database_url``… (+44 more)

### Community 90 - "AdmitFlow"
Cohesion: 0.29
Nodes (7): AdmitFlow, Current status, Demonstration and submission, Development, Product scope, Stack, Student-first course guidance

### Community 91 - "pathlib"
Cohesion: 0.06
Nodes (29): Expose only the existing Meta webhook through the temporary demo tunnel., Bounded synthetic PDF upload/queue/OpenAI/search check; removes its own upload., Five bounded live embedding searches through the real authenticated staff API., Local operational commands with secrets entered through protected prompts., main(), prepare(), Path, Download only local PDF layout/table assets; no OCR, generation or document… (+21 more)

### Community 93 - "test_decision_reranking.py"
Cohesion: 0.21
Nodes (18): UUID, Reorder only original, safe tenant candidates; never invent text or sources.…, rerank(), chunks(), Intent, asyncio, BaseModel, MonkeyPatch (+10 more)

### Community 95 - "AllProvidersFailedError"
Cohesion: 0.11
Nodes (24): decide(), Any, Typed decisions through the existing OpenAI-only provider boundary., Validate structured model output; refusal/malformed output is never a decision.…, AllProvidersFailedError, Exception, Raised when the entire LLM fallback chain is exhausted., apply_whatsapp_formatting() (+16 more)

### Community 96 - "Git & GitHub Workflow"
Cohesion: 0.12
Nodes (15): build(), Rebuild the committed, fictional digital-PDF fixture with reportlab., Branching model — feature branch → PR → `main`, Commits — Conventional Commits, small and coherent, Git & GitHub Workflow, Merging, No AI attribution — the human is the sole author  ⚠️, Pull Requests (+7 more)

### Community 97 - "package.json"
Cohesion: 0.22
Nodes (8): name, private, version, react-dom, @types/node, @types/react, @types/react-dom, typescript

### Community 98 - "InputGuardrailResult"
Cohesion: 0.22
Nodes (9): _deterministic_check(), InputGuardrailResult, LLMGuardrailResponse, LLMOutputGuardrailResponse, BaseModel, Result of the input guardrail check., Structured output expected from the LLM output classifier., Structured output expected from the LLM classifier. (+1 more)

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
Cohesion: 0.06
Nodes (37): decrypt_bytes(), _fernet(), Authenticate and decrypt source bytes for an authorized ingestion task., test_local_cohort_counts_conversions_and_observed_stages(), test_tenant_is_derived_from_session_and_period_is_bounded(), test_zero_filled_weekly_buckets_and_empty_rates(), Any, test_concurrent_reviews_allocate_one_seat_and_repeated_approval_is_idempotent() (+29 more)

### Community 103 - "next-env.d.ts"
Cohesion: 0.50
Nodes (3): NOTE: This file should not be edited, frontend_next_types_root_params_d, frontend_next_types_routes_d

### Community 104 - "encrypt_pii"
Cohesion: 0.07
Nodes (43): decrypt_pii(), encrypt_pii(), Encrypt a PII string, returning a url-safe base64 Fernet token. Fernet is…, Decrypt a token produced by :func:`encrypt_pii`. Raises…, test_profile_and_facts_survive_encryption_without_selecting_a_course(), exercise(), test_all_aggregates_share_a_snapshot_during_concurrent_arrivals(), interleave() (+35 more)

### Community 106 - "layout.tsx"
Cohesion: 0.25
Nodes (5): frontend_app_globals, metadata, config, @fontsource-variable/dm-sans, next

### Community 108 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, lint, record:demo, start, test:e2e:live, typecheck

### Community 109 - "backend/README.md"
Cohesion: 0.13
Nodes (14): Contextual retrieval and reference scope, Isolated full-stack Compose, Outbound integrations and live notifications, Staff access and privacy operations, Typed OpenAI decisions and required reranking, Explicit Telegram receiver, Isolated local full-stack runtime, Stop and recover (+6 more)

### Community 110 - "generate"
Cohesion: 0.19
Nodes (14): content(), decide(), DraftContent, DraftDecision, DraftRequest, generate(), latest(), Any (+6 more)

### Community 112 - "TelegramBot"
Cohesion: 0.09
Nodes (52): asyncio, Application-layer PII protection: symmetric encryption + deterministic hashing.…, ConversationEvent, ConversationReply, Trusted bot-to-institution mapping; token is application-encrypted., TelegramBot, Bounded bulk model context; reset boundaries preserve the staff audit trail., Institution document extraction, durable ingestion and retrieval. (+44 more)

### Community 113 - "models/__init__.py"
Cohesion: 0.07
Nodes (66): Base, IdMixin, Declarative base, metadata naming convention, and shared column mixins. Every…, Declarative base shared by every AdmitFlow model., UUID primary key with an application-side default. UUIDs avoid cross-tenant…, Server-side created/updated timestamps., Row-level tenant scoping (ADR-003). Mixed into every tenant-scoped table., TenantMixin (+58 more)

### Community 114 - "AGENTS.md"
Cohesion: 0.27
Nodes (6): CI mirrors this exactly, Fast iteration vs the gate, Quality Gates — Definition of Done, The baseline gate (every change), The enforced-numbers ledger, The tiers — add gates by what the change touches

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
Cohesion: 0.08
Nodes (27): _flush_engine_state(), handle_turn(), _load_engine_state(), Any, AsyncSession, Engine Dispatcher (Task 8 & 17). This module contains the main entry point for…, Load EngineState from DB records., Flush mutations back to DB records. (+19 more)

### Community 120 - "Settings"
Cohesion: 0.17
Nodes (15): Environment-backed application configuration., Settings, configured_keys(), MonkeyPatch, Point ``security.get_settings`` at settings with the crypto keys set., Point ``security.get_settings`` at settings with no crypto keys., test_hash_phone_differs_per_pepper_key(), unset_keys() (+7 more)

### Community 121 - "Lead"
Cohesion: 0.17
Nodes (20): Lead, A prospective applicant with optional phone contact and channel identities.…, action(), application_action(), collect_application(), prompt(), Any, AsyncSession (+12 more)

### Community 122 - "tests/test_conversation_readiness.py"
Cohesion: 0.14
Nodes (20): Detail, BaseModel, Only explicitly supplied application details may be reused in an encrypted…, validated_details(), ApplicationTurn, BaseModel, academic_number_supported(), An interest score, phone number or unrelated number is not an academic fact. (+12 more)

### Community 124 - "WhatsApp readiness check — October 22, 2026"
Cohesion: 0.15
Nodes (13): Decision so far, Delivery diagnosis and configuration repair (October 23, approximately 00:16 IST), Evidence collected before configuration, Final Postman retry (October 23), Live checkpoint (approximately 22:54 IST), Missing-reply investigation (approximately 22:59 IST), New test account configuration (October 23, approximately 09:45 IST), Next live checks and evidence required (+5 more)

### Community 125 - "Reply"
Cohesion: 0.12
Nodes (21): GroundingSource, BaseModel, field_validator, Channel-neutral input and validated plain-text reply boundary., Internal evidence persisted in encrypted replies, excluded from channel…, Reply, Case, BaseModel (+13 more)

### Community 126 - "test_handle_turn_basic_flow"
Cohesion: 0.33
Nodes (5): Any, asyncio, patch, sample_whatsapp_payload(), test_handle_turn_basic_flow()

### Community 127 - "hash_phone"
Cohesion: 0.09
Nodes (25): EncryptionKeyNotConfiguredError, hash_phone(), RuntimeError, Raised when a PII helper is used but its key is unset in settings., Return a deterministic keyed hash of a phone number for lookup/dedup. Keyed…, payment_webhook(), Db, post (+17 more)

### Community 128 - "payments.tsx"
Cohesion: 0.32
Nodes (6): label(), money(), outcomes, Payment, Payments(), statuses

### Community 130 - "Adaptive course guidance: evidence and implementation"
Cohesion: 0.29
Nodes (7): Adaptive course guidance: evidence and implementation, Adaptive method, not a required sequence, Asking useful questions, Boundaries and verification, Primary-source research and limits, Product decision, Text, buttons and respectful pacing

### Community 131 - "Knowledge"
Cohesion: 0.44
Nodes (9): refresh(), api(), Knowledge(), action(), assignScope(), login(), search(), upload() (+1 more)

### Community 133 - "env.py"
Cohesion: 0.22
Nodes (9): do_run_migrations(), Connection, Alembic migration environment (async). Reads the database URL from application…, Emit SQL to stdout without a live DB connection., Run migrations against a live database via an async engine., run_migrations_offline(), run_migrations_online(), logging_config (+1 more)

### Community 135 - "Course"
Cohesion: 0.09
Nodes (20): Batch, Course, A program a lead can be qualified for and pay to apply to., A dated intake of a course with finite seats (SPEC §7.5)., Bounded chronological transcript across inbound, replies and standalone…, event_text(), AsyncSession, Human-readable callback summaries without exposing routing or signature details. (+12 more)

### Community 136 - "process_event"
Cohesion: 0.10
Nodes (23): is_reset_event(), process_event(), Serialize by locked lead, then atomically commit memory, result and one reply., callback(), test_explicit_consent_and_stop_during_staff_takeover(), exercise(), inbound(), prepare() (+15 more)

### Community 137 - "page.tsx"
Cohesion: 0.12
Nodes (13): DeliveryBudget(), Usage, Exports(), Configuration, Integrations(), Request, Doc, errors (+5 more)

### Community 138 - "reindex_batch"
Cohesion: 0.40
Nodes (6): main(), AsyncSession, UUID, reindex_batch(), test_index_rename_clear_and_legacy_backfill(), exercise()

### Community 140 - "RuleOperator"
Cohesion: 0.18
Nodes (17): Qualification-rule comparison operators (SPEC §7.4). Evaluated…, RuleOperator, ExtractionResponse, BaseModel, Qualification Node (Task 15). Extracts rule fields using the LLM and runs…, Structured output expected from the LLM when extracting fields., _coerce_values(), evaluate_rule() (+9 more)

### Community 141 - "identity_database"
Cohesion: 0.43
Nodes (7): identity_database(), Use a disposable pgvector database; never mutate the demo database., test_downgrade_preserves_legacy_rows_and_refuses_to_destroy_telegram_data(), insert_rows(), inspect_and_clean(), remove_test_bot(), verify_legacy()

### Community 143 - "add_institution_knowledge_workspace_b627da2f7e11.py"
Cohesion: 0.40
Nodes (4): Column, DateTime, _timestamps(), upgrade()

### Community 144 - "log_delivery_status"
Cohesion: 0.40
Nodes (5): log_delivery_status(), Request, Response, Observe only authenticated status events, without recipient or error text., middleware

### Community 145 - "test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment"
Cohesion: 0.19
Nodes (10): payments(), Any, get, Any, MonkeyPatch, test_absent_link_does_not_clear_uncertainty_or_authorize_retry(), test_known_configuration_failure_can_only_requeue_same_bounded_invoice(), test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment() (+2 more)

### Community 146 - "get_sessionmaker"
Cohesion: 0.06
Nodes (50): async_sessionmaker, get_session(), get_sessionmaker(), AsyncSession, Return the process-wide async session factory., FastAPI dependency yielding a session that closes after the request., deliver(), dispatch_pending() (+42 more)

### Community 147 - "notifications.tsx"
Cohesion: 0.33
Nodes (4): labels, Notice, Notifications(), Snapshot

### Community 153 - "record-demo.mjs"
Cohesion: 0.40
Nodes (4): credentials, headers, journey, target

### Community 155 - "add_conversation_runtime_714f092da3b8.py"
Cohesion: 0.50
Nodes (3): columns(), Column, upgrade()

### Community 157 - "sqlalchemy"
Cohesion: 0.09
Nodes (51): Audit-log write helper. :func:`write_audit_log` is the one path significant…, ApplicationStatus, PaymentStatus, Enumerated types used across the schema. These are Python ``str`` enums mapped…, Payment order lifecycle (SPEC §7.10)., Application review status (SPEC §7.9 / lifecycle)., Application form submissions and their payment orders., Lead, its semantic facts (lead_facts), and episodic messages (ADR-004). (+43 more)

### Community 158 - "durable_payments_outbound_f129a064c5e8.py"
Cohesion: 0.50
Nodes (3): common(), Column, upgrade()

### Community 164 - "AdmitFlow pitch deck"
Cohesion: 0.29
Nodes (7): AdmitFlow pitch deck, Slide 1: AdmitFlow, Slide 2: The admissions handoff, Slide 3: A working institution workspace, Slide 4: Answers from approved documents, Slide 5: AI with institution control, Slide 6: An institution pilot

### Community 165 - "Language review packet"
Cohesion: 0.40
Nodes (5): Current templates, Language review packet, Live exercise, Reference clarification, Reminder consent and outreach copy

### Community 166 - "11. Human-in-the-Loop (Full Workflow)"
Cohesion: 0.40
Nodes (5): 11.1 Auto-Escalation Triggers, 11.2 Co-pilot Mode, 11.3 Business Hours, 11.4 Never Escalate, 11. Human-in-the-Loop (Full Workflow)

### Community 167 - "Phase 5: Dashboard Frontend (Next.js)"
Cohesion: 0.04
Nodes (45): AdmitFlow — Task List, AIBoomi Startup Weekend session handoff (2026-10-22), Current direction and hackathon resources (2026-10-23), Final Postman diagnostic (October 23, executed; delivery blocked), Phase 1: Foundation, Phase 3–4 addition (see ADR-008), Phase 4: Advanced Bot Features, Phase 5: Dashboard Frontend (Next.js) (+37 more)

### Community 168 - "AdmitFlow submission requirements"
Cohesion: 0.50
Nodes (4): AdmitFlow submission requirements, Demonstration, Required artifacts, Truthful claims

### Community 173 - "RazorpayClient"
Cohesion: 0.09
Nodes (32): AsyncBaseTransport, Credentials, PaymentLink, PaymentProviderError, BaseModel, Exception, field_validator, Bounded Razorpay requests; ambiguous link creation is never blindly retried. (+24 more)

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

### Community 183 - "test_worker_broker.py"
Cohesion: 0.25
Nodes (7): Tests for the TaskIQ broker setup and task execution (Task 3). All tests run…, When REDIS_URL is unset the factory should yield an InMemoryBroker., The ping task should run and return the expected payload., Ping without an explicit payload should default to 'pong'., test_broker_is_in_memory_without_redis_url(), test_ping_task_default_payload(), test_ping_task_returns_result()

### Community 185 - "AdmitFlow execution and demonstration checklist"
Cohesion: 0.67
Nodes (3): AdmitFlow execution and demonstration checklist, Build and verify, Demonstrate and submit

## Knowledge Gaps
- **447 isolated node(s):** `admitflow-backend`, `fs`, `path`, `crypto`, `root` (+442 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1252 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CRM search and institution downloads` connect `PublicCatalogue` to `test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment`, `backend/README.md`, `leads.py`?**
  _High betweenness centrality (0.145) - this node is a cross-community bridge._
- **Why does `write_audit_log()` connect `write_audit_log` to `journey.py`, `analytics`, `payments/conversation.py`, `parse_callback`, `transport.py`, `test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment`, `get_sessionmaker`, `test_telegram_contracts.py`, `outreach/followups.py`, `sqlalchemy`, `leads.py`, `management.py`, `knowledge/processing.py`, `Phase 5: Dashboard Frontend (Next.js)`, `RazorpayClient`, `record_stage_changes`, `change_password`, `guidance.py`, `process_followup`, `PublicCatalogue`, `session.py`, `generate`, `TelegramBot`, `models/__init__.py`, `Lead`, `hash_phone`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Why does `AdmitFlow — Task List` connect `Phase 5: Dashboard Frontend (Next.js)` to `WhatsAppSender`, `2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md`, `dispatcher.py`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `encrypt_pii()` (e.g. with `Consequences` and `Decision`) actually correct?**
  _`encrypt_pii()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 23 inferred relationships involving `Reply` (e.g. with `advance_application()` and `request_staff()`) actually correct?**
  _`Reply` has 23 INFERRED edges - model-reasoned connections that need verification._
- **Are the 60 inferred relationships involving `LeadStatus` (e.g. with `record_stage_changes()` and `Lead`) actually correct?**
  _`LeadStatus` has 60 INFERRED edges - model-reasoned connections that need verification._
- **What connects `admitflow-backend`, `fs`, `path` to the rest of the system?**
  _447 weakly-connected nodes found - possible documentation gaps or missing edges._