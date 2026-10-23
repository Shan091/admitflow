import { expect, test } from "@playwright/test";

test("delivery warning and an administrator's budget changes remain clear on mobile", async ({
  page,
}) => {
  let config = {
    name: "Synthetic Institute",
    timezone: "Asia/Kolkata",
    business_hours: {},
    reengagement_delay_days: 3,
    retention_days: null,
    telegram_daily_send_limit: 1000,
  };
  let unavailable = false;
  await page.route("**/api/**", async (route) => {
    const path = new URL(route.request().url()).pathname;
    let body: unknown = [];
    if (path === "/api/staff/me")
      body = {
        email: "admin@example.test",
        role: "admin",
        institution: "Synthetic Institute",
      };
    if (path === "/api/staff/settings") {
      if (route.request().method() === "PUT")
        config = route.request().postDataJSON();
      body = config;
    }
    if (path === "/api/staff/delivery-budget")
      body = {
        available: !unavailable,
        attempts: unavailable ? null : 800,
        confirmed_sent: unavailable ? null : 790,
        limit: config.telegram_daily_send_limit,
        remaining: Math.max(0, config.telegram_daily_send_limit - 800),
        warning: config.telegram_daily_send_limit <= 1000,
        deferred: config.telegram_daily_send_limit === 0 ? 2 : 0,
        resets_at: "2026-10-24T18:30:00Z",
        timezone: config.timezone,
      };
    await route.fulfill({ json: body });
  });
  await page.goto("/");
  await page
    .getByRole("button", { name: "Knowledge library", exact: true })
    .click();
  const summary = page.getByRole("region", {
    name: "Telegram delivery budget",
  });
  await expect(summary).toContainText("Approaching daily delivery budget");
  await expect(summary).toContainText("800 of 1000 send attempts");
  for (const width of [1440, 390]) {
    await page.setViewportSize({ width, height: 1000 });
    await page.evaluate(() => window.scrollTo(0, 0));
    await expect(page.locator("body")).toHaveJSProperty("scrollWidth", width);
    if (process.env.CAPTURE_UI === "1")
      await page.screenshot({
        path: `test-results/delivery-budget-${width}.png`,
        fullPage: true,
      });
  }
  await page
    .getByRole("button", { name: "Institution management", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Institution settings", exact: true })
    .click();
  await page.getByLabel("Daily Telegram send attempts").fill("0");
  await page
    .getByRole("button", { name: "Save settings", exact: true })
    .click();
  await expect(summary).toContainText("Telegram sends paused");
  await expect(summary).toContainText("2 replies waiting");
  expect(config.telegram_daily_send_limit).toBe(0);
  await page.getByLabel("Daily Telegram send attempts").fill("2000");
  await page
    .getByRole("button", { name: "Save settings", exact: true })
    .click();
  await expect(summary).toContainText("Telegram delivery today");
  unavailable = true;
  await page.evaluate(() =>
    window.dispatchEvent(new Event("admitflow:budget-changed")),
  );
  await expect(summary).toContainText("Delivery status is unavailable");
  await expect(summary).not.toContainText("0 of");
});
