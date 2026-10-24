# AdmitFlow pitch deck

Owner: **shan**. The editable [six-slide PowerPoint](artifacts/admitflow-pitch-final.pptx)
contains actual synthetic-data product screens and speaker notes. This replaces the
older conversation-only draft. Commercial assumptions are explicitly labelled.

## Slide 1: AdmitFlow

Admissions conversations with context for your team.
Telegram for students. A workspace for institutions. Owner: shan.

## Slide 2: The admissions handoff

Students ask in chat. Staff need the course, the answers already given and the reason
behind the next step. Less repeated information collection is the product hypothesis;
customer demand and time savings remain unmeasured.

## Slide 3: A working institution workspace

Telegram collects course choices and explicit answers. Staff control the catalog,
batches and application fees. The actual catalog screenshot uses synthetic data.
Applications/review, takeover/co-pilot and consent-aware follow-ups are implemented;
the actual Razorpay test-card journey remains unverified.

## Slide 4: Answers from approved documents

PDF tables and headings stay together. OpenAI searches and reranks approved evidence.
Answers stay grounded or abstain. Student messages omit source footers; the saved
internal evidence and staff search keep document references. Digital PDF, DOCX and
text are supported; OCR is outside this version. Screenshot: actual upload controls.

## Slide 5: AI with institution control

OpenAI handles interpretation, typed extraction, embeddings and evidence reranking.
Code controls eligibility, fees, tenant access and application changes.
Live OpenAI and handset checks pass. The current backend gate has 252 default tests;
the prior full PostgreSQL run has 87 cases. See tasks/todo.md for the changed-slice run.
Stack: FastAPI, PostgreSQL/pgvector, Redis/TaskIQ and Next.js.

## Slide 6: An institution pilot

Proposed buyer: admissions teams in Kerala institutions. A paid institution workspace
is the business model to test; pricing and willingness to pay are unvalidated.
Pilot measures: repeated questions, staff review time and application completion.
Next: payment validation and an approved institution pilot. Public deployment awaits
the owner's explicit instruction.
