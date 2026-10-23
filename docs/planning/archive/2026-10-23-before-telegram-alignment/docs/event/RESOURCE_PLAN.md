# Hackathon resources for AdmitFlow

Newer user decision: Telegram is the active channel and OpenAI is the selected AI
provider. Use only necessary resources; Neysa access is optional and no comparison
or deployment there is required. See [CURRENT_STATE.md](CURRENT_STATE.md) for the
current audit and planning baseline. Earlier allocations below remain reference
options rather than active requirements.

Updated: 2026-10-23, Asia/Kolkata. This is a proposed allocation, not evidence of activated credits, spending, deployment or completed features.

## Goal

Use the hackathon resources to advance AdmitFlow's full institutional MVP roadmap: accurate course guidance, deterministic qualification, persistent leads/applications, and usable staff operations. Keep the full plan; select a bounded, verified milestone for the event. Work only in this repository and preserve existing changes.

## What is offered

### October 23 Downloads guide: hosted inference access

The user-provided `C:/Users/shanx/Downloads/AIBoomi_Startup_Weekend_Kochi.pdf`
is a five-page Neysa LLM inference quickstart. It adds concrete hosted-model
resources to the earlier generic infrastructure-credit plan:

- Models labeled **Gemma 4 26B A4B** and **Qwen3.6 27B**, with separate hosted
  endpoints and OpenAI-compatible chat-completions request patterns.
- Neysa V3 portal key management; discover the exact deployed ID using
  `GET /v1/models` before requesting `POST /v1/chat/completions`.
- The guide records a successful Gemma smoke response. Its Qwen sample produced
  reasoning-style text and ended with `finish_reason=length`; output presentation
  needs validation before student-facing use. These are supplied-guide findings,
  not our own live test results.
- Hosted inference access does not prove app/database hosting entitlement,
  embedding support, structured-output compatibility, quota or expiry.

Proposed use: compare these endpoints with the credited OpenAI setup on a small,
fixed synthetic admissions set, then select a provider based on observed quality
and reliability. No provider switch, key activation or inference call was made.
Detailed deliverables, evaluation proposal and time budget:
[SUBMISSION_PLAN.md](SUBMISSION_PLAN.md).

### Participant credits and other support

