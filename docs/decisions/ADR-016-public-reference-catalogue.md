# ADR-016: Public programme references and an explicit local demo reset

Status: Accepted

## Context

The owner requested deletion of existing dummy data and replacement with public
JAIN (Deemed-to-be University), **Kochi** information, using SerpAPI for discovery.
The owner will fill the Razorpay API credentials; only placeholders are requested now.
Admin access, bot connection and secrets must remain usable.

Public listings establish that a programme option was published. They do not establish
current intake capacity, fees, admission approval or authority for this demonstration
to collect university applications or money.

## Decision

- Discover sources with SerpAPI; fetch the official
  [Kochi directory](https://www.jainuniversity.ac.in/kochi/programs.php), six department
  listings and 64 linked detail pages. Search snippets are leads, not verified facts.
  The snapshot is [catalogue.json](../../backend/data/jain-kochi/catalogue.json).
- Keep source/listing URLs, study level and degree names. Paraphrase overview,
  eligibility and duration; preserve missing/conflicting information as unverified.
  These are 64 published **options**, including specializations, not a claim of 64
  independently accredited degrees or confirmed current intakes.
- Add `Course.is_reference` and `reference_url`. References are explorable without
  fabricated batches/seats. Known failed configured rules still fail; reference mode
  never grants eligibility, even if a batch is added.
- Course controls explore information without selecting an admissions intake,
  collecting an application or requesting payment. Fee answers and the dashboard
  show **unverified**, never the internal zero placeholder as a free application.
  Institution-configured admissions offerings retain existing behavior.
- Reference records are read-only in catalogue editing and can be archived. A normal
  edit cannot turn a scraped reference into a live admissions offering.
- Index one campus/contact document and one per option with OpenAI embeddings.
  Keep tenant/course scope, encrypted upload sources, official URL metadata and ready
  uploads. Existing RAG support checks and reranking remain active.
- Label the institution as an independent public-information demo. Do not imply
  official representation, live seats, fees or admissions/payment authorization.
- Reset only the explicitly named loopback development database with `--apply`.
  Validate dummy institution names, one preserved admin and absence of payment orders.
  Prepare all embeddings before deletion. Delete/import in one transaction. Preserve
  login credentials, sessions, bot token and polling high-water mark. Remove the unused
  synthetic tenant, old student activity, fake courses/intakes/rules/discounts, documents
  and test audit entries; write a fresh reset audit event. Clear only these tenants'
  Redis budget counters. Never flush shared Redis or delete other database volumes.
- Quiesce writers first: an operator requirement, not automatic process shutdown.
  Reject incomplete embedding sets and nonofficial URLs. Skip synthetic seeding when
  a reference catalogue exists. Keep SerpAPI and webhook secrets in ignored `.env`,
  initially leave Razorpay API placeholders empty. After the owner supplies test values,
  verify them with a read-only provider probe and save institution credentials encrypted.
  Live payments remain disabled.

## Evidence and limits

Quality gates, real PostgreSQL reset/rollback/reference/application/payment cases and
desktop/mobile UI checks verify boundaries. Synthetic OpenAI calls check graduate and
undergraduate guidance and the indexed campus answer; temporary leads are rolled back,
with no Telegram test send. Evidence: `JAIN_KOCHI_VALIDATION.json` and
`JAIN_KOCHI_RELEASE.json` under `docs/event/`.

Summaries are not official admissions decisions. Public pages may be outdated or
inconsistent. Regulatory, ranking, earnings and outcome claims were not independently
verified. Model guidance remains probabilistic and exploratory. Razorpay credential
verification and encrypted provisioning passed after the owner supplied test values.
A public test webhook and actual test-card validation await authorized test ingress. No public deployment occurred. The separate
Compose application database is outside this reset; the target is local dashboard
port 3000 / API port 8000.
