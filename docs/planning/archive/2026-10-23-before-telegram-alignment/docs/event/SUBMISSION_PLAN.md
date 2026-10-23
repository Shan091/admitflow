# AdmitFlow: AIBoomi submission plan

Newer user decision: use Telegram for the current build and OpenAI for AI. Neysa
and a provider comparison are not required. See [CURRENT_STATE.md](CURRENT_STATE.md)
before relying on the older channel/provider proposal below; feature scope and
the plan/task list are being reconciled after the current-state explanation.

Planning checkpoint: October 23, 2026, approximately 6:35 PM IST.
Status: proposal for discussion; no product implementation or submission performed.
The user confirms no surprise requirement or revised deadline has been announced.

## Submission outcome

Submit AdmitFlow as an institutional admissions product: a prospective student
explores approved courses, shares relevant information, receives a rule-based
eligibility result, and leaves a persisted inquiry that admissions staff can act on.
WhatsApp remains the intended student channel. Keep the full institutional MVP in
the roadmap; make the event submission demonstrate one complete journey.

Proposed opening line:
"AdmitFlow helps institutions turn student inquiries into informed admissions
conversations, with grounded course guidance and context for their staff."

This is positioning, not evidence of customers, revenue, improved conversion, or
successful live WhatsApp delivery.

## What must be handed in

