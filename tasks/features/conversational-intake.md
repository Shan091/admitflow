# Feature: disclosed adaptive conversational intake

## Outcome

Let a learner describe what they already know or what they enjoy in their own words. Extract only
catalog-bounded course-discovery facts, then choose the next question or recommendation from the
facts already known. A learner who already knows a course can name it; an undecided learner can
start from interests and activities. Tap-based exploration and browsing remain available.

This is institution-course discovery, not an aptitude test, personality assessment, broad career
prediction, or guarantee of admission or employment.

## Settled boundaries

- The fictional demo catalog is sample data. Expand to at least 28 complete offerings: at least
  five in each agreed field and coverage of certificate/vocational, diploma, undergraduate, and
  postgraduate levels.
- Use conversation-only exploration: no numerical aptitude/readiness-to-fit score or personality
  label.
- OpenAI-assisted text processing is enabled by default for this hackathon demo. At `/start`, clearly
  explain that typed messages are sent to OpenAI and stored locally, and instruct users to enter only
  fictional demo text. Provide persistent controls to turn processing off or back on. While off,
  button-based course exploration remains usable and typed text must not be sent to any AI provider.
  This is the product behavior chosen for the demo, not a legal/privacy determination.
- For each extraction request, send only the current user message plus the fictional, allowlisted
  catalog vocabulary needed to normalize it; do not send names, chat IDs, contact details, or the
  full transcript. Use stateless requests (`store=false`). Do not claim this alone makes the demo
  production-safe.
- Localize the processing disclosure and opt-out control; disclose that most other replies remain in
  English and need fluent-speaker review.
  General course, eligibility, FAQ, and payment copy still requires fluent-speaker review before
  the product can claim complete language support.
- The model may extract intent and explicit user-stated course, field, study level, interest, or
  activity from a schema. Code validates every value against the seeded catalog and chooses the
  next question. Course matches, facts, prerequisites, fees, eligibility, and payment gates stay
  code-owned. No model-created course or requirement may be displayed.
- Preserve the direct known-course route, known-field route, unsure/explore route, and browse/FAQ
  route as optional shortcuts; natural-language input may enter/switch between them without
  resetting unrelated student facts.
- A parent can contribute parent-attributed preferences but cannot replace the learner's choices.
  Non-catalog, unclear, unsupported, crisis, or sensitive questions fail safely into bounded
  responses or a staff-dashboard handoff; no live contact or SLA is configured.

## Acceptance examples

1. `/start` discloses processing and local storage, then starts the discovery flow without a consent
   prompt. “I like numbers and helping people” is processed only with fictional demo text.
2. “I enjoy organizing data and making charts; I want a diploma” extracts only
   matching catalog facts, persists them as student-attributed facts, and recommends only complete
   matching diploma entries or asks one relevant follow-up if evidence is insufficient.
3. “I know I want Applied Data Analytics Diploma” finds the exact seeded course without asking the
   student to walk through field/level/activity prompts.
4. “I am not sure” asks one short exploratory question with optional taps; it does not produce a
   score or label.
5. “I want medicine” never invents a medical program; the bot explains catalog scope and offers a
   truthful staff handoff/browse choice.
6. If extraction errors, refuses, times out, or returns out-of-catalog values, no partial facts are
   trusted; the student gets a button-based fallback and existing course/fee rules are unchanged.
7. After opt-out, FAQ routing, vector retrieval, and discovery extraction receive no message text;
   an explicit re-enable action restores AI processing. Deterministic local fee,
   payment-status, deletion, and qualification branches continue to work.

## Verification

- Test catalog coverage, unique IDs, complete facts, idempotent seed updates, and recommendation
  provenance with local SQLite only.
- Test the initial processing disclosure, enabled-by-default discovery, opt-out and re-enable, and
  explicit proof that no external AI provider receives text while processing is off.
- Test extraction schema, unknown/ambiguous values, parent attribution, multilingual paraphrase
  fixtures, prompt-injection text, OpenAI failure, and dynamic one-question selection with fake APIs.
- Run `bash scripts/verify.sh` and `git diff --check`. A live smoke test may use synthetic fictional
  prompts only; never use real student chat data.
- Rehearse the disclosed adaptive Telegram flow and opt-out controls before describing them as a
  live demo.

## Open production gates

Privacy/legal review including minors and guardian consent; fluent-speaker review for English,
Malayalam, Hindi, and Hinglish; adversarial extraction and safety evaluation; accurate all-level
eligibility; retention/expiry policy; deployment security, tenant isolation, monitoring, and a real
staff escalation contact/SLA. This feature alone does not make AdmitFlow production-ready.
