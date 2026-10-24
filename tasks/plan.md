# AdmitFlow implementation plan

This is the active roadmap for the approved Telegram/OpenAI
MVP and subsequent institutional product. Detailed acceptance is in [todo.md](todo.md);
product behavior is in [SPEC.md](../SPEC.md); the decision is
[ADR-012](../docs/decisions/ADR-012-telegram-openai-mvp.md).

## Outcome

A student completes a Telegram inquiry with course/batch choice, grounded answers,
remembered/corrected facts and code-based eligibility. Authorized staff inspect the
persisted inquiry and conversation and manage human requests in a minimal dashboard.

The user authorized updating the current plan/task files after reviewing the approach.
Their exact previous contents are preserved in the
[preserved baseline](../docs/planning/archive/2026-10-23-before-telegram-alignment/README.md).
Existing source, Git history and unrelated edits/deletions remain preserved.

## Current foundation

FastAPI, PostgreSQL models/migrations, Redis/TaskIQ, encryption/audit helpers, rules,
discovery, retrieval and dispatcher modules exist. Telegram identity storage is now
implemented and locally verified. The institution knowledge workspace now has a
staff frontend and API. Telegram transport, durable inbox/outbox, the student journey
and lead/human-request screens are implemented and locally exercised. A real user
confirmed Telegram replies; live OpenAI structured output and embeddings passed.
Source findings and verification limits are in
[CURRENT_STATE.md](../docs/event/CURRENT_STATE.md). Baseline modules are reusable work,
not evidence of a complete admissions journey. Preserve historical task IDs 1-42;
new work uses Tasks 43-60 to avoid rewriting what past IDs meant.

## Necessary stack

Telegram private chat; OpenAI-only inference/embeddings; Python/FastAPI/Pydantic/uv;
PostgreSQL/SQLAlchemy/Alembic/pgvector; Redis/TaskIQ; Next.js/TypeScript with plain CSS
for the initial knowledge workspace. Tailwind remains optional for subsequent screens.
Retain the existing AI wrapper initially. Use long polling for the initial receiver.
Hosting is selected during release planning; no sponsor infrastructure is required.
Basic safe telemetry is required; extra monitoring services remain optional.

## Current execution: institution documents (Tasks 30, 52 and 54)

The user prioritized institution file/folder ingestion within this existing plan.
Accepted formats are digital PDF, DOCX and UTF-8 text (TXT/Markdown/CSV). OCR remains excluded. Task 42.1 now adds offline Docling layout/table parsing
and section-aware chunks for digital PDFs; DOCX preserves headings and table order. Reuse the current RAG tables;
use OpenAI embeddings with the schema's 1536 dimensions. Administrator uploads
authorize the reference material for indexing; extracted text remains untrusted data.

- [x] Implement institution-code/email/password login and tenant-bound staff sessions.
- [x] Build file and nested-folder selection, batch upload and per-document status UI.
- [x] Parse supported files with size/page/archive/text limits and actionable failures.
- [x] Task 42.1: Preserve digital PDF layout/tables and section ancestry; isolate parsing in a bounded child and dedicated worker.
- [x] Persist encrypted originals and recoverable, deduplicated ingestion jobs.
- [x] Publish source-linked chunks atomically; support failed-job retry and deletion.
- [x] Search ready documents by meaning within the authenticated institution.
- [x] Prove PDF/DOCX/text indexing and isolation in disposable PostgreSQL/pgvector.
- [x] Complete the final backend gate, frontend checks and scoped adversarial review.
- [x] Validate live OpenAI embeddings and connect uploaded material to source-quoted Telegram answers.
- [x] Publish the reviewed platform through fresh repository PR #1 with green CI.

Detailed command/results and scope limits belong in [todo.md](todo.md). The document
workspace and student-to-staff implementation have separate acceptance evidence below.

## Current execution: student-to-staff journey

Continue the same task IDs below. Checkboxes here record implementation/validation,
not Git publication or production approval.

