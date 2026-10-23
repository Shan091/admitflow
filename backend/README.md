# AdmitFlow Backend

Admissions engagement backend using FastAPI and a hand-rolled async conversation
engine. Telegram and OpenAI are the selected product channel/provider. Follow
[SPEC.md](../SPEC.md) and the existing [plan](../tasks/plan.md) and
[task list](../tasks/todo.md).

## Stack

- **Python 3.12+**, managed with **uv**
- **FastAPI**, SQLAlchemy/Alembic, PostgreSQL/pgvector, Redis/TaskIQ and OpenAI
- **ruff / mypy --strict / pytest** in CI (GitHub Actions)

## Local development

```bash
# Install dependencies (creates .venv)
uv sync

# Run the API (http://localhost:8000, Swagger at /docs)
uv run uvicorn src.main:app --reload

# Run tests
uv run pytest
```

## Configuration

Settings load from environment / a `.env` file. Copy the template and fill in values:

```bash
cp .env.example .env
```

Model IDs are config-driven. [ADR-012](../docs/decisions/ADR-012-telegram-openai-mvp.md)
defines the active channel/provider decision.

## Current implementation and verification

Telegram bot and encrypted student identity storage is implemented. Phone contact
is optional; composite database constraints prevent cross-institution bot/lead links.
The Telegram receiver/sender, persistent admissions journey and staff inquiry/request
screens are now implemented. The API retains historical WhatsApp routes for compatibility;
the active demonstration uses Telegram. See the local runtime guide below.

The default gate expects no live Redis configuration. Isolate local live credentials
before running it and restore them afterward; never commit or print environment values.
The gate excludes real-service integration tests. Identity/migration checks use their
own disposable PostgreSQL container and do not apply changes to the demo database:

```bash
uv run pytest -m integration tests/integration/test_telegram_identity.py
```

Docker must be running. The new migration can downgrade cleanly for legacy data;
if Telegram-only rows exist, it refuses before dropping their identity tables.
Explicitly migrate those rows before a downgrade; phone numbers are never fabricated.

Create the Telegram bot through verified BotFather and save its token locally as
`TELEGRAM_BOT_TOKEN` for the upcoming adapter configuration. No token is needed for
automated tests. Do not claim a live bot from a passing schema test.

## Institution knowledge workspace

This slice provides manually provisioned staff login, administrator file/folder uploads,
background indexing, status/retry/delete and source-linked semantic search. It reuses
the existing documents/chunks tables. It does not finish the Telegram adapter or the
lead and human-request screens. The live demo database has not been migrated by
the automated tests; apply the migration deliberately before starting this workspace.

From `backend/`, after configuring PostgreSQL/pgvector, Redis, `PII_ENCRYPTION_KEY`
and `OPENAI_API_KEY` in ignored local configuration:

```bash
uv sync
uv run alembic upgrade head
uv run python -m src.scripts.provision_staff --institution-code your-code --institution-name "Your institution" --email admin@example.edu
uv run uvicorn src.main:app --reload
# Separate terminal, from backend/:
uv run taskiq worker src.tasks.broker:broker src.tasks.knowledge
```

The provisioning command prompts twice for a password (12–1024 characters), never
prints it, creates an institution if needed, and refuses to overwrite an existing account.
Use the institution code, email and password to sign in. Then from `frontend/`:

```bash
npm ci
npm run dev
```

The frontend proxies `/api` to `BACKEND_URL` (default `http://127.0.0.1:8000`). Use
`http://127.0.0.1:3000` locally. Fonts are bundled locally. For another browser origin,
set `STAFF_ALLOWED_ORIGINS` as a JSON array on the backend. Production requires
HTTPS, `APP_ENV=prod`, `DEBUG=false` and shared Redis; secure cookies and shared
rate limits depend on that configuration. This is not a production deployment checklist.

Default upload limits are 10 MiB/file, 30 MiB and 25 files/request. The UI batches larger
folder selections automatically and preserves nested paths. Supported: digital PDF
(100 pages maximum), DOCX and UTF-8 TXT/Markdown/CSV. No OCR, archive/folder ZIP
import, legacy DOC or complex layout reconstruction. DOCX archive expansion and
extracted text are bounded. A PDF with blank/scanned pages needs a searchable copy.

