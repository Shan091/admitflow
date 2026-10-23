"use client";

import { useEffect, useState } from "react";

type Usage = {
  available: boolean;
  attempts: number | null;
  confirmed_sent: number | null;
  limit: number;
  remaining: number | null;
  warning: boolean;
  deferred: number;
  resets_at: string;
  timezone: string;
};

export default function DeliveryBudget({
  request,
  onError,
}: {
  request: (path: string) => Promise<unknown>;
  onError: (error: unknown) => string;
}) {
  const [usage, setUsage] = useState<Usage | null>(null);
  const [failed, setFailed] = useState(false);
  useEffect(() => {
    let active = true;
    async function refresh() {
      try {
        const result = (await request("/staff/delivery-budget")) as Usage;
        if (active) {
          setUsage(result);
          setFailed(typeof result.available !== "boolean");
        }
      } catch (error) {
        if (active) {
          onError(error);
          setFailed(true);
        }
      }
    }
    void refresh();
    const timer = setInterval(() => void refresh(), 60000);
    const changed = () => void refresh();
    window.addEventListener("admitflow:budget-changed", changed);
    return () => {
      active = false;
      clearInterval(timer);
      window.removeEventListener("admitflow:budget-changed", changed);
    };
  }, [request, onError]);
  if (!usage && !failed) return null;
  if (failed || !usage?.available)
    return (
      <div
        className="delivery-budget warning"
        role="region"
        aria-label="Telegram delivery budget"
        aria-live="polite"
      >
        Delivery status is unavailable. Queued replies will wait if delivery
        limits cannot be checked.
      </div>
    );
  let reset = "the next institution day";
  try {
    reset =
      new Date(usage.resets_at).toLocaleString("en-IN", {
        timeZone: usage.timezone,
        day: "numeric",
        month: "short",
        hour: "2-digit",
        minute: "2-digit",
      }) + ` (${usage.timezone})`;
  } catch {
    /* Legacy timezone settings must not break the workspace. */
  }
  return (
    <div
      className={`delivery-budget${usage.warning ? " warning" : ""}`}
      role="region"
      aria-label="Telegram delivery budget"
      aria-live="polite"
    >
      <strong>
        {usage.limit === 0
          ? "Telegram sends paused"
          : usage.remaining === 0
            ? "Daily delivery budget reached"
            : usage.warning
              ? "Approaching daily delivery budget"
              : "Tracked Telegram delivery today"}
      </strong>
      <span>
        {usage.attempts} of {usage.limit} send attempts · {usage.confirmed_sent}{" "}
        confirmed delivered.
      </span>
      {(usage.warning || usage.deferred > 0) && (
        <span>
          {usage.deferred > 0
            ? `${usage.deferred} ${usage.deferred === 1 ? "reply" : "replies"} waiting. `
            : ""}
          {usage.limit === 0
            ? "An administrator can increase the limit in institution settings."
            : `Budget resets ${reset}. Replies stay queued when the limit is reached.`}
        </span>
      )}
    </div>
  );
}