The public [AIBoomi event page](https://luma.com/StartupWeekendKochi), opened October 23, confirms **$100 OpenAI API credits per participant plus Neysa infrastructure credits**. Its $17,500 prize-credit pool is for the top three teams; four weeks of post-event mentor office hours are for the top five. Those rewards are not available participant credits.

The saved [participant handbook](PARTICIPANT_HANDBOOK.txt), captured October 22, also lists **SerpAPI credits, on-floor mentors, workshops, Wi-Fi and power**. The live handbook could not be refreshed in this check; confirm the current participant kit and kickoff announcements.

Unknown until redemption/setup: exact Neysa/SerpAPI quantities, eligible services and accounts, activation steps, expiry, quotas, regions and continuation charges. Do not assume team members can pool credits. Keep redemption codes and API keys out of chat, source, logs and event documents.

## Useful resources mapped to the plan

| Resource | Concrete AdmitFlow use | Relevant tasks | Boundary |
| --- | --- | --- | --- |
| OpenAI API credits | Extract learner facts into typed schemas, generate grounded admissions replies, embed approved knowledge, and evaluate conversation quality | 9-17, 23, 40 | Code owns eligibility, fees and consequential state transitions. Structured output validates format, not factual truth. Use models supported by the credited project and configuration roles. |
| Neysa infrastructure credits | Evaluate suitable VM/container hosting for the API and worker with stable HTTPS and persistent data | 3, 17, 38, 39 | First confirm the grant covers the required CPU/GPU, storage, networking and region. Hosting selection remains subject to an explicit decision against ADR-007; no stack migration is implied. |
| Neysa GPU access, if that is what the grant provides | Time-box an embedding/reranker or later decision-model benchmark against a fixed evaluation set | 41, 42 | Optional measured work after the core journey. Do not add model hosting merely to consume GPU credits, or leave idle compute running. |
| SerpAPI credits, if supplied | Help staff find official institution pages, prospectus links and FAQ source candidates during knowledge onboarding | 13, 30 | Restrict to approved domains, record source/date and require review before indexing. Live search does not decide course eligibility, fees, seats or admissions. |
| Product/education/business mentors | Find a pilot institution, identify the payer and staff workflow, and test the value proposition | MVP acceptance and pilot planning | Record actual feedback. Do not claim customer validation or willingness to pay without evidence. |
| Engineering/provider mentors | Review durable processing, tenant isolation, deployment and credit configuration | 17, 25, 35-39 | Bring one concrete architecture question, failure or acceptance test. Support access does not guarantee Meta account reinstatement. |

Provider references: [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs), [OpenAI evaluations](https://developers.openai.com/api/docs/guides/evals), [Neysa container-compatible platform](https://neysa.ai/neysa-velocis/ai-platform-as-a-service/), [SerpAPI search documentation](https://serpapi.com/search-api).

## What is already useful in AdmitFlow

- The provider factory and configuration roles can support the credited OpenAI project without changing domain rules. Confirm model access/schema compatibility before configuring a provider.
- PostgreSQL models/migrations, code-owned qualification rules, encryption/audit helpers, and the Redis/TaskIQ foundation are reusable parts of the full plan. Their presence does not prove complete integration or production readiness.
- The existing RAG pipeline is a starting point for approved institution knowledge. Complete the retrieval-confidence, source-grounding and reply-validation checks before real applicant use.
- Existing tests and the last recorded gate provide a baseline. Automated tests must continue using fake APIs; live evaluations need an explicit budget and sanitized synthetic inputs.

The next useful result is a complete inquiry-to-staff workflow with reliable memory and a persisted lead. Sponsor-resource use should support that result rather than become a separate feature requirement.

## Suggested allocation and activation order

1. **Verify grants first.** Ask the official organizer/provider desk for activation links, eligible project/account, exact quota, expiry and post-credit billing. Redeem locally through the official provider interface. Document activation status only.
2. **Prioritize OpenAI development and evaluations.** Build a fixed synthetic set covering course selection, qualification extraction, corrections, multiple turns, unsupported questions and the intended languages. Schema validity alone is not a passing answer. Keep native-speaker review as a separate requirement.
3. **Use a bounded budget.** An illustrative allocation of the advertised $100 is $40 for iteration, $30 for controlled evaluations, $10 for embeddings/RAG, and $20 reserved for integration/rehearsal. This is a planning suggestion, not spend authorization or a workload guarantee. Start with a small live smoke check before any approved batch, enforce batch/request caps and record actual usage. Dashboard budget alerts should not be assumed to stop spending.
4. **Confirm Neysa fit before deployment.** Check stable public HTTPS, persistent volumes, database backups, private data-service access, secret handling, region and ongoing cost. A normal web/worker workload does not itself require a GPU. If the grant is GPU-only, use it only for a useful bounded experiment and keep the existing hosting plan until a decision is recorded.
5. **Use search only where helpful.** SerpAPI can accelerate staff-assisted source discovery. Store reviewed knowledge with provenance; avoid a paid search on every student message and never let unreviewed search results overwrite structured institution facts.
6. **Use mentors early.** Ask for a pilot introduction, the highest-value admissions workflow, a review of security/reliability boundaries, and guidance on the announced surprise requirement. Return with evidence and measurable results for a second review.

## Event and release boundaries

The saved handbook permits continuing a declared prototype with the surprise requirement, while the event listing says build from scratch. Confirm the permitted scope and disclose the baseline at kickoff. The surprise element and any updated submission schedule remain unconfirmed here. Credits do not waive those rules.

WhatsApp delivery remains blocked by Meta's account restriction. API credits, a new client or a hosting change cannot reverse that decision. No renewed message sends, credit redemption, paid batch, infrastructure provisioning, provider/hosting change, or deployment was performed for this resource plan.

## Acceptance before using a resource

- Official activation and eligible service are confirmed; expiry and continuation costs recorded without secrets.
- A selected task has a clear outcome and acceptance checks; provider usage stays within an approved cap.
- Institution data is approved and source-attributed; synthetic inputs are used for evaluations and event demonstrations.
- Actual outputs, failures, latency and usage are recorded; unfinished work and external restrictions remain explicit.
- Keep the full MVP roadmap separate from the subset verified during the hackathon.