An accepted upload is durable even if enqueueing fails. Keep the API recovery loop
and worker running: recovery republishes queued jobs and reclaims expired attempts.
Identical bytes are deduplicated per institution, keeping the first source path. Failed
attempts retain encrypted originals for Retry; Remove deletes the original and all
published chunks. Empty search results indicate no passage passed the current
similarity floor; it is not a calibrated factual-answer confidence score. Model changes
require reindexing existing uploads; no model migration UI is provided yet.

Original bytes are encrypted with the configured Fernet key. Extracted institution
reference text and embeddings are stored in PostgreSQL and sent to OpenAI for
embedding. Do not use this reference library for applicant personal documents.
Do not rotate the encryption key without migrating encrypted records. ADMIN may
upload/retry/delete; AGENT may list/search. No anonymous upload or self-registration.

Limits per five-minute window: 10 logins per connecting-host/account combination,
100 per connecting host, 30 upload/retry requests per institution and 60 searches per
institution. No forwarded-IP header is trusted directly; configure trusted proxy handling
on the ASGI server before relying on per-host limits behind a reverse proxy.

Verification:

```bash
bash scripts/verify.sh
uv run pytest -m integration tests/integration/test_knowledge_workspace.py
# From frontend/:
npm run typecheck
npm run build
```

The integration suite uses a disposable pgvector container and synthetic embeddings:
it verifies real database operations, tenant boundaries, queue/provider failures, retry,
deletion during indexing, duplicate claims and migration rollback safety without paid
API requests. In addition to synthetic UI fixtures, a real Chrome check now covers
staff login, live OpenAI indexing/search and the persisted Telegram inquiry. Live
OpenAI structured output/embeddings and a handset-confirmed Telegram roundtrip pass.
Extended device source/correction/human-request checks remain tracked separately.

## Telegram admissions runtime

Follow [LOCAL_RUNTIME.md](../docs/engineering/LOCAL_RUNTIME.md) for the complete local
profile, migrations, synthetic seed, staff credentials and API/worker/receiver/frontend
commands. It also explains safe token rotation, readiness, paused human requests and
uncertain delivery. Keep one polling receiver per bot and run both task modules:

```bash
uv run taskiq worker src.tasks.broker:broker src.tasks.telegram src.tasks.knowledge --workers 1
uv run python -m src.telegram.receiver --institution-code demo
```

The active journey uses encrypted conversation inbox/outbox/memory tables. The original
WhatsApp dispatcher/nodes remain historical compatibility code; they are not evidence
of the Telegram acceptance checks. A read-only staff view does not create conversation
memory. Staff access is audited, and callback choices display readable course/batch
summaries instead of internal signatures. Rule evidence remains code-owned.

## Application payments

Eligible students explicitly start and submit an encrypted application. `/pay` previews
the DB-owned fee; `/discount CODE` applies an institution code before invoicing. Only
the signed confirmation tap queues a payment-link request. Queue recovery handles
known rejections; ambiguous provider creation and Telegram delivery remain unresolved
for staff review. A fee waiver is separate from a captured payment.

For a Razorpay **test** account, save `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET` and
`RAZORPAY_WEBHOOK_SECRET` in ignored `backend/.env`, with `PAYMENTS_LIVE_ENABLED=false`.
Provision the institution's encrypted configuration with:

```bash
uv run python -m src.scripts.provision_payments --institution-code demo
```

Provisioning performs a read-only credential probe. Configure the provider's
`payment_link.paid` event to the HTTPS endpoint `/api/payments/webhook/<institution-id>`
using the same webhook secret. A local endpoint alone cannot receive public events;
public ingress and an actual test-card journey must be verified before claiming live
payment acceptance. No production payment is enabled by local provisioning.

