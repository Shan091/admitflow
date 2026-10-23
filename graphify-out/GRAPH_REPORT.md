# Graph Report - admitflow  (2026-10-24)

## Corpus Check
- 267 files · ~141,008 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 3, .example 2, .css 2)

## Summary
- 2421 nodes · 6598 edges · 152 communities (137 shown, 15 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 415 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `009933e2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ADR-008: System-1 Decision Layer (Laya / Jev)
- Conversation Engine (hand-rolled dispatcher)
- AdmitFlow Complete Specification
- Finalized Production Stack
- write_audit_log
- generate_completion
- Code Owns the Money
- journey.py
- RedisMutex
- verify_webhook
- WhatsAppSender
- transport.py
- settings.py
- sqlalchemy_ext_asyncio
- PII Encryption & Audit Log
- Razorpay Payment Integration
- get_settings
- admissions.tsx
- tasks/processing.py
- encrypt_pii
- AIBoomi Startup Weekend Kochi: fresh-session context
- Lead
- exports.py
- Course
- LeadStatus
- Stages
- models/__init__.py
- test_webhook.py
- run_postman_check.cjs
- Task List
- TelegramClient
- crm.py
- Phase 5: Dashboard Frontend (Next.js)
- management.py
- Code Standards
- outreach/followups.py
- Event preparation and execution plan
- 7. Core Feature Specifications
- analytics
- main.py
- auth.py
- operations.py
- Hackathon resources for AdmitFlow
- manifest.json
- test_workspace_limits.py
- AdmitFlow: current state and planning baseline
- AdmitFlow: AIBoomi submission plan
- AdmitFlow — Complete Specification
- normalize_e164
- integration/test_followups.py
- ADR-011: Advanced RAG Strategy (Latency vs Precision)
- Testing
- test_payment_jobs.py
- AdmitFlow project handoff
- detect_intent
- ADR-009: Application-Layer PII Encryption and Audit Logging
- RuleOperator
- test_staff_payments.py
- copilot.py
- ADR-010: Triage Fallback Routing (Anti-Spam)
- ADR-012: Telegram and OpenAI for the first complete admissions MVP
- prepare
- compilerOptions
- Login
- Reply
- staff/payments.py
- api.py
- ExtractionError
- alembic
- provision_payments.py
- Official source snapshots
- get_engine
- consent.py
- test_telegram_journey.py
- signin
- management.tsx
- integration/test_telegram_identity.py
- AdmitFlow execution and demonstration checklist
- handle_turn
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
- institution.py
- Settings
- test_qualification.py
- Phase 3: AI Core (Engine + RAG)
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
- scripts/__init__.py
- layout.tsx
- frontend/AGENTS.md
- scripts
- Local Telegram/OpenAI runtime
- AdmitFlow pitch deck copy
- add_institution_knowledge_workspace_b627da2f7e11.py
- typing
- sqlalchemy
- Quality Gates — Definition of Done
- integration/conftest.py
- devDependencies
- applications.tsx
- dependencies
- update
- live
- Language review packet
- get_sessionmaker
- reindex_names.py
- WhatsApp readiness check — October 22, 2026
- staff/applications.py
- receiver.py
- retrieval.py
- payments.tsx
- test_expired_lease_recovery_cap_and_configuration_cancellation
- react
- Knowledge
- log_delivery_status
- env.py
- test_shared_budget_preserves_queues_and_settings_wake_deliveries
- test_knowledge_workspace.py
- payments/service.py
- page.tsx
- index_known_name
- test_mutex.py
- timeline.py
- Phase 1: Foundation
- AdmitFlow — Task List
- Phase 3–4 addition (see ADR-008)
- Phase 4: Advanced Bot Features
- Phase 6: Production Hardening
- notifications.tsx
- ExtractionResponse
- Implementation Plan: AdmitFlow
- AdmitFlow submission requirements
- TriageResponse

## God Nodes (most connected - your core abstractions)
1. `encrypt_pii()` - 102 edges
2. `LeadStatus` - 90 edges
3. `get_settings()` - 87 edges
4. `write_audit_log()` - 84 edges
5. `decrypt_pii()` - 75 edges
6. `Lead` - 74 edges
7. `Reply` - 71 edges
8. `TelegramBot` - 64 edges
9. `get_sessionmaker()` - 51 edges
10. `Course` - 50 edges

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

## Communities (152 total, 15 thin omitted)

### Community 0 - "ADR-008: System-1 Decision Layer (Laya / Jev)"
Cohesion: 0.18
Nodes (17): ADR-001: Hybrid Architecture, ADR-004: Dual Memory Architecture, Episodic Memory (messages table), Semantic Memory (lead_facts table), ADR-005: Three-Layer Guardrails and RAG, Three-Layer Guardrails, ADR-007: Finalized Production Stack, ADR-008: System-1 Decision Layer (Laya / Jev) (+9 more)

### Community 1 - "Conversation Engine (hand-rolled dispatcher)"
Cohesion: 0.25
Nodes (8): Conversation Engine (hand-rolled dispatcher), System-1 decide() Decision Layer, FastAPI WhatsApp Webhook, Langfuse LLM Tracing, pgvector RAG Pipeline, Redis (mutex / dedup / rate-limit), TaskIQ Background Worker, Three-Layer Guardrails

### Community 2 - "AdmitFlow Complete Specification"
Cohesion: 0.15
Nodes (13): Outbound integrations and live notifications, AI Impact Statement, Student-to-staff demonstration, Executed final check, One final WhatsApp check with Postman, Prior-work disclosure draft, AdmitFlow necessary resources, Planning baseline before Telegram alignment (+5 more)

### Community 3 - "Finalized Production Stack"
Cohesion: 0.18
Nodes (11): ADR-002: Webhook Concurrency and Deduplication, Per-Phone Redis Mutex, Webhook Deduplication (Redis SETNX), ADR-003: Multi-Tenancy Strategy, Multi-Tenancy (Row-Level Isolation), Finalized Production Stack, Fly.io (Backend + Worker + Scheduler), Langfuse Cloud (LLM Tracing) (+3 more)

### Community 4 - "write_audit_log"
Cohesion: 0.14
Nodes (28): Any, AsyncSession, UUID, Record persisted ORM transitions atomically; never infer an earlier stage., Append one entry to ``audit_logs`` on ``session``; return it flushed, not…, record_stage_changes(), write_audit_log(), lead_summary() (+20 more)

### Community 5 - "generate_completion"
Cohesion: 0.05
Nodes (57): AllProvidersFailedError, generate_completion(), Any, Exception, Bounded OpenAI-only model roles; provider details never escape in errors., Raised when the entire LLM fallback chain is exhausted., Generate a completion with automatic provider fallback. Tries the fast model,…, apply_whatsapp_formatting() (+49 more)

### Community 6 - "Code Owns the Money"
Cohesion: 0.50
Nodes (5): ADR-006: Code-Owned Qualification and Payments, Intent: Admissions Flow and Discounts, Discount Codes, Code Owns Eligibility, Code Owns the Money

### Community 7 - "journey.py"
Cohesion: 0.17
Nodes (29): Trusted bot-to-institution mapping; token is application-encrypted., TelegramBot, Event, escalation_reason(), Reason, build_reply(), button(), courses() (+21 more)

### Community 8 - "RedisMutex"
Cohesion: 0.08
Nodes (22): Redis, Background loop that extends the TTL while the lock is held., Async context-manager mutex backed by Redis ``SET NX``. Parameters: redis: An…, Attempt to acquire the lock, retrying up to ``retry_count`` times., Release the lock using the Lua CAS script (owner-safe)., RedisMutex, asyncio, Retry behaviour when the lock is initially held. (+14 more)

### Community 9 - "verify_webhook"
Cohesion: 0.50
Nodes (4): get, Response, Handle Meta's webhook challenge., verify_webhook()

### Community 10 - "WhatsAppSender"
Cohesion: 0.08
Nodes (28): Any, RuntimeError, Send an interactive list message. `sections` is a list of section dicts…, Send a pre-approved template message., Raised when the Meta Cloud API returns an error response., Service for sending messages via Meta WhatsApp Cloud API., Post the payload to Meta and extract the created message ID., Meta API expects the phone number without the leading '+'. (+20 more)

### Community 11 - "transport.py"
Cohesion: 0.08
Nodes (34): Durable, minimal institution events and signed outbound integrations., destination(), post_event(), PrivateTransportLogs, protect_logs(), public_ip(), LogRecord, HTTPS delivery pins a public resolved address while retaining TLS host… (+26 more)

### Community 12 - "settings.py"
Cohesion: 0.09
Nodes (26): Expose only the existing Meta webhook through the temporary demo tunnel., get_redis(), Redis, RuntimeError, Shared async Redis client for application code. Carry-over prerequisite #1: the…, Raised when Redis is needed but ``REDIS_URL`` is unset in settings., Return the process-wide async Redis client singleton. The client is created…, RedisNotConfiguredError (+18 more)

### Community 13 - "sqlalchemy_ext_asyncio"
Cohesion: 0.11
Nodes (26): chunk_text(), embed_text(), ingest_document(), Any, AsyncSession, UUID, RAG pipeline core logic (Task 13). Handles ingestion (chunking, embedding),…, Hybrid search (dense + lexical with RRF). (+18 more)

### Community 16 - "get_settings"
Cohesion: 0.10
Nodes (21): AsyncBroker, get_settings(), Return the process-wide :class:`Settings` singleton., _build_broker(), TaskIQ broker singleton. In production (and local dev with Redis running) the…, Construct the right broker based on the current settings. This is a plain…, Tests use explicit configuration and never implicitly load developer…, A real Redis worker must stay listening while its queue is idle. (+13 more)

### Community 17 - "admissions.tsx"
Cohesion: 0.13
Nodes (14): Admissions(), Detail, Human, Inquiry, labels, Request, RuleEvidence, statusLabel() (+6 more)

### Community 18 - "tasks/processing.py"
Cohesion: 0.12
Nodes (15): ping(), process_inbound_message(), Any, task, Background tasks for message processing. For now this module holds only the…, Smoke-test task: returns ``{"result": payload}``. Enqueued from the…, Process an inbound WhatsApp message (Task 17). This is a placeholder for the…, Tests for the TaskIQ broker setup and task execution (Task 3). All tests run… (+7 more)

### Community 19 - "encrypt_pii"
Cohesion: 0.09
Nodes (34): decrypt_pii(), encrypt_pii(), Encrypt a PII string, returning a url-safe base64 Fernet token. Fernet is…, Decrypt a token produced by :func:`encrypt_pii`. Raises…, test_all_aggregates_share_a_snapshot_during_concurrent_arrivals(), interleave(), test_search_pages_are_bounded_and_do_not_drop_or_repeat_records(), seed() (+26 more)

### Community 20 - "AIBoomi Startup Weekend Kochi: fresh-session context"
Cohesion: 0.11
Nodes (19): AIBoomi Startup Weekend Kochi: fresh-session context, Assessment and next decision, Current readiness session (October 22), Event sources and local copies, Existing prototype rule and surprise element, Existing working-tree changes, Fresh-message prompt, Handoff status (+11 more)

### Community 21 - "Lead"
Cohesion: 0.22
Nodes (22): Lead, A prospective applicant with optional phone contact and channel identities.…, button(), discount_action(), order_reply(), payment_action(), preview(), Any (+14 more)

### Community 22 - "exports.py"
Cohesion: 0.13
Nodes (21): clean(), download(), export_rows(), ExportRequest, Db, post, Response, Audited institution exports, with explicit limits and spreadsheet-safe text. (+13 more)

### Community 23 - "Course"
Cohesion: 0.09
Nodes (27): Application, PaymentOrder, Structured application data collected from an admission-ready lead (SPEC §7.9).…, A Razorpay order for an application fee (SPEC §7.10). Amount is DB-sourced…, Batch, Course, A program a lead can be qualified for and pay to apply to., A dated intake of a course with finite seats (SPEC §7.5). (+19 more)

### Community 24 - "LeadStatus"
Cohesion: 0.07
Nodes (47): LeadStatus, MessageDirection, Enumerated types used across the schema. These are Python ``str`` enums mapped…, Lead lifecycle states (SPEC §7.3). Where a lead *stands*, not a fixed track —…, Direction of a WhatsApp message row (episodic memory, ADR-004)., _flush_engine_state(), _load_engine_state(), AsyncSession (+39 more)

### Community 25 - "Stages"
Cohesion: 0.13
Nodes (15): 10. Reflect & learn, 1. Understand & spec  (`/spec`), 2. Plan & pick a task  (`/plan`), 3. Branch, 4. Build with TDD  (`/build`, `/test`), 5. Verify (the quality gate), 6. Self-review, then adversarial review  (`/review`), 7. Commit & open the PR (+7 more)

### Community 26 - "models/__init__.py"
Cohesion: 0.15
Nodes (18): ORM models package. Importing this package registers every model on…, IntegrationEvent, NotificationReceipt, Minimal committed events, per-user read receipts and a recoverable webhook…, WebhookDelivery, WebhookEndpoint, Leased at-least-once webhook delivery with stable recipient deduplication IDs., Commit minimal events/outbox rows in the source audit transaction. (+10 more)

### Community 27 - "test_webhook.py"
Cohesion: 0.11
Nodes (18): parametrize, test_delivery_status_logs_are_authenticated_and_exclude_pii(), test_tunnel_app_exposes_no_other_routes(), app(), client(), mock_settings(), Any, FastAPI (+10 more)

### Community 28 - "run_postman_check.cjs"
Cohesion: 0.18
Nodes (9): collection, config, crypto, fs, keys, newman, path, root (+1 more)

### Community 29 - "Task List"
Cohesion: 0.15
Nodes (13): Checkpoint: Advanced Features, Checkpoint: AI Core, Checkpoint: Dashboard Complete, Checkpoint: Foundation, Checkpoint: Production Ready, Checkpoint: WhatsApp Ingress, Phase 1: Foundation, Phase 2: WhatsApp Ingress (+5 more)

### Community 30 - "TelegramClient"
Cohesion: 0.10
Nodes (25): private_send(), normalize_update(), protect_logs(), Any, LogRecord, RuntimeError, TaskIQ changes log levels; redact before either HTTP client or root handlers…, TelegramAPIError (+17 more)

### Community 31 - "crm.py"
Cohesion: 0.13
Nodes (24): Core cross-cutting concerns: settings, security, schemas, guardrails, tracing., name_tokens(), normalized_phone(), UUID, query_tokens(), Tenant-keyed blind name prefixes; plaintext remains in encrypted columns only., token(), words() (+16 more)

### Community 32 - "Phase 5: Dashboard Frontend (Next.js)"
Cohesion: 0.17
Nodes (12): Phase 5: Dashboard Frontend (Next.js), Task 24: Initialize Next.js + dark mode + glassmorphism, Task 25: Authentication (email + password), Task 26: Dashboard home (funnel analytics), Task 27: Leads CRM page, Task 28: Course & batch management, Task 29: Chat takeover + co-pilot UI, Task 30: Document management (RAG) (+4 more)

### Community 33 - "management.py"
Cohesion: 0.08
Nodes (59): require_admin(), archive_course(), archive_discount(), BatchInput, catalog(), catalog_detail(), course_view(), CourseInput (+51 more)

### Community 34 - "Code Standards"
Cohesion: 0.18
Nodes (11): Async & I/O, Code Standards, Configuration — settings, not literals, Dependencies, Errors, Formatting, LLM calls, Logging & observability (+3 more)

### Community 35 - "outreach/followups.py"
Cohesion: 0.07
Nodes (43): office_open(), datetime, Deterministic clear support signals and institution-local office hours., activity(), after_send(), before_send(), Check, course_available() (+35 more)

### Community 36 - "Event preparation and execution plan"
Cohesion: 0.18
Nodes (11): Business and mentor preparation, Evaluation and demo evidence, Event preparation and execution plan, Kickoff disclosure draft, Latest direction (October 23), Minimum demonstrable product, Next action: one-hour v1 readiness check, Submission checklist (+3 more)

### Community 37 - "7. Core Feature Specifications"
Cohesion: 0.20
Nodes (10): 7.10 Payment Integration & Discounts (Razorpay), 7.1 WhatsApp Number Architecture, 7.2 Multi-Tenancy (Row-Level Isolation), 7.3 Lead Lifecycle States, 7.5 Batch & Intake Management, 7.6 Cold Lead Re-engagement, 7.7 Language Support, 7.8 Lead Sources & Outbound (+2 more)

### Community 38 - "analytics"
Cohesion: 0.07
Nodes (37): alias, Admissions analytics, AdmitFlow Backend, Application payments, Configuration, Consented follow-up reminders, Current implementation and verification, Institution knowledge workspace (+29 more)

### Community 39 - "main.py"
Cohesion: 0.10
Nodes (18): recovery_loop(), create_app(), lifespan(), FastAPI, FastAPI application entry point. Boots the API, manages the TaskIQ broker…, Start / stop the TaskIQ broker alongside the FastAPI process. The…, Application factory — builds and configures the FastAPI instance., Tests for the /debug endpoints (Task 3 verification). (+10 more)

### Community 40 - "auth.py"
Cohesion: 0.16
Nodes (20): Dashboard access role (SPEC — admin vs agent)., StaffRole, A dashboard user (admin or agent) belonging to one institution., StaffUser, main(), provision(), Manually provision an institution administrator without printing credentials., main() (+12 more)

### Community 41 - "operations.py"
Cohesion: 0.20
Nodes (17): resumed_status(), active_request(), finish_takeover(), ManualMessage, Any, AsyncSession, BaseModel, Db (+9 more)

### Community 42 - "Hackathon resources for AdmitFlow"
Cohesion: 0.20
Nodes (10): Acceptance before using a resource, Event and release boundaries, Goal, Hackathon resources for AdmitFlow, October 23 Downloads guide: hosted inference access, Participant credits and other support, Suggested allocation and activation order, Useful resources mapped to the plan (+2 more)

### Community 43 - "manifest.json"
Cohesion: 0.20
Nodes (9): SPEC.md, bytes, sha256, tasks/plan.md, bytes, sha256, tasks/todo.md, bytes (+1 more)

### Community 44 - "test_workspace_limits.py"
Cohesion: 0.09
Nodes (20): ASGIApp, Reject oversized multipart streams before they can fill temporary storage., UploadBodyLimit, Custom header + strict cookies prevent cross-origin simple-request CSRF., require_browser_write(), check_login_limit(), Request, MonkeyPatch (+12 more)

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

### Community 49 - "integration/test_followups.py"
Cohesion: 0.13
Nodes (21): age(), outreach(), fixture, parametrize, Real database consent, reminder leases, freshness, delivery and the two-message…, seed(), test_exactly_two_reminders_then_cold_without_duplicate_delivery(), exercise() (+13 more)

### Community 50 - "ADR-011: Advanced RAG Strategy (Latency vs Precision)"
Cohesion: 0.25
Nodes (7): 1. Complex Document Ingestion (`docling` or `unstructured`), 2. Pluggable Reranking Architecture (Cohere API over Local CPU), 3. Contextual Query Rewriting, ADR-011: Advanced RAG Strategy (Latency vs Precision), Consequences, Context, Decision

### Community 51 - "Testing"
Cohesion: 0.22
Nodes (9): Browser announcement regions, Coverage, LLM and decision-layer tests, Philosophy — pragmatic TDD, Running tests, Test layout, Testing, The two patterns (+1 more)

### Community 52 - "test_payment_jobs.py"
Cohesion: 0.14
Nodes (18): DiscountType, How a discount code reduces the fee., PaymentLink, PaymentProviderError, BaseModel, Exception, field_validator, Read an existing exact reference; absence never authorizes another creation. (+10 more)

### Community 53 - "AdmitFlow project handoff"
Cohesion: 0.25
Nodes (8): AdmitFlow project handoff, Current direction, Development rules, Event submission, Execution checkpoint, First usable release, Historical evidence, Resume prompt

### Community 54 - "detect_intent"
Cohesion: 0.20
Nodes (15): detect_intent(), Classify the user's intent to route to the correct node. Design Decision: If a…, asyncio, Test routing for course discovery., Test routing for knowledge questions., Test routing for qualification answers., Test routing for human handoff., Test routing for empty messages without calling LLM defaults to discovery. (+7 more)

### Community 55 - "ADR-009: Application-Layer PII Encryption and Audit Logging"
Cohesion: 0.22
Nodes (8): ADR-009: Application-Layer PII Encryption and Audit Logging, Alternatives Considered, Consequences, Context, Deterministic encryption of the phone number (so it is both stored and searchable), Full envelope encryption (per-tenant data keys wrapped by a master key), Rely on the provider's at-rest encryption only, Status

### Community 56 - "RuleOperator"
Cohesion: 0.27
Nodes (13): Qualification-rule comparison operators (SPEC §7.4). Evaluated…, RuleOperator, _coerce_values(), evaluate_rule(), Any, Evaluate a qualification rule deterministically. Args: operator: The…, test_evaluate_rule_in_list(), test_evaluate_rule_missing_extracted_value() (+5 more)

### Community 57 - "test_staff_payments.py"
Cohesion: 0.13
Nodes (17): Code-owned application fees and authenticated Razorpay payment processing., payments(), Any, get, UUID, seed(), exercise(), Any (+9 more)

### Community 58 - "copilot.py"
Cohesion: 0.13
Nodes (24): load_memory(), recent_history(), Any, AsyncSession, UUID, timeline(), event_text(), AsyncSession (+16 more)

### Community 59 - "ADR-010: Triage Fallback Routing (Anti-Spam)"
Cohesion: 0.33
Nodes (5): ADR-010: Triage Fallback Routing (Anti-Spam), Consequences, Context, Decision, Status

### Community 60 - "ADR-012: Telegram and OpenAI for the first complete admissions MVP"
Cohesion: 0.29
Nodes (7): ADR-012: Telegram and OpenAI for the first complete admissions MVP, Consequences, Context, Decision, Implemented runtime boundaries, References and verification, Supersession and preserved decisions

### Community 61 - "prepare"
Cohesion: 0.13
Nodes (19): test_budget_pause_does_not_spend_a_reminder_and_stop_cancels_it(), exercise(), inbound(), prepare(), Any, MonkeyPatch, parametrize, UUID (+11 more)

### Community 63 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 64 - "Login"
Cohesion: 0.19
Nodes (16): Login, logout(), me(), AsyncSession, BaseModel, Db, get, post (+8 more)

### Community 65 - "Reply"
Cohesion: 0.18
Nodes (17): action(), application_action(), collect_application(), prompt(), Any, AsyncSession, Explicit, encrypted, deterministic application collection in a private…, Button (+9 more)

### Community 66 - "staff/payments.py"
Cohesion: 0.21
Nodes (16): PaymentStatus, Payment order lifecycle (SPEC §7.10)., locked(), owned(), provider(), Db, post, UUID (+8 more)

### Community 67 - "api.py"
Cohesion: 0.15
Nodes (24): encrypt_bytes(), Encrypt uploaded source bytes before persistence, without lossy text decoding., documents(), get_upload(), Any, BaseModel, Db, delete (+16 more)

### Community 68 - "ExtractionError"
Cohesion: 0.19
Nodes (17): extract_file(), ExtractionError, ValueError, Bounded extraction of institution reference documents; never execute uploads., A safe, public error code rather than parser output containing document text., validate_path(), Hash the tested code/configuration without reading secrets or runtime data., parametrize (+9 more)

### Community 69 - "alembic"
Cohesion: 0.06
Nodes (9): alembic, columns(), Column, upgrade(), common(), Column, upgrade(), pgvector_sqlalchemy (+1 more)

### Community 70 - "provision_payments.py"
Cohesion: 0.12
Nodes (21): AsyncBaseTransport, Credentials, Bounded Razorpay requests; ambiguous link creation is never blindly retried., RazorpayClient, discounted_amount(), Integer monetary arithmetic and exact-byte webhook authentication., verify_webhook(), provision() (+13 more)

### Community 71 - "Official source snapshots"
Cohesion: 0.50
Nodes (4): Conflicts to confirm, October 23 planning refresh, Official source snapshots, Sources

### Community 72 - "get_engine"
Cohesion: 0.12
Nodes (18): AsyncEngine, DatabaseNotConfiguredError, get_engine(), RuntimeError, Raised when a DB session is requested but ``DATABASE_URL`` is unset., Return the process-wide async engine (one pool for the app)., main(), run() (+10 more)

### Community 73 - "consent.py"
Cohesion: 0.15
Nodes (19): cancel_queued(), note_inbound(), preference_reply(), Any, AsyncSession, datetime, Student-owned reminder preferences apply even while staff has paused the bot., parse_callback() (+11 more)

### Community 74 - "test_telegram_journey.py"
Cohesion: 0.18
Nodes (12): send(), A student must confirm a fresh code-owned fee quote; retries cannot create…, completion(), journey(), Any, fixture, MonkeyPatch, Synthetic student-to-staff journey against PostgreSQL, without external API… (+4 more)

### Community 75 - "signin"
Cohesion: 0.13
Nodes (16): test_local_cohort_counts_conversions_and_observed_stages(), test_tenant_is_derived_from_session_and_period_is_bounded(), test_zero_filled_weekly_buckets_and_empty_rates(), Encrypted explicit application collection, replay safety and tenant-scoped…, Any, Real database management: administrator writes, role/tenant boundaries and…, test_catalog_writes_validate_rules_capacity_and_ownership(), test_discount_management_rejects_invalid_values_duplicates_and_foreign_writes() (+8 more)

### Community 76 - "management.tsx"
Cohesion: 0.14
Nodes (10): Batch, Course, empty, Management(), operators, parseValue(), Rule, Settings (+2 more)

### Community 77 - "integration/test_telegram_identity.py"
Cohesion: 0.15
Nodes (15): alembic_config, Integration test: ``write_audit_log`` persists to real Postgres and reads back.…, _alembic_config(), monkeypatch_session(), pg_url(), fixture, MonkeyPatch, Migration + schema integration tests against real Postgres. Spins up… (+7 more)

### Community 78 - "AdmitFlow execution and demonstration checklist"
Cohesion: 0.67
Nodes (3): AdmitFlow execution and demonstration checklist, Build and verify, Demonstrate and submit

### Community 79 - "handle_turn"
Cohesion: 0.22
Nodes (9): handle_turn(), Any, Process a single turn of conversation., Any, asyncio, fixture, patch, sample_whatsapp_payload() (+1 more)

### Community 84 - "analytics.tsx"
Cohesion: 0.28
Nodes (7): Analytics(), Conversion, labels, frontend_app_analytics_module, rate(), Report, shortDate()

### Community 89 - "configured_keys"
Cohesion: 0.33
Nodes (7): configured_keys(), fixture, MonkeyPatch, Point ``security.get_settings`` at settings with the crypto keys set., Point ``security.get_settings`` at settings with no crypto keys., test_hash_phone_differs_per_pepper_key(), unset_keys()

### Community 90 - "AdmitFlow"
Cohesion: 0.33
Nodes (6): AdmitFlow, Current status, Demonstration and submission, Development, Product scope, Stack

### Community 91 - "institution.py"
Cohesion: 0.12
Nodes (38): Base, IdMixin, Declarative base, metadata naming convention, and shared column mixins. Every…, Declarative base shared by every AdmitFlow model., UUID primary key with an application-side default. UUIDs avoid cross-tenant…, Server-side created/updated timestamps., Row-level tenant scoping (ADR-003). Mixed into every tenant-scoped table., TenantMixin (+30 more)

### Community 92 - "Settings"
Cohesion: 0.11
Nodes (19): Environment-backed application configuration., Settings, hash_telegram_identifier(), UUID, Hash an identifier in its tenant/bot/type domain using the lookup secret. This…, test_private_identities_are_encrypted_unique_and_tenant_bound(), exercise(), identity() (+11 more)

### Community 93 - "test_qualification.py"
Cohesion: 0.20
Nodes (14): AsyncSession, Run the qualification loop., run_qualification(), base_state(), MockResult, Any, asyncio, fixture (+6 more)

### Community 94 - "Phase 3: AI Core (Engine + RAG)"
Cohesion: 0.18
Nodes (11): Phase 3: AI Core (Engine + RAG), Task 10: Input guardrail node, Task 11: Triage node (intent detection), Task 12: Discovery node, Task 13: RAG pipeline, Task 14: RAG node, Task 15: Qualification node, Task 16: Output guardrail (+3 more)

### Community 95 - "evaluate_faq.py"
Cohesion: 0.26
Nodes (14): answer_question(), copy(), Case, cases(), evaluate(), main(), BaseModel, Bounded live FAQ evaluation on the fictional demo tenant; no messages or writes. (+6 more)

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
Cohesion: 0.15
Nodes (8): credentials, headers, journey, target, ref_node_child_process, ref_node_fs, ref_node_path, @playwright/test

### Community 100 - "AGENTS.md"
Cohesion: 0.25
Nodes (7): AIBoomi Startup Weekend handoff, How we build — read the handbook, Knowledge graph, Quick commands (from `backend/`), The rules you cannot skip, What this project is, Workflow triggers

### Community 101 - "Security & Production Readiness"
Cohesion: 0.18
Nodes (11): Dependency & secret scanning, Deploy & rollback, External surfaces, Guardrails & money, Local full-stack (docker-compose), Multi-tenancy — isolation is a correctness bug if wrong, Observability, PII & data protection (DPDPA) (+3 more)

### Community 102 - "validate_services.py"
Cohesion: 0.32
Nodes (7): embed_chunks(), Use the configured OpenAI model with the database's explicit 1536 dimensions., main(), Probe, BaseModel, Bounded live checks; print sanitized results without credentials or update…, validate()

### Community 103 - "next-env.d.ts"
Cohesion: 0.50
Nodes (3): NOTE: This file should not be edited, frontend_next_types_root_params_d, frontend_next_types_routes_d

### Community 104 - "payments/webhook.py"
Cohesion: 0.19
Nodes (14): LinkEntity, LinkEnvelope, PaidEvent, PaidPayload, payment_webhook(), PaymentEntity, PaymentEnvelope, BaseModel (+6 more)

### Community 106 - "layout.tsx"
Cohesion: 0.25
Nodes (5): frontend_app_globals, metadata, config, @fontsource-variable/dm-sans, next

### Community 108 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, lint, record:demo, start, test:e2e:live, typecheck

### Community 109 - "Local Telegram/OpenAI runtime"
Cohesion: 0.25
Nodes (8): Configuration and data services, Delivery budget operation, Local Telegram/OpenAI runtime, Migrate and seed, Optional reminders and scheduler, Packaging and release limits, Run the processes, Validate and recover

### Community 110 - "AdmitFlow pitch deck copy"
Cohesion: 0.29
Nodes (7): AdmitFlow pitch deck copy, Slide 1: AdmitFlow, Slide 2: The admissions inquiry, Slide 3: A working student journey, Slide 4: Institution knowledge and control, Slide 5: Technology and verification, Slide 6: Pilot and next steps

### Community 111 - "add_institution_knowledge_workspace_b627da2f7e11.py"
Cohesion: 0.40
Nodes (4): Column, DateTime, _timestamps(), upgrade()

### Community 112 - "typing"
Cohesion: 0.17
Nodes (19): asyncio, ConversationEvent, ConversationReply, Strict private-chat normalization and token-safe Telegram HTTP transport., Telegram transport and tenant-scoped identity helpers., Durable deliveries for explicit staff replies, payment events and consented…, Durable private-chat intake and transactional engine/outbox processing., Real database delivery claims, deduplication, ordering and ambiguous-send… (+11 more)

### Community 113 - "sqlalchemy"
Cohesion: 0.16
Nodes (17): Audit-log write helper. :func:`write_audit_log` is the one path significant…, Application form submissions and their payment orders., AuditLog, Append-only audit trail (SPEC §12 / security-and-production.md)., One recorded significant action (state change, payment, deletion, takeover).…, Lead, its semantic facts (lead_facts), and episodic messages (ADR-004)., capture_event(), Connection (+9 more)

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

### Community 119 - "update"
Cohesion: 0.22
Nodes (13): deliver(), dispatch_pending(), UUID, recovery_loop(), dispatch_due(), recover_payments(), main(), Produce due reminder jobs and recover queued deliveries; safe to run after… (+5 more)

### Community 120 - "live"
Cohesion: 0.19
Nodes (13): Acknowledge, current(), live(), Any, AsyncSession, BaseModel, Db, get (+5 more)

### Community 121 - "Language review packet"
Cohesion: 0.50
Nodes (4): Current templates, Language review packet, Live exercise, Reminder consent and outreach copy

### Community 122 - "get_sessionmaker"
Cohesion: 0.20
Nodes (14): async_sessionmaker, get_session(), get_sessionmaker(), AsyncSession, Async engine and session factory. Built lazily from ``settings.database_url``…, Return the process-wide async session factory., FastAPI dependency yielding a session that closes after the request., process_telegram_event() (+6 more)

### Community 123 - "reindex_names.py"
Cohesion: 0.36
Nodes (7): main(), AsyncSession, UUID, Backfill encrypted lead names from latest submitted forms and rebuild blind…, reindex_batch(), test_index_rename_clear_and_legacy_backfill(), exercise()

### Community 124 - "WhatsApp readiness check — October 22, 2026"
Cohesion: 0.15
Nodes (13): Decision so far, Delivery diagnosis and configuration repair (October 23, approximately 00:16 IST), Evidence collected before configuration, Final Postman retry (October 23), Live checkpoint (approximately 22:54 IST), Missing-reply investigation (approximately 22:59 IST), New test account configuration (October 23, approximately 09:45 IST), Next live checks and evidence required (+5 more)

### Community 125 - "staff/applications.py"
Cohesion: 0.27
Nodes (13): CRM search and institution downloads, ApplicationStatus, Application review status (SPEC §7.9 / lifecycle)., applications(), detail(), owned(), Any, Db (+5 more)

### Community 126 - "receiver.py"
Cohesion: 0.24
Nodes (11): argparse, main(), provision_bot(), UUID, One advisory-locked long poller per bot, with durable offsets and queue…, recovery(), run(), accept_update() (+3 more)

### Community 127 - "retrieval.py"
Cohesion: 0.23
Nodes (8): BaseModel, Translate non-ASCII questions for English reference material without lowering…, retrieval_query(), RetrievalQuery, MonkeyPatch, Translate retrieval queries without weakening the relevance floor., test_english_query_does_not_call_model(), test_non_ascii_query_uses_validated_translation()

### Community 128 - "payments.tsx"
Cohesion: 0.32
Nodes (6): label(), money(), outcomes, Payment, Payments(), statuses

### Community 129 - "test_expired_lease_recovery_cap_and_configuration_cancellation"
Cohesion: 0.18
Nodes (9): configure(), event_for(), test_delivery_claim_retry_and_minimal_payload(), exercise(), test_expired_lease_recovery_cap_and_configuration_cancellation(), exercise(), inspect(), test_source_transaction_rolls_back_event_and_outbox() (+1 more)

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

### Community 135 - "test_knowledge_workspace.py"
Cohesion: 0.08
Nodes (32): decrypt_bytes(), _fernet(), Application-layer PII protection: symmetric encryption + deterministic hashing.…, Authenticate and decrypt source bytes for an authorized ingestion task., Institution document extraction, durable ingestion and retrieval., process_upload(), UUID, Durable upload claims, bounded embedding and atomic publication of ready… (+24 more)

### Community 136 - "payments/service.py"
Cohesion: 0.28
Nodes (8): EncryptionKeyNotConfiguredError, RuntimeError, Raised when a PII helper is used but its key is unset in settings., process_payment(), Explicit fee requests, immutable invoices and recoverable payment-link creation., create_payment_link(), task, cryptography_fernet

### Community 137 - "page.tsx"
Cohesion: 0.14
Nodes (10): DeliveryBudget(), Usage, Exports(), Configuration, Integrations(), Request, Doc, errors (+2 more)

### Community 138 - "index_known_name"
Cohesion: 0.40
Nodes (5): index_known_name(), Connection, Mapper, Keep index updates atomic with encrypted names, including name removal., listens_for

### Community 139 - "test_mutex.py"
Cohesion: 0.33
Nodes (5): MutexAcquireError, RuntimeError, Redis distributed mutex with owner-safe release and keepalive (Task 7). Ensures…, Raised when the mutex cannot be acquired after all retries., Tests for the Redis distributed mutex (Task 7). The mutex must guarantee: 1.…

### Community 140 - "timeline.py"
Cohesion: 0.29
Nodes (6): Cursor, BaseModel, datetime, field_validator, Bounded chronological transcript across inbound, replies and standalone…, base64

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

### Community 147 - "notifications.tsx"
Cohesion: 0.33
Nodes (4): labels, Notice, Notifications(), Snapshot

### Community 148 - "ExtractionResponse"
Cohesion: 0.67
Nodes (3): ExtractionResponse, BaseModel, Structured output expected from the LLM when extracting fields.

### Community 149 - "Implementation Plan: AdmitFlow"
Cohesion: 0.40
Nodes (4): Architecture Decisions, Implementation Plan: AdmitFlow, Overview, Risks and Mitigations

### Community 150 - "AdmitFlow submission requirements"
Cohesion: 0.50
Nodes (4): AdmitFlow submission requirements, Demonstration, Required artifacts, Truthful claims

### Community 151 - "TriageResponse"
Cohesion: 0.67
Nodes (3): BaseModel, Structured output expected from the LLM triage classifier., TriageResponse

## Knowledge Gaps
- **409 isolated node(s):** `admitflow-backend`, `fs`, `path`, `crypto`, `root` (+404 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1071 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CRM search and institution downloads` connect `staff/applications.py` to `test_staff_payments.py`, `AdmitFlow Complete Specification`, `write_audit_log`?**
  _High betweenness centrality (0.114) - this node is a cross-community bridge._
- **Why does `LeadStatus` connect `LeadStatus` to `test_expired_lease_recovery_cap_and_configuration_cancellation`, `write_audit_log`, `journey.py`, `payments/service.py`, `encrypt_pii`, `Lead`, `exports.py`, `Course`, `models/__init__.py`, `crm.py`, `outreach/followups.py`, `analytics`, `operations.py`, `integration/test_followups.py`, `test_payment_jobs.py`, `test_staff_payments.py`, `Reply`, `staff/payments.py`, `get_engine`, `test_telegram_journey.py`, `signin`, `integration/test_telegram_identity.py`, `handle_turn`, `Settings`, `test_qualification.py`, `payments/webhook.py`, `typing`, `sqlalchemy`, `staff/applications.py`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `write_audit_log()` connect `write_audit_log` to `test_expired_lease_recovery_cap_and_configuration_cancellation`, `test_knowledge_workspace.py`, `journey.py`, `payments/service.py`, `transport.py`, `Phase 1: Foundation`, `Lead`, `exports.py`, `models/__init__.py`, `management.py`, `outreach/followups.py`, `analytics`, `auth.py`, `operations.py`, `test_staff_payments.py`, `copilot.py`, `Login`, `Reply`, `staff/payments.py`, `api.py`, `provision_payments.py`, `consent.py`, `integration/test_telegram_identity.py`, `payments/webhook.py`, `typing`, `sqlalchemy`, `update`, `live`, `get_sessionmaker`, `staff/applications.py`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `encrypt_pii()` (e.g. with `Consequences` and `Decision`) actually correct?**
  _`encrypt_pii()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 54 inferred relationships involving `LeadStatus` (e.g. with `record_stage_changes()` and `Lead`) actually correct?**
  _`LeadStatus` has 54 INFERRED edges - model-reasoned connections that need verification._
- **What connects `admitflow-backend`, `fs`, `path` to the rest of the system?**
  _409 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `write_audit_log` be split into smaller, more focused modules?**
  _Cohesion score 0.13793103448275862 - nodes in this community are weakly interconnected._