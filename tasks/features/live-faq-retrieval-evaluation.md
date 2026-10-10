# Feature: Live FAQ retrieval evaluation

## Outcome

Calibrate the small seeded FAQ retriever against a repeatable set of fictional paraphrases and
out-of-scope questions using live OpenAI embeddings, without building a document-ingestion system.

## Acceptance criteria

- [x] The evaluator indexes/reuses the seeded corpus through the normal repository and embedding
  services; it does not print API keys or send applicant information.
- [x] Fixed expected-answer and abstention cases report expected source, actual source, top score,
  score margin, and pass/fail.
- [x] Evaluation uses the same retrieval decision path and configured thresholds as Telegram.
- [x] Any threshold changes have measured evidence and preserve fail-closed behavior for
  out-of-scope and ambiguous cases.
- [x] Results and API usage are recorded truthfully; no real user content is added to the fixture.

## Dependencies and decisions

- Dependencies: seeded FAQ vectors, configured OpenAI embedding key, SQLite demo database.
- Decisions: `docs/DECISIONS.md` #5 and #6; `text-embedding-3-small`, SQLite vectors, NumPy cosine,
  curated search phrasings, minimum cosine `0.58`, top-result margin `0.05`, abstain if uncertain.

## Verification

- [x] Run the evaluator with configured live credentials and capture only aggregate/sample scores;
  27/27 passed with the recorded thresholds.
- [x] `bash scripts/verify.sh` passed (37 tests); `git diff --check` passed.
- [ ] Record the exact pushed SHA and matching GitHub Actions result.

## Risks and limitations

- Small hand-authored cases are a smoke/calibration set, not a statistical quality guarantee.
- OpenAI API usage is billable; fixture queries are short and fictional.