Staff can read `/api/staff/payments`; administrators can explicitly POST
`/<order-id>/reconcile` or `/<order-id>/retry` under that prefix. Reconciliation reads
the existing exact reference and cannot create a replacement. A lookup reporting paid
waits for signed confirmation. Only known configuration/rate failures below the attempt
limit can retry the same invoice. These actions require the normal staff session and
browser-write protection and are audited.

Staff lead detail now returns a unified, encrypted-source transcript with `message_id`,
`kind`, `created_at` and `older_cursor`. Pass the opaque cursor as `?cursor=...` to load
the next older 50-message page. It includes standalone payment deliveries and their
actual queued/sent/failed/uncertain status. It replaces event-number-only pagination.

## Staff takeover and reviewed co-pilot

Inquiry detail includes Take over, manual staff replies, co-pilot drafts and Resume AI.
The staff session and browser-write protection apply to every operation. Takeover pauses
automatic conversation replies while preserving inbound messages; a currently sending
bot reply must finish first. Resume waits for queued staff replies and restores saved
facts plus confirmed delivered conversation history.

Under `/api/staff/leads/<lead-id>`, POST `/takeover` and `/resume` control the mode.
POST `/messages` accepts `{request_id: <UUID>, text: <reviewed reply>}`; retry with the
same reference and text after an interrupted response. A changed reply requires a new
reference. The durable worker sends the reply; an API success means queued, not delivered.

POST `/draft` with `{request_id: <UUID>}` generates one encrypted, expiring draft without
sending. POST `/draft/<draft-id>` accepts `decision: approve|ignore`; approval requires
`reviewed: true` and optionally edited `text`. New student messages, staff revisions,
expiry or inactive routing prevent approval. Generation is bounded and throttled; provider
failure leaves manual composition available. Resume invalidates an unfinished draft.
The UI asks staff to review factual claims and confirm the exact text before queuing.

Institution timezone/business hours affect support wording. Immediate staff response is
never promised. Clear human requests, frustration and urgent safety signals use the staff
queue; the admissions inbox does not provide emergency support.

Tests ignore implicit local dotenv files. Use explicit environment variables for the Redis
integration check and `Settings(_env_file=...)` only in dedicated configuration fixtures.
Runtime CLI configuration still reads the normal ignored local `.env`.

## Telegram delivery budgets

Both conversation replies and standalone staff/payment messages reserve one shared
send attempt before making a Telegram request. Each institution starts with a daily
limit of 1000; an administrator can set 0–100000 in Institution settings. Zero pauses
new sends. The day resets at midnight in the configured institution timezone, including
daylight-saving changes. This is an operational cap rather than a provider billing limit.

Reservations are atomic in Redis and keyed by internal delivery/attempt references.
Replaying a database claim does not spend the same reservation twice; failed and
ambiguous attempts conservatively use budget. Deferred messages retain `queued` status,
do not increment their delivery attempts and are eligible again at the local reset.
Increasing the cap or changing timezone wakes budget-deferred work for re-evaluation.
Telegram's `retry_after` is preserved instead of shortened and measured from rejection.
Explicit rate-limit rejections remain queued beyond three attempts, subject to the same
daily cap; they do not become ambiguous retries. Existing ordering/recovery
and uncertain-delivery handling remain in force.

`GET /api/staff/delivery-budget` is session/tenant scoped. It returns tracked attempts,
confirmed database deliveries, queued budget deferrals and the next reset. The workspace
warns at 80% use or when counts cannot be checked. It never presents an unknown budget
count as zero. Confirmed-delivery totals use durable database records even if a Redis
statistics update fails. Attempt accounting begins when this feature is activated.

Production requires shared persistent Redis: a failed/unconfigured budget store defers
sends for a retry instead of bypassing the cap. Development without Redis uses a bounded
in-process fallback; that fallback is not a cross-process or production guarantee.
Preserve Redis persistence during restarts. Reservations and statistics expire after
several days and contain internal identifiers, not student contact data.

## Consented follow-up reminders

Existing and new inquiries default to no proactive reminders. A student opens
`/followups` and taps Enable reminders to opt in, or uses `/stop` / No reminders to
opt out. Preference changes are audited. These controls work while staff takeover
pauses normal bot replies. Every incoming message cancels queued older reminders and
moves the next eligible time out by the institution's configured delay.

