# Feature: consent-gated adaptive conversational intake

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
- OpenAI may process free-text course/discovery messages only after an explicit affirmative
  consent. Before consent, explain what message content is sent, that messages are stored locally,
  and to use demo text only. A decline or later opt-out must leave tap/browse functionality usable
  and must not call OpenAI for routing, retrieval, or profile extraction.
- For each extraction request, send only the current user message plus the fictional, allowlisted
  catalog vocabulary needed to normalize it; do not send names, chat IDs, contact details, or the
  full transcript. Use stateless requests (`store=false`). Do not claim this alone makes the demo
  production-safe.
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

1. Before consent, “I like numbers and helping people” results in no API call and a clear choice of
   enabling AI-guided demo chat or continuing with buttons.
2. After consent, “I enjoy organizing data and making charts; I want a diploma” extracts only
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
7. After opt-out, FAQ routing and vector retrieval receive no message text; deterministic local fee,
   payment-status, deletion, and qualification branches continue to work.

## Verification

- Test catalog coverage, unique IDs, complete facts, idempotent seed updates, and recommendation
  provenance with local SQLite only.
- Test consent display, grant, refusal, opt-out, and explicit proof that both router and embedder are
  not called when consent is absent/revoked.
- Test extraction schema, unknown/ambiguous values, parent attribution, multilingual paraphrase
  fixtures, prompt-injection text, OpenAI failure, and dynamic one-question selection with fake APIs.
- Run `bash scripts/verify.sh` and `git diff --check`. A live smoke test may use synthetic fictional
  prompts only; never use real student chat data.
- Rehearse the consent and adaptive Telegram paths manually before describing them as a live demo.

## Open production gates

Privacy/legal review including minors and guardian consent; fluent-speaker review for English,
Malayalam, Hindi, and Hinglish; adversarial extraction and safety evaluation; accurate all-level
eligibility; retention/expiry policy; deployment security, tenant isolation, monitoring, and a real
staff escalation contact/SLA. This feature alone does not make AdmitFlow production-ready.
