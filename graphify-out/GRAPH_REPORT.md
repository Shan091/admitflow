# Graph Report - admitflow  (2026-10-24)

## Corpus Check
- 215 files · ~111,665 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 3, .example 2, .ini 1)

## Summary
- 1931 nodes · 4950 edges · 134 communities (119 shown, 15 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 332 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `37d53cc4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ADR-008: System-1 Decision Layer (Laya / Jev)
- Conversation Engine (hand-rolled dispatcher)
- AdmitFlow Complete Specification
- Finalized Production Stack
- models/__init__.py
- guardrails.py
- Code Owns the Money
- journey.py
- RedisMutex
- generate_completion
- WhatsAppSender
- WhatsApp readiness check — October 22, 2026
- TelegramBot
- core/rag.py
- PII Encryption & Audit Log
- Razorpay Payment Integration
- get_settings
- admissions.tsx
- dispatcher.py
- security.py
- AIBoomi Startup Weekend Kochi: fresh-session context
- RuleOperator
- test_webhook.py
- get_redis
- LeadStatus
- Stages
- knowledge/processing.py
- collections_abc
- run_postman_check.cjs
- Task List
- test_rag_node.py
- test_migrations.py
- Phase 5: Dashboard Frontend (Next.js)
- management.py
- Code Standards
- normalize_e164
- Event preparation and execution plan
- 7. Core Feature Specifications
- workspace
- main.py
- auth.py
- TelegramClient
- Hackathon resources for AdmitFlow
- manifest.json
- test_workspace_limits.py
- AdmitFlow: current state and planning baseline
- AdmitFlow: AIBoomi submission plan
- AdmitFlow — Complete Specification
- 13. Dashboard Features
- RazorpayClient
- ADR-011: Advanced RAG Strategy (Latency vs Precision)
- decide
- Settings
- AdmitFlow project handoff
- detect_intent
- ADR-009: Application-Layer PII Encryption and Audit Logging
- ExtractionError
- sqlalchemy_ext_asyncio
- json
- ADR-010: Triage Fallback Routing (Anti-Spam)
- ADR-012: Telegram and OpenAI for the first complete admissions MVP
- signin
- compilerOptions
- seed_demo.py
- 11. Human-in-the-Loop (Full Workflow)
- Implementation Plan: AdmitFlow
- api.py
- AdmitFlow Backend
- identity_database
- get_sessionmaker
- Official source snapshots
- write_audit_log
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
- encrypt_pii
- whatsapp/__init__.py
- integration/__init__.py
- admitflow-backend
- test_telegram_journey.py
- AdmitFlow
- test_knowledge_workspace.py
- test_payment_contracts.py
- Phase 3: AI Core (Engine + RAG)
- evaluate_faq.py
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
- leads.py
- Quality Gates — Definition of Done
- Phase 6: Production Hardening
- devDependencies
- page.tsx
- dependencies
- hashlib
- .__call__
- AdmitFlow submission requirements
- Language review packet
- One final WhatsApp check with Postman
- staff/payments.py
- review
- timeline
- enqueue_outbound
- payments.tsx
- conftest.py
- react
- api
- test_rag.py
- mock_settings

## God Nodes (most connected - your core abstractions)
1. `get_settings()` - 73 edges
2. `encrypt_pii()` - 69 edges
3. `LeadStatus` - 64 edges
4. `TelegramBot` - 57 edges
5. `write_audit_log()` - 54 edges
6. `Reply` - 52 edges
7. `decrypt_pii()` - 48 edges
8. `Lead` - 46 edges
9. `get_sessionmaker()` - 43 edges
10. `Settings` - 42 edges

## Surprising Connections (you probably didn't know these)
- `Task 42.3: Pluggable Reranker (Cohere API vs Local)` --references--> `search_chunks()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/core/rag.py
- `Task 4: PII encryption utilities and audit log infrastructure` --references--> `write_audit_log()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/db/audit.py
- `Task 17: Wire webhook → TaskIQ → engine dispatcher → WhatsApp` --references--> `handle_turn()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/engine/dispatcher.py
- `Task 8: Engine state definition and lifecycle` --references--> `handle_turn()`  [INFERRED]
  docs/planning/archive/2026-10-23-before-telegram-alignment/tasks/todo.md → backend/src/engine/dispatcher.py
- `Feature status and integration gaps` --references--> `decide()`  [INFERRED]
  docs/event/CURRENT_STATE.md → frontend/app/applications.tsx

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Finalized Production Stack Components** — docs_decisions_adr_007_finalized_stack_finalized_stack, docs_decisions_adr_007_finalized_stack_fly_io, docs_decisions_adr_007_finalized_stack_neon, docs_decisions_adr_007_finalized_stack_redis, docs_decisions_adr_007_finalized_stack_langfuse [EXTRACTED 1.00]
- **handle_turn() Per-Turn Pipeline** — spec_hand_rolled_dispatcher, docs_decisions_adr_008_system_1_decision_layer_decide, docs_decisions_adr_005_three_layer_guardrails_three_layer_guardrails, docs_decisions_adr_004_memory_architecture_episodic_memory, spec_code_owns_the_money [EXTRACTED 1.00]
- **System-1 Decision Engine (decide + primitives + models)** — docs_decisions_adr_008_system_1_decision_layer_system_1_decision_layer, docs_decisions_adr_008_system_1_decision_layer_decide, docs_research_system_1_decision_models_laya_jev_choice, docs_research_system_1_decision_models_laya_jev_score, docs_research_system_1_decision_models_laya_jev_noul, docs_research_system_1_decision_models_laya_jev_laya [EXTRACTED 1.00]
- **AdmitFlow AI Core Architecture** — tasks_plan_conversation_engine, tasks_plan_decide_decision_layer, tasks_plan_three_layer_guardrails, tasks_plan_rag_pipeline [INFERRED 0.85]
- **WhatsApp Ingress → Worker → Engine Flow** — tasks_plan_fastapi_webhook, tasks_plan_redis, tasks_plan_taskiq, tasks_plan_conversation_engine [INFERRED 0.85]

## Communities (134 total, 15 thin omitted)

### Community 0 - "ADR-008: System-1 Decision Layer (Laya / Jev)"
Cohesion: 0.18
Nodes (17): ADR-001: Hybrid Architecture, ADR-004: Dual Memory Architecture, Episodic Memory (messages table), Semantic Memory (lead_facts table), ADR-005: Three-Layer Guardrails and RAG, Three-Layer Guardrails, ADR-007: Finalized Production Stack, ADR-008: System-1 Decision Layer (Laya / Jev) (+9 more)

### Community 1 - "Conversation Engine (hand-rolled dispatcher)"
Cohesion: 0.25
Nodes (8): Conversation Engine (hand-rolled dispatcher), System-1 decide() Decision Layer, FastAPI WhatsApp Webhook, Langfuse LLM Tracing, pgvector RAG Pipeline, Redis (mutex / dedup / rate-limit), TaskIQ Background Worker, Three-Layer Guardrails

### Community 2 - "AdmitFlow Complete Specification"
Cohesion: 0.18
Nodes (10): AI Impact Statement, Student-to-staff demonstration, Prior-work disclosure draft, AdmitFlow necessary resources, Planning baseline before Telegram alignment, AdmitFlow institution knowledge workspace, AdmitFlow Complete Specification, AdmitFlow Platform (+2 more)

### Community 3 - "Finalized Production Stack"
Cohesion: 0.18
Nodes (11): ADR-002: Webhook Concurrency and Deduplication, Per-Phone Redis Mutex, Webhook Deduplication (Redis SETNX), ADR-003: Multi-Tenancy Strategy, Multi-Tenancy (Row-Level Isolation), Finalized Production Stack, Fly.io (Backend + Worker + Scheduler), Langfuse Cloud (LLM Tracing) (+3 more)

### Community 4 - "models/__init__.py"
Cohesion: 0.10
Nodes (52): Base, IdMixin, Declarative base, metadata naming convention, and shared column mixins. Every…, Declarative base shared by every AdmitFlow model., UUID primary key with an application-side default. UUIDs avoid cross-tenant…, Server-side created/updated timestamps., Row-level tenant scoping (ADR-003). Mixed into every tenant-scoped table., TenantMixin (+44 more)

### Community 5 - "guardrails.py"
Cohesion: 0.09
Nodes (34): apply_whatsapp_formatting(), check_input_safety(), check_output_safety(), _deterministic_check(), InputGuardrailResult, LLMGuardrailResponse, LLMOutputGuardrailResponse, OutputGuardrailResult (+26 more)

### Community 6 - "Code Owns the Money"
Cohesion: 0.50
Nodes (5): ADR-006: Code-Owned Qualification and Payments, Intent: Admissions Flow and Discounts, Discount Codes, Code Owns Eligibility, Code Owns the Money

### Community 7 - "journey.py"
Cohesion: 0.13
Nodes (37): Lead, A prospective applicant with optional phone contact and channel identities.…, action(), application_action(), collect_application(), prompt(), Any, AsyncSession (+29 more)

### Community 8 - "RedisMutex"
Cohesion: 0.05
Nodes (36): MutexAcquireError, Redis, RuntimeError, Redis distributed mutex with owner-safe release and keepalive (Task 7). Ensures…, Background loop that extends the TTL while the lock is held., Raised when the mutex cannot be acquired after all retries., Async context-manager mutex backed by Redis ``SET NX``. Parameters: redis: An…, Attempt to acquire the lock, retrying up to ``retry_count`` times. (+28 more)

### Community 9 - "generate_completion"
Cohesion: 0.12
Nodes (22): AllProvidersFailedError, generate_completion(), Any, Exception, Raised when the entire LLM fallback chain is exhausted., Generate a completion with automatic provider fallback. Tries the fast model,…, BaseModel, Triage Node (Task 11). Routes incoming messages to the appropriate downstream… (+14 more)

### Community 10 - "WhatsAppSender"
Cohesion: 0.09
Nodes (23): Any, Send an interactive list message. `sections` is a list of section dicts…, Send a pre-approved template message., Service for sending messages via Meta WhatsApp Cloud API., Post the payload to Meta and extract the created message ID., Meta API expects the phone number without the leading '+'., Send a simple text message. Returns the Meta message ID., Send an interactive message with up to 3 buttons. `buttons` should be a list of… (+15 more)

### Community 11 - "WhatsApp readiness check — October 22, 2026"
Cohesion: 0.06
Nodes (32): ping(), process_inbound_message(), Any, task, Background tasks for message processing. For now this module holds only the…, Smoke-test task: returns ``{"result": payload}``. Enqueued from the…, Process an inbound WhatsApp message (Task 17). This is a placeholder for the…, Tests for the TaskIQ broker setup and task execution (Task 3). All tests run… (+24 more)

### Community 12 - "TelegramBot"
Cohesion: 0.11
Nodes (40): ApplicationStatus, DiscountType, PaymentStatus, Enumerated types used across the schema. These are Python ``str`` enums mapped…, How a discount code reduces the fee., Payment order lifecycle (SPEC §7.10)., Application review status (SPEC §7.9 / lifecycle)., PaymentOrder (+32 more)

### Community 13 - "core/rag.py"
Cohesion: 0.20
Nodes (13): chunk_text(), embed_text(), ingest_document(), Any, AsyncSession, UUID, RAG pipeline core logic (Task 13). Handles ingestion (chunking, embedding),…, Hybrid search (dense + lexical with RRF). (+5 more)

### Community 16 - "get_settings"
Cohesion: 0.12
Nodes (22): AsyncBroker, get_settings(), Application settings singleton. Loads configuration from the environment (and…, Return the process-wide :class:`Settings` singleton., _build_broker(), TaskIQ broker singleton. In production (and local dev with Redis running) the…, Construct the right broker based on the current settings. This is a plain…, main() (+14 more)

### Community 17 - "admissions.tsx"
Cohesion: 0.18
Nodes (8): Admissions(), Detail, Human, Inquiry, labels, Request, RuleEvidence, statusLabel()

### Community 18 - "dispatcher.py"
Cohesion: 0.15
Nodes (17): _flush_engine_state(), handle_turn(), _load_engine_state(), Any, AsyncSession, Engine Dispatcher (Task 8 & 17). This module contains the main entry point for…, Load EngineState from DB records., Flush mutations back to DB records. (+9 more)

### Community 19 - "security.py"
Cohesion: 0.13
Nodes (17): EncryptionKeyNotConfiguredError, _fernet(), RuntimeError, Application-layer PII protection: symmetric encryption + deterministic hashing.…, Raised when a PII helper is used but its key is unset in settings., hash_telegram_identifier(), UUID, Private Telegram identity lookup without storing raw identifiers in indexes. (+9 more)

### Community 20 - "AIBoomi Startup Weekend Kochi: fresh-session context"
Cohesion: 0.11
Nodes (19): AIBoomi Startup Weekend Kochi: fresh-session context, Assessment and next decision, Current readiness session (October 22), Event sources and local copies, Existing prototype rule and surprise element, Existing working-tree changes, Fresh-message prompt, Handoff status (+11 more)

### Community 21 - "RuleOperator"
Cohesion: 0.27
Nodes (13): Qualification-rule comparison operators (SPEC §7.4). Evaluated…, RuleOperator, _coerce_values(), evaluate_rule(), Any, Evaluate a qualification rule deterministically. Args: operator: The…, test_evaluate_rule_in_list(), test_evaluate_rule_missing_extracted_value() (+5 more)

### Community 22 - "test_webhook.py"
Cohesion: 0.11
Nodes (19): parametrize, test_delivery_status_logs_are_authenticated_and_exclude_pii(), test_tunnel_app_exposes_no_other_routes(), test_tunnel_app_keeps_webhook_verification(), app(), client(), mock_settings(), Any (+11 more)

### Community 23 - "get_redis"
Cohesion: 0.13
Nodes (15): get_redis(), Redis, RuntimeError, Shared async Redis client for application code. Carry-over prerequisite #1: the…, Raised when Redis is needed but ``REDIS_URL`` is unset in settings., Return the process-wide async Redis client singleton. The client is created…, RedisNotConfiguredError, post (+7 more)

### Community 24 - "LeadStatus"
Cohesion: 0.12
Nodes (31): LeadStatus, Lead lifecycle states (SPEC §7.3). Where a lead *stands*, not a fixed track —…, AsyncSession, Run the qualification loop., run_qualification(), EngineState, InvalidTransitionError, BaseModel (+23 more)

### Community 25 - "Stages"
Cohesion: 0.13
Nodes (15): 10. Reflect & learn, 1. Understand & spec  (`/spec`), 2. Plan & pick a task  (`/plan`), 3. Branch, 4. Build with TDD  (`/build`, `/test`), 5. Verify (the quality gate), 6. Self-review, then adversarial review  (`/review`), 7. Commit & open the PR (+7 more)

### Community 26 - "knowledge/processing.py"
Cohesion: 0.16
Nodes (15): embed_chunks(), process_upload(), UUID, Durable upload claims, bounded embedding and atomic publication of ready…, Use the configured OpenAI model with the database's explicit 1536 dimensions., Claim once, process outside the transaction, then publish only the current…, main(), Probe (+7 more)

### Community 27 - "collections_abc"
Cohesion: 0.06
Nodes (23): alembic, do_run_migrations(), Alembic migration environment (async). Reads the database URL from application…, Emit SQL to stdout without a live DB connection., Run migrations against a live database via an async engine., run_migrations_offline(), run_migrations_online(), columns() (+15 more)

### Community 28 - "run_postman_check.cjs"
Cohesion: 0.18
Nodes (9): collection, config, crypto, fs, keys, newman, path, root (+1 more)

### Community 29 - "Task List"
Cohesion: 0.17
Nodes (12): Checkpoint: Advanced Features, Checkpoint: AI Core, Checkpoint: Dashboard Complete, Checkpoint: Foundation, Checkpoint: Production Ready, Checkpoint: WhatsApp Ingress, Phase 1: Foundation, Phase 2: WhatsApp Ingress (+4 more)

### Community 30 - "test_rag_node.py"
Cohesion: 0.23
Nodes (11): process_rag_node(), AsyncSession, Retrieve context and answer knowledge questions., mock_state(), asyncio, fixture, patch, Unit tests for the RAG node. (+3 more)

### Community 31 - "test_migrations.py"
Cohesion: 0.21
Nodes (12): alembic_config, _alembic_config(), monkeypatch_session(), pg_url(), fixture, MonkeyPatch, Migration + schema integration tests against real Postgres. Spins up…, Start Postgres, point settings at it, yield the asyncpg URL. (+4 more)

### Community 32 - "Phase 5: Dashboard Frontend (Next.js)"
Cohesion: 0.17
Nodes (12): Phase 5: Dashboard Frontend (Next.js), Task 24: Initialize Next.js + dark mode + glassmorphism, Task 25: Authentication (email + password), Task 26: Dashboard home (funnel analytics), Task 27: Leads CRM page, Task 28: Course & batch management, Task 29: Chat takeover + co-pilot UI, Task 30: Document management (RAG) (+4 more)

### Community 33 - "management.py"
Cohesion: 0.13
Nodes (37): require_admin(), archive_course(), archive_discount(), BatchInput, catalog(), catalog_detail(), course_view(), CourseInput (+29 more)

### Community 34 - "Code Standards"
Cohesion: 0.20
Nodes (10): Async & I/O, Code Standards, Configuration — settings, not literals, Dependencies, Errors, Formatting, Logging & observability, Project layout (+2 more)

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
Cohesion: 0.11
Nodes (21): Code-owned application fees and authenticated Razorpay payment processing., payments(), Any, get, fixture, workspace(), UUID, seed() (+13 more)

### Community 39 - "main.py"
Cohesion: 0.10
Nodes (18): recovery_loop(), create_app(), ready(), lifespan(), FastAPI, FastAPI application entry point. Boots the API, manages the TaskIQ broker…, Start / stop the TaskIQ broker alongside the FastAPI process. The…, Application factory — builds and configures the FastAPI instance. (+10 more)

### Community 40 - "auth.py"
Cohesion: 0.28
Nodes (12): Login, logout(), me(), BaseModel, Db, get, post, Response (+4 more)

### Community 41 - "TelegramClient"
Cohesion: 0.07
Nodes (38): recover_payments(), task, Encrypted outbound-message delivery jobs carry only internal identifiers., send_outbound_message(), normalize_update(), protect_logs(), Any, RuntimeError (+30 more)

### Community 42 - "Hackathon resources for AdmitFlow"
Cohesion: 0.20
Nodes (10): Acceptance before using a resource, Event and release boundaries, Goal, Hackathon resources for AdmitFlow, October 23 Downloads guide: hosted inference access, Participant credits and other support, Suggested allocation and activation order, Useful resources mapped to the plan (+2 more)

### Community 43 - "manifest.json"
Cohesion: 0.20
Nodes (9): SPEC.md, bytes, sha256, tasks/plan.md, bytes, sha256, tasks/todo.md, bytes (+1 more)

### Community 44 - "test_workspace_limits.py"
Cohesion: 0.13
Nodes (15): ASGIApp, Reject oversized multipart streams before they can fill temporary storage., UploadBodyLimit, Custom header + strict cookies prevent cross-origin simple-request CSRF., require_browser_write(), MonkeyPatch, Bound resource use and reject browser cross-origin mutations before database…, test_custom_header_and_origin_required() (+7 more)

### Community 45 - "AdmitFlow: current state and planning baseline"
Cohesion: 0.22
Nodes (9): AdmitFlow: current state and planning baseline, Confirmed user direction, Feature status and integration gaps, Features to finalize next, How to reconcile the planning documents, Proposed architecture for the next plan, Stack inventory, Verification evidence and its limits (+1 more)

### Community 46 - "AdmitFlow: AIBoomi submission plan"
Cohesion: 0.22
Nodes (9): AdmitFlow: AIBoomi submission plan, Deck and presentation, Open decisions, Proposed schedule from Friday evening, Submission outcome, The journey to demonstrate, Use the provided resources, What must be handed in (+1 more)

### Community 47 - "AdmitFlow — Complete Specification"
Cohesion: 0.13
Nodes (15): 12. Edge Cases & Error Handling, 14. Data Privacy (DPDPA-Ready), 15. Memory Architecture, 16. Success Criteria, 17.1 Conversation engine — DECIDED: hand-rolled dispatcher, 17.2 Still open, 17. Decisions & Open Questions, 1. Objective (+7 more)

### Community 48 - "13. Dashboard Features"
Cohesion: 0.22
Nodes (9): 13.1 Authentication, 13.2 Roles & Permissions, 13.3 UI Aesthetic, 13.4 Real-Time Notifications, 13.5 Funnel Analytics, 13.6 Data Export & Integration, 13.7 Document Management (RAG), 13.8 Onboarding (MVP) (+1 more)

### Community 49 - "RazorpayClient"
Cohesion: 0.16
Nodes (14): AsyncBaseTransport, PaymentLink, PaymentProviderError, Exception, field_validator, Read an existing exact reference; absence never authorizes another creation., RazorpayClient, Any (+6 more)

### Community 50 - "ADR-011: Advanced RAG Strategy (Latency vs Precision)"
Cohesion: 0.25
Nodes (7): 1. Complex Document Ingestion (`docling` or `unstructured`), 2. Pluggable Reranking Architecture (Cohere API over Local CPU), 3. Contextual Query Rewriting, ADR-011: Advanced RAG Strategy (Latency vs Precision), Consequences, Context, Decision

### Community 51 - "decide"
Cohesion: 0.20
Nodes (12): LLM calls, Coverage, LLM and decision-layer tests, Philosophy — pragmatic TDD, Running tests, Test layout, Testing, The two patterns (+4 more)

### Community 52 - "Settings"
Cohesion: 0.14
Nodes (23): Core cross-cutting concerns: settings, security, schemas, guardrails, tracing., hash_phone(), Return a deterministic keyed hash of a phone number for lookup/dedup. Keyed…, Environment-backed application configuration., Settings, configured_keys(), fixture, MonkeyPatch (+15 more)

### Community 53 - "AdmitFlow project handoff"
Cohesion: 0.25
Nodes (8): AdmitFlow project handoff, Current direction, Development rules, Event submission, Execution checkpoint, First usable release, Historical evidence, Resume prompt

### Community 54 - "detect_intent"
Cohesion: 0.20
Nodes (15): detect_intent(), Classify the user's intent to route to the correct node. Design Decision: If a…, asyncio, Test routing for course discovery., Test routing for knowledge questions., Test routing for qualification answers., Test routing for human handoff., Test routing for empty messages without calling LLM defaults to discovery. (+7 more)

### Community 55 - "ADR-009: Application-Layer PII Encryption and Audit Logging"
Cohesion: 0.20
Nodes (9): ADR-009: Application-Layer PII Encryption and Audit Logging, Alternatives Considered, Consequences, Context, Decision, Deterministic encryption of the phone number (so it is both stored and searchable), Full envelope encryption (per-tenant data keys wrapped by a master key), Rely on the provider's at-rest encryption only (+1 more)

### Community 56 - "ExtractionError"
Cohesion: 0.24
Nodes (16): extract_file(), ExtractionError, ValueError, Bounded extraction of institution reference documents; never execute uploads., A safe, public error code rather than parser output containing document text., validate_path(), parametrize, Untrusted institutional files must extract safely or fail explicitly. (+8 more)

### Community 57 - "sqlalchemy_ext_asyncio"
Cohesion: 0.14
Nodes (14): Discovery Node (Task 12). Presents available courses as WhatsApp interactive…, ExtractionResponse, BaseModel, Qualification Node (Task 15). Extracts rule fields using the LLM and runs…, Structured output expected from the LLM when extracting fields., RAG Node (Task 14). Graph node that retrieves from the knowledge base and…, RuntimeError, WhatsApp message sending service (Task 6). Uses httpx2 to call the Meta Graph… (+6 more)

### Community 58 - "json"
Cohesion: 0.29
Nodes (4): Five bounded live embedding searches through the real authenticated staff API., Hash the tested code/configuration without reading secrets or runtime data., json, pathlib

### Community 59 - "ADR-010: Triage Fallback Routing (Anti-Spam)"
Cohesion: 0.33
Nodes (5): ADR-010: Triage Fallback Routing (Anti-Spam), Consequences, Context, Decision, Status

### Community 60 - "ADR-012: Telegram and OpenAI for the first complete admissions MVP"
Cohesion: 0.29
Nodes (7): ADR-012: Telegram and OpenAI for the first complete admissions MVP, Consequences, Context, Decision, Implemented runtime boundaries, References and verification, Supersession and preserved decisions

### Community 61 - "signin"
Cohesion: 0.11
Nodes (23): decrypt_bytes(), Authenticate and decrypt source bytes for an authorized ingestion task., Any, Real database management: administrator writes, role/tenant boundaries and…, test_catalog_writes_validate_rules_capacity_and_ownership(), test_discount_management_rejects_invalid_values_duplicates_and_foreign_writes(), test_settings_validate_timezone_hours_and_tenant_scope(), fake_embeddings() (+15 more)

### Community 63 - "compilerOptions"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 64 - "seed_demo.py"
Cohesion: 0.13
Nodes (19): argparse, Dashboard access role (SPEC — admin vs agent)., StaffRole, main(), provision(), Manually provision an institution administrator without printing credentials., main(), Idempotent synthetic institution/catalog/staff seed; no real applicant data. (+11 more)

### Community 65 - "11. Human-in-the-Loop (Full Workflow)"
Cohesion: 0.40
Nodes (5): 11.1 Auto-Escalation Triggers, 11.2 Co-pilot Mode, 11.3 Business Hours, 11.4 Never Escalate, 11. Human-in-the-Loop (Full Workflow)

### Community 66 - "Implementation Plan: AdmitFlow"
Cohesion: 0.40
Nodes (4): Architecture Decisions, Implementation Plan: AdmitFlow, Overview, Risks and Mitigations

### Community 67 - "api.py"
Cohesion: 0.16
Nodes (23): encrypt_bytes(), Encrypt uploaded source bytes before persistence, without lossy text decoding., documents(), get_upload(), Any, BaseModel, Db, delete (+15 more)

### Community 68 - "AdmitFlow Backend"
Cohesion: 0.25
Nodes (8): AdmitFlow Backend, Application payments, Configuration, Current implementation and verification, Institution knowledge workspace, Local development, Stack, Telegram admissions runtime

### Community 69 - "identity_database"
Cohesion: 0.38
Nodes (7): identity_database(), fixture, Use a disposable pgvector database; never mutate the demo database., test_downgrade_preserves_legacy_rows_and_refuses_to_destroy_telegram_data(), inspect_and_clean(), remove_test_bot(), verify_legacy()

### Community 70 - "get_sessionmaker"
Cohesion: 0.10
Nodes (28): async_sessionmaker, AsyncEngine, DatabaseNotConfiguredError, get_engine(), get_session(), get_sessionmaker(), AsyncSession, RuntimeError (+20 more)

### Community 71 - "Official source snapshots"
Cohesion: 0.50
Nodes (4): Conflicts to confirm, October 23 planning refresh, Official source snapshots, Sources

### Community 72 - "write_audit_log"
Cohesion: 0.20
Nodes (13): Any, AsyncSession, UUID, Audit-log write helper. :func:`write_audit_log` is the one path significant…, Append one entry to ``audit_logs`` on ``session``; return it flushed, not…, write_audit_log(), AuditLog, One recorded significant action (state change, payment, deletion, takeover).… (+5 more)

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
Cohesion: 0.18
Nodes (10): Any, asyncio, fixture, patch, sample_whatsapp_payload(), test_handle_turn_basic_flow(), Tests for the Redis distributed mutex (Task 7). The mutex must guarantee: 1.…, Tests for the shared async Redis client helper (carry-over prerequisite #1).… (+2 more)

### Community 84 - "encrypt_pii"
Cohesion: 0.09
Nodes (30): decrypt_pii(), encrypt_pii(), Encrypt a PII string, returning a url-safe base64 Fernet token. Fernet is…, Decrypt a token produced by :func:`encrypt_pii`. Raises…, process_payment(), create_payment_link(), task, Payment-link creation runs after the requesting conversation transaction… (+22 more)

### Community 89 - "test_telegram_journey.py"
Cohesion: 0.11
Nodes (32): Batch, Course, QualificationRule, A program a lead can be qualified for and pay to apply to., A dated intake of a course with finite seats (SPEC §7.5)., A structured eligibility rule evaluated in code, not by the LLM (ADR-006).…, Event, callback_data() (+24 more)

### Community 90 - "AdmitFlow"
Cohesion: 0.33
Nodes (6): AdmitFlow, Current status, Demonstration and submission, Development, Product scope, Stack

### Community 91 - "test_knowledge_workspace.py"
Cohesion: 0.09
Nodes (32): asyncio, ConversationEvent, ConversationReply, OutboundMessage, event_text(), AsyncSession, Human-readable callback summaries without exposing routing or signature details., Institution document extraction, durable ingestion and retrieval. (+24 more)

### Community 92 - "test_payment_contracts.py"
Cohesion: 0.12
Nodes (19): Credentials, BaseModel, Bounded Razorpay requests; ambiguous link creation is never blindly retried., discounted_amount(), Integer monetary arithmetic and exact-byte webhook authentication., verify_webhook(), MonkeyPatch, parametrize (+11 more)

### Community 94 - "Phase 3: AI Core (Engine + RAG)"
Cohesion: 0.18
Nodes (11): Phase 3: AI Core (Engine + RAG), Task 10: Input guardrail node, Task 11: Triage node (intent detection), Task 12: Discovery node, Task 13: RAG pipeline, Task 14: RAG node, Task 15: Qualification node, Task 16: Output guardrail (+3 more)

### Community 95 - "evaluate_faq.py"
Cohesion: 0.29
Nodes (11): Case, cases(), evaluate(), main(), BaseModel, Bounded live FAQ evaluation on the fictional demo tenant; no messages or writes., score_answer(), Evaluation rejects irrelevant quotations and does not count provider errors as… (+3 more)

### Community 96 - "Git & GitHub Workflow"
Cohesion: 0.22
Nodes (9): Branching model — feature branch → PR → `main`, Commits — Conventional Commits, small and coherent, Git & GitHub Workflow, Merging, No AI attribution — the human is the sole author  ⚠️, Pull Requests, Review gate — adversarial, before merge, What never gets committed (+1 more)

### Community 97 - "package.json"
Cohesion: 0.22
Nodes (8): name, private, version, react-dom, @types/node, @types/react, @types/react-dom, typescript

### Community 98 - "log_delivery_status"
Cohesion: 0.50
Nodes (4): log_delivery_status(), Response, Observe only authenticated status events, without recipient or error text., middleware

### Community 99 - "record-demo.mjs"
Cohesion: 0.22
Nodes (7): credentials, headers, journey, target, ref_node_fs, ref_node_path, @playwright/test

### Community 100 - "AGENTS.md"
Cohesion: 0.25
Nodes (7): AIBoomi Startup Weekend handoff, How we build — read the handbook, Knowledge graph, Quick commands (from `backend/`), The rules you cannot skip, What this project is, Workflow triggers

### Community 101 - "Security & Production Readiness"
Cohesion: 0.18
Nodes (11): Dependency & secret scanning, Deploy & rollback, External surfaces, Guardrails & money, Local full-stack (docker-compose), Multi-tenancy — isolation is a correctness bug if wrong, Observability, PII & data protection (DPDPA) (+3 more)

### Community 102 - "AdmitFlow — Task List"
Cohesion: 0.15
Nodes (13): AdmitFlow — Task List, AIBoomi Startup Weekend session handoff (2026-10-22), Current direction and hackathon resources (2026-10-23), Final Postman diagnostic (October 23, executed; delivery blocked), Phase 1: Foundation, Readiness blocker: idle Redis worker restart (in progress), Readiness tunnel setup (in progress), Task 1: Initialize Python project, FastAPI, settings, and Docker (+5 more)

### Community 103 - "next-env.d.ts"
Cohesion: 0.50
Nodes (3): NOTE: This file should not be edited, frontend_next_types_root_params_d, frontend_next_types_routes_d

### Community 104 - "payments/webhook.py"
Cohesion: 0.21
Nodes (13): LinkEntity, LinkEnvelope, PaidEvent, PaidPayload, payment_webhook(), PaymentEntity, PaymentEnvelope, BaseModel (+5 more)

### Community 106 - "layout.tsx"
Cohesion: 0.25
Nodes (5): frontend_app_globals, metadata, config, @fontsource-variable/dm-sans, next

### Community 108 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, lint, record:demo, start, test:e2e:live, typecheck

### Community 109 - "Local Telegram/OpenAI runtime"
Cohesion: 0.33
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

### Community 113 - "leads.py"
Cohesion: 0.35
Nodes (12): course_options(), get_lead(), human_requests(), lead_detail(), leads(), Any, Db, get (+4 more)

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
Cohesion: 0.17
Nodes (9): Applications(), Detail, fields, statuses, Summary, Doc, errors, Match (+1 more)

### Community 118 - "dependencies"
Cohesion: 0.40
Nodes (5): dependencies, @fontsource-variable/dm-sans, next, react, react-dom

### Community 119 - "hashlib"
Cohesion: 0.13
Nodes (15): Expose only the existing Meta webhook through the temporary demo tunnel., Bounded OpenAI-only model roles; provider details never escape in errors., Bounded login throttling; shared Redis when configured, development fallback., get, Response, WhatsApp Webhook routing (Task 5). Handles GET (challenge) and POST (incoming…, Handle Meta's webhook challenge., verify_webhook() (+7 more)

### Community 120 - ".__call__"
Cohesion: 0.33
Nodes (4): private_send(), Receive, Scope, Send

### Community 121 - "AdmitFlow submission requirements"
Cohesion: 0.50
Nodes (4): AdmitFlow submission requirements, Demonstration, Required artifacts, Truthful claims

### Community 122 - "Language review packet"
Cohesion: 0.67
Nodes (3): Current templates, Language review packet, Live exercise

### Community 124 - "staff/payments.py"
Cohesion: 0.53
Nodes (9): locked(), owned(), provider(), Db, post, UUID, Scoped payment monitoring and explicit, read-only provider reconciliation., reconcile() (+1 more)

### Community 125 - "review"
Cohesion: 0.39
Nodes (9): applications(), detail(), owned(), Any, Db, get, post, UUID (+1 more)

### Community 126 - "timeline"
Cohesion: 0.22
Nodes (8): Cursor, Any, AsyncSession, BaseModel, datetime, field_validator, UUID, timeline()

### Community 127 - "enqueue_outbound"
Cohesion: 0.29
Nodes (5): enqueue_outbound(), AsyncSession, Any, test_signed_full_payment_is_atomic_replay_safe_and_amount_checked(), prepare()

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

### Community 132 - "test_rag.py"
Cohesion: 0.50
Nodes (4): Sanitizer to prevent RAG poisoning. Blocks chunks that contain obvious prompt…, sanitize_chunks(), Unit tests for the RAG pipeline., test_sanitize_chunks()

### Community 133 - "mock_settings"
Cohesion: 0.50
Nodes (4): mock_settings(), fixture, MonkeyPatch, Ensure all three models are configured for fallback testing.

## Knowledge Gaps
- **382 isolated node(s):** `admitflow-backend`, `fs`, `path`, `crypto`, `root` (+377 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 899 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `handle_turn()` connect `dispatcher.py` to `normalize_e164`, `models/__init__.py`, `guardrails.py`, `get_sessionmaker`, `journey.py`, `RedisMutex`, `WhatsAppSender`, `WhatsApp readiness check — October 22, 2026`, `pytest`, `AdmitFlow — Complete Specification`, `encrypt_pii`, `Settings`, `detect_intent`, `get_redis`, `LeadStatus`, `Phase 3: AI Core (Engine + RAG)`, `test_rag_node.py`?**
  _High betweenness centrality (0.270) - this node is a cross-community bridge._
- **Why does `17.1 Conversation engine — DECIDED: hand-rolled dispatcher` connect `AdmitFlow — Complete Specification` to `dispatcher.py`, `decide`?**
  _High betweenness centrality (0.235) - this node is a cross-community bridge._
- **Why does `decide()` connect `decide` to `Implementation Plan: AdmitFlow`, `3. Tech Stack & Commands`, `AdmitFlow: current state and planning baseline`, `Phase 3–4 addition (see ADR-008)`, `AdmitFlow — Complete Specification`, `page.tsx`?**
  _High betweenness centrality (0.197) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `encrypt_pii()` (e.g. with `Consequences` and `Decision`) actually correct?**
  _`encrypt_pii()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `LeadStatus` (e.g. with `Lead` and `application_action()`) actually correct?**
  _`LeadStatus` has 39 INFERRED edges - model-reasoned connections that need verification._
- **What connects `admitflow-backend`, `fs`, `path` to the rest of the system?**
  _382 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `models/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10052677787532924 - nodes in this community are weakly interconnected._