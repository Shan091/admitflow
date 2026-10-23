# AdmitFlow — Development Lifecycle

**This is the single source of truth for how we build AdmitFlow.** It is written to be
agent-neutral: Claude, Codex, Antigravity, Gemini, or a human should be able to read this
and drive a change end-to-end without any other context. If you only read one file, read
this one — it links to the depth.

> New here? Read this file top to bottom once, then keep it open as a checklist.

## The loop

```
understand → spec/ADR → plan/task → branch → build (TDD) → verify → review → PR → CI → merge → deploy → reflect
```

Every change — feature, bugfix, or chore — walks this loop. Small changes walk it fast;
they never skip a stage. The stages below map 1:1 to the repo's workflow triggers
(`/spec`, `/plan`, `/build`, `/test`, `/review`, `/ship` in [.agents/workflows/](../../.agents/workflows/)),
which are thin pointers — **the substance lives here.**

> This is the same Think → Plan → Build → Review → Test → Ship → Reflect sprint that
> disciplined agent teams converge on (e.g. [gstack](https://github.com/garrytan/gstack)),
> adapted to AdmitFlow's stack and quality bar.

## Ground rules (non-negotiable)

1. **`main` is protected.** Never commit directly to `main`. Every change lands via a
   feature branch and a Pull Request. See [git-and-github.md](git-and-github.md).
2. **No AI attribution in git.** Commits and PRs carry no `Co-Authored-By` or
   "Generated with…" trailers. The human is the sole author. See [git-and-github.md](git-and-github.md).
3. **The quality gate is the floor, not the goal.** `bash backend/scripts/verify.sh` must
   be green before you open a PR. See [quality-gates.md](quality-gates.md).
4. **Tests are pragmatic-TDD.** Logic-heavy and risky code is test-first; glue is
   test-after; nothing ships untested. See [testing.md](testing.md).
5. **Every PR gets an adversarial review pass** (`/review`) before merge, plus green CI.
6. **Secrets, PII, and tenant isolation are not optional.** See [security-and-production.md](security-and-production.md).

## Stages

### 1. Understand & spec  (`/spec`)
Before code: know the objective, the users, and the acceptance criteria. For anything
non-trivial or architecture-touching, confirm there is a spec ([../../SPEC.md](../../SPEC.md))
and, if a decision is being made, an ADR in [../decisions/](../decisions/). If the request
is ambiguous, ask — do not guess. **Exit:** you can state the acceptance criteria in one
sentence and point to the spec/ADR that governs them.

### 2. Plan & pick a task  (`/plan`)
Work is sliced into small, vertically-complete tasks in [../../tasks/plan.md](../../tasks/plan.md)
and [../../tasks/todo.md](../../tasks/todo.md). Pick the next unblocked task; read its
acceptance criteria and dependencies. If your change isn't a listed task, add it first.
**Exit:** a single task with clear acceptance criteria is selected and in progress.

### 3. Branch
Cut a feature branch off up-to-date `main`. Naming and conventions:
[git-and-github.md](git-and-github.md). **Exit:** you are on a `feat/…`, `fix/…`, or
`chore/…` branch, not `main`.

### 4. Build with TDD  (`/build`, `/test`)
RED → GREEN → REFACTOR. Write the failing test that describes the behavior, make it pass
with the minimum code, then clean up with tests green. For bugs, use the Prove-It pattern:
a failing test that reproduces the bug first. Follow the conventions in
[code-standards.md](code-standards.md) and the strategy in [testing.md](testing.md).
**Exit:** the behavior is implemented and covered; you did not gold-plate beyond the task.

### 5. Verify (the quality gate)
Run the full local gate — the same steps CI runs:
```bash
bash backend/scripts/verify.sh
```
This runs ruff (lint), ruff format check, mypy `--strict`, and pytest. It must be green.
Scale-up gates (integration, observability, security) apply by what the change touches —
see the tiered table in [quality-gates.md](quality-gates.md). **Exit:** the gate is green
at the tier your change requires.

### 6. Self-review, then adversarial review  (`/review`)
First re-read your own diff against the five axes (correctness, readability, architecture,
security, performance). Then run an **adversarial review pass** — a fresh agent (or you,
deliberately trying to break it) reviews the diff for bugs, security holes, and drift from
the spec. On changes that touch an external surface, PII, or money, review through a
threat lens too (untrusted input, authz, tenant scope — OWASP/STRIDE-style) as covered in
[security-and-production.md](security-and-production.md). Address findings; don't wave them
through. **Exit:** no open Critical/Important findings.

### 7. Commit & open the PR
Commit in small, coherent steps using Conventional Commits, push the branch, and open a PR
with a summary, test evidence, and anything intentionally out of scope. Exact format and
the no-attribution rule: [git-and-github.md](git-and-github.md). **Exit:** PR is open and
describes what changed, why, and how it was tested.

### 8. CI → merge
CI ([.github/workflows/ci.yml](../../.github/workflows/ci.yml)) runs the same gate on the
PR. Merge only when CI is green **and** the review is clean. Squash-merge to keep `main`
history linear; delete the branch. **Exit:** the PR is merged; the task checkbox in
[../../tasks/todo.md](../../tasks/todo.md) is ticked.

### 9. Deploy & confirm  (`/ship`)
Production readiness (secrets set, migrations applied, observability wired, rollback known)
is covered in [security-and-production.md](security-and-production.md). **Exit:** the change
is live, health checks pass, and traces/logs look sane.

### 10. Reflect & learn
Close the loop. After a change ships, spend a moment on what the codebase should remember:
- If a bug reached this stage, confirm the regression test that now guards it exists (Prove-It).
- If a decision was made, record it — a new/updated ADR in [../decisions/](../decisions/), or a
  number in [../../CONSTRAINTS.md](../../CONSTRAINTS.md).
- If the process itself was wrong or missing something, fix *this handbook* and the per-agent
  pointers, not just the code.

Keep it lightweight — a few lines, not a ceremony. **Exit:** durable learnings are written
down where the next person (or agent) will find them, not left in your head.

## Reference docs

| Topic | File |
|-------|------|
| Branching, commits, PRs, review gate, no-AI-attribution | [git-and-github.md](git-and-github.md) |
| Test strategy, TDD, unit vs integration, running tests | [testing.md](testing.md) |
| Definition of done, the tiered gate, CI mirror | [quality-gates.md](quality-gates.md) |
| Python conventions, structure, typing, logging, errors | [code-standards.md](code-standards.md) |
| Secrets, PII, tenant isolation, auth, deploy readiness | [security-and-production.md](security-and-production.md) |
