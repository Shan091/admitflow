"use client";

import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import Discounts from "./discounts";
import StaffAccounts from "./staff-accounts";

type Batch = {
  id?: string;
  name: string;
  capacity: number;
  seats_remaining: number;
  is_active: boolean;
};
type Rule = {
  field: string;
  operator: string;
  value: string | number | boolean | (string | number)[];
};
type Course = {
  id?: string;
  name: string;
  description: string;
  application_fee: number;
  is_active: boolean;
  batches: Batch[];
  is_reference?: boolean;
  reference_url?: string | null;
  rules: Rule[];
};
type Settings = {
  name: string;
  timezone: string;
  business_hours: Record<string, { start: string; end: string }>;
  reengagement_delay_days: number;
  telegram_daily_send_limit: number;
  retention_days: number | null;
};
const empty: Course = {
  name: "",
  description: "",
  application_fee: 0,
  is_active: true,
  batches: [],
  rules: [],
};
const weekdays = [
  ["mon", "Monday"],
  ["tue", "Tuesday"],
  ["wed", "Wednesday"],
  ["thu", "Thursday"],
  ["fri", "Friday"],
  ["sat", "Saturday"],
  ["sun", "Sunday"],
] as const;
const operators = [">=", "<=", "=", "!=", ">", "<", "in", "not_in"];
function valueText(value: Rule["value"]): string {
  return Array.isArray(value) ? value.join(", ") : String(value);
}
function parseValue(text: string, operator: string): Rule["value"] {
  const scalar = (value: string): string | number =>
    /^-?\d+(\.\d+)?$/.test(value.trim()) ? Number(value) : value.trim();
  if (["in", "not_in"].includes(operator)) return text.split(",").map(scalar);
  if (text === "true" || text === "false") return text === "true";
  return scalar(text);
}

