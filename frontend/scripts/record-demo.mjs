// Records actual local staff behavior using synthetic data. No credentials enter the video.
import { chromium } from "@playwright/test";
import { readFile, mkdir, stat } from "node:fs/promises";
import { resolve } from "node:path";

const journey = process.argv.includes("--journey");
const outputName = journey ? "student-to-staff-walkthrough.webm" : "staff-walkthrough.webm";
const target = resolve(`../docs/event/artifacts/${outputName}`);
try {
  await stat(target);
  throw new Error(
    "Recording exists; choose a new output before recording again.",
  );
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}
await mkdir(resolve("../docs/event/artifacts"), { recursive: true });
const credentials = JSON.parse(
  await readFile(resolve("../backend/.demo-credentials.json"), "utf8"),
);
const browser = await chromium.launch({ channel: "chrome", headless: true });
const context = await browser.newContext({
  viewport: { width: 1440, height: 1000 },
  recordVideo: {
    dir: resolve("test-results/recording"),
    size: { width: 1440, height: 1000 },
  },
});
const headers = { "X-AdmitFlow-Request": "1" };
try {
  const login = await context.request.post(
    "http://127.0.0.1:3000/api/staff/login",
    { data: credentials, headers },
  );
  if (!login.ok()) throw new Error("Demo sign-in failed");
  const page = await context.newPage();
  const video = page.video();
  await page.goto("http://127.0.0.1:3000");
  await page
    .getByRole("heading", { name: "Knowledge library", exact: true })
    .waitFor();
  await page
    .getByRole("row")
    .filter({ hasText: "synthetic-campus-reference.txt" })
    .getByText("Ready", { exact: true })
    .waitFor();
  await page.waitForTimeout(3500);
  if (!journey) {
    await page
      .getByLabel("Search institution knowledge")
      .fill("Where is the demo campus?");
    await page.getByRole("button", { name: "Search knowledge" }).click();
    await page.locator(".result").filter({ hasText: "Kochi" }).waitFor();
    await page.locator(".search-section").scrollIntoViewIfNeeded();
    await page.waitForTimeout(4500);
  }
  await page
    .getByRole("button", { name: "Admissions inquiries", exact: true })
    .click();
  await page.locator(".inquiry-row").first().waitFor();
  await page.locator(".inquiry-row").first().click();
  await page
    .getByRole("heading", { name: "Conversation", exact: true })
    .waitFor();
  await page.locator(".inquiry-facts").scrollIntoViewIfNeeded();
  await page.waitForTimeout(4500);
  await page.getByText("View rule evidence", { exact: true }).click();
  await page.waitForTimeout(4000);
  await page.locator(".conversation-heading").scrollIntoViewIfNeeded();
  await page.waitForTimeout(4000);
  await page.locator(".message").last().scrollIntoViewIfNeeded();
  await page.waitForTimeout(4500);
  if (journey) {
    for (const text of [
      "Selected course:",
      "Selected batch:",
      "Actually my age is 17",
      "Actually my age is 21",
      "Source: synthetic-campus-reference.txt",
      "could not find a supporting passage",
      "Automated qualification is paused",
    ]) {
      await page.locator(".message").filter({ hasText: text }).first().scrollIntoViewIfNeeded();
      await page.waitForTimeout(4000);
    }
  }
  await page
    .getByRole("button", { name: "Staff requests", exact: true })
    .click();
  await page
    .getByRole("heading", { name: "Staff requests", exact: true })
    .waitFor();
  await page.waitForTimeout(3500);
  if (journey) {
    await page.locator(".human-row").filter({ hasText: "resumed" }).first().waitFor();
    await page.locator(".human-row").first().scrollIntoViewIfNeeded();
    await page.waitForTimeout(4000);
  }
  await page.getByRole("button", { name: "Sign out", exact: true }).click();
  await page.getByRole("heading", { name: "Welcome back" }).waitFor();
  await context.close();
  await video.saveAs(target);
  console.log(
    `Recorded actual local staff workflow to docs/event/artifacts/${outputName}`,
  );
} finally {
  await context.close();
  await browser.close();
}
