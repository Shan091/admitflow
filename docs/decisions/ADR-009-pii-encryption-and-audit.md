# ADR-009: Application-Layer PII Encryption and Audit Logging

## Status
Accepted


## Context
AdmitFlow stores applicant personal data — WhatsApp phone numbers, names, and
later emails — for institutions in India, so it must satisfy the DPDPA (India's
data-protection law). Two obligations drive this decision:

1. **Confidentiality at rest.** If the database (or a backup/dump) is ever
   exposed, raw applicant PII must not be readable.
2. **Accountability.** Significant actions on that data (status changes,
   payments, deletions, human takeover) must be attributable — who did what,
   when — per SPEC §12 and §14.

The managed Postgres provider (Neon, ADR-007) already encrypts data on disk,
but that only protects against someone stealing the physical disk. It does
**not** protect against a leaked connection string, a compromised query path, or
an accidental data export — in all of those the provider hands back plaintext.
We needed protection that travels with the data itself.

Lead rows also need to be found by phone number (dedup on inbound WhatsApp
messages, "Delete My Data" lookups). If the phone number is encrypted
non-deterministically, we cannot search for it directly, because the same number
encrypts to different ciphertext every time.

## Decision
**Encrypt PII in the application layer before it reaches the database, and keep
a deterministic keyed hash alongside it for lookup.** Record significant actions
through a single append-only audit helper.

- **Encryption** (`backend/src/core/security.py`): `encrypt_pii` / `decrypt_pii`
  use **Fernet** (from the `cryptography` library) — authenticated symmetric
  encryption (AES-128-CBC + HMAC) with a random IV per message. The master key
  lives in settings (`PII_ENCRYPTION_KEY`), sourced from the platform secret
  store in production. Ciphertext is stored in the `*_enc` columns (`phone_enc`,
  `name_enc`).
- **Lookup hash**: `hash_phone` is a **keyed HMAC-SHA256** of the phone number
  (key = `PHONE_HASH_KEY`), stored in `leads.phone_hash` and covered by
  `UniqueConstraint(tenant_id, phone_hash)`. Deterministic, so we can look a lead
  up by number; keyed, so the stored digests can't be reversed with a
  precomputed table of all phone numbers.
- **Fail-closed**: the keys are optional in `Settings` so the app still boots
  without them, but the crypto helpers raise `EncryptionKeyNotConfiguredError`
  the instant they are used while a key is unset — the same contract as
  `DatabaseNotConfiguredError`. We never silently store plaintext.
- **Audit** (`backend/src/db/audit.py`): `write_audit_log(...)` is the single
  path significant actions take into the append-only `audit_logs` table. It
  requires `tenant_id` (tenant scoping is mandatory), references records by id
  only, and must never carry raw PII in its free-form `details`.

## Alternatives Considered

### Rely on the provider's at-rest encryption only
- Pros: zero application code.
- Cons: protects only against physical disk theft; a leaked DSN or an export
  returns plaintext. Rejected — insufficient for DPDPA.

### Full envelope encryption (per-tenant data keys wrapped by a master key)
- Pros: finer blast-radius control; rotate one tenant's key independently.
- Cons: materially more moving parts (key hierarchy, wrapping/unwrapping,
  storage of wrapped keys). Deferred — a single master Fernet key meets the
  current bar; the `security.py` surface is small enough to upgrade later
  without touching call sites.

### Deterministic encryption of the phone number (so it is both stored and searchable)
- Pros: one column instead of two.
- Cons: deterministic encryption leaks equality and is weaker. Rejected in
  favour of non-deterministic ciphertext (`phone_enc`) **plus** a separate keyed
  hash (`phone_hash`) for search — the standard split.

## Consequences
- Every write of applicant PII must go through `encrypt_pii`, and every lead
  lookup/dedup must go through `hash_phone`. Call sites land with the webhook
  ingress (Task 5) and the engine.
- **Phone numbers must be E.164-normalized by the caller before hashing.** The
  hash is byte-exact, so `"+919876543210"` and `"919876543210"` would create
  duplicate leads. Normalization is the ingress's job (documented on
  `hash_phone`), not the crypto primitive's.
- Two secrets (`PII_ENCRYPTION_KEY`, `PHONE_HASH_KEY`) must be set in every
  non-local environment. Losing `PII_ENCRYPTION_KEY` means the encrypted PII is
  unrecoverable; key rotation needs a migration (re-encrypt) and is a follow-up.
- Follow-ups: fail-at-boot validation that both keys are set when
  `app_env == "prod"`, and wrapping a malformed-key error into
  `EncryptionKeyNotConfiguredError` for a consistent fail-loud story.
