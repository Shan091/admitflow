# Local Telegram/OpenAI runtime

Use this repository and the existing plan. The event runtime is local. No cloud
account or additional AI provider is required. This runbook preserves existing volumes
and does not reset an institution or bot checkpoint.

## Configuration and data services

Install Python/uv, Node/npm and Docker Desktop. In `backend/`, copy `.env.example`
to `.env` if one does not already exist. Keep existing local configuration intact.
Set `OPENAI_API_KEY`, `TELEGRAM_BOT_TOKEN`, `PII_ENCRYPTION_KEY` and
`PHONE_HASH_KEY`. Generate the encryption key using the command in `.env.example`.
Use a separate random lookup/signing key. Never put credentials in frontend code.

For a new local data profile, copy `backend/readiness-db.env.example` to
`backend/.env.readiness-db`, choose a local database password, then set the matching
`DATABASE_URL` in `backend/.env`:

```text
DATABASE_URL=postgresql+asyncpg://admitflow_demo:YOUR_LOCAL_PASSWORD@127.0.0.1:5432/admitflow_demo
REDIS_URL=redis://127.0.0.1:6379/0
```

URL-encode reserved characters in the database password. From the repository root:

```bash
docker compose -f docs/event/readiness-services.yaml up -d --wait
```

The profile uses PostgreSQL with pgvector and Redis on loopback-only ports. If those
ports belong to another project, resolve that conflict instead of stopping unrelated
services. Do not delete volumes to retry application setup.

## Migrate and seed

From `backend/`:

```bash
uv sync --frozen
uv run alembic upgrade head
uv run python -m src.scripts.seed_demo
```

The idempotent seed creates a synthetic institution (`TELEGRAM_INSTITUTION_CODE`,
default `demo`), courses, available batches and age/marks rules. It writes a randomly
generated administrator password to ignored `.demo-credentials.json` only when
creating the demo account. It never prints or overwrites the password. Existing
staff accounts retain their credentials. For a real approved institution, use the
separate manual provisioning command documented in backend/README.md.

## Run the processes

Use separate terminals. The first three commands run from `backend/`:

```bash
uv run uvicorn src.main:app --host 127.0.0.1 --port 8000
uv run taskiq worker src.tasks.broker:broker src.tasks.telegram src.tasks.knowledge --workers 1
uv run python -m src.telegram.receiver --institution-code demo
```

From `frontend/`:

```bash
npm ci
npm run dev
```

Open `http://127.0.0.1:3000` and use the local demo credentials. The API proxies through
the same frontend origin. `BACKEND_URL` defaults to `http://127.0.0.1:8000`.
The receiver verifies the configured bot, refuses an existing webhook, binds the bot
to its institution, and takes a per-bot advisory lock. Only one receiver may run per bot.
Multiple institutions require separately provisioned bots and receiver configuration.

The API's `/health` is liveness. `/ready` checks PostgreSQL and Redis without external
model/Telegram calls. It does not prove a working handset journey or a calibrated model.
The debug enqueue route is unavailable outside development.

## Validate and recover

```bash
# From backend/; the OpenAI option makes bounded paid requests.
uv run python -m src.scripts.validate_services --openai --telegram
uv run python -m src.scripts.evaluate_live
uv run python -m src.scripts.evaluate_faq
uv run pytest -m integration
# From frontend/; requires local processes, seeded staff and an existing Telegram inquiry.
npm run test:e2e:live
```

`evaluate_live` makes five embedding searches, plus query-translation calls for
non-ASCII questions, against the uploaded synthetic campus reference. Do not run live
checks in ordinary CI. Synthetic tests use fake providers and disposable containers.
`evaluate_faq` runs 24 sequential cases across English, Hindi, Hinglish and Malayalam
through the actual FAQ answering function. It checks expected source quotations and
explicit abstention, writes docs/event/EVALUATION_RESULTS.json and exits nonzero for
any failed case. It uses only the fictional demo tenant, reads the database without
committing changes and sends no Telegram messages. It can make up to 24 embedding,
12 query-translation and 24 quotation-selection calls, with the configured provider
retry limits. Results do not establish fluency or broad relevance accuracy.
Default backend checks expect isolated live configuration as documented in backend/README.md.

Accepted events and polling checkpoints commit together. Queue outages preserve
pending inbox/outbox records. Keep the receiver running so it republishes pending
work. Processing locks one lead and commits state plus one validated reply atomically.
Restarting the worker does not reset facts or create another lead.

Replies have queued, sending, sent, failed and uncertain delivery states. A rejected
Telegram rate-limit response can retry a bounded number of times after the advertised
delay. A network timeout or interrupted sender can mean Telegram already delivered
the message. Such replies remain uncertain and are not blindly resent. Review them
against the handset before taking manual action. Current staff UI displays the status;
it does not offer an unreviewed resend button.

When rotating a bot token, update the ignored configuration and restart the receiver
so provisioning refreshes the encrypted database credential. HTTP logging redacts
Telegram token URLs. Do not enable raw provider debug logs around private content.

## Packaging and release limits

The backend Dockerfile includes the API, worker/receiver source and migrations, and
runs under a non-root account. A local build is:

```bash
docker build -t admitflow-local:validation backend
```

Production is a separate milestone: use HTTPS, `APP_ENV=prod`, `DEBUG=false`, explicit
allowed origins, secret management, database persistence/backups, restore/retention
checks and approved institution material. No cloud deployment, judge-accessible URL,
license selection or Git publication follows from a successful local demo.

The repository's `docs/event/BUILD_MANIFEST.json` fingerprints tested code and
configuration while excluding credentials and runtime data. Regenerate it with
`uv run python -m src.scripts.record_build` after final source changes.
