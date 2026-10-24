# ADR-014: Natural collection, context reset and responsive replies

Status: Accepted. Task 62 follows the owner's walkthrough of separate message examples;
the pasted examples were not evidence of conflicting replies.

## Decision

- A confirmed course and intake with code-verified entry rules can start an encrypted
  draft without a separate application menu. Submission always needs a final explicit
  review/confirmation. No seat is reserved or admission granted by creating a draft.
- Reuse only explicitly supplied, validated application details. Structured OpenAI
  extraction supports multiple fields and corrections. Greetings, acknowledgments,
  questions and refusals are not personal field values. Never infer birthdate from age.
- Keep repeated collection prompts short. Explain submission/review at the beginning
  and final review, rather than repeating storage implementation details at every turn.
  `/pause` preserves a draft; `/apply` resumes; `/cancel` explicitly discards a draft.
  Course exploration and questions can interrupt collection without forcing submission.
- `/reset` requires a signed, one-use confirmation. It clears profile/facts/draft and
  records a model-history boundary. Earlier transcripts stay available to authorized
  staff under existing retention/privacy controls, but are excluded from model context.
  Old course/application buttons are rejected using the confirmed reset message boundary.
- Reset preserves submitted applications/payments, opt-out/consent preferences and
  active staff ownership. It cannot reopen an already submitted case as a new application
  or bypass a safety/staff hold. Reset before submission provides a fresh testing flow.
- Typing uses Telegram's [sendChatAction](https://core.telegram.org/bots/api#sendchataction).
  The provider clears it when a message arrives and expires it within five seconds.
  Start after 350 ms, renew every four seconds, bound each attempt to 1.5 seconds and
  stop on failure or completion. No retry, message content, outbox row or daily-send
  charge is attached to typing; its failure never fails the durable reply.
- Preserve two-step interpretation/planning for free-form guidance with corrected facts.
  Remove the redundant outer classifier on discovery and redundant qualification
  extraction. An unambiguous number answering the displayed eligibility field uses
  the same typed limits/evidence/rule/audit path without a model call. No inferred facts.
- Load at most 20 model-context entries in bulk, with one additional tenant-scoped
  catalog-name lookup for callbacks. Keep staff pagination/audit history unchanged.
- Accept punctuation after a numerical academic fact and equivalent decimal spellings,
  without matching a prefix of a different number. Conservatively supplement omitted
  literal `age 19, marks 65` statements; hypothetical/third-party/requirements contexts
  are excluded. A directly named verified course can be proposed without inventing a
  fit explanation, while selection still requires code-owned confirmation.

## Evidence and limits

`CONVERSATION_EVALUATION_RESULTS.json` records five synthetic collection cases with
model-call counts and local elapsed times. This small sample is not a production
percentile or a before/after speedup.
`CONVERSATION_RELEASE_RESULTS.json` records the tested source and final gates.
Earlier failing synthetic evaluations are retained privately during development;
the final guidance report records the subsequent regression run. No real student
outcome, new handset receipt, typing observation or public deployment is claimed.
