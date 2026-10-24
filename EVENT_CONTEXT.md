# AdmitFlow project handoff

## Current direction

**User review first:** The user wants to see and personally test the app before
owner/team/license or submission packaging work continues. The native app is running
at http://127.0.0.1:3000, with API on 8000 and the dedicated knowledge worker active.
Use the existing private backend/.demo-credentials.json for login; never paste its
password or provider keys into chat. A browser-panel open was queued for this chat.
Keep submission details deferred while the user tests. Record and fix their findings.


**Current structured-document slice:** `codex/document-structure` continues from
merged PR #11 (`b120461`). Task 42.1 now uses offline CPU Docling layout/table parsing
for digital PDFs, heading-aware chunks and ordered DOCX blocks. Parsing runs in a
bounded child process and a separate serial TaskIQ knowledge worker, so folder jobs
do not occupy the Telegram worker. OCR and fine-tuning remain excluded; OpenAI owns
decisions, embeddings and required reranking.

The backend gate passes 251 default tests/117 strictly typed source files. Full
PostgreSQL passes 87 tests, including real complex-PDF upload and atomic publication;
two actual Redis tests pass separately. Frontend lint/build pass. The live native
PDF -> dedicated Redis worker -> Docling -> OpenAI -> source-search check passes all
four checks and removes its own temporary synthetic upload. No Telegram message was
sent. Windows process-tree termination was confirmed against real child processes.
The final Linux nonroot image passes the bounded parser with networking disabled;
nine current Compose checks pass, including both real worker queues. The preceding
stop/start check also confirmed credential persistence. PR #12 is open; CI found a
Linux typing issue in a Windows-only process flag, fixed with an explicit platform
guard. The corrected final local gate passes again (including explicit Linux typing).
CI rerun and exact-head merge remain before publication. Native API runs as PID 3552
and the dedicated knowledge worker as main PID 17580; recheck process identity before
restarting. Existing common worker/receiver/scheduler and data remain intact.

See docs/engineering/DOCUMENT_INGESTION.md and
[document results](docs/event/DOCUMENT_PIPELINE_RESULTS.json). Next: finish the
PR gate, then the active completion audit. Actual Razorpay test credentials,
explicit handset checks, production hosting (deferred by user), and final event
owner/team/license/portal/recording details remain unverified. Earlier slices below
are historical evidence, not instructions to rebuild completed Tasks 42.1/42.2.


**Current contextual-retrieval slice:** Task 42.2 is implemented on
`codex/contextual-retrieval`, after full-stack runtime PR #10 merged as `0d5b122`.
Bounded OpenAI reference resolution asks for clarification when uncertain, preserves
numeric values across supported formats and never changes authoritative course IDs.
Document metadata scopes are tenant/admin controlled and applied before ranking.
Explicit catalog names override a selected course for lookup only. A failing
cross-course application-fee regression was fixed so the matching database row
supplies the amount. Duplicate active course names now require a matching explicit
selection or clarification, with a failing-then-passing database regression.
Adversarial review covered tenant/admin/CSRF authority, metadata joins, numeric
fidelity, duplicate/overlapping catalog names and quotation source identity; no
open critical/important finding remains. Staff scope/search controls pass desktop/mobile checks and
failure recovery; no live document scope was changed.

The gate passes 240 tests/113 source files; full PostgreSQL passes 86 tests plus two
actual Redis cases, and all twelve browser scenarios pass. Live resolution improved
from 7/8 to 8/8 after clarifying the singular-reference rule; 24/24 source/abstention
cases pass again. Native API/worker/frontend run this source; the container stack also builds/starts with the same code. No Telegram message was sent. Continue Task 42.1
complex digital-document structure and semantic chunking before final release checks.


