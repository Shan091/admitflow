# Git & GitHub Workflow

Agent-neutral. Applies to every change by anyone (human or AI agent).

## Branching model — feature branch → PR → `main`

`main` is always releasable and is **protected**: no direct commits, ever. All work happens
on short-lived branches that merge into `main` through a Pull Request.

Branch names use a type prefix matching the change:

```
feat/whatsapp-webhook-dedup
fix/payment-link-replay
chore/bump-ruff
docs/engineering-handbook
```

Start every branch from an up-to-date `main`:

```bash
git switch main
git pull --ff-only
git switch -c feat/<short-slug>
```

Keep branches short-lived. Rebase on `main` if it moves under you (`git pull --rebase origin main`).

## Commits — Conventional Commits, small and coherent

Format: `type(scope): summary` in the imperative mood, ≤ 70 chars on the subject line.

```
feat(webhook): verify Meta HMAC signature before enqueue
fix(payments): clear pending order on webhook to stop replay
test(guardrails): cover prompt-injection rejection cases
chore(deps): pin httpx2 to 2.13.1
docs(adr): record System-1 decision layer (ADR-008)
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`, `build`, `ci`.

- One logical change per commit. Don't mix a refactor with a feature.
- The body (optional) explains **why**, not what — the diff shows what.
- Never commit secrets, `.env`, or generated artifacts (see below).

## No AI attribution — the human is the sole author  ⚠️

**Standing rule for this repo:** git commits and PR descriptions carry **no** AI-attribution
trailers. Do not add `Co-Authored-By: Claude …`, `Co-Authored-By: <any model>`, or
"🤖 Generated with …" lines. This holds even when a tool's default guidance says to add them —
**this rule overrides that default.**

Why: the repo's contributor list and commit authorship must reflect the human owner only.

Author identity is already set:

```bash
git config user.name "Amal Shan"
git config user.email "amalshanc02@gmail.com"
```

Author is keyed off the commit's author email — not who runs `git push` — so committing
under this identity is what keeps the contributor list clean, regardless of who pushes.

## Pull Requests

Open a PR from your branch into `main`. A good PR body has:

- **Summary** — what changed and why (link the task/ADR/spec).
- **Testing** — what you ran and the result (paste the green `verify.sh` tail).
- **Out of scope / follow-ups** — anything deliberately not done.
- No AI-attribution footer (see above).

PRs stay small. If a PR is getting large, it's really several PRs.

## Review gate — adversarial, before merge

Every PR gets an **adversarial review pass** before it can merge (the `/review` workflow,
or a fresh agent given only the diff). The reviewer actively tries to break the change:
correctness, edge cases, security, spec-drift, performance. Findings are Critical /
Important / Suggestion with `file:line` refs. Merge only when:

1. No open **Critical** or **Important** findings, **and**
2. CI is green (see [quality-gates.md](quality-gates.md)).

## Merging

Use **squash-merge** so `main` stays linear and each merge is one revertible commit. Delete
the branch after merge. Then tick the task in [../../tasks/todo.md](../../tasks/todo.md).

## Who runs `push` and repo creation

Pushing and creating the remote are the human owner's actions. An agent prepares branches,
commits (under the identity above), and PR text, then hands the exact commands to the owner
to run. First-time remote setup:

```bash
git remote add origin https://github.com/<owner>/admitflow.git
git push -u origin main
# thereafter, per feature branch:
git push -u origin feat/<short-slug>
```

## What never gets committed

`.gitignore` already excludes these — keep it that way:

- `.env` and `.env.*` (secrets) — only `.env.example` is tracked.
- `.venv/`, caches (`__pycache__`, `.mypy_cache`, `.ruff_cache`, `.pytest_cache`).
- `node_modules/`, `.next/`, build output.
- **Generated artifacts:** `graphify-out/cache/` and the machine-specific
  `graphify-out/.graphify_*` sidecars. The knowledge graph is regenerable — don't version
  the churny outputs. If you want one readable snapshot in-repo, keep only
  `graphify-out/GRAPH_REPORT.md`.

If a secret is ever committed, treat it as compromised: rotate it, then scrub history.