export default function Management({
  request,
  onError,
  admin,
  institutionCode = "",
}: {
  request: (path: string, init?: RequestInit) => Promise<unknown>;
  onError: (error: unknown) => string;
  admin: boolean;
  institutionCode?: string;
}) {
  const [tab, setTab] = useState<
    "catalog" | "settings" | "discounts" | "staff"
  >("catalog");
  const [courses, setCourses] = useState<Course[]>([]);
  const [course, setCourse] = useState<Course | null>(null);
  const [settings, setSettings] = useState<Settings | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [archive, setArchive] = useState(false);
  useEffect(() => {
    let active = true;
    Promise.all([request("/staff/catalog"), request("/staff/settings")])
      .then(([catalog, config]) => {
        if (active) {
          setCourses(catalog as Course[]);
          setSettings(config as Settings);
        }
      })
      .catch((e) => {
        if (active) setError(onError(e));
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [request, onError]);
  function choose(item: Course) {
    setCourse(structuredClone(item));
    setArchive(false);
    setNotice("");
    setError("");
  }
  async function save(event: FormEvent) {
    event.preventDefault();
    setSaving(true);
    setError("");
    setNotice("");
    try {
      if (tab === "catalog" && course) {
        const { id, ...body } = course;
        delete body.is_reference;
        delete body.reference_url;
        const saved = (await request(`/staff/catalog${id ? `/${id}` : ""}`, {
          method: id ? "PUT" : "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        })) as Course;
        setCourses((await request("/staff/catalog")) as Course[]);
        setCourse(saved);
        setNotice("Course, batches and eligibility rules saved.");
      } else if (settings) {
        setSettings(
          (await request("/staff/settings", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(settings),
          })) as Settings,
        );
        setNotice("Institution settings saved.");
        window.dispatchEvent(new Event("admitflow:budget-changed"));
      }
    } catch (e) {
      setError(onError(e));
    } finally {
      setSaving(false);
    }
  }
  async function archiveCourse() {
    if (!course?.id) return;
    setSaving(true);
    setError("");
    try {
      await request(`/staff/catalog/${course.id}`, { method: "DELETE" });
      setCourses((await request("/staff/catalog")) as Course[]);
      setCourse({ ...course, is_active: false });
      setArchive(false);
      setNotice("Course archived. Saved inquiries retain their history.");
    } catch (e) {
      setError(onError(e));
    } finally {
      setSaving(false);
    }
  }
  function batch(index: number, values: Partial<Batch>) {
    if (course)
      setCourse({
        ...course,
        batches: course.batches.map((item, i) =>
          i === index ? { ...item, ...values } : item,
        ),
      });
  }
  function rule(index: number, values: Partial<Rule>) {
    if (course)
      setCourse({
        ...course,
        rules: course.rules.map((item, i) =>
          i === index ? { ...item, ...values } : item,
        ),
      });
  }
  return (
    <>
      <header className="page-heading">
        <div>
          <h1>Institution management</h1>
          <p>
            Courses, seats and the rules behind your admissions conversations.
          </p>
        </div>
      </header>
      <div className="management-tabs" aria-label="Management sections">
        {(
          [
            "catalog",
            "discounts",
            "settings",
            ...(admin ? ["staff" as const] : []),
          ] as const
        ).map((item) => (
          <button
            key={item}
            className={tab === item ? "primary" : "secondary"}
            aria-pressed={tab === item}
            onClick={() => {
              setTab(item);
              setNotice("");
              setError("");
            }}
          >
            {item === "catalog"
              ? "Course catalog"
              : item === "discounts"
                ? "Discount codes"
                : item === "staff"
                  ? "Staff accounts"
                  : "Institution settings"}
          </button>
        ))}
      </div>
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
      {!admin && (
        <p className="notice">
          You can review this information. An administrator manages changes.
        </p>
      )}
      {loading ? (
        <p className="empty">Loading institution information…</p>
      ) : tab === "staff" ? (
        <StaffAccounts
          request={request}
          onError={onError}
          institutionCode={institutionCode}
        />
      ) : tab === "discounts" ? (
        <Discounts request={request} onError={onError} admin={admin} />
      ) : tab === "catalog" ? (
        <div className="management-layout">
          <section aria-label="Course catalog">
            <div className="management-toolbar">
              <h2>Courses</h2>
              {admin && (
                <button className="secondary" onClick={() => choose(empty)}>
                  New course
                </button>
              )}
            </div>
            {courses.length === 0 && (
              <p className="empty">
                Create a course, add a batch and define eligibility rules to
                start student inquiries.
              </p>
            )}
            {courses.map((item) => (
              <button
                className="inquiry-row"
                key={item.id}
                aria-pressed={course?.id === item.id}
                onClick={() => choose(item)}
              >
                <strong>{item.name}</strong>
                <span>
                  {item.is_active ? "Active" : "Archived"} ·{" "}
                  {item.batches.filter((b) => b.is_active).length} active
                  batches
                </span>
                <span>
                  Application fee: {item.is_reference
                    ? "Unverified"
                    : `INR ${(item.application_fee / 100).toFixed(2)}`}
                </span>
              </button>
            ))}
          </section>
          <section aria-label="Course editor">
            {!course ? (
              <div className="empty">
                <h2>Select a course</h2>
                <p>
                  Review batches, available seats and institution-owned
                  eligibility rules.
                </p>
              </div>
            ) : (
              <form className="management-form" onSubmit={save}>
                <h2>{course.id ? "Course details" : "New course"}</h2>
                {course.is_reference && (
                  <p className="notice">
                    Published programme for exploration. Fees and intakes are unverified;
                    applications and payments are unavailable here.
                    {course.reference_url && (
                      <> <a href={course.reference_url} target="_blank" rel="noreferrer">University programme page</a></>
                    )}
                  </p>
                )}
                <fieldset disabled={!admin || saving || course.is_reference}>
                  <label>
                    Course name
                    <input
                      required
                      maxLength={255}
                      value={course.name}
                      onChange={(e) =>
                        setCourse({ ...course, name: e.target.value })
                      }
                    />
                  </label>
                  <label>
                    Description
                    <textarea
                      maxLength={10000}
                      rows={3}
                      value={course.description}
                      onChange={(e) =>
                        setCourse({ ...course, description: e.target.value })
                      }
                    />
                  </label>
                  <label>
                    Application fee (INR)
                    <input
                      type="number"
                      min="0"
                      max="10000000"
                      step="0.01"
                      required
                      value={course.is_reference ? "" : course.application_fee / 100}
                      placeholder={course.is_reference ? "Unverified" : undefined}
                      onChange={(e) =>
                        setCourse({
                          ...course,
                          application_fee: Math.round(
                            Number(e.target.value) * 100,
                          ),
                        })
                      }
                    />
                  </label>
                  <label className="management-check">
                    <input
                      type="checkbox"
                      checked={course.is_active}
                      onChange={(e) =>
                        setCourse({ ...course, is_active: e.target.checked })
                      }
                    />
                    Available to students
                  </label>
                  <div className="management-toolbar">
                    <h3>Batches</h3>
                    <button
                      type="button"
                      className="text-button"
                      onClick={() =>
                        setCourse({
                          ...course,
                          batches: [
                            ...course.batches,
                            {
                              name: "",
                              capacity: 20,
                              seats_remaining: 20,
                              is_active: true,
                            },
                          ],
                        })
                      }
                    >
                      Add batch
                    </button>
                  </div>
                  {course.batches.map((item, index) => (
                    <div
                      className="management-subform"
                      key={item.id || `new-${index}`}
                    >
                      <label>
                        Batch name
                        <input
                          required
                          value={item.name}
                          onChange={(e) =>
                            batch(index, { name: e.target.value })
                          }
                        />
                      </label>
                      <div className="management-pair">
                        <label>
                          Capacity
                          <input
                            type="number"
                            min="1"
                            max="1000000"
                            required
                            value={item.capacity}
                            onChange={(e) =>
                              batch(index, { capacity: Number(e.target.value) })
                            }
                          />
                        </label>
                        <label>
                          Available seats
                          <input
                            type="number"
                            min="0"
                            max={item.capacity}
                            required
                            value={item.seats_remaining}
                            onChange={(e) =>
                              batch(index, {
                                seats_remaining: Number(e.target.value),
                              })
                            }
                          />
                        </label>
                      </div>
                      <label className="management-check">
                        <input
                          type="checkbox"
                          checked={item.is_active}
                          onChange={(e) =>
                            batch(index, { is_active: e.target.checked })
                          }
                        />
                        Batch active
                      </label>
                      <button
                        type="button"
                        className="text-button danger"
                        onClick={() =>
                          setCourse({
                            ...course,
                            batches: course.batches.filter(
                              (_, i) => i !== index,
                            ),
                          })
                        }
                      >
                        Remove batch
                      </button>
                    </div>
                  ))}
                  <p className="quiet">
                    Removed batches are archived when saved. Existing inquiries
                    keep their selected batch.
                  </p>
                  <div className="management-toolbar">
                    <h3>Eligibility rules</h3>
                    <button
                      type="button"
                      className="text-button"
                      onClick={() =>
                        setCourse({
                          ...course,
                          rules: [
                            ...course.rules,
                            { field: "age", operator: ">=", value: 18 },
                          ],
                        })
                      }
                    >
                      Add rule
                    </button>
                  </div>
                  {course.rules.map((item, index) => (
                    <div className="management-subform" key={index}>
                      <div className="management-pair">
                        <label>
                          Field
                          <input
                            required
                            pattern="[a-z][a-z0-9_]*"
                            value={item.field}
                            onChange={(e) =>
                              rule(index, { field: e.target.value })
                            }
                          />
                        </label>
                        <label>
                          Comparison
                          <select
                            value={item.operator}
                            onChange={(e) =>
                              rule(index, {
                                operator: e.target.value,
                                value: parseValue(
                                  valueText(item.value),
                                  e.target.value,
                                ),
                              })
                            }
                          >
                            {operators.map((operator) => (
                              <option key={operator}>{operator}</option>
                            ))}
                          </select>
                        </label>
                      </div>
                      <label>
                        {["in", "not_in"].includes(item.operator)
                          ? "Allowed values (separated by commas)"
                          : "Required value"}
                        <input
                          required
                          value={valueText(item.value)}
                          onChange={(e) =>
                            rule(index, {
                              value: parseValue(e.target.value, item.operator),
                            })
                          }
                        />
                      </label>
                      <button
                        type="button"
                        className="text-button danger"
                        onClick={() =>
                          setCourse({
                            ...course,
                            rules: course.rules.filter((_, i) => i !== index),
                          })
                        }
                      >
                        Remove rule
                      </button>
                    </div>
                  ))}
                  <p className="quiet">
                    Without valid rules, eligibility requires staff review. No
                    student is approved automatically.
                  </p>
                  {admin && (
                    <button className="primary" disabled={saving}>
                      {saving ? "Saving…" : "Save course"}
                    </button>
                  )}
                </fieldset>
                {admin && course.id && course.is_active && (
                  <div className="management-archive">
                    {archive ? (
                      <>
                        <p>
                          Archive this course? Students will no longer be able
                          to choose it.
                        </p>
                        <button
                          type="button"
                          className="secondary danger"
                          disabled={saving}
                          onClick={() => void archiveCourse()}
                        >
                          Confirm archive
                        </button>
                        <button
                          type="button"
                          className="text-button"
                          onClick={() => setArchive(false)}
                        >
                          Cancel
                        </button>
                      </>
                    ) : (
                      <button
                        type="button"
                        className="text-button danger"
                        onClick={() => setArchive(true)}
                      >
                        Archive course
                      </button>
                    )}
                  </div>
                )}
              </form>
            )}
          </section>
        </div>
      ) : (
        settings && (
          <form className="management-form management-settings" onSubmit={save}>
            <fieldset disabled={!admin || saving}>
              <h2>Institution settings</h2>
              <label>
                Institution name
                <input
                  required
                  value={settings.name}
                  onChange={(e) =>
                    setSettings({ ...settings, name: e.target.value })
                  }
                />
              </label>
              <label>
                Timezone
                <input
                  required
                  placeholder="Asia/Kolkata"
                  value={settings.timezone}
                  onChange={(e) =>
                    setSettings({ ...settings, timezone: e.target.value })
                  }
                />
              </label>
              <label>
                Daily Telegram send attempts
                <input
                  type="number"
                  min="0"
                  max="100000"
                  required
                  value={settings.telegram_daily_send_limit ?? 1000}
                  onChange={(e) =>
                    setSettings({
                      ...settings,
                      telegram_daily_send_limit: Number(e.target.value),
                    })
                  }
                />
                <span className="quiet">
                  Resets at midnight in the institution timezone. Set 0 to pause
                  sends. Failed or uncertain attempts also use this budget;
                  replies stay queued at the limit.
                </span>
              </label>
              <h3>Business hours</h3>
              <p className="quiet">
                Leave closed days unchecked. Times use your institution
                timezone.
              </p>
              {weekdays.map(([key, label]) => (
                <div className="management-hours" key={key}>
                  <label className="management-check">
                    <input
                      type="checkbox"
                      checked={!!settings.business_hours[key]}
                      onChange={(e) => {
                        const hours = { ...settings.business_hours };
                        if (e.target.checked)
                          hours[key] = { start: "09:00", end: "17:00" };
                        else delete hours[key];
                        setSettings({ ...settings, business_hours: hours });
                      }}
                    />
                    {label}
                  </label>
                  {settings.business_hours[key] && (
                    <>
                      <label>
                        Opens
                        <input
                          type="time"
                          required
                          value={settings.business_hours[key].start}
                          onChange={(e) =>
                            setSettings({
                              ...settings,
                              business_hours: {
                                ...settings.business_hours,
                                [key]: {
                                  ...settings.business_hours[key],
                                  start: e.target.value,
                                },
                              },
                            })
                          }
                        />
                      </label>
                      <label>
                        Closes
                        <input
                          type="time"
                          required
                          value={settings.business_hours[key].end}
                          onChange={(e) =>
                            setSettings({
                              ...settings,
                              business_hours: {
                                ...settings.business_hours,
                                [key]: {
                                  ...settings.business_hours[key],
                                  end: e.target.value,
                                },
                              },
                            })
                          }
                        />
                      </label>
                    </>
                  )}
                </div>
              ))}
              <label>
                Follow-up delay (days)
                <input
                  type="number"
                  min="1"
                  max="365"
                  required
                  value={settings.reengagement_delay_days}
                  onChange={(e) =>
                    setSettings({
                      ...settings,
                      reengagement_delay_days: Number(e.target.value),
                    })
                  }
                />
              </label>
              <label>
                Inactive conversation history (days, blank keeps history)
                <input
                  type="number"
                  min="1"
                  max="3650"
                  value={settings.retention_days ?? ""}
                  onChange={(e) =>
                    setSettings({
                      ...settings,
                      retention_days: e.target.value
                        ? Number(e.target.value)
                        : null,
                    })
                  }
                />
              </label>
              <p className="quiet">
                Scheduled checks apply these values. Follow-ups require student
                consent. Conversation retention clears stored dialogue and saved
                facts after inactivity. Applications and payment records remain;
                complete inquiry erasure requires an administrator’s explicit
                confirmation.
              </p>
              {admin && (
                <button className="primary" disabled={saving}>
                  {saving ? "Saving…" : "Save settings"}
                </button>
              )}
            </fieldset>
          </form>
        )
      )}
    </>
  );
}
