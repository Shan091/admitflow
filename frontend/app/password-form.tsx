"use client";
import { useState } from "react";
import type { FormEvent } from "react";

export default function PasswordForm({
  request,
  onError,
  onDone,
}: {
  request: (path: string, init?: RequestInit) => Promise<unknown>;
  onError: (error: unknown) => string;
  onDone: () => Promise<void>;
}) {
  const [current, setCurrent] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [pending, setPending] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  async function save(event: FormEvent) {
    event.preventDefault();
    setError("");
    setNotice("");
    if (password !== confirm) {
      setError("The new passwords do not match.");
      return;
    }
    setPending(true);
    try {
      await request("/staff/password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          current_password: current,
          new_password: password,
        }),
      });
      setCurrent("");
      setPassword("");
      setConfirm("");
      setNotice("Password changed. Other sessions have been signed out.");
      await onDone();
    } catch (error) {
      setError(onError(error));
    } finally {
      setPending(false);
    }
  }
  return (
    <form
      className="account-form"
      onSubmit={(event) => void save(event)}
      aria-busy={pending}
    >
      <h2>Change your password</h2>
      <p>
        Use at least 12 characters. Choose a private password that differs from
        your current one.
      </p>
      <label>
        Current password
        <input
          type="password"
          autoComplete="current-password"
          value={current}
          maxLength={1024}
          required
          onChange={(event) => setCurrent(event.target.value)}
        />
      </label>
      <label>
        New private password
        <input
          type="password"
          autoComplete="new-password"
          value={password}
          minLength={12}
          maxLength={1024}
          required
          onChange={(event) => setPassword(event.target.value)}
        />
      </label>
      <label>
        Confirm new password
        <input
          type="password"
          autoComplete="new-password"
          value={confirm}
          minLength={12}
          maxLength={1024}
          required
          onChange={(event) => setConfirm(event.target.value)}
        />
      </label>
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
      <button className="primary" disabled={pending}>
        {pending ? "Changing password…" : "Save private password"}
      </button>
    </form>
  );
}
