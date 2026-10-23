import { expect, test } from "@playwright/test";
import { mkdirSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { execFileSync } from "node:child_process";

test("administrator configures webhooks and reads live notifications", async ({
  page,
}) => {
  let configured = false;
  let enabled = false;
  const items = ["qualified", "delivery", "draft", "payment"].map(
    (kind, index) => ({
      id: `event-${index}`,
      kind,
      lead_id: null,
      created_at: "2026-10-24T00:00:00Z",
      unread: true,
    }),
  );
  await page.routeWebSocket("**/api/staff/notifications/ws", (socket) => {
    const update = () =>
      socket.send(
        JSON.stringify({
          unread_count: items.filter((item) => item.unread).length,
          items,
        }),
      );
    update();
    socket.onMessage((raw) => {
      const body = JSON.parse(String(raw));
      expect(body.action).toBe("acknowledge");
      for (const item of items)
        if (body.ids.includes(item.id)) item.unread = false;
      update();
    });
  });
  await page.route("**/api/**", async (route) => {
    const path = new URL(route.request().url()).pathname;
    let body: unknown = [];
    if (path === "/api/staff/me")
      body = {
        email: "admin@example.test",
        role: "admin",
        institution: "Synthetic Institute",
      };
    if (path === "/api/staff/notifications")
      body = {
        unread_count: items.filter((item) => item.unread).length,
        items,
      };
    if (path === "/api/staff/integrations") {
      if (route.request().method() === "PUT") {
        const input = route.request().postDataJSON();
        expect(input.url).toBe("https://hooks.example.test/events");
        expect(input.enabled).toBe(true);
        configured = true;
        enabled = true;
        body = {
          status: "saved",
          signing_secret: "synthetic-signing-secret-shown-once",
        };
      } else
        body = {
          configured,
          enabled,
          host: configured ? "hooks.example.test" : null,
          counts: { dead: 1 },
          deliveries: [
            {
              id: "synthetic-delivery",
              event_id: "synthetic-event",
              status: "dead",
              attempts: 6,
              error_code: "http_503",
              created_at: "2026-10-24T00:00:00Z",
            },
          ],
        };
    }
    await route.fulfill({ json: body });
  });
  await page.goto("/");
  await page
    .getByRole("button", { name: "Outbound webhooks", exact: true })
    .click();
  await page
    .getByLabel("Destination URL")
    .fill("https://hooks.example.test/events");
  await page.getByLabel("Enable event delivery").check();
  await page.getByRole("button", { name: "Save webhook", exact: true }).click();
  await expect(page.getByLabel("Signing secret", { exact: true })).toHaveValue(
    "synthetic-signing-secret-shown-once",
  );
  await expect(
    page.getByRole("heading", { name: "Destination: hooks.example.test" }),
  ).toBeVisible();
  await expect(page.getByText("dead · 6 attempts · http 503")).toBeVisible();
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
        path: `playwright-report/integrations-${width}.png`,
        fullPage: true,
      });
    }
  }
  await page
    .getByRole("button", { name: "Notifications (4 unread)", exact: true })
    .click();
  const panel = page.getByRole("region", {
    name: "Notifications",
    exact: true,
  });
  for (const label of [
    "New eligible inquiry",
    "Message delivery needs attention",
    "Co-pilot draft ready",
    "Payment received",
  ])
    await expect(panel.getByText(label, { exact: true })).toBeVisible();
  await expect(panel.getByText(/Live updates connected/)).toBeVisible();
  if (process.env.CAPTURE_UI === "1")
    await page.screenshot({
      path: "playwright-report/notifications-390.png",
      fullPage: true,
    });
  await panel.getByRole("button", { name: "Mark shown as read" }).click();
  await expect(
    page.getByRole("button", { name: "Notifications (0 unread)", exact: true }),
  ).toBeVisible();
});

test("actual authenticated WebSocket receives a committed synthetic eligibility event", async ({
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
  const python = (source: string, args: string[] = []) =>
    execFileSync("uv", ["run", "python", "-c", source, ...args], {
      cwd: resolve("../backend"),
      encoding: "utf8",
    }).trim();
  let lead = "";
  try {
    await page.goto("/");
    await page.getByRole("button", { name: /^Notifications \(/ }).click();
    const panel = page.getByRole("region", {
      name: "Notifications",
      exact: true,
    });
    await expect(panel.getByText(/Live updates connected/)).toBeVisible();
    lead = python(`import asyncio,json
from pathlib import Path
from sqlalchemy import select
from src.db.models import Lead,Institution,WebhookEndpoint
from src.db.session import get_sessionmaker
from src.db.enums import LeadStatus
import src.db.audit
async def main():
 async with get_sessionmaker()() as db:
  slug=json.loads(Path('.demo-credentials.json').read_text())['institution']
  tenant=await db.scalar(select(Institution.id).where(Institution.slug==slug))
  assert not await db.scalar(select(WebhookEndpoint.id).where(WebhookEndpoint.tenant_id==tenant,WebhookEndpoint.enabled.is_(True))), 'Synthetic live check requires no external webhook'
  lead=Lead(tenant_id=tenant)
  db.add(lead)
  await db.commit()
  lead.status=LeadStatus.ADMISSION_READY
  await db.commit()
  print(lead.id)
asyncio.run(main())`);
    expect(lead).toMatch(/^[0-9a-f-]{36}$/);
    await expect(
      panel.getByText("New eligible inquiry", { exact: true }).first(),
    ).toBeVisible({ timeout: 10000 });
    await panel.getByRole("button", { name: "Mark shown as read" }).click();
    await expect(
      page.getByRole("button", {
        name: "Notifications (0 unread)",
        exact: true,
      }),
    ).toBeVisible();
  } finally {
    if (lead)
      python(
        `import asyncio,sys,uuid
from sqlalchemy import delete
from src.db.models import Lead
from src.db.session import get_sessionmaker
async def main():
 async with get_sessionmaker()() as db:
  await db.execute(delete(Lead).where(Lead.id==uuid.UUID(sys.argv[1])))
  await db.commit()
asyncio.run(main())`,
        [lead],
      );
  }
});
