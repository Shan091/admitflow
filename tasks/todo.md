# Hackathon implementation checklist

Update this checklist at the start of each work slice. A checkbox is complete only after its
acceptance criteria pass and the corresponding milestone is committed.

## Foundation and repository

- [x] Confirm feature scope, decisions, and dependency order against `SPEC.md` and `docs/DECISIONS.md`.
- [x] Install the locked Python 3.12 environment and record the lockfile.
- [x] Verify seed/schema initialization, configuration, health endpoint, dashboard, and CI setup.
- [x] Commit and push the verified foundation milestone; record its exact test commands/results.

## Telegram course discovery and qualification

- [x] Test eligible, ineligible, malformed, missing, and boundary qualification inputs.
- [x] Test lead/message persistence and idempotent handling of duplicate Telegram updates.
- [x] Test Telegram flow service behavior with fake updates; no live API in automated tests.
- [x] Verify dashboard lead list/detail from the same SQLite records.
- [ ] Complete and record a live Telegram walkthrough when a bot token is configured.

## FAQ embeddings and vector retrieval

- [x] Test vector packing during seed indexing, cosine ranking, dimension mismatch, and tenant scoping.
- [x] Test embedding reuse/content invalidation, score threshold, margin, and fail-closed behavior.
- [x] Test fee questions use structured prices before intent routing or FAQ retrieval.
- [x] Verify fixed expected question-to-FAQ matches with fake vectors.
- [ ] Calibrate similarity and margin thresholds using live embedding/query examples.
- [ ] Run and separately record a live OpenAI embedding smoke check when a key is configured.

## Final verification and submission

- [x] Run `bash scripts/verify.sh`; record actual output and results in `CHANGELOG.md` and `SUBMISSION.md`.
- [x] Review diff, claims, credentials, and AI usage record; ensure no real applicant data is seeded.
- [ ] Confirm GitHub Actions result for the pushed commit SHA and update submission record.
- [ ] Rehearse demo, record limitations and demo access steps, and finalize submission metadata.
