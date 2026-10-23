# AIBoomi Startup Weekend Kochi: fresh-session context

Updated: 2026-10-23, Asia/Kolkata.
Working repository: C:/Users/shanx/Documents/admitflow (renamed from v1; same repository and history).

## Latest decision: use v1 itself

### Newer user direction: Telegram and OpenAI (October 23)

The active student channel is now **Telegram instead of WhatsApp**. Use **OpenAI**
for AI; Neysa and other sponsor services are optional and unnecessary unless a
concrete need is established. This supersedes older statements below requiring
WhatsApp for the current build and the prior provider-comparison proposal.
Preserve historical WhatsApp evidence/code and the full institutional roadmap.
The user wants the current approach, stack, built features and gaps explained
before finalizing SPEC, tasks/plan.md and tasks/todo.md. The source audit and
proposed planning baseline are in [CURRENT_STATE.md](docs/event/CURRENT_STATE.md).
No Telegram adapter, bot connection or real Telegram journey has been established
by that audit. No product code or runtime configuration was changed.

Latest explicit user direction (October 23): **build the real institutional MVP in this admitflow repository and retain its full plan as the product roadmap**. Keep the active documentation focused on AdmitFlow itself, without comparisons to other folders. Preserve existing changes and deletions. The full roadmap is a staged objective; completion of every task during the hackathon is not claimed. Telegram is now the active channel as described above. The historical Meta restriction remains unresolved; do not repeat failed sends while restricted or claim WhatsApp live readiness.

Resource use is planned in [docs/event/RESOURCE_PLAN.md](docs/event/RESOURCE_PLAN.md). The public event page confirms $100 OpenAI API credits per participant plus Neysa infrastructure credits; the saved handbook also lists SerpAPI and mentors. Exact redemption terms, expiry and Neysa/SerpAPI allocations remain unverified. No credits have been redeemed or spent and no infrastructure provisioned by this planning update.

Continue in C:/Users/shanx/Documents/admitflow with its existing code and Git history. References to v1 mean this renamed repository. The earlier context-preservation-only request is superseded by the October 22 request to start the bounded real WhatsApp readiness check. No new repository has been created.

## Current readiness session (October 22)

Latest update (October 23): see READINESS_CHECK.md and docs/event/POSTMAN_CHECK.md before relying on the older checkpoint below. Meta restrictions prevented handset delivery on both the original and replacement test accounts. The replacement business profile is completed; new app callback and test-account subscription were repaired. Current temporary callback: `https://lopez-monitor-lets-sections.trycloudflare.com/api/webhook`; receiver verifies signatures and logs sanitized status/error codes. User authorized a final Postman retry, executed via a temporary Newman installation: HTTP 200 accepted, followed by a signed **failed / 131031** event (`f3fc27bca826` hashed reference). Health remains BLOCKED (account 141006, business 141010). No further test sends planned while restricted. Meta review/verification requires the user. Telegram was discussed as a fallback; no bot token, adapter, or live Telegram journey has been established. Default Python gate last passed 114 tests before these external configuration changes; Postman collection and runner checks are separate. Old runtime/tunnel hostnames and OAuth-tool-availability notes below are historical.

Latest connection checkpoint: WhatsApp Business Tools MCP added globally at `https://mcp.facebook.com/whatsapp_business_tools`; Meta OAuth completed successfully. The current session's tool catalog still lacks WhatsApp tools, so reload/restart Codex and resume here. First inspect business/account/phone state and webhook subscriptions. User suspects unpublished app status; this has not yet been verified as the cause. The only observed inbound event so far was Meta's sample payload, which did reach the worker but had no matching tenant. Do not claim a real roundtrip.

Read [docs/event/READINESS_CHECK.md](docs/event/READINESS_CHECK.md) for current evidence and restart commands. Initial baseline gate: 106 tests passed. After a minimal idle-worker repair and webhook-only tunnel entry point: 112 tests passed, 5 integration tests deselected, 2 warnings; a separate real-Redis regression passed. PostgreSQL/Redis are running, migrations applied, synthetic catalog seeded, and a separate worker ping succeeded in 0.221s. Meta/OpenAI read-only credential checks succeeded. Public webhook challenge succeeded; unsigned POSTs and debug exposure are rejected. The user was asked to configure the callback/messages subscription and send a demo-phone inquiry; no live ingress/reply or lead was observed at the checkpoint. Course-tap parsing remains a source-identified gap, memory remains unproven, no dashboard is claimed. Secrets are in ignored backend/.env, never this handoff or chat. Existing changes/deletions remain preserved. The surprise requirement remains unknown.

## User direction: applies from now on