Only inactive early-stage inquiries are considered: new, discovering, qualifying,
admission ready or an incomplete application. Payment/review/final states, active
human requests, staff takeover, inactive courses and pending student/bot work block
outreach. Explicit configured office hours are required; unknown or closed hours do
not permit a reminder. A reminder never invents a deadline, scarcity, a fee or approval.

The worker claims a short generation lease in encrypted conversation memory, releases
the database lock during OpenAI calls and rechecks current state before queuing.
Only language, public course name and stage are provided for reminder generation,
with a separate structured safety check. Unsafe/refused/unavailable model output uses
reviewed neutral copy. No student message, contact, form or fact value is sent for this
reminder-generation context. The encrypted outbox includes Continue inquiry and No
reminders controls.

Each inquiry allows at most two reminder delivery opportunities. Queue deferral at the
daily budget or outside office hours does not spend one; explicit Telegram rate limits
retry the same reminder. Ambiguous delivery spends its opportunity and stops automatic
outreach, preserving the unresolved state for staff. A confirmed second reminder marks
the still-inactive early-stage lead cold. New student activity never loses saved facts.
An already in-flight Telegram request cannot be recalled by a later opt-out.

Run the worker with the reminder task module and a scheduler producer:

```bash
uv run taskiq worker src.tasks.broker:broker src.tasks.telegram src.tasks.knowledge src.tasks.followups --workers 1
uv run python -m src.scripts.scheduler
# One read/dispatch/recovery sweep, using the same consent rules:
uv run python -m src.scripts.scheduler --once
```

The scheduler scans durable due times and recovers queued standalone deliveries.
Expired generation leases can be reclaimed after restart; duplicate jobs cannot
publish/send the same reminder twice. `FOLLOWUPS_ENABLED=false` disables new generation
and cancels pending reminders at send-time checks after processes reload configuration.
Stopping the scheduler stops new scheduled claims; keep the delivery worker running to
finish existing explicit work. Never manufacture consent or age a real inquiry to test
outreach; use disposable synthetic database fixtures.

A migration downgrade cancels queued reminders before removing consent fields, and
marks in-flight reminder requests uncertain. Older sender code therefore cannot execute
leftover queued outreach after rollback. A later upgrade again defaults all inquiries
to no consent; it does not invent or recover an opt-in from historical messages.

## Admissions analytics

The staff workspace opens on Overview. `GET /api/staff/analytics` derives the institution
from the authenticated session and accepts `from`, `to` (inclusive local dates) and
`bucket=day|week`. The default is the last 30 institution-local dates; a request is
bounded to 366 dates. Weeks begin Monday, partial edge weeks include only the selected
period and missing buckets are zero-filled. Local midnight/DST boundaries use the
configured IANA timezone. All aggregates share a repeatable-read snapshot, so concurrent
arrivals cannot mismatch a numerator and its denominator.

The cohort is inquiries created in the selected period, with progress observed as of
the report timestamp. Application conversion counts distinct applicants over inquiries;
fee satisfaction counts applicants with confirmed paid/waived orders over applicants;
enrollment conversion counts enrolled/approved applicants over applicants. Paid and
waived totals stay separate. An empty denominator produces an undefined rate rather
than a fabricated zero or 100 percent.

Current lifecycle counts are distinct from reached-stage counts. Real ORM lead-status
changes append `lead.stage_changed` audit rows in the same transaction; rollback removes
both. The reach calculation uses those observed from/to states and current states,
without inventing earlier transitions for older records. Every inquiry belongs to the
created-inquiry baseline, and stages can be skipped. Future bulk SQL status writers must
explicitly retain equivalent stage auditing; the existing bulk delivery updates only
change timestamps. No raw contact, fact, form or message data is returned in analytics.

The chart also has an exact-count table and accessible lifecycle table. The interface
shows rates with their denominators, date/timezone coverage, error/retry and empty states.
It does not claim current-state distribution is complete historical conversion evidence.
# CRM search and institution downloads

