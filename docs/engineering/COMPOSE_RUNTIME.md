# Isolated local full-stack runtime

This profile uses the existing repository and synthetic institution seed. It does not
reuse the running readiness database, its volumes, its staff credentials or its bot
checkpoint. It is local development packaging, not a public production deployment.

From `backend/`, run:

```bash
uv run python -m src.scripts.configure_compose
```

This exclusively creates the ignored repository-root `.env` with fresh database,
application-encryption and lookup keys. It never reads/copies backend/.env and refuses
to overwrite any existing file. Keep this configuration with backups of its volumes;
changing encryption keys makes old encrypted records unreadable.

From the repository root:

```bash
docker compose config --quiet
docker compose up --build -d --wait
```

The default stack includes PostgreSQL/pgvector, persistent Redis, an idempotent
migration/seed job, API, TaskIQ worker, scheduler and standalone Next.js dashboard.
Only the API image builds the shared backend tag; other Python services reuse it.
Startup waits for healthy data services and successful migrations/seed. Data services
have no host ports. The dashboard is at http://127.0.0.1:13000; API readiness is at
http://127.0.0.1:18000/ready. Both host listeners are loopback-only. These ports avoid
the existing native development runtime on 3000/8000 and readiness data on 5432/6379.

Credentials are generated once inside a private named volume. To save a local copy:

```bash
docker compose cp bootstrap:/run/admitflow/.demo-credentials.json backend/.demo-compose-credentials.json
```

Treat that ignored file as a password. Do not paste it in chat, commit it or print it
into logs. Seed reruns preserve existing accounts/catalog and the credential file.
The development configuration intentionally leaves OpenAI and Telegram credentials
empty. Add only the credentials intended for this separate database if testing those
integrations, then recreate affected services. Model-dependent actions are unavailable
until configured; health/readiness does not claim a provider or handset journey.

The frontend's internal backend URL is baked into its rewrite during image build.
`BACKEND_URL` defaults to http://api:8000 in its Dockerfile; a different network target
requires rebuilding with the appropriate build argument. No API keys enter that image.
The production server runs as the unprivileged node user. Python services run as uid
10001. No source tree, developer credential file or Docker socket is mounted.

## Verification without provider calls

From `backend/`:

```bash
uv run python scripts/verify_compose.py
# Also prove stop/start preserves private credentials:
uv run python scripts/verify_compose.py --restart
```

This reads the isolated seed credential privately and checks the dashboard, authenticated
same-origin API proxy, session-protected WebSocket, database/Redis readiness, a real
TaskIQ ping/result roundtrip and a scheduler sweep. It does not call OpenAI, poll
Telegram, send a message or configure external webhooks. Unit/database/browser evidence
for the product remains separate from this packaging check.

## Explicit Telegram receiver

The receiver is in the `telegram` profile so starting a second local stack cannot
silently create a second poller for the existing bot. It uses the same image, database
and configured institution code as the stack:

```bash
docker compose --profile telegram up -d receiver
```

Do this only after configuring an institution-owned bot in the root `.env` and ensuring
that no other receiver uses it. Never point the existing active demo bot at a fresh
empty database: its independent checkpoint could consume updates from that bot. Use a
separate test bot or a deliberately planned migration of the actual database/checkpoint.
The service's configuration is validated separately from any live container poller.

## Stop and recover

```bash
docker compose stop
docker compose up -d --wait
```

Named volumes preserve database, Redis and synthetic credentials. Re-run the verification
after restart. Do not delete volumes as a startup repair. `docker compose down` removes
only this project's containers/network unless volume removal is explicitly requested;
never add a volume-removal option for existing data. The separate readiness profile and
native Telegram runtime are unaffected.

For real hosting, use the production readiness checklist after the remaining build
tasks; choose a destination, TLS domain, backups and secret store before deployment.