- Work in this v1 repository.
- Keep all durable event context and handoff material inside this repository, not in .codex.
- Focus on this project and AIBoomi Startup Weekend Kochi. Do not bring unrelated projects or events into the handoff or future discussion.
- The submitted idea originally used WhatsApp; the user has now selected Telegram for the active build/demo.
- The exact application text has not been supplied. Do not invent it.
- The user wants to prepare before tomorrow's event and resume in a fresh conversation without lost context.

## Start here

Latest planning checkpoint (October 23, Friday evening):
[Submission plan](docs/event/SUBMISSION_PLAN.md) maps required deliverables, the
proposed inquiry-to-staff demo, resource use, provider evaluation and upload timing.
The user confirms no surprise requirement or revised deadline has been announced.
The Downloads PDF is a Neysa inference quickstart with hosted Gemma and Qwen
endpoints; it adds concrete inference resources, not new submission requirements.
Its Qwen sample has reasoning/truncation caveats. Browser-based demonstration is a
proposed fallback while Meta remains blocked, not an implemented or selected
replacement for WhatsApp. Root README and final submission assets remain to be
prepared. No product code, endpoint calls, redemption, deployment or submission was
performed for this planning checkpoint.

Read:

1. This file.
2. [Preparation plan](docs/event/PREPARATION_PLAN.md).
3. [Official sources and discrepancies](docs/event/SOURCES.md).
   [Resource plan](docs/event/RESOURCE_PLAN.md) maps the advertised resources to AdmitFlow tasks.
4. [AGENTS.md](AGENTS.md), [SPEC.md](SPEC.md), [tasks/todo.md](tasks/todo.md).
5. [Development lifecycle](docs/engineering/development-lifecycle.md) and relevant ADRs in docs/decisions/.

Some previously present product/workflow documents are currently deleted in the working tree. Do not restore them automatically or treat their old descriptions as current implementation. Respect the user's existing changes.

## Event sources and local copies

- Event page: https://luma.com/StartupWeekendKochi?tk=r54eXV
- Handbook: https://docs.google.com/document/d/1ZJV4q2CkU7fzwJ3WcHTjvRDfJgFInYV7AYT9BuDonFg/edit?tab=t.0
- Full handbook text: [docs/event/PARTICIPANT_HANDBOOK.txt](docs/event/PARTICIPANT_HANDBOOK.txt)
- Rendered event page text: [docs/event/EVENT_PAGE.txt](docs/event/EVENT_PAGE.txt)
- Source provenance/conflicts: [docs/event/SOURCES.md](docs/event/SOURCES.md)

Both pages were opened in a browser on 2026-10-22. Public Google Docs plain-text export succeeded. These local reference snapshots contain no credentials or private application text. Official updates at kickoff may supersede them.

## Verified event information

- AIBoomi Startup Weekend | Kochi, in person in Ernakulam/Kochi, Kerala.
- Event listing: Friday, October 23, 2026 at 4 PM through Saturday, October 24 at 4 PM.
- Advertised sprint: approximately 20 hours.
- Handbook submission deadline: Saturday, October 24 at 12 PM; portal locks.
- Handbook finale: Saturday 12-2 PM. Confirm the detailed schedule at kickoff.
- Solo or duo; maximum two people. Team roster locks after registration.
- The user's teammate situation is not known.
- Exact venue is hidden behind registration on the public listing. Do not invent an address.
- Public registration was closed at capture. The user says they are participating; do not infer they lack registration.
- Bring laptop/charger, phone, government ID, preferred extension, adapters/headphones, water, comfortable overnight clothing, and optional sleeping items.
- The handbook describes Wi-Fi, power, food/snacks, quiet zones, and mentors. Confirm operational details on site.

## Existing prototype rule and surprise element

The handbook also requires core MVP work during the hack window and allows attributed libraries/boilerplates/model weights.
Practical consequence:

- Disclose the precise pre-event baseline, including what works and what is unverified.
- Implement the announced surprise requirement during the event.
- Keep meaningful Git history and actual verification evidence.
- Confirm permitted scope with organizers because the event page also says build from scratch.
- The surprise element is UNKNOWN in this conversation. Do not invent it or mark compliance complete.

Other rules:

- One entry per team; no parallel entries by the same participant.
- No plagiarism; attribute sources.
- Open-licensed or consented self-collected data preferred.
- Proprietary data requires written permission and disclosure.
- Follow API terms/rate limits.
- Participants retain IP; organizers may feature the project with credit.
- Include an appropriate LICENSE file; handbook gives MIT/Apache-2.0 as common examples.
- No missed deadline, falsified data, or unsafe/illegal work.

## Submission requirements

