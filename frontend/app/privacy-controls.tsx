"use client";
import { useState } from "react";

export default function PrivacyControls({
  leadId,
  request,
  onError,
  onDeleted,
}: {
  leadId: string;
  request: (path: string, init?: RequestInit) => Promise<unknown>;
  onError: (error: unknown) => string;
  onDeleted: () => void;
}) {
  const [confirm, setConfirm] = useState(false);
  const [typed, setTyped] = useState("");
  const [pending, setPending] = useState(false);
  const [error, setError] = useState("");
  async function erase() {
    setPending(true);
    setError("");
    try {
      await request(`/staff/leads/${leadId}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ confirm_id: leadId }),
      });
      onDeleted();
    } catch (error) {
      setError(onError(error));
    } finally {
      setPending(false);
    }
  }
  return (
    <section className="privacy-controls" aria-label="Inquiry data privacy">
      <h3>Inquiry data privacy</h3>
      {confirm ? (
        <>
          <p>
            Delete this institution’s inquiry, conversation, facts, application,
            payment records and linked deliveries permanently. This cannot be
            undone. Messages already delivered remain in Telegram.
          </p>
          <label>
            Enter {leadId.slice(0, 8)} to confirm
            <input
              value={typed}
              autoComplete="off"
              onChange={(event) => setTyped(event.target.value)}
            />
          </label>
          {error && (
            <p className="error" role="alert">
              {error}
            </p>
          )}
          <button
            className="danger"
            disabled={pending || typed !== leadId.slice(0, 8)}
            onClick={() => void erase()}
          >
            {pending ? "Deleting…" : "Confirm permanent deletion"}
          </button>
          <button
            className="text-button"
            disabled={pending}
            onClick={() => {
              setConfirm(false);
              setTyped("");
            }}
          >
            Cancel deletion
          </button>
        </>
      ) : (
        <button className="text-button" onClick={() => setConfirm(true)}>
          Delete inquiry data
        </button>
      )}
    </section>
  );
}
