import { expect, test } from "@playwright/test";

test("payment lookup needs confirmation and never implies paid", async ({
  page,
}) => {
  let calls = 0;
  const invoice = {
    id: "8b517c2d-bc5a-435f-82be-c9bb0d940001",
    lead_id: "8b517c2d-bc5a-435f-82be-c9bb0d940002",
    application_id: "8b517c2d-bc5a-435f-82be-c9bb0d940003",
    amount: 10025,
    currency: "INR",
    status: "created",
    creation_state: "uncertain",
    attempts: 1,
    error_code: "network_ambiguous",
    link_sent: false,
    delivery_status: null,
    created_at: "2026-10-23T12:00:00Z",
  };
  await page.route("**/api/**", async (route) => {
    const path = new URL(route.request().url()).pathname;
    let body: unknown = [];
    if (path === "/api/staff/me")
      body = {
        email: "admin@example.test",
        role: "admin",
        institution: "Synthetic Institute",
      };
    if (path === "/api/staff/payments") body = [invoice];
    if (path === "/api/staff/leads")
      body = [
        {
          id: invoice.lead_id,
          status: "payment_pending",
          course: "Synthetic course",
          course_id: null,
        },
      ];
    if (path === `/api/staff/leads/${invoice.lead_id}`) {
      const older = new URL(route.request().url()).searchParams.has("cursor");
      body = {
        id: invoice.lead_id,
        status: "payment_pending",
        course_id: null,
        batch_id: null,
        batch_name: null,
        memory: { facts: {} },
        older_cursor: older ? null : "opaque-cursor",
        messages: [
          {
            message_id: older ? "student:older" : "payment:latest",
            event_id: invoice.lead_id,
            direction: older ? "inbound" : "outbound",
            kind: older ? "student" : "payment_paid",
            text: older
              ? "Earlier student message"
              : "Payment delivery needs review",
            status: older ? "done" : "uncertain",
            created_at: invoice.created_at,
          },
        ],
      };
    }
    if (path.endsWith("/reconcile")) {
      calls++;
      invoice.error_code = "awaiting_signed_confirmation";
      invoice.creation_state = "created";
      body = { result: "awaiting_signed_confirmation" };
    }
    await route.fulfill({ json: body });
  });
  await page.goto("/");
  await page.getByRole("button", { name: "Payments", exact: true }).click();
  await page.getByRole("button", { name: /₹100\.25/ }).click();
  await page
    .getByRole("button", { name: "Check provider", exact: true })
    .click();
  expect(calls).toBe(0);
  await expect(
    page.getByRole("group", { name: "Confirm payment action" }),
  ).toContainText("No new payment link will be created.");
  await page.getByRole("button", { name: "Confirm", exact: true }).click();
  await expect(page.getByRole("status")).toContainText("remains unconfirmed");
  expect(calls).toBe(1);
  await expect(
    page.getByRole("region", { name: "Payment detail" }),
  ).toContainText("awaiting signed confirmation");
  await expect(
    page.getByRole("button", { name: "Retry request", exact: true }),
  ).toHaveCount(0);
  for (const width of [1440, 390]) {
    await page.setViewportSize({ width, height: 1000 });
    await expect(page.locator("body")).toHaveJSProperty("scrollWidth", width);
    await page.screenshot({
      path: `test-results/payments-${width}.png`,
      fullPage: true,
    });
  }
  await page.getByRole("button", { name: "View inquiry", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Admissions inquiries", exact: true }),
  ).toBeVisible();
  await expect(
    page.getByText("Payment delivery needs review", { exact: true }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Load earlier messages", exact: true })
    .click();
  await expect(
    page.getByText("Earlier student message", { exact: true }),
  ).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Load earlier messages", exact: true }),
  ).toHaveCount(0);
  await expect(page.locator(".conversation .message")).toHaveCount(2);
  for (const width of [1440, 390]) {
    await page.setViewportSize({ width, height: 1000 });
    await expect(page.locator("body")).toHaveJSProperty("scrollWidth", width);
    await page.screenshot({
      path: `test-results/transcript-${width}.png`,
      fullPage: true,
    });
  }
});