- GitHub repository URL.
- README with project overview, problem, idea/stack/tools, and product demo link.
- Hosted/live demo optional but strongly favored; a short recording is a fallback.
- Pitch deck: at most six slides.
- AI Impact Statement: at most 200 words.
- Explain model choice, data provenance/licenses, hallucination/bias mitigations, guardrails, and expected impact.
- Document actual working behavior, limitations, and team details.

Suggested deck:

1. Problem and who is affected.
2. Insight and why now/why this team.
3. Solution demo.
4. Models, data, architecture.
5. Value and go-to-market.
6. Roadmap and risks.

Judging:

- Problem relevance 20%.
- Innovation/creativity 20%.
- Technical execution 25%.
- UX/UI 15%.
- Business viability 10%.
- Presentation 10%.
  Tie-breakers: technical execution, problem relevance, judge's choice.
  Desk round: maximum five minutes, top five shortlisted.
  Final: three-minute live demo plus two-minute Q&A.

Perks advertised: $100 OpenAI API credits per participant plus Neysa credits; handbook also mentions SerpAPI. Prize pool: $17,500 OpenAI credits, with $10,000/$5,000/$2,500 top-three amounts in the handbook. Event listing also mentions four weeks of mentor office hours for top five. Credits/redemption have NOT been tested; never store credit codes or secrets here.

## Source inconsistencies to confirm

- Event listing says Friday-Saturday, Oct 23-24; portions of handbook still say Sat-Sun.
- Overall event ends at 4 PM Saturday, but submission is noon and handbook finals are noon-2 PM.
- Luma says build from scratch; handbook explicitly allows declared prototypes with the surprise element.
- Flagship-event perk date differs: March 2027 on listing vs February 2027 in handbook.
  Plan against the earlier noon deadline. Confirm with organizers at kickoff; no organizer message has been sent by the assistant.

## v1 baseline: facts from repository inspection

Observed HEAD: 1076c2ff1abee7919124c94297328000daf2cd55
Observed branch: feat/engine-dispatcher

Recent history:

- 1076c2f: style: format test_qualification.py
- fec14ae: fix(lint): resolve line too long error in dispatcher.py
- 57d010a: feat(engine): implement conversation dispatcher and task routing
  These commits are dated October 9, 2026.

Observed architecture:

- Python 3.12+, FastAPI.
- SQLAlchemy/Alembic, PostgreSQL and pgvector.
- TaskIQ worker, Redis broker/dedup/mutex.
- Meta WhatsApp webhook and sending service.
- Hand-rolled async conversation dispatcher.
- Structured qualification rules, retrieval, multi-provider LLM factory.
- Next.js dashboard is planned; no implemented frontend was observed.

Files directly inspected:

- backend/src/main.py
- backend/src/tasks/processing.py
- backend/src/engine/dispatcher.py
- backend/tests/test_dispatcher.py
- backend/pyproject.toml
- backend/scripts/verify.sh
- backend/README.md
- tasks/todo.md
- SPEC.md
- AGENTS.md and development lifecycle.

Readiness evidence:

- A dispatcher implementation and a mocked dispatcher test exist.
- Task 17 acceptance boxes remain unchecked for full end-to-end loop and episodic/semantic memory.
- Task 19 payments acceptance remains unchecked.
- Task 24 onward dashboard work remains unchecked.
- Forms, co-pilot, re-engagement, deployment, and hardening are largely planned in the task list.
- A stale docstring in processing.py calls the worker a placeholder even though it invokes handle_turn. Judge actual source/tests and live behavior, not docstrings alone.
- Existing code does not prove real-device end-to-end readiness.
- Unchecked task boxes do not mean the dispatcher is absent.

No fresh v1 quality gate was run in this conversation. No v1 WhatsApp live roundtrip, Redis/worker runtime, migration, deployed stack, current provider access, or live payment was verified. Do not invent a passing test count or claim production readiness.

## Assessment and next decision

The WhatsApp product direction fits the user's submitted idea. Channel alignment alone is not enough to establish technical readiness.

The immediate recommendation is a ONE-HOUR readiness check in v1:

1. Real WhatsApp message reaches webhook.
2. Message is queued and processed by worker.
3. Reply reaches the actual demo phone.
4. Student selects a seeded course.
5. Next message retains relevant earlier context.
6. Lead persists and can be inspected.

If it passes, proceed with the smallest event-specific feature on this foundation.
If it fails, report the exact blocker and prioritize the smallest repair in v1.
Do not turn a short readiness check into a broad architecture rewrite.

## Proposed MVP scope

One institution and one complete, truthful journey:
WhatsApp conversation -> relevant catalog course -> deterministic eligibility -> persisted, staff-visible lead.

Priority:

1. Real WhatsApp ingress/worker/reply.
2. Course selection and cross-message memory.
3. Code-owned eligibility and prices; fail-closed unsupported answers.
4. Smallest honest staff-visible lead surface. The full dashboard must not be assumed available.
5. Surprise element, implemented during the event.