After `uv run alembic upgrade head`, run `uv run python -m src.scripts.reindex_names`
to populate known names from the latest historical application and rebuild lookup tokens.
The command commits batches of 200 inquiries, is rerunnable, and prints counts only.
Run it again after rotating `PHONE_HASH_KEY` (phone hashes also require their existing
separate rotation procedure). New application submissions update the encrypted known
name and its blind prefix index atomically; removing/changing a name clears/rebuilds it.
The maintenance backfill can restore an absent known name from an existing application.

`POST /api/staff/leads/search` accepts `query`, `status`, `course_id`, `offset`. Name
words match prefixes of at least two Unicode characters; combining marks are retained.
Phone search requires a full international number beginning with `+`; no contact is
invented for Telegram users. Query text is excluded from URLs/audit details. Lookup
tokens are tenant-keyed HMACs, not plaintext. As with any blind prefix index, within-tenant
prefix equality/length information is visible to a database reader; protect the hash key
separately from the database. Bulk SQL name changes must rebuild the index explicitly.

`POST /api/staff/exports` is administrator-only and accepts `dataset` (`leads`,
`applications`, `payments`) and `format` (`csv`, `xlsx`). Inquiry exports also accept
the search/status/course filters. Downloads are access-audited and `no-store`. CSV
neutralizes formula prefixes and Excel forces string cells. `STAFF_EXPORT_MAX_ROWS`
defaults to 10,000; oversized exports fail rather than silently dropping rows. Application
exports include submitted form fields; payment amounts are database minor units. No
lookup tokens, ciphertext, webhook payloads or payment URLs are exported.

Rollback: stop processes using the new model, downgrade to `e31b0847c629`, then run
the previous release. The downgrade drops only the regenerable name index; known
encrypted names/application forms remain intact.
# Outbound integrations and live notifications

Upgrade to `6dd017583606`. Include `src.tasks.integrations` in the TaskIQ worker's
module list alongside Telegram, knowledge and follow-ups. The API dispatches committed
webhook work every three seconds when `INTEGRATION_RECOVERY_ENABLED=true`; the scheduler
also recovers it. Configuration is optional: no endpoint means no external deliveries.
The dashboard's administrator-only Outbound webhooks page configures a public HTTPS
destination and shows delivery status. URL/signing secrets are encrypted. A newly created
or rotated signing secret is returned once; later reads expose only the hostname.

Signatures cover `timestamp + "." + exact_body_bytes` with HMAC-SHA256, using the
shown signing secret as UTF-8 bytes. Headers are `X-AdmitFlow-Timestamp`,
`X-AdmitFlow-Signature: v1=<hex digest>` and `X-AdmitFlow-Delivery`. Receivers must
verify the signature in constant time, reject stale request timestamps, and durably
deduplicate the delivery ID before side effects. Retries preserve the delivery/event
IDs and body, but sign a fresh attempt timestamp. Events can be duplicated or arrive
out of order; they contain type, institution/inquiry references, state and event time,
never names, phone numbers, conversation text or arbitrary audit details.

Six delivery attempts are allowed, with bounded exponential backoff. A crashed lease
is recoverable and may replay a received request. Redirects and permanent 4xx responses
(except 408/429) become dead deliveries; transient failures retry. Destinations resolve
again for each attempt, reject any nonpublic address, and pin the selected IP while
preserving TLS hostname/certificate checks. Proxies and redirects are disabled, response
bodies are not consumed, and an overall deadline bounds the attempt. HTTP traces for
the delivery's async context are suppressed so URL paths/query credentials cannot leak.
Saving configuration cancels older queued/leased work; an in-flight request may arrive.
Older events are not replayed into a newly configured destination.

Notifications use a same-origin authenticated WebSocket at
`/api/staff/notifications/ws` through the Next.js proxy. Origin, session expiry and
active-account checks are enforced; snapshots refresh every two seconds without holding
an idle database transaction. Qualified inquiries, failed/uncertain Telegram deliveries,
reviewable co-pilot drafts and confirmed payments produce notifications in the source
transaction. Read receipts belong to each staff account, and unread events are shown
first so backlogs larger than 50 remain accessible. Read/access audit events never
generate another notification or webhook. The HTTP snapshot/read routes support recovery.

