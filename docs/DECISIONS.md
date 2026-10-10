# Project decisions

Record consequential choices here. Each entry is short; update it when evidence changes a choice.

1. **Demo channel — Telegram webhook through FastAPI.** Telegram sends updates to the public
   HTTPS `/api/v1/webhooks/telegram` route using a configured secret-token header. The app does not
   run `getUpdates` polling; registering or clearing the webhook is an operator action.
2. **Runtime and persistence — one FastAPI process and SQLite.** This is enough for one seeded
   demo tenant; no Redis, TaskIQ, Postgres, or separate frontend in this scope.
3. **Architecture — domain/services/adapters.** Keep one real adapter per boundary; introduce a
   small Protocol only where injection or a test double needs it. No speculative ports framework.
4. **Eligibility and fees — code-owned.** Structured seed data and Python rules determine
   eligibility and prices; model output cannot change either.
5. **Knowledge retrieval — OpenAI embeddings + SQLite vectors + NumPy cosine.** Embed seeded
   FAQ question/answer chunks with `text-embedding-3-small`; no general upload/parser or vector DB.
6. **Fail-closed retrieval and initial thresholds.** Begin at cosine `0.72` and top-result margin
   `0.05`; calibrate against fixed demo cases. These are provisional, not guarantees. Abstain on
   weak, ambiguous, or unavailable retrieval.
7. **Fee routing and fee payment.** Route price questions to structured course data before RAG;
   exclude amounts from free-form FAQ chunks. Qualified demo applicants may receive a Razorpay
   Payment Link created in test mode from the server-owned course fee. Never accept a client amount
   or mark a payment paid from a browser redirect; accept only signature-verified webhooks. Live
   payments, refunds, uploads, and production finance workflows are deferred.
8. **Staff dashboard access.** Protect dashboard routes with one environment-configured staff
   username/password and a signed, HTTP-only, SameSite=Lax session cookie. No self-registration,
   roles, or production identity provider in the hackathon demo. Missing credentials fail closed.

## References

- OpenAI embeddings: https://developers.openai.com/api/docs/guides/embeddings
- OpenAI Decisions: https://developers.openai.com/api/docs/guides/decisions
- Python Telegram Bot async lifecycle:
  https://github.com/python-telegram-bot/python-telegram-bot/wiki/Frequently-requested-design-patterns
- Razorpay Payment Links API: https://razorpay.com/docs/api/payments/payment-links/
- Razorpay webhook security checklist: https://razorpay.com/security/checklist/
