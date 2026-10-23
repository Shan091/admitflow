"use client";
import { useCallback, useEffect, useState } from "react";
import type { FormEvent } from "react";

type User = {
  id: string;
  email: string;
  role: string;
  is_active: boolean;
  must_change_password: boolean;
  is_you: boolean;
};
export default function StaffAccounts({
  request,
  onError,
  institutionCode,
}: {
  request: (path: string, init?: RequestInit) => Promise<unknown>;
  onError: (error: unknown) => string;
  institutionCode: string;
}) {
  const [users, setUsers] = useState<User[]>([]);
  const [offset, setOffset] = useState(0);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("agent");
  const [selected, setSelected] = useState<User | null>(null);
  const [editRole, setEditRole] = useState("agent");
  const [active, setActive] = useState(true);
  const [reset, setReset] = useState("");
  const [pending, setPending] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const load = useCallback(async () => {
    try {
      setUsers((await request(`/staff/users?offset=${offset}`)) as User[]);
    } catch (error) {
      setError(onError(error));
    }
  }, [offset, request, onError]);
  useEffect(() => {
    void load();
  }, [load]);
  async function mutate(
    path: string,
    method: string,
    body: unknown,
    notice: string,
  ) {
    setPending(true);
    setError("");
    setNotice("");
    try {
      await request(path, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      setNotice(notice);
      setPassword("");
      setReset("");
      setSelected(null);
      await load();
    } catch (error) {
      setError(onError(error));
    } finally {
      setPending(false);
    }
  }
  function create(event: FormEvent) {
    event.preventDefault();
    void mutate(
      "/staff/users",
      "POST",
      { email: email.trim().toLowerCase(), password, role },
      "Staff account created. Share the initial password securely; a private password is required before institution data can be viewed.",
    );
  }
  return (
    <section aria-label="Staff accounts">
      <h2>Staff accounts</h2>
      {institutionCode && (
        <p>
          Staff sign in with institution code <strong>{institutionCode}</strong>
          , their email and their initial password.
        </p>
      )}
      <p>
        Administrators manage access for this institution. Role changes,
        deactivation and password resets end the affected account’s sessions.
      </p>
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
      <form className="account-form" onSubmit={create} aria-busy={pending}>
        <h3>Create an account</h3>
        <label>
          Staff email
          <input
            type="email"
            value={email}
            maxLength={320}
            required
            onChange={(event) => setEmail(event.target.value)}
            autoComplete="off"
          />
        </label>
        <label>
          New account role
          <select
            value={role}
            onChange={(event) => setRole(event.target.value)}
          >
            <option value="agent">Staff member</option>
            <option value="admin">Administrator</option>
          </select>
        </label>
        <label>
          Initial password
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
        <button className="primary" disabled={pending}>
          Create staff account
        </button>
      </form>
      <h3>Current accounts</h3>
      {users.map((user) => (
        <article className="staff-account-row" key={user.id}>
          <div>
            <strong>
              {user.email}
              {user.is_you ? " (you)" : ""}
            </strong>
            <p>
              {user.role === "admin" ? "Administrator" : "Staff member"} ·{" "}
              {user.is_active ? "Active" : "Inactive"}
              {user.must_change_password
                ? " · Private password setup required"
                : ""}
            </p>
          </div>
          <button
            className="secondary"
            onClick={() => {
              setSelected(user);
              setEditRole(user.role);
              setActive(user.is_active);
              setReset("");
            }}
          >
            Manage {user.email}
          </button>
        </article>
      ))}
      <div className="account-pagination">
        <button
          className="secondary"
          disabled={offset === 0}
          onClick={() => setOffset(Math.max(0, offset - 50))}
        >
          Previous accounts
        </button>
        <button
          className="secondary"
          disabled={users.length < 50}
          onClick={() => setOffset(offset + 50)}
        >
          Next accounts
        </button>
      </div>
      {selected && (
        <section className="account-editor" aria-label="Manage staff account">
          <h3>{selected.email}</h3>
          <label>
            Account role
            <select
              value={editRole}
              onChange={(event) => setEditRole(event.target.value)}
            >
              <option value="agent">Staff member</option>
              <option value="admin">Administrator</option>
            </select>
          </label>
          <label className="check">
            <input
              type="checkbox"
              checked={active}
              onChange={(event) => setActive(event.target.checked)}
            />
            Account active
          </label>
          <p>
            At least one active administrator with a private password must
            remain.
          </p>
          <button
            className="primary"
            disabled={pending}
            onClick={() =>
              void mutate(
                `/staff/users/${selected.id}`,
                "PUT",
                { role: editRole, is_active: active },
                "Staff access updated. Previous sessions have ended.",
              )
            }
          >
            Save staff access
          </button>
          {!selected.is_you && (
            <>
              <label>
                Replacement initial password
                <input
                  type="password"
                  autoComplete="new-password"
                  value={reset}
                  minLength={12}
                  maxLength={1024}
                  onChange={(event) => setReset(event.target.value)}
                />
              </label>
              <button
                className="secondary"
                disabled={pending || reset.length < 12}
                onClick={() =>
                  void mutate(
                    `/staff/users/${selected.id}/reset-password`,
                    "POST",
                    { password: reset },
                    "Password reset. Share it securely; the account must set a private password before viewing data.",
                  )
                }
              >
                Reset staff password
              </button>
            </>
          )}
          <button className="text-button" onClick={() => setSelected(null)}>
            Cancel account changes
          </button>
        </section>
      )}
    </section>
  );
}
