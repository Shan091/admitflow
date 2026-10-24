import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { expect, test } from "@playwright/test";

for (const width of [1440, 390]) {
  test(`demo application review stays clearly separate from seat allocation at ${width}px`, async ({ page, context }) => {
    const credentials = JSON.parse(readFileSync(resolve("../backend/.demo-credentials.json"), "utf8"));
    const login = await context.request.post("/api/staff/login", {
      data: credentials, headers: { "X-AdmitFlow-Request": "1" },
    });
    expect(login.ok()).toBe(true);
    const application = {
      id: "synthetic-demo", lead_id: "synthetic-inquiry", course: "Synthetic programme",
      status: "under_review", is_demo: true, submitted_at: "2026-10-24T00:00:00Z",
      payments: ["paid"], form: { full_name: "Synthetic Student" },
    };
    await page.route("**/api/staff/applications**", async route => {
      expect(route.request().method()).toBe("GET");
      await route.fulfill({ json: route.request().url().includes("synthetic-demo") ? application : [application] });
    });
    await page.setViewportSize({ width, height: 1000 });
    await page.goto("/");
    await page.getByRole("button", { name: "Applications", exact: true }).click();
    await page.getByRole("button", { name: "Synthetic programme", exact: false }).click();
    await expect(page.getByText("Demo application · Razorpay test payment required.", { exact: false })).toBeVisible();
    await page.getByRole("button", { name: "Approve application", exact: true }).click();
    await expect(page.getByText("Approve this demo application?", { exact: false })).toContainText("No university seat will be allocated.");
    expect(await page.locator("body").evaluate(body => body.scrollWidth)).toBeLessThanOrEqual(width);
    if (process.env.CAPTURE_UI === "1") await page.screenshot({ path: `test-results/demo-application-${width}.png`, fullPage: true });
  });
}
