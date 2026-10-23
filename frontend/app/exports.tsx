"use client";

import { useState } from "react";

export default function Exports({
  onError,
}: {
  onError: (error: unknown) => string;
}) {
  const [dataset, setDataset] = useState("leads");
  const [format, setFormat] = useState("csv");
  const [query, setQuery] = useState("");
  const [pending, setPending] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  async function download() {
    setPending(true);
    setError("");
    setNotice("");
    try {
      const response = await fetch("/api/staff/exports", {
        method: "POST",
        credentials: "same-origin",
        cache: "no-store",
        headers: {
          "X-AdmitFlow-Request": "1",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          dataset,
          format,
          query: dataset === "leads" ? query : "",
        }),
      });
      if (!response.ok) {
        const body = await response.json().catch(() => ({}));
        throw Object.assign(
          new Error(
            typeof body.detail === "string"
              ? body.detail
              : "Download failed. Try again.",
          ),
          { status: response.status },
        );
      }
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      anchor.href = url;
      anchor.download = `admitflow-${dataset}.${format}`;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
      setNotice(
        "Download prepared. Keep applicant information in an approved, secure location.",
      );
    } catch (error) {
      setError(onError(error));
    } finally {
      setPending(false);
    }
  }
  return (
    <>
      <header className="page-heading">
        <div>
          <h1>Data exports</h1>
          <p>
            Download your institution’s inquiries, applications and payment
            records.
          </p>
        </div>
      </header>
      <section
        className="export-form"
        aria-label="Export data"
        aria-busy={pending}
      >
        <h2>Prepare a download</h2>
        <p>
          Downloads include personal information and are recorded in the access
          audit. Amounts are in minor currency units (paise for INR). Oversized
          exports are rejected with a clear limit.
        </p>
        <label>
          Records
          <select
            value={dataset}
            onChange={(event) => setDataset(event.target.value)}
          >
            <option value="leads">Admissions inquiries</option>
            <option value="applications">Applications</option>
            <option value="payments">Payments</option>
          </select>
        </label>
        {dataset === "leads" && (
          <label>
            Inquiry name or full phone (optional)
            <input
              type="search"
              maxLength={200}
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Name prefix or +91…"
            />
          </label>
        )}
        <label>
          File format
          <select
            value={format}
            onChange={(event) => setFormat(event.target.value)}
          >
            <option value="csv">CSV</option>
            <option value="xlsx">Excel (.xlsx)</option>
          </select>
        </label>
        <button
          className="primary"
          disabled={pending}
          onClick={() => void download()}
        >
          {pending ? "Preparing download…" : "Download records"}
        </button>
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
      </section>
    </>
  );
}
