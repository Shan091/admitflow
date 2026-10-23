# Intent: Admissions Flow and Discounts

- **Outcome:** Model the messy reality of admissions by inserting a manual "Application Review" step after payment, and allow the AI to use pre-defined discount codes as a sales tool.
- **User:** Institution Admissions Staff (who review applications and define discount codes) and Students (who get a smoother, more flexible payment experience).
- **Why now:** Because paying an application fee doesn't guarantee enrollment, and fixed prices without discount codes lose potential leads who are price-sensitive. 
- **Success:** The AI can suggest active discount codes (fetched from the database). If the user accepts, the AI passes the code to the backend. **The Python backend validates the code and calculates the final Razorpay amount** (preserving our safety guardrails). After payment, the lead goes to an `under_review` queue in the dashboard where staff can "Approve", "Waitlist", or "Reject".
- **Constraint:** We must add a `discount_codes` table to the database, update the LLM prompt to inject available codes, and add the review states (`under_review`, `rejected`, `waitlisted`) to the state machine before we start writing the backend code.
- **Out of scope:** The AI inventing its own discounts, negotiating percentages, or processing refunds for rejected students (refunds happen manually in Razorpay).
