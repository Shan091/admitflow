# AdmitFlow institution knowledge workspace

This is the initial staff surface for the existing roadmap. It supports institution
login, file/folder selection, ingestion status, retry/delete and source-passage search.
It also includes inquiry filters, selected course/batch and eligibility evidence,
ordered conversation history and the human-request queue. Staff can acknowledge,
resolve and explicitly resume automation. The same live Telegram inquiry is visible here.

Use the [backend setup](../backend/README.md#institution-knowledge-workspace) first:
migrate PostgreSQL, configure Redis/encryption/OpenAI, provision an administrator,
and run the API plus knowledge worker. From this directory:

```bash
npm ci
npm run dev
```

Open `http://127.0.0.1:3000`. API requests use a same-origin rewrite to
`BACKEND_URL`, defaulting to `http://127.0.0.1:8000`. If overriding the URL through
`.env.local`, restart Next.js and configure the backend's allowed browser origins.
Session cookies are HttpOnly; no credentials or tenant authority are stored in localStorage.
Never place API keys in a `NEXT_PUBLIC_` variable or browser code.

Administrators may upload/retry/remove; agents may view/search. File uploads and
folder selection preserve source paths. Larger folders are divided into batches of
25 files or 28 MiB; files are limited to 10 MiB. Successful earlier batches remain
saved when a later request fails. Identical bytes retain their original source path.
Visible pages refresh every four seconds. Search returns original passages and sources;
it does not generate an answer. Follow the backend README for supported formats,
scanned-PDF handling, processing recovery and sensitive-data restrictions.

The interface uses warm neutral surfaces, green actions, table-based document status,
inline deletion confirmation and responsive layouts. Typography is bundled DM Sans;
plain CSS keeps this initial surface small. The product requirements remain in
[SPEC.md](../SPEC.md), and progress stays in the existing plan/todo files.

```bash
npm run typecheck
npm run build
npm start
```

Browser acceptance includes synthetic API fixtures and a real Chrome test through
the Next.js proxy with the local backend, real OpenAI indexing/search and the persisted
Telegram inquiry at desktop/mobile widths. The real test requires local credentials
and an existing inquiry, makes paid embedding calls, and runs only when requested:

```bash
npm run lint
npm run test:e2e:live
```

The complete synthetic student-to-staff journey and tenant boundaries are tested in
`backend/tests/integration/test_telegram_journey.py`. Selected live correction,
source/abstention and human-request checks are verified in the existing task list.
`npm run record:demo -- --journey` records the actual staff view of that saved journey;
it sends no Telegram messages and protects existing recording files from overwrite.

The standalone nonroot container and internal build-time rewrite are described in
[COMPOSE_RUNTIME.md](../docs/engineering/COMPOSE_RUNTIME.md). Runtime secrets belong
to the backend; rebuilding the frontend is required when its rewrite target changes.
