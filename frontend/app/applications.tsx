"use client";

import { useCallback, useEffect, useState } from "react";

type Summary = {
  id: string;
  lead_id: string;
  course: string;
  status: string;
  submitted_at: string;
};
type Detail = {
  id: string;
  lead_id: string;
  status: string;
  form: Record<string, string | null>;
  payments: string[];
};
const statuses = [
  "submitted",
  "under_review",
  "approved",
  "waitlisted",
  "rejected",
];
const fields: Record<string, string> = {
  full_name: "Full name",
  dob: "Date of birth",
  parent_name: "Parent or guardian",
  address: "Address",
  previous_school: "Previous school",
};
export default function Applications({
  request,
  onError,
  admin,
  onOpenInquiry,
}: {
  request: (path: string, init?: RequestInit) => Promise<unknown>;
  onError: (error: unknown) => string;
  admin: boolean;
  onOpenInquiry: (id: string) => void;
}) {
  const [rows, setRows] = useState<Summary[]>([]),
    [detail, setDetail] = useState<Detail | null>(null);
  const [status, setStatus] = useState(""),
    [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(true),
    [pending, setPending] = useState(false);
  const [error, setError] = useState(""),
    [notice, setNotice] = useState("");
  const [confirm, setConfirm] = useState<
    "approve" | "waitlist" | "reject" | null
  >(null);
  const refresh = useCallback(async () => {
    setLoading(true);
    try {
      const query = new URLSearchParams({ offset: String(offset) });
      if (status) query.set("status", status);
      setRows((await request(`/staff/applications?${query}`)) as Summary[]);
    } catch (e) {
      setError(onError(e));
    } finally {
      setLoading(false);
    }
  }, [request, onError, status, offset]);
  useEffect(() => {
    void refresh();
  }, [refresh]);
  async function select(id: string) {
    setPending(true);
    setError("");
    setNotice("");
    setConfirm(null);
    try {
      setDetail((await request(`/staff/applications/${id}`)) as Detail);
    } catch (e) {
      setError(onError(e));
    } finally {
      setPending(false);
    }
  }
  async function decide() {
    if (!detail || !confirm) return;
    setPending(true);
    setError("");
    setNotice("");
    try {
      await request(`/staff/applications/${detail.id}/${confirm}`, {
        method: "POST",
      });
      setDetail((await request(`/staff/applications/${detail.id}`)) as Detail);
      setConfirm(null);
      setNotice("Application decision saved.");
      await refresh();
    } catch (e) {
      setError(onError(e));
    } finally {
      setPending(false);
    }
  }
  return (
    <>
      <header className="page-heading">
        <div>
          <h1>Applications</h1>
          <p>
            Review submitted details, payment state and admission decisions.
          </p>
        </div>
        <button className="secondary" onClick={() => void refresh()}>
          Refresh
        </button>
      </header>
      {error && (
        <p role="alert" className="error">
          {error}
        </p>
      )}
      {notice && (
        <p role="status" className="notice">
          {notice}
        </p>
      )}
      <div className="inquiry-filters">
        <label>
          Application status
          <select
            value={status}
            onChange={(e) => {
              setStatus(e.target.value);
              setOffset(0);
              setDetail(null);
            }}
          >
            <option value="">All statuses</option>
            {statuses.map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
        </label>
      </div>
      <div className="admissions-layout">
        <section aria-label="Application list" aria-busy={loading}>
          {loading ? (
            <p className="empty">Loading applications…</p>
          ) : rows.length === 0 ? (
            <div className="empty">
              <h2>No applications here yet</h2>
              <p>
                A student must meet the course criteria, explicitly start a form
                and review it before submitting.
              </p>
            </div>
          ) : (
            rows.map((row) => (
              <button
                className="inquiry-row"
                key={row.id}
                aria-pressed={detail?.id === row.id}
                onClick={() => void select(row.id)}
              >
                <strong>{row.course}</strong>
                <span>{row.status.replaceAll("_", " ")}</span>
                <span>
                  Submitted {new Date(row.submitted_at).toLocaleString()}
                </span>
              </button>
            ))
          )}
          {(offset > 0 || rows.length === 50) && (
            <div className="pagination">
              <button
                className="secondary"
                disabled={offset === 0 || loading}
                onClick={() => setOffset(Math.max(0, offset - 50))}
              >
                Previous
              </button>
              <span>Page {offset / 50 + 1}</span>
              <button
                className="secondary"
                disabled={rows.length < 50 || loading}
                onClick={() => setOffset(offset + 50)}
              >
                Next
              </button>
            </div>
          )}
        </section>
        <section aria-label="Application detail" className="inquiry-detail">
          {!detail ? (
            <div className="empty">
              <h2>Select an application</h2>
              <p>
                Submitted information is available only to authorized
                institution staff. Access is recorded.
              </p>
            </div>
          ) : (
            <>
              <div className="management-toolbar">
                <h2>Application details</h2>
                <span className="status queued">
                  {detail.status.replaceAll("_", " ")}
                </span>
              </div>
              <dl className="inquiry-facts">
                {Object.entries(fields).map(([key, label]) => (
                  <div key={key}>
                    <dt>{label}</dt>
                    <dd>{detail.form[key] || "Not provided"}</dd>
                  </div>
                ))}
                <div>
                  <dt>Payment</dt>
                  <dd>
                    {detail.payments.length
                      ? detail.payments.join(", ")
                      : "No payment recorded"}
                  </dd>
                </div>
              </dl>
              <button
                className="text-button"
                onClick={() => onOpenInquiry(detail.lead_id)}
              >
                View inquiry and conversation
              </button>
              {admin && !["approved", "rejected"].includes(detail.status) && (
                <div className="management-archive">
                  {confirm ? (
                    <>
                      <p>
                        {confirm === "approve"
                          ? "Approve this application and allocate one available seat? Any configured application fee must be paid."
                          : confirm === "reject"
                            ? "Reject this application? This is a final decision."
                            : "Place this application on the waitlist? No seat will be allocated."}
                      </p>
                      <button
                        className="primary"
                        disabled={pending}
                        onClick={() => void decide()}
                      >
                        Confirm {confirm}
                      </button>
                      <button
                        className="text-button"
                        disabled={pending}
                        onClick={() => setConfirm(null)}
                      >
                        Cancel
                      </button>
                    </>
                  ) : (
                    (["approve", "waitlist", "reject"] as const).map(
                      (action) => (
                        <button
                          className="secondary"
                          key={action}
                          disabled={pending}
                          onClick={() => setConfirm(action)}
                        >
                          {action === "approve"
                            ? "Approve application"
                            : action === "waitlist"
                              ? "Waitlist application"
                              : "Reject application"}
                        </button>
                      ),
                    )
                  )}
                </div>
              )}
              <p className="quiet">
                Submission does not grant admission. Approval allocates a seat
                only when the server confirms payment and capacity.
              </p>
            </>
          )}
        </section>
      </div>
    </>
  );
}
