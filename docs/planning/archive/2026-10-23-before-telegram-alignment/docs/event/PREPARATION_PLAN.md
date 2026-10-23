# Event preparation and execution plan

Read [../../EVENT_CONTEXT.md](../../EVENT_CONTEXT.md) first. Dates and times below use Asia/Kolkata. This is a proposed plan, not evidence of completed work.

## Latest direction (October 23)

For the Friday-evening submission discussion, use
[SUBMISSION_PLAN.md](SUBMISSION_PLAN.md): deliverables, proposed demo scope, the
Downloads Neysa inference guide, resource use and upload timing. The user confirms
no surprise requirement or revised deadline has been announced at this checkpoint.

Build the real institutional MVP in this AdmitFlow repository, keeping the full task plan as the
roadmap. Use [RESOURCE_PLAN.md](RESOURCE_PLAN.md) for sponsor-resource allocation and activation
questions. Select a verifiable event milestone without representing the whole roadmap as done.
The WhatsApp restriction remains unresolved. The readiness checklist below is historical/pending;
it does not direct repeated sends while Meta blocks delivery. Preserve existing work and record
the pre-event baseline and actual event-built increment.

## Next action: one-hour v1 readiness check

Current session evidence: [READINESS_CHECK.md](READINESS_CHECK.md). The folder is now `admitflow`; v1 references mean this same repository. The baseline gate passed on October 22, but the real-device journey remains unverified.

Purpose: decide whether the existing WhatsApp foundation is usable without spending the event repairing infrastructure.

1. Record current branch, commit, and dirty state. Read project rules and the relevant Task 17 acceptance criteria. Preserve unrelated work.
2. Check configuration PRESENCE without printing values: database, Redis, worker, WhatsApp/Meta configuration, provider configuration, and public webhook URL. Confirm test/demo recipient and account access.
3. Start or inspect the existing intended services using this repo's documented commands. Do not assume credentials, migrations, provider permissions, or a deployed stack exist.
4. Send a real message from the intended demo phone. Trace ingress -> queue -> worker -> dispatcher -> WhatsApp reply. Save sanitized evidence and actual latency.
5. Run a second and third turn: select an actual seeded course, answer qualification or discovery, and confirm persisted context rather than a fresh restart.
6. Inspect the lead in the actual data store; report whether a staff UI exists. Do not describe a database inspection as a finished dashboard.
7. Run the repo quality gate when its environment is ready:
   From v1: bash backend/scripts/verify.sh
   From backend: bash scripts/verify.sh
   On this Windows machine, use the explicit Git Bash executable if needed.
8. At the hour boundary, report pass/fail, blocker, evidence, and estimated repair scope.

Passing means a real message roundtrip plus course selection and memory work; it does NOT imply the full MVP is done. Mock tests alone cannot establish live readiness.

If the check fails: keep WhatsApp as the product channel, report the exact blocker, and choose the smallest repair within v1. Avoid an unapproved rewrite or an expansion into broad infrastructure work.

## Tonight / before kickoff

- Verify event invite and venue using the user's registration information. Do not infer venue from the public map.
- Identify whether the user is solo or has a registered teammate when division of labor matters.
- Record a clean, attributable baseline commit using the existing branch/PR workflow. Do not rewrite history or present old work as event work.
- Create a disclosure listing prior modules, working behavior, missing behavior, and baseline SHA.
- Prepare a small synthetic catalog and reproducible demo personas. Avoid real applicant records.
- Check device, provider access, network/hotspot, tunnel reliability, and local run instructions.
- Draft the README, deck structure, and AI Impact Statement. Leave new-feature results and surprise compliance unclaimed.
- Rehearse the existing journey and record a dated baseline clip if useful. A final recording must include the new event feature.
- Pack laptop/charger, phone/charger, ID, power extension, adapters/headphones, water, and comfortable overnight items.
- Rest before the sprint. Avoid starting a broad architectural migration.

## Kickoff disclosure draft

"We are continuing an existing AdmitFlow WhatsApp prototype. Our pre-event baseline is [actual SHA], with [verified existing features]. [Unverified/planned items] are not being claimed as working. During this event we will implement [announced surprise requirement and bounded new capability], with separate commits, verification, and a final demonstration."

