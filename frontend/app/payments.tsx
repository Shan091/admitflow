"use client";

import { useCallback, useEffect, useState } from "react";

type Payment = {
  id: string;
  lead_id: string;
  application_id: string;
  amount: number;
  is_demo: boolean;
  currency: string;
  status: string;
  creation_state: string;
  attempts: number;
  error_code: string | null;
  link_sent: boolean;
  delivery_status: string | null;
  created_at: string;
};
const statuses = ["created", "link_sent", "paid", "waived", "failed"];
const outcomes: Record<string, string> = {
  test_payment_confirmed: "Captured Razorpay test payment verified. The demo application is ready for staff review.",
  test_payment_pending: "No captured test payment confirmed yet. The demo application remains unpaid.",
  link_recovered: "Existing link recovered. Its delivery is tracked below.",
  awaiting_signed_confirmation:
    "The provider reports activity. Payment remains unconfirmed until its verified event arrives.",
  not_found:
    "No matching link found. The earlier request remains unresolved; no new link was created.",
  link_unavailable:
    "The existing link is cancelled or expired. Contact the institution's payment administrator.",
  already_settled: "This invoice is already paid or waived.",
  queued: "Request queued with the original invoice and fee.",
};
const label = (value: string) => value.replaceAll("_", " ");
const money = (row: Payment) =>
  new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: row.currency,
  }).format(row.amount / 100);

