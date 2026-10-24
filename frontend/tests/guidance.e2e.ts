import { expect, test } from "@playwright/test";

for (const recorded of [true, false]) {
  test(`staff guidance evidence is readable with recorded=${recorded}`, async ({ page }) => {
    const id = "8c22128b-b325-4e30-b6d7-2a991e31f005";
    await page.route("**/api/**", async (route) => {
      const path = new URL(route.request().url()).pathname;
      let result: unknown = [];
      if (path === "/api/staff/me") result = {
        email: "staff@example.test", role: "agent", institution: "Synthetic Institute",
      };
      if (path === "/api/staff/leads") result = [{
        id, status: "discovering", course: null,
      }];
      if (path === `/api/staff/leads/${id}`) result = {
        id, status: "discovering", copilot_mode: false, draft_stale: false,
        course_id: null, batch_id: null, batch_name: null, messages: [], older_cursor: null,
        memory: { facts: {}, guidance: {
          stage: "comparing", deeper: true,
          notes: recorded ? [
            { topic: "interest", evidence: "I enjoy illustrating stories and making short videos." },
            { topic: "background", evidence: "I finished Class 12 and helped with our school magazine." },
            { topic: "constraint", evidence: "I prefer an evening option and cannot relocate." },
          ] : [],
          themes: recorded ? [{ theme: "creative", evidence: "I enjoy illustrating stories" }] : [],
        } },
      };
      await route.fulfill({ json: result });
    });
    await page.goto("/");
    await page.getByRole("button", { name: "Admissions inquiries", exact: true }).click();
    await page.locator(".inquiry-row").first().click();
    const profile = page.getByRole("region", { name: "Course guidance", exact: true });
    await expect(profile).toContainText("Comparing options");
    await expect(profile).toContainText("not an aptitude test or an eligibility decision");
    if (recorded) {
      await expect(profile).toContainText("I prefer an evening option and cannot relocate.");
      await profile.getByText("View tentative interest themes", { exact: true }).click();
      await expect(profile).toContainText("creative: I enjoy illustrating stories");
    } else {
      await expect(profile).toContainText("No interests or background have been recorded yet.");
      await expect(profile.locator("details")).toHaveCount(0);
    }
    for (const width of [1440, 390]) {
      await page.setViewportSize({ width, height: 1000 });
      await profile.scrollIntoViewIfNeeded();
      await expect(page.locator("body")).toHaveJSProperty("scrollWidth", width);
      if (recorded && process.env.CAPTURE_UI === "1") await page.screenshot({
        path: `test-results/guidance-${width}.png`, fullPage: true,
      });
    }
  });
}