Keep payments, extensive application forms, broad dashboard CRUD, automated re-engagement, and production rollout outside initial scope unless core work is complete and time permits.

A staff handoff brief with conversation evidence and a suggested next action was discussed as ONE possible feature. It is not selected or implemented and must fit the surprise requirement.
Do not promise a counselor response time or active staff service without an operational path.

Positioning draft:
"AdmitFlow helps prospective students explore an institution's courses and gives admissions staff the context to continue the conversation."

Institutions as paying customers is a hypothesis to validate with mentors. No customer, revenue, conversion improvement, or production deployment claim was established.

## Preparation plan summary

Before kickoff:

- Run the bounded readiness check and record evidence.
- Record the pre-event baseline and working/unverified behavior.
- Use synthetic catalog/persona data.
- Prepare README/deck/AI-statement outlines.
- Verify run instructions, phone/network/hotspot and any intended tunnel.
- Pack and rest.
- Leave event-specific implementation and surprise work for the event.

Proposed schedule:

- Friday 4-5 PM: kickoff, disclosure, surprise/deadline confirmation, choose one outcome.
- 5-10 PM: implementation and essential tests.
- 10-11 PM: integrated checkpoint and scope reduction if needed.
- Overnight: essential repairs and planned rest.
- Saturday 7-9 AM: full journey and rehearsal.
- 9-10 AM: final documentation, deck, AI statement, recording.
- 10-11 AM: upload and verify links.
- 11 AM-noon: submission buffer.

Detailed plan, demo timings, mentor questions, and checklists:
[docs/event/PREPARATION_PLAN.md](docs/event/PREPARATION_PLAN.md).

## Workflow and environment

- Follow AGENTS.md and docs/engineering/development-lifecycle.md.
- Preserve the existing branch and unrelated work.
- Main is protected; use branch -> PR -> squash merge. Do not commit directly to main.
- No AI-attribution trailers in commits or PRs.
- Test-first for domain/policy risks; fake APIs for automated tests.
- Review security, PII, tenant isolation, and truthful demo claims.
- Do not print or commit .env or secrets.
- Record actual commands/results for the exact tested commit/working tree.
- Do not mark completion solely because docs exist.

Commands:
From repository root: bash backend/scripts/verify.sh
From backend: bash scripts/verify.sh
From backend: uv sync
From backend: uv run uvicorn src.main:app --reload

Windows observations:

- PowerShell.
- Working Git Bash: C:/Program Files/Git/bin/bash.exe.
- Default bash can resolve to C:/Windows/system32/bash.exe; prefer explicit Git Bash if necessary.
- uv: C:/Users/shanx/.local/bin/uv.exe.
- System Python was 3.14; use backend/.venv/Scripts/python.exe and declared project requirements.
- Sandbox read-only Git required a per-command safe.directory override:
  git -c safe.directory=C:/Users/shanx/Documents/v1 ...
  No global Git trust config was changed.
- Filesystem restrictions may require approved escalation until this folder is the actual writable workspace.

Graph:

- graphify-out/graph.json exists; CLI failed with ModuleNotFoundError for graphify.
- Inline JSON traversal was used.
- GRAPH_REPORT.md dated Oct 1 cites commit 38b39a0e; graph is stale relative to observed HEAD.
- Actual query tokens: whatsapp, webhook, engine, rag, qualification, razorpay.
- Traversal exposed architecture/planning links, not fresh runtime proof.
- No graph rebuild, package install, or sub-agent work was performed.

## Existing working-tree changes

At the latest read-only check, Git showed pre-existing deletions in agent/workflow configuration and some top-level product/spec-reference docs. These changes were not made by this handoff work. Preserve them; do not auto-restore, stage, or commit them.

This handoff adds documentation and links only. No product code, external messages, deployments, payments, or submission actions were performed. No PR/push/merge or fresh v1 test result is claimed.

## Fresh-message prompt

Open C:/Users/shanx/Documents/v1 as the workspace and send:

"Read AGENTS.md, EVENT_CONTEXT.md, docs/event/PREPARATION_PLAN.md, and docs/event/SOURCES.md. We are preparing the WhatsApp admissions product for AIBoomi Startup Weekend Kochi on October 23-24, 2026. Work only in v1 and keep durable context here. Start with the one-hour real WhatsApp readiness check, preserve existing changes, and report evidence before broad implementation. Disclose prior work and leave room for the announced surprise element. Do not assume an implemented dashboard, passing v1 quality gate, or known surprise requirement."

## Handoff status

These files are local planning material unless later Git history establishes otherwise.
The documentation task remains unchecked until the repository's completion requirements are met.