export default function Payments({
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
  const [rows, setRows] = useState<Payment[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [status, setStatus] = useState("");
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(true);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [confirm, setConfirm] = useState<"reconcile" | "retry" | null>(null);
  const refresh = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      setRows(
        (await request(
          `/staff/payments?offset=${offset}${status ? `&status=${status}` : ""}`,
        )) as Payment[],
      );
    } catch (e) {
      setError(onError(e));
    } finally {
      setLoading(false);
    }
  }, [request, onError, offset, status]);
  useEffect(() => {
    void refresh();
  }, [refresh]);
  const detail = rows.find((row) => row.id === selected);
  async function act() {
    if (!detail || !confirm || pending) return;
    setPending(true);
    setError("");
    setNotice("");
    try {
      const result = (await request(`/staff/payments/${detail.id}/${confirm}`, {
        method: "POST",
      })) as { result: string };
      setNotice(outcomes[result.result] || "Payment state refreshed.");
      setConfirm(null);
      await refresh();
    } catch (e) {
      setError(onError(e));
    } finally {
      setPending(false);
    }
  }
  const settled = detail && ["paid", "waived"].includes(detail.status);
  const canCheck =
    detail &&
    !settled &&
    ["uncertain", "failed", "created"].includes(detail.creation_state);
  const canRetry =
    detail &&
    !settled &&
    detail.creation_state === "failed" &&
    detail.attempts < 3 &&
    ["configuration_unavailable", "provider_429"].includes(
      detail.error_code || "",
    );
  return (
    <>
      <header className="page-heading">
        <div>
          <h1>Payments</h1>
          <p>
            Track application fees, delivery and requests that need attention.
          </p>
        </div>
        <button
          className="secondary"
          disabled={loading || pending}
          onClick={() => void refresh()}
        >
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
          Payment status
          <select
            value={status}
            disabled={pending}
            onChange={(e) => {
              setStatus(e.target.value);
              setOffset(0);
              setSelected(null);
              setConfirm(null);
              setNotice("");
            }}
          >
            <option value="">All statuses</option>
            {statuses.map((item) => (
              <option key={item} value={item}>
                {label(item)}
              </option>
            ))}
          </select>
        </label>
      </div>
      <div className="admissions-layout">
        <section aria-label="Payment list" aria-busy={loading}>
          {loading ? (
            <p className="empty">Loading payments…</p>
          ) : rows.length === 0 ? (
            <div className="empty">
              <h2>No payments here yet</h2>
              <p>
                An invoice appears after a student confirms the application fee.
                A full discount is recorded as waived.
              </p>
            </div>
          ) : (
            rows.map((row) => (
              <button
                key={row.id}
                className="inquiry-row"
                aria-pressed={selected === row.id}
                disabled={pending}
                onClick={() => {
                  setSelected(row.id);
                  setConfirm(null);
                  setNotice("");
                }}
              >
                <strong>{money(row)}{row.is_demo ? " · Test" : ""}</strong>
                <span>{label(row.status)}</span>
                <span>
                  Invoice {row.id.slice(-8)} · {label(row.creation_state)}
                </span>
              </button>
            ))
          )}
          {(offset > 0 || rows.length === 50) && (
            <div className="pagination">
              <button
                className="secondary"
                disabled={offset === 0 || loading || pending}
                onClick={() => {
                  setOffset(Math.max(0, offset - 50));
                  setSelected(null);
                }}
              >
                Previous
              </button>
              <span>Page {offset / 50 + 1}</span>
              <button
                className="secondary"
                disabled={rows.length < 50 || loading || pending}
                onClick={() => {
                  setOffset(offset + 50);
                  setSelected(null);
                }}
              >
                Next
              </button>
            </div>
          )}
        </section>
        <section aria-label="Payment detail" className="inquiry-detail">
          {!detail ? (
            <div className="empty">
              <h2>Select a payment</h2>
              <p>Inspect its fee, delivery and provider request state.</p>
            </div>
          ) : (
            <>
              <div className="management-toolbar">
                <div>
                  <h2>{money(detail)}</h2>
                  <p className="quiet">{detail.is_demo ? "Demo application fee · Razorpay test mode" : "Application fee"}</p>
                </div>
                <span className="status queued">{label(detail.status)}</span>
              </div>
              <dl className="inquiry-facts payment-facts">
                <div>
                  <dt>Invoice</dt>
                  <dd>{detail.id}</dd>
                </div>
                <div>
                  <dt>Provider request</dt>
                  <dd>{label(detail.creation_state)}</dd>
                </div>
                <div>
                  <dt>Link delivery</dt>
                  <dd>
                    {detail.link_sent
                      ? "Confirmed sent"
                      : detail.delivery_status
                        ? label(detail.delivery_status)
                        : "Not queued"}
                  </dd>
                </div>
                <div>
                  <dt>Creation attempts</dt>
                  <dd>{detail.attempts}</dd>
                </div>
                {detail.error_code && (
                  <div>
                    <dt>Attention</dt>
                    <dd>{label(detail.error_code)}</dd>
                  </div>
                )}
              </dl>
              <p className="quiet small">
                Payment or a fee waiver allows application review. Admission and
                seat allocation require a separate decision.
              </p>
              <button
                className="text-button"
                disabled={pending}
                onClick={() => onOpenInquiry(detail.lead_id)}
              >
                View inquiry
              </button>
              {admin && (canCheck || canRetry) && (
                <div className="management-archive">
                  {canCheck && (
                    <button
                      className="secondary"
                      disabled={pending}
                      onClick={() => setConfirm("reconcile")}
                    >
                      Check provider
                    </button>
                  )}
                  {canRetry && (
                    <button
                      className="secondary"
                      disabled={pending}
                      onClick={() => setConfirm("retry")}
                    >
                      Retry request
                    </button>
                  )}
                </div>
              )}
              {confirm && (
                <div
                  className="management-archive"
                  role="group"
                  aria-label="Confirm payment action"
                >
                  <p>
                    {confirm === "reconcile"
                      ? "Look up this invoice at the provider? An existing payable link can be recovered for delivery. No new payment link will be created."
                      : "Retry the original request using the same invoice and fee? Only a request known to have failed before creation can be retried."}
                  </p>
                  <button
                    className="primary"
                    disabled={pending}
                    onClick={() => void act()}
                  >
                    {pending ? "Checking…" : "Confirm"}
                  </button>
                  <button
                    className="text-button"
                    disabled={pending}
                    onClick={() => setConfirm(null)}
                  >
                    Cancel
                  </button>
                </div>
              )}
            </>
          )}
        </section>
      </div>
    </>
  );
}
