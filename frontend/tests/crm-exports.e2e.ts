import { expect, test } from "@playwright/test";
import { mkdirSync } from "node:fs";

test("inquiry search uses a private body, all statuses and downloadable exports", async ({
  page,
}) => {
  const bodies: Record<string, unknown>[] = [];
  await page.route("**/api/**", async (route) => {
    const url = new URL(route.request().url());
    let body: unknown = [];
    if (url.pathname === "/api/staff/me")
      body = {
        email: "admin@example.test",
        role: "admin",
        institution: "Synthetic Institute",
      };
    if (
      url.pathname === "/api/staff/leads" ||
      url.pathname === "/api/staff/leads/search"
    ) {
      if (url.pathname.endsWith("search")) {
        expect(url.search).toBe("");
        expect(route.request().method()).toBe("POST");
        bodies.push(route.request().postDataJSON());
      }
      body = [
        {
          id: "synthetic-inquiry",
          name: "Asha നായർ",
          status: "enrolled",
          course: "Synthetic course",
        },
      ];
    }
    if (url.pathname === "/api/staff/exports") {
      const request = route.request().postDataJSON();
      bodies.push(request);
      return route.fulfill({
        status: 200,
        contentType: "text/csv",
        body: "inquiry_id,name\nsynthetic,Asha\n",
      });
    }
    await route.fulfill({ json: body });
  });
  await page.goto("/");
  await page
    .getByRole("button", { name: "Admissions inquiries", exact: true })
    .click();
  await expect(page.getByRole("button", { name: /Asha നായർ/ })).toBeVisible();
  await page.getByLabel("Find an inquiry").fill("AS നായ");
  await page.getByRole("button", { name: "Search", exact: true }).click();
  await expect
    .poll(() => bodies.some((body) => body.query === "AS നായ"))
    .toBe(true);
  await page
    .getByRole("combobox", { name: "Status", exact: true })
    .selectOption("enrolled");
  await expect
    .poll(() => bodies.some((body) => body.status === "enrolled"))
    .toBe(true);
  expect(
    await page
      .getByRole("combobox", { name: "Status", exact: true })
      .locator("option")
      .count(),
  ).toBe(13);
  for (const width of [1440, 390]) {
    await page.setViewportSize({ width, height: 950 });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
    if (process.env.CAPTURE_UI === "1") {
      mkdirSync("playwright-report", { recursive: true });
      await page.screenshot({
        path: `playwright-report/crm-${width}.png`,
        fullPage: true,
      });
    }
  }
  await page.getByRole("button", { name: "Data exports", exact: true }).click();
  await expect(
    page.getByRole("heading", { name: "Data exports", exact: true }),
  ).toBeVisible();
  await page
    .getByRole("combobox", { name: "Records", exact: true })
    .selectOption("payments");
  const downloading = page.waitForEvent("download");
  await page.getByRole("button", { name: "Download records" }).click();
  expect((await downloading).suggestedFilename()).toBe(
    "admitflow-payments.csv",
  );
  expect(bodies.at(-1)).toMatchObject({
    dataset: "payments",
    format: "csv",
    query: "",
  });
  await expect(page.getByRole("status")).toContainText("Download prepared");
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
  if (process.env.CAPTURE_UI === "1")
    await page.screenshot({
      path: "playwright-report/exports-390.png",
      fullPage: true,
    });
});