**Current local-runtime slice:** `codex/full-stack-runtime` implements Task 38 after
PR #9 was squash-merged as `d4971d1`. The root Compose stack has its own synthetic
PostgreSQL/Redis/credential volumes and loopback ports 13000/18000; the existing native
runtime and bot checkpoint are preserved. Migration/seed dependency ordering, API,
worker, scheduler and standalone nonroot frontend build/start successfully. All nine
live smoke/restart checks pass, including actual authenticated proxy/WebSocket,
Redis/TaskIQ result and credential persistence. See `docs/event/COMPOSE_RESULTS.json`
and `docs/engineering/COMPOSE_RUNTIME.md`. The backend gate passes 234 tests/111 source
files; all nine affected PostgreSQL journey/account cases pass. The receiver image CLI
and profile validate; no second live poller or provider calls were started. Legacy
WhatsApp ingress and preexisting jobs are disabled by default; nondev debug is forced off.

Adversarial review checked private config creation, image/build-context secret exclusion,
nonroot volume ownership, seed/restart preservation, startup ordering, shared image
reuse and authenticated proxy/WebSocket paths. The initial duplicate-image export
race was fixed by building one shared backend image. No open critical/important
findings remain for this group.

The user says to finish remaining build tasks before choosing production hosting.
Tasks 42.1/42.2 are now implemented; use the latest slice above for remaining checks. Actual payment-account and handset-only checks, event identity/
license/portal confirmation and public hosting remain separately unverified.


Adversarial review checked tenant scope, session/setup bypasses, last-admin races,
provider claims versus deletion, financial retention boundaries, source-ID forgery
and ranking timeout/refusal fallback. No unresolved critical/important findings
remain for this group. Nested generated graph output is retained locally and ignored.

**Current staff/privacy and OpenAI slice:** Tasks 25/34/36/37 and 40/42.3 have
implementation and verification evidence on `codex/institution-access-and-privacy`.
Administrator-managed staff accounts require private password setup; role/reset/
deactivation revokes sessions. Explicit inquiry erasure is separate from automatic
conversation-history retention, which preserves profiles, forms and financial records.
Migration `c4817a02f59d` is applied locally. Source checks pass 231 default tests and
strict typing across 110 files. The preceding staff/privacy group passed 84 PostgreSQL
plus two Redis cases; after the OpenAI changes, all ten affected PostgreSQL document/
journey cases pass. The final three account/privacy/staff-control browser cases pass;
the full eleven-scenario frontend suite and lint/build passed during this group.

The user selected OpenAI itself for the decision layer, removed Task 41 model training,
and required reranking now. Typed interpretation/extraction uses `decide()`;
code retains eligibility, readiness state and consequential business decisions.
OpenAI reranks at most twelve approved tenant passages with an eight-second additional
timeout and safe baseline fallback. Live synthetic checks pass 4/4 ranking cases
and 24/24 FAQ source/abstention cases, without sends or database writes. The current
API, worker and scheduler run this source; all five authenticated live retrieval
checks pass after restart. See
`docs/event/RERANKING_RESULTS.json` and `EVALUATION_RESULTS.json`.


**Published integration/notification slice:** PR #8 passed CI and was squash-merged as `2b3dd6e`. The primary agent completed Tasks 32/33.
Minimal events/outbox rows commit with source actions; encrypted per-tenant webhook
configuration, rotating signatures, public-IP-pinned HTTPS, stable deduplication IDs,
recoverable leases, six-attempt backoff and dead/cancelled monitoring are implemented.
The socket uses real staff sessions, origin checks, repeated expiry/account validation,
per-user receipts and unread-first paging. Both Telegram senders/recovery emit attention
events; read audit actions cannot cause an event loop. The group gate passes 220 default
tests/105 source files, 75 PostgreSQL plus two Redis cases across full/focused runs,
frontend lint/build and all nine browser scenarios. The actual same-origin socket received
a synthetic committed eligibility event; that temporary inquiry was removed. Desktop/mobile
QA completed in two rounds. Migration `6dd017583606` is applied; API, worker (including
`src.tasks.integrations`), scheduler and frontend run current source. No real external
webhook is configured and no Telegram message was sent for this group. The full roadmap
remains open: continue staff administration, deletion/retention and operational milestones.

**Published CRM/export slice:** PR #7 passed both CI checks and was squash-merged as `009933e`.
 The primary agent owns all remaining tasks; the user
