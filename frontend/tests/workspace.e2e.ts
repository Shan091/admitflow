import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { expect, test } from "@playwright/test";

test("administrator manages catalog and discount codes", async ({
  page,
  context,
}) => {
  const credentials = JSON.parse(
    readFileSync(resolve("../backend/.demo-credentials.json"), "utf8"),
  );
  const login = await context.request.post("/api/staff/login", {
    data: credentials,
    headers: { "X-AdmitFlow-Request": "1" },
  });
  expect(login.ok()).toBe(true);
  await page.goto("/");
  await page
    .getByRole("button", { name: "Institution management", exact: true })
    .click();
  await page.getByRole("button", { name: "New course", exact: true }).click();
  const name = `Synthetic catalog check ${Date.now()}`;
  await page.getByLabel("Course name", { exact: true }).fill(name);
  await page
    .getByLabel("Application fee (INR)", { exact: true })
    .fill("100.25");
  await page.getByRole("button", { name: "Add batch", exact: true }).click();
  await page.getByLabel("Batch name", { exact: true }).fill("Morning");
  await page.getByRole("button", { name: "Add rule", exact: true }).click();
  await page.getByRole("button", { name: "Save course", exact: true }).click();
  await expect(page.getByRole("status")).toHaveText(
    "Course, batches and eligibility rules saved.",
  );
  const catalog = await (
    await context.request.get("/api/staff/catalog")
  ).json();
  const course = catalog.find((item: { name: string }) => item.name === name);
  expect(course.application_fee).toBe(10025);
  expect(course.rules[0].value).toBe(18);
  await page
    .getByRole("button", { name: "Archive course", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Confirm archive", exact: true })
    .click();
  await expect(page.getByRole("status")).toHaveText(
    "Course archived. Saved inquiries retain their history.",
  );
  await page
    .getByRole("button", { name: "Discount codes", exact: true })
    .click();
  await page.getByRole("button", { name: "New discount", exact: true }).click();
  await page
    .getByLabel("Discount code", { exact: true })
    .fill(`CHECK-${Date.now()}`);
  await page.getByLabel("Discount type", { exact: true }).selectOption("flat");
  await page.getByLabel("Amount off (INR)", { exact: true }).fill("10.50");
  await page
    .getByRole("button", { name: "Save discount", exact: true })
    .click();
  await expect(page.getByRole("status")).toHaveText("Discount code saved.");
  const discounts = await (
    await context.request.get("/api/staff/discounts")
  ).json();
  expect(
    discounts.some(
      (item: { amount: number; discount_type: string }) =>
        item.amount === 1050 && item.discount_type === "flat",
    ),
  ).toBe(true);
  for (const width of [1440, 390]) {
    await page.setViewportSize({ width, height: 1000 });
    await expect
      .poll(() =>
        page.evaluate(() => document.documentElement.scrollWidth <= innerWidth),
      )
      .toBe(true);
    await page.screenshot({
      path: `test-results/discounts-${width}.png`,
      fullPage: true,
    });
  }
  await page
    .getByRole("button", { name: "Deactivate discount", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Confirm deactivation", exact: true })
    .click();
  await expect(page.getByRole("status")).toHaveText(
    "Discount code deactivated. Existing payment records are preserved.",
  );
  await page.getByRole("button", { name: "Sign out", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Welcome back" }),
  ).toBeVisible();
});

test("real staff login, live upload/search and persisted Telegram inquiry", async ({
  page,
}) => {
  const credentials = JSON.parse(
    readFileSync(resolve("../backend/.demo-credentials.json"), "utf8"),
  );
  await page.goto("/");
  await page.getByLabel("Institution code").fill(credentials.institution);
  await page.getByLabel("Work email").fill(credentials.email);
  await page.getByLabel("Password", { exact: true }).fill(credentials.password);
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Knowledge library", exact: true }),
  ).toBeVisible();

  await page.getByLabel("Choose documents", { exact: true }).setInputFiles({
    name: "synthetic-campus-reference.txt",
    mimeType: "text/plain",
    buffer: Buffer.from(
      "Synthetic institution reference. The demo campus is in Kochi. The library is open from 9 AM to 5 PM. Hostel accommodation is available on campus. This is synthetic demonstration data.",
    ),
  });
  const row = page
    .getByRole("row")
    .filter({ hasText: "synthetic-campus-reference.txt" });
  await expect(row.getByText("Ready", { exact: true })).toBeVisible({
    timeout: 65000,
  });
  await page
    .getByLabel("Search institution knowledge")
    .fill("Where is the demo campus?");
  await page.getByRole("button", { name: "Search knowledge" }).click();
  await expect(
    page.locator(".result").filter({ hasText: "Kochi" }),
  ).toBeVisible({ timeout: 20000 });

  await page
    .getByRole("button", { name: "Admissions inquiries", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Admissions inquiries", exact: true }),
  ).toBeVisible();
  // Application QA records can be newer than the handset conversation. Select
  // actual persisted inbound evidence instead of assuming the first row is it.
  const inquiries = (await (
    await page.request.get("/api/staff/leads")
  ).json()) as { id: string }[];
  let savedInquiry: string | null = null;
  for (const candidate of inquiries) {
    const detail = await (
      await page.request.get(`/api/staff/leads/${candidate.id}`)
    ).json();
    if (
      detail.messages.some(
        (message: { direction: string }) => message.direction === "inbound",
      )
    ) {
      savedInquiry = candidate.id;
      break;
    }
  }
  expect(
    savedInquiry,
    "The demo must contain a real saved student message",
  ).not.toBeNull();
  const inquiry = page
    .locator(".inquiry-row")
    .filter({ hasText: `Inquiry ${savedInquiry!.slice(0, 8)}` });
  await expect(inquiry).toBeVisible({ timeout: 15000 });
  await inquiry.click();
  await expect(
    page.getByRole("heading", { name: "Conversation", exact: true }),
  ).toBeVisible();
  await expect(page.locator(".message.inbound").first()).toBeVisible();
  for (const viewport of [
    { width: 1440, height: 1000 },
    { width: 390, height: 844 },
  ]) {
    await page.setViewportSize(viewport);
    await expect
      .poll(() =>
        page.evaluate(() => document.documentElement.scrollWidth <= innerWidth),
      )
      .toBe(true);
    await page.screenshot({
      path: `test-results/inquiries-${viewport.width}.png`,
      fullPage: true,
    });
  }
  await page
    .getByRole("button", { name: "Staff requests", exact: true })
    .click();
  await expect(
    page.getByRole("heading", { name: "Staff requests", exact: true }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Sign out", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Welcome back" }),
  ).toBeVisible();
});
