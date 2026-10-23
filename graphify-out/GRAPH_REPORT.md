# Graph Report - admitflow  (2026-10-24)

## Corpus Check
- 223 files · ~118,565 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 3, .example 2, .ini 1)

## Summary
- 2029 nodes · 5305 edges · 141 communities (126 shown, 15 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 336 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `64105a90`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ADR-008: System-1 Decision Layer (Laya / Jev)
- Conversation Engine (hand-rolled dispatcher)
- AdmitFlow Complete Specification
- Finalized Production Stack
- lead.py
- test_guardrails.py
- Code Owns the Money
- journey.py
- RedisMutex
- generate_completion
- WhatsAppSender
- WhatsApp readiness check — October 22, 2026
- payments/service.py
- core/rag.py
- PII Encryption & Audit Log
- Razorpay Payment Integration
- get_settings
- admissions.tsx
- dispatcher.py
- tests/test_telegram_identity.py
- AIBoomi Startup Weekend Kochi: fresh-session context
- enums.py
- test_webhook.py
- test_telegram_journey.py
- LeadStatus
- Stages
- knowledge/processing.py
- test_knowledge_workspace.py
- run_postman_check.cjs
- Task List
- test_rag_node.py
- test_tenant_fk_and_unique_constraints_hold
- Phase 5: Dashboard Frontend (Next.js)
- management.py
- Code Standards
- normalize_e164
- Event preparation and execution plan
- 7. Core Feature Specifications
- workspace
- main.py
- auth.py
- test_payment_conversation.py
- Hackathon resources for AdmitFlow
- manifest.json
- test_workspace_limits.py
- AdmitFlow: current state and planning baseline
- AdmitFlow: AIBoomi submission plan
- AdmitFlow — Complete Specification
- 13. Dashboard Features
- RazorpayClient
- ADR-011: Advanced RAG Strategy (Latency vs Precision)
- Testing
- Settings
- AdmitFlow project handoff
- detect_intent
- ADR-009: Application-Layer PII Encryption and Audit Logging
- ExtractionError
- sqlalchemy_ext_asyncio
- copilot.py
- ADR-010: Triage Fallback Routing (Anti-Spam)
- ADR-012: Telegram and OpenAI for the first complete admissions MVP
- test_staff_operations.py
- compilerOptions
- Course
- 11. Human-in-the-Loop (Full Workflow)
- Implementation Plan: AdmitFlow
- api.py
- AdmitFlow Backend
- encrypt_pii
- get_engine
- Official source snapshots
- TelegramClient
- 10. Observability & Tracing
- 2. Boundaries & Invariants
- 3. Tech Stack & Commands
- management.tsx
- 8. RAG (Retrieval-Augmented Generation)
- AdmitFlow execution and demonstration checklist
- pytest
- verify.sh
- db/__init__.py
- src/__init__.py
- tasks/__init__.py
- process_event
- whatsapp/__init__.py
- integration/__init__.py
- admitflow-backend
- decrypt_pii
- AdmitFlow
- models/__init__.py
- test_payment_contracts.py
- Phase 3: AI Core (Engine + RAG)
- evaluate
- Git & GitHub Workflow
- package.json
- log_delivery_status
- record-demo.mjs
- AGENTS.md
- Security & Production Readiness
- AdmitFlow — Task List
- next-env.d.ts
- payments/webhook.py
- scripts/__init__.py
- layout.tsx
- frontend/AGENTS.md
- scripts
- Local Telegram/OpenAI runtime
- AdmitFlow pitch deck copy
- Phase 3–4 addition (see ADR-008)
- Phase 4: Advanced Bot Features
- write_audit_log
- Quality Gates — Definition of Done
- Phase 6: Production Hardening
- devDependencies
- page.tsx
- dependencies
- json
- timeline.py
- README.md
- test_payment_jobs.py
- Reply
- staff/payments.py
- get_sessionmaker
- test_escalation.py
- enqueue_outbound
- payments.tsx
- conftest.py
- react
- api
- retrieval.py
- env.py
- receiver.py
- decrypt_bytes
- Phase 1: Foundation
- Admissions
- tasks/outbound.py
- 5. Code Style
- 17. Decisions & Open Questions

## God Nodes (most connected - your core abstractions)
1. `encrypt_pii()` - 82 edges
2. `get_settings()` - 74 edges
3. `LeadStatus` - 67 edges
4. `write_audit_log()` - 61 edges
5. `Reply` - 61 edges
6. `TelegramBot` - 60 edges
7. `decrypt_pii()` - 59 edges
8. `Lead` - 53 edges
9. `Settings` - 44 edges
10. `get_sessionmaker()` - 43 edges

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

## Communities (141 total, 15 thin omitted)

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

### Community 4 - "lead.py"
Cohesion: 0.13
Nodes (34): IdMixin, Declarative base, metadata naming convention, and shared column mixins. Every…, UUID primary key with an application-side default. UUIDs avoid cross-tenant…, Server-side created/updated timestamps., Row-level tenant scoping (ADR-003). Mixed into every tenant-scoped table., TenantMixin, TimestampMixin, Application (+26 more)

### Community 5 - "test_guardrails.py"
Cohesion: 0.09
Nodes (33): apply_whatsapp_formatting(), check_input_safety(), check_output_safety(), _deterministic_check(), InputGuardrailResult, LLMGuardrailResponse, LLMOutputGuardrailResponse, OutputGuardrailResult (+25 more)

### Community 6 - "Code Owns the Money"
Cohesion: 0.50
Nodes (5): ADR-006: Code-Owned Qualification and Payments, Intent: Admissions Flow and Discounts, Discount Codes, Code Owns Eligibility, Code Owns the Money

### Community 7 - "journey.py"
Cohesion: 0.17
Nodes (32): QualificationRule, A structured eligibility rule evaluated in code, not by the LLM (ADR-006).…, Lead, A prospective applicant with optional phone contact and channel identities.…, answer_question(), build_reply(), button(), copy() (+24 more)

### Community 8 - "RedisMutex"
Cohesion: 0.07
Nodes (27): MutexAcquireError, Redis, RuntimeError, Redis distributed mutex with owner-safe release and keepalive (Task 7). Ensures…, Background loop that extends the TTL while the lock is held., Raised when the mutex cannot be acquired after all retries., Async context-manager mutex backed by Redis ``SET NX``. Parameters: redis: An…, Attempt to acquire the lock, retrying up to ``retry_count`` times. (+19 more)

### Community 9 - "generate_completion"
Cohesion: 0.16
Nodes (18): AllProvidersFailedError, generate_completion(), Any, Exception, Bounded OpenAI-only model roles; provider details never escape in errors., Raised when the entire LLM fallback chain is exhausted., Generate a completion with automatic provider fallback. Tries the fast model,…, asyncio (+10 more)

### Community 10 - "WhatsAppSender"
Cohesion: 0.09
Nodes (23): Any, Send an interactive list message. `sections` is a list of section dicts…, Send a pre-approved template message., Service for sending messages via Meta WhatsApp Cloud API., Post the payload to Meta and extract the created message ID., Meta API expects the phone number without the leading '+'., Send a simple text message. Returns the Meta message ID., Send an interactive message with up to 3 buttons. `buttons` should be a list of… (+15 more)

### Community 11 - "WhatsApp readiness check — October 22, 2026"
Cohesion: 0.07
Nodes (28): ping(), process_inbound_message(), Any, task, Background tasks for message processing. For now this module holds only the…, Smoke-test task: returns ``{"result": payload}``. Enqueued from the…, Process an inbound WhatsApp message (Task 17). This is a placeholder for the…, Tests for the TaskIQ broker setup and task execution (Task 3). All tests run… (+20 more)

### Community 12 - "payments/service.py"
Cohesion: 0.18
Nodes (20): ApplicationStatus, DiscountType, PaymentStatus, How a discount code reduces the fee., Payment order lifecycle (SPEC §7.10)., Application review status (SPEC §7.9 / lifecycle)., existing_payment(), fee_details() (+12 more)

### Community 13 - "core/rag.py"
Cohesion: 0.13
Nodes (21): chunk_text(), embed_text(), ingest_document(), Any, AsyncSession, UUID, RAG pipeline core logic (Task 13). Handles ingestion (chunking, embedding),…, Hybrid search (dense + lexical with RRF). (+13 more)

### Community 16 - "get_settings"
Cohesion: 0.07
Nodes (31): AsyncBroker, Shared async Redis client for application code. Carry-over prerequisite #1: the…, get_settings(), Application settings singleton. Loads configuration from the environment (and…, Return the process-wide :class:`Settings` singleton., _build_broker(), TaskIQ broker singleton. In production (and local dev with Redis running) the…, Construct the right broker based on the current settings. This is a plain… (+23 more)

### Community 17 - "admissions.tsx"
Cohesion: 0.19
Nodes (11): Detail, Human, Inquiry, labels, Request, RuleEvidence, Request, StaffControls() (+3 more)

### Community 18 - "dispatcher.py"
Cohesion: 0.14
Nodes (19): MessageDirection, Direction of a WhatsApp message row (episodic memory, ADR-004)., _flush_engine_state(), handle_turn(), _load_engine_state(), Any, AsyncSession, Engine Dispatcher (Task 8 & 17). This module contains the main entry point for… (+11 more)

### Community 19 - "tests/test_telegram_identity.py"
Cohesion: 0.19
Nodes (10): hash_telegram_identifier(), UUID, Private Telegram identity lookup without storing raw identifiers in indexes., Hash an identifier in its tenant/bot/type domain using the lookup secret. This…, MonkeyPatch, parametrize, Telegram identities must be independent of phone numbers and tenant-bound., test_lookup_hash_is_stable_scoped_and_does_not_reveal_identifiers() (+2 more)

### Community 20 - "AIBoomi Startup Weekend Kochi: fresh-session context"
Cohesion: 0.11
Nodes (19): AIBoomi Startup Weekend Kochi: fresh-session context, Assessment and next decision, Current readiness session (October 22), Event sources and local copies, Existing prototype rule and surprise element, Existing working-tree changes, Fresh-message prompt, Handoff status (+11 more)

### Community 21 - "enums.py"
Cohesion: 0.16
Nodes (19): Enumerated types used across the schema. These are Python ``str`` enums mapped…, Qualification-rule comparison operators (SPEC §7.4). Evaluated…, RuleOperator, ExtractionResponse, BaseModel, Qualification Node (Task 15). Extracts rule fields using the LLM and runs…, Structured output expected from the LLM when extracting fields., _coerce_values() (+11 more)

### Community 22 - "test_webhook.py"
Cohesion: 0.11
Nodes (19): parametrize, test_delivery_status_logs_are_authenticated_and_exclude_pii(), test_tunnel_app_exposes_no_other_routes(), test_tunnel_app_keeps_webhook_verification(), app(), client(), mock_settings(), Any (+11 more)

### Community 23 - "test_telegram_journey.py"
Cohesion: 0.10
Nodes (20): Application-layer PII protection: symmetric encryption + deterministic hashing.…, Channel-neutral input and validated plain-text reply boundary., Input Guardrail Node (Task 10). Detects prompt injection, profanity, and abuse…, BaseModel, Triage Node (Task 11). Routes incoming messages to the appropriate downstream…, Structured output expected from the LLM triage classifier., TriageResponse, Strict private-chat normalization and token-safe Telegram HTTP transport. (+12 more)

### Community 24 - "LeadStatus"
Cohesion: 0.11
Nodes (31): LeadStatus, Lead lifecycle states (SPEC §7.3). Where a lead *stands*, not a fixed track —…, AsyncSession, Run the qualification loop., run_qualification(), EngineState, InvalidTransitionError, BaseModel (+23 more)

### Community 25 - "Stages"
Cohesion: 0.13
Nodes (15): 10. Reflect & learn, 1. Understand & spec  (`/spec`), 2. Plan & pick a task  (`/plan`), 3. Branch, 4. Build with TDD  (`/build`, `/test`), 5. Verify (the quality gate), 6. Self-review, then adversarial review  (`/review`), 7. Commit & open the PR (+7 more)

### Community 26 - "knowledge/processing.py"
Cohesion: 0.15
Nodes (16): embed_chunks(), process_upload(), UUID, Durable upload claims, bounded embedding and atomic publication of ready…, Use the configured OpenAI model with the database's explicit 1536 dimensions., Claim once, process outside the transaction, then publish only the current…, main(), Probe (+8 more)

### Community 27 - "test_knowledge_workspace.py"
Cohesion: 0.06
Nodes (28): alembic, alembic_config, columns(), Column, upgrade(), Column, DateTime, _timestamps() (+20 more)

### Community 28 - "run_postman_check.cjs"
Cohesion: 0.18
Nodes (9): collection, config, crypto, fs, keys, newman, path, root (+1 more)

### Community 29 - "Task List"
Cohesion: 0.15
Nodes (13): Checkpoint: Advanced Features, Checkpoint: AI Core, Checkpoint: Dashboard Complete, Checkpoint: Foundation, Checkpoint: Production Ready, Checkpoint: WhatsApp Ingress, Phase 1: Foundation, Phase 2: WhatsApp Ingress (+5 more)

### Community 30 - "test_rag_node.py"
Cohesion: 0.23
Nodes (11): process_rag_node(), AsyncSession, Retrieve context and answer knowledge questions., mock_state(), asyncio, fixture, patch, Unit tests for the RAG node. (+3 more)

### Community 31 - "test_tenant_fk_and_unique_constraints_hold"
Cohesion: 0.17
Nodes (13): _alembic_config(), monkeypatch_session(), pg_url(), fixture, MonkeyPatch, Start Postgres, point settings at it, yield the asyncpg URL., The tier requirement: alembic upgrade head then downgrade base, both clean., Round-trip an Institution -> Lead; the tenant FK + phone uniqueness bind. (+5 more)

### Community 32 - "Phase 5: Dashboard Frontend (Next.js)"
Cohesion: 0.17
Nodes (12): Phase 5: Dashboard Frontend (Next.js), Task 24: Initialize Next.js + dark mode + glassmorphism, Task 25: Authentication (email + password), Task 26: Dashboard home (funnel analytics), Task 27: Leads CRM page, Task 28: Course & batch management, Task 29: Chat takeover + co-pilot UI, Task 30: Document management (RAG) (+4 more)

### Community 33 - "management.py"
Cohesion: 0.14
Nodes (36): require_admin(), archive_course(), archive_discount(), BatchInput, catalog(), catalog_detail(), course_view(), CourseInput (+28 more)

### Community 34 - "Code Standards"
Cohesion: 0.18
Nodes (11): Async & I/O, Code Standards, Configuration — settings, not literals, Dependencies, Errors, Formatting, LLM calls, Logging & observability (+3 more)

### Community 35 - "normalize_e164"
Cohesion: 0.14
Nodes (10): InvalidPhoneError, normalize_e164(), ValueError, E.164 phone-number normalization. Carry-over prerequisite #3: un-normalized…, Raised when a phone string cannot be normalized to E.164., Normalize *raw* into canonical E.164 (``+<digits>``). Strips whitespace,…, Tests for E.164 phone normalization (carry-over prerequisite #3). The…, normalize_e164 → canonical E.164 string. (+2 more)

### Community 36 - "Event preparation and execution plan"
Cohesion: 0.18
Nodes (11): Business and mentor preparation, Evaluation and demo evidence, Event preparation and execution plan, Kickoff disclosure draft, Latest direction (October 23), Minimum demonstrable product, Next action: one-hour v1 readiness check, Submission checklist (+3 more)

### Community 37 - "7. Core Feature Specifications"
Cohesion: 0.18
Nodes (11): 7.10 Payment Integration & Discounts (Razorpay), 7.1 WhatsApp Number Architecture, 7.2 Multi-Tenancy (Row-Level Isolation), 7.3 Lead Lifecycle States, 7.4 Course Qualification Rules (Structured), 7.5 Batch & Intake Management, 7.6 Cold Lead Re-engagement, 7.7 Language Support (+3 more)

### Community 38 - "workspace"
Cohesion: 0.10
Nodes (22): Code-owned application fees and authenticated Razorpay payment processing., payments(), Any, get, fixture, workspace(), Any, UUID (+14 more)

### Community 39 - "main.py"
Cohesion: 0.10
Nodes (18): recovery_loop(), create_app(), ready(), lifespan(), FastAPI, FastAPI application entry point. Boots the API, manages the TaskIQ broker…, Start / stop the TaskIQ broker alongside the FastAPI process. The…, Application factory — builds and configures the FastAPI instance. (+10 more)

### Community 40 - "auth.py"
Cohesion: 0.17
Nodes (19): Login, logout(), me(), BaseModel, Db, get, post, Request (+11 more)

### Community 41 - "test_payment_conversation.py"
Cohesion: 0.14
Nodes (19): normalize_update(), protect_logs(), TaskIQ changes log levels; redact before either HTTP client or root handlers…, TokenSafeFilter, callback_data(), parse_callback(), UUID, Compact callback signatures bind catalog/language choices to one conversation. (+11 more)

### Community 42 - "Hackathon resources for AdmitFlow"
Cohesion: 0.20
Nodes (10): Acceptance before using a resource, Event and release boundaries, Goal, Hackathon resources for AdmitFlow, October 23 Downloads guide: hosted inference access, Participant credits and other support, Suggested allocation and activation order, Useful resources mapped to the plan (+2 more)

### Community 43 - "manifest.json"
Cohesion: 0.20
Nodes (9): SPEC.md, bytes, sha256, tasks/plan.md, bytes, sha256, tasks/todo.md, bytes (+1 more)

### Community 44 - "test_workspace_limits.py"
Cohesion: 0.09
Nodes (19): ASGIApp, Reject oversized multipart streams before they can fill temporary storage., UploadBodyLimit, private_send(), check_login_limit(), Request, MonkeyPatch, Bound resource use and reject browser cross-origin mutations before database… (+11 more)

### Community 45 - "AdmitFlow: current state and planning baseline"
Cohesion: 0.22
Nodes (9): AdmitFlow: current state and planning baseline, Confirmed user direction, Feature status and integration gaps, Features to finalize next, How to reconcile the planning documents, Proposed architecture for the next plan, Stack inventory, Verification evidence and its limits (+1 more)

### Community 46 - "AdmitFlow: AIBoomi submission plan"
Cohesion: 0.22
Nodes (9): AdmitFlow: AIBoomi submission plan, Deck and presentation, Open decisions, Proposed schedule from Friday evening, Submission outcome, The journey to demonstrate, Use the provided resources, What must be handed in (+1 more)

### Community 47 - "AdmitFlow — Complete Specification"
Cohesion: 0.22
Nodes (9): 12. Edge Cases & Error Handling, 14. Data Privacy (DPDPA-Ready), 15. Memory Architecture, 16. Success Criteria, 1. Objective, 4. Project Structure, 6. Testing Strategy, 9. Guardrails (Three-Layer) (+1 more)

### Community 48 - "13. Dashboard Features"
Cohesion: 0.22
Nodes (9): 13.1 Authentication, 13.2 Roles & Permissions, 13.3 UI Aesthetic, 13.4 Real-Time Notifications, 13.5 Funnel Analytics, 13.6 Data Export & Integration, 13.7 Document Management (RAG), 13.8 Onboarding (MVP) (+1 more)

### Community 49 - "RazorpayClient"
Cohesion: 0.16
Nodes (14): AsyncBaseTransport, PaymentLink, PaymentProviderError, BaseModel, Exception, field_validator, Read an existing exact reference; absence never authorizes another creation., RazorpayClient (+6 more)

### Community 50 - "ADR-011: Advanced RAG Strategy (Latency vs Precision)"
Cohesion: 0.25
Nodes (7): 1. Complex Document Ingestion (`docling` or `unstructured`), 2. Pluggable Reranking Architecture (Cohere API over Local CPU), 3. Contextual Query Rewriting, ADR-011: Advanced RAG Strategy (Latency vs Precision), Consequences, Context, Decision

### Community 51 - "Testing"
Cohesion: 0.25
Nodes (8): Coverage, LLM and decision-layer tests, Philosophy — pragmatic TDD, Running tests, Test layout, Testing, The two patterns, Unit vs integration

### Community 52 - "Settings"
Cohesion: 0.13
Nodes (26): Core cross-cutting concerns: settings, security, schemas, guardrails, tracing., hash_phone(), Return a deterministic keyed hash of a phone number for lookup/dedup. Keyed…, Environment-backed application configuration., Settings, configured_keys(), fixture, MonkeyPatch (+18 more)

### Community 53 - "AdmitFlow project handoff"
Cohesion: 0.25
Nodes (8): AdmitFlow project handoff, Current direction, Development rules, Event submission, Execution checkpoint, First usable release, Historical evidence, Resume prompt

### Community 54 - "detect_intent"
Cohesion: 0.20
Nodes (15): detect_intent(), Classify the user's intent to route to the correct node. Design Decision: If a…, asyncio, Test routing for course discovery., Test routing for knowledge questions., Test routing for qualification answers., Test routing for human handoff., Test routing for empty messages without calling LLM defaults to discovery. (+7 more)

### Community 55 - "ADR-009: Application-Layer PII Encryption and Audit Logging"
Cohesion: 0.15
Nodes (12): DatabaseNotConfiguredError, RuntimeError, Raised when a DB session is requested but ``DATABASE_URL`` is unset., ADR-009: Application-Layer PII Encryption and Audit Logging, Alternatives Considered, Consequences, Context, Decision (+4 more)

### Community 56 - "ExtractionError"
Cohesion: 0.24
Nodes (16): extract_file(), ExtractionError, ValueError, Bounded extraction of institution reference documents; never execute uploads., A safe, public error code rather than parser output containing document text., validate_path(), parametrize, Untrusted institutional files must extract safely or fail explicitly. (+8 more)

### Community 57 - "sqlalchemy_ext_asyncio"
Cohesion: 0.19
Nodes (9): Discovery Node (Task 12). Presents available courses as WhatsApp interactive…, RAG Node (Task 14). Graph node that retrieves from the knowledge base and…, RuntimeError, WhatsApp message sending service (Task 6). Uses httpx2 to call the Meta Graph…, Raised when the Meta Cloud API returns an error response., WhatsAppAPIError, Tests for the WhatsApp Message Sending Service (Task 6). The sender calls the…, sqlalchemy_ext_asyncio (+1 more)

### Community 58 - "copilot.py"
Cohesion: 0.16
Nodes (18): content(), decide(), DraftContent, DraftDecision, DraftRequest, generate(), latest(), Any (+10 more)

### Community 59 - "ADR-010: Triage Fallback Routing (Anti-Spam)"
Cohesion: 0.33
Nodes (5): ADR-010: Triage Fallback Routing (Anti-Spam), Consequences, Context, Decision, Status

### Community 60 - "ADR-012: Telegram and OpenAI for the first complete admissions MVP"
Cohesion: 0.29
Nodes (7): ADR-012: Telegram and OpenAI for the first complete admissions MVP, Consequences, Context, Decision, Implemented runtime boundaries, References and verification, Supersession and preserved decisions

### Community 61 - "test_staff_operations.py"
Cohesion: 0.08
Nodes (35): Any, Real database management: administrator writes, role/tenant boundaries and…, test_catalog_writes_validate_rules_capacity_and_ownership(), test_discount_management_rejects_invalid_values_duplicates_and_foreign_writes(), test_settings_validate_timezone_hours_and_tenant_scope(), fake_embeddings(), Any, MonkeyPatch (+27 more)

### Community 63 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 64 - "Course"
Cohesion: 0.13
Nodes (22): argparse, Dashboard access role (SPEC — admin vs agent)., StaffRole, Batch, Course, A program a lead can be qualified for and pay to apply to., A dated intake of a course with finite seats (SPEC §7.5)., A dashboard user (admin or agent) belonging to one institution. (+14 more)

### Community 65 - "11. Human-in-the-Loop (Full Workflow)"
Cohesion: 0.40
Nodes (5): 11.1 Auto-Escalation Triggers, 11.2 Co-pilot Mode, 11.3 Business Hours, 11.4 Never Escalate, 11. Human-in-the-Loop (Full Workflow)

### Community 66 - "Implementation Plan: AdmitFlow"
Cohesion: 0.40
Nodes (4): Architecture Decisions, Implementation Plan: AdmitFlow, Overview, Risks and Mitigations

### Community 67 - "api.py"
Cohesion: 0.17
Nodes (22): documents(), get_upload(), Any, BaseModel, Db, delete, get, post (+14 more)

### Community 68 - "AdmitFlow Backend"
Cohesion: 0.22
Nodes (9): AdmitFlow Backend, Application payments, Configuration, Current implementation and verification, Institution knowledge workspace, Local development, Stack, Staff takeover and reviewed co-pilot (+1 more)

### Community 69 - "encrypt_pii"
Cohesion: 0.12
Nodes (31): encrypt_pii(), Encrypt a PII string, returning a url-safe base64 Fernet token. Fernet is…, Trusted bot-to-institution mapping; token is application-encrypted., TelegramBot, action(), application_action(), collect_application(), prompt() (+23 more)

### Community 70 - "get_engine"
Cohesion: 0.18
Nodes (13): AsyncEngine, get_engine(), Return the process-wide async engine (one pool for the app)., main(), run(), provision(), Read-only credential probe, then encrypted institution-owned Razorpay…, migrated_db() (+5 more)

### Community 71 - "Official source snapshots"
Cohesion: 0.50
Nodes (4): Conflicts to confirm, October 23 planning refresh, Official source snapshots, Sources

### Community 72 - "TelegramClient"
Cohesion: 0.18
Nodes (12): Any, RuntimeError, TelegramAPIError, TelegramClient, Any, MonkeyPatch, test_outbound_dedup_claims_order_and_uncertainty(), deliver() (+4 more)

### Community 73 - "10. Observability & Tracing"
Cohesion: 0.50
Nodes (4): 10.1 LLM Tracing (Langfuse), 10.2 Structured Logging, 10.3 Error Monitoring (Sentry), 10. Observability & Tracing

### Community 74 - "2. Boundaries & Invariants"
Cohesion: 0.50
Nodes (4): 2. Boundaries & Invariants, Always Do, Ask First, Never Do

### Community 75 - "3. Tech Stack & Commands"
Cohesion: 0.50
Nodes (4): 3. Tech Stack & Commands, Deployment, Hybrid Architecture, Key Commands

### Community 76 - "management.tsx"
Cohesion: 0.14
Nodes (10): Batch, Course, empty, Management(), operators, parseValue(), Rule, Settings (+2 more)

### Community 77 - "8. RAG (Retrieval-Augmented Generation)"
Cohesion: 0.50
Nodes (4): 8.1 Per-Institution Knowledge Base, 8.2 Retrieval Pipeline, 8.3 RAG Guardrail, 8. RAG (Retrieval-Augmented Generation)

### Community 78 - "AdmitFlow execution and demonstration checklist"
Cohesion: 0.67
Nodes (3): AdmitFlow execution and demonstration checklist, Build and verify, Demonstrate and submit

### Community 79 - "pytest"
Cohesion: 0.10
Nodes (20): get_redis(), Redis, RuntimeError, Raised when Redis is needed but ``REDIS_URL`` is unset in settings., Return the process-wide async Redis client singleton. The client is created…, RedisNotConfiguredError, Any, asyncio (+12 more)

### Community 84 - "process_event"
Cohesion: 0.38
Nodes (7): process_telegram_event(), task, send_telegram_reply(), process_event(), UUID, Serialize by locked lead, then atomically commit memory, result and one reply., send_reply()

### Community 89 - "decrypt_pii"
Cohesion: 0.11
Nodes (21): decrypt_pii(), Decrypt a token produced by :func:`encrypt_pii`. Raises…, send(), change_then_reply(), expire(), cancel_then_fail(), verify(), completion() (+13 more)

### Community 90 - "AdmitFlow"
Cohesion: 0.33
Nodes (6): AdmitFlow, Current status, Demonstration and submission, Development, Product scope, Stack

### Community 91 - "models/__init__.py"
Cohesion: 0.11
Nodes (24): Base, Declarative base shared by every AdmitFlow model., AuditLog, One recorded significant action (state change, payment, deletion, takeover).…, ConversationEvent, ConversationMemory, ConversationReply, HumanRequest (+16 more)

### Community 92 - "test_payment_contracts.py"
Cohesion: 0.13
Nodes (17): Credentials, Bounded Razorpay requests; ambiguous link creation is never blindly retried., discounted_amount(), Integer monetary arithmetic and exact-byte webhook authentication., verify_webhook(), MonkeyPatch, parametrize, Money stays integer/code-owned; signatures use exact bytes; creation never… (+9 more)

### Community 94 - "Phase 3: AI Core (Engine + RAG)"
Cohesion: 0.18
Nodes (11): Phase 3: AI Core (Engine + RAG), Task 10: Input guardrail node, Task 11: Triage node (intent detection), Task 12: Discovery node, Task 13: RAG pipeline, Task 14: RAG node, Task 15: Qualification node, Task 16: Output guardrail (+3 more)

### Community 95 - "evaluate"
Cohesion: 0.33
Nodes (9): Case, cases(), evaluate(), main(), BaseModel, score_answer(), Evaluation rejects irrelevant quotations and does not count provider errors as…, test_supported_answer_requires_expected_fact_and_reference() (+1 more)

### Community 96 - "Git & GitHub Workflow"
Cohesion: 0.22
Nodes (9): Branching model — feature branch → PR → `main`, Commits — Conventional Commits, small and coherent, Git & GitHub Workflow, Merging, No AI attribution — the human is the sole author  ⚠️, Pull Requests, Review gate — adversarial, before merge, What never gets committed (+1 more)

### Community 97 - "package.json"
Cohesion: 0.22
Nodes (8): name, private, version, react-dom, @types/node, @types/react, @types/react-dom, typescript

### Community 98 - "log_delivery_status"
Cohesion: 0.40
Nodes (5): log_delivery_status(), Request, Response, Observe only authenticated status events, without recipient or error text., middleware

### Community 99 - "record-demo.mjs"
Cohesion: 0.20
Nodes (7): credentials, headers, journey, target, ref_node_fs, ref_node_path, @playwright/test

### Community 100 - "AGENTS.md"
Cohesion: 0.25
Nodes (7): AIBoomi Startup Weekend handoff, How we build — read the handbook, Knowledge graph, Quick commands (from `backend/`), The rules you cannot skip, What this project is, Workflow triggers

### Community 101 - "Security & Production Readiness"
Cohesion: 0.18
Nodes (11): Dependency & secret scanning, Deploy & rollback, External surfaces, Guardrails & money, Local full-stack (docker-compose), Multi-tenancy — isolation is a correctness bug if wrong, Observability, PII & data protection (DPDPA) (+3 more)

### Community 102 - "AdmitFlow — Task List"
Cohesion: 0.25
Nodes (8): AdmitFlow — Task List, AIBoomi Startup Weekend session handoff (2026-10-22), Current direction and hackathon resources (2026-10-23), Final Postman diagnostic (October 23, executed; delivery blocked), Readiness blocker: idle Redis worker restart (in progress), Readiness tunnel setup (in progress), Test-number delivery diagnosis (October 23, blocked on Meta account restriction), WhatsApp readiness check (2026-10-22, in progress)

### Community 103 - "next-env.d.ts"
Cohesion: 0.50
Nodes (3): NOTE: This file should not be edited, frontend_next_types_root_params_d, frontend_next_types_routes_d

### Community 104 - "payments/webhook.py"
Cohesion: 0.15
Nodes (18): EncryptionKeyNotConfiguredError, RuntimeError, Raised when a PII helper is used but its key is unset in settings., LinkEntity, LinkEnvelope, PaidEvent, PaidPayload, payment_webhook() (+10 more)

### Community 106 - "layout.tsx"
Cohesion: 0.25
Nodes (5): frontend_app_globals, metadata, config, @fontsource-variable/dm-sans, next

### Community 108 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, lint, record:demo, start, test:e2e:live, typecheck

### Community 109 - "Local Telegram/OpenAI runtime"
Cohesion: 0.29
Nodes (6): Configuration and data services, Local Telegram/OpenAI runtime, Migrate and seed, Packaging and release limits, Run the processes, Validate and recover

### Community 110 - "AdmitFlow pitch deck copy"
Cohesion: 0.29
Nodes (7): AdmitFlow pitch deck copy, Slide 1: AdmitFlow, Slide 2: The admissions inquiry, Slide 3: A working student journey, Slide 4: Institution knowledge and control, Slide 5: Technology and verification, Slide 6: Pilot and next steps

### Community 111 - "Phase 3–4 addition (see ADR-008)"
Cohesion: 0.29
Nodes (7): Phase 3–4 addition (see ADR-008), Task 40: `decide()` System-1 decision-layer abstraction, Task 41: Distill decisions into self-hosted Laya (post-demo), Task 42.1: Complex Document Parsing & Semantic Chunking, Task 42.2: Contextual Query Rewriting, Task 42.3: Pluggable Reranker (Cohere API vs Local), Task 42: Advanced RAG Strategy (ADR-011)

### Community 112 - "Phase 4: Advanced Bot Features"
Cohesion: 0.29
Nodes (7): Phase 4: Advanced Bot Features, Task 18: Application form collection node, Task 19: Razorpay integration, Task 20: Human handoff + co-pilot mode, Task 21: Cold lead re-engagement worker, Task 22: WhatsApp rate-limit tracking, Task 23: Langfuse tracing integration

### Community 113 - "write_audit_log"
Cohesion: 0.09
Nodes (46): Any, AsyncSession, UUID, Audit-log write helper. :func:`write_audit_log` is the one path significant…, Append one entry to ``audit_logs`` on ``session``; return it flushed, not…, write_audit_log(), resumed_status(), applications() (+38 more)

### Community 114 - "Quality Gates — Definition of Done"
Cohesion: 0.33
Nodes (6): CI mirrors this exactly, Fast iteration vs the gate, Quality Gates — Definition of Done, The baseline gate (every change), The enforced-numbers ledger, The tiers — add gates by what the change touches

### Community 115 - "Phase 6: Production Hardening"
Cohesion: 0.33
Nodes (6): Phase 6: Production Hardening, Task 35: Sentry error monitoring, Task 36: Delete My Data endpoint, Task 37: Data retention auto-cleanup, Task 38: Docker Compose for local development, Task 39: Production deployment

### Community 116 - "devDependencies"
Cohesion: 0.33
Nodes (6): devDependencies, @playwright/test, @types/node, @types/react, @types/react-dom, typescript

### Community 117 - "page.tsx"
Cohesion: 0.15
Nodes (9): Applications(), Detail, fields, statuses, Summary, Doc, errors, Match (+1 more)

### Community 118 - "dependencies"
Cohesion: 0.40
Nodes (5): dependencies, @fontsource-variable/dm-sans, next, react, react-dom

### Community 119 - "json"
Cohesion: 0.12
Nodes (16): Expose only the existing Meta webhook through the temporary demo tunnel., Five bounded live embedding searches through the real authenticated staff API., Hash the tested code/configuration without reading secrets or runtime data., Bounded login throttling; shared Redis when configured, development fallback., get, Response, WhatsApp Webhook routing (Task 5). Handles GET (challenge) and POST (incoming…, Handle Meta's webhook challenge. (+8 more)

### Community 120 - "timeline.py"
Cohesion: 0.16
Nodes (15): Event, BaseModel, Cursor, Any, AsyncSession, BaseModel, datetime, field_validator (+7 more)

### Community 121 - "README.md"
Cohesion: 0.15
Nodes (10): AI Impact Statement, Student-to-staff demonstration, Current templates, Language review packet, Live exercise, Prior-work disclosure draft, AdmitFlow submission requirements, Demonstration (+2 more)

### Community 122 - "test_payment_jobs.py"
Cohesion: 0.25
Nodes (11): asyncio, PaymentOrder, A Razorpay order for an application fee (SPEC §7.10). Amount is DB-sourced…, OutboundMessage, PaymentEvent, Immutable fee requests, bounded coupon reservations and non-repeating provider…, Any, Real database tenant ownership, deduplication and migration data-preservation… (+3 more)

### Community 123 - "Reply"
Cohesion: 0.31
Nodes (11): field_validator, Reply, button(), discount_action(), order_reply(), payment_action(), preview(), Any (+3 more)

### Community 124 - "staff/payments.py"
Cohesion: 0.53
Nodes (9): locked(), owned(), provider(), Db, post, UUID, Scoped payment monitoring and explicit, read-only provider reconciliation., reconcile() (+1 more)

### Community 125 - "get_sessionmaker"
Cohesion: 0.24
Nodes (13): async_sessionmaker, get_session(), get_sessionmaker(), AsyncSession, Return the process-wide async session factory., FastAPI dependency yielding a session that closes after the request., recover_payments(), recover_outbound() (+5 more)

### Community 126 - "test_escalation.py"
Cohesion: 0.21
Nodes (11): escalation_reason(), office_open(), datetime, Reason, Deterministic clear support signals and institution-local office hours., parametrize, Clear support signals escalate; office hours never promise an immediate reply., test_clear_escalation_signals() (+3 more)

### Community 127 - "enqueue_outbound"
Cohesion: 0.25
Nodes (6): enqueue_outbound(), AsyncSession, UUID, Any, test_signed_full_payment_is_atomic_replay_safe_and_amount_checked(), prepare()

### Community 128 - "payments.tsx"
Cohesion: 0.32
Nodes (6): label(), money(), outcomes, Payment, Payments(), statuses

### Community 129 - "conftest.py"
Cohesion: 0.29
Nodes (5): Staff authentication and institution-scoped access., isolated_local_login_windows(), fixture, MonkeyPatch, Keep development-only throttle state independent across database test cases.

### Community 130 - "react"
Cohesion: 0.29
Nodes (4): blank, Discount, Discounts(), react

### Community 131 - "api"
Cohesion: 0.48
Nodes (7): api(), Knowledge(), action(), login(), search(), upload(), send()

### Community 132 - "retrieval.py"
Cohesion: 0.23
Nodes (8): BaseModel, Translate non-ASCII questions for English reference material without lowering…, retrieval_query(), RetrievalQuery, MonkeyPatch, Translate retrieval queries without weakening the relevance floor., test_english_query_does_not_call_model(), test_non_ascii_query_uses_validated_translation()

### Community 133 - "env.py"
Cohesion: 0.22
Nodes (9): do_run_migrations(), Alembic migration environment (async). Reads the database URL from application…, Emit SQL to stdout without a live DB connection., Run migrations against a live database via an async engine., run_migrations_offline(), run_migrations_online(), Connection, logging_config (+1 more)

### Community 134 - "receiver.py"
Cohesion: 0.31
Nodes (9): main(), provision_bot(), UUID, One advisory-locked long poller per bot, with durable offsets and queue…, recovery(), run(), accept_update(), Any (+1 more)

### Community 135 - "decrypt_bytes"
Cohesion: 0.29
Nodes (8): decrypt_bytes(), encrypt_bytes(), _fernet(), Encrypt uploaded source bytes before persistence, without lossy text decoding., Authenticate and decrypt source bytes for an authorized ingestion task., readable_pdf(), test_upload_formats_search_duplicates_and_tenant_isolation(), index()

### Community 136 - "Phase 1: Foundation"
Cohesion: 0.40
Nodes (5): Phase 1: Foundation, Task 1: Initialize Python project, FastAPI, settings, and Docker, Task 2: PostgreSQL schema (SQLAlchemy + Alembic), Task 3: TaskIQ + Redis broker setup, Task 4: PII encryption utilities and audit log infrastructure

### Community 138 - "tasks/outbound.py"
Cohesion: 0.50
Nodes (3): task, Encrypted outbound-message delivery jobs carry only internal identifiers., send_outbound_message()

### Community 139 - "5. Code Style"
Cohesion: 0.50
Nodes (4): 5. Code Style, Python (Backend), Separation of Concerns, TypeScript (Frontend)

### Community 140 - "17. Decisions & Open Questions"
Cohesion: 0.67
Nodes (3): 17.1 Conversation engine — DECIDED: hand-rolled dispatcher, 17.2 Still open, 17. Decisions & Open Questions

## Knowledge Gaps
- **395 isolated node(s):** `admitflow-backend`, `fs`, `path`, `crypto`, `root` (+390 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 940 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `handle_turn()` connect `dispatcher.py` to `normalize_e164`, `lead.py`, `encrypt_pii`, `test_guardrails.py`, `journey.py`, `RedisMutex`, `WhatsAppSender`, `WhatsApp readiness check — October 22, 2026`, `17. Decisions & Open Questions`, `pytest`, `Settings`, `detect_intent`, `LeadStatus`, `Phase 3: AI Core (Engine + RAG)`, `models/__init__.py`, `get_sessionmaker`, `test_rag_node.py`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **Why does `AdmitFlow — Complete Specification` connect `AdmitFlow — Complete Specification` to `11. Human-in-the-Loop (Full Workflow)`, `7. Core Feature Specifications`, `10. Observability & Tracing`, `2. Boundaries & Invariants`, `3. Tech Stack & Commands`, `17. Decisions & Open Questions`, `5. Code Style`, `8. RAG (Retrieval-Augmented Generation)`, `13. Dashboard Features`, `2026-10-23-before-telegram-alignment/docs/event/RESOURCE_PLAN.md`?**
  _High betweenness centrality (0.106) - this node is a cross-community bridge._
- **Why does `WhatsApp readiness check — October 22, 2026` connect `WhatsApp readiness check — October 22, 2026` to `AdmitFlow Complete Specification`, `core/rag.py`?**
  _High betweenness centrality (0.100) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `encrypt_pii()` (e.g. with `Consequences` and `Decision`) actually correct?**
  _`encrypt_pii()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 41 inferred relationships involving `LeadStatus` (e.g. with `Lead` and `application_action()`) actually correct?**
  _`LeadStatus` has 41 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `Reply` (e.g. with `request_staff()` and `timeline()`) actually correct?**
  _`Reply` has 16 INFERRED edges - model-reasoned connections that need verification._
- **What connects `admitflow-backend`, `fs`, `path` to the rest of the system?**
  _395 weakly-connected nodes found - possible documentation gaps or missing edges._