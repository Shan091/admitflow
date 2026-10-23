# AI Impact Statement

AdmitFlow uses OpenAI to interpret admissions messages, extract explicitly supplied
eligibility facts, translate retrieval queries and select supporting document passages.
OpenAI embeddings support search over institution-approved PDF, DOCX and text
references. Model identifiers and credentials remain server configuration.

Code evaluates institution-defined eligibility rules, validates course and batch choices,
and controls staff-request states. Eligibility does not grant admission or reserve a seat.
The assistant returns source quotations and abstains when it cannot support an answer.
Human requests pause automated qualification until staff explicitly resume it.

The demonstration uses synthetic institution material and student test answers.
Routing identifiers, conversation content and eligibility memory are encrypted in
application storage. Tenant-scoped access, expiring staff sessions and adversarial tests
protect institutional boundaries. Live OpenAI checks and a user-confirmed Telegram
roundtrip have passed. Language fluency and real-applicant outcomes remain unvalidated.

Our intended impact is less repeated information collection and clearer staff review
of admissions inquiries. We have not measured conversion improvements, revenue or
staff time savings. Institution material requires approval and appropriate rights before
ingestion. A real pilot requires additional privacy and operational review.
