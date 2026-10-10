# Feature: Core bootstrap

## Outcome

Provide a runnable FastAPI + SQLite base for the Telegram feature.

## Acceptance criteria

- [x] Python 3.12 dependencies install from `uv.lock`.
- [x] `GET /health` returns `{"status":"ok"}`.
- [x] SQLite schema initializes and fictional demo catalog seeds idempotently.
- [x] Settings load from environment; no credentials are stored in Git.
- [x] README run/check commands match actual project commands.

## Implementation slices

- [x] Add project configuration, app entrypoint, settings, seed data, SQLite repository, and
  health route.
- [x] Add the baseline verify script and CI workflow.
- [x] Run install, health, and quality checks; record actual results.

## Verification

- [x] `uv sync --locked --python 3.12`
- [x] Start the app and request `/health` (`200 OK`; dashboard also returned `200`).
- [x] `bash scripts/verify.sh`

## Risks and limitations

- The hosted Telegram and OpenAI integrations require user-provided credentials; automated tests
  must not require them.
