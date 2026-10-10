# AdmitFlow

AdmitFlow is a hackathon demo of an admissions assistant. A student can explore a fictional
institution's courses in Telegram, answer eligibility questions evaluated by code, and ask
questions answered from seeded institution FAQs using OpenAI embeddings and local vector search.
Staff can inspect saved leads and conversations in a local read-only dashboard.

This is a demo using fictional sample data. Eligibility results are not real admission decisions.
Use fictional/demo answers only: Telegram user IDs, usernames, and chat messages are stored in the
local SQLite database. The staff dashboard is unauthenticated and intended for local demonstration.

## Requirements

- Python 3.12
- `uv`
- Telegram bot token for live Telegram interaction (optional for local dashboard/tests)
- OpenAI API key for Decisions API and embedding-backed FAQ answers (optional; RAG stays
  unavailable without it)

## Setup and run

```bash
uv sync --python 3.12
cp .env.example .env
# Add credentials to .env locally; never commit it.
uv run uvicorn admitflow.main:app --reload
```

Open `http://127.0.0.1:8000/` for the dashboard and `/health` for health status. Configure
`TELEGRAM_BOT_TOKEN` to start Telegram long-polling. Configure `OPENAI_API_KEY` to enable intent
routing and semantic FAQ search.

## Tests and checks

Run the same quality gate used by GitHub Actions before pushing:

```bash
bash scripts/verify.sh
```

The gate runs Ruff lint and format checks, strict mypy, and pytest. Automated tests use fake
Telegram updates, fake embeddings, and temporary SQLite databases; they do not call Telegram or
OpenAI and do not spend API credits. Live API checks are manual and must be reported separately.
CI runs on pushes and pull requests; its status applies to the exact commit shown by GitHub.

## Demo walkthrough

1. Send `/start` to the configured Telegram bot.
2. Choose a seeded course, answer the two qualification prompts, and view the code-computed result.
3. Ask a seeded FAQ question; if retrieval is unavailable or uncertain, the bot says so.
4. Open the local dashboard to view the same lead and conversation.

## Current status

Check `tasks/todo.md` for completion state. `CHANGELOG.md` and `SUBMISSION.md` contain only
checks actually performed. Payments, document uploads, deployment, and a production WhatsApp
integration are out of scope for this demo.
