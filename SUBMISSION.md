# Project submission

## Project

- **Project name:** AdmitFlow
- **Short description:** A Telegram admissions assistant that remembers inquiries, checks
  seeded eligibility rules in code, and answers institution FAQs with fail-closed vector search.
- **Code repository URL:** https://github.com/Shan091/admitflow
- **Final implementation commit SHA:** `634579532c8b77ae9f0f8c6da86cb137f9f095d8` (code milestone)
- **Working demo:** Local dashboard and `/health` run without credentials. Live Telegram bot
  username and walkthrough are pending bot-token setup and a real rehearsal.
- **Demo access requirements:** Telegram account; local `.env` with a bot token and OpenAI API key
  for live bot and FAQ retrieval. Do not include credential values.

## Participants

| Participant name | GitHub handle | Contribution |
| --- | --- | --- |
| TODO | TODO | TODO |

## Run and demonstrate

- **Prerequisites and versions:** Python 3.12.5, uv 0.11.2 (verified locally)
- **Install command:** `uv sync --python 3.12`
- **Required environment variables:** `TELEGRAM_BOT_TOKEN`, `OPENAI_API_KEY`, optional
  `OPENAI_DECISIONS_MODEL`, `OPENAI_EMBEDDING_MODEL`, `DATABASE_PATH`
- **Start command:** `uv run uvicorn admitflow.main:app --reload`
- **Demo walkthrough:** Pending live Telegram setup and rehearsal; see the local-only verification
  steps in `README.md`.
- **Checks performed and results:** `uv sync --locked --python 3.12` and
  `uv lock --check --python 3.12` passed. Latest local `bash scripts/verify.sh` passed (Ruff lint,
  formatting, strict mypy, and 25 pytest tests); a local Uvicorn smoke check returned `/health`
  `200` and dashboard `200`; `git diff --check` passed. GitHub Actions passed on code commit
  `634579532c8b77ae9f0f8c6da86cb137f9f095d8` (24 tests); follow-up check is pending push.
- **Live integration checks:** Not run; `OPENAI_API_KEY` and `TELEGRAM_BOT_TOKEN` are not configured
  in this environment. Automated tests use local SQLite and fake embeddings; no API credits spent.
- **Known limitations:** Single fictional tenant, seeded FAQ corpus, local dashboard, no payments,
  uploads, production hosting, authentication, privacy/retention controls, or real admission
  decisions. Demo chat identifiers and messages are stored locally; use fictional test inputs only.
- **Libraries and APIs:** FastAPI, python-telegram-bot, OpenAI API (`gpt-6-luna`,
  `text-embedding-3-small`), SQLite, NumPy; link exact references in `docs/DECISIONS.md`.
- **AI usage:** `AI_USAGE.md`
- **Development log:** `CHANGELOG.md`