requested faster grouped execution without delegation. Task 27 now provides all twelve
status filters, private Unicode known-name prefix/exact international phone lookup,
transactional blind indexes and legacy-name backfill. Task 32 CSV/Excel downloads
are administrator-only, tenant-scoped, audited, formula-safe and explicitly bounded.
Migration `a82df107e436` is applied locally and both saved inquiries were reindexed.
Actual authenticated downloads returned two inquiries, one application and no payments.
The gate passes 200 default tests/97 source files; 69 PostgreSQL and two Redis cases
pass, including reversible migration, index changes and pagination. Frontend lint/build,
staff-controls regression and new CRM/download browser checks pass. Outbound webhooks,
notifications and all remaining milestones are still open. No Telegram message was sent
for these checks. API/worker/frontend use the updated source; receiver/scheduler remain
running. Publication will follow the same green-CI reviewed-PR gate.

**Latest publication override:** The user deleted the first GitHub repository and
created a fresh empty `Shan091/admitflow`, explicitly requesting only newly made
commits in its published history. The verified source tree from local `26f5a3b` was
imported without its ancestors. The replacement repository's PR #1 passed both CI
jobs and was squash-merged as `64105a9`; its tree matches the verified platform source.
PR #2 then passed both CI jobs and was squash-merged as `af9981c`, publishing the staff
controls. Published ancestry starts at fresh root `1ac0ffe`; these commits were all
created during this publication using actual current timestamps. No old Git history was pushed into the replacement. Earlier history
remains on local branches; earlier publication hashes/PR notes below are historical.

**Published follow-up slice:** Task 22 is published through merged PR #4 (`ff35eba`),
and Task 21 through merged PR #5 (`91f4370`): student opt-in through /followups,
/stop even during staff takeover, source freshness/cancellation, office hours, recoverable
generation leases and at most two delivery opportunities. Unsafe/unavailable generation
uses reviewed neutral copy; a separate typed OpenAI safety check guards generated text.
The group gate passes 186 default tests, strict typing over 92 source files and 62
PostgreSQL/Redis integration cases. Live generation/safety checks pass in all four
languages (8 successful structured calls, no Telegram reminder sent). A focused rollback
regression was reproduced/fixed: queued reminders cannot remain executable after removal
of consent fields; in-flight requests remain uncertain. Migration `e31b0847c629` is applied
locally, existing inquiries remain opted out, API/worker were restarted, the one-shot
scheduler queued zero jobs and its continuous producer is running. Authenticated saved
inquiry reads and readiness pass. Both backend and frontend CI passed before the squash merge.

**Published reporting slice:** Task 26 passed both CI checks and was squash-merged through PR #6 as `ab516b1`.
The default Overview shows tenant-scoped creation-cohort conversions, observed stage
reach/current state counts and local daily/weekly inquiry charts. Real ORM status
transitions are audited atomically; older stage history is not invented. All aggregates
share a repeatable-read snapshot. The group gate passes 193 default tests/93 source
files, 65 PostgreSQL cases plus two Redis cases, frontend lint/build and all six browser
scenarios. Desktop/mobile layout and two bounded visual passes are complete; the legacy
table minimum width is overridden only for analytics. Live authenticated metrics for
the saved demo data have consistent totals (two inquiries, one applicant); readiness
passes. API/worker/frontend have been restarted on current sources. No Telegram message
or historical backfill was used. Publication follows its own PR/CI gate. Continue CRM,
exports/integrations, privacy/retention and the rest of the existing roadmap.

The user now assigns all remaining tasks to the primary agent and requests faster grouped
execution; the earlier analytics handoff proposal is withdrawn. Continue the full existing roadmap after the reporting slice. Do not repeat unchanged full checks: use focused tests
during work and one full applicable gate when a feature group is ready. The Razorpay test
account and final owner/team/submission details remain deferred user-side prerequisites.
No whole-goal completion claim.

Execute the existing [implementation plan](tasks/plan.md) and track verified work in
[tasks/todo.md](tasks/todo.md). Use [SPEC.md](SPEC.md) and
[ADR-012](docs/decisions/ADR-012-telegram-openai-mvp.md) for product/architecture decisions.
Do not create another roadmap. Calendar-free project documentation describes milestones;
Git, archived source snapshots and verification records preserve actual provenance.

