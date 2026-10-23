"use client";

import { useEffect, useRef, useState } from "react";

type Notice = {
  id: string;
  kind: string;
  lead_id: string | null;
  created_at: string;
  unread: boolean;
};
type Snapshot = { unread_count: number; items: Notice[] };
const labels: Record<string, string> = {
  qualified: "New eligible inquiry",
  delivery: "Message delivery needs attention",
  draft: "Co-pilot draft ready",
  payment: "Payment received",
};

export default function Notifications({
  request,
  onError,
  onOpenInquiry,
}: {
  request: (path: string, init?: RequestInit) => Promise<unknown>;
  onError: (error: unknown) => string;
  onOpenInquiry: (id: string) => void;
}) {
  const [open, setOpen] = useState(false);
  const [snapshot, setSnapshot] = useState<Snapshot>({
    unread_count: 0,
    items: [],
  });
  const [connection, setConnection] = useState("Connecting");
  const [error, setError] = useState("");
  const socket = useRef<WebSocket | null>(null);
  useEffect(() => {
    if (!open) return;
    const escape = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpen(false);
    };
    document.addEventListener("keydown", escape);
    return () => document.removeEventListener("keydown", escape);
  }, [open]);
  useEffect(() => {
    let disposed = false;
    let timer: ReturnType<typeof setTimeout>;
    let backoff = 1000;
    const apply = (value: unknown) => {
      const data = value as Snapshot;
      if (
        !disposed &&
        Number.isInteger(data?.unread_count) &&
        Array.isArray(data.items)
      )
        setSnapshot(data);
    };
    const refresh = () =>
      request("/staff/notifications")
        .then(apply)
        .catch((error) => {
          if (!disposed) setError(onError(error));
        });
    const connect = () => {
      if (disposed) return;
      const channel = new WebSocket(
        `${location.protocol === "https:" ? "wss:" : "ws:"}//${location.host}/api/staff/notifications/ws`,
      );
      socket.current = channel;
      channel.onopen = () => {
        backoff = 1000;
        setConnection("Live updates connected");
        setError("");
      };
      channel.onmessage = (event) => {
        try {
          apply(JSON.parse(event.data));
        } catch {
          setError("An update could not be read. Refresh the page.");
        }
      };
      channel.onclose = () => {
        if (disposed) return;
        setConnection("Reconnecting to live updates");
        void refresh();
        timer = setTimeout(connect, backoff);
        backoff = Math.min(backoff * 2, 30000);
      };
    };
    void refresh();
    connect();
    return () => {
      disposed = true;
      clearTimeout(timer);
      socket.current?.close();
      socket.current = null;
    };
  }, [request, onError]);
  async function mark(ids: string[]) {
    if (!ids.length) return;
    const payload = { action: "acknowledge", ids };
    if (socket.current?.readyState === WebSocket.OPEN)
      socket.current.send(JSON.stringify(payload));
    else {
      try {
        await request("/staff/notifications/read", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        setSnapshot((await request("/staff/notifications")) as Snapshot);
      } catch (error) {
        setError(onError(error));
      }
    }
  }
  return (
    <div className="notification-center">
      <button
        className="notification-toggle"
        aria-expanded={open}
        aria-controls="notification-panel"
        aria-label={`Notifications (${snapshot.unread_count} unread)`}
        onClick={() => setOpen(!open)}
      >
        <svg
          aria-hidden="true"
          viewBox="0 0 24 24"
          width="18"
          height="18"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.7"
        >
          <path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9M10 21h4" />
        </svg>
        <span>Notifications</span>
        <span className="notification-count">{snapshot.unread_count}</span>
      </button>
      {open && (
        <section
          id="notification-panel"
          className="notification-panel"
          aria-label="Notifications"
        >
          <h2>Notifications</h2>
          <p className="small">
            {connection}. Read status is saved for your account.
          </p>
          {error && (
            <p className="error" role="alert">
              {error}
            </p>
          )}
          {snapshot.items.length ? (
            <>
              <button
                className="text-button"
                disabled={!snapshot.items.some((item) => item.unread)}
                onClick={() =>
                  void mark(
                    snapshot.items
                      .filter((item) => item.unread)
                      .map((item) => item.id),
                  )
                }
              >
                Mark shown as read
              </button>
              <ul>
                {snapshot.items.map((item) => (
                  <li key={item.id} className={item.unread ? "unread" : ""}>
                    <strong>{labels[item.kind] || "Institution update"}</strong>
                    <time dateTime={item.created_at}>
                      {new Date(item.created_at).toLocaleString("en-IN", {
                        dateStyle: "medium",
                        timeStyle: "short",
                      })}
                    </time>
                    {item.lead_id && (
                      <button
                        className="text-button"
                        onClick={() => {
                          void mark([item.id]);
                          onOpenInquiry(item.lead_id!);
                          setOpen(false);
                        }}
                      >
                        Open inquiry
                      </button>
                    )}
                  </li>
                ))}
              </ul>
            </>
          ) : (
            <p>
              No notifications yet. Eligibility, delivery, draft and payment
              updates will appear here.
            </p>
          )}
          <button className="text-button" onClick={() => setOpen(false)}>
            Close notifications
          </button>
        </section>
      )}
    </div>
  );
}
