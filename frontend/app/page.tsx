"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import type { FormEvent, InputHTMLAttributes } from "react";
import Admissions from "./admissions";
import Management from "./management";
import Applications from "./applications";
import Payments from "./payments";
import DeliveryBudget from "./delivery-budget";
import Analytics from "./analytics";
import Exports from "./exports";
import Integrations from "./integrations";
import Notifications from "./notifications";
import PasswordForm from "./password-form";

type Staff = {
  email: string;
  role: string;
  institution: string;
  must_change_password?: boolean;
  institution_code?: string;
};
type Doc = {
  id: string;
  filename: string;
  relative_path: string;
  byte_size: number;
  status: "queued" | "processing" | "ready" | "failed";
  error_code: string | null;
  chunk_count: number;
  attempts: number;
  course_id?: string | null;
};
type Match = {
  text: string;
  source: string;
  document_id: string;
  chunk: number;
  similarity: number;
};
const errors: Record<string, string> = {
  unsupported_type: "Choose a PDF, DOCX, TXT, Markdown or CSV file.",
  unsafe_path: "This folder path cannot be imported.",
  file_too_large: "This file exceeds the 10 MB limit.",
  batch_too_large: "Split this selection into smaller batches.",
  invalid_document:
    "This file could not be read. Export a new copy and try again.",
  password_protected: "Remove the PDF password before uploading.",
  ocr_required:
    "This PDF contains scanned or blank pages. Upload a fully searchable PDF.",
  archive_limit: "This Word file exceeds safe extraction limits.",
  text_limit: "Split this document into smaller files.",
  page_limit: "Use a PDF with at most 100 pages.",
  no_text: "This document has no readable text.",
  invalid_text: "Save this text file as UTF-8 and try again.",
  processing_timeout: "Indexing took too long. Retry or split the file.",
  indexing_failed: "Indexing failed. Check the embedding service and retry.",
};

async function api(path: string, init: RequestInit = {}) {
  const response = await fetch(`/api${path}`, {
    ...init,
    credentials: "same-origin",
    cache: "no-store",
    headers: { "X-AdmitFlow-Request": "1", ...init.headers },
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message =
      typeof body.detail === "string"
        ? body.detail
        : `The request could not be completed (${response.status}).`;
    throw Object.assign(new Error(message), { status: response.status });
  }
  return body;
}

function Icon({ kind }: { kind: "file" | "upload" | "search" | "folder" }) {
  const paths = {
    file: (
      <>
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <path d="M14 2v6h6M8 13h8M8 17h5" />
      </>
    ),
    upload: (
      <>
        <path d="M12 16V3m-5 5 5-5 5 5M4 16v4h16v-4" />
      </>
    ),
    search: (
      <>
        <circle cx="10.5" cy="10.5" r="6.5" />
        <path d="m16 16 5 5" />
      </>
    ),
    folder: <path d="M3 7V5h6l2 2h10v13H3z" />,
  };
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      {paths[kind]}
    </svg>
  );
}

