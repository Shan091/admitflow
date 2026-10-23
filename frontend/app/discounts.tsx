"use client";

import { useEffect, useState } from "react";
import type { FormEvent } from "react";

type Discount = {
  id?: string;
  code: string;
  discount_type: "percent" | "flat";
  amount: number;
  max_uses: number | null;
  is_active: boolean;
  uses_count?: number;
};
const blank: Discount = {
  code: "",
  discount_type: "percent",
  amount: 10,
  max_uses: null,
  is_active: true,
};
export default function Discounts({
  request,
  onError,
  admin,
}: {
  request: (path: string, init?: RequestInit) => Promise<unknown>;
  onError: (error: unknown) => string;
  admin: boolean;
}) {
  const [records, setRecords] = useState<Discount[]>([]);
  const [current, setCurrent] = useState<Discount | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [archive, setArchive] = useState(false);
  useEffect(() => {
    let active = true;
    request("/staff/discounts")
      .then((data) => {
        if (active) setRecords(data as Discount[]);
      })
      .catch((e) => {
        if (active) setError(onError(e));
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [request, onError]);
  async function save(event: FormEvent) {
    event.preventDefault();
    if (!current) return;
    setSaving(true);
    setError("");
    setNotice("");
    try {
      const { id, uses_count, ...body } = current;
      void uses_count;
      const result = (await request(`/staff/discounts${id ? `/${id}` : ""}`, {
        method: id ? "PUT" : "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      })) as Discount;
      setCurrent(result);
      setRecords((await request("/staff/discounts")) as Discount[]);
      setNotice("Discount code saved.");
    } catch (e) {
      setError(onError(e));
    } finally {
      setSaving(false);
    }
  }
  async function disable() {
    if (!current?.id) return;
    setSaving(true);
    setError("");
    try {
      await request(`/staff/discounts/${current.id}`, { method: "DELETE" });
      setCurrent({ ...current, is_active: false });
      setRecords((await request("/staff/discounts")) as Discount[]);
      setArchive(false);
      setNotice(
        "Discount code deactivated. Existing payment records are preserved.",
      );
    } catch (e) {
      setError(onError(e));
    } finally {
      setSaving(false);
    }
  }
  return (
    <>
      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}
      {notice && (
        <p className="notice" role="status">
          {notice}
        </p>
      )}
      <div className="management-layout">
        <section aria-label="Discount codes">
          <div className="management-toolbar">
            <h2>Discount codes</h2>
            {admin && (
              <button
                className="secondary"
                onClick={() => {
                  setCurrent({ ...blank });
                  setArchive(false);
                  setNotice("");
                }}
              >
                New discount
              </button>
            )}
          </div>
          {loading ? (
            <p className="empty">Loading discount codes…</p>
          ) : records.length === 0 ? (
            <p className="empty">
              No discount codes yet. Add an offer with an explicit value and
              optional usage limit.
            </p>
          ) : (
            records.map((item) => (
              <button
                className="inquiry-row"
                key={item.id}
                onClick={() => {
                  setCurrent({ ...item });
                  setArchive(false);
                  setNotice("");
                }}
              >
                <strong>{item.code}</strong>
                <span>
                  {item.discount_type === "percent"
                    ? `${item.amount}%`
                    : `INR ${(item.amount / 100).toFixed(2)}`}{" "}
                  · {item.is_active ? "Active" : "Inactive"}
                </span>
                <span>
                  {item.uses_count ?? 0} used
                  {item.max_uses ? ` of ${item.max_uses}` : ""}
                </span>
              </button>
            ))
          )}
        </section>
        <section aria-label="Discount editor">
          {!current ? (
            <div className="empty">
              <h2>Select a discount</h2>
              <p>
                Values are applied by the backend. The assistant cannot invent a
                discount.
              </p>
            </div>
          ) : (
            <form className="management-form" onSubmit={save}>
              <h2>{current.id ? "Discount details" : "New discount"}</h2>
              <fieldset disabled={!admin || saving}>
                <label>
                  Discount code
                  <input
                    required
                    pattern="[A-Za-z0-9_-]+"
                    maxLength={64}
                    value={current.code}
                    onChange={(e) =>
                      setCurrent({ ...current, code: e.target.value })
                    }
                  />
                </label>
                <label>
                  Discount type
                  <select
                    aria-label="Discount type"
                    value={current.discount_type}
                    onChange={(e) =>
                      setCurrent({
                        ...current,
                        discount_type: e.target
                          .value as Discount["discount_type"],
                        amount: 10,
                      })
                    }
                  >
                    <option value="percent">Percentage</option>
                    <option value="flat">Fixed amount (INR)</option>
                  </select>
                </label>
                <label>
                  {current.discount_type === "percent"
                    ? "Percentage off"
                    : "Amount off (INR)"}
                  <input
                    type="number"
                    required
                    min={current.discount_type === "percent" ? 1 : 0.01}
                    max={current.discount_type === "percent" ? 100 : 10000000}
                    step={current.discount_type === "percent" ? 1 : 0.01}
                    value={
                      current.discount_type === "percent"
                        ? current.amount
                        : current.amount / 100
                    }
                    onChange={(e) =>
                      setCurrent({
                        ...current,
                        amount:
                          current.discount_type === "percent"
                            ? Number(e.target.value)
                            : Math.round(Number(e.target.value) * 100),
                      })
                    }
                  />
                </label>
                <label>
                  Maximum uses (blank for unlimited)
                  <input
                    type="number"
                    min={Math.max(1, current.uses_count ?? 0)}
                    max={1000000000}
                    value={current.max_uses ?? ""}
                    onChange={(e) =>
                      setCurrent({
                        ...current,
                        max_uses: e.target.value
                          ? Number(e.target.value)
                          : null,
                      })
                    }
                  />
                </label>
                <label className="management-check">
                  <input
                    type="checkbox"
                    checked={current.is_active}
                    onChange={(e) =>
                      setCurrent({ ...current, is_active: e.target.checked })
                    }
                  />
                  Discount active
                </label>
                <p className="quiet">
                  Used {current.uses_count ?? 0} times. Usage is recorded by
                  payment processing and cannot be reset here.
                </p>
                {admin && (
                  <button className="primary">
                    {saving ? "Saving…" : "Save discount"}
                  </button>
                )}
              </fieldset>
              {admin && current.id && current.is_active && (
                <div className="management-archive">
                  {archive ? (
                    <>
                      <p>Deactivate this discount for new payments?</p>
                      <button
                        type="button"
                        className="secondary danger"
                        disabled={saving}
                        onClick={() => void disable()}
                      >
                        Confirm deactivation
                      </button>
                      <button
                        type="button"
                        className="text-button"
                        onClick={() => setArchive(false)}
                      >
                        Cancel
                      </button>
                    </>
                  ) : (
                    <button
                      type="button"
                      className="text-button danger"
                      onClick={() => setArchive(true)}
                    >
                      Deactivate discount
                    </button>
                  )}
                </div>
              )}
            </form>
          )}
        </section>
      </div>
    </>
  );
}