- [x] Tasks 44–47: Typed events/replies, signed callbacks, private Telegram transport,
  durable polling checkpoints, serialized inbox processing, reply outbox and OpenAI-only roles.
- [x] Task 48: Seed a fictional institution/catalog/staff account and confirm a real Telegram roundtrip.
- [x] Tasks 49–51: Persist recent history, encrypted facts/corrections, course/batch selection
  and deterministic eligible/ineligible/information-needed/staff-review outcomes.
- [x] Task 52: Index approved references, filter relevance, quote exact passages with sources
  and abstain for unsupported questions. Prove with synthetic PostgreSQL journey tests.
- [x] Task 53 implementation: Validate all replies, bind callbacks, bound model/network
  requests and preserve uncertain delivery. Translate non-ASCII search queries without
  lowering the similarity floor; the five-case live retrieval smoke check passes.
- [x] Tasks 54–57: Authenticate staff, scope lead/history APIs, build inquiry/detail/request
  screens and support acknowledge/resolve/explicit resume with audit evidence.
- [x] Task 58 core checks: Database journey and adversarial cases, real browser workflow,
  live OpenAI calls and user-confirmed Telegram replies.
- [x] Verify the user-sent age corrections, sourced campus answer and unsupported-question
  abstention: four confirmed sends, matching persisted facts/results and staff transcript.
- [x] Complete live `/human` intake and staff controls: confirmed reply, persisted
  request, real-browser acknowledgment/resolution and explicit resume. Resolve and
  opening the resume confirmation both preserve the pause; confirming resume releases it.
- [x] Expand the evaluation to 24 multilingual FAQ cases and add database coverage for
  provider outage, refusal and invalid schemas. Save actual results and a language review packet.
- [x] Restore valid OpenAI credentials and pass the expanded live FAQ evaluation.
  Initial valid-key run: 20/24; passing the translated question to quote selection
  fixes the four non-English failures, with a failing-then-passing database regression.
  The full bounded rerun passes 24/24 without lowering the relevance floor.
- [x] Review the core language templates with the agent, as requested by the user.
  This is an agent assessment of meaning and safety wording, not human/native approval.
- [x] Finish the final gate after all edits and confirm the updated container build.
  Backend: 156 default tests and 16 integration tests; frontend lint/build previously pass.
  Updated image matches all 68 source files and passes the non-root production smoke check.
- [x] Task 59 runtime choice: Use the existing local data services and documented API,
  worker, receiver and frontend commands. No cloud provisioning is necessary for this build.
- [x] Task 60 drafts: Six-slide editable deck, 177-word AI statement and demonstration script.
- [x] Record and inspect the actual 33-second local staff walkthrough; preserve the
  tested code/configuration fingerprint in docs/event/BUILD_MANIFEST.json.
- [x] Record and inspect a 58-second staff view of the saved live student journey,
  including selection, corrections, sourced/unsupported answers and the resumed staff request.
