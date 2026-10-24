# AI Impact Statement

AdmitFlow uses OpenAI to interpret admissions messages, extract explicitly supplied
facts, resolve conversational references, embed approved documents, rerank evidence
and select supporting quotations. Digital PDFs use offline pretrained Docling layout
and table models; DOCX/text extraction preserves source structure. No decision-model
fine-tuning or OCR is used. Credentials and model configuration remain server-side.

Code owns eligibility rules, prices, course/batch choices, authorization and consequential
changes. Eligibility grants neither admission nor a seat. Unsupported questions receive
abstention; staff requests pause automation until an explicit resume.

The demonstration uses synthetic institution material and student answers. Identifiers,
conversation content and eligibility memory are encrypted in application storage.
Tenant-scoped access, expiring staff sessions, bounded workers, deletion/retention controls
and adversarial checks protect institutional boundaries. Live OpenAI, document-search
and user-confirmed Telegram checks have passed. Language fluency and real-applicant
outcomes remain unvalidated.

The intended impact is less repeated information collection and clearer staff review.
Conversion gains, revenue and time savings have not been measured. Institutions must
authorize reference material and its use. A real pilot requires operational and privacy
review; final source-code licensing remains an owner decision.
