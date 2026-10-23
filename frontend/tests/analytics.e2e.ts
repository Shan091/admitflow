import { expect, test } from "@playwright/test";

test("overview shows real denominators, period controls and recoverable empty/error states", async ({
  page,
}) => {
  let fail = false;
  let empty = false;
  const queries: string[] = [];
  const states = [
    "new",
    "discovering",
    "qualifying",
    "admission_ready",
    "form_collecting",
    "payment_pending",
    "under_review",
    "enrolled",
    "rejected",
    "waitlisted",
    "handed_off",
    "cold",
  ];
  await page.route("**/api/**", async (route) => {
    const url = new URL(route.request().url());
    let body: unknown = [];
    if (url.pathname === "/api/staff/me")
      body = {
        email: "admin@example.test",
        role: "admin",
        institution: "Synthetic Institute",
      };
    if (url.pathname === "/api/staff/delivery-budget")
      body = {
        available: true,
        attempts: 100,
        confirmed_sent: 98,
        limit: 1000,
        remaining: 900,
        warning: false,
        deferred: 0,
        resets_at: "2026-10-26T18:30:00Z",
        timezone: "Asia/Kolkata",
      };
    if (url.pathname === "/api/staff/analytics") {
      queries.push(url.search);
      if (fail)
        return route.fulfill({
          status: 503,
          json: {
            detail: "The overview is temporarily unavailable. Try again.",
          },
        });
      const weekly = url.searchParams.get("bucket") === "week";
      body = {
        period: {
          from: "2026-10-24",
          to: "2026-10-26",
          bucket: weekly ? "week" : "day",
          timezone: "Asia/Kolkata",
        },
        totals: {
          inquiries: empty ? 0 : 10,
          applicants: empty ? 0 : 5,
          fee_paid: empty ? 0 : 2,
          fee_waived: empty ? 0 : 2,
        },
        conversions: {
          application: {
            converted: empty ? 0 : 5,
            of: empty ? 0 : 10,
            percent: empty ? null : 50,
          },
          enrollment: {
            converted: empty ? 0 : 3,
            of: empty ? 0 : 5,
            percent: empty ? null : 60,
          },
          fee_satisfied: {
            converted: empty ? 0 : 4,
            of: empty ? 0 : 5,
            percent: empty ? null : 80,
          },
        },
        stages: states.map((state, index) => ({
          state,
          current: empty
            ? 0
            : (
                {
                  new: 1,
                  discovering: 2,
                  qualifying: 1,
                  form_collecting: 1,
                  payment_pending: 1,
                  under_review: 1,
                  enrolled: 3,
                } as Record<string, number>
              )[state] || 0,
          reached: empty ? 0 : Math.max(0, 10 - index),
          percent: empty ? null : Math.max(0, 100 - index * 10),
        })),
        series: (weekly
          ? [
              { period: "2026-10-19", count: 7 },
              { period: "2026-10-26", count: 3 },
            ]
          : [
              { period: "2026-10-24", count: 5 },
              { period: "2026-10-25", count: 2 },
              { period: "2026-10-26", count: 3 },
            ]
        ).map((point) => ({ ...point, count: empty ? 0 : point.count })),
        coverage:
          "Inquiries created in the selected period; progress as of now. Stage reach includes recorded transitions and current states. Earlier transitions are not inferred; stages may be skipped.",
        as_of: "2026-10-26T12:00:00Z",
      };
    }
    await route.fulfill({ json: body });
  });
  await page.goto("/");
  await expect(
    page.getByRole("heading", { name: "Admissions overview", exact: true }),
  ).toBeVisible();
  await expect(
    page.getByText("5 of 10 inquiries applied", { exact: true }),
  ).toBeVisible();
  await expect(
    page.getByText("3 of 5 applicants enrolled", { exact: true }),
  ).toBeVisible();
  await expect(
    page.getByRole("img", { name: /New inquiries by day/ }),
  ).toBeVisible();
  for (const width of [1440, 390]) {
    await page.setViewportSize({ width, height: 1000 });
    await page.evaluate(() => window.scrollTo(0, 0));
    await expect(page.locator("body")).toHaveJSProperty("scrollWidth", width);
    if (process.env.CAPTURE_UI === "1")
      await page.screenshot({
        path: `test-results/analytics-${width}.png`,
        fullPage: true,
      });
  }
  await page.getByLabel("Group inquiries").selectOption("week");
  await page.getByRole("button", { name: "Apply period", exact: true }).click();
  await expect(
    page.getByText("Weekly, starting Monday in the institution timezone.", {
      exact: true,
    }),
  ).toBeVisible();
  expect(
    queries.some(
      (query) =>
        query.includes("bucket=week") && query.includes("from=2026-10-24"),
    ),
  ).toBe(true);
  fail = true;
  await page
    .getByRole("button", { name: "Refresh overview", exact: true })
    .click();
  await expect(
    page
      .getByRole("region", { name: "Admissions analytics" })
      .getByRole("alert"),
  ).toContainText("temporarily unavailable");
  fail = false;
  empty = true;
  await page.getByRole("button", { name: "Try again", exact: true }).click();
  await expect(
    page.getByText(/No inquiries were created in this period/),
  ).toBeVisible();
  await expect(page.locator("body")).not.toContainText("NaN");
  await expect(
    page.getByText("0 of 0 inquiries applied", { exact: true }),
  ).toBeVisible();
});
