import { expect, test } from "@playwright/test";
import { mkdirSync } from "node:fs";

test("administrator assigns document scope and searches course references", async ({ page }) => {
  const courseId = "ea0fd91e-375b-4af7-a064-8531c94f3730";
  const docId = "e11d68ab-6b46-45b2-a11b-99f019572906";
  let scope: string | null = null;
  let saved = false;
  let rejectScope = false;
  await page.route("**/api/**", async (route) => {
    const path = new URL(route.request().url()).pathname;
    let body: unknown = [];
    if (path === "/api/staff/me") body = {
      email: "admin@example.test", role: "admin", institution: "Synthetic Institute",
    };
    if (path === "/api/staff/catalog") body = [{ id: courseId, name: "Nursing", is_active: true }];
    if (path === "/api/knowledge/documents") body = [{
      id: docId, filename: "Nursing prospectus.pdf", relative_path: "Nursing prospectus.pdf",
      byte_size: 2048, status: "ready", error_code: null, chunk_count: 4, attempts: 1,
      course_id: scope,
    }];
    if (path.endsWith("/scope")) {
      expect(route.request().method()).toBe("PATCH");
      if (rejectScope) {
        await route.fulfill({ status: 409, json: { detail: "Course scope could not be saved." } });
        return;
      }
      scope = route.request().postDataJSON().course_id;
      saved = true;
      body = { status: "saved" };
    }
    if (path === "/api/knowledge/search") {
      expect(route.request().postDataJSON()).toEqual({ query: "Hostel?", course_id: courseId });
      body = { matches: [], message: "No supporting passage found." };
    }
    await route.fulfill({ json: body });
  });
  await page.goto("/");
  await page.getByRole("button", { name: "Knowledge library", exact: true }).click();
  const control = page.getByLabel("Course scope for Nursing prospectus.pdf", { exact: true });
  await expect(control).toBeEnabled();
  await control.selectOption(courseId);
  await expect.poll(() => saved).toBe(true);
  await expect(control).toHaveValue(courseId);
  await expect(page.getByText("Course scope updated for Nursing prospectus.pdf.", { exact: true })).toBeVisible();
  await page.getByLabel("Search course", { exact: true }).selectOption(courseId);
  await page.getByLabel("Search institution knowledge").fill("Hostel?");
  await page.getByRole("button", { name: "Search knowledge", exact: true }).click();
  await expect(page.getByText("No supporting passage found.", { exact: true })).toBeVisible();
  mkdirSync("playwright-report", { recursive: true });
  for (const width of [1440, 390]) {
    await page.setViewportSize({ width, height: 1000 });
    await control.scrollIntoViewIfNeeded();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.screenshot({ path: `playwright-report/knowledge-scope-${width}.png`, fullPage: true });
  }
  rejectScope = true;
  await control.selectOption("");
  await expect(page.getByText("Course scope could not be saved.", { exact: true })).toBeVisible();
  await expect(control).toHaveValue(courseId);
});
