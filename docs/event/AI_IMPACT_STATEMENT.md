# AI Impact Statement

AdmitFlow uses the configured OpenAI gpt-4.1-mini model for interpreting admissions
messages, extracting explicit facts, resolving references, reranking evidence and
selecting exact quotations. text-embedding-3-small supplies document embeddings.
Digital PDFs use offline pretrained Docling layout/TableFormer models; DOCX/text
extraction preserves structure. No fine-tuning or OCR is used.

Code controls eligibility, fees, authorization and consequential changes. Eligibility
confers neither admission nor a reserved seat. Tenant-scoped retrieval, relevance
checks and exact-quote validation prevent unsupported answers; missing evidence
produces abstention. Source references remain internal, while staff search displays
them. Staff requests pause automation until explicit resume.

The demonstration uses authored synthetic institution material and student answers,
without a public training dataset or real applicant records. Owner shan licenses
project source under MIT. Third-party code/models retain upstream terms; Docling
model cards identify Apache-2.0 and CDLA-Permissive-2.0. OpenAI is accessed as a
hosted API. See DATA_PROVENANCE.md for sources and limits.

Encrypted identifiers/conversations, scoped staff sessions, bounded workers and
deletion/retention controls protect institutional data. Live OpenAI, uploaded-PDF
and handset checks pass. General language fluency and real-applicant outcomes
remain unvalidated. Reduced repetition and clearer staff review are intended
benefits; revenue, conversion gains and time savings have not been measured.
