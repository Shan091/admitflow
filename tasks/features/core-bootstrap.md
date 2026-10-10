# Feature: Core bootstrap

## Outcome

Provide a runnable FastAPI + SQLite base for the Telegram feature.

## Acceptance criteria

- [ ] Python 3.12 dependencies install from `uv.lock`.
- [ ] `GET /health` returns `{"status":"ok"}`.
- [ ] SQLite schema initializes and fictional demo catalog seeds idempotently.
- [ ] Settings load from environment; no credentials are stored in Git.
- [ ] README run/check commands match actual project commands.

## Implementation slices

- [ ] Add project configuration, app entrypoint, settings, seed data, SQLite repository, and
  health route.
- [ ] Add the baseline verify script and CI workflow.
- [ ] Run install, health, and quality checks; record actual results.

## Verification

- [ ] `uv sync --python 3.12`
- [ ] Start the app and request `/health`.
- [ ] `bash scripts/verify.sh`

## Risks and limitations

- The hosted Telegram and OpenAI integrations require user-provided credentials; automated tests
  must not require them.
