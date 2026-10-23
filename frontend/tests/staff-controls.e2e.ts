import { expect, test } from "@playwright/test";

test("staff reviews drafts and retries a manual send with the same reference", async ({
  page,
}) => {
  const leadId = "8c22128b-b325-4e30-b6d7-2a991e31f005";
  let active = false;
  let draft:
    | { id: string; text: string; evidence: string; status: string }
    | undefined;
  let approvals = 0;
  const requests: string[] = [];
  const sent = new Set<string>();
  await page.route("**/api/**", async (route) => {
    const path = new URL(route.request().url()).pathname;
    let result: unknown = [];
    if (path === "/api/staff/me")
      result = {
        email: "staff@example.test",
        role: "agent",
        institution: "Synthetic Institute",
      };
    if (path === "/api/staff/leads")
      result = [
        {
          id: leadId,
          status: active ? "handed_off" : "qualifying",
          course: "Synthetic course",
          course_id: null,
        },
      ];
    if (path === `/api/staff/leads/${leadId}`)
      result = {
        id: leadId,
        status: active ? "handed_off" : "qualifying",
        copilot_mode: active,
        draft_stale: false,
        course_id: null,
        batch_id: null,
        batch_name: null,
        memory: { facts: { age: 20 }, staff_draft: draft },
        older_cursor: null,
        messages: [
          {
            message_id: "student:1",
            event_id: leadId,
            direction: "inbound",
            kind: "student",
            text: "Can you help with course choices?",
            status: "done",
            created_at: "2026-10-24T01:00:00+05:30",
          },
        ],
      };
    if (path.endsWith("/takeover")) {
      active = true;
      result = { copilot_mode: true };
    }
    if (path.endsWith("/resume")) {
      active = false;
      result = { copilot_mode: false };
    }
    if (path.endsWith("/draft")) {
      const body = route.request().postDataJSON();
      draft = {
        id: body.request_id,
        text: "I can help you compare the available courses.",
        evidence: "No relevant policy was found. Ask a clarifying question.",
        status: "pending",
      };
      result = draft;
    }
    if (draft && path.endsWith(`/draft/${draft.id}`)) {
      const body = route.request().postDataJSON();
      if (body.decision === "approve") {
        expect(body.reviewed).toBe(true);
        approvals++;
        draft.status = "edited";
      } else draft.status = "ignored";
      result = { id: "draft-delivery", status: draft.status };
    }
    if (path.endsWith("/messages")) {
      const body = route.request().postDataJSON();
      requests.push(body.request_id);
      sent.add(body.request_id);
      if (requests.length === 1) {
        await route.fulfill({
          status: 503,
          json: {
            detail: "Connection interrupted. Check the conversation and retry.",
          },
        });
        return;
      }
      result = { id: "manual-delivery", status: "queued" };
    }
    await route.fulfill({ json: result });
  });
  await page.goto("/");
  await page
    .getByRole("button", { name: "Admissions inquiries", exact: true })
    .click();
  await page.locator(".inquiry-row").first().click();
  await page.getByRole("button", { name: "Take over", exact: true }).click();
  expect(active).toBe(false);
  await page.getByRole("button", { name: "Confirm", exact: true }).click();
  await expect(
    page.getByText("Bot replies paused", { exact: true }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Generate co-pilot draft", exact: true })
    .click();
  await expect(page.getByLabel("Review or edit draft")).toHaveValue(
    "I can help you compare the available courses.",
  );
  await expect(
    page.getByRole("button", { name: "Approve reply", exact: true }),
  ).toBeDisabled();
  expect(approvals).toBe(0);
  await page
    .getByLabel("Review or edit draft")
    .fill("Which course would you like to discuss?");
  await page
    .getByRole("checkbox", {
      name: "I reviewed the wording, facts and sources.",
    })
    .check();
  for (const width of [1440, 390]) {
    await page.setViewportSize({ width, height: 1000 });
    await page.evaluate(() => window.scrollTo(0, 0));
    await expect(page.locator("body")).toHaveJSProperty("scrollWidth", width);
    if (process.env.CAPTURE_UI === "1")
      await page.screenshot({
        path: `test-results/staff-controls-${width}.png`,
        fullPage: true,
      });
  }
  await page
    .getByRole("button", { name: "Approve reply", exact: true })
    .click();
  expect(approvals).toBe(0);
  await page.getByRole("button", { name: "Confirm", exact: true }).click();
  await expect.poll(() => approvals).toBe(1);
  await page
    .getByLabel("Staff reply", { exact: true })
    .fill("Here is my follow-up staff reply.");
  await page
    .getByRole("button", { name: "Send staff reply", exact: true })
    .click();
  await page.getByRole("button", { name: "Confirm", exact: true }).click();
  await expect(
    page
      .getByRole("region", { name: "Staff conversation controls" })
      .getByRole("alert"),
  ).toContainText("Connection interrupted");
  await page.getByRole("button", { name: "Confirm", exact: true }).click();
  await expect.poll(() => requests.length).toBe(2);
  expect(requests[0]).toBe(requests[1]);
  expect(sent.size).toBe(1);
  await expect(page.getByLabel("Staff reply", { exact: true })).toHaveValue("");
  await page.getByRole("button", { name: "Resume AI", exact: true }).click();
  await page.getByRole("button", { name: "Confirm", exact: true }).click();
  await expect(
    page.getByRole("button", { name: "Take over", exact: true }),
  ).toBeVisible();
});
