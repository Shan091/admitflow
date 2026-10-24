# Student-to-staff demonstration

Use the synthetic institution and catalog. Confirm that the API, knowledge/Telegram
worker, receiver and staff frontend are running. Keep credentials and terminals with
private configuration out of the recording. No real applicant documents are required.

1. Open the configured Telegram bot and send `/start`. The current guidance flow is
   English and starts with free text. Share synthetic interests/background, compare a
   relevant unfamiliar option, then explicitly choose a course and batch. A decided
   applicant can use `/courses` or type a unique course name without a compulsory quiz.
2. Provide synthetic age 20 and marks 70. Show the code-evaluated eligible result and
   the explanation that eligibility does not mean admission or a reserved seat.
3. Correct age to 17, then 21. Show the changed result and persisted correction history.
4. Ask where the demo campus is. Show the grounded answer without a source footer. Source references stay internal.
5. Ask an unsupported question. Show abstention rather than an invented answer.
6. Open Admissions inquiries in the staff workspace. Select the same inquiry and show
   the selected course/batch, facts, eligibility evidence and ordered conversation.
7. Send `/human` in Telegram. Show the request in Staff requests. Acknowledge and
   resolve it, then explicitly resume automation. Show that Resolve alone does not resume it.
8. Return to Knowledge library. Show approved references and indexing states. Explain
   that original files are encrypted and only ready material appears in search.

For a short final demo, focus on one adaptive guidance question, a supported course
choice, one correction and the saved guidance evidence in the staff conversation.
Existing recordings predate Task 61 and demonstrate their original behavior.
Keep the full grounded-answer/abstention and human-request sequence ready for desk review.
Upload [the synthetic counselling PDF](artifacts/synthetic-counselling-reference.pdf),
wait for Ready, then ask “What is the demo admissions counselling room called?”
The expected answer contains Lotus Hall. Show source evidence in staff search only.
For desk review, demonstrate applications/review, catalog controls, reviewed co-pilot
and opted-in follow-ups separately. Do not claim a real payment until the Razorpay
provider journey is validated. A new external staff test message needs authorization;
the previously authorized send already has user-confirmed receipt.

The [local staff walkthrough](artifacts/staff-walkthrough.webm) is a silent, 33-second
recording of the actual production frontend against the local API. It shows reference
search, the persisted Telegram inquiry, rule evidence, conversation, staff-request
screen and logout. It does not record the handset steps above or demonstrate a
populated human-request queue. Record those separately for the final event video.

The newer [58-second journey walkthrough](artifacts/student-to-staff-walkthrough.webm)
shows the actual staff view of the saved live course/batch choices, age corrections,
sourced campus answer, unsupported-question abstention and resumed staff request.
It is a silent record of persisted behavior, with no simulated handset or new staff
state changes. Run `npm run record:demo -- --journey` from frontend/ to record it to
a new output after preserving any existing recording.

The actual handset roundtrip, one authorized staff reply and the uploaded-PDF answer
have user confirmation. See [sanitized evidence](LIVE_HANDSET_RESULTS.json). Historical
recordings may show source footers; current student messages omit them.
The actual handset roundtrip has user confirmation. The user also sent both age
corrections and FAQ checks; all four replies have confirmed sends and match saved
facts/results and the staff transcript. The resent `/human` produced a confirmed
reply and staff request; actual Chrome controls passed acknowledgment, resolution
with pause preserved and explicit confirmed resume. These are saved state checks;
the next student message after resume was not part of this live sequence. Do not label a recording
of synthetic tests as live Telegram evidence. See tasks/todo.md for exact limits.

Disclosure: this project includes an existing backend foundation. The Telegram identity,
transport, durable inbox/outbox, staff knowledge workspace and admissions workflow
are the new implementation work described in the active task evidence. Do not claim
all source was created during the event. Confirm organizer acceptance of prior work.
