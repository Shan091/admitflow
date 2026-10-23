# AdmitFlow — Task List

## Current execution: Telegram and OpenAI

Execute [plan.md](plan.md) and [SPEC.md](../SPEC.md). Use this task list for progress;
there is no parallel roadmap. Prior task IDs and historical results below remain
baseline evidence, not Telegram end-to-end acceptance. Original dated records are
preserved in the [baseline archive](../docs/planning/archive/2026-10-23-before-telegram-alignment/README.md).

### Active work ownership

The user has assigned **all remaining tasks to the primary agent**. The previous
proposal to reserve Task 26 for another agent is superseded; nothing is waiting for
an external analytics handoff. Tasks 22 and 21 were published through merged PRs #4 and #5. Continue Task 26
analytics/reporting and the rest of this existing roadmap.
Group related implementation work, use focused tests during development, and run the
full applicable gate once each feature group is ready. Keep the repository's review,
privacy, tenant-isolation and release requirements intact.

### Task 43: Telegram identity and trusted bot-to-institution mapping

**Status:** Published in the fresh repository through merged PR #1; verification below records the original task evidence.
**Dependencies:** Existing schema, encryption and audit foundation.

- [x] Add institution-owned Telegram bots and encrypted student routing fields.
- [x] Permit institution/lead creation without fabricated WhatsApp contacts.
- [x] Enforce same-tenant bot/lead identity links and scoped unique user/chat lookups.
- [x] Add domain-separated keyed lookup hashes with private-chat identifier validation.
- [x] Add a migration preserving existing rows and refusing destructive identity downgrade.
- [x] Prove migration up/down, legacy preservation and cross-tenant/duplicate rejection in real PostgreSQL.
- [x] Pass the full backend gate and complete an adversarial review of the scoped changes.
- [x] Commit, PR, CI and merge under the repository workflow (fresh repository PR #1).

**Verification:** Test-first regression failed because TelegramBot/TelegramIdentity
were absent. Focused identity/schema checks passed 16 tests. A first real-database
run exposed duplicate generated constraint names; explicit names fixed the migration.
`pytest -m integration tests/integration/test_telegram_identity.py -q --tb=short`
then passed 2 tests against disposable pgvector PostgreSQL, including rollback safety.
`bash backend/scripts/verify.sh` passed lint, formatting and strict mypy, with
123 tests passed, 7 integration tests deselected and 2 existing RAG AsyncMock warnings.
Live .env was temporarily isolated and restored for the default gate; no secrets
were printed and no paid model/Telegram call was made. Scoped review checked composite
ownership FKs, keyed lookup separation, nullable contact pairing and downgrade data
preservation; no open important/critical finding. `graphify update .` succeeded with
code extraction only; source/paper semantic enrichment was not requested.
These checks do not establish a live Telegram journey. Next implementation task: 44.

### Current execution: institution document workspace (Tasks 30, 52 and 54)

**Status:** Implemented and locally verified; live-provider/bot and selected live journey checks passed. Agent language review is recorded. Publication is now authorized;
PR/CI/merge remain separate release gates. No new roadmap replaces this file.

- [x] Manually provision institution administrators; verify salted passwords and expiring sessions.
- [x] Enforce administrator writes, staff reads and session-derived institution scope.
- [x] Upload multiple files or a nested folder with preserved relative source paths.
- [x] Extract digital PDF, DOCX and UTF-8 TXT/Markdown/CSV; report OCR-required PDFs explicitly.
- [x] Bound file/batch/page/archive/text sizes; reject unsafe paths and unsupported files.
- [x] Encrypt original bytes, deduplicate per institution and retain durable queued jobs.
- [x] Index through TaskIQ with atomic claims/publication, retry and expired-lease recovery.
- [x] Show queued/indexing/ready/failed states and source passages in the staff UI.
- [x] Search ready material in pgvector with a similarity floor and suspicious-chunk exclusion.
- [x] Delete original uploads and their indexed chunks; prevent publication after deletion.
- [x] Verify extraction/passwords, request limits, account-rotation throttling and invalid vectors.
- [x] Verify real PostgreSQL upload/index/search, duplicate deliveries, provider failure/retry,
  tenant isolation, agent permissions, session expiry and safe migration up/down.
- [x] Pass the final backend gate and frontend typecheck/build; complete adversarial review.
- [x] Confirm mobile/desktop behavior after the responsive fix.
- [x] Validate live OpenAI requests and the Telegram answer path separately; see current evidence below.
- [x] Publish through the authorized PR/CI workflow (fresh repository PR #1).

**Verification:** Test-first extraction/password imports initially failed; 16 focused tests
now pass. Regression tests first exposed account-rotation bypass and a missing API-key
argument; the 5 workspace security/configuration checks now pass. The complete
`bash backend/scripts/verify.sh` passes lint/format/strict mypy and **144 tests**, with
11 integration tests deselected and 2 pre-existing RAG AsyncMock warnings. Local live
configuration was temporarily isolated and restored without printing credentials.

`uv run pytest -m integration tests/integration/test_knowledge_workspace.py --tb=short`
passes **4 tests** against disposable PostgreSQL/pgvector with synthetic embedding
responses. Coverage includes three formats, tenant/role isolation, source encryption,
CSRF/origin checks, actual vector queries, duplicate uploads/deliveries/claims,
queue/provider failure, retry, deletion during indexing, expired-lease recovery,
session expiry and upgrade/downgrade safety. No demo database was changed.

`npm run typecheck` and `npm run build` pass. Browser fixture checks pass login,
upload, source-passage search, confirmation/deletion and logout; desktop (1440 px)
and mobile (390 px) have no page overflow after the hidden-element fix. These UI
checks use synthetic API responses, separately from the real API/database tests.
The Impeccable detector reports no findings. Fonts are bundled locally. Scoped
adversarial review addressed login rotation, dotenv-to-provider key propagation,
source-blob loading, long paths and worker/delete locking; no open important/critical
finding within this slice. `graphify update .` completed using code extraction only.

These results do not establish a paid OpenAI request, calibrated multilingual relevance,
a grounded Telegram answer, production deployment or PR/CI/merge. Setup, limits,
roles, encryption/storage behavior and operational recovery are in backend/README.md.

### Current execution: Telegram/OpenAI student-to-staff implementation

The entries below track implemented acceptance separately from shipping. Git publication
is authorized; the verified platform was published through fresh repository PR #1.

- [x] Task 44 implementation: Typed channel-neutral events and validated replies, with
  transport length limits and one validation boundary for every reply branch.
- [x] Task 45 implementation: Private-chat normalization, token-safe HTTP, long polling,
  sender, prompt callback acknowledgment and signed conversation-bound choices.
- [x] Task 46 implementation: Encrypted durable inbox, same-transaction offset commit,
  scoped update dedup, lead-row serialization, per-bot receiver lock and reply outbox.
  Restart recovery republishes pending work; interrupted/ambiguous sends stay uncertain.
- [x] Task 47 implementation: OpenAI-only model roles, explicit masked API-key loading,
  typed contracts, deadlines, bounded retries/output and sanitized usage/latency logs.
- [x] Task 48 implementation/live checkpoint: Idempotent synthetic institution, courses,
  batches, rules and staff seed; actual Redis/TaskIQ processing and handset-confirmed replies.
- [x] Task 49 implementation: Encrypted conversation memory, explicit fact corrections,
  newest-first loading with chronological presentation, stored inbound/outbound outcomes.
- [x] Task 50 implementation: Tenant/actor-bound course and batch choices, active/capacity
  checks, explicit multi-batch selection and invalidation/re-evaluation on course changes.
- [x] Task 51 implementation: Typed evidence-backed extraction, active-question numeric
  routing, code-owned rules, missing/eligible/ineligible/review outcomes and no-rule abstention.
- [x] Task 52 implementation: Ready-upload search, relevance floor, suspicious-chunk
  exclusion, exact source quotations and unsupported-question abstention.
- [x] Task 53 implementation: Validated plain-text sends, safe failure replies, per-chat/
  institution model limits, language preference/templates and bounded query translation.
- [x] Task 54 implementation: Manual staff provisioning, salted scrypt, hashed expiring
  sessions, CSRF/origin controls, shared production throttles and tenant authorization.
- [x] Task 55 implementation: Audited tenant-scoped inquiry/detail, ordered conversation,
  selected course/batch, eligibility evidence and human-request APIs.
- [x] Task 56 implementation: Staff login, inquiry/status/course filters, detail, facts,
  evidence, source documents, conversation/history pagination and human-request queue.
- [x] Task 57 implementation: Recorded student request, paused qualification, staff
  acknowledge/resolve and separate explicit resume. Subsequent messages remain visible.
- [x] Task 58 core acceptance: Real database journey, duplicate/concurrent processing,
  cross-tenant negatives, correction/grounding/abstention/request controls and live API smoke checks.
- [x] Task 59 local-runtime choice: Existing PostgreSQL/Redis plus API, TaskIQ worker,
  one polling receiver and Next.js. Added data-store readiness and production debug rejection.
- [x] Task 60 draft assets: Root setup/status docs, demonstration script, six-slide
  editable deck and 178-word AI Impact Statement.

**Live evidence:** `python -m src.scripts.validate_services --openai --telegram`
passed structured output, 1536-dimensional embeddings, bot identity and absence of a
webhook conflict. The user confirmed receiving replies from `@mike0011_bot`.
The first real conversation persisted six inbound events and age/marks field memory
with an eligible result. Subsequent user-sent checks brought the saved total to ten:
age 17 produces an ineligible response, age 21 restores eligible, the campus question
returns the exact Kochi quote with its reference file/passage, and the moon question
abstains. All four additional replies have confirmed sends. Nine replies are confirmed
sent overall; one earlier send remains uncertain after an intermittent network failure
and is deliberately not blindly retried. Authenticated staff API validation confirms
all 20 inbound/outbound entries, age 21, the eligible result and both FAQ responses.
The local services stopped during an interruption and were restarted without losing
the stored inquiry. The user's resent `/human` was then processed, its acknowledgment
reply confirmed sent, and an open request persisted with the lead handed off.
The real Chrome staff dashboard displayed the request and conversation. Clicking
Acknowledge persisted acknowledged; Resolve persisted resolved while keeping the lead
handed off. Opening the resume confirmation also preserved that pause; Confirm resume
persisted resumed and changed the lead to qualifying for the next student message.
All four actions have audit records: human.requested, human.acknowledged,
human.resolved and human.resumed. Final totals: **11 events**, **10 sent replies**,
**one earlier uncertain reply** and **one resumed human request**. The staff actions
send no Telegram reply; the next-message behavior remains distinct from this saved
resume-state verification. Resolved/resumed browser screenshots were visually checked.

The HTTP client's default INFO logger initially exposed a token-bearing URL in local
worker output. A redaction regression test now passes, HTTP logging is restricted,
the user revoked/replaced the token, and the replacement passed bot verification.
No token value is recorded in repository documentation. Receiver/worker restart
preserved existing conversation data and refreshed the encrypted bot credential.

**Database evidence:** The complete final opt-in integration suite passed **15 tests**. It
initially exposed old fixtures using plain PostgreSQL without pgvector; switching
those fixtures to the actual required pgvector image fixed the failures. A subsequent
scoped journey run passes **4 tests**, including no-rule, closed-batch, foreign-course,
explicit-refusal and uncertain-send cases. A test-first regression exposed later replies
overtaking an earlier queued reply; outbox delivery now preserves per-inquiry order.
Another failing regression required explicit refusal to persist an information-needed
outcome rather than repeat the qualification question. Both fixes pass the final suite.

**Browser/provider evidence:** A real Chrome test through the Next.js proxy passed
staff login, real upload/indexing and semantic search using OpenAI, loading the actual
persisted Telegram inquiry, conversation viewing, both viewport widths and logout.
The test now waits for inquiry data rather than allowing a loading-state-only pass.
The five-case live retrieval smoke test originally failed Hindi/Malayalam, then passed
English, Hindi, Hinglish, Malayalam and unsupported-question abstention after bounded
query translation. This small test is not a language fluency or broad relevance claim.

**Final local verification:** `bash backend/scripts/verify.sh` passes lint, formatting,
strict mypy and **156 tests**, with 16 integration tests deselected and two pre-existing
RAG AsyncMock warnings. Live configuration was isolated and restored. The separate
full integration run passes all **16 tests**. Frontend lint and production build previously passed;
the real Chrome workflow passes with mandatory inquiry loading and both viewport sizes.
Scoped adversarial review covered callback ownership, tenant boundaries, provider
grounding/refusal, delivery ordering/uncertainty, read-only detail access and request
state transitions; no unresolved important/critical finding within the implemented slice.

The original Dockerfile build and production smoke passed. A later BuildKit parent-cache
error prevented a direct refresh; the verified refresh reused the built dependency image
after an exact uv.lock hash comparison, then copied the current source/migrations.
`admitflow-local:verified` is image
`sha256:32518f7a92778f07575762f4d916324dfb3fcc3e777d4adaa2bb4c13fec6d65b`.
All **67** Python/JSON source files match the host. The image starts with production
settings, reports healthy, runs as UID 10001, includes the conversation migration,
excludes demo credentials and returns 404 for the debug route. This is local packaging
evidence, not a cloud/database readiness claim.

The [staff walkthrough](../docs/event/artifacts/staff-walkthrough.webm) records **33 seconds**
of the actual local production frontend: ready reference search, persisted inquiry,
rule evidence, conversation, staff-request screen and logout. An extracted frame was
visually inspected. It is silent staff evidence, not a final handset/event submission video.
The tested code/configuration fingerprint is in [BUILD_MANIFEST.json](../docs/event/BUILD_MANIFEST.json).

**Expanded acceptance work:** Added a bounded 24-case live FAQ evaluator covering
campus, library and hostel facts plus unsupported Wi-Fi password, job guarantee and
moon questions in English, Hindi, Hinglish and Malayalam. It scores actual source
quotations/abstention, exits nonzero on failure and never commits database changes or
sends Telegram messages. Test-first scoring checks reject missing/wrong sources,
irrelevant quotations and outage messages presented as abstention; both tests pass.
The full gate now passes 156 tests, and the full database suite passes 16, including
provider outage, model refusal and invalid-schema cases preserving facts and allowing
handoff. The CLI's first live run completed **0/24** because provider authentication
failed, not because measured multilingual answer quality was zero. A separate read-only
OpenAI credential probe returns **401 invalid_api_key**. Earlier successful live evidence
is historical and must not be presented as current credential readiness. A valid replacement
key was requested; do not repeat live calls until it is saved. Raw results are in
[EVALUATION_RESULTS.json](../docs/event/EVALUATION_RESULTS.json).

The [language review packet](../docs/event/LANGUAGE_REVIEW.md) contains actual bot
templates and reviewer fields. Fluent approval remains unclaimed. A
[prior-work disclosure draft](../docs/event/PRIOR_WORK_DISCLOSURE.md) is prepared.
The new [58-second journey recording](../docs/event/artifacts/student-to-staff-walkthrough.webm)
shows the actual staff view of the saved live course/batch choices, corrections,
sourced/unsupported answers and resumed request; an extracted frame was inspected.
It is silent and does not show new handset activity or replay staff state changes.
`npm run record:demo -- --journey` reproduces it; existing recordings are protected
against overwrite. The original 33-second staff recording remains preserved.

The final source-layer image is `admitflow-local:release-check`,
`sha256:ccd06cf787add026fdf5d6f22c6a39f3fc1ee01efcf80de15d47d914427df851`.
It reuses verified dependencies after exact uv.lock hash comparison, matches all 68
source files, starts healthy with production settings under UID 10001 and excludes
demo credentials. The latest code/configuration fingerprint is
`ac310de5df8d2eb057483feba0a21008ee28ec5f005a7c15e8ab3e103cf81885`.
Adversarial review of the added evaluator checked synthetic-tenant restriction,
no persisted lead/messages, source/abstention scoring, bounded calls, sanitized errors
and nonzero failure exit. No runtime conversation behavior was changed by this slice.

**Remaining acceptance and release work:**

- [x] Complete the final repository gate, full integration run, frontend lint/build and container smoke after edits.
- [x] Record the local staff walkthrough and fingerprint the tested source/configuration.
- [x] Confirm live age corrections, sourced FAQ and unsupported-question abstention in persisted replies and staff visibility.
- [x] Confirm live `/human` intake and staff acknowledgment, resolution and explicit resume, including pause preservation and audit records.
- [x] Prepare and execute the 24-case FAQ evaluation, add provider-failure database coverage and create the fluent-review packet.
- [x] Replace the invalid OpenAI key and pass the expanded live FAQ evaluation: **24/24**.
- [x] Complete agent review of the language templates as requested; record scope and limits in LANGUAGE_REVIEW.md.
- [x] Record the longer actual staff view of the saved student journey and prepare prior-work disclosure.
- [ ] Final demo recording, owner/team/license details, judge-accessible links and portal/prior-work confirmation.
- [ ] Git publication, PR/CI/adversarial merge gate and any selected-host deployment.

### Release tracking for the existing plan

**Full-roadmap execution authorized:** The user explicitly includes every later product
milestone and wants owner/team/license/submission details handled last. Agent language
review is accepted; seek human input only when necessary. Keep using Telegram/OpenAI,
the existing plan and this task list. The user's latest instruction authorizes Git publication.

**Current implementation slice: Tasks 28/34.** Catalog/settings tests first failed with
404s. New tenant-scoped administrator APIs now pass real database create/edit/archive,
rule/capacity validation and role/tenant negatives. Windows lacked IANA timezone data;
adding the standard tzdata package made valid timezone validation portable. The
management frontend now passes the actual desktop/mobile browser workflow and build.
Discount management passes its database and permanent browser tests; the duplicate-code
regression exposed audit flushing outside the conflict handler and is fixed. Applying
settings to scheduled operations remains open. Tasks 18/31 application collection/review
now pass two database tests plus labelled synthetic staff-browser validation. The current
full backend gate passes **156 tests**, strict types in 70 source files, lint and format;
the full integration suite passes **22 tests** after isolating development login-throttle
state between cases (retaining enforcement within each test). Frontend lint/build and
the catalog/discount real-browser test pass. No open important/critical finding remains
in the reviewed catalog/application slice. Current image packaging predates tzdata and
these application changes and must be rebuilt before claiming a final deployable image.
The earlier push hold has been superseded by explicit user authorization to publish to
Shan091/admitflow. Preserve the existing history and publish a feature-branch checkpoint.
The full integration rerun at this earlier checkpoint passed **22 tests** after isolation.

**Publication checkpoint:** The current backend baseline gate passes **160 tests**, lint,
format and strict typing across 81 source files. Frontend lint and production build pass.
The database integration rerun passes **28 tests** with the Redis-only case skipped
while local configuration is isolated; that case then passes separately against local
Redis (**29 integration tests verified in total**). Pattern scans of publishable
files and 197 historical Git blobs found no credential matches. Local configuration and
generated graph outputs are excluded. The payment implementation has automated coverage
for fee confirmation, duplicate jobs, uncertain outcomes and signed payment events; its
real Razorpay test-card journey, reconciliation and later operations remain unfinished.
Publication must not tick the remaining roadmap or the PR/CI/merge release gates.

- [x] Push preserved main history (`96b5c75`) and checkpoint (`a4212cb`) to Shan091/admitflow.
- [x] Open [draft PR #1](https://github.com/Shan091/admitflow/pull/1) from `codex/telegram-admissions-checkpoint`.
- [ ] Complete CI and adversarial review before merging; full roadmap completion remains open.

**Replacement repository publication:** The user subsequently deleted/recreated the
remote and explicitly requested fresh commit history. A fresh baseline and verified
source snapshot were created without old ancestors. New PR #1 passed backend/frontend
CI and was squash-merged to replacement `main` (`64105a9`). Its complete tree matches
the verified `26f5a3b` source. Remote main has exactly **2 newly made commits**, with
old history retained locally only. Earlier publication entries above refer to the
deleted repository. Current staff-controls work remains local/in progress until its
complete gate and browser verification pass.

**Credential/retrieval follow-up:** The user saved a valid replacement OpenAI key;
structured output, 1536-dimensional embeddings and Telegram provisioning pass again.
The first 24-case run with the valid key passed 20. Library/hostel cases in Hindi and
Malayalam retrieved supporting chunks but failed quotation selection. A new database
regression first failed because quotation selection saw the original-language question;
it now receives the validated translated query. The scoped database run passes all
three management/translation tests, and the live rerun passes **24/24**. No similarity
threshold was lowered. API/worker were restarted to load the valid credential.

**Payment/ordering/transcript follow-up:** The current backend gate passes **163 tests**,
lint/format and strict types across **83 source files**. The disposable PostgreSQL suite
passes **32 integration cases**, with the Redis case then passing separately (**33 total**).
Provider lookup regressions first failed because the method was absent; ordering first
failed because a bot reply overtook an earlier standalone send. Both now pass. Signed
settlement also cancels an unsent payment link; its regression first reproduced the
stale queued link. Staff lookup cannot create another link or infer settlement, and
cross-tenant/staff-write negatives pass. A 77-message transcript test verifies two pages,
equal-time cursor stability, bot/student/payment kinds and invalid/foreign access.

Frontend lint/build, payment/transcript fixture-browser checks and the catalog/discount
workflow pass. The real staff login/upload/OpenAI search/saved inquiry workflow passes
after replacing an incorrect first-row assumption with selection of actual inbound
evidence. Desktop/mobile screenshots were inspected with no overflow; design detector
reports no findings. Synthetic browser fixtures are separate from real service evidence.
The local database is at `f129a064c5e8`; API, worker, receiver and frontend were restarted.
Health/readiness pass, the worker listens, the bot receiver is ready, and audited staff
reads retain **22 transcript entries across 2 inquiries**. No fake payment/Telegram event
was added to the demo database. The user needs a Razorpay test account before real
payment validation. Targeted review checked auth/tenant scope, invoice invariants,
raw-body signatures, lock order, bounded claims and encrypted/audited transcript reads;
the identified ordering and stale-link defects are fixed. Next: Tasks 20/29 staff
takeover/co-pilot, followed by the remaining product and operations milestones.

- [ ] Task 44 release: Typed channel-neutral engine events and validated reply boundary.
- [ ] Task 45: Telegram private-chat receiver, sender and callback acknowledgment.
- [ ] Task 46: Durable event intake, scoped dedup/locking and restart recovery.
- [ ] Task 47: OpenAI-only configuration, typed contracts and bounded failure handling.
- [ ] Task 48: Reproducible synthetic catalog/startup and first live Telegram roundtrip.
- [ ] Task 49: Recent inbound/outbound history, facts and correction semantics.
- [ ] Task 50: Validated course/batch selection and availability.
- [ ] Task 51: State-aware qualification and deterministic eligibility outcomes.
- [ ] Task 52: Reviewed knowledge ingestion, relevance/abstention and source grounding.
- [ ] Task 53: Input/retrieval/output validation, language experience and safe sends.
- [ ] Task 54: Staff provisioning, authentication and tenant authorization.
- [ ] Task 55: Tenant-scoped lead/conversation and human-request APIs.
- [ ] Task 56: Staff login, lead list/detail and human-request queue UI.
- [ ] Task 57: Human-request acknowledgment, resolution and automated-flow resume.
- [ ] Task 58: Integrated evaluations, security/failure checks and live evidence.
- [ ] Task 59: Packaging, runtime choice and selected-host deployment readiness.
- [ ] Task 60: Final product README, demo recording, deck, AI statement and submission.

Tick implementation acceptance only with command/result/build evidence. A live
roundtrip additionally requires a configured Telegram bot and user/device confirmation.
Applications, payments, co-pilot, follow-ups and other later work retain their original
IDs below. Historical WhatsApp/default-provider instructions do not override ADR-012.

## Retained foundation and institutional roadmap

The user selected this AdmitFlow repository and its **full institutional MVP roadmap**.
Preserve all tasks and existing completion evidence. Keep active planning self-contained.
See [EVENT_CONTEXT.md](../EVENT_CONTEXT.md) and the
[resource plan](../docs/event/RESOURCE_PLAN.md) before starting implementation.

- [ ] Record and verify hackathon credit activation, eligible services, quotas, expiry and
  post-credit costs. No grant redemption, spending or cloud provisioning is authorized by a
  planning checklist alone.
- [ ] Select a bounded event milestone from the full roadmap after confirming prior-work
  disclosure and the announced surprise requirement. Define acceptance and verification first.
- [ ] Prioritize resources that improve the admissions journey: structured extraction and
  evaluation, supported hosting, approved institution knowledge and pilot/mentor feedback.

---

## Phase 1: Foundation

### Task 1: Initialize Python project, FastAPI, settings, and Docker
**Description:** Create the `backend/` directory, `requirements.txt`, FastAPI app entry, settings singleton, and Dockerfile.
**Acceptance criteria:**
- [x] FastAPI boots on localhost:8000
- [x] `/docs` shows Swagger UI
- [x] Settings loaded from `.env`
**Verification:** `uvicorn src.main:app --reload` starts successfully
**Dependencies:** None
**Estimated scope:** Small

### Task 2: PostgreSQL schema (SQLAlchemy + Alembic)
**Description:** Define all core SQLAlchemy models: Institution, StaffUser, Course, Batch, QualificationRule, DiscountCode, Lead, LeadFact, Message, Application, PaymentOrder, AuditLog. Every table has `tenant_id`.
**Acceptance criteria:**
- [x] All models defined with proper relationships
- [x] Alembic migration runs cleanly
- [x] `tenant_id` on every tenant-scoped table
**Verification:** `alembic upgrade head` succeeds
**Dependencies:** Task 1
**Estimated scope:** Large

### Task 3: TaskIQ + Redis broker setup
**Description:** Configure TaskIQ with Redis as the message broker for background processing.
**Acceptance criteria:**
- [x] TaskIQ broker boots successfully
- [x] A dummy task can be enqueued and processed
**Verification:** Trigger a test task from a `/debug` endpoint
**Dependencies:** Task 1
**Estimated scope:** Small

### Task 4: PII encryption utilities and audit log infrastructure
**Description:** Build `security.py` (encrypt/decrypt PII fields) and the audit log write utility.
**Acceptance criteria:**
- [x] Phone numbers and names can be encrypted/decrypted transparently
- [x] `write_audit_log()` function writes to the `audit_log` table
**Verification:** Unit tests for encryption roundtrip and audit log writes
**Dependencies:** Task 2
**Estimated scope:** Small

---

## Phase 2: WhatsApp Ingress

> **Phase 1 → Phase 2 carry-over (from the foundation readiness audit).**
> Phase 1 (Tasks 1–4) is complete and green — no defects. These are *forward-looking
> prerequisites* the Phase 2 webhook needs; none existed yet at end of Phase 1. Do them
> as the opening moves of the tasks noted, not as afterthoughts:
>
> 1. **Shared async Redis client/helper** — a `redis.asyncio` client for app code (the
>    TaskIQ broker's internal Redis is separate). Needed by **Task 5** (`SETNX` dedup) and
>    **Task 7** (Lua CAS mutex). The `redis[hiredis]` dep is already installed; this is
>    net-new code, no mutex/dedup foundation exists today.
> 2. **Meta webhook config in `Settings` + `.env.example`** — `meta_app_secret` (HMAC body
>    verify), `whatsapp_verify_token` (GET challenge), Meta access token, and Graph API
>    version. None exist yet. Owned by **Task 5** (and reused by Task 6 sending).
> 3. **E.164 phone-normalization helper feeding `hash_phone`** — deliberately deferred from
>    Task 4 to its first caller. Un-normalized input (`+91 98765…` vs `919876…`) defeats the
>    `(tenant_id, phone_hash)` unique constraint and creates duplicate leads. Owned by
>    **Task 5** (lead creation / lookup by phone).
> 4. **Decision: UNIQUE/partial index on `messages.wa_message_id`?** Today it is indexed but
>    *not* UNIQUE — dedup is Redis-`SETNX`-only by design (ADR-002). Make a conscious call in
>    **Task 5** on whether to add a DB-level backstop for when the Redis layer is bypassed.
>
> Naming note: acceptance text below says "`audit_log`"; the real table is `audit_logs`
> (code + migration agree) — cosmetic, no change needed.

### Task 5: Meta WhatsApp webhook (HMAC + dedup + enqueue)
**Description:** Build `GET` (challenge verification) and `POST` (HMAC verify body, Redis SETNX dedup on `message.id`, extract payload, enqueue to TaskIQ).
**Acceptance criteria:**
- [x] `GET /api/webhook` passes Meta challenge
- [x] `POST /api/webhook` returns 200 OK immediately
- [x] Duplicate `message.id` silently dropped
- [x] Valid messages enqueued to TaskIQ
**Verification:** Test with ngrok + Meta test tool
**Dependencies:** Task 3
**Estimated scope:** Medium

### Task 6: WhatsApp message sending service
**Description:** Build `whatsapp.py` service with functions to send: text, interactive buttons, interactive lists, and template messages via Meta Cloud API.
**Acceptance criteria:**
- [x] `send_text()`, `send_buttons()`, `send_list()`, `send_template()` all work
**Verification:** Send a test message to a verified number
**Dependencies:** Task 1
**Estimated scope:** Medium

### Task 7: Redis distributed mutex
**Description:** Implement `redis_mutex(key)` async context manager using Redis Lua CAS for owner-safe release, with keepalive TTL extension.
**Acceptance criteria:**
- [x] Only one worker processes a message per phone number at a time
- [x] Lock auto-releases after TTL if worker crashes
**Verification:** Unit test with simulated concurrent access
**Dependencies:** Task 3
**Estimated scope:** Small

---

## Phase 3: AI Core (Engine + RAG)

### Task 8: Engine state definition and lifecycle
**Description:** Define the conversation state schema (a plain dataclass/Pydantic model loaded per turn, not a graph state) including: `lead_status`, `conversation_history`, `current_course`, `extracted_facts`, `pending_order`, `applied_discount`, `co_pilot_mode`, `consult_stage`. Build `engine/state.py` (lifecycle states + allowed transitions) and the `engine/dispatcher.py` skeleton (`handle_turn()`).
**Acceptance criteria:**
- [x] State schema defined with all required fields
- [x] Lead lifecycle transitions enforced in code
**Verification:** Unit test state transitions
**Dependencies:** Task 2
**Estimated scope:** Medium

### Task 9: Multi-provider LLM factory with fallback
**Description:** Build `llm_factory.py` that tries Gemini → OpenAI → Anthropic with automatic fallback on API errors (chain per ADR-007; model IDs config-driven).
**Acceptance criteria:**
- [x] Primary provider used when healthy
- [x] Automatic fallback to next provider on error
- [x] All providers return the same interface
**Verification:** Mock primary provider failure, verify fallback triggers
**Dependencies:** Task 1
**Estimated scope:** Medium

### Task 10: Input guardrail node
**Description:** First node in the graph. Detects prompt injection, profanity, and abuse patterns. Issues canned refusal and halts processing.
**Acceptance criteria:**
- [x] Injection attempts detected and blocked
- [x] Profanity detected and blocked
- [x] Clean messages pass through unchanged
**Verification:** Unit tests with adversarial inputs
**Dependencies:** Task 8
**Estimated scope:** Medium

### Task 11: Triage node (intent detection)
**Description:** Routes incoming messages to the appropriate downstream node: Discovery, RAG, Qualification, Handoff.
**Acceptance criteria:**
- [x] Correct routing for course exploration, knowledge questions, qualification answers, and human requests
**Verification:** Unit tests with representative message types
**Dependencies:** Task 8, 9
**Estimated scope:** Medium

### Task 12: Discovery node
**Description:** Presents available courses as WhatsApp interactive lists/buttons. Handles course selection and batch routing.
**Acceptance criteria:**
- [x] Courses fetched from DB filtered by `tenant_id`
- [x] Only batches with `seats_remaining > 0` shown
- [x] Tap-based selection updates lead state to `discovering`
**Verification:** Integration test with seeded course data
**Dependencies:** Task 8, 6
**Estimated scope:** Medium

### Task 13: RAG pipeline
**Description:** Build document ingestion (chunk, embed, store in pgvector), hybrid search (dense + lexical with RRF), and RAG chunk sanitizer.
**Acceptance criteria:**
- [x] Documents chunked and embedded per tenant
- [x] Search returns relevant chunks above confidence threshold
- [x] Chunks sanitized before injection
**Verification:** Golden question retrieval test (≥80% hit rate)
**Dependencies:** Task 2
**Estimated scope:** Large

### Task 14: RAG node
**Description:** Graph node that retrieves from the knowledge base and generates an answer. Fail-closed below confidence threshold.
**Acceptance criteria:**
- [x] Answers knowledge questions from institution documents
- [x] Says "I don't have that information" below threshold (no hallucination)
**Verification:** Test with institution FAQ documents
**Dependencies:** Task 13, 9
**Estimated scope:** Medium

### Task 15: Qualification node
**Description:** Asks the user questions to extract field values, then verifies against structured course rules in code. Extraction uses native structured outputs (JSON-schema / function calling), not free-text parsing — extracted fields feed deterministic rule eval (ADR-007 LLM efficiency).
**Acceptance criteria:**
- [x] AI asks the right questions to fill rule fields
- [x] Field values extracted via structured output into a typed schema (no regex/free-text parsing)
- [x] Code evaluates field/operator/value rules deterministically
- [x] Lead marked `admission_ready` only when ALL rules pass
**Verification:** Unit tests for rule engine + integration test with mocked LLM
**Dependencies:** Task 8, 9, 12
**Estimated scope:** Large

### Task 16: Output guardrail
**Description:** Validates AI response before sending to WhatsApp. Blocks hallucinated fees, made-up course names, PII leakage, and ensures WhatsApp-safe formatting.
**Acceptance criteria:**
- [x] Monetary figures not from DB are blocked
- [x] Course names not in the DB are flagged
- [x] WhatsApp formatting applied correctly
**Verification:** Unit tests with adversarial AI outputs
**Dependencies:** Task 8
**Estimated scope:** Medium

### Task 17: Wire webhook → TaskIQ → engine dispatcher → WhatsApp
**Description:** Connect all the pieces: TaskIQ worker picks up the message, runs it through the full `handle_turn()` dispatcher (decide → dispatch → generate → guard), and sends the response.
**Acceptance criteria:**
- [ ] Full loop works end-to-end
- [ ] Episodic memory (`messages` table) persists conversation between turns; recent turns reloaded each message
- [ ] Semantic memory (`lead_facts`) updated after each turn
**Verification:** End-to-end test on a real WhatsApp device
**Dependencies:** Task 5, 6, 7, 8–16
**Estimated scope:** Medium

---

## Phase 4: Advanced Bot Features

### Task 18: Application form collection node
**Description:** Collect structured application data through explicit Telegram prompts.
**Acceptance criteria:**
- [x] Full name, DOB, parent/guardian, address and previous school collected after an explicit start; cancel and review/submit are supported.
- [x] Form saved encrypted in the application table; new DOB/school values are not written to legacy plaintext columns.
- [x] Lead moves through form_collecting to payment_pending (or under_review for a zero-fee course).
**Evidence:** Database form journey proves invalid-DOB rejection, stale-submit nonce rejection,
explicit submission, replay protection, encryption, no seat reservation and application-state
preservation through later qualification/course requests and human resume. Live transport
for the earlier inquiry is separate; no new handset application submission is claimed.
**Verification:** Integration test collecting a full application
**Dependencies:** Task 15, 17
**Estimated scope:** Medium

### Task 19: Razorpay integration
**Description:** Build discount code validation, payment link creation (raw httpx), HMAC webhook verification, and in-chat confirmation.
**Acceptance criteria:**
- [x] Invoice and provider request use DB-sourced integer paise, with validated discounts.
- [x] Fee preview and an expiring, nonce-bound explicit tap precede link creation.
- [x] Immutable invoice, atomic job claims and outbound dedup prevent duplicate creation/sends; uncertain attempts are not blindly repeated.
- [x] Raw-body HMAC, full captured amount/reference checks and replay-safe events update payment status.
- [x] Verified settlement queues one encrypted Telegram confirmation; a full discount is WAIVED, not a fabricated PAID payment.
- [x] Staff monitoring and administrator reconciliation recover only an existing exact-reference link; lookup alone cannot confirm payment.
- [x] Known pre-creation configuration/rate failures can retry the same bounded invoice; missing or ambiguous links cannot authorize retry.
- [ ] Complete the actual Razorpay test-mode link/card/webhook/Telegram journey.
**Verification:** Provider contracts, fee-change reconfirmation, concurrent creation,
waiver, signed event tampering/replay, tenant/role boundaries and reconciliation are
automated. Browser fixture checks cover explicit staff confirmation, unresolved state,
inquiry navigation and mobile/desktop rendering. The user needs to create a Razorpay
test account; no real provider payment is claimed. Live payments remain disabled.
**Dependencies:** Task 17, 6
**Estimated scope:** Large

### Staff takeover and reviewed co-pilot evidence (Tasks 20 and 29)

The staff dashboard can pause bot replies, compose a manual Telegram reply, generate
an encrypted OpenAI draft, inspect its reference lookup, edit/approve/ignore it, and
resume AI. Draft generation never sends a message. Approval checks the latest saved
student event, staff revision, expiry, reviewed flag and active tenant-owned routing.
Exact retries reuse one durable outbox entry. Resume preserves facts and includes only
confirmed delivered replies in AI context. Office-hours and urgent-support copy is
reviewed in all four supported language variants.

The backend gate passes **175 tests**, lint/format and strict typing over **86 source
files**; two pre-existing RAG AsyncMock warnings remain. The final PostgreSQL run
passes **40 cases** (the Redis-only case is skipped there); the explicit Redis check
passes separately, for **41 integration cases**. These checks cover takeover, scoped access, pause/resume, draft expiry/replay, provider failures,
concurrent staff edits and cancellation during provider I/O. Frontend lint/build and
all **4 browser scenarios** pass, including mobile/desktop layout and manual-send retries.
Live OpenAI generated a 237-character draft from the saved Telegram inquiry; it was
ignored and AI resumed. Student facts were preserved and **zero outbound messages were
added**. This does not establish handset receipt of a new staff-authored reply.

Adversarial review reproduced and fixed stale ORM state overwriting a concurrent staff
revision, and cancelled draft generations overwriting the staff disposition. Default
tests now disable implicit developer dotenv loading, including LiteLLM's dotenv import;
explicit fixture configuration remains supported. No local secrets are moved or exposed.
Published through fresh repository PR #2 after both backend and frontend CI passed.
The published ancestry contains only newly created commits; prior repository history
remains local. The remaining handset/payment checks stay open.

### Task 20: Human handoff + co-pilot mode
**Description:** Handoff node for escalation. Co-pilot mode: AI generates suggested replies visible in dashboard.
**Acceptance criteria:**
- [x] Escalate clear frustration, explicit human requests and urgent safety signals; ordinary questions/refusals remain in the normal journey.
- [x] Co-pilot generates encrypted drafts without sending; approval requires explicit review, fresh context and an active takeover.
- [x] "Resume AI" restores the bot with confirmed staff replies and saved student facts; pending staff sends must finish first.
- [x] Institution-local office hours affect escalation wording without promising immediate support.
**Verification:** Integration test with escalation triggers
**Dependencies:** Task 17
**Estimated scope:** Large

### Task 21: Cold lead re-engagement worker
**Description:** Scheduled TaskIQ task that finds stale leads and sends AI-generated, context-aware follow-up hooks.
**Acceptance criteria:**
- [x] Identify opted-in stale inquiries using the configured delay; new messages, opt-out and staff takeover invalidate pending outreach.
- [x] Generate a context-aware multilingual reminder with a continue button; no invented urgency, deadlines, prices or admission promises.
- [x] At most two reminder delivery opportunities; a confirmed second reminder marks a still-inactive early-stage inquiry `cold`.
**Verification:** The feature-group gate passes lint/format, strict typing over **92
source files** and **186 default tests** (two pre-existing RAG AsyncMock warnings).
The full PostgreSQL suite passes **60 cases** and two real Redis cases pass separately:
**62 integration cases** total. Sixteen follow-up database scenarios cover explicit signed
consent, opt-out during takeover, fresh-state checks, queued inbound messages, office
hours/unknown hours, inactive courses, global disable, provider ambiguity, expired leases,
concurrent jobs and the two-reminder cap. Five unit cases cover eligibility and generated
copy refusal/provider-failure fallbacks.

Live OpenAI generation plus independent typed safety checks pass in English, Hindi,
Hinglish and Malayalam (**8 successful structured calls**, no neutral fallbacks).
No Telegram reminder was sent. Migration `e31b0847c629` is applied locally; existing
inquiries remain opted out. The API and worker were restarted with the follow-up task
module, the scheduler's one-shot sweep queued zero jobs, its continuous producer is
running, and authenticated saved-inquiry reads/readiness pass.

Post-review regression reproduced queued reminders remaining executable after consent
fields were rolled back. Downgrade now cancels queued reminders and preserves in-flight
uncertainty; the focused rollback/up-down test passes after the fix. Scoped adversarial
review covered consent defaults/signatures, source freshness, lock release/leases, send
opportunity counting, safe provider fallback, tenant boundaries and rollback. No open
important/critical finding remains. Publication follows the separate PR/CI workflow.
Reminder copy has agent language review; handset-delivered reminders and native-speaker
certification are not claimed. Task 26 analytics and the remaining roadmap stay open.
**Dependencies:** Task 17, 6
**Estimated scope:** Medium

### Task 22: Telegram delivery limits and queuing
**Description:** Track institution send volume, honor Telegram retry delays and queue messages when a configured send budget is reached. ADR-012 supersedes the old Meta tier requirements.
**Acceptance criteria:**
- [x] Conversation replies and standalone deliveries serialize claims per lead and preserve order in both directions; uncertain delivery is not automatically repeated.
- [x] Shared Redis reservations count send attempts per institution-local day; confirmed-delivery totals come from durable database records.
- [x] Workspace warning at 80% usage; authenticated counts, queued totals, reset time and administrator budget control.
- [x] Both bot and standalone replies stay queued at the cap; zero pauses new claims, raising the cap wakes deferred work, and production budget outages defer safely.
**Verification:** The backend gate passes **181 tests**, lint/format and strict typing
across **87 source files**. The full PostgreSQL suite passes **44 cases**; two Redis-only
cases pass separately (**46 integration cases** total). Six budget unit cases cover local
midnight/DST, replay, pause and unavailable budget storage. Four budget database cases
cover both delivery queues, concurrent claims, scoped settings, exact provider retry delay,
migration up/down and preservation. Rate-limited replies remain queued beyond three
attempts and wait the full delay measured from rejection. Final review reproduced a lost-statistics-write
regression; the four budget database cases pass after making confirmed counts DB-owned.
The real Redis test admits exactly seven of 100 competing reservations, replays without
spending again and proves tenant isolation. Failed/uncertain attempts consume budget.

Frontend lint/build and **all five browser scenarios** pass, including budget pause/change,
unavailable statistics, existing staff/payment flows and live OpenAI knowledge search.
Desktop/mobile screenshots show no overflow; the UI detector reports no findings. The
local database is at `9c5027e2d614`; API/worker/frontend were restarted on current sources,
and authenticated budget/readiness reads pass. No synthetic outbound event or unsolicited
Telegram message was added for this validation. Counts track attempts from activation;
they are an operational send cap, not a provider billing guarantee. Production requires
shared persistent Redis; the in-process development fallback is explicitly limited.

Adversarial review covered atomic caps, ambiguous sends, crash/replay reservation safety,
zero-limit revocation, repeated provider rate limits, tenant/admin boundaries, browser-write protection, local days and
queue recovery. No open important/critical finding remains in this slice. Publication
follows the separate feature-branch/PR/CI gate; GitHub records its result. Task 21
consent-aware follow-ups is next.
**Dependencies:** Task 6
**Estimated scope:** Small

### Task 23: Langfuse tracing integration
**Description:** Add `@observe()` decorators to all LLM-calling functions. Configure Langfuse client in `tracing.py`.
**Acceptance criteria:**
- [ ] Every LLM call visible in Langfuse with input/output/latency/cost
- [ ] Graph execution path traceable per conversation
**Verification:** Run a conversation and verify traces appear in Langfuse dashboard
**Dependencies:** Task 17
**Estimated scope:** Small

---

## Phase 5: Dashboard Frontend (Next.js)

### Task 24: Initialize the Next.js staff workspace
**Description:** The current SPEC uses the existing responsive staff design and plain CSS; the archived dark/glass/Tailwind baseline is superseded.
**Acceptance criteria:**
- [x] Next.js app runs on localhost:3000; lint/build and browser navigation pass.
- [x] Current staff-design tokens, responsive layouts and visible focus styles are in place; no dark/glass redesign is claimed.
**Verification:** Visual inspection of a test page
**Dependencies:** None
**Estimated scope:** Small

### Task 25: Authentication (email + password)
**Description:** Login with expiring opaque database sessions and administrator/staff roles under the current SPEC; JWT storage from the archived baseline is superseded.
**Acceptance criteria:**
- [x] Provisioned staff accounts can log in; default Overview and unauthorized access are verified.
- [ ] Institution-managed staff creation/invitation remains part of the administration milestone; public self-registration is not claimed.
- [x] Hashed opaque sessions use expiring HttpOnly cookies; passwords are salted hashes.
- [x] Route guards enforce tenant scope and administrator writes versus staff reads.
**Verification:** Login flow + unauthorized access blocked
**Dependencies:** Task 24, Task 2 (backend auth endpoints)
**Estimated scope:** Medium

### Task 26: Dashboard home (funnel analytics)
**Current execution:** Implemented on `codex/institution-reporting`, based on fresh
`origin/main` after PR #5 (`91f4370`). Real ORM transitions append same-transaction
`lead.stage_changed` audit records; current counts and known stage reach remain separate.
Older transitions are not invented. All aggregates use one repeatable-read snapshot,
creation-cohort date bounds and session-derived tenant scope. Application/payment
records supply verified conversions; paid and waived remain distinct. The Overview
home preserves access to knowledge, inquiries, staff requests, management and payments.
**Description:** Main dashboard page with funnel visualization and time-series lead charts.
**Acceptance criteria:**
- [x] Lifecycle funnel separates current states from observed reach, with explicit inquiry-cohort denominators; application, fee-satisfaction and enrollment conversions have real numerators/denominators.
- [x] Institution-local daily/weekly inquiry series, zero-filled gaps, accessible exact counts and bounded date filters.
**Verification:** The group gate passes lint/format, strict typing over **93 source
files** and **193 default tests**, with two existing RAG AsyncMock warnings. The full
PostgreSQL suite passes **65 cases**, and two real Redis cases pass separately:
**67 integration cases** total. Seven analytics unit cases cover local/DST boundaries,
Monday buckets, zero/invalid denominators, date limits and calendar extremes. Five
real-database cases cover scoped counts, corrections/history, empty/weekly data,
tenant/session controls, transactional/no-op/rollback auditing and consistent metrics
under a concurrent arrival.

Frontend lint/build and **all six browser scenarios** pass. The new overview case
covers filter changes, chart/denominator content and error/empty recovery. Real login
now confirms the Overview data before navigating to live upload/search and the saved
Telegram inquiry. Desktop/mobile inspection passes after a scoped override of the
legacy table minimum width; two bounded visual rounds are complete, with captures
under ignored `frontend/playwright-report/analytics-*.png`. Normal browser runs keep
layout assertions and make captures opt-in with `CAPTURE_UI=1`. The UI detector reports
no findings. API/worker/frontend run the current sources; live authenticated analytics
reports two saved demo inquiries and one applicant, with matching current-state and
series totals and healthy readiness. No history was backfilled and no Telegram message
was sent for analytics validation.

Scoped adversarial review covered tenant/session isolation, conversion subset rules,
concurrent snapshots, audit rollback/no-op behavior, date limits and data freshness
labels. No open important/critical finding remains in this slice. Publication follows
the feature-branch/PR/CI workflow; remaining CRM/exports/operations work stays open.
**Dependencies:** Task 25
**Estimated scope:** Medium

### Task 27: Leads CRM page
**Description:** Table/grid of all leads with status filters, search, and click-to-view detail.
**Acceptance criteria:**
- [ ] Leads fetched from FastAPI, filtered by tenant
- [ ] Status indicators (color-coded by lifecycle state)
- [ ] Search by name/phone
**Verification:** Load with seeded leads
**Dependencies:** Task 25
**Estimated scope:** Medium

### Task 28: Course & batch management
**Description:** CRUD pages for courses, batches, discount codes, and qualification rules builder.
**Acceptance criteria:**
- [x] Create/edit/archive courses and batches; archiving preserves existing inquiry references.
- [x] Qualification rules builder with typed field/operator/value validation.
- [x] Batch capacity and available seats visible; invalid capacity rejected.
- [x] Administrator discount-code create/edit/deactivate, percentage/fixed values, usage limits and immutable usage counts.
**Evidence:** Real database management tests cover roles, tenant boundaries, invalid values
and duplicate-code conflicts. Actual Chrome creation/archive, rules, fees and seat values
pass at desktop/mobile widths. The permanent catalog/discount browser test passes,
including INR-to-paise conversion and deactivation. Settings and application screens
inherit the existing staff design; detector checks report no findings.
**Verification:** Create a course with rules, verify in DB
**Dependencies:** Task 25
**Estimated scope:** Large

### Task 29: Chat takeover + co-pilot UI
**Description:** Messaging interface showing chat history, AI suggested replies, and manual send.
**Acceptance criteria:**
- [x] Unified student/bot/standalone-delivery history with payment labels, timestamps and delivery states; stable tenant-scoped cursor pagination includes equal-time messages.
- [x] AI-suggested replies support review, edit, approve and ignore; stale/expired drafts cannot be approved.
- [x] Manual text input queues a tenant-scoped Telegram reply with an exact-text confirmation and replay-safe send reference.
- [x] "Take Over" and "Resume AI" buttons, confirmations and bot-pause status.
**Verification:** PostgreSQL/API and browser scenarios cover takeover, manual-send retry, reviewed drafts and resume. A handset-confirmed staff-authored delivery is still a separate live check.
- [ ] Confirm one explicitly authorized staff reply on the Telegram handset.
**Dependencies:** Task 25, 20
**Estimated scope:** Large

### Task 30: Document management (RAG)
**Description:** Upload/delete institution documents for the RAG knowledge base.
**Acceptance criteria:**
- [x] File upload triggers durable backend ingestion (verified with an isolated worker invocation).
- [x] Document list shows indexed files and failure/retry states.
- [x] Delete removes chunks from pgvector; an active worker cannot republish a deleted upload.
- [ ] Upload a PDF and verify a grounded answer through the live Telegram bot.
**Verification:** See current execution evidence above. API/database and fixture-backed UI
checks are complete locally; live bot acceptance remains pending.
**Dependencies:** Task 13; provisioning/authentication slice of Task 54.
**Estimated scope:** Medium

### Task 31: Application submissions view
**Description:** Table of submitted application forms with detail view and manual review actions (Approve, Waitlist, Reject).
**Acceptance criteria:**
- [x] Submitted encrypted form fields displayed through audited tenant-scoped staff APIs.
- [x] Application links to the saved inquiry and conversation.
- [x] Explicit administrator approve/waitlist/reject controls; unpaid approval is blocked,
  final decisions cannot be overwritten, and approval allocates one available seat atomically.
**Evidence:** Two simultaneous approvals compete for one seat: one succeeds and one receives
409; repeating the winner does not allocate another seat. Actual staff-browser validation
uses a labelled synthetic seeded form, blocks unpaid approval, saves waitlist, checks
desktop/mobile and opens its inquiry. No Telegram updates were fabricated for that fixture.
**Verification:** Submit an application via bot, verify it appears in dashboard
**Dependencies:** Task 25, 18
**Estimated scope:** Small

### Task 32: Data export + webhook config
**Description:** CSV/Excel export for leads, applications, payments. Outbound webhook URL configuration.
**Acceptance criteria:**
- [ ] Export buttons generate downloadable CSV/Excel
- [ ] Webhook URL configurable per institution
- [ ] Events pushed to webhook URL in real-time
**Verification:** Export data + configure a test webhook URL
**Dependencies:** Task 25
**Estimated scope:** Medium

### Task 33: Real-time WebSocket notifications
**Description:** Notification bell with live badge count for new events.
**Acceptance criteria:**
- [ ] WebSocket connection established on dashboard load
- [ ] Badge increments on: new qualified lead, dead-letter message, co-pilot suggestion, payment received
**Verification:** Trigger an event from the bot, verify badge updates
**Dependencies:** Task 25
**Estimated scope:** Medium

### Task 34: Institution settings
**Description:** Settings page for business hours, re-engagement timing, and general config.
**Acceptance criteria:**
- [x] Business hours and IANA timezone configurable with opening/closing validation.
- [x] Re-engagement delay and optional retention period configurable by administrators.
- [ ] Verify the configured values affect follow-up, escalation and cleanup behavior once those operations are implemented.
**Verification:** Update settings, verify they affect bot behavior
**Dependencies:** Task 25
**Estimated scope:** Small

---

## Phase 6: Production Hardening

### Task 35: Sentry error monitoring
**Description:** Integrate Sentry SDK in both FastAPI and TaskIQ worker.
**Acceptance criteria:**
- [ ] Unhandled exceptions reported to Sentry with full context
**Verification:** Trigger a test error, verify it appears in Sentry
**Dependencies:** Task 17
**Estimated scope:** Small

### Task 36: Delete My Data endpoint
**Description:** API endpoint that purges all data for a given phone number: conversation state, lead facts, messages, application, payment orders.
**Acceptance criteria:**
- [ ] All user data deleted across all tables
- [ ] Deletion logged in audit trail
**Verification:** Delete a test user, verify no data remains
**Dependencies:** Task 4
**Estimated scope:** Small

### Task 37: Data retention auto-cleanup
**Description:** Scheduled job that deletes conversations older than the configured retention period.
**Acceptance criteria:**
- [ ] Conversations beyond retention period auto-deleted
- [ ] Configurable per tenant
**Verification:** Test with artificially aged data
**Dependencies:** Task 4
**Estimated scope:** Small

### Task 38: Docker Compose for local development
**Description:** `docker-compose.yml` with all services: FastAPI, TaskIQ worker, PostgreSQL+pgvector, Redis, Langfuse.
**Acceptance criteria:**
- [ ] `docker compose up --build` starts everything
**Verification:** Full stack boots from clean state
**Dependencies:** All previous tasks
**Estimated scope:** Medium

### Task 39: Production deployment
**Description:** Deploy Next.js to Vercel; backend API + TaskIQ worker + scheduler to Fly.io (always-on machines); Neon (managed Postgres + pgvector); Redis on Fly; Langfuse Cloud. Per ADR-007.
**Acceptance criteria:**
- [ ] Frontend accessible on production URL
- [ ] Backend API accessible on production URL
- [ ] Webhooks configured with production URLs
**Verification:** End-to-end test on production
**Dependencies:** All previous tasks
**Estimated scope:** Medium

---

## Phase 3–4 addition (see ADR-008)

### Task 40: `decide()` System-1 decision-layer abstraction
**Description:** Build `src/decision/` — a `decide()` interface exposing choice/score/noul primitives with calibrated probabilities. Demo backend uses Gemini Flash structured outputs; the interface is backend-agnostic so a self-hosted Laya backend can drop in later (ADR-008). Used by input guardrail, triage, readiness scoring, and escalation detection.
**Acceptance criteria:**
- [ ] `decide()` returns typed answers (label+prob / score / yes-no prob) via Gemini Flash structured output
- [ ] Guardrail, triage, readiness, and escalation call `decide()` (no ad-hoc LLM calls)
- [ ] Backend is swappable behind the interface (config-selected)
**Verification:** Unit tests with a mocked backend; each decision site covered
**Dependencies:** Task 9, 10, 11, 15
**Estimated scope:** Medium

### Task 41: Distill decisions into self-hosted Laya (post-demo)
**Description:** Stand up self-hosted Laya (Jev-compatible `/v1/systemone`) as a `decide()` backend. Use labels collected during the demo to fine-tune/calibrate the high-frequency decisions (triage, guardrail-triage, readiness, escalation). Switch per decision only after evaluating Malayalam/Hinglish accuracy and fitting calibration.
**Acceptance criteria:**
- [ ] Laya backend implements the `decide()` interface
- [ ] Malayalam/Hinglish accuracy measured per decision vs the LLM backend
- [ ] Calibration (temperature) fitted; over-confidence checked (ECE)
- [ ] OTHER/ESCALATE option present on all choice decisions
**Verification:** Offline eval set per decision; shadow-run against live LLM decisions before cutover
**Dependencies:** Task 40, 17
**Estimated scope:** Large

### Task 42: Advanced RAG Strategy (ADR-011)
**Description:** Implement the advanced RAG pipeline to handle complex document parsing, latency-optimized reranking, and contextual query rewriting.
This epic is broken down into sub-tasks for focused implementation.

### Task 42.1: Complex Document Parsing & Semantic Chunking
**Description:** Integrate `docling` (or `unstructured`) to parse uploaded PDFs into Markdown, preserving tables and structure. Replace the naive sliding window chunker in `rag.py` with a semantic, Markdown-header-aware chunker.
**Acceptance criteria:**
- [ ] Document ingestion pipeline uses `docling`/`unstructured` for PDFs
- [ ] Tables and multi-column layouts are preserved in Markdown
- [ ] Semantic chunking implemented (retains parent-child headers)
**Verification:**
- [ ] Unit tests uploading a complex PDF and verifying structural chunks
**Dependencies:** Task 13
**Files likely touched:** `backend/pyproject.toml`, `backend/src/core/rag.py`
**Estimated scope:** Medium

### Task 42.2: Contextual Query Rewriting
**Description:** Add a query resolution step before vector search. Use Gemini Flash to rewrite the raw WhatsApp message into a standalone query (resolving slang and pronouns using conversation history).
**Acceptance criteria:**
- [ ] Query rewriter LLM chain implemented
- [ ] Uses previous conversation turns to resolve ambiguous intent
- [ ] Pre-filters search space using metadata tags if a specific course is identified
**Verification:**
- [ ] Unit tests for query resolution given ambiguous user inputs
**Dependencies:** Task 13
**Files likely touched:** `backend/src/core/rag.py`
**Estimated scope:** Medium

### Task 42.3: Pluggable Reranker (Cohere API vs Local)
**Description:** Add a config-driven reranker layer to `search_chunks`. In dev mode, use a fast/free pass-through or tiny local cross-encoder. In prod mode, use Cohere's Rerank API via LiteLLM for high precision without CPU bloat.
**Acceptance criteria:**
- [ ] Reranking logic implemented after hybrid search
- [ ] `use_reranker` and `reranker_provider` (local vs cohere) added to settings
- [ ] Latency stays well within budget (since compute is offloaded)
**Verification:**
- [ ] Unit tests mock the reranker and verify correct top-N sorting
**Dependencies:** Task 42.2
**Files likely touched:** `backend/src/core/rag.py`, `backend/src/core/settings.py`
**Estimated scope:** Medium

---

## AIBoomi Startup Weekend session handoff

**Scope:** Preserve context in this repository; no new repository, product changes, or deployment.
**Dependencies:** Public event/handbook snapshots and repository inspection.
**Acceptance criteria:**
- [ ] Root EVENT_CONTEXT.md records the latest user direction, event rules, baseline facts, unknowns, and restart prompt.
- [ ] docs/event/ holds the preparation plan, source snapshots, and discrepancies.
- [ ] AGENTS.md links the handoff and local links/content have been checked.
- [ ] Follow the existing completion/commit workflow before marking this milestone complete.

Start at [../EVENT_CONTEXT.md](../EVENT_CONTEXT.md). Next implementation step proposed: bounded real WhatsApp readiness check, after the user resumes.

## WhatsApp readiness check (in progress)

**Scope:** One-hour evidence check in the renamed admitflow repository; preserve the dirty baseline. Local configuration authorized by the user. No broad implementation.
**Evidence:** [../docs/event/READINESS_CHECK.md](../docs/event/READINESS_CHECK.md).
**Acceptance criteria:**
- [ ] Real demo-phone ingress -> Redis queue -> registered worker -> delivered WhatsApp reply evidenced with latency.
- [ ] Seeded course selection, next-turn memory, and tenant-scoped persisted lead inspected.
- [ ] Pass/fail/blocker and smallest repair scope recorded at the timebox boundary.
- [ ] Prior-work disclosure updated from actual evidence; surprise requirement remains unclaimed until announced and implemented.

Fresh default baseline gate: 106 passed, 4 integration tests deselected, 2 warnings. This is not a live readiness pass.

### Readiness blocker: idle Redis worker restart (in progress)

**Evidence:** Actual TaskIQ worker raised Redis TimeoutError after five idle seconds, then restarted. Credentials validated separately using read-only Meta/OpenAI requests.
**Acceptance:** A real Redis listener remains alive beyond five seconds and consumes subsequent work; configure the blocking broker read timeout without changing normal Redis calls. Regression test first, then full gate and actual queue/worker smoke check.

### Readiness tunnel setup (in progress)

**Scope:** Expose only the existing signed Meta webhook via a temporary tunnel; keep local debug/docs routes private. Verify handshake, invalid signature rejection, and other-route 404s. No production deployment or dashboard claim.

### Test-number delivery diagnosis (blocked on Meta account restriction)

**Scope:** Correct the existing app callback and missing account subscription; observe signed delivery statuses without PII. Preserve other app subscriptions and existing webhook fields.
**Evidence:** READINESS_CHECK.md records successful subscription repair and a real failure webhook (131031). Meta health API reports the test account banned (141014), sending BLOCKED. Appeal in Meta Business Support Home is the next required user action; local configuration cannot lift the restriction.
**Verification:** Missing-status regression reproduced; focused tests cover signed status logs, invalid-signature rejection, PII exclusion, and tunnel route restrictions. Full gate result recorded in the readiness report when completed. No phone-delivery or complete learner-journey claim.

### Final Postman diagnostic (executed; delivery blocked)

User authorized executing the Postman setup and one final send. Imported collection ran via isolated temporary Newman, using ignored local credentials in memory. Health BLOCKED; send accepted HTTP 200; signed failure event 131031 confirmed (`f3fc27bca826` hashed reference). Safe local runner added; syntax checked. Corrected sandbox variable declarations, then read-only execution produced 2 assertions with 1 expected restriction failure. No subsequent send. Details: [../docs/event/POSTMAN_CHECK.md](../docs/event/POSTMAN_CHECK.md). Further delivery depends on Meta account access, not another client or API retry.
