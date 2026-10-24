# ADR-017: Explicit demo applications for public-reference courses

Status: Accepted and enabled locally for the owner-confirmed test flow.

The owner wants each confirmed catalogue choice to proceed through application, Razorpay
test payment and human approval. They explicitly selected demo mode. ADR-016 remains the
boundary for real university offerings: public references do not establish fees, seats,
intakes or authority to admit applicants.

## Decision

- Keep courses as public references. A separate nullable database demo fee opts a course
  into a local, explicitly enabled, institution-scoped test application flow. No fake batch,
  academic rule or seat is created. The owner selected INR 3,000 (300,000 paise) per demo application.
- Persist demo markers on applications and invoices. Code permits this flow only in
  development, for the configured demo institution, with Razorpay test credentials and live
  mode disabled. Recheck those guards before provider link creation and staff approval.
- A confirmed course choice starts a labelled demo draft and reuses explicit saved details.
  Review/submit and payment confirmation remain explicit. An interest match never becomes
  an academic eligibility approval. Reference-only behavior remains when demo mode is off.
- A submitted demo application previews its database-owned test fee. Discounts cannot waive
  the required demo payment. Payment links and receipts are labelled test/demo throughout.
- Staff approve only after verified settlement. Demo approval does not decrement a university
  seat or represent university admission. Show demo labels in staff application/payment views.
- Existing signed webhook confirmation remains authoritative. A development-only, test-key
  status check may verify exact provider reference, paid link, captured payment, amount and
  currency so localhost demos can complete without public deployment. No student assertion
  or return URL can mark an invoice paid. Ordinary payments retain their existing controls.
- Do not delete existing inquiries, keys or checkpoints. Configure all 64 imported references
  through an explicit local script after migration and owner fee selection. Leave official fees and
  knowledge provenance intact. Preserve unrelated working-tree changes.

## Verification

Use test-first coverage for guards, tenant scope, every opted-in course, draft/replay safety,
real-reference restrictions, paid-before-approval, provider confirmation matching, duplicate
confirmation and seat preservation. Verify normal admissions/payment regressions, quality
and browser checks. Provider test-card completion is not claimed without actual evidence.

## Local activation and evidence

All 64 reference courses have the separate INR 3,000 test fee. The owner explicitly
approved restoring the archived BA Communication Design (Animation and VFX) option.
No batches, university prices or academic eligibility approvals were fabricated.
Existing student activity, knowledge and bot credentials/checkpoints were preserved.
The scheduler checks up to ten due demo invoices per sweep within a seven-day window,
with a per-invoice cooldown; staff can also check an older demo invoice explicitly.
Production and ordinary invoice confirmation retain the signed-webhook boundary.

See [demo verification](../event/DEMO_APPLICATIONS_VALIDATION.json) for automated,
local catalogue, provider and browser evidence. An actual test-card payment and
handset receipt of the new flow remain unverified. A private provider test link was
created, checked and cancelled without sending a Telegram message or charging money.

Rollback: disable `DEMO_ADMISSIONS_ENABLED` and restart API/worker/scheduler/receiver.
Leave the migration and explicit demo markers in place to keep submitted records
interpretable; do not downgrade after collecting demo applications or invoices.
Before any schema downgrade, back up and retire demo records with owner approval.
The migration reverses on an empty/disposable database (covered by integration tests).