- [ ] Final handset recording, owner/team/license details, organizer/portal verification and submission.
- [x] Publish the existing main baseline and feature checkpoint; open [draft PR #1](https://github.com/Shan091/admitflow/pull/1).
- [x] Verify code publication through PR #12 with adversarial review, both exact-head CI checks green and squash merge (`f532f1c`).

The user has explicitly authorized pushing to Shan091/admitflow. Publish the existing
main baseline and a feature-branch checkpoint, preserving source history. Keep credentials
and runtime data local. The full roadmap remains in progress; publication is not a
claim that all milestones are complete or that this checkpoint is production ready.

Latest override: the user replaced that GitHub repository and requested a fresh commit
history. The verified source snapshot is now on replacement `main` (`64105a9`) after
new PR #1 and green CI, with only new publication commits. Previous Git history is
preserved locally. New work continues on `codex/staff-copilot`; no old ancestry may
be pushed back into this replacement repository.

## Milestone 1: Telegram transport and recoverable processing

Tasks 43-48. Outcome: a real Telegram message is accepted durably, processed by the
existing worker and answered through a validated Telegram sender in the right tenant.

| Order | Task | Depends on |
| --- | --- | --- |
| 1 | 43: Channel identity and tenant/bot mapping migration | Existing schema/security foundation |
| 2 | 44: Typed channel-neutral engine events and reply boundary | 43 |
| 3 | 45: Telegram private-chat receiver, sender and callback acknowledgment | 43, 44 |
| 4 | 46: Durable event intake, scoped dedup/locking and restart recovery | 43, 44, 45 |
| 5 | 47: OpenAI-only configuration, typed contracts and bounded failure handling | Existing provider wrapper; integrates with 44 |
| 6 | 48: Reproducible synthetic catalog, local startup and first live roundtrip | 43-47 |

Exit: prove a real reply, identity stability, duplicate protection and recoverable
intake. No phone-number fabrication, client-controlled tenant selection or public
debug endpoint. No claim that a transport roundtrip finishes admissions integration.

## Milestone 2: Complete student admissions conversation

Tasks 49-53. Outcome: exploration, selection, questions, corrections and grounded
answers operate as one persistent journey.

| Order | Task | Depends on |
| --- | --- | --- |
| 7 | 49: Recent inbound/outbound history, durable facts and correction semantics | 44, 46, 47 |
| 8 | 50: Validated course/batch selection and availability | 45, 48, 49 |
| 9 | 51: State-aware qualification, typed facts and deterministic outcomes | 47, 49, 50 |
| 10 | 52: Approved knowledge ingestion, relevance/abstention and source grounding | 47, 48, 49 |
| 11 | 53: Input/retrieval/output validation, localized prompts and safe sends | 49-52 |

Exit: a synthetic student selects course/batch, answers questions, corrects a fact,
asks a grounded/unsupported FAQ, and resumes correctly after restart. Demonstrate
both passing and failing eligibility without treating eligibility as admission.

## Milestone 3: Staff visibility and human-request workflow

Tasks 54-57. Outcome: authenticated staff can inspect and act on the same inquiry.

| Order | Task | Depends on |
| --- | --- | --- |
| 12 | 54: Staff provisioning, authentication and tenant authorization | 43 |
| 13 | 55: Tenant-scoped lead/detail/conversation and human-request APIs | 49, 51, 54 |
| 14 | 56: Next.js login, leads, detail and human-request queue | 54, 55 |
| 15 | 57: End-to-end human-request acknowledgment, resolution and resume | 51, 53, 55, 56 |

Staff authentication may start alongside Milestone 2 after Task 43. Exit: an authorized
staff member sees the real persisted conversation/result; a second tenant cannot.
Human-request controls operate without promising unconfigured staff replies or SLAs.
Staff-authored Telegram replies and reviewed co-pilot drafts are implemented under
Tasks 20/29; their scoped verification and live-check limits are recorded in todo.md.

## Milestone 4: Verification, reproducibility and event delivery

Tasks 58-60. Outcome: one demonstrable release with trustworthy evidence and submission.

| Order | Task | Depends on |
| --- | --- | --- |
| 16 | 58: Integrated synthetic evaluation, security/failure cases and live evidence | 43-57 |
| 17 | 59: Packaging, runtime choice and deployment readiness if hosting is selected | 48, 53-58 |
| 18 | 60: Final README, demo recording, deck, AI statement and submission | 58; 59 if hosted |

Exit: repository gate and applicable frontend/integration checks pass; no fabricated
claims; final recording/build and judge links are verified. Hosting is optional for
the event, but a working demo and reproducible startup are required. A hosted release
must pass its extra secret, persistence, backup/rollback and real-roundtrip checks.

## Later institutional product milestones

The user has now explicitly authorized execution of every later product milestone.
Continue in this same plan, preserve Telegram/OpenAI and use only necessary services.
Owner/team/license and submission details are deferred until the implementation end.
Human input is required only for credentials, account access or decisions that cannot
be established locally. Git publication is now authorized. Catalog/settings and
applications/review have local evidence; continue payment validation and staff operations.

Payment foundations now include staff monitoring, exact-reference provider lookup and
safe bounded retry. Conversation and standalone sends preserve per-lead ordering in
both directions, and their messages share a cursor-paginated staff transcript. Automated
database/provider/browser checks cover these paths; the real Razorpay test-account
journey remains open. Staff takeover/co-pilot now passes backend, database and browser
checks. A live OpenAI draft was ignored without adding outbound messages; a new
handset-confirmed staff send remains separate. Continue Tasks 21/22 follow-ups and
send budgets, then the remaining institutional milestones. Task 22 is now implemented
and verified: both Telegram outboxes share an atomic daily attempt budget, capped work
stays queued, and staff see usage/reset warnings. Task 22 is published through merged PR #4. Consent-aware follow-ups (Task 21)
now have verified generation, explicit opt-in/out, a two-reminder cap and a running local
scheduler. Task 26 now has a verified Overview with creation-cohort conversions,
observed lifecycle reach and institution-local daily/weekly inquiry charts. Continue
CRM, exports/integrations and the remaining institutional product milestones.

- [x] Tasks 20/29: takeover, pause/resume, reviewed drafts and replay-safe staff-send UI.
- [x] Verify staff behavior against PostgreSQL, live OpenAI and desktop/mobile browser scenarios.
- [x] Publish the staff slice through merged PR #2 with green backend/frontend CI.
- [x] Task 22: daily send budgets, durable deferral, warning/settings UI and Redis concurrency evidence.
- [x] Task 21: explicit follow-up consent, bounded outreach and scheduled recovery; published through PR #5 with green CI.
- [x] Task 26: truthful cohort analytics, transactional stage history, accessible charts and default Overview; database/browser checks pass.
- [x] Task 27: tenant-scoped CRM, all lifecycle filters and private known-name/phone search; database and browser checks pass.
- [x] Task 32 exports: audited CSV/Excel downloads for inquiries, applications and payments; signed transactional webhook delivery and administrator configuration also pass database/browser checks.
- [x] Task 33: authenticated live notifications, durable per-user read receipts and all four event categories; source/database/browser checks pass.
- [x] Institution-managed staff accounts, forced private-password setup and session revocation; PostgreSQL and browser checks pass.
- [x] Explicit full inquiry erasure and separately scoped conversation-history retention; role, tenant, concurrency and financial-preservation checks pass.
- [x] Typed OpenAI decisions and required bounded passage reranking; no model training. Unit/database checks and live 4/4 ranking plus 24/24 FAQ checks pass.
- [x] Task 38: isolated full-stack Compose build/start, real proxy/WebSocket/queue/scheduler checks and credential-preserving restart pass; receiver polling is an explicit profile.
- [x] Task 42.2: bounded contextual OpenAI query resolution, uncertainty clarification, course-scoped references and matching database fee lookup; unit/database/browser and live evaluations pass.
- [x] Confirm an explicitly authorized staff reply on the Telegram handset; user confirmed receipt and automation resumed.
- [x] Confirm the uploaded synthetic PDF produces a Lotus Hall answer on the Telegram handset.
- [x] Task 29.1: show grounded student answers without source footers, retaining internal evidence and staff search sources; backend/database/live-provider checks pass.

| Phase | Retained work and historical IDs |
| --- | --- |
| Applications and payments | 18 form collection; 19 Razorpay/discounts/signed payment events; 31 review queue |
| Staff-assisted operations | 20 and 29 direct takeover/co-pilot; 21 consent-aware follow-ups |
| Institution administration | 28 course/batch/rule CRUD; 30 reviewed document uploads; 34 settings/business hours |
| Reporting and integrations | 26 analytics; 32 export/outbound webhooks; 33 notifications |
| Reliability and operations | 22 channel-specific rate/send queue; 23 optional Langfuse; 35 optional Sentry; 36 deletion; 37 retention; 38 full Compose; 39 production topology |
| Evidence-driven AI improvements | 40 typed OpenAI decisions (implemented); 42.3 required OpenAI reranking (implemented); 42.2 contextual resolution/course scopes (implemented); 42.1 offline layout/table parsing and semantic chunks (implemented) |

Security, auditability, tenant isolation and safe handling remain requirements of the
first milestone that touches them. Real applicant pilots additionally require verified
deletion/retention, access/privacy and operational readiness. Optional vendor work does
not block synthetic event delivery. The full roadmap is not promised within the event.

## Submission materials and owner review

- [x] User walkthrough completed; the user reported everything tested worked.
- [x] Owner shan recorded and MIT selected from the handbook's permitted examples; root LICENSE and third-party provenance are present.
- [x] Six-slide editable PowerPoint with actual synthetic-data screens, speaker notes and visual/package QA.
- [x] Refresh README, AI statement under 200 words, prior-work disclosure and demonstration script.
- [ ] Record the final working-build demonstration and verify public judge access.
- [ ] Obtain current portal details and organizer prior-work acceptance, then submit.

Public deployment is deferred until the user explicitly instructs it. The actual
Razorpay provider/card/webhook/Telegram journey remains open pending test credentials.
The existing plan remains authoritative; these items complete its submission slice.

## Delivery rules

Build/test the smallest vertical task; keep IDs and dependencies visible. Domain/risk
logic is test-first. Preserve source/evidence; do not convert old mocked-test checkboxes
into Telegram completion. Each completed implementation task records build/commit,
commands, actual outcomes, limitations and review, then follows the repository PR gate.
Never tick a task because a document, model/table or function merely exists.

## Risks and unresolved inputs

The main risks are the phone-based legacy schema, inconsistent memory, unconnected
output checks, weak relevance gating, external delivery uncertainty and missing staff
authorization. Tasks 43-58 address them explicitly. Verify model access, language
quality and actual startup instead of assuming them. Keep provider calls bounded and
synthetic; activation/billing/hosting changes require their own concrete setup decision.

Organizer confirmation is still needed for prior-work permission, submission portal,
surprise requirement and any deadline changes. Verify the actual deadline from original event sources and upload with a buffer.
Execution checks are in [PREPARATION_PLAN.md](../docs/event/PREPARATION_PLAN.md).


## Task 61: Adaptive, student-first course guidance

- [x] Document primary-source research, psychometric limits and conversation decisions.
- [x] Replace the menu-first discovery loop with an English adaptive conversation over
  explicit interests/background/goals and a provisional, correctable student profile.
- [x] Offer optional deeper exploration; use text questions and contextual choices.
- [x] Match verified institution courses, enforce eligibility/availability in code and
  explain fit; acknowledge unavailable interests without enrollment pressure.
- [x] Preserve direct course choice, FAQs, human help, consent and application/payment controls.
- [x] Verify unit/adversarial, real database and bounded live OpenAI student scenarios;
  adversarial review and final local checks pass; update this checklist.
- [x] Publish through the protected-main PR/CI gate ([PR #15](https://github.com/Shan091/admitflow/pull/15)).

## Task 62: Natural admissions conversation and responsive Telegram delivery

- [x] Reuse explicitly provided application details; collect missing details naturally
  after a confirmed course/intake, with explicit review before submission.
- [x] Shorten repeated copy; handle greetings, questions, pauses and corrections during collection.
- [x] Add a confirmed `/reset` that clears conversational context/drafts without deleting
  submitted applications, payments, consent preferences or staff ownership.
- [x] Show best-effort typing during processing; eliminate redundant model calls and
  transcript queries, and measure response latency without sending test messages.
- [x] Verify regressions, database boundaries, provider scenarios and quality gate;
  document limits in ADR-014 and the conversation release evidence.
- [ ] Publish through the reviewed protected-main PR/CI gate.