Fill with actual evidence. Confirm the prior-work exception, surprise requirement, and deadline with organizers. No organizer has been contacted by the assistant.

## Suggested time budget

| Time | Outcome |
| --- | --- |
| Fri Oct 23, 4-5 PM | Kickoff, prior-work disclosure, deadline/surprise confirmation, one new outcome selected |
| 5-10 PM | Build the smallest event-specific capability and essential tests |
| 10-11 PM | Integrated working checkpoint; reduce scope if needed |
| Overnight | Resolve essential blockers, record progress, take planned rest |
| Sat Oct 24, 7-9 AM | Full journey verification, edge cases, final rehearsal |
| 9-10 AM | Finish deck, README, AI statement, backup recording |
| 10-11 AM | Upload and check all submission/demo links |
| 11 AM-noon | Submission buffer; avoid risky changes |

The page lists an overall 4 PM Saturday end; the handbook's submission is noon. Confirm conflicts on site and plan against the earlier deadline.

## Minimum demonstrable product

Target a real student-facing journey, plus the surprise element:
- WhatsApp message and response.
- Relevant catalog-backed course choice.
- Correct memory of earlier stated information.
- Eligibility rules and prices owned by code.
- Persisted lead and the smallest honest staff-visible view.
- Unknown/unsupported information handled without fabricated answers.
- Clear indication of illustrative data and demo limitations.

Payments are optional for the initial event scope. Application forms, broad dashboard CRUD, automated re-engagement, and production rollout are deferred unless core work is complete and time remains.

A staff handoff brief with evidence and suggested next action is a possible extension, subject to surprise compatibility and user agreement.

## Evaluation and demo evidence

Use fake provider tests for policy and domain rules. Live tests require the configured service and may cost money; do not silently make paid evaluation batches.

Proposed acceptance checks, NOT yet run in v1:
- Real webhook -> queue -> worker -> reply.
- Two-turn state persistence and course selection.
- Deterministic eligible/ineligible cases with explicit configured rules.
- Unsupported FAQ safely abstains.
- Tenant-scoped retrieval and no cross-tenant answer.
- Explicit handoff stores context without promising unconfigured staff response.
- Malformed/duplicate webhook handling consistent with actual code.
- Any selected payment flow uses test mode, explicit confirmation, server prices, and signed event verification.
- Restart/reconnect behavior appropriate for the demo.
- Surprise feature has a visible, tested before/after outcome.

Record exact commands, dates, commit, actual outputs, and known failures. No fresh v1 quality-gate result has been established in this conversation.

## Three-minute demo outline

| Segment | Suggested time |
| --- | --- |
| User problem and institution context | 0:00-0:20 |
| Real WhatsApp learner journey | 0:20-1:20 |
| New surprise-compatible capability | 1:20-2:10 |
| Staff-visible result and key safety boundary | 2:10-2:40 |
| Buyer hypothesis and next step | 2:40-3:00 |

Show the useful outcome early. Use synthetic inputs. Keep a final-build recording available if network delivery fails; label a recording as a recording.

## Submission checklist

- [ ] GitHub URL accessible to judges; appropriate license and source attribution.
- [ ] README: problem, users, actual behavior, stack, setup, model/data provenance, evaluation, limitations, team.
- [ ] Existing baseline and event-built delta clearly disclosed.
- [ ] Surprise requirement implemented and evidenced.
- [ ] Final commit and actual verification results recorded.
- [ ] Product demo link; hosted demo or short recording.
- [ ] Pitch deck of at most 6 slides.
- [ ] AI Impact Statement of at most 200 words.
- [ ] Secrets and private applicant information excluded.
- [ ] Submission uploaded and links checked before noon.

## Business and mentor preparation

Proposed payer: an institution handling course inquiries. This is a hypothesis, not a validated customer or revenue claim.
Ask mentors to challenge:
- Which institution type has a sufficiently costly inquiry/follow-up problem?
- What evidence would justify adoption beyond an auto-reply bot?
- Which person controls the buying decision?
- What narrow pilot outcome can be measured without overstating causality?
- Which pricing approach should be tested with actual buyers?

Do not fabricate testimonials, conversion improvements, active customers, deployment reliability, language fluency, or verified admissions outcomes.
