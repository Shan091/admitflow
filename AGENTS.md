# Agent instructions

This repo is being built for DevDay Exchange Community Hackathon: Kochi. Follow the event's
official rules: start implementation from scratch at the event, keep changes simple, document
actual work, protect credentials, and keep a timely Git history. Do not copy implementation
code from `Documents/v1`; use its product notes only as context.

## Build loop

1. Read `SPEC.md`, `docs/DECISIONS.md`, and the selected feature brief under `tasks/features/`.
2. Update `tasks/todo.md` before work; write acceptance criteria and dependencies.
3. Test-first for domain rules and retrieval policy; tests may use fake APIs, not live paid calls.
4. Run `bash scripts/verify.sh`. Record exact commands and real results in `CHANGELOG.md` and,
   when appropriate, `README.md` or `SUBMISSION.md`.
5. Review the diff for correctness, secrets, and misleading demo claims. Commit coherent
   milestones; update `AI_USAGE.md` for meaningful Codex assistance.

The source event rules are in the [hackathon template repository](https://github.com/anima-regem/devday-kochi-hackathon-template/blob/main/RULES.md).

## Project rules

- Python 3.12, FastAPI, Telegram webhook delivery, SQLite, NumPy, OpenAI API.
- Eligibility and fees are computed from seeded structured data, never from model output.
- Retrieval is tenant-scoped and fail-closed. Do not send an answer when indexing/search fails.
- Do not put real keys, participant private data, or `.env` in Git.
- Mark a task `[x]` only after its acceptance criteria have been verified and the milestone
  committed. Report test results for the commit that is pushed; never invent a green check.
- No AI-attribution trailers in Git commit messages.
