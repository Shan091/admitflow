# Graph Report - admitflow  (2026-10-24)

## Corpus Check
- 293 files · ~154,157 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 5, .example 2, .css 2)

## Summary
- 2621 nodes · 7259 edges · 159 communities (142 shown, 17 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 455 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0d5b122c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- AdmitFlow Complete Specification
- Conversation Engine (hand-rolled dispatcher)
- AdmitFlow Task List
- Finalized Production Stack
- leads.py
- analytics
- Code Owns the Money
- journey.py
- RedisMutex
- write_audit_log
- TestWhatsAppSender
- staff/integrations.py
- WhatsAppSender
- DocumentChunk
- PII Encryption & Audit Log
- Razorpay Payment Integration
- get_settings
- admissions.tsx
- retrieval.py
- Settings
- AIBoomi Startup Weekend Kochi: fresh-session context
- payments/conversation.py
- exports.py
- Course
- LeadStatus
- Stages
- test_knowledge_workspace.py
- test_webhook.py
- run_postman_check.cjs
- Task List
- get_engine
- test_crm_search.py
- Phase 5: Dashboard Frontend (Next.js)
- management.py
- Code Standards
- outreach/followups.py
- Event preparation and execution plan
- 7. Core Feature Specifications
- preference_reply
- main.py
- knowledge/processing.py
- operations.py
- Hackathon resources for AdmitFlow
- manifest.json
- fastapi
- AdmitFlow: current state and planning baseline
- AdmitFlow: AIBoomi submission plan
- AdmitFlow — Complete Specification
- normalize_e164
- age
- ADR-011: Required OpenAI passage reranking
- Testing
- check_input_safety
- AdmitFlow project handoff
- detect_intent
- EncryptionKeyNotConfiguredError
- RuleOperator
- test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment
- copilot.py
- ADR-010: Triage Fallback Routing (Anti-Spam)
- ADR-012: Telegram and OpenAI for the first complete admissions MVP
- prepare
- compilerOptions
- auth.py
- encrypt_pii
- typing
- api.py
- telegram/service.py
- sqlalchemy
- RazorpayClient
- Official source snapshots
- test_discovery.py
- Reply
- get_sessionmaker
- budget.py
- management.tsx
- hashlib
- test_integrations_notifications.py
- dispatcher.py
- verify.sh
- db/__init__.py
- src/__init__.py
- tasks/__init__.py
- analytics.tsx
- whatsapp/__init__.py
- integration/__init__.py
- admitflow-backend
- signin
- README.md
- decrypt_pii
- workspace
- test_decision_reranking.py
- ADR-009: Application-Layer PII Encryption and Audit Logging
- Institution
- Git & GitHub Workflow
- package.json
- 13. Dashboard Features
- @playwright/test
- AGENTS.md
- Security & Production Readiness
- fake_embeddings
- next-env.d.ts
- payments/webhook.py
- reindex_batch
- layout.tsx
- frontend/AGENTS.md
- scripts
- backend/README.md
- AdmitFlow pitch deck copy
- send_outbound
- TelegramClient
- models/__init__.py
- Quality Gates — Definition of Done
- inbound
- devDependencies
- applications.tsx
- dependencies
- scheduler.py
- test_settings.py
- test_rag_node.py
- guardrails.py
- scope.py
- WhatsApp readiness check — October 22, 2026
- review
- erase_inquiry
- TokenSafeFilter
- payments.tsx
- test_expired_lease_recovery_cap_and_configuration_cancellation
- StaffAccounts
- Knowledge
- test_local_runtime.py
- env.py
- test_shared_budget_preserves_queues_and_settings_wake_deliveries
- pydantic
- event_dependencies
- page.tsx
- AdmitFlow execution and demonstration checklist
- add_institution_knowledge_workspace_b627da2f7e11.py
- test_stage_audit_is_atomic_and_noop_updates_do_not_create_history
- tasks/processing.py
- crm_data
- index_known_name
- test_handle_turn_basic_flow
- notifications.tsx
- Implementation Plan: AdmitFlow
- .__call__
- 11. Human-in-the-Loop (Full Workflow)
- record-demo.mjs
- generate_completion
- 10. Observability & Tracing
- 2. Boundaries & Invariants
- 3. Tech Stack & Commands
- 5. Code Style
- 8. RAG (Retrieval-Augmented Generation)
- timeline
- 17. Decisions & Open Questions
- privacy_dependencies

## God Nodes (most connected - your core abstractions)
1. `encrypt_pii()` - 104 edges
2. `write_audit_log()` - 96 edges
3. `get_settings()` - 91 edges
4. `LeadStatus` - 90 edges
5. `Lead` - 79 edges
6. `decrypt_pii()` - 75 edges
7. `Reply` - 74 edges
8. `TelegramBot` - 66 edges
9. `signin()` - 59 edges
10. `Course` - 56 edges

## Surprising Connections (you probably didn't know these)
- `Task 42.3: Pluggable Reranker (Cohere API vs Local)` --references--> `search_chunks()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/core/rag.py
- `Task 4: PII encryption utilities and audit log infrastructure` --references--> `write_audit_log()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/db/audit.py
- `17.1 Conversation engine — DECIDED: hand-rolled dispatcher` --references--> `handle_turn()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/SPEC.md → backend/src/engine/dispatcher.py
- `Missing-reply investigation (approximately 22:59 IST)` --references--> `process_inbound_message()`  [INFERRED]
  docs/event/READINESS_CHECK.md → backend/src/tasks/processing.py
- `Consequences` --references--> `EncryptionKeyNotConfiguredError`  [INFERRED]
  docs/decisions/ADR-009-pii-encryption-and-audit.md → backend/src/core/security.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Finalized Production Stack Components** — docs_decisions_adr_007_finalized_stack_finalized_stack, docs_decisions_adr_007_finalized_stack_fly_io, docs_decisions_adr_007_finalized_stack_neon, docs_decisions_adr_007_finalized_stack_redis, docs_decisions_adr_007_finalized_stack_langfuse [EXTRACTED 1.00]
- **handle_turn() Per-Turn Pipeline** — spec_hand_rolled_dispatcher, docs_decisions_adr_008_system_1_decision_layer_decide, docs_decisions_adr_005_three_layer_guardrails_three_layer_guardrails, docs_decisions_adr_004_memory_architecture_episodic_memory, spec_code_owns_the_money [EXTRACTED 1.00]
- **System-1 Decision Engine (decide + primitives + models)** — docs_decisions_adr_008_system_1_decision_layer_system_1_decision_layer, docs_decisions_adr_008_system_1_decision_layer_decide, docs_research_system_1_decision_models_laya_jev_choice, docs_research_system_1_decision_models_laya_jev_score, docs_research_system_1_decision_models_laya_jev_noul, docs_research_system_1_decision_models_laya_jev_laya [EXTRACTED 1.00]
- **AdmitFlow AI Core Architecture** — tasks_plan_conversation_engine, tasks_plan_decide_decision_layer, tasks_plan_three_layer_guardrails, tasks_plan_rag_pipeline [INFERRED 0.85]
- **WhatsApp Ingress → Worker → Engine Flow** — tasks_plan_fastapi_webhook, tasks_plan_redis, tasks_plan_taskiq, tasks_plan_conversation_engine [INFERRED 0.85]

## Communities (159 total, 17 thin omitted)

### Community 0 - "AdmitFlow Complete Specification"
Cohesion: 0.20
Nodes (18): ADR-001: Hybrid Architecture, ADR-004: Dual Memory Architecture, Episodic Memory (messages table), Semantic Memory (lead_facts table), ADR-005: Three-Layer Guardrails and RAG, Three-Layer Guardrails, ADR-007: Finalized Production Stack, ADR-008: System-1 Decision Layer (Laya / Jev) (+10 more)

### Community 1 - "Conversation Engine (hand-rolled dispatcher)"
Cohesion: 0.25
Nodes (8): Conversation Engine (hand-rolled dispatcher), System-1 decide() Decision Layer, FastAPI WhatsApp Webhook, Langfuse LLM Tracing, pgvector RAG Pipeline, Redis (mutex / dedup / rate-limit), TaskIQ Background Worker, Three-Layer Guardrails

### Community 2 - "AdmitFlow Task List"
Cohesion: 0.23
Nodes (7): Executed final check, One final WhatsApp check with Postman, AdmitFlow necessary resources, Planning baseline before Telegram alignment, AdmitFlow Platform, AdmitFlow Implementation Plan, AdmitFlow Task List

### Community 3 - "Finalized Production Stack"
Cohesion: 0.18
Nodes (11): ADR-002: Webhook Concurrency and Deduplication, Per-Phone Redis Mutex, Webhook Deduplication (Redis SETNX), ADR-003: Multi-Tenancy Strategy, Multi-Tenancy (Row-Level Isolation), Finalized Production Stack, Fly.io (Backend + Worker + Scheduler), Langfuse Cloud (LLM Tracing) (+3 more)

### Community 4 - "leads.py"
Cohesion: 0.18
Nodes (24): lead_statement(), lead_summary(), LeadFilters, LeadSearch, Any, BaseModel, Select, UUID (+16 more)

### Community 5 - "analytics"
Cohesion: 0.07
Nodes (37): alias, Admissions analytics, AdmitFlow Backend, Application payments, Configuration, Consented follow-up reminders, Current implementation and verification, Institution knowledge workspace (+29 more)

### Community 6 - "Code Owns the Money"
Cohesion: 0.50
Nodes (5): ADR-006: Code-Owned Qualification and Payments, Intent: Admissions Flow and Discounts, Discount Codes, Code Owns Eligibility, Code Owns the Money

### Community 7 - "journey.py"
Cohesion: 0.18
Nodes (30): Lead, A prospective applicant with optional phone contact and channel identities.…, escalation_reason(), Reason, answer_question(), build_reply(), button(), copy() (+22 more)

### Community 8 - "RedisMutex"
Cohesion: 0.07
Nodes (28): MutexAcquireError, Redis, RuntimeError, Redis distributed mutex with owner-safe release and keepalive (Task 7). Ensures…, Background loop that extends the TTL while the lock is held., Raised when the mutex cannot be acquired after all retries., Async context-manager mutex backed by Redis ``SET NX``. Parameters: redis: An…, Attempt to acquire the lock, retrying up to ``retry_count`` times. (+20 more)

### Community 9 - "write_audit_log"
Cohesion: 0.20
Nodes (11): Any, AsyncSession, UUID, Record persisted ORM transitions atomically; never infer an earlier stage., Append one entry to ``audit_logs`` on ``session``; return it flushed, not…, record_stage_changes(), write_audit_log(), Unit test for the audit-log write helper. The real INSERT path (JSONB, server-… (+3 more)

### Community 10 - "TestWhatsAppSender"
Cohesion: 0.15
Nodes (10): asyncio, fixture, Successfully sending a template message., API errors (non-200) raise WhatsAppAPIError., Fails loud if access token or phone ID are missing., WhatsApp sender operations., Successfully sending a text message., Successfully sending an interactive buttons message. (+2 more)

### Community 11 - "staff/integrations.py"
Cohesion: 0.09
Nodes (34): destination(), post_event(), PrivateTransportLogs, protect_logs(), public_ip(), LogRecord, HTTPS delivery pins a public resolved address while retaining TLS host…, resolve_public() (+26 more)

### Community 12 - "WhatsAppSender"
Cohesion: 0.18
Nodes (13): Any, Send an interactive list message. `sections` is a list of section dicts…, Send a pre-approved template message., Service for sending messages via Meta WhatsApp Cloud API., Post the payload to Meta and extract the created message ID., Meta API expects the phone number without the leading '+'., Send a simple text message. Returns the Meta message ID., Send an interactive message with up to 3 buttons. `buttons` should be a list of… (+5 more)

### Community 13 - "DocumentChunk"
Cohesion: 0.09
Nodes (30): chunk_text(), embed_text(), ingest_document(), Any, AsyncSession, UUID, RAG pipeline core logic (Task 13). Handles ingestion (chunking, embedding),…, Hybrid search (dense + lexical with RRF). (+22 more)

### Community 16 - "get_settings"
Cohesion: 0.11
Nodes (22): AsyncBroker, get_settings(), Application settings singleton. Loads configuration from the environment (and…, Return the process-wide :class:`Settings` singleton., embed_chunks(), Use the configured OpenAI model with the database's explicit 1536 dimensions., main(), Probe (+14 more)

### Community 17 - "admissions.tsx"
Cohesion: 0.12
Nodes (15): Admissions(), Detail, Human, Inquiry, labels, Request, RuleEvidence, statusLabel() (+7 more)

### Community 18 - "retrieval.py"
Cohesion: 0.11
Nodes (23): contextual_query(), numeric_values(), BaseModel, Bounded query resolution for approved evidence; never turn queries into facts., Resolve pronouns/slang using bounded recent turns; uncertainty asks the…, ResolvedQuestion, retrieval_query(), RetrievalQuery (+15 more)

### Community 19 - "Settings"
Cohesion: 0.14
Nodes (25): hash_phone(), Return a deterministic keyed hash of a phone number for lookup/dedup. Keyed…, Environment-backed application configuration., Settings, configured_keys(), fixture, MonkeyPatch, Unit tests for application-layer PII protection (encrypt/decrypt + phone hash). (+17 more)

### Community 20 - "AIBoomi Startup Weekend Kochi: fresh-session context"
Cohesion: 0.11
Nodes (19): AIBoomi Startup Weekend Kochi: fresh-session context, Assessment and next decision, Current readiness session (October 22), Event sources and local copies, Existing prototype rule and surprise element, Existing working-tree changes, Fresh-message prompt, Handoff status (+11 more)

### Community 21 - "payments/conversation.py"
Cohesion: 0.27
Nodes (18): button(), discount_action(), order_reply(), payment_action(), preview(), Any, AsyncSession, UUID (+10 more)

### Community 22 - "exports.py"
Cohesion: 0.20
Nodes (16): clean(), download(), export_rows(), ExportRequest, Db, post, Response, Audited institution exports, with explicit limits and spreadsheet-safe text. (+8 more)

### Community 23 - "Course"
Cohesion: 0.11
Nodes (31): Batch, Course, QualificationRule, A program a lead can be qualified for and pay to apply to., A dated intake of a course with finite seats (SPEC §7.5)., A structured eligibility rule evaluated in code, not by the LLM (ADR-006).…, Event, Human-readable callback summaries without exposing routing or signature details. (+23 more)

### Community 24 - "LeadStatus"
Cohesion: 0.11
Nodes (31): LeadStatus, Lead lifecycle states (SPEC §7.3). Where a lead *stands*, not a fixed track —…, AsyncSession, Run the qualification loop., run_qualification(), EngineState, InvalidTransitionError, BaseModel (+23 more)

### Community 25 - "Stages"
Cohesion: 0.13
Nodes (15): 10. Reflect & learn, 1. Understand & spec  (`/spec`), 2. Plan & pick a task  (`/plan`), 3. Branch, 4. Build with TDD  (`/build`, `/test`), 5. Verify (the quality gate), 6. Self-review, then adversarial review  (`/review`), 7. Commit & open the PR (+7 more)

### Community 26 - "test_knowledge_workspace.py"
Cohesion: 0.08
Nodes (37): alembic_config, asyncio, Application-layer PII protection: symmetric encryption + deterministic hashing.…, ConversationEvent, OutboundMessage, Institution (the tenant root) and its staff users., Async engine and session factory. Built lazily from ``settings.database_url``…, Bounded chronological transcript across inbound, replies and standalone… (+29 more)

### Community 27 - "test_webhook.py"
Cohesion: 0.11
Nodes (19): parametrize, test_delivery_status_logs_are_authenticated_and_exclude_pii(), test_tunnel_app_exposes_no_other_routes(), test_tunnel_app_keeps_webhook_verification(), app(), client(), mock_settings(), Any (+11 more)

### Community 28 - "run_postman_check.cjs"
Cohesion: 0.20
Nodes (8): collection, config, crypto, fs, keys, newman, path, root

### Community 29 - "Task List"
Cohesion: 0.15
Nodes (13): Checkpoint: Advanced Features, Checkpoint: AI Core, Checkpoint: Dashboard Complete, Checkpoint: Foundation, Checkpoint: Production Ready, Checkpoint: WhatsApp Ingress, Phase 1: Foundation, Phase 2: WhatsApp Ingress (+5 more)

### Community 30 - "get_engine"
Cohesion: 0.07
Nodes (37): AsyncEngine, get_engine(), Return the process-wide async engine (one pool for the app)., Case, cases(), evaluate(), main(), BaseModel (+29 more)

### Community 31 - "test_crm_search.py"
Cohesion: 0.19
Nodes (16): Core cross-cutting concerns: settings, security, schemas, guardrails, tracing., name_tokens(), normalized_phone(), UUID, query_tokens(), Tenant-keyed blind name prefixes; plaintext remains in encrypted columns only., token(), words() (+8 more)

### Community 32 - "Phase 5: Dashboard Frontend (Next.js)"
Cohesion: 0.04
Nodes (45): AdmitFlow — Task List, AIBoomi Startup Weekend session handoff (2026-10-22), Current direction and hackathon resources (2026-10-23), Final Postman diagnostic (October 23, executed; delivery blocked), Phase 1: Foundation, Phase 3–4 addition (see ADR-008), Phase 4: Advanced Bot Features, Phase 5: Dashboard Frontend (Next.js) (+37 more)

### Community 33 - "management.py"
Cohesion: 0.14
Nodes (37): require_admin(), archive_course(), archive_discount(), BatchInput, catalog(), catalog_detail(), course_view(), CourseInput (+29 more)

### Community 34 - "Code Standards"
Cohesion: 0.18
Nodes (11): Async & I/O, Code Standards, Configuration — settings, not literals, Dependencies, Errors, Formatting, LLM calls, Logging & observability (+3 more)

### Community 35 - "outreach/followups.py"
Cohesion: 0.09
Nodes (35): office_open(), datetime, Deterministic clear support signals and institution-local office hours., activity(), after_send(), before_send(), Check, course_available() (+27 more)

### Community 36 - "Event preparation and execution plan"
Cohesion: 0.18
Nodes (11): Business and mentor preparation, Evaluation and demo evidence, Event preparation and execution plan, Kickoff disclosure draft, Latest direction (October 23), Minimum demonstrable product, Next action: one-hour v1 readiness check, Submission checklist (+3 more)

### Community 37 - "7. Core Feature Specifications"
Cohesion: 0.20
Nodes (10): 7.10 Payment Integration & Discounts (Razorpay), 7.1 WhatsApp Number Architecture, 7.2 Multi-Tenancy (Row-Level Isolation), 7.3 Lead Lifecycle States, 7.5 Batch & Intake Management, 7.6 Cold Lead Re-engagement, 7.7 Language Support, 7.8 Lead Sources & Outbound (+2 more)

### Community 38 - "preference_reply"
Cohesion: 0.60
Nodes (6): cancel_queued(), note_inbound(), preference_reply(), Any, AsyncSession, datetime

### Community 39 - "main.py"
Cohesion: 0.10
Nodes (18): recovery_loop(), recovery_loop(), create_app(), lifespan(), FastAPI, FastAPI application entry point. Boots the API, manages the TaskIQ broker…, Start / stop the TaskIQ broker alongside the FastAPI process. The…, Application factory — builds and configures the FastAPI instance. (+10 more)

### Community 40 - "knowledge/processing.py"
Cohesion: 0.12
Nodes (28): decrypt_bytes(), Authenticate and decrypt source bytes for an authorized ingestion task., extract_file(), ExtractionError, ValueError, Bounded extraction of institution reference documents; never execute uploads., A safe, public error code rather than parser output containing document text., validate_path() (+20 more)

### Community 41 - "operations.py"
Cohesion: 0.18
Nodes (17): resumed_status(), active_request(), finish_takeover(), ManualMessage, Any, AsyncSession, BaseModel, Db (+9 more)

### Community 42 - "Hackathon resources for AdmitFlow"
Cohesion: 0.20
Nodes (10): Acceptance before using a resource, Event and release boundaries, Goal, Hackathon resources for AdmitFlow, October 23 Downloads guide: hosted inference access, Participant credits and other support, Suggested allocation and activation order, Useful resources mapped to the plan (+2 more)

### Community 43 - "manifest.json"
Cohesion: 0.20
Nodes (9): SPEC.md, bytes, sha256, tasks/plan.md, bytes, sha256, tasks/todo.md, bytes (+1 more)

### Community 44 - "fastapi"
Cohesion: 0.11
Nodes (18): ASGIApp, Reject oversized multipart streams before they can fill temporary storage., UploadBodyLimit, Custom header + strict cookies prevent cross-origin simple-request CSRF., require_browser_write(), Bounded login throttling; shared Redis when configured, development fallback., MonkeyPatch, Bound resource use and reject browser cross-origin mutations before database… (+10 more)

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

### Community 49 - "age"
Cohesion: 0.10
Nodes (23): age(), outreach(), fixture, parametrize, seed(), test_exactly_two_reminders_then_cold_without_duplicate_delivery(), exercise(), test_existing_inquiries_upgrade_without_invented_consent() (+15 more)

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
Cohesion: 0.25
Nodes (8): AdmitFlow project handoff, Current direction, Development rules, Event submission, Execution checkpoint, First usable release, Historical evidence, Resume prompt

### Community 54 - "detect_intent"
Cohesion: 0.20
Nodes (15): detect_intent(), Classify the user's intent to route to the correct node. Design Decision: If a…, asyncio, Test routing for course discovery., Test routing for knowledge questions., Test routing for qualification answers., Test routing for human handoff., Test routing for empty messages without calling LLM defaults to discovery. (+7 more)

### Community 55 - "EncryptionKeyNotConfiguredError"
Cohesion: 0.17
Nodes (13): EncryptionKeyNotConfiguredError, RuntimeError, Raised when a PII helper is used but its key is unset in settings., hash_telegram_identifier(), UUID, Private Telegram identity lookup without storing raw identifiers in indexes., Hash an identifier in its tenant/bot/type domain using the lookup secret. This…, MonkeyPatch (+5 more)

### Community 56 - "RuleOperator"
Cohesion: 0.19
Nodes (16): Qualification-rule comparison operators (SPEC §7.4). Evaluated…, RuleOperator, ExtractionResponse, BaseModel, Qualification Node (Task 15). Extracts rule fields using the LLM and runs…, Structured output expected from the LLM when extracting fields., _coerce_values(), evaluate_rule() (+8 more)

### Community 57 - "test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment"
Cohesion: 0.19
Nodes (10): payments(), Any, get, Any, MonkeyPatch, test_absent_link_does_not_clear_uncertainty_or_authorize_retry(), test_known_configuration_failure_can_only_requeue_same_bounded_invoice(), test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment() (+2 more)

### Community 58 - "copilot.py"
Cohesion: 0.18
Nodes (19): load_memory(), event_text(), AsyncSession, content(), decide(), DraftContent, DraftDecision, DraftRequest (+11 more)

### Community 59 - "ADR-010: Triage Fallback Routing (Anti-Spam)"
Cohesion: 0.33
Nodes (5): ADR-010: Triage Fallback Routing (Anti-Spam), Consequences, Context, Decision, Status

### Community 60 - "ADR-012: Telegram and OpenAI for the first complete admissions MVP"
Cohesion: 0.29
Nodes (7): ADR-012: Telegram and OpenAI for the first complete admissions MVP, Consequences, Context, Decision, Implemented runtime boundaries, References and verification, Supersession and preserved decisions

### Community 61 - "prepare"
Cohesion: 0.19
Nodes (12): prepare(), Any, MonkeyPatch, parametrize, test_clear_escalation_records_request_outside_hours_without_a_model(), unavailable(), test_copilot_provider_failure_never_queues_a_message(), test_copilot_requires_review_rejects_stale_and_deduplicates_approval() (+4 more)

### Community 63 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 64 - "auth.py"
Cohesion: 0.06
Nodes (73): Dashboard access role (SPEC — admin vs agent)., StaffRole, A dashboard user (admin or agent) belonging to one institution., StaffUser, main(), provision(), Manually provision an institution administrator without printing credentials., admin_scope() (+65 more)

### Community 65 - "encrypt_pii"
Cohesion: 0.09
Nodes (34): encrypt_pii(), Encrypt a PII string, returning a url-safe base64 Fernet token. Fernet is…, Trusted bot-to-institution mapping; token is application-encrypted., TelegramBot, test_all_aggregates_share_a_snapshot_during_concurrent_arrivals(), interleave(), test_search_pages_are_bounded_and_do_not_drop_or_repeat_records(), seed() (+26 more)

### Community 66 - "typing"
Cohesion: 0.11
Nodes (33): Audit-log write helper. :func:`write_audit_log` is the one path significant…, ApplicationStatus, DiscountType, PaymentStatus, Enumerated types used across the schema. These are Python ``str`` enums mapped…, How a discount code reduces the fee., Payment order lifecycle (SPEC §7.10)., Application review status (SPEC §7.9 / lifecycle). (+25 more)

### Community 67 - "api.py"
Cohesion: 0.14
Nodes (28): encrypt_bytes(), _fernet(), Encrypt uploaded source bytes before persistence, without lossy text decoding., assign_scope(), documents(), get_upload(), Any, BaseModel (+20 more)

### Community 68 - "telegram/service.py"
Cohesion: 0.20
Nodes (16): process_telegram_event(), task, Telegram inbox and outbox jobs contain only internal identifiers., send_telegram_reply(), normalize_update(), accept_update(), process_event(), Any (+8 more)

### Community 69 - "sqlalchemy"
Cohesion: 0.06
Nodes (11): alembic, columns(), Column, upgrade(), common(), Column, upgrade(), collections_abc (+3 more)

### Community 70 - "RazorpayClient"
Cohesion: 0.05
Nodes (54): argparse, AsyncBaseTransport, compose(), Verify the isolated local Compose stack without external API calls or sends., seed_credentials(), verify(), Credentials, PaymentLink (+46 more)

### Community 71 - "Official source snapshots"
Cohesion: 0.50
Nodes (4): Conflicts to confirm, October 23 planning refresh, Official source snapshots, Sources

### Community 72 - "test_discovery.py"
Cohesion: 0.12
Nodes (16): present_courses(), AsyncSession, Discovery Node (Task 12). Presents available courses as WhatsApp interactive…, Fetch active courses with available batches and present to user. Only shows…, RAG Node (Task 14). Graph node that retrieves from the knowledge base and…, RuntimeError, WhatsApp message sending service (Task 6). Uses httpx2 to call the Meta Graph…, Raised when the Meta Cloud API returns an error response. (+8 more)

### Community 73 - "Reply"
Cohesion: 0.18
Nodes (17): action(), application_action(), collect_application(), prompt(), Any, AsyncSession, Explicit, encrypted, deterministic application collection in a private…, Button (+9 more)

### Community 74 - "get_sessionmaker"
Cohesion: 0.17
Nodes (20): async_sessionmaker, get_session(), get_sessionmaker(), AsyncSession, Return the process-wide async session factory., FastAPI dependency yielding a session that closes after the request., deliver(), dispatch_pending() (+12 more)

### Community 75 - "budget.py"
Cohesion: 0.09
Nodes (34): get_redis(), Redis, RuntimeError, Shared async Redis client for application code. Carry-over prerequisite #1: the…, Raised when Redis is needed but ``REDIS_URL`` is unset in settings., Return the process-wide async Redis client singleton. The client is created…, RedisNotConfiguredError, day_window() (+26 more)

### Community 76 - "management.tsx"
Cohesion: 0.10
Nodes (13): blank, Discount, Discounts(), Batch, Course, empty, Management(), operators (+5 more)

### Community 77 - "hashlib"
Cohesion: 0.10
Nodes (20): log_delivery_status(), Request, Response, Expose only the existing Meta webhook through the temporary demo tunnel., Observe only authenticated status events, without recipient or error text., Integer monetary arithmetic and exact-byte webhook authentication., get, post (+12 more)

### Community 78 - "test_integrations_notifications.py"
Cohesion: 0.12
Nodes (11): Leased at-least-once webhook delivery with stable recipient deduplication IDs., Durable, minimal institution events and signed outbound integrations., Backfill encrypted lead names from latest submitted forms and rebuild blind…, Staff authentication and institution-scoped access., task, Integration queue messages contain identifiers only., send_webhook(), Keep development-only throttle state independent across database test cases. (+3 more)

### Community 79 - "dispatcher.py"
Cohesion: 0.11
Nodes (23): MessageDirection, Direction of a WhatsApp message row (episodic memory, ADR-004)., _flush_engine_state(), handle_turn(), _load_engine_state(), Any, AsyncSession, Engine Dispatcher (Task 8 & 17). This module contains the main entry point for… (+15 more)

### Community 84 - "analytics.tsx"
Cohesion: 0.28
Nodes (7): Analytics(), Conversion, labels, frontend_app_analytics_module, rate(), Report, shortDate()

### Community 89 - "signin"
Cohesion: 0.13
Nodes (16): test_local_cohort_counts_conversions_and_observed_stages(), test_tenant_is_derived_from_session_and_period_is_bounded(), test_zero_filled_weekly_buckets_and_empty_rates(), test_downloads_roles_datasets_limits_and_tenants(), test_search_scope_validation_and_audit(), Any, Real database management: administrator writes, role/tenant boundaries and…, test_catalog_writes_validate_rules_capacity_and_ownership() (+8 more)

### Community 90 - "README.md"
Cohesion: 0.10
Nodes (18): AI Impact Statement, Student-to-staff demonstration, Current templates, Language review packet, Live exercise, Reference clarification, Reminder consent and outreach copy, Prior-work disclosure draft (+10 more)

### Community 91 - "decrypt_pii"
Cohesion: 0.18
Nodes (11): decrypt_pii(), Decrypt a token produced by :func:`encrypt_pii`. Raises…, test_configuration_roles_encryption_and_tenant_ownership(), inspect(), change_then_reply(), test_expired_draft_and_disabled_channel_cannot_queue_staff_replies(), expire(), cancel_then_fail() (+3 more)

### Community 92 - "workspace"
Cohesion: 0.14
Nodes (13): fixture, workspace(), UUID, seed(), exercise(), exercise(), exercise(), Any (+5 more)

### Community 93 - "test_decision_reranking.py"
Cohesion: 0.21
Nodes (18): UUID, Reorder only original, safe tenant candidates; never invent text or sources.…, rerank(), chunks(), Intent, asyncio, BaseModel, MonkeyPatch (+10 more)

### Community 94 - "ADR-009: Application-Layer PII Encryption and Audit Logging"
Cohesion: 0.15
Nodes (12): DatabaseNotConfiguredError, RuntimeError, Raised when a DB session is requested but ``DATABASE_URL`` is unset., ADR-009: Application-Layer PII Encryption and Audit Logging, Alternatives Considered, Consequences, Context, Decision (+4 more)

### Community 95 - "Institution"
Cohesion: 0.24
Nodes (11): Institution, An institution, optionally connected to a legacy WhatsApp number. The tenant…, _roundtrip(), identity_database(), fixture, Use a disposable pgvector database; never mutate the demo database., test_downgrade_preserves_legacy_rows_and_refuses_to_destroy_telegram_data(), insert_rows() (+3 more)

### Community 96 - "Git & GitHub Workflow"
Cohesion: 0.22
Nodes (9): Branching model — feature branch → PR → `main`, Commits — Conventional Commits, small and coherent, Git & GitHub Workflow, Merging, No AI attribution — the human is the sole author  ⚠️, Pull Requests, Review gate — adversarial, before merge, What never gets committed (+1 more)

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

### Community 102 - "fake_embeddings"
Cohesion: 0.19
Nodes (11): fake_embeddings(), Any, MonkeyPatch, test_duplicate_claim_and_abandoned_attempt_recovery(), claims(), paused(), recover(), test_expired_session_rejected() (+3 more)

### Community 103 - "next-env.d.ts"
Cohesion: 0.50
Nodes (3): NOTE: This file should not be edited, frontend_next_types_root_params_d, frontend_next_types_routes_d

### Community 104 - "payments/webhook.py"
Cohesion: 0.36
Nodes (8): LinkEntity, LinkEnvelope, PaidEvent, PaidPayload, PaymentEntity, PaymentEnvelope, BaseModel, Raw-body authenticated, amount-checked and replay-safe payment confirmation.

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
Cohesion: 0.10
Nodes (18): Contextual retrieval and reference scope, Isolated full-stack Compose, Outbound integrations and live notifications, Staff access and privacy operations, Typed OpenAI decisions and required reranking, Explicit Telegram receiver, Isolated local full-stack runtime, Stop and recover (+10 more)

### Community 110 - "AdmitFlow pitch deck copy"
Cohesion: 0.29
Nodes (7): AdmitFlow pitch deck copy, Slide 1: AdmitFlow, Slide 2: The admissions inquiry, Slide 3: A working student journey, Slide 4: Institution knowledge and control, Slide 5: Technology and verification, Slide 6: Pilot and next steps

### Community 111 - "send_outbound"
Cohesion: 0.28
Nodes (7): task, Encrypted outbound-message delivery jobs carry only internal identifiers., send_outbound_message(), create_payment_link(), task, Payment-link creation runs after the requesting conversation transaction…, send_outbound()

### Community 112 - "TelegramClient"
Cohesion: 0.17
Nodes (13): Any, RuntimeError, TelegramAPIError, TelegramClient, deliver(), parametrize, test_provider_retry_delay_is_not_shortened(), exercise() (+5 more)

### Community 113 - "models/__init__.py"
Cohesion: 0.08
Nodes (61): Base, IdMixin, Declarative base, metadata naming convention, and shared column mixins. Every…, Declarative base shared by every AdmitFlow model., UUID primary key with an application-side default. UUIDs avoid cross-tenant…, Server-side created/updated timestamps., Row-level tenant scoping (ADR-003). Mixed into every tenant-scoped table., TenantMixin (+53 more)

### Community 114 - "Quality Gates — Definition of Done"
Cohesion: 0.33
Nodes (6): CI mirrors this exactly, Fast iteration vs the gate, Quality Gates — Definition of Done, The baseline gate (every change), The enforced-numbers ledger, The tiers — add gates by what the change touches

### Community 115 - "inbound"
Cohesion: 0.32
Nodes (7): test_budget_pause_does_not_spend_a_reminder_and_stop_cancels_it(), exercise(), test_explicit_consent_and_stop_during_staff_takeover(), exercise(), inbound(), UUID, exercise()

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
Cohesion: 0.18
Nodes (12): dispatch_due(), Local operational commands with secrets entered through protected prompts., main(), Produce due reminder jobs and recover queued deliveries; safe to run after…, run(), purge_retained(), datetime, Expire inactive dialogue; applications, payments and CRM records survive. (+4 more)

### Community 120 - "test_settings.py"
Cohesion: 0.29
Nodes (6): Tests for the settings singleton., test_defaults_boot_without_env(), test_dotenv_is_explicit_in_tests(), test_env_overrides_defaults(), test_get_settings_is_cached_singleton(), test_get_settings_returns_settings_instance()

### Community 121 - "test_rag_node.py"
Cohesion: 0.23
Nodes (11): process_rag_node(), AsyncSession, Retrieve context and answer knowledge questions., mock_state(), asyncio, fixture, patch, Unit tests for the RAG node. (+3 more)

### Community 122 - "guardrails.py"
Cohesion: 0.19
Nodes (13): _deterministic_check(), InputGuardrailResult, LLMGuardrailResponse, LLMOutputGuardrailResponse, OutputGuardrailResult, BaseModel, Input Guardrail Node (Task 10). Detects prompt injection, profanity, and abuse…, Result of the input guardrail check. (+5 more)

### Community 123 - "scope.py"
Cohesion: 0.11
Nodes (18): AmbiguousCourseReference, AsyncSession, Course, UUID, ValueError, question_courses(), Code-owned course scopes for approved institution references., More than one active course has the requested name without a selected owner. (+10 more)

### Community 124 - "WhatsApp readiness check — October 22, 2026"
Cohesion: 0.15
Nodes (13): Decision so far, Delivery diagnosis and configuration repair (October 23, approximately 00:16 IST), Evidence collected before configuration, Final Postman retry (October 23), Live checkpoint (approximately 22:54 IST), Missing-reply investigation (approximately 22:59 IST), New test account configuration (October 23, approximately 09:45 IST), Next live checks and evidence required (+5 more)

### Community 125 - "review"
Cohesion: 0.33
Nodes (10): CRM search and institution downloads, applications(), detail(), owned(), Any, Db, get, post (+2 more)

### Community 126 - "erase_inquiry"
Cohesion: 0.27
Nodes (10): erase(), erase_inquiry(), EraseRequest, in_flight(), AsyncSession, BaseModel, Db, delete (+2 more)

### Community 127 - "TokenSafeFilter"
Cohesion: 0.33
Nodes (5): protect_logs(), LogRecord, TaskIQ changes log levels; redact before either HTTP client or root handlers…, TokenSafeFilter, test_http_logs_redact_bot_credentials()

### Community 128 - "payments.tsx"
Cohesion: 0.32
Nodes (6): label(), money(), outcomes, Payment, Payments(), statuses

### Community 129 - "test_expired_lease_recovery_cap_and_configuration_cancellation"
Cohesion: 0.15
Nodes (11): configure(), event_for(), test_delivery_claim_retry_and_minimal_payload(), exercise(), test_expired_lease_recovery_cap_and_configuration_cancellation(), exercise(), inspect(), test_more_than_one_page_of_unread_events_remains_accessible() (+3 more)

### Community 130 - "StaffAccounts"
Cohesion: 1.00
Nodes (3): StaffAccounts(), create(), mutate()

### Community 131 - "Knowledge"
Cohesion: 0.44
Nodes (9): refresh(), api(), Knowledge(), action(), assignScope(), login(), search(), upload() (+1 more)

### Community 132 - "test_local_runtime.py"
Cohesion: 0.14
Nodes (14): configure(), main(), Path, Create private isolated local Compose configuration without copying live…, Hash the tested code/configuration without reading secrets or runtime data., asyncio, MonkeyPatch, Path (+6 more)

### Community 133 - "env.py"
Cohesion: 0.22
Nodes (9): do_run_migrations(), Connection, Alembic migration environment (async). Reads the database URL from application…, Emit SQL to stdout without a live DB connection., Run migrations against a live database via an async engine., run_migrations_offline(), run_migrations_online(), logging_config (+1 more)

### Community 135 - "pydantic"
Cohesion: 0.19
Nodes (11): decide(), Any, Typed decisions through the existing OpenAI-only provider boundary., Validate structured model output; refusal/malformed output is never a decision.…, BaseModel, Triage Node (Task 11). Routes incoming messages to the appropriate downstream…, Structured output expected from the LLM triage classifier., TriageResponse (+3 more)

### Community 137 - "page.tsx"
Cohesion: 0.12
Nodes (13): DeliveryBudget(), Usage, Exports(), Configuration, Integrations(), Request, Doc, errors (+5 more)

### Community 138 - "AdmitFlow execution and demonstration checklist"
Cohesion: 0.67
Nodes (3): AdmitFlow execution and demonstration checklist, Build and verify, Demonstrate and submit

### Community 139 - "add_institution_knowledge_workspace_b627da2f7e11.py"
Cohesion: 0.22
Nodes (7): Column, DateTime, _timestamps(), upgrade(), isolated_local_login_windows(), fixture, MonkeyPatch

### Community 141 - "tasks/processing.py"
Cohesion: 0.12
Nodes (15): ping(), process_inbound_message(), Any, task, Background tasks for message processing. For now this module holds only the…, Smoke-test task: returns ``{"result": payload}``. Enqueued from the…, Process an inbound WhatsApp message (Task 17). This is a placeholder for the…, Tests for the TaskIQ broker setup and task execution (Task 3). All tests run… (+7 more)

### Community 145 - "index_known_name"
Cohesion: 0.40
Nodes (5): index_known_name(), Connection, Mapper, Keep index updates atomic with encrypted names, including name removal., listens_for

### Community 146 - "test_handle_turn_basic_flow"
Cohesion: 0.29
Nodes (6): Any, asyncio, fixture, patch, sample_whatsapp_payload(), test_handle_turn_basic_flow()

### Community 147 - "notifications.tsx"
Cohesion: 0.33
Nodes (4): labels, Notice, Notifications(), Snapshot

### Community 149 - "Implementation Plan: AdmitFlow"
Cohesion: 0.40
Nodes (4): Architecture Decisions, Implementation Plan: AdmitFlow, Overview, Risks and Mitigations

### Community 150 - ".__call__"
Cohesion: 0.33
Nodes (4): private_send(), Receive, Scope, Send

### Community 151 - "11. Human-in-the-Loop (Full Workflow)"
Cohesion: 0.40
Nodes (5): 11.1 Auto-Escalation Triggers, 11.2 Co-pilot Mode, 11.3 Business Hours, 11.4 Never Escalate, 11. Human-in-the-Loop (Full Workflow)

### Community 153 - "record-demo.mjs"
Cohesion: 0.40
Nodes (4): credentials, headers, journey, target

### Community 155 - "generate_completion"
Cohesion: 0.12
Nodes (22): AllProvidersFailedError, generate_completion(), Any, Exception, Bounded OpenAI-only model roles; provider details never escape in errors., Raised when the entire LLM fallback chain is exhausted., Generate a completion with automatic provider fallback. Tries the fast model,…, unavailable() (+14 more)

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

### Community 168 - "timeline"
Cohesion: 0.22
Nodes (8): Cursor, Any, AsyncSession, BaseModel, datetime, field_validator, UUID, timeline()

### Community 171 - "17. Decisions & Open Questions"
Cohesion: 0.67
Nodes (3): 17.1 Conversation engine — DECIDED: hand-rolled dispatcher, 17.2 Still open, 17. Decisions & Open Questions

## Knowledge Gaps
- **416 isolated node(s):** `admitflow-backend`, `fs`, `path`, `crypto`, `root` (+411 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1142 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CRM search and institution downloads` connect `review` to `test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment`, `leads.py`, `backend/README.md`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Why does `write_audit_log()` connect `write_audit_log` to `test_expired_lease_recovery_cap_and_configuration_cancellation`, `leads.py`, `analytics`, `journey.py`, `staff/integrations.py`, `payments/conversation.py`, `exports.py`, `Course`, `test_knowledge_workspace.py`, `Phase 5: Dashboard Frontend (Next.js)`, `management.py`, `outreach/followups.py`, `preference_reply`, `knowledge/processing.py`, `operations.py`, `test_staff_lookup_is_scoped_read_only_and_cannot_confirm_payment`, `copilot.py`, `auth.py`, `typing`, `api.py`, `telegram/service.py`, `RazorpayClient`, `Reply`, `get_sessionmaker`, `test_integrations_notifications.py`, `payments/webhook.py`, `send_outbound`, `models/__init__.py`, `scheduler.py`, `review`, `erase_inquiry`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `AdmitFlow — Task List` connect `Phase 5: Dashboard Frontend (Next.js)` to `WhatsAppSender`, `2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md`, `dispatcher.py`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `encrypt_pii()` (e.g. with `Consequences` and `Decision`) actually correct?**
  _`encrypt_pii()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 54 inferred relationships involving `LeadStatus` (e.g. with `record_stage_changes()` and `Lead`) actually correct?**
  _`LeadStatus` has 54 INFERRED edges - model-reasoned connections that need verification._
- **What connects `admitflow-backend`, `fs`, `path` to the rest of the system?**
  _416 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `analytics` be split into smaller, more focused modules?**
  _Cohesion score 0.06612685560053981 - nodes in this community are weakly interconnected._