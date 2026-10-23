"use client";

import { useCallback, useEffect, useState } from "react";

type Request = (path: string, init?: RequestInit) => Promise<unknown>;
type Configuration = {
  configured: boolean;
  enabled: boolean;
  host: string | null;
  counts: Record<string, number>;
  deliveries: {
    id: string;
    event_id: string;
    status: string;
    attempts: number;
    error_code: string | null;
    created_at: string;
  }[];
};

export default function Integrations({
  request,
  onError,
}: {
  request: Request;
  onError: (error: unknown) => string;
}) {
  const [configuration, setConfiguration] = useState<Configuration | null>(
    null,
  );
  const [url, setUrl] = useState("");
  const [enabled, setEnabled] = useState(false);
  const [rotate, setRotate] = useState(false);
  const [secret, setSecret] = useState("");
  const [reveal, setReveal] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [pending, setPending] = useState(false);
  const load = useCallback(async () => {
    try {
      const data = (await request("/staff/integrations")) as Configuration;
      setConfiguration(data);
      setEnabled(data.enabled);
    } catch (error) {
      setError(onError(error));
    }
  }, [request, onError]);
  useEffect(() => {
    void load();
  }, [load]);
  async function save(event: React.FormEvent) {
    event.preventDefault();
    setPending(true);
    setError("");
    setNotice("");
    setSecret("");
    try {
      const result = (await request("/staff/integrations", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url: url.trim() || null,
          enabled,
          rotate_secret: rotate,
        }),
      })) as { signing_secret: string | null };
      setSecret(result.signing_secret || "");
      setUrl("");
      setRotate(false);
      setNotice(
        "Webhook configuration saved. New events will use this configuration.",
      );
      await load();
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
          <h1>Outbound webhooks</h1>
          <p>Send signed institution events to your approved integration.</p>
        </div>
        <button className="secondary" onClick={() => void load()}>
          Refresh delivery status
        </button>
      </header>
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
      {configuration ? (
        <>
          <form
            className="integration-form"
            onSubmit={(event) => void save(event)}
            aria-busy={pending}
          >
            <h2>
              {configuration.configured
                ? `Destination: ${configuration.host}`
                : "Connect an integration"}
            </h2>
            <p>
              Events contain record references and state changes. Student names,
              contact details and conversations are excluded. Only public HTTPS
              destinations on port 443 are supported.
            </p>
            <label>
              Destination URL
              <input
                type="url"
                value={url}
                onChange={(event) => setUrl(event.target.value)}
                maxLength={2048}
                required={!configuration.configured}
                placeholder={
                  configuration.configured
                    ? "Leave blank to keep the current URL"
                    : "https://your-service.example/events"
                }
                autoComplete="off"
              />
            </label>
            <label className="check">
              <input
                type="checkbox"
                checked={enabled}
                onChange={(event) => setEnabled(event.target.checked)}
              />
              Enable event delivery
            </label>
            {configuration.configured && (
              <label className="check">
                <input
                  type="checkbox"
                  checked={rotate}
                  onChange={(event) => setRotate(event.target.checked)}
                />
                Rotate the signing secret
              </label>
            )}
            <p>
              Saving cancels queued events from the previous configuration.
              Requests already in progress may still arrive. Receivers must
              deduplicate the delivery ID before taking action.
            </p>
            <button className="primary" disabled={pending}>
              {pending ? "Saving…" : "Save webhook"}
            </button>
          </form>
          {secret && (
            <section
              className="integration-secret"
              aria-label="New signing secret"
            >
              <h2>Save the signing secret</h2>
              <p>
                This value is shown once. Store it securely in your receiver
                before processing events.
              </p>
              <label>
                Signing secret
                <input
                  readOnly
                  type={reveal ? "text" : "password"}
                  value={secret}
                  autoComplete="off"
                />
              </label>
              <button
                className="text-button"
                type="button"
                onClick={() => setReveal(!reveal)}
              >
                {reveal ? "Hide secret" : "Reveal secret"}
              </button>{" "}
              <button
                className="secondary"
                onClick={async () => {
                  try {
                    await navigator.clipboard.writeText(secret);
                    setNotice("Signing secret copied. Store it securely.");
                  } catch {
                    setError(
                      "Copy was unavailable. Select the secret field and copy it securely.",
                    );
                  }
                }}
              >
                Copy signing secret
              </button>
            </section>
          )}
          <section
            className="integration-deliveries"
            aria-label="Webhook deliveries"
          >
            <h2>Recent deliveries</h2>
            <p>
              {Object.entries(configuration.counts)
                .map(([state, count]) => `${state}: ${count}`)
                .join(" · ") || "No events have been queued."}
            </p>
            {configuration.deliveries.length ? (
              <ul>
                {configuration.deliveries.map((row) => (
                  <li key={row.id}>
                    <strong>Delivery {row.id.slice(0, 8)}</strong>
                    <span>
                      {row.status} · {row.attempts} attempts
                      {row.error_code
                        ? ` · ${row.error_code.replaceAll("_", " ")}`
                        : ""}
                    </span>
                    <time dateTime={row.created_at}>
                      {new Date(row.created_at).toLocaleString("en-IN")}
                    </time>
                  </li>
                ))}
              </ul>
            ) : (
              <p>
                New eligible events appear after delivery is enabled. Earlier
                events are not replayed.
              </p>
            )}
          </section>
        </>
      ) : (
        <p className="empty">Loading integration settings…</p>
      )}
    </>
  );
}
