# AdmitFlow

An admissions-engagement platform for institutions. Students explore courses,
ask questions and share eligibility information through Telegram. Staff inspect
persisted inquiries, conversation context and code-evaluated eligibility results.

## Product scope

The first release covers Telegram onboarding and language preference, course/batch
selection, qualification, memory/corrections, grounded institution FAQs and a minimal
authenticated staff dashboard with a human-request queue. The full roadmap also
includes applications, payments, co-pilot, follow-ups and institution administration.

The current implementation also includes encrypted application submission/review,
catalog/settings/discount management, payment monitoring and safe reconciliation.
Staff takeover/co-pilot, consent-aware follow-ups, analytics/exports, signed webhooks,
live notifications, staff accounts, erasure and retention are implemented. Staff transcripts
include standalone deliveries and stable pagination. Real Razorpay test-card validation
and public deployment remain unverified; staff-reply and uploaded-PDF handset receipt
are confirmed. Deployment is deferred until the owner explicitly authorizes it;
see [tasks/todo.md](tasks/todo.md) for verified acceptance and remaining work.

## Stack

Python/FastAPI/Pydantic, PostgreSQL/SQLAlchemy/Alembic/pgvector, Redis/TaskIQ,
OpenAI and Next.js/TypeScript. Digital PDF structure uses offline CPU Docling
layout/table models, isolated in a bounded child process and dedicated serial worker. Only necessary
services are required; additional AI providers and sponsor infrastructure are optional.
Business rules, prices and authorization remain code-owned.

## Current status

The backend foundation, AI/domain modules and Telegram identity migration exist.
The identity change has passed the backend gate and separate PostgreSQL migration/
isolation tests. Institution staff can now upload individual files/folders, index digital
PDF/DOCX/text, inspect status, retry/delete and search source passages. The Telegram
adapter and staff inquiry/request screens are implemented. A real user confirmed
Telegram replies, and the same inquiry persists in the authenticated staff workspace.
Live OpenAI structured output, embeddings, document indexing and search have passed.
After replacing an invalid key, live credential probes pass again and the expanded
24-case multilingual FAQ evaluation passes. Results use synthetic reference material;
they are not a fluency or production-readiness claim.
Live corrections, sourced/unsupported answers and the user-requested staff workflow
have passed selected checks. Language wording has agent review, as requested;
human/native fluency and real-applicant outcomes remain unvalidated.
Synthetic data is used for development/demonstrations.

Follow the existing [plan](tasks/plan.md) and [task list](tasks/todo.md) for progress,
[specification](SPEC.md) for behavior, [ADR-012](docs/decisions/ADR-012-telegram-openai-mvp.md)
for the active stack decision, and [backend instructions](backend/README.md) for setup.

## Development

Read [AGENTS.md](AGENTS.md) and the [development lifecycle](docs/engineering/development-lifecycle.md).

```bash
cd backend
uv sync
uv run uvicorn src.main:app --reload
bash scripts/verify.sh
```

Use ignored local configuration for secrets. Current test instructions and known
environment assumptions are in the backend README. These commands start the
backend. Full receiver/worker/demo setup is in the backend README below.

For document ingestion, follow the [knowledge workspace setup](backend/README.md#institution-knowledge-workspace).
Prepare the offline PDF assets and run the API, interactive worker and separate
serial knowledge worker following the [document runbook](docs/engineering/DOCUMENT_INGESTION.md).
Provision an administrator, then start the frontend:

```bash
cd frontend
npm ci
npm run dev
```

Open `http://127.0.0.1:3000`. Choose files or a folder, wait for Ready, then search.
Supported formats: digital PDF, DOCX, TXT, Markdown and CSV. Scanned PDFs need a
searchable replacement. Live indexing/search requires an OpenAI API key; automated
tests substitute synthetic embeddings. Original files are encrypted; extracted reference
text is stored in the institution-scoped database. Upload institution reference material,
not applicant personal files. OpenAI remains the decision, embedding and reranking provider;
no fine-tuning or extra hosted inference service is required.

## Demonstration and submission

Local workspace: `http://127.0.0.1:3000`. Demo staff credentials are in the ignored
`backend/.demo-credentials.json` created by the seed command. Do not publish it.
The configured Telegram demonstration bot is `https://t.me/mike0011_bot`; it requires
the local receiver/worker and is not an independently hosted service.

Use the [demo script](docs/event/DEMO_SCRIPT.md), [six-slide deck copy](docs/event/PITCH_DECK.md)
and [AI Impact Statement](docs/event/AI_IMPACT_STATEMENT.md). The editable
[six-slide PowerPoint](docs/event/artifacts/admitflow-pitch-final.pptx) is ready locally. The actual local [staff walkthrough](docs/event/artifacts/staff-walkthrough.webm) is recorded;
the longer [saved student journey](docs/event/artifacts/student-to-staff-walkthrough.webm)
shows corrections, sourced answers and the staff request in the actual dashboard;
the final handset/event video and public demo link remain pending. Artifact requirements and outstanding
organizer inputs are in [submission requirements](docs/event/SUBMISSION_PLAN.md).
Prior work and verification evidence are preserved in repository records.
Owner: **shan**. Project source is licensed under [MIT](LICENSE); third-party
code, models and event materials retain their own terms. See [data/model provenance](docs/event/DATA_PROVENANCE.md).

The [prior-work disclosure](docs/event/PRIOR_WORK_DISCLOSURE.md),
[language review packet](docs/event/LANGUAGE_REVIEW.md) and
[expanded evaluation results](docs/event/EVALUATION_RESULTS.json) record remaining
review and verification limits. The source-display update passes 252 default tests
and 16 affected PostgreSQL cases; the preceding full build passes
87 PostgreSQL tests and two separate Redis checks, plus strict typing and frontend
lint/build. The [live PDF report](docs/event/DOCUMENT_PIPELINE_RESULTS.json) verifies
upload, dedicated worker, Docling, OpenAI embeddings and programme-specific search.
Its temporary synthetic upload was removed; no Telegram message was sent by that check.
A separate retained synthetic counselling PDF produced a handset-confirmed Lotus Hall
answer. Student replies now contain the grounded answer without a citation footer;
source metadata remains encrypted internally and staff search retains its references.
See [handset evidence](docs/event/LIVE_HANDSET_RESULTS.json).