Telegram is the active student channel. OpenAI is the AI provider. Use only necessary
resources; Neysa, SerpAPI and additional model providers are not prerequisites.
Continue in this repository with existing source/history. Preserve unrelated edits and
deletions. Keep durable context in the repository and secrets only in ignored local config.

## First usable release

Telegram onboarding, language preference, course/batch selection, context-aware
qualification, persistent memory/corrections, grounded institution FAQs and staff
login/lead detail/conversation/human-request queue. Python owns eligibility, prices,
tenant authorization and consequential state changes.

Applications/review, Razorpay, co-pilot, follow-ups, broad management screens,
analytics/exports and production operations remain later milestones in the same plan.
The roadmap is not a claim that all features are implemented or event-deliverable.

## Execution checkpoint

Tasks 43–57 and the core local acceptance for Tasks 58–59 are implemented and
verified; Task 60 has local draft assets and a staff recording. Telegram live selection,
corrections, grounded/unsupported answers and staff-request controls passed. See the
latest evidence below and tasks/todo.md rather than interpreting the starting audit
as the current state. Git publication is now authorized; PR/CI/merge remain release gates.

The existing backend includes FastAPI, SQLAlchemy/Alembic, pgvector, TaskIQ/Redis,
qualification/retrieval/guardrail modules and a WhatsApp-oriented dispatcher.
[CURRENT_STATE.md](docs/event/CURRENT_STATE.md) records the starting source findings;
new execution evidence in tasks/todo.md takes precedence over that audit. The code
knowledge graph has been updated successfully; historical missing-CLI notes are stale.

## Historical evidence

[READINESS_CHECK.md](docs/event/READINESS_CHECK.md) and
[POSTMAN_CHECK.md](docs/event/POSTMAN_CHECK.md) preserve prior commands/results.
The recorded default gate passed 114 tests with integration exclusions and existing
RAG AsyncMock warnings. That result does not establish the current edited build.
Meta accepted requests but then rejected delivery with 131031. Do not repeat failed
WhatsApp sends while restricted or claim a successful handset journey.

The [preserved baseline](docs/planning/archive/2026-10-23-before-telegram-alignment/README.md)
contains prior specs/plans and event context. Do not reinterpret old test checkboxes
as proof that Telegram or a complete admissions workflow works.

## Event submission

Use [SUBMISSION_PLAN.md](docs/event/SUBMISSION_PLAN.md) for required artifacts,
[PREPARATION_PLAN.md](docs/event/PREPARATION_PLAN.md) for execution checks and
[SOURCES.md](docs/event/SOURCES.md) for original event rules and schedule provenance.
The portal, prototype permission, surprise requirement and any updated event rules
remain external inputs. Disclose prior work and event-built changes honestly.

## Development rules

Read [AGENTS.md](AGENTS.md) and the [development lifecycle](docs/engineering/development-lifecycle.md).
Current work is on feat/engine-dispatcher; preserve the working tree. Never commit to
main. Use branch/PR/squash merge, no attribution trailers, pragmatic TDD, the backend
quality gate and relevant integration checks. No task is complete merely because
source code or a planning document exists. Record evidence before ticking acceptance.

The institution document workspace is implemented and locally verified: staff login,
PDF/DOCX/text file/folder uploads, durable indexing/status/retry/delete and source-linked
search. See current execution in tasks/todo.md for the gate, pgvector and browser
evidence. Telegram private transport, durable processing/replies, encrypted memory,
course/batch selection, code-owned eligibility and the staff inquiry/request workflow
are implemented. OpenAI live structured output, 1536-dimensional embeddings and
real staff document indexing/search pass. The user confirmed receiving replies from
the configured bot; the persisted live inquiry has both required eligibility fields.
The replacement token was verified after the user revoked the token exposed by the
HTTP client's original local INFO logging. Redaction is tested and enabled.