export default function Knowledge() {
  const [view, setView] = useState<
    | "overview"
    | "knowledge"
    | "leads"
    | "requests"
    | "management"
    | "applications"
    | "payments"
    | "exports"
    | "integrations"
    | "account"
  >("overview");
  const [staff, setStaff] = useState<Staff | null>(null);
  const [inquiryFocus, setInquiryFocus] = useState<string | null>(null);
  const [checking, setChecking] = useState(true);
  const [docs, setDocs] = useState<Doc[]>([]);
  const [knowledgeCourses, setKnowledgeCourses] = useState<
    { id: string; name: string; is_active: boolean }[]
  >([]);
  const [searchCourse, setSearchCourse] = useState("");
  const [knowledgeCoursesReady, setKnowledgeCoursesReady] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [busy, setBusy] = useState(false);
  const [pending, setPending] = useState<string | null>(null);
  const [progress, setProgress] = useState("");
  const [query, setQuery] = useState("");
  const [searching, setSearching] = useState(false);
  const [matches, setMatches] = useState<Match[] | null>(null);
  const [searchMessage, setSearchMessage] = useState("");
  const [searchError, setSearchError] = useState("");
  const [filter, setFilter] = useState("");
  const [offset, setOffset] = useState(0);
  const [deleteId, setDeleteId] = useState<string | null>(null);
  const fileInput = useRef<HTMLInputElement>(null);
  const folderInput = useRef<HTMLInputElement>(null);
  const folderAttributes = {
    webkitdirectory: "",
    directory: "",
  } as InputHTMLAttributes<HTMLInputElement>;

  const sessionFailure = useCallback((e: unknown) => {
    if (e instanceof Error && "status" in e && e.status === 401) {
      setStaff(null);
      setDocs([]);
      setMatches(null);
    }
    return e instanceof Error ? e.message : "Something went wrong. Try again.";
  }, []);
  const refresh = useCallback(async () => {
    try {
      setDocs(await api(`/knowledge/documents?offset=${offset}&limit=100`));
    } catch (e) {
      setError(sessionFailure(e));
    }
  }, [offset, sessionFailure]);

  useEffect(() => {
    api("/staff/me")
      .then(setStaff)
      .catch((e) => {
        if (!(e instanceof Error && "status" in e && e.status === 401)) {
          setError(
            "The workspace could not be reached. Check the connection and reload.",
          );
        }
      })
      .finally(() => setChecking(false));
  }, []);
  useEffect(() => {
    if (!staff || staff.must_change_password) return;
    void refresh();
    const timer = setInterval(() => {
      if (document.visibilityState === "visible") void refresh();
    }, 4000);
    return () => clearInterval(timer);
  }, [staff, refresh]);
  useEffect(() => {
    if (!staff || staff.must_change_password || view !== "knowledge") return;
    let active = true;
    setKnowledgeCourses([]);
    setKnowledgeCoursesReady(false);
    setSearchCourse("");
    api("/staff/catalog")
      .then((courses) => { if (active) {
        setKnowledgeCourses(courses);
        setKnowledgeCoursesReady(true);
      } })
      .catch((error) => { if (active) setError(sessionFailure(error)); });
    return () => { active = false; };
  }, [staff, view, sessionFailure]);

  async function login(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setBusy(true);
    const data = new FormData(event.currentTarget);
    try {
      await api("/staff/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(Object.fromEntries(data)),
      });
      setStaff(await api("/staff/me"));
    } catch (e) {
      setError(sessionFailure(e));
    } finally {
      setBusy(false);
    }
  }

  async function upload(files: File[]) {
    if (!files.length || busy) return;
    setBusy(true);
    setError("");
    setNotice("");
    setMatches(null);
    let accepted = 0,
      duplicates = 0;
    const rejected: string[] = [];
    try {
      let batch: File[] = [],
        bytes = 0,
        sent = 0;
      async function send() {
        if (!batch.length) return;
        setProgress(
          `Uploading ${sent + 1}–${sent + batch.length} of ${files.length} files`,
        );
        const data = new FormData();
        batch.forEach((file) =>
          data.append("files", file, file.webkitRelativePath || file.name),
        );
        const result = await api("/knowledge/documents", {
          method: "POST",
          body: data,
        });
        accepted += result.accepted.filter(
          (d: { duplicate: boolean }) => !d.duplicate,
        ).length;
        duplicates += result.accepted.filter(
          (d: { duplicate: boolean }) => d.duplicate,
        ).length;
        result.rejected.forEach((d: { filename: string; error_code: string }) =>
          rejected.push(
            `${d.filename}: ${errors[d.error_code] || d.error_code}`,
          ),
        );
        sent += batch.length;
        batch = [];
        bytes = 0;
      }
      for (const file of files) {
        if (file.size > 10 * 1024 * 1024) {
          rejected.push(`${file.name}: exceeds 10 MB.`);
          continue;
        }
        if (batch.length === 25 || bytes + file.size > 28 * 1024 * 1024)
          await send();
        batch.push(file);
        bytes += file.size;
      }
      await send();
      setNotice(
        `${accepted} ${accepted === 1 ? "document" : "documents"} accepted for indexing.${duplicates ? ` ${duplicates} already in your library.` : ""}`,
      );
      if (rejected.length) setError(rejected.join("\n"));
      setOffset(0);
      await refresh();
    } catch (e) {
      setError(
        `${sessionFailure(e)} Previously accepted files remain in your library.`,
      );
    } finally {
      setBusy(false);
      setProgress("");
      if (fileInput.current) fileInput.current.value = "";
      if (folderInput.current) folderInput.current.value = "";
    }
  }

  async function action(doc: Doc, kind: "retry" | "delete") {
    setPending(doc.id);
    setError("");
    try {
      await api(
        `/knowledge/documents/${doc.id}${kind === "retry" ? "/retry" : ""}`,
        { method: kind === "retry" ? "POST" : "DELETE" },
      );
      setDeleteId(null);
      setMatches(null);
      await refresh();
    } catch (e) {
      setError(sessionFailure(e));
    } finally {
      setPending(null);
    }
  }

  async function assignScope(doc: Doc, courseId: string) {
    setPending(doc.id);
    setError("");
    setNotice("");
    setMatches(null);
    try {
      await api(`/knowledge/documents/${doc.id}/scope`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ course_id: courseId || null }),
      });
      setMatches(null);
      setNotice(`Course scope updated for ${doc.filename}.`);
      await refresh();
    } catch (error) {
      setError(sessionFailure(error));
    } finally {
      setPending(null);
    }
  }

  async function search(event: FormEvent) {
    event.preventDefault();
    setSearching(true);
    setMatches(null);
    setSearchError("");
    setSearchMessage("");
    try {
      const result = await api("/knowledge/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, course_id: searchCourse || null }),
      });
      setMatches(result.matches);
      setSearchMessage(result.message);
    } catch (e) {
      setSearchError(sessionFailure(e));
    } finally {
      setSearching(false);
    }
  }

  if (checking)
    return (
      <main className="session-loading" aria-busy="true">
        Opening your workspace…
      </main>
    );
  if (!staff)
    return (
      <main className="login-shell">
        <div className="login-story">
          <a className="brand" href="/">
            Admit<span>Flow</span>
            <span className="brand-dot" />
          </a>
          <div>
            <h1>
              Institution knowledge.
              <br />
              Ready for the next question.
            </h1>
            <p>
              A single place for the documents that inform your admissions
              conversations.
            </p>
          </div>
          <p className="quiet">
            Your institution’s workspace. Your institution’s information.
          </p>
        </div>
        <div className="login-form">
          <form onSubmit={login}>
            <h2>Welcome back</h2>
            <p>Sign in to manage and search your institution’s documents.</p>
            <label>
              Institution code
              <input
                name="institution"
                autoComplete="organization"
                pattern="[a-z0-9-]+"
                required
                placeholder="Your institution code"
              />
            </label>
            <label>
              Work email
              <input
                type="email"
                name="email"
                autoComplete="username"
                required
                placeholder="you@institution.edu"
              />
            </label>
            <label>
              Password
              <input
                type="password"
                name="password"
                autoComplete="current-password"
                required
              />
            </label>
            {error && (
              <p className="error" role="alert">
                {error}
              </p>
            )}
            <button className="primary full" disabled={busy}>
              {busy ? "Signing in…" : "Sign in"}
            </button>
            <p className="quiet small">
              Access is provisioned by your institution administrator.
            </p>
          </form>
        </div>
      </main>
    );

  if (staff.must_change_password)
    return (
      <main className="password-setup">
        <a className="brand" href="/">
          AdmitFlow
        </a>
        <h1>Set your private password</h1>
        <p>
          Your initial password provides setup access only. Choose a private
          password before viewing institution data.
        </p>
        <PasswordForm
          request={api}
          onError={sessionFailure}
          onDone={async () => setStaff((await api("/staff/me")) as Staff)}
        />
        <button
          className="text-button"
          onClick={async () => {
            await api("/staff/logout", { method: "POST" });
            setStaff(null);
          }}
        >
          Sign out
        </button>
      </main>
    );

  const visible = docs.filter((d) =>
    d.relative_path.toLowerCase().includes(filter.toLowerCase()),
  );
  const ready = docs.filter((d) => d.status === "ready").length;
  return (
    <div className="workspace">
      <aside className="sidebar">
        <a className="brand" href="/">
          Admit<span>Flow</span>
          <span className="brand-dot" />
        </a>
        <div className="institution">
          <span className="institution-avatar">
            {staff.institution.slice(0, 1)}
          </span>
          <div>
            <strong>{staff.institution}</strong>
            <span>Institution workspace</span>
          </div>
        </div>
        <nav aria-label="Workspace" className="workspace-nav">
          {(
            [
              ["overview", "Overview"],
              ["knowledge", "Knowledge library"],
              ["leads", "Admissions inquiries"],
              ["requests", "Staff requests"],
              ["management", "Institution management"],
              ["applications", "Applications"],
              ["payments", "Payments"],
              ["account", "Your account"],
              ...(staff.role === "admin"
                ? ([
                    ["exports", "Data exports"],
                    ["integrations", "Outbound webhooks"],
                  ] as const)
                : []),
            ] as const
          ).map(([key, label]) => (
            <button
              type="button"
              key={key}
              aria-current={view === key ? "page" : undefined}
              onClick={() => setView(key)}
            >
              {label}
            </button>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <span className="small">{staff.email}</span>
          <button
            className="text-button"
            onClick={async () => {
              try {
                await api("/staff/logout", { method: "POST" });
                setStaff(null);
                setDocs([]);
                setMatches(null);
              } catch (e) {
                setError(sessionFailure(e));
              }
            }}
          >
            Sign out
          </button>
        </div>
      </aside>
      <main className="main">
        <header className="topbar">
          <span>
            Workspace <span className="slash">/</span>{" "}
            {view === "overview"
              ? "Overview"
              : view === "knowledge"
                ? "Knowledge"
                : view === "leads"
                  ? "Inquiries"
                  : view === "management"
                    ? "Institution management"
                    : view === "applications"
                      ? "Applications"
                      : view === "payments"
                        ? "Payments"
                        : view === "exports"
                          ? "Data exports"
                          : view === "account"
                            ? "Your account"
                            : view === "integrations"
                              ? "Outbound webhooks"
                              : "Staff requests"}
          </span>
          <div className="topbar-actions">
            <span className="role">
              {staff.role === "admin" ? "Administrator" : "Staff member"}
            </span>
            <Notifications
              request={api}
              onError={sessionFailure}
              onOpenInquiry={(id) => {
                setInquiryFocus(id);
                setView("leads");
              }}
            />
          </div>
        </header>
        <div className="content">
          <DeliveryBudget request={api} onError={sessionFailure} />
          {view === "overview" ? (
            <Analytics request={api} onError={sessionFailure} />
          ) : view === "management" ? (
            <Management
              request={api}
              onError={sessionFailure}
              admin={staff.role === "admin"}
              institutionCode={staff.institution_code || ""}
            />
          ) : view === "applications" ? (
            <Applications
              request={api}
              onError={sessionFailure}
              admin={staff.role === "admin"}
              onOpenInquiry={(id) => {
                setInquiryFocus(id);
                setView("leads");
              }}
            />
          ) : view === "payments" ? (
            <Payments
              request={api}
              onError={sessionFailure}
              admin={staff.role === "admin"}
              onOpenInquiry={(id) => {
                setInquiryFocus(id);
                setView("leads");
              }}
            />
          ) : view === "exports" ? (
            <Exports onError={sessionFailure} />
          ) : view === "integrations" ? (
            <Integrations request={api} onError={sessionFailure} />
          ) : view === "account" ? (
            <>
              <header className="page-heading">
                <div>
                  <h1>Your account</h1>
                  <p>{staff.email}</p>
                </div>
              </header>
              <PasswordForm
                request={api}
                onError={sessionFailure}
                onDone={async () => setStaff((await api("/staff/me")) as Staff)}
              />
            </>
          ) : view !== "knowledge" ? (
            <Admissions
              key={view}
              view={view}
              request={api}
              onError={sessionFailure}
              initialLead={inquiryFocus}
              admin={staff.role === "admin"}
              onDeleted={() => setInquiryFocus(null)}
            />
          ) : (
            <>
              <header className="page-heading">
                <div>
                  <h1>Knowledge library</h1>
                  <p>
                    The source material behind better admissions conversations.
                  </p>
                </div>
                <span className="library-count">
                  {ready} ready on this page
                </span>
              </header>
              {staff.role === "admin" && (
                <section
                  className={`upload-zone ${busy ? "uploading" : ""}`}
                  aria-label="Upload institution documents"
                  onDragOver={(event) => event.preventDefault()}
                  onDrop={(event) => {
                    event.preventDefault();
                    if (
                      Array.from(event.dataTransfer.items).some(
                        (i) => i.webkitGetAsEntry()?.isDirectory,
                      )
                    ) {
                      setError(
                        "Use Choose folder to import a folder and its contents.",
                      );
                      return;
                    }
                    void upload(Array.from(event.dataTransfer.files));
                  }}
                >
                  <div className="upload-icon">
                    <Icon kind="upload" />
                  </div>
                  <div className="upload-copy">
                    <h2>
                      {busy
                        ? progress || "Preparing your documents…"
                        : "Bring your institution’s knowledge together"}
                    </h2>
                    <p>
                      Drop files here, or choose a folder to import its
                      contents.
                    </p>
                    <span className="quiet small">
                      PDF, DOCX, TXT, Markdown and CSV · Up to 10 MB per file ·
                      Readable text only
                    </span>
                  </div>
                  <div className="upload-actions">
                    <button
                      className="primary"
                      disabled={busy}
                      onClick={() => fileInput.current?.click()}
                    >
                      Choose files
                    </button>
                    <button
                      className="secondary"
                      disabled={busy}
                      onClick={() => folderInput.current?.click()}
                    >
                      Choose folder
                    </button>
                    <input
                      ref={fileInput}
                      className="visually-hidden"
                      aria-label="Choose documents"
                      type="file"
                      multiple
                      accept=".pdf,.docx,.txt,.md,.csv"
                      onChange={(e) =>
                        void upload(Array.from(e.target.files || []))
                      }
                    />
                    <input
                      ref={folderInput}
                      className="visually-hidden"
                      aria-label="Choose a document folder"
                      type="file"
                      multiple
                      {...folderAttributes}
                      onChange={(e) =>
                        void upload(Array.from(e.target.files || []))
                      }
                    />
                  </div>
                </section>
              )}
              <div aria-live="polite">
                {notice && <p className="notice">{notice}</p>}
                {error && (
                  <p className="error preserve" role="alert">
                    {error}
                  </p>
                )}
              </div>
              <section className="library" aria-labelledby="documents-title">
                <div className="section-header">
                  <h2 id="documents-title">
                    Your documents <span className="count">{docs.length}</span>
                  </h2>
                  <label className="filter">
                    <Icon kind="search" />
                    <input
                      aria-label="Filter documents on this page"
                      placeholder="Find a document…"
                      value={filter}
                      onChange={(e) => setFilter(e.target.value)}
                    />
                  </label>
                </div>
                {docs.length === 0 ? (
                  <div className="empty">
                    <Icon kind="file" />
                    <h3>Your library starts here</h3>
                    <p>
                      Upload your prospectus, fee information or FAQs. Once
                      indexed, your team can search their contents.
                    </p>
                  </div>
                ) : visible.length === 0 ? (
                  <p className="empty">No documents match this filter.</p>
                ) : (
                  <div
                    className="table-scroll"
                    role="region"
                    aria-label="Institution documents"
                    tabIndex={0}
                  >
                    <table>
                      <thead>
                        <tr>
                          <th>Document</th>
                          <th>Status</th>
                          <th>Indexed passages</th>
                          <th>
                            <span className="visually-hidden">Actions</span>
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {visible.map((doc) => (
                          <tr key={doc.id}>
                            <td>
                              <div className="file-name">
                                <Icon kind="file" />
                                <div>
                                  <strong>{doc.filename}</strong>
                                  <span>
                                    {doc.relative_path !== doc.filename
                                      ? `${doc.relative_path} · `
                                      : ""}
                                    {Math.max(
                                      1,
                                      Math.round(doc.byte_size / 1024),
                                    )}{" "}
                                    KB
                                  </span>
                                  {staff.role === "admin" ? (
                                    <label className="document-course-scope">
                                      Use this document for
                                      <select
                                        aria-label={`Course scope for ${doc.filename}`}
                                        value={doc.course_id || ""}
                                        disabled={!knowledgeCoursesReady || pending !== null || doc.status !== "ready"}
                                        onChange={(event) => void assignScope(doc, event.target.value)}
                                      >
                                        <option value="">Shared institution information</option>
                                        {doc.course_id && !knowledgeCourses.some((course) => course.id === doc.course_id) && (
                                          <option value={doc.course_id}>{knowledgeCoursesReady ? "Assigned course unavailable" : "Loading assigned course…"}</option>
                                        )}
                                        {knowledgeCourses.map((course) => (
                                          <option key={course.id} value={course.id}>{course.name}</option>
                                        ))}
                                      </select>
                                    </label>
                                  ) : (
                                    <span>{doc.course_id ? knowledgeCourses.find((course) => course.id === doc.course_id)?.name || "Assigned course unavailable" : "Shared institution information"}</span>
                                  )}
                                  {doc.error_code && (
                                    <p className="file-error">
                                      {errors[doc.error_code] ||
                                        "Indexing failed. Try uploading a new copy."}
                                    </p>
                                  )}
                                </div>
                              </div>
                            </td>
                            <td>
                              <span className={`status ${doc.status}`}>
                                <i />
                                {
                                  {
                                    queued: "Queued",
                                    processing: "Indexing",
                                    ready: "Ready",
                                    failed: "Needs attention",
                                  }[doc.status]
                                }
                              </span>
                            </td>
                            <td className="numeric">
                              {doc.status === "ready" ? doc.chunk_count : "—"}
                            </td>
                            <td>
                              {staff.role === "admin" && (
                                <div className="row-actions">
                                  {doc.status === "failed" && (
                                    <button
                                      className="text-button"
                                      disabled={pending === doc.id}
                                      onClick={() => void action(doc, "retry")}
                                    >
                                      Retry
                                    </button>
                                  )}
                                  {deleteId === doc.id ? (
                                    <>
                                      <button
                                        className="danger"
                                        disabled={pending === doc.id}
                                        onClick={() =>
                                          void action(doc, "delete")
                                        }
                                      >
                                        {pending === doc.id
                                          ? "Removing…"
                                          : "Remove permanently"}
                                      </button>
                                      <button
                                        className="text-button"
                                        onClick={() => setDeleteId(null)}
                                      >
                                        Cancel
                                      </button>
                                    </>
                                  ) : (
                                    <button
                                      className="text-button muted"
                                      disabled={pending === doc.id}
                                      onClick={() => setDeleteId(doc.id)}
                                    >
                                      Remove
                                    </button>
                                  )}
                                </div>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
                {(offset > 0 || docs.length === 100) && (
                  <div className="pagination">
                    <button
                      className="secondary"
                      disabled={offset === 0}
                      onClick={() => {
                        setOffset(Math.max(0, offset - 100));
                        setFilter("");
                      }}
                    >
                      Previous
                    </button>
                    <span>Page {Math.floor(offset / 100) + 1}</span>
                    <button
                      className="secondary"
                      disabled={docs.length < 100}
                      onClick={() => {
                        setOffset(offset + 100);
                        setFilter("");
                      }}
                    >
                      Next
                    </button>
                  </div>
                )}
              </section>
              <section
                className="search-section"
                aria-labelledby="search-title"
              >
                <div className="search-intro">
                  <h2 id="search-title">Find the answer in your documents</h2>
                  <p>
                    Search in your own words. Results show the original passages
                    and where they came from.
                  </p>
                </div>
                <label className="knowledge-search-course">
                  Search course
                  <select aria-label="Search course" value={searchCourse} disabled={!knowledgeCoursesReady} onChange={(event) => {
                    setSearchCourse(event.target.value);
                    setMatches(null);
                  }}>
                    <option value="">All documents</option>
                    {knowledgeCourses.map((course) => (
                      <option key={course.id} value={course.id}>{course.name} and shared information</option>
                    ))}
                  </select>
                </label>
                <form className="search-form" onSubmit={search}>
                  <label className="search-box">
                    <Icon kind="search" />
                    <input
                      aria-label="Search institution knowledge"
                      placeholder="For example, what are the hostel fees?"
                      value={query}
                      minLength={2}
                      maxLength={1000}
                      required
                      onChange={(e) => setQuery(e.target.value)}
                    />
                  </label>
                  <button
                    className="primary"
                    disabled={searching || query.trim().length < 2}
                  >
                    {searching ? "Searching…" : "Search knowledge"}
                  </button>
                </form>
                {searchError && (
                  <p role="alert" className="error">
                    {searchError}
                  </p>
                )}
                <div
                  className="results"
                  aria-live="polite"
                  aria-busy={searching}
                >
                  {searching && (
                    <p className="quiet">Finding relevant passages…</p>
                  )}
                  {matches && matches.length === 0 && (
                    <p className="no-match">{searchMessage}</p>
                  )}
                  {matches?.map((match, index) => (
                    <article
                      className="result"
                      key={`${match.document_id}-${match.chunk}`}
                    >
                      <div className="source-line">
                        <Icon kind="file" />
                        <strong>{match.source}</strong>
                        <span>Passage {match.chunk}</span>
                      </div>
                      <p>{match.text}</p>
                      <span className="result-number">Result {index + 1}</span>
                    </article>
                  ))}
                </div>
              </section>
              <footer className="workspace-footer">
                Knowledge stays within your institution. Only ready documents
                appear in search.
              </footer>
            </>
          )}
        </div>
      </main>
    </div>
  );
}
