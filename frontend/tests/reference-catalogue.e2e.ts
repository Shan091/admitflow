import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { expect, test } from "@playwright/test";

test("published programmes do not display an invented zero fee", async ({ page, context }) => {
  const credentials = JSON.parse(readFileSync(resolve("../backend/.demo-credentials.json"), "utf8"));
  const login = await context.request.post("/api/staff/login", {
    data: credentials, headers: { "X-AdmitFlow-Request": "1" },
  });
  expect(login.ok()).toBe(true);
  const response = await context.request.get("/api/staff/catalog");
  const catalogue = await response.json();
  const reference = catalogue.find((course: { is_reference?: boolean }) => course.is_reference);
  expect(reference).toBeTruthy();
  expect(reference.batches).toHaveLength(0);
  await page.goto("/");
  await page.getByRole("button", { name: "Institution management", exact: true }).click();
  await page.getByRole("button", { name: reference.name, exact: false }).click();
  await expect(page.getByText("Published programme for exploration.", { exact: false })).toBeVisible();
  const fee = page.getByLabel("Application fee (INR)", { exact: true });
  await expect(fee).toBeDisabled();
  await expect(fee).toHaveValue("");
  await expect(fee).toHaveAttribute("placeholder", "Unverified");
  for (const width of [1440, 390]) {
    await page.setViewportSize({ width, height: 1000 });
    await fee.scrollIntoViewIfNeeded();
    expect(await page.locator("body").evaluate((body) => body.scrollWidth)).toBeLessThanOrEqual(width);
    if (process.env.CAPTURE_UI === "1") await page.locator(".management-form").screenshot({
      path: `test-results/reference-programme-${width}.png`,
    });
  }
});
