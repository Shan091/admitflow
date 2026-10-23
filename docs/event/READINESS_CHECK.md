# WhatsApp readiness check — October 22, 2026

Repository: `C:/Users/shanx/Documents/admitflow`, renamed from v1; same Git repository.
Baseline branch: `feat/engine-dispatcher`.
Baseline HEAD: `1076c2ff1abee7919124c94297328000daf2cd55`.
Initial checks: approximately 22:25–22:34 IST. This is an interim report, not a claim that an hour or the live journey has completed.

## Decision so far

**Live readiness not established.** Configuration is the first blocker. No real phone message, Meta delivery, Redis worker execution, course selection, cross-turn memory, or persisted lead has been verified. No implemented staff dashboard was found. Do not build broad event features before resolving these checks.

The user subsequently authorized local configuration. A git-ignored `backend/.env` was created without overwriting an existing file. Local PII keys and a webhook verify token were generated without displaying values. External credentials remain to be supplied locally. No external WhatsApp message has been sent.

## Evidence collected before configuration

| Check | Actual result |
| --- | --- |
| Git baseline | Branch and SHA above; existing tracked deletions and edits preserved. No commit, reset, checkout, restoration, staging, push, or merge performed. |
| Environment files | Neither root `.env` nor `backend/.env` existed initially. |
| Process configuration presence | Database/Redis URLs, PII keys, Meta app secret, webhook verify token, WhatsApp access token/phone number ID, provider API keys, model-role overrides, and public URL variables checked were absent. Defaults in Settings still exist; credential validity was not tested. |
| Local TCP ports | 5432, 6379, 8000, 3000, 8080 closed on IPv4 localhost at inspection; this does not rule out a remote deployment or alternate ports. |
| Docker | Initially no reachable daemon; after authorized Docker Desktop startup, `docker info --format '{{.ServerVersion}}'` returned `29.2.1`. |
| In-process `/health` | 200, `status=ok`, `env=dev`; no server or dependency connectivity implied. |
| In-process webhook GET | 500, `Webhook verify token not configured` (synthetic challenge/token). |
| In-process webhook POST | 500, `Meta app secret not configured` (empty synthetic body). |
| Dependency constructors | `InMemoryBroker`; database factory, Redis client, and WhatsApp sender raised their missing-configuration errors. |
| Graph navigation | CLI failed with `ModuleNotFoundError: graphify`. JSON fallback used exact graph vocabulary: whatsapp, webhook, worker, redis, dispatcher, engine, qualification. Stale graph points to plans/ADRs, not current runtime proof. No graph regeneration performed. |

Command for in-process probes: `backend/.venv/Scripts/python.exe -` from `backend`, using FastAPI `TestClient`, the broker type, and dependency factories. No configured external API calls were made. LiteLLM attempted to fetch its public price map, failed under sandbox networking, and used its local backup; provider connectivity remains untested.

## Fresh baseline quality gate

Command from repository root, in PowerShell:

```powershell
& 'C:/Program Files/Git/bin/bash.exe' backend/scripts/verify.sh
```

Initial sandbox attempt stopped on the uv cache access error. The approved rerun outside the sandbox completed:

```text
ruff: All checks passed!
format: 66 files already formatted
mypy: Success: no issues found in 36 source files
pytest: 106 passed, 4 deselected, 2 warnings in 12.06s
OK — all quality gates green.
```

Warnings: unawaited AsyncMock coroutines at `src/core/rag.py:70` and `:95` in `tests/unit/core/test_rag.py::test_ingest_document`. The default gate excludes real-database integration tests. No product source changed for this run; do not describe it as a Postgres/Redis/Meta integration pass.

## Source findings to reproduce before repair

- `backend/src/engine/dispatcher.py:116`: reads only `text.body`. Discovery emits `course_<UUID>` interactive buttons/list rows (`nodes/discovery.py:46`, `:53`), but the dispatcher has no interactive reply parsing/validation or selection path to set `current_course_id`. A course tap is therefore expected to redisplay discovery rather than select the course; this is source evidence, not a live-device observation.
- `backend/src/engine/dispatcher.py:43`: ascending message timestamp with `limit(20)` loads the oldest 20 messages, despite the recent-history comment.
- `backend/src/engine/dispatcher.py:159`: saves inbound messages; the inspected sender/nodes do not persist outbound messages. Complete conversational memory remains unproven.
- `backend/src/whatsapp/webhook.py:92`: catches queue/dedup errors and still returns 200. A Meta webhook 200 alone cannot prove processing or reply delivery.
- `backend/src/engine/dispatcher.py:204`: handoff text promises someone will arrive shortly without a verified staff service. Do not present this as an operational handoff.

