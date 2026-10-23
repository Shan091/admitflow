"use client";

import { useEffect, useRef, useState } from "react";

export type StaffDraft = {
  id: string;
  text?: string;
  evidence?: string;
  status: string;
};
type Request = (path: string, init?: RequestInit) => Promise<unknown>;

export default function StaffControls({
  leadId,
  active,
  draft,
  stale,
  request,
  onError,
  onRefresh,
}: {
  leadId: string;
  active: boolean;
  draft?: StaffDraft;
  stale: boolean;
  request: Request;
  onError: (error: unknown) => string;
  onRefresh: () => Promise<void>;
}) {
  const [text, setText] = useState("");
  const [draftText, setDraftText] = useState(draft?.text || "");
  const [reviewed, setReviewed] = useState(false);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [confirm, setConfirm] = useState<
    "takeover" | "resume" | "send" | "approve" | null
  >(null);
  const manual = useRef<{ text: string; request_id: string } | null>(null);
  const generation = useRef<string | null>(null);
  useEffect(() => {
    setDraftText(draft?.text || "");
    setReviewed(false);
  }, [draft?.id, draft?.text]);
  async function post(path: string, body?: unknown) {
    return request(`/staff/leads/${leadId}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
    });
  }
  async function run(action: string) {
    if (pending) return;
    setPending(true);
    setError("");
    setNotice("");
    try {
      if (action === "takeover" || action === "resume") {
        await post(`/${action}`);
        setNotice(
          action === "takeover"
            ? "Staff takeover is active. Bot replies are paused."
            : "AI will continue on the next student message.",
        );
      } else if (action === "send") {
        const value = text.trim();
        if (!manual.current || manual.current.text !== value)
          manual.current = { text: value, request_id: crypto.randomUUID() };
        await post("/messages", manual.current);
        setText("");
        manual.current = null;
        setNotice(
          "Staff reply queued. Check its delivery in the conversation.",
        );
      } else if (action === "generate") {
        generation.current ||= crypto.randomUUID();
        await post("/draft", { request_id: generation.current });
        generation.current = null;
        setNotice("Draft ready for review. Nothing has been sent.");
      } else if (draft) {
        await post(`/draft/${draft.id}`, {
          decision: action === "ignore" ? "ignore" : "approve",
          reviewed,
          ...(action === "ignore" ? {} : { text: draftText }),
        });
        setReviewed(false);
        setNotice(
          action === "ignore"
            ? "Draft ignored. Nothing was sent."
            : "Reviewed staff reply queued. Check its delivery below.",
        );
      }
      setConfirm(null);
      await onRefresh();
    } catch (e) {
      if (
        e instanceof Error &&
        "status" in e &&
        [409, 503].includes(Number(e.status))
      )
        generation.current = null;
      setError(onError(e));
    } finally {
      setPending(false);
    }
  }
  const pendingDraft = draft?.status === "pending";
  return (
    <section
      className="staff-panel"
      aria-label="Staff conversation controls"
      aria-busy={pending}
    >
      <div className="management-toolbar">
        <h3>{active ? "Staff takeover" : "Conversation controls"}</h3>
        <span className="status queued">
          {active ? "Bot replies paused" : "AI available"}
        </span>
      </div>
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
      {!active ? (
        <>
          <p className="quiet small">
            Take over to answer personally or review an AI draft. Incoming
            messages remain saved.
          </p>
          <button
            className="secondary"
            disabled={pending}
            onClick={() => setConfirm("takeover")}
          >
            Take over
          </button>
        </>
      ) : (
        <>
          <div className="staff-actions">
            <button
              className="secondary"
              disabled={pending}
              onClick={() => void run("generate")}
            >
              {pending ? "Working…" : "Generate co-pilot draft"}
            </button>
            <button
              className="text-button"
              disabled={pending}
              onClick={() => setConfirm("resume")}
            >
              Resume AI
            </button>
          </div>
          {draft?.status === "generating" && (
            <p className="quiet small">
              A draft is being generated. Refresh the inquiry to check its
              state.
            </p>
          )}
          {draft?.status === "failed" && (
            <p className="quiet small">
              Draft generation failed. Try again or write a staff reply.
            </p>
          )}
          {(pendingDraft || draft?.status === "stale") && (
            <div className="management-form staff-draft">
              <h4>Co-pilot draft</h4>
              <p className="quiet small">
                Review the wording, facts and reference lookup. A draft does not
                make an admission or payment decision.
              </p>
              {stale && (
                <p role="status" className="error">
                  The conversation changed or this draft expired. Generate a
                  fresh draft before approving.
                </p>
              )}
              <label>
                Review or edit draft
                <textarea
                  value={draftText}
                  maxLength={3500}
                  rows={5}
                  disabled={pending || stale}
                  onChange={(e) => {
                    setDraftText(e.target.value);
                    setReviewed(false);
                    setConfirm(null);
                  }}
                />
              </label>
              {draft?.evidence && (
                <details className="evidence">
                  <summary>Reference lookup</summary>
                  <p>{draft.evidence}</p>
                </details>
              )}
              <label className="management-check">
                <input
                  type="checkbox"
                  checked={reviewed}
                  disabled={pending || stale}
                  onChange={(e) => setReviewed(e.target.checked)}
                />
                I reviewed the wording, facts and sources.
              </label>
              <div className="staff-actions">
                <button
                  className="primary"
                  disabled={pending || stale || !reviewed || !draftText.trim()}
                  onClick={() => setConfirm("approve")}
                >
                  Approve reply
                </button>
                <button
                  className="text-button"
                  disabled={pending}
                  onClick={() => void run("ignore")}
                >
                  Ignore draft
                </button>
              </div>
            </div>
          )}
          <div className="management-form staff-compose">
            <label>
              Staff reply
              <textarea
                value={text}
                maxLength={3500}
                rows={4}
                disabled={pending}
                onChange={(e) => {
                  setText(e.target.value);
                  setConfirm(null);
                }}
                placeholder="Write a reply for this student"
              />
            </label>
            <button
              className="secondary"
              disabled={pending || !text.trim()}
              onClick={() => setConfirm("send")}
            >
              Send staff reply
            </button>
          </div>
        </>
      )}
      {confirm && (
        <div
          className="management-archive"
          role="group"
          aria-label="Confirm conversation action"
        >
          <p>
            {confirm === "takeover"
              ? "Pause bot replies and take responsibility for responding to this student?"
              : confirm === "resume"
                ? "Resolve the staff request and resume AI on the next student message? Queued staff replies must finish first."
                : "Queue this exact reply for the student? Its delivery status will appear in the conversation."}
          </p>
          {(confirm === "send" || confirm === "approve") && (
            <p className="staff-preview">
              {confirm === "send" ? text : draftText}
            </p>
          )}
          <button
            className="primary"
            disabled={pending}
            onClick={() => void run(confirm)}
          >
            {pending ? "Saving…" : "Confirm"}
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
    </section>
  );
}