Requirements below come from the saved [participant handbook](PARTICIPANT_HANDBOOK.txt).
The live [event page](https://luma.com/StartupWeekendKochi) was checked October 23;
the live handbook could not be refreshed. On-site instructions can supersede these.

| Deliverable | Planned contents | Ready when |
| --- | --- | --- |
| GitHub repository URL | This repository, judge-accessible source, setup instructions, license and attributions | A judge can open it and identify the final build and event work |
| Root README | Problem/users, actual working journey, stack/tools, setup, demo link, team, models/data, evaluation and limitations | Claims match the demonstrated build; root README is currently absent |
| Product demo link | A concise recording of the final working build; a hosted interactive demo if feasible | Link opens for judges and clearly identifies real, recorded, or simulated behavior |
| Pitch deck, at most 6 slides | Problem; insight; solution; technology; value/GTM; next steps | Within the limit, aligned with the actual demo and rehearsed |
| AI Impact Statement, at most 200 words | What AI does, actual models and rationale, data/licenses, hallucination/bias mitigations, expected outcomes | Word count checked; describes the models and guardrails actually used |

A separate live demo URL is optional but strongly favored. The README still needs
a product demo link. Prepare a recording even if a live demo is available.

Supporting material in the repository: baseline/event-work disclosure, source/data
notes, actual verification evidence, and concise known limitations. An appropriate
license is also required by the handbook; choose it deliberately before publishing.
The portal URL, exact fields, file types and upload limits remain unknown.

## The journey to demonstrate

Use one fictional institution, a small synthetic course catalog, and synthetic
student personas. Label these as illustrative data.

1. The student asks about courses in a supported language.
2. AdmitFlow presents options from the approved catalog and accepts a course choice.
3. The student supplies relevant facts; the next turn retains earlier context and
   handles a correction.
4. Code evaluates configured eligibility rules and provides the relevant next step.
   Institution-owned fees and rules cannot be invented by the model.
5. A minimal staff view shows the persisted inquiry, course, collected facts,
   conversation context, eligibility result and next action.
6. An unsupported question produces an honest uncertainty response or handoff.

The proposed differentiator is the useful context retained for admissions staff,
together with grounded guidance and code-owned decisions. A concise staff handoff
brief is a candidate event feature; it has not yet been selected or implemented.
Leave room to adapt it to any announced surprise requirement.

The minimal staff view is part of the proposed event slice. Broader dashboard CRUD,
payments, extensive forms, re-engagement and production hardening remain on the
full roadmap. Do not let them delay the complete inquiry-to-staff demonstration.

## WhatsApp and demonstration decision

Latest recorded evidence in [POSTMAN_CHECK.md](POSTMAN_CHECK.md): Meta reports
sending blocked; an accepted API request subsequently failed with code 131031.
There is no verified handset roundtrip, complete course-selection journey, or
finished staff dashboard. No fresh runtime checks were run for this plan.

- If Meta restores access, verify the real phone journey before choosing it for
  the final demo. Account review needs the user's Meta access.
- If the restriction persists, proposed fallback: a clearly labeled browser
  conversation demonstrator using the same admissions engine and database, plus
  the staff view. This would be new work, not a currently available feature.
- Disclose the channel restriction and distinguish engine behavior from WhatsApp
  transport. Ask organizers whether this fallback meets the submitted idea/rules.
  A recording cannot establish a WhatsApp journey that has never succeeded.
- Do not spend the event repeating sends while the account remains restricted.

## Use the provided resources

The Downloads PDF is a Neysa inference quickstart, not an additional submission
handbook. See [SOURCES.md](SOURCES.md) for its provenance and
[RESOURCE_PLAN.md](RESOURCE_PLAN.md) for the broader resource plan.

| Resource | Planned use | First decision/check |
| --- | --- | --- |
| OpenAI participant credits | Candidate for learner-fact extraction and grounded replies; approved embedding usage if needed | Confirm activation, eligible project/models, quota and expiry |
| Neysa hosted Gemma endpoint | Compare on the same admissions cases; possible reply provider if it passes | Discover exact model ID; verify output, latency, schema behavior and limits |
| Neysa hosted Qwen endpoint | Same bounded comparison; consider only after checking answer presentation | The guide reports reasoning-style text and truncation in its sample |
| Neysa infrastructure grant | Host the API/worker only if the grant supports the required workload and persistence | Inference endpoint access does not establish app/database hosting access |
| SerpAPI, if supplied | Optional discovery of official institutional source documents for staff review | Confirm grant; review and attribute sources before indexing |
| Product/domain mentors | Challenge the payer, staff workflow, differentiation and pilot outcome | Bring the working journey and one concrete adoption question |
| Engineering/provider mentors | Clarify Neysa model behavior, endpoint limits and viable hosting | Bring a sanitized failing request or measured comparison |

Run a time-boxed comparison before selecting a provider, not a multi-model feature
for its own sake. Proposed set: 12 synthetic cases spanning course choice,
multi-turn recall/corrections, supported and unsupported questions, instruction
injection, and English/Hindi/Malayalam examples. Check answer correctness,
faithfulness to the supplied source, extraction validity, reasoning leakage,
truncation, latency, failures and reported usage. Use identical cases and record
actual outputs. This is a smoke evaluation, not proof of broad language quality;
language claims need fluent-speaker review.

Start with one request per candidate after access and a bounded usage cap are
confirmed; do not launch an uncapped batch. Select the simplest passing provider
setup. Do not assume Neysa supports every OpenAI feature, structured-output mode,
embedding API or reasoning parameter. Keep eligibility, prices and consequential
state changes in code regardless of provider. No endpoint was called for this plan.

The guide labels its models "Gemma 4 26B A4B" and "Qwen3.6 27B" and instructs
participants to discover IDs with `GET /v1/models`, then use
`POST /v1/chat/completions`. Its recorded smoke results are the guide author's
evidence, not fresh verification of our access or integration. Obtain keys via
the Neysa V3 portal and keep them local.

## Deck and presentation

| Slide | Content |
| --- | --- |
| 1. Problem | A specific student inquiry and the staff follow-up gap it creates |
| 2. Insight | Institution-owned knowledge, readiness-aware conversations and useful staff context; state buyer assumptions |
| 3. Solution | The actual student-to-staff journey, with screenshots and demo link |
| 4. Technology | Model role, approved data, retrieval, code-owned rules, persistence and measured evidence |
| 5. Value and GTM | Institution as proposed payer, narrow pilot segment, buyer/reach strategy and metrics to validate |
| 6. Next steps | Event-built increment/surprise feature if announced, current restrictions and next product milestones |

Handbook judging weights: problem 20%, innovation 20%, technical execution 25%,
UX/UI 15%, business viability 10%, presentation 10%. Prioritize a working,
understandable outcome and evidence alongside the story.

Prepare for a maximum five-minute desk review and a three-minute final demo plus
two-minute Q&A. Suggested three-minute run: 20 seconds problem; 80 seconds student
journey; 40 seconds staff outcome/event feature; 20 seconds technical evidence and
limits; 20 seconds buyer hypothesis and pilot next step.

## Proposed schedule from Friday evening

All times IST. Use Saturday October 24 at noon as the planning deadline until
organizers confirm otherwise; the advertised 4 PM event end is not the upload target.

| Window | Concrete output |
| --- | --- |
| First 30 minutes after planning | Confirm prior-work permission, portal/deadline, surprise status, team details and resource activation path |
| Next 30-45 minutes | Select demo path and bounded provider comparison; freeze the event slice |
| Friday evening to 11 PM | Complete and test course choice, memory/corrections, persisted inquiry and minimal staff view |
| By 11 PM | Demonstrate one integrated journey; cut optional work if it fails |
| Overnight | Repair essentials, incorporate an announced surprise requirement and take planned rest |
| Saturday 7-9 AM | Run quality gate and journey checks; record actual results; rehearse |
| 9-10 AM | Freeze demo features; finish README, deck, AI statement, recording and limitation notes |
| 10-11 AM | Upload to portal and verify judge access to every link |
| 11 AM-noon | Submission buffer and rehearsal |

If time slips, reduce optional capabilities while preserving the complete core
journey and submission package. The schedule is a target, not a readiness estimate.

## Open decisions

- Organizer permission for the disclosed existing prototype and any required
  event-built increment. Public listing says build from scratch; the saved
  handbook describes a declared-prototype exception.
- Surprise requirement: not announced according to the user at this checkpoint.
- Demo channel if Meta stays blocked: proposed browser demonstrator, pending scope
  agreement and organizer acceptance.
- Team roster and division of work; plan remains usable solo.
- Portal URL/fields, actual grants, usage caps, provider choice, hosting fit,
  repository visibility/access and appropriate license.

Planning creates no claim of readiness, redemption, paid inference, deployment,
publication, organizer contact or completed submission.
