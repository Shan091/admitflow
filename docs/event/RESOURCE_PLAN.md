# AdmitFlow necessary resources

Use the current [plan](../../tasks/plan.md). Telegram and OpenAI are selected; sponsor
resources are optional. No credits, provider comparison or infrastructure migration
is required merely because a resource is advertised.

| Resource | Use | Check before activation/use |
| --- | --- | --- |
| Telegram bot | Student private-chat channel | Create with verified BotFather; save token locally; validate bot and tenant mapping |
| OpenAI API | Interpretation, typed extraction, grounded replies, embeddings and required evidence reranking | Verify model access, schema compatibility, usage cap and actual outputs |
| Local PostgreSQL/pgvector + Redis | Persistent domain state, retrieval, queue/locks | Use isolated synthetic/test data and documented startup |
| Staff frontend | Login, leads, conversation and human-request queue | Serve authenticated API data with tenant isolation |
| Hosting, if selected | Stable receiver/API/worker/data and staff UI | Verify persistence, secrets, backup/rollback and ongoing cost |
| Mentors | Buyer/workflow/pilot feedback and concrete engineering questions | Record actual feedback; do not claim validation in advance |

OpenAI participant credits are advertised in the [event source](https://luma.com/StartupWeekendKochi).
Verify grant eligibility, activation, quota, expiry and continuation charges through
official channels. Keep keys/codes out of documents, logs, screenshots and Git.

The user-provided Neysa inference guide and other offers remain optional reference
material in [SOURCES.md](SOURCES.md). Neysa, SerpAPI, additional AI providers and model
decision-model self-hosting are not dependencies. Digital PDF parsing uses local
pretrained CPU layout/table weights inside the existing backend image; this adds no
hosted inference provider, training process or sponsor account. Use synthetic bounded smoke checks before any
approved paid batch, and measure actual usage, failures and latency.
