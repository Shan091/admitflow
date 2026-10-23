"use client";
import StaffControls from "./staff-controls";
import PrivacyControls from "./privacy-controls";
import type { StaffDraft } from "./staff-controls";

import { useCallback, useEffect, useRef, useState } from "react";

type Request = (path: string, init?: RequestInit) => Promise<unknown>;
type Inquiry = {
  id: string;
  name?: string | null;
  status: string;
  course: string | null;
};
type RuleEvidence = {
  field: string;
  operator: string;
  expected: unknown;
  actual: unknown;
  passed: boolean;
};
const labels: Record<string, string> = {
  new: "New inquiry",
  discovering: "Exploring courses",
  qualifying: "Collecting eligibility details",
  admission_ready: "Eligibility criteria met",
  handed_off: "Staff review requested",
  form_collecting: "Application in progress",
  payment_pending: "Fee pending",
  under_review: "Application under review",
  enrolled: "Enrolled",
  rejected: "Rejected",
  waitlisted: "Waitlisted",
  cold: "Inactive",
};
function statusTone(status: string) {
  if (["admission_ready", "enrolled"].includes(status)) return "ready";
  if (status === "rejected") return "failed";
  if (
    ["handed_off", "under_review", "payment_pending", "waitlisted"].includes(
      status,
    )
  )
    return "processing";
  return "queued";
}
function statusLabel(status: string) {
  return labels[status] || status.replaceAll("_", " ");
}
type Human = {
  id: string;
  lead_id: string;
  status: "open" | "acknowledged" | "resolved" | "resumed";
};
type Detail = {
  id: string;
  status: string;
  copilot_mode: boolean;
  conversation_purged_at?: string | null;
  draft_stale: boolean;
  course_id: string | null;
  batch_id: string | null;
  batch_name: string | null;
  memory: {
    language?: string;
    staff_draft?: StaffDraft;
    facts?: Record<string, unknown>;
    eligibility?: { outcome: string; rules?: RuleEvidence[] };
  };
  messages: {
    direction: string;
    text: string;
    status: string;
    event_id: string;
    message_id: string;
    kind: string;
    created_at: string;
  }[];
  older_cursor: string | null;
};