Rollback: stop the new API/worker/scheduler, downgrade to `a82df107e436`, then start the
previous release. This removes endpoint configuration, integration delivery history and
notification receipts, while preserving source audit/domain records. Event, delivery and
read-receipt rows cascade with their inquiry; no new student text is retained here.

# Staff access and privacy operations

Upgrade to `c4817a02f59d` before running this source. Administrators manage institution
staff at `/api/staff/users`; new/reset credentials permit only private password setup,
identity lookup and logout. `POST /api/staff/password` verifies the current password,
revokes old sessions and issues a new cookie. Role changes and deactivation revoke
sessions; concurrent changes preserve an active administrator with a private password.
Initial passwords are shared manually; there is no email invitation delivery service.

`DELETE /api/staff/leads/{id}` requires an administrator, browser-write protection
and JSON `confirm_id` equal to the inquiry UUID. It permanently erases the linked
inquiry data graph. Active provider operations return conflict until they settle;
outbound claims serialize against deletion. The audit receipt retains the staff actor
and reason without a student reference. External providers/backups are outside this
logical erasure; deleting an inquiry does not release enrolled seats.

`uv run python -m src.scripts.scheduler --once` runs history retention independently
of queue dispatch. Run without `--once` for the continuous scheduler. An institution's
optional retention period uses last inbound/outbound activity or creation, skips active
work, expires history/facts/memory, cancels reminder consent and invalidates pending
payment-creation consent. It preserves inquiry identity, applications and financial
records. Full deletion is a separate explicit administrator action.

Rollback: stop current API/worker/scheduler, downgrade to `6dd017583606`, then run
the previous source. The password migration disables setup-only accounts and revokes
their sessions before removing that guard; the history marker is regenerable.
Downgrading does not restore erased data; recovery requires an appropriate backup.

# Typed OpenAI decisions and required reranking

`src/decision/decide()` validates typed OpenAI interpretation/extraction and rejects
refusal or invalid output. No fine-tuning, distillation or separate model service is
required. Eligibility, readiness state, money and authorization remain code-owned.

Both Telegram FAQ and authenticated document search rerank up to twelve approved,
relevance-filtered tenant passages, then select five original passages. The structured
ranking must contain exactly the supplied IDs once each. `KNOWLEDGE_RERANK_TIMEOUT_SECONDS`
(default 8) bounds the entire added model operation; invalid output, refusal or outage
preserves baseline order. Existing relevance floors, injection filtering, exact-source
quotation and abstention still apply. The compatibility hybrid helper is not this path.

Run `uv run python -m src.scripts.evaluate_reranking` for four bounded multilingual
synthetic ranking cases, and `uv run python -m src.scripts.evaluate_faq` for the
24-case source/abstention check. These make paid OpenAI calls but no Telegram sends or
database writes. Reports are saved under `docs/event/`; they do not establish broad
fluency or production latency. CI uses mocked models and disposable test databases.

# Isolated full-stack Compose

See [the runtime runbook](../docs/engineering/COMPOSE_RUNTIME.md). From backend,
`uv run python -m src.scripts.configure_compose` exclusively creates a private root
configuration. Then run `docker compose up --build -d --wait` from the root. The UI
uses loopback port 13000 and the API uses 18000; internal data services have no host
ports. This is a separate synthetic database, not the existing native demo data.

`uv run python scripts/verify_compose.py --restart` verifies persisted login credentials,
API proxy, authenticated notifications socket, actual queue/result and scheduler.
Telegram polling is opt-in through the `telegram` profile; use a separate bot or an
explicit database/checkpoint migration. Live OpenAI/Telegram keys are never copied.
Legacy WhatsApp ingress/jobs are off unless `LEGACY_WHATSAPP_ENABLED=true`; this
compatibility switch is not required for Telegram. Nondevelopment APIs force debug off.
