# Feature: FAQ vector search

## Outcome

Answer seeded knowledge questions from institution FAQ chunks using OpenAI embeddings and local
cosine search, with a reliable abstention path.

## Acceptance criteria

- [x] FAQ question/answer chunks are embedded in batches with `text-embedding-3-small`.
- [x] Embeddings are tenant-scoped in SQLite and reused while the content hash/model match.
- [x] Query vectors are ranked with cosine similarity; initial min score is `0.72` and margin
  `0.05`; deterministic fake-vector cases verify accept/abstain behavior.
- [x] Weak or ambiguous matches abstain; embedding/search failure never triggers an ungrounded answer.
- [x] Fee questions route to structured pricing before retrieval; FAQs contain no price amounts.
- [ ] Calibrate thresholds using live embeddings and expected question variants.

## Verification

- [x] Fixed-vector known, weak, and ambiguous queries select or abstain as expected.
- [x] Fee queries use structured course data.
- [ ] Automated checks use fixed/fake vectors; one live embedding smoke check is recorded
  separately before the demo.
- [x] Run `bash scripts/verify.sh`.
