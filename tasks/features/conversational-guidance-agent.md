# Feature: conversational career-informed course guidance

## Outcome

Replace a course-menu-first experience with a natural multi-turn conversation that helps a learner
understand what they want to study, then compare suitable courses. The agent should adapt to what a
learner has already said: a student who knows a course can jump to it, one who knows a field can
compare relevant offerings, and an undecided student can explore from concrete interests and goals.
Learners can ask unrelated admissions questions, change direction, pause, resume, and correct the
agent without restarting or losing unrelated facts.

The long-term goal is production-grade guidance. The current Telegram app remains a fictional
single-tenant hackathon demo until real institution data, privacy controls, age policy, localization,
human escalation, and operational requirements are verified.

## Evidence and design basis

- The v1 product defines lifecycle stages as a record of where a lead stands, not a mandatory
  sequence. Each turn reloads recent messages and facts, routes the message, updates the readiness
  signal, dispatches to a handler, validates the response, then persists the turn.
- Career-guidance research supports conversations and active exploration. Social Cognitive Career
  Theory offers a useful non-test lens: interests develop alongside learning experiences,
  self-efficacy, expected outcomes, goals, supports, and barriers. This is a conversation-design
  framework, not a basis for diagnosing or scoring a learner.
- Sources currently reviewed: OECD, [*Career Conversations* (2021)](https://doi.org/10.1787/15b83760-en);
  Lent, Brown & Hackett, [*Toward a Unifying Social Cognitive Theory of Career and Academic
  Interest, Choice, and Performance* (1994)](https://doi.org/10.1006/jvbe.1994.1027); [NCERT Career
  Guide](https://ncert.ncert.org.in/CareerGuide.php?ln=en); [NCERT My Career
  Advisor](https://mycareeradvisor.ncert.gov.in/); and India's [National Career
  Service](https://www.dge.gov.in/ncs).
- These sources do not establish that an AI conversation is equivalent to a trained career
  counsellor. Claims about AI effectiveness require direct evaluation.

## Current-state findings

- `/start` already opens with an exploratory question and shortcuts; it no longer lists courses as
  the first response.
- The seed contains 28 fictional course offerings in five fields and four education levels.
- Discovery extraction currently records course, field, education level, interest, activity,
  uncertainty, and correction. The extractor sees the current message and the allowlisted catalog.
- The service now asks for one complementary signal when context is thin, then reflects the
  learner's stated interests/activity/level and waits for confirmation before showing course cards.
  Confirmation is tied to a fingerprint of the current facts, so corrections and path changes make
  old buttons stale. It still does not explore goals, learning experiences, expected outcomes,
  constraints, or barriers in a coherent adaptive dialogue.
- The extractor currently classifies career/profession requests outside the institution catalog as
  `out_of_scope`. That matches the earlier product decision but may conflict with the newer request
  for broader career guidance. Resolve this boundary before changing that behavior.
- Course matching uses direct overlap with seeded interests and activities. It has a first
  deterministic sufficiency/confirmation policy, but that policy still needs evaluation against a
  human-reviewed golden set; there is no validated general-career evidence corpus.

## Proposed turn model

Each incoming turn should use the same loop, while selecting the next action from current context:

1. **Triage and interrupts:** handle opt-out, explicit human request, urgent/sensitive content,
   language change, FAQ/fee/payment questions, deletion, and course/path changes before discovery.
2. **Rebuild context:** load the recent conversation and attributed facts; retain verified facts,
   unresolved questions, corrections, current learner/speaker, selected course, and lifecycle stage.
3. **Interpret this turn:** extract only explicitly stated facts using a strict schema. Keep learner
   and parent statements attributed separately. Never infer ability, personality, marks, identity,
   or likely outcomes from demographics or writing style.
4. **Choose one useful next move:** if the learner knows a course, resolve it directly; if they know
   a field, clarify desired study level or course differences only when needed; if unsure, ask one
   short question about a concrete activity, learning experience, goal, or practical concern. Do
   not repeat facts already established. Offer optional tap replies without forcing a path.
5. **Reflect and correct:** when enough facts exist to compare options, briefly summarize what the
   agent understood and invite a correction before relying on a material assumption.
6. **Compare, do not pronounce a winner:** show at most three complete catalog offerings with
   source-backed fit reasons, meaningful differences, prerequisites, trade-offs, and unknowns.
   Explain that the learner chooses; provide an ask-more, revise, browse, or staff-handoff action.
7. **Transition only when appropriate:** move to code-owned qualification after a learner selects
   an offering or asks about applying. Eligibility and money remain deterministic. Enrollment
   readiness is soft and separate from hard eligibility.
8. **Persist and resume:** store the exchange, fact provenance, last useful question, and state so a
   later turn can continue without forcing the learner to repeat themselves.

This is an adaptive turn loop, not an eight-question script. Greetings, uncertain replies, and
unsupported media should receive a graceful clarification or available action, not a spurious
handoff. Repeated ambiguity, unsupported catalog claims, sensitive situations, or user-requested
human support should produce a truthful staff-dashboard handoff; no contact/SLA may be invented.

## Existing decisions to preserve

- The earlier explicit scope is institution-course recommendations only, with unsupported needs
  handed to a counsellor. The newer “career guidance” wording may supersede that; keep the scope
  change open until clarified. Planning default: use career-guidance conversation techniques while
  recommending only verified institution offerings.
- Use conversation and optional taps; no aptitude score, personality label, or single objectively
  “right” course.
- Support vocational/certificate, diploma, undergraduate, and postgraduate learners; the fictional
  Kerala catalog presently covers tech/data, business/accounting, design/media, hospitality/tourism,
  and non-regulated vocational skills.
- Student preferences lead when a parent participates; record whose preference is whose.
- Gently challenge a mistaken assumption using verified facts, alternatives, and trade-offs, then
  leave the choice with the learner.
- English, Malayalam, Hindi, and Hinglish are selectable. Most non-discovery replies still require
  translation and fluent-speaker review.
- Use complete verified course facts only. Keep fees, hard eligibility, payment, and course facts
  code-owned. Do not invent regulated requirements, institution details, job prospects, or placement
  guarantees.
- The demo has no real counsellor contact or response-time promise. Human work appears in the staff
  dashboard; the reply says contact details are not configured.
- OpenAI text processing is disclosed and on by default. The learner is not asked for consent or
  required to complete a consent step; persistent opt-out/re-enable controls remain. The demo uses
  fictional text only. This does not resolve
  production legal/privacy obligations or age-appropriate processing.

## Acceptance criteria

- `/start` asks an open question before displaying a course list and offers optional shortcuts for
  known course, known field, exploration, and browsing/questions.
- A learner can answer in natural language over multiple turns. The next question uses the learner's
  existing facts and asks only for information that can change the next recommendation or action.
- A known-course learner can jump directly to that offering; ambiguous/unlisted names are clarified
  without inventing a match.
- An unsure learner receives a short, low-pressure prompt anchored in things they enjoy, have tried,
  want to learn, or hope study will help them do. No formal assessment or score is produced.
- Before a material recommendation, the system reflects its understanding and requires a clear
  confirmation; typed corrections or stale tap replies cannot surface recommendations from old
  facts, while unrelated valid facts remain intact.
- A recommendation is based on complete catalog records, includes provenance/fit reasons and real
  trade-offs, and does not imply admission, employment, earnings, or that one option is objectively
  best.
- Course selection, eligibility, costs, FAQ answers, parent attribution, and payment remain safe and
  code-verified; unsupported levels or missing data create a truthful handoff.
- A learner can interrupt discovery to ask an FAQ/fee question, change language/path, pause, resume,
  request staff, or delete data without the bot becoming stuck in a questionnaire.
- After AI opt-out, typed content does not go to the discovery model, intent router, or embedder.
- Failure of extraction, retrieval, database, messaging, or the model does not create partial facts,
  fabricate an answer, send duplicate payment actions, or strand the learner without an available
  recovery action.

## Verification plan

- Add turn-sequence tests rather than testing only isolated extractions: vague opening, follow-up,
  correction, known-course shortcut, interest change, recommendation, interruption, and resume.
- Evaluate fixed fictional dialogues in English, Hindi, Malayalam, and Hinglish; test code-switching,
  short/empty answers, spelling variation, ambiguity, contradictions, prompt injection, parent-child
  disagreement, and unsupported/regulated interests.
- Evaluate retrieval and recommendations against a human-reviewed golden set with expected matches,
  acceptable alternatives, required facts, and abstentions. Track coverage as well as incorrect-match
  rate; do not tune to maximize recommendations at the expense of honesty.
- Verify that model output cannot create a course, prerequisite, fee, eligibility result, factual
  career claim, or unverified institutional promise.
- Run `bash scripts/verify.sh`, `git diff --check`, migration/data-preservation tests, and end-to-end
  Telegram/dashboard tests. Record the exact SHA and CI result before marking implementation tasks
  complete.

## Production gates and open decisions

- **Scope conflict:** earlier institution-only decision vs. newer career-guidance wording. Resolve
  whether occupation/pathway discussion is in scope; course recommendations can remain catalog-only.
- **Age policy:** youngest user, treatment of minors, guardian participation and privacy obligations.
- **Catalog:** new domains/courses, first real institution's catalog, official source ownership,
  completeness and update cadence. Fictional seed data is demo-only.
- **Guidance data:** authoritative source for occupations, qualifications, and pathway facts if the
  broader scope is approved; provenance, effective date, review process, licensing, stale-data
  behavior, and referral when absent.
- **People and operations:** real counsellor contact, escalation SLA, business hours, staff takeover,
  monitoring, audit, incident response, and model/provider outage policy.
- **Privacy/security:** documented purpose and lawful processing basis, age-appropriate notice,
  data minimization, retention/expiry implementation, deletion verification, tenant isolation,
  encryption, access controls, and external processor review.
- **Quality:** native-speaker review, counsellor review, bias/equity testing, evidence-based
  recommendation evaluation, safety review, and production monitoring thresholds.

No hackathon smoke test or green unit suite alone satisfies the production gates above.