export default function Admissions({
  view,
  request,
  onError,
  initialLead = null,
  admin = false,
  onDeleted,
}: {
  view: "leads" | "requests";
  request: Request;
  onError: (error: unknown) => string;
  initialLead?: string | null;
  admin?: boolean;
  onDeleted?: () => void;
}) {
  const [rows, setRows] = useState<Inquiry[]>([]);
  const [requests, setRequests] = useState<Human[]>([]);
  const [courses, setCourses] = useState<{ id: string; name: string }[]>([]);
  const [status, setStatus] = useState("");
  const [course, setCourse] = useState("");
  const [search, setSearch] = useState("");
  const [query, setQuery] = useState("");
  const refreshVersion = useRef(0);
  const [offset, setOffset] = useState(0);
  const [selected, setSelected] = useState<string | null>(initialLead);
  const [detail, setDetail] = useState<Detail | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [pending, setPending] = useState<string | null>(null);
  const [notice, setNotice] = useState("");
  const [confirmResume, setConfirmResume] = useState<string | null>(null);
  const [olderLoaded, setOlderLoaded] = useState(false);
  useEffect(() => {
    if (initialLead) {
      setSelected(initialLead);
      setOlderLoaded(false);
      setDetail(null);
    }
  }, [initialLead]);

  const refresh = useCallback(async () => {
    const version = ++refreshVersion.current;
    try {
      const params = new URLSearchParams({ offset: String(offset) });
      if (status) params.set("status", status);
      if (course) params.set("course_id", course);
      const [inquiries, humans, catalog] = await Promise.all([
        query
          ? request("/staff/leads/search", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                query,
                status: status || null,
                course_id: course || null,
                offset,
              }),
            })
          : request(`/staff/leads?${params}`),
        request(`/staff/human-requests?offset=${offset}`),
        request("/staff/courses"),
      ]);
      if (version !== refreshVersion.current) return;
      setRows(inquiries as Inquiry[]);
      setRequests(humans as Human[]);
      setCourses(catalog as { id: string; name: string }[]);
      if (selected && !olderLoaded) {
        const latest = (await request(`/staff/leads/${selected}`)) as Detail;
        if (version !== refreshVersion.current) return;
        setDetail(latest);
      }
      setError("");
    } catch (error) {
      if (version === refreshVersion.current) setError(onError(error));
    } finally {
      if (version === refreshVersion.current) setLoading(false);
    }
  }, [offset, status, course, query, selected, olderLoaded, request, onError]);

  useEffect(() => {
    void refresh();
    const timer = setInterval(() => {
      if (document.visibilityState === "visible") void refresh();
    }, 8000);
    return () => {
      clearInterval(timer);
      refreshVersion.current++;
    };
  }, [refresh]);

  async function select(id: string) {
    setSelected(id);
    setOlderLoaded(false);
    setDetail(null);
    setPending(id);
    try {
      setDetail((await request(`/staff/leads/${id}`)) as Detail);
    } catch (error) {
      setError(onError(error));
    } finally {
      setPending(null);
    }
  }
  async function act(
    item: Human,
    action: "acknowledge" | "resolve" | "resume",
  ) {
    setPending(item.id);
    setError("");
    setNotice("");
    try {
      await request(`/staff/human-requests/${item.id}/${action}`, {
        method: "POST",
      });
      setConfirmResume(null);
      setNotice(
        action === "resume"
          ? "Automation will continue on the student's next message."
          : "Request updated. Automation remains paused until explicitly resumed.",
      );
      await refresh();
    } catch (error) {
      setError(onError(error));
    } finally {
      setPending(null);
    }
  }
  async function older() {
    if (!detail?.older_cursor || !selected) return;
    setPending("older");
    try {
      const previous = (await request(
        `/staff/leads/${selected}?cursor=${encodeURIComponent(detail.older_cursor)}`,
      )) as Detail;
      setDetail({
        ...detail,
        older_cursor: previous.older_cursor,
        messages: [...previous.messages, ...detail.messages],
      });
      setOlderLoaded(true);
    } catch (error) {
      setError(onError(error));
    } finally {
      setPending(null);
    }
  }

  const list = view === "leads" ? rows : requests;
  return (
    <>
      <header className="page-heading">
        <div>
          <h1>
            {view === "leads" ? "Admissions inquiries" : "Staff requests"}
          </h1>
          <p>
            {view === "leads"
              ? "The conversations, choices and evidence behind each inquiry."
              : "Review student requests and decide when automation can continue."}
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
      {view === "leads" && (
        <form
          className="inquiry-search"
          onSubmit={(event) => {
            event.preventDefault();
            setOffset(0);
            setLoading(true);
            setQuery(search.trim());
            if (query === search.trim()) void refresh();
          }}
        >
          <label htmlFor="inquiry-search">Find an inquiry</label>
          <p id="inquiry-search-help">
            Use a known name prefix (at least two characters per word) or a full
            phone with country code. Telegram does not share phone numbers
            automatically.
          </p>
          <div>
            <input
              id="inquiry-search"
              aria-describedby="inquiry-search-help"
              value={search}
              maxLength={200}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Name or +91…"
              type="search"
            />
            <button className="primary" type="submit">
              Search
            </button>
            {(search || query) && (
              <button
                className="text-button"
                type="button"
                onClick={() => {
                  setSearch("");
                  setQuery("");
                  setOffset(0);
                }}
              >
                Clear search
              </button>
            )}
          </div>
        </form>
      )}
      {view === "leads" && (
        <div className="inquiry-filters">
          <label>
            Status
            <select
              value={status}
              onChange={(e) => {
                setStatus(e.target.value);
                setOffset(0);
              }}
            >
              <option value="">All statuses</option>
              {Object.keys(labels).map((value) => (
                <option key={value} value={value}>
                  {statusLabel(value)}
                </option>
              ))}
            </select>
          </label>
          <label>
            Course
            <select
              value={course}
              onChange={(e) => {
                setCourse(e.target.value);
                setOffset(0);
              }}
            >
              <option value="">All courses</option>
              {courses.map((row) => (
                <option key={row.id} value={row.id}>
                  {row.name}
                </option>
              ))}
            </select>
          </label>
        </div>
      )}
      <div className="admissions-layout">
        <section
          aria-label={view === "leads" ? "Inquiries" : "Human requests"}
          aria-busy={loading}
        >
          {loading ? (
            <p className="empty">Loading inquiries…</p>
          ) : list.length === 0 ? (
            <div className="empty">
              <h2>
                {view === "leads" ? "No inquiries yet" : "No staff requests"}
              </h2>
              <p>
                {view === "leads"
                  ? "Student inquiries appear after a message reaches your institution's Telegram bot. Try changing the filters if you expected an inquiry."
                  : "An explicit student request appears here with its conversation context."}
              </p>
            </div>
          ) : view === "leads" ? (
            rows.map((row) => (
              <button
                className={`inquiry-row ${selected === row.id ? "selected" : ""}`}
                key={row.id}
                onClick={() => void select(row.id)}
              >
                <strong>{row.name || `Inquiry ${row.id.slice(0, 8)}`}</strong>
                <span>{row.course || "Course not selected"}</span>
                <span className={`status ${statusTone(row.status)}`}>
                  {statusLabel(row.status)}
                </span>
              </button>
            ))
          ) : (
            requests.map((item) => (
              <article className="human-row" key={item.id}>
                <button
                  className="text-button"
                  onClick={() => void select(item.lead_id)}
                >
                  Open inquiry {item.lead_id.slice(0, 8)}
                </button>
                <span className="status queued">{item.status}</span>
                <div className="row-actions">
                  {item.status === "open" && (
                    <button
                      className="secondary"
                      disabled={pending === item.id}
                      onClick={() => void act(item, "acknowledge")}
                    >
                      Acknowledge
                    </button>
                  )}
                  {["open", "acknowledged"].includes(item.status) && (
                    <button
                      className="secondary"
                      disabled={pending === item.id}
                      onClick={() => void act(item, "resolve")}
                    >
                      Resolve request
                    </button>
                  )}
                  {item.status === "resolved" &&
                    (confirmResume === item.id ? (
                      <>
                        <span>Resume on the next student message?</span>
                        <button
                          className="primary"
                          disabled={pending === item.id}
                          onClick={() => void act(item, "resume")}
                        >
                          Confirm resume
                        </button>
                        <button
                          className="text-button"
                          onClick={() => setConfirmResume(null)}
                        >
                          Cancel
                        </button>
                      </>
                    ) : (
                      <button
                        className="secondary"
                        onClick={() => setConfirmResume(item.id)}
                      >
                        Resume automation
                      </button>
                    ))}
                </div>
              </article>
            ))
          )}
          {(offset > 0 || list.length === 50) && (
            <div className="pagination">
              <button
                className="secondary"
                disabled={offset === 0}
                onClick={() => setOffset(Math.max(0, offset - 50))}
              >
                Previous
              </button>
              <span>Page {Math.floor(offset / 50) + 1}</span>
              <button
                className="secondary"
                disabled={list.length < 50}
                onClick={() => setOffset(offset + 50)}
              >
                Next
              </button>
            </div>
          )}
        </section>
        <section className="inquiry-detail" aria-label="Inquiry detail">
          {!selected ? (
            <div className="empty">
              <h2>Select an inquiry</h2>
              <p>
                Review the student's conversation, selected course and
                eligibility evidence.
              </p>
            </div>
          ) : !detail ? (
            <p aria-busy="true">Loading conversation…</p>
          ) : (
            <>
              <header className="section-header">
                <h2>Inquiry {detail.id.slice(0, 8)}</h2>
                <span className="status queued">
                  {statusLabel(detail.status)}
                </span>
              </header>
              <dl className="inquiry-facts">
                <dt>Course</dt>
                <dd>
                  {courses.find((row) => row.id === detail.course_id)?.name ||
                    "Not selected"}
                </dd>
                <dt>Batch</dt>
                <dd>
                  {detail.batch_name ||
                    (detail.batch_id
                      ? "Selected batch is unavailable"
                      : "Not selected")}
                </dd>
                <dt>Language preference</dt>
                <dd>{detail.memory.language || "Not selected"}</dd>
                <dt>Eligibility</dt>
                <dd>
                  {detail.memory.eligibility?.outcome.replaceAll("_", " ") ||
                    "Not evaluated"}
                </dd>
                {Object.entries(detail.memory.facts || {}).map(
                  ([key, value]) => (
                    <div className="fact-pair" key={key}>
                      <dt>{key.replaceAll("_", " ")}</dt>
                      <dd>{String(value)}</dd>
                    </div>
                  ),
                )}
              </dl>
              {detail.memory.eligibility?.rules && (
                <details className="evidence">
                  <summary>View rule evidence</summary>
                  <div className="rule-evidence">
                    {detail.memory.eligibility.rules.map((rule, index) => (
                      <p key={`${rule.field}-${index}`}>
                        <strong>{rule.field.replaceAll("_", " ")}</strong>
                        <br />
                        Required: {rule.operator}{" "}
                        {Array.isArray(rule.expected)
                          ? rule.expected.join(", ")
                          : String(rule.expected)}
                        . Student answered: {String(rule.actual)}.<br />
                        {rule.passed ? "Criterion met" : "Criterion not met"}
                      </p>
                    ))}
                  </div>
                </details>
              )}
              <h3 className="conversation-heading">Conversation</h3>
              {detail.conversation_purged_at && (
                <p className="notice">
                  Earlier conversation history was removed under this
                  institution’s retention policy.
                </p>
              )}
              <StaffControls
                key={detail.id}
                leadId={detail.id}
                active={detail.copilot_mode}
                draft={detail.memory.staff_draft}
                stale={detail.draft_stale}
                request={request}
                onError={onError}
                onRefresh={async () => {
                  setOlderLoaded(false);
                  setDetail(
                    (await request(`/staff/leads/${detail.id}`)) as Detail,
                  );
                }}
              />
              {detail.older_cursor && (
                <button
                  className="secondary"
                  disabled={pending === "older"}
                  onClick={() => void older()}
                >
                  Load earlier messages
                </button>
              )}
              <div className="conversation" aria-live="polite">
                {detail.messages.length === 0 && (
                  <p className="quiet">
                    No Telegram conversation is stored for this inquiry.
                  </p>
                )}
                {detail.messages.map((message) => (
                  <article
                    className={`message ${message.direction}`}
                    key={message.message_id}
                  >
                    <div>
                      <strong>
                        {message.direction === "inbound"
                          ? "Student"
                          : message.kind === "payment_paid"
                            ? "Payment confirmation"
                            : message.kind === "payment_link"
                              ? "Payment link"
                              : message.kind === "staff_reply"
                                ? "Staff member"
                                : "AdmitFlow"}
                      </strong>
                      <span>{message.status}</span>
                    </div>
                    <p>{message.text}</p>
                    <time className="quiet small" dateTime={message.created_at}>
                      {new Date(message.created_at).toLocaleString()}
                    </time>
                  </article>
                ))}
              </div>
              <p className="quiet small">
                Eligibility is not admission or a reserved seat. “Uncertain”
                delivery requires review; it is not automatically resent.
              </p>
              {admin && (
                <PrivacyControls
                  key={`privacy-${detail.id}`}
                  leadId={detail.id}
                  request={request}
                  onError={onError}
                  onDeleted={() => {
                    setSelected(null);
                    setDetail(null);
                    setOffset(0);
                    setNotice(
                      "Inquiry data deleted. A deletion receipt was recorded.",
                    );
                    onDeleted?.();
                  }}
                />
              )}
            </>
          )}
        </section>
      </div>
    </>
  );
}
