"use client";

import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import styles from "./analytics.module.css";

type Conversion = { converted: number; of: number; percent: number | null };
type Report = {
  period: {
    from: string;
    to: string;
    bucket: "day" | "week";
    timezone: string;
  };
  totals: {
    inquiries: number;
    applicants: number;
    fee_paid: number;
    fee_waived: number;
  };
  conversions: {
    application: Conversion;
    enrollment: Conversion;
    fee_satisfied: Conversion;
  };
  stages: {
    state: string;
    current: number;
    reached: number;
    percent: number | null;
  }[];
  series: { period: string; count: number }[];
  coverage: string;
  as_of: string;
};
const labels: Record<string, string> = {
  new: "New inquiry",
  discovering: "Exploring courses",
  qualifying: "Eligibility details",
  admission_ready: "Eligibility criteria met",
  form_collecting: "Application started",
  payment_pending: "Fee pending",
  under_review: "Under review",
  enrolled: "Enrolled",
  rejected: "Rejected",
  waitlisted: "Waitlisted",
  handed_off: "Staff review requested",
  cold: "Cold",
};
function rate(value: number | null) {
  return value === null ? "—" : `${value}%`;
}
function shortDate(value: string) {
  return new Date(`${value}T12:00:00Z`).toLocaleDateString("en-IN", {
    timeZone: "UTC",
    day: "numeric",
    month: "short",
  });
}

