# ADR-015: Supportive guidance and contextual answer controls

Status: Accepted

## Context

A reported novice journey repeatedly asked for projects and technologies, while
offering no helpful answer controls. The student needs a supportive conversation
that learns consequential background and preferences, checks real prerequisites
and explains feasible courses. Examples of useful information are not a required
question sequence.

## Decision

- Apply the research-to-behavior mapping in
  [ADAPTIVE_GUIDANCE_RESEARCH.md](../engineering/ADAPTIVE_GUIDANCE_RESEARCH.md):
  flexible CIP/CASVE decision purposes, tentative RIASEC activity themes, distinct
  interests/skills/values, and OARS listening principles. These sources support the
  design; they do not validate generated questions, a Kerala assessment or outcomes.
- Keep the existing OpenAI interpretation/planning and code-owned catalogue,
  eligibility, consent, staff ownership and selection boundaries. No training,
  copied test items, new assessment vendor or mandatory questionnaire.
- Generate short contextual answer options when they lower effort. Add an
  uncertainty option; keep free text available. Precise academic facts use text,
  never suggested ages/marks. Course cards retain their explicit selection controls.
- Sign answer references with the existing lead/bot HMAC. Store labels encrypted in
  conversation memory behind a fresh nonce; consume once. A subsequent text turn,
  replacement offer or confirmed reset invalidates the offer. Existing message-ID
  reset floors and staff/submitted locks apply. Stale taps cannot consume a newer offer.
- Persist only a verified clicked label with the encrypted normalized event, so
  staff transcripts and model history see the actual answer. External Telegram JSON
  cannot set that internal field. Offering an option never creates profile evidence;
  choosing a label equal to a course name never invokes the direct-name selector.
- Reject recognizable portfolio/technology proof questions during ordinary
  exploration. After two ordinary or three deeper questions without accepted new
  profile/fact information, offer a gentle next-step choice. Useful new information
  resets this safeguard; actual eligibility questions are exempt. This is a recovery
  mechanism, not a theory-mandated question count. An explicit deeper request restarts
  exploration. The policy still asks for timely supported options and honest gaps.
- An unanswered prerequisite is not repeated unchanged: offer to explore or return to
  entry checks. Recommendation evidence must come from a stated interest, strength,
  value, goal or course preference; schooling alone cannot establish interest fit.
- Use the same response composer in production processing and bounded live-provider
  evaluations. Choices and recovery add no model request. Retain ADR-014 typing,
  confirmed reset and latency optimizations.

## Consequences and limits

The bot adapts its next purpose rather than forcing background, interest, eligibility
and recommendation into a universal order. Unknown prerequisites remain unknown;
preliminary interest fit does not imply admission. No verified offering means an
honest gap rather than an unrelated substitute.

Generated conversation remains probabilistic. The interview-pattern check catches
the reported class of prompts, not every possible poor question. Synthetic tests
cover state, controls and representative provider behavior; real-student outcomes
and psychometric validity have not been measured. Evidence and verification counts
are recorded with Task 63, rather than inferred from these decisions.
