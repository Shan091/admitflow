# Feature: FAQ vector search

## Outcome

Answer seeded knowledge questions from institution FAQ chunks using OpenAI embeddings and local
cosine search, with a reliable abstention path.

## Acceptance criteria

- [ ] FAQ question/answer chunks are embedded in batches with `text-embedding-3-small`.
- [ ] Embeddings are tenant-scoped in SQLite and reused while the content hash/model match.
- [ ] Query vectors are ranked with cosine similarity; initial min score is `0.72` and margin
  `0.05`, then calibrated using fixed examples.
- [ ] Weak or ambiguous matches abstain; API failure never triggers an ungrounded answer.
- [ ] Fee questions route to structured pricing before retrieval; FAQs contain no price amounts.

## Verification

- [ ] Known queries find expected chunks; unrelated and ambiguous queries abstain.
- [ ] Fee queries use structured course data.
- [ ] Automated checks use fixed/fake vectors; one live embedding smoke check is recorded
  separately before the demo.
- [ ] Run `bash scripts/verify.sh`.
