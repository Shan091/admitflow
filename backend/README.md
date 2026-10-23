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
