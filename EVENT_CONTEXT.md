# AdmitFlow project handoff

## Current direction

**Latest publication override:** The user deleted the first GitHub repository and
created a fresh empty `Shan091/admitflow`, explicitly requesting only newly made
commits in its published history. The verified source tree from local `26f5a3b` was
imported without its ancestors. The replacement repository's PR #1 passed both CI
jobs and was squash-merged as `64105a9`; its tree matches the verified platform source.
PR #2 then passed both CI jobs and was squash-merged as `af9981c`, publishing the staff
controls. Published ancestry starts at fresh root `1ac0ffe`; these commits were all
created during this publication using actual current timestamps. No old Git history was pushed into the replacement. Earlier history
remains on local branches; earlier publication hashes/PR notes below are historical.

**Current budget slice:** Branch `codex/telegram-send-budgets` is based on fresh
`origin/main` after PR #3. Task 22 is implemented with per-institution daily send-attempt
limits, atomic shared Redis reservations, queued deferral, exact provider retry delays,
usage warnings and administrator settings. Zero pauses new claims; raising a cap wakes
budget-deferred work. Confirmed counts use durable DB records, including after a lost
Redis statistics update. The backend gate passes 181 tests/87 strict-typed source files;
44 PostgreSQL cases and two Redis cases pass, with four budget DB cases rerun after the
statistics fix; final delivery cases also cover repeated rate limits and the complete
provider delay measured from rejection. All five browser scenarios pass on the rebuilt/restarted workspace.
Migration `9c5027e2d614` is applied locally; API and worker use current sources, readiness
and authenticated budget reads pass. No new Telegram message was sent for this slice.
Publication uses the separate feature-branch/PR/CI gate; continue Task 21 consent-aware follow-ups and
the full remaining roadmap. Staff controls are already published through merged PR #2.
The Razorpay test account remains a user-side prerequisite; owner/team/submission details
remain deferred. No whole-goal completion claim.

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