These are pre-existing findings. At initial inspection no application repair had been made; the later scoped worker repair is recorded below. First unblock configuration and a single real text roundtrip, then reproduce course selection with a failing test before the smallest scoped repair. Do not claim memory, tenant isolation, guardrails, or handoff are complete based on the baseline gate.

## Setup and bounded repair checkpoint (approximately 22:52 IST)

The user confirmed an existing Meta test app, selected OpenAI, and entered credentials in the ignored local file. Presence checks printed booleans only. Read-only Meta phone lookup returned HTTP 200; OpenAI model lookup confirmed access to `gpt-4.1-mini`. No live generation or phone delivery is implied by model lookup. Model compatibility reference: [official OpenAI model page](https://developers.openai.com/api/docs/models/gpt-4.1-mini), opened this session.

Local setup performed after authorization:

- Docker Desktop started. Cached `pgvector/pgvector:pg16` and `redis:7-alpine` images started with `docker compose -f docs/event/readiness-services.yaml up -d --wait`; both healthy. Only loopback ports 5432/6379 exposed. New named PostgreSQL volume; no existing data reused or deleted.
- Dedicated database initially had zero public tables. Both Alembic revisions applied: `64cfce85009d` then `c470f1ebc811`. Downgrade and all other Postgres integration tests have not been run.
- Synthetic institution, `Demo Computer Science`, `Synthetic October Demo` batch with 20 seats, and illustrative age >=17 rule persisted. These are not real institution offers. Tenant UUID: `717770d3-b072-4b9d-aae9-9ebd8e300165`; course UUID: `4f1fdbf2-65e3-485a-92b4-065bea8eccc5`.
- Actual worker initially crashed after approximately five idle seconds with `redis.exceptions.TimeoutError` in `ListQueueBroker.listen()` / `BRPOP`. A new real-Redis regression failed with that error (1 failed in 7.31s). Minimal repair: queue broker `socket_timeout=None`; other Redis client/result-backend behavior unchanged. Same regression passed (1 passed in 6.99s).
- Repaired separate TaskIQ worker consumed a synthetic ping through real Redis and returned the expected result in **0.221s**. This is a worker smoke check, not WhatsApp latency.
- Added a temporary webhook-only ASGI entry point, `scripts.readiness_webhook:app`, reusing the existing webhook and broker lifespan. Tests cover other-route 404s, challenge verification, wrong-token rejection, and missing-signature rejection. The normal API remains loopback-only.
- Temporary Cloudflare quick tunnel points to the webhook-only entry point. Public HTTPS challenge returned 200 with matching synthetic challenge; `/debug/enqueue-ping` returned 404; unsigned POST returned 401. This is not Meta subscription or device-delivery evidence.
- User was asked to configure the callback, subscribe to `messages`, and send a synthetic inquiry from the allowed demo phone. Actual ingress/delivery still pending at this checkpoint.

Post-repair gate: **112 passed, 5 integration tests deselected, 2 warnings**, 69 files formatted, mypy clean across 36 source files. Same two pre-existing RAG AsyncMock warnings. The gate was run with the ignored `.env` temporarily moved to `.env.readiness-running` and restored in `finally`, because existing tests assume no configured Redis broker. Live services had already loaded their configuration. Do not run the default tests with live credentials injected or mistake integration deselection for a pass.

Current local processes started in this session:

```text
API: python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --env-file .env --no-access-log
Worker: uv run --no-sync --env-file .env taskiq worker --workers 1 src.tasks.broker:broker src.tasks.processing
Tunnel origin: python -m uvicorn scripts.readiness_webhook:app --host 127.0.0.1 --port 8001 --env-file .env --no-access-log
Tunnel: cloudflared tunnel --url http://127.0.0.1:8001 --no-autoupdate
```

Run from `backend` except cloudflared. `--env-file .env` is necessary to export provider keys to LiteLLM. The callback hostname is temporary; reconnecting may change it. The tunnel has no uptime guarantee and is not a production deployment. Keep generated PII keys stable for the local data; do not overwrite them on restart. Database and application secrets are in ignored `.env` / `.env.readiness-db`, never in this report.

## Live checkpoint (approximately 22:54 IST)

This check has used approximately half of its one-hour budget; it has not passed or exhausted the hour. The remaining dependency is the user's Meta callback/subscription configuration and actual phone message. Do not claim completion from elapsed time or substitute synthetic webhook traffic for phone ingress.

Callback currently requested: `https://warm-headers-live-classroom.trycloudflare.com/api/webhook`. User should use the local `WHATSAPP_VERIFY_TOKEN` value, subscribe to `messages`, then send `Hi, show me courses` from the allowed demo phone. Verification token values must never appear in reports. The user has confirmed credentials were saved; callback setup/message sending has not yet been confirmed.

Last tenant-scoped counts: **0 leads, 0 messages, 0 lead facts**. The repaired worker remained listening and executed the ping without another idle timeout in observed logs. No application phone message has been sent by the assistant.

Review of the scoped diff found no new critical/important issues: blocking timeout change is confined to the dedicated queue pool; integration test uses a unique queue and removes only its own data; tunnel app has only the existing signed webhook. Pre-existing findings above remain open. Existing user deletions and edits remain preserved; no commit or PR made. `graphify update .` was attempted after code changes and failed with the same missing-package error; the graph remains stale, with no rebuild claimed.

Next step on user reply: confirm real ingress and separate worker execution, then phone delivery/latency. If discovery returns a course button, ask the user to tap it and inspect the actual stored `current_course_id`; expect the recorded parsing gap to require a small test-first repair. Do not implement an event feature or invent surprise compliance while waiting. Repair estimates: course selection likely one small dispatcher/test change after reproduction; complete outbound memory and safe operational handoff require separate evidence and scoping. No reliable total ETA until the first live attempt.

## Next live checks and evidence required

### Missing-reply investigation (approximately 22:59 IST)

The user reported no reply. All four local service ports (5432, 6379, 8000, 8001) were open; tunnel and worker processes remained running. The worker log recorded `process_inbound_message` task `cb453d4d666944c4b22b09d776983bd1` at 22:58:24, followed by a warning that the payload phone-number ID had no matching institution. The received ID is the placeholder used in Meta's sample webhook event, rather than the configured sender. No tenant remapping or fake institution was added to accommodate this sample.

Sanitized inspection confirmed that the configured WhatsApp sender still matches the seeded synthetic tenant; that tenant had 0 leads, 0 messages, 0 facts. Redis queue depth was 0 and one webhook dedup key existed. This establishes webhook ingress and worker dispatch for a **Meta sample event**, not actual-phone ingress or reply delivery. The sample exits before LLM calls or sending.

The user was asked whether they used the Meta Test button or the actual phone, and to send a real inquiry from the allowed recipient phone to the test business number shown in WhatsApp API Setup. Await that actual message before changing application logic. Do not describe this sample as the real roundtrip.

### WhatsApp Business Tools MCP connection

The user reported that the Meta app is unpublished and requested use of Meta's WhatsApp Business Tools MCP, providing its setup documentation. Unpublished status has not yet been independently established as the cause of missing phone ingress. The connector can help inspect actual account and subscription setup; no publication or registration change has been performed.

No `whatsapp_biz_` tools were available in this session's catalog. The installed Codex CLI was located and used, with approved access to Codex configuration, to add `whatsapp_business_tools` at `https://mcp.facebook.com/whatsapp_business_tools`. CLI output confirmed the server was added and OAuth started, then **Successfully logged in** (exit 0). Authentication completed, but a fresh tool-catalog check still showed no WhatsApp tools in this running session. Reload/restart Codex to load them before inspecting assets. Do not save OAuth authorization links, state, codes, or tokens in event documents.

After connection, start with read-only business/account/phone discovery, inspect app/WABA subscriptions, and verify that the configured phone matches the local synthetic tenant. Only then make the smallest necessary webhook subscription/configuration repair within the user's authorized demo setup. Tool availability may require refreshing or restarting the client. Keep account changes and any real messaging evidence distinct from the earlier Meta sample event.

1. Configure a confirmed Meta test app/number and provider locally; establish test-recipient access. Never record secret values here.
2. Start dedicated local PostgreSQL with pgvector and Redis; check migrations before touching data. Use only synthetic institution/catalog/persona records.
3. Start API and explicitly register `src.tasks.processing` with the worker. Ensure provider keys reach the process environment, not only Settings (provider keys are not Settings fields).
4. Configure a public HTTPS webhook at `/api/webhook` and the messages subscription. Confirm the tunnel points to this checkout. Inspect public exposure first: `/debug/enqueue-ping` currently lacks auth.
5. User sends one real message from the demo phone; record sanitized ingress/queue/worker/send/delivery evidence and elapsed latency.
6. Tap a seeded course, continue with earlier facts, inspect tenant-scoped lead/course/fact/message persistence. A DB inspection is not a finished dashboard.
7. At the one-hour boundary, record pass/fail/blocker and a bounded repair estimate. Do not spend the hour waiting without reporting.

## Delivery diagnosis and configuration repair (October 23, approximately 00:16 IST)

- User requested continuing with the Meta test number and authorized configuration repairs and test sends. App `agent` is now confirmed published.
- Direct app-token subscription inspection showed the current tunnel callback had an unnecessary trailing slash. Saved the canonical callback `https://approximately-singer-tex-travelers.trycloudflare.com/api/webhook`, preserving all existing subscribed fields. Meta returned success; public challenge verification matched.
- The configured sender was confirmed to belong to the test account identified by the local token's granular scopes. That account was subscribed to `Otohom_Test_Env` and Meta's test app, but not `agent`. Added `agent` and read back its subscription successfully. Other subscriptions were preserved.
- Earlier absence of delivery logs was inconclusive: the existing webhook explicitly discards status events. Added authenticated, sanitized status logging only to the temporary readiness entry point. It records the state, a hashed message reference, and numeric error codes; no phone numbers, payloads, error text, or tokens. Regression first failed for the missing log, then all 8 focused tests passed, including invalid-signature and PII-exclusion checks.
- Restarted the webhook origin and worker with host network access and provider environment loaded. Removed the confirmed obsolete worker process tree. The new worker logged `Listening started`. No inbound learner journey has yet been verified.
- A fresh `hello_world` send was accepted by Meta, followed by a signed failure webhook: `status=failed`, error **131031**. This establishes account-to-app routing and signed status reception, not handset delivery.
- Direct Meta account and phone `health_status` reads confirmed overall sending **BLOCKED**: account error **141014**, account banned. Meta prescribed an appeal at `https://business.facebook.com/accountquality`. The phone and app themselves were reported available. Other health flags reported payment-method error 141006 and unverified business 141010; those are secondary observations, not proof that adding payment details would clear the ban on this test account.
- Stop further test sends while the restriction remains. User action in Meta Business Support Home is required; no appeal submitted, payment method added, replacement account created, or ban bypass attempted. Local configuration cannot clear Meta's account restriction.
- Live readiness remains failed/blocked on Meta account access. Course selection, memory, persisted live lead, and actual phone delivery remain unverified.
- Full gate passed after this change: lint clean, 69 files formatted, strict mypy clean across 36 source files, **114 passed, 5 integration tests deselected, 2 existing RAG AsyncMock warnings**. Live `.env` was temporarily isolated and restored in `finally`; services retained their startup configuration. Scoped adversarial review found no new important/critical issue: status logging occurs only after signed route acceptance and excludes phone/payload/error text. `graphify update .` still fails with the existing missing-module error; graph remains stale. No commit or PR made.

## New test account configuration (October 23, approximately 09:45 IST)

The user switched local credentials to another test sender and completed the new business profile. Meta's account name is `Test Messaging Account`, account review `APPROVED`; new business ID `2155291628698538`, new app ID `28915484464739225`. Initial incomplete-profile error 131000 cleared on recheck. Health still reported sending BLOCKED, payment-method flag 141006 and business verification flag 141010; no card was added and these flags were not assumed to explain delivery without a real event.

The new app had neither a WhatsApp callback nor an account subscription. The old tunnel hostname no longer resolved. Reloaded the webhook receiver with the new local app secret, created a fresh tunnel, verified its challenge and saved the new callback plus `messages` field. Added the new app's test-account subscription. Meta confirmed both saves. Current callback is `https://lopez-monitor-lets-sections.trycloudflare.com/api/webhook`. Local DNS lagged; public DNS resolved and a TLS-verified request through its public address passed; Meta independently verified the callback on save.

One authorized `hello_world` send was accepted, then the receiver logged a signed failure event: `status=failed`, code **131031**, hashed reference `492f149c905f`. Therefore the new app's status routing works, but handset delivery remains blocked by Meta. Completing the business profile did not establish sending readiness. No billing changes, account creation, or appeal submission were performed. The worker/tenant live learner journey has not been migrated or verified for this new sender; default gate result above covers the last code change, not this external configuration.

## Final Postman retry (October 23)

The user requested one final Postman attempt and then explicitly requested that the assistant execute all setup. Newman 6 was installed in a temporary directory; no application dependency or desktop app was installed. The imported diagnostic collection ran using local credentials in memory through `backend/scripts/run_postman_check.cjs`, with sanitized output only. Public callback challenge passed before sending. Health returned HTTP 200, overall BLOCKED, account 141006 and business 141010. Exactly one fresh send was accepted (HTTP 200), followed by a signed **failed** event with **131031**, hashed reference `f3fc27bca826`. This is confirmed Meta delivery rejection, not an unobserved callback or Postman transport problem. No more sends planned while restricted. Full steps and limitations: [POSTMAN_CHECK.md](POSTMAN_CHECK.md).

## Prior-work disclosure draft

We are continuing an existing AdmitFlow prototype at `1076c2ff1abee7919124c94297328000daf2cd55`, with existing FastAPI webhook, TaskIQ wiring, database models/migrations, sender, dispatcher, discovery, qualification, and RAG code. Before the event, the default local quality gate passed (106 tests); real WhatsApp delivery, course selection, memory, persistence, and a staff dashboard were not yet demonstrated. We will disclose any later pre-event repairs separately. The surprise requirement is unknown and will be implemented during the event after it is announced. Confirm the prototype exception and permitted scope with organizers; no organizer contact has been made.