export default function Analytics({
  request,
  onError,
}: {
  request: (path: string, init?: RequestInit) => Promise<unknown>;
  onError: (error: unknown) => string;
}) {
  const [report, setReport] = useState<Report | null>(null);
  const [filters, setFilters] = useState({ from: "", to: "", bucket: "day" });
  const [query, setQuery] = useState("");
  const [reload, setReload] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError("");
    request(`/staff/analytics${query ? `?${query}` : ""}`, {
      signal: controller.signal,
    })
      .then((value) => {
        const data = value as Report;
        if (
          !data?.period ||
          !data.totals ||
          !data.conversions ||
          !Array.isArray(data.stages) ||
          !Array.isArray(data.series) ||
          data.series.length === 0
        )
          throw new Error("The overview could not be loaded. Try again.");
        if (!controller.signal.aborted) {
          setReport(data);
          setFilters((previous) =>
            previous.from
              ? previous
              : {
                  from: data.period.from,
                  to: data.period.to,
                  bucket: data.period.bucket,
                },
          );
        }
      })
      .catch((error) => {
        if (!controller.signal.aborted) {
          setReport(null);
          setError(onError(error));
        }
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [query, reload, request, onError]);
  function apply(event: FormEvent) {
    event.preventDefault();
    setQuery(new URLSearchParams(filters).toString());
    setReload((value) => value + 1);
  }
  const peak = Math.max(
    1,
    ...(report?.series.map((point) => point.count) || []),
  );
  const points =
    report?.series.map((point, index) => ({
      x:
        report.series.length === 1
          ? 210
          : 30 + (index * 370) / (report.series.length - 1),
      y: 145 - (point.count / peak) * 115,
      ...point,
    })) || [];
  return (
    <section aria-label="Admissions analytics" aria-busy={loading}>
      <header className={`page-heading ${styles.heading}`}>
        <div>
          <h1>Admissions overview</h1>
          <p>See how inquiries move toward an application.</p>
        </div>
        <button
          className="secondary"
          type="button"
          disabled={loading}
          onClick={() => setReload((value) => value + 1)}
        >
          Refresh overview
        </button>
      </header>
      <form
        className={styles.filters}
        onSubmit={apply}
        aria-label="Analytics period"
      >
        <label>
          From
          <input
            type="date"
            required
            value={filters.from}
            max={filters.to || undefined}
            onChange={(event) =>
              setFilters({ ...filters, from: event.target.value })
            }
          />
        </label>
        <label>
          To
          <input
            type="date"
            required
            value={filters.to}
            min={filters.from || undefined}
            onChange={(event) =>
              setFilters({ ...filters, to: event.target.value })
            }
          />
        </label>
        <label>
          Group inquiries
          <select
            value={filters.bucket}
            onChange={(event) =>
              setFilters({ ...filters, bucket: event.target.value })
            }
          >
            <option value="day">Daily</option>
            <option value="week">Weekly</option>
          </select>
        </label>
        <button className="primary" disabled={loading}>
          Apply period
        </button>
      </form>
      {error && (
        <div className={styles.feedback}>
          <p className="error" role="alert">
            {error}
          </p>
          <button
            className="secondary"
            onClick={() => setReload((value) => value + 1)}
          >
            Try again
          </button>
        </div>
      )}
      {loading && (
        <p className={styles.feedback} role="status">
          Loading the overview…
        </p>
      )}
      {report && !loading && (
        <>
          <p className={styles.period}>
            {shortDate(report.period.from)}–{shortDate(report.period.to)} ·{" "}
            {report.period.timezone} · Inquiries created in this period
          </p>
          <dl className={styles.metrics} aria-label="Conversion summary">
            <div>
              <dt>New inquiries</dt>
              <dd>{report.totals.inquiries}</dd>
              <span>Created in the selected period</span>
            </div>
            <div>
              <dt>Application conversion</dt>
              <dd>{rate(report.conversions.application.percent)}</dd>
              <span>
                {report.conversions.application.converted} of{" "}
                {report.conversions.application.of} inquiries applied
              </span>
            </div>
            <div>
              <dt>Enrollment conversion</dt>
              <dd>{rate(report.conversions.enrollment.percent)}</dd>
              <span>
                {report.conversions.enrollment.converted} of{" "}
                {report.conversions.enrollment.of} applicants enrolled
              </span>
            </div>
          </dl>
          <div className={styles.layout}>
            <section
              className={styles.trend}
              aria-label="Inquiry creation trend"
            >
              <h2>New inquiries</h2>
              <p className="quiet small">
                {report.period.bucket === "week"
                  ? "Weekly, starting Monday"
                  : "Daily"}{" "}
                in the institution timezone.
              </p>
              {report.totals.inquiries === 0 ? (
                <p className={styles.empty}>
                  No inquiries were created in this period. Choose another
                  period to explore earlier activity.
                </p>
              ) : (
                <>
                  <svg
                    className={styles.chart}
                    viewBox="0 0 420 180"
                    role="img"
                    aria-label={`New inquiries by ${report.period.bucket}. Exact counts are available below.`}
                  >
                    <title>New inquiries by {report.period.bucket}</title>
                    <line
                      x1="30"
                      y1="145"
                      x2="400"
                      y2="145"
                      stroke="var(--line)"
                    />
                    <line
                      x1="30"
                      y1="30"
                      x2="400"
                      y2="30"
                      stroke="var(--line)"
                      strokeDasharray="3 6"
                    />
                    <text x="0" y="34">
                      {peak}
                    </text>
                    <text x="10" y="149">
                      0
                    </text>
                    <polyline
                      fill="none"
                      stroke="var(--green)"
                      strokeWidth="2.5"
                      points={points
                        .map((point) => `${point.x},${point.y}`)
                        .join(" ")}
                    />
                    {points.length <= 64 &&
                      points.map((point) => (
                        <circle
                          key={point.period}
                          cx={point.x}
                          cy={point.y}
                          r="3.5"
                          fill="var(--green)"
                        />
                      ))}
                    <text x="30" y="174">
                      {shortDate(points[0].period)}
                    </text>
                    <text x="400" y="174" textAnchor="end">
                      {shortDate(points[points.length - 1].period)}
                    </text>
                  </svg>
                </>
              )}
              <details className={styles.counts}>
                <summary>View period counts</summary>
                <table>
                  <thead>
                    <tr>
                      <th scope="col">Period beginning</th>
                      <th scope="col">Inquiries</th>
                    </tr>
                  </thead>
                  <tbody>
                    {report.series.map((point) => (
                      <tr key={point.period}>
                        <th scope="row">{point.period}</th>
                        <td>{point.count}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </details>
              <div className={styles.fees}>
                <h3>Application fees</h3>
                <p>
                  {report.totals.fee_paid} paid · {report.totals.fee_waived}{" "}
                  waived
                </p>
                <p className="quiet small">
                  {report.conversions.fee_satisfied.converted} of{" "}
                  {report.conversions.fee_satisfied.of} applicants have a
                  confirmed payment or waiver. A waiver is counted separately
                  from payment.
                </p>
              </div>
              <p className={styles.coverage}>{report.coverage}</p>
              <p className={styles.coverage}>
                Updated{" "}
                {new Date(report.as_of).toLocaleString("en-IN", {
                  timeZone: report.period.timezone,
                })}{" "}
                ({report.period.timezone}).
              </p>
            </section>
            <section aria-label="Lifecycle funnel">
              <h2>Lifecycle reach</h2>
              <p className="quiet small">
                Reached at least once, alongside the current stage. Each rate
                uses all inquiries in this period.
              </p>
              <table className={styles.stages}>
                <thead>
                  <tr>
                    <th scope="col">Stage</th>
                    <th scope="col">Current</th>
                    <th scope="col">Reached</th>
                    <th scope="col">Rate</th>
                  </tr>
                </thead>
                <tbody>
                  {report.stages.map((stage) => (
                    <tr key={stage.state}>
                      <th scope="row">
                        {labels[stage.state] ||
                          stage.state.replaceAll("_", " ")}
                      </th>
                      <td>{stage.current}</td>
                      <td>
                        <span className={styles.reach}>
                          {stage.reached}
                          <span aria-hidden="true" className={styles.bar}>
                            <span style={{ width: `${stage.percent || 0}%` }} />
                          </span>
                        </span>
                      </td>
                      <td>{rate(stage.percent)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>
          </div>
        </>
      )}
    </section>
  );
}
