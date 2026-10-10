# Feature: FAQ vector search

## Outcome

Answer seeded knowledge questions from institution FAQ chunks using OpenAI embeddings and local
cosine search, with a reliable abstention path.

## Acceptance criteria

- [x] Each FAQ's canonical question and a few curated search phrasings are embedded in one vector
  with `text-embedding-3-small`; answers remain separate from the search text.
- [x] Embeddings are tenant-scoped in SQLite and reused while the content hash/model match.
- [x] Query vectors are ranked with cosine similarity; calibrated min score is `0.58` and margin
  `0.05`; deterministic fake-vector cases verify accept/abstain behavior.
- [x] Weak or ambiguous matches abstain; embedding/search failure never triggers an ungrounded answer.
- [x] Fee questions route to structured pricing before retrieval; FAQs contain no price amounts.
- [x] Calibrate with live embeddings: 15 expected FAQ variants and 12 unsupported queries passed;
  lowest expected score `0.648`, highest unsupported score `0.491`.

## Verification

- [x] Fixed-vector known, weak, and ambiguous queries select or abstain as expected.
- [x] Fee queries use structured course data.
- [x] Automated checks use fixed/fake vectors; the live evaluator is separate and uses fictional
  questions only. The final 27-question embedding request used 207 input tokens.
- [x] Run `bash scripts/verify.sh`.