The five-case live retrieval smoke check passes English, Hindi, Hinglish, Malayalam
and unsupported abstention after query translation. This does not establish fluency.
The user-sent age corrections (17 then 21), sourced campus answer and unsupported
moon-question abstention are persisted, confirmed sent and visible through the staff
API. Eleven inbound events and eleven replies are saved: ten sent, one earlier uncertain.
The local processes stopped during an interruption and were restarted without data
loss. The resent `/human` produced a confirmed reply and persisted request. Real Chrome
staff controls passed acknowledgment, resolution with pause retained, and explicit
confirmed resume to qualifying. All four request actions have audit records; one
resumed request remains saved. Automation continues on the next student message.
The backend gate, database and browser evidence
is in tasks/todo.md; startup and recovery are in docs/engineering/LOCAL_RUNTIME.md.
Final verification passes 156 default tests and 16 integration tests, prior frontend lint/build,
and the updated image's source-match/non-root production smoke checks. The actual
33-second local staff walkthrough is saved in docs/event/artifacts/staff-walkthrough.webm.
The tested source/configuration is fingerprinted in docs/event/BUILD_MANIFEST.json.
The additional 58-second student-to-staff-walkthrough.webm records the actual staff
view of the saved live journey. The language-review packet and prior-work disclosure
draft are in docs/event/. The expanded 24-case FAQ evaluator is implemented and tested,
but its live run failed authentication: the current OpenAI key returns 401 invalid_api_key.
The user was asked to save a replacement key locally. Do not repeat calls until then,
and do not describe prior successful validation as current credential readiness.
Questions about full-roadmap scope, owner/team/license, portal/prior-work confirmation
and fluent reviewers were answered: execute every later milestone; defer owner/team,
license and submission details until the end; use agent language review and ask humans
only when necessary. A valid replacement OpenAI key is saved and live probes pass.
After a regression-backed translated-question fix, the expanded FAQ run passes 24/24.
Do not treat the earlier credential failure as the latest state. Current slice: catalog
and settings APIs pass three scoped management/translation database checks; the new
management frontend builds, with real-browser verification/full final gate still pending.
No subsequent all-roadmap completion is claimed by this checkpoint.
The event deck, AI statement and demonstration script are drafts; final owner/team,
license, portal and public-link details remain open. The user explicitly
previously requested no Git push; the latest explicit authorization supersedes that hold.

## Resume prompt

Latest override: the user explicitly authorized pushing to the new Shan091/admitflow
repository. Existing main history (`96b5c75`) and feature checkpoint (`a4212cb`) are
published. [Draft PR #1](https://github.com/Shan091/admitflow/pull/1) is open from
`codex/telegram-admissions-checkpoint`; CI and review/merge remain separate gates.
The current backend gate passes 163 tests and strict typing across 83 source files;
frontend lint and production build pass. The database integration run passes 32 tests;
the Redis-only case passes separately, for all 33 integration cases verified.
The full roadmap remains in progress, including real payment-provider validation and
staff/product operations. Publication does not establish full-roadmap completion.

Latest direction: implement every later product milestone. Catalog/settings/discount
management and application collection/review are now implemented with scoped database
and browser evidence in tasks/todo.md. New migration d82c0a75b912 adds encrypted form
payloads. The local database is now at f129a064c5e8, including durable payment/outbound
storage, without deleting existing rows. API/worker/receiver/frontend were restarted;
health/readiness and the real staff upload/search/saved-conversation browser check pass.
The user has also authorized Git publication to the new Shan091/admitflow repository;
this supersedes all earlier no-push notes above. Git Credential Manager provides API
access without exposing or persisting its token. Publish the existing main baseline,
then the checked feature branch and a draft PR. Test-local login-throttle isolation
retains enforcement within each case. Payment creation, fee confirmation, signed
webhooks and durable outbound delivery have automated tests. Staff monitoring,
read-only reconciliation, safe bounded retry, bidirectional send ordering and unified
cursor-paginated transcript now have database and browser evidence. No lookup alone
marks an invoice paid. The user needs to create a Razorpay test account before live
test-card/webhook validation. Next: staff takeover/co-pilot and the remaining roadmap.
Never publish local secrets; do not mark the whole goal complete at this checkpoint.

Read AGENTS.md, this handoff, SPEC.md, tasks/plan.md and tasks/todo.md. Execute the
current task, preserve existing changes, use Telegram and OpenAI, and report actual
verification. Do not start another planning cycle or assume live readiness.
