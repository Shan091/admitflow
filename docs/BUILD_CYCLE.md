# Feature build cycle

Use this loop for each feature. Keep the feature brief and `tasks/todo.md` synchronized.

1. **Understand:** Read `SPEC.md`, relevant entries in `docs/DECISIONS.md`, and current repo
   state. State the user outcome and what is excluded.
2. **Specify:** Create/update a feature brief with acceptance examples, dependencies, risks, and
   verification commands. Add a decision entry only when a load-bearing choice is made.
3. **Slice:** Break work into small vertical tasks with an owner, dependencies, and checkbox.
4. **Build:** Test-first for domain, eligibility, retrieval, and other risk-heavy logic; test-after
   for thin glue. Use fakes in automated tests for paid/network APIs.
5. **Verify:** Run the relevant focused checks, then `bash scripts/verify.sh`. Record actual
   output/results, including failures or checks unavailable due to missing credentials.
6. **Review:** Inspect the diff for behavior, tenant scoping, credential/PII leakage, and claims
   that overstate the demo. Address important findings.
7. **Record and commit:** Update README when behavior/setup changes, CHANGELOG with timestamp,
   files, validation, and limitations, and AI_USAGE for meaningful AI assistance. Commit a
   coherent milestone; push to the authorized repo and check CI on that exact SHA.
8. **Close:** Mark the task complete only when its acceptance criteria are verified and the
   milestone is committed. Record remaining limitations and next task.

The event's instructions take precedence over v1's protected-main/PR workflow where they differ.
