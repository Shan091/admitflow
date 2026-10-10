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
5. **Knowledge retrieval — OpenAI embeddings + SQLite vectors + NumPy cosine.** Embed each seeded
   FAQ's canonical question plus a few curated search phrasings with `text-embedding-3-small`;
   keep the answer as a separate stored value. Version the cached-vector key when this text profile
   changes. No general upload/parser or vector DB.
6. **Fail-closed retrieval and calibrated initial thresholds.** Use cosine `0.58` and top-result
   margin `0.05`; a live fixed set passed 15 expected FAQ variants and abstained on 12 unsupported
   questions. Its lowest expected score was `0.648`, and highest unsupported score was `0.491`.
   These small synthetic cases are calibration evidence, not guarantees. Abstain on weak,
   ambiguous, or unavailable retrieval.
7. **Fee routing and fee payment.** Route application-fee questions to structured course data
   before RAG; send unknown tuition/hostel charges and refund requests to an explicit safe response.
   Exclude amounts from free-form FAQ chunks. Qualified demo applicants may receive a Razorpay
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
