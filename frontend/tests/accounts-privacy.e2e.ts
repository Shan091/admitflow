import { expect, test } from "@playwright/test";
import { mkdirSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { execFileSync } from "node:child_process";
import { randomBytes } from "node:crypto";

test("staff management and permanent deletion require explicit input", async ({
  page,
}) => {
  const leadId = "2f83de01-c97d-408c-aaf0-5f8ab5471f0e";
  let deleted = false;
  const users = [
    {
      id: "staff-new",
      email: "new@example.test",
      role: "agent",
      is_active: true,
      must_change_password: true,
      is_you: false,
    },
  ];
  await page.route("**/api/**", async (route) => {
    const path = new URL(route.request().url()).pathname;
    let body: unknown = [];
    if (path === "/api/staff/me")
      body = {
        email: "admin@example.test",
        role: "admin",
        institution: "Synthetic Institute",
        institution_code: "synthetic",
      };
    if (path === "/api/staff/users") {
      if (route.request().method() === "POST") {
        const input = route.request().postDataJSON();
        expect(input.email).toBe("new@example.test");
        expect(input.password).toBe("synthetic-initial-password");
        body = { id: "staff-new", status: "created" };
      } else body = users;
    }
    if (path === "/api/staff/leads")
      body = deleted
        ? []
        : [
            {
              id: leadId,
              name: "Synthetic privacy subject",
              status: "qualifying",
              course: null,
            },
          ];
    if (path === `/api/staff/leads/${leadId}`) {
      if (route.request().method() === "DELETE") {
        expect(route.request().postDataJSON()).toEqual({ confirm_id: leadId });
        deleted = true;
        body = { status: "deleted", receipt_id: "synthetic-receipt" };
      } else
        body = {
          id: leadId,
          status: "qualifying",
          copilot_mode: false,
          draft_stale: false,
          memory: {},
          course_id: null,
          batch_id: null,
          batch_name: null,
          messages: [],
          older_cursor: null,
        };
    }
    await route.fulfill({ json: body });
  });
  await page.goto("/");
  await page
    .getByRole("button", { name: "Institution management", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Staff accounts", exact: true })
    .click();
  await page.getByLabel("Staff email").fill("new@example.test");
  await page
    .getByLabel("Initial password", { exact: true })
    .fill("synthetic-initial-password");
  await page
    .getByRole("button", { name: "Create staff account", exact: true })
    .click();
  await expect(page.getByRole("status")).toContainText("Staff account created");
  await expect(
    page.getByLabel("Initial password", { exact: true }),
  ).toHaveValue("");
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
        path: `playwright-report/accounts-${width}.png`,
        fullPage: true,
      });
    }
  }
  await page
    .getByRole("button", { name: "Admissions inquiries", exact: true })
    .click();
  await page.getByRole("button", { name: /Synthetic privacy subject/ }).click();
  await page
    .getByRole("button", { name: "Delete inquiry data", exact: true })
    .click();
  const confirm = page.getByRole("button", {
    name: "Confirm permanent deletion",
    exact: true,
  });
  await expect(confirm).toBeDisabled();
  await page
    .getByLabel(`Enter ${leadId.slice(0, 8)} to confirm`)
    .fill(leadId.slice(0, 8));
  await expect(
    page.getByRole("region", {
      name: "Staff conversation controls",
      exact: true,
    }),
  ).toHaveCount(1);
  if (process.env.CAPTURE_UI === "1")
    await page.screenshot({
      path: "playwright-report/privacy-390.png",
      fullPage: true,
    });
  await confirm.click();
  await expect(page.getByRole("status")).toContainText("Inquiry data deleted");
  await expect(
    page.getByRole("heading", { name: "No inquiries yet", exact: true }),
  ).toBeVisible();
});

test("real staff setup blocks data, rotates credentials and revokes sessions", async ({
  page,
  request,
}) => {
  const credentials = JSON.parse(
    readFileSync(resolve("../backend/.demo-credentials.json"), "utf8"),
  );
  expect(
    (
      await request.post("/api/staff/login", {
        data: credentials,
        headers: { "X-AdmitFlow-Request": "1" },
      })
    ).ok(),
  ).toBe(true);
  const email = `browser-${randomBytes(6).toString("hex")}@example.test`;
  const initial = randomBytes(24).toString("base64url");
  const password = randomBytes(24).toString("base64url");
  const created = await request.post("/api/staff/users", {
    data: { email, password: initial, role: "agent" },
    headers: { "X-AdmitFlow-Request": "1" },
  });
  expect(created.ok()).toBe(true);
  const id = (await created.json()).id;
  let syntheticLead = "";
  try {
    await page.goto("/");
    await page.getByLabel("Institution code").fill(credentials.institution);
    await page.getByLabel("Work email").fill(email);
    await page.getByLabel("Password", { exact: true }).fill(initial);
    await page.getByRole("button", { name: "Sign in", exact: true }).click();
    await expect(
      page.getByRole("heading", {
        name: "Set your private password",
        exact: true,
      }),
    ).toBeVisible();
    await expect(
      page.getByRole("navigation", { name: "Workspace" }),
    ).toHaveCount(0);
    await page.setViewportSize({ width: 390, height: 950 });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
    ).toBe(true);
    if (process.env.CAPTURE_UI === "1") {
      mkdirSync("playwright-report", { recursive: true });
      await page.screenshot({
        path: "playwright-report/password-setup-390.png",
        fullPage: true,
      });
    }
    await page.getByLabel("Current password", { exact: true }).fill(initial);
    await page
      .getByLabel("New private password", { exact: true })
      .fill(password);
    await page
      .getByLabel("Confirm new password", { exact: true })
      .fill(password);
    await page
      .getByRole("button", { name: "Save private password", exact: true })
      .click();
    await expect(
      page.getByRole("navigation", { name: "Workspace" }),
    ).toBeVisible();
    expect(
      (
        await request.put(`/api/staff/users/${id}`, {
          data: { role: "agent", is_active: false },
          headers: { "X-AdmitFlow-Request": "1" },
        })
      ).ok(),
    ).toBe(true);
    await page.reload();
    await expect(
      page.getByRole("heading", { name: "Welcome back", exact: true }),
    ).toBeVisible();
    await page.context().addCookies((await request.storageState()).cookies);
    syntheticLead = execFileSync(
      "uv",
      [
        "run",
        "python",
        "-c",
        `import asyncio,json
from pathlib import Path
from sqlalchemy import select
from src.db.models import Institution,Lead
from src.db.session import get_sessionmaker
async def main():
 async with get_sessionmaker()() as db:
  code=json.loads(Path('.demo-credentials.json').read_text())['institution']
  tenant=await db.scalar(select(Institution.id).where(Institution.slug==code))
  lead=Lead(tenant_id=tenant)
  db.add(lead)
  await db.commit()
  print(lead.id)
asyncio.run(main())`,
      ],
      { cwd: resolve("../backend"), encoding: "utf8" },
    ).trim();
    expect(syntheticLead).toMatch(/^[0-9a-f-]{36}$/);
    await page.goto("/");
    await page
      .getByRole("button", { name: "Admissions inquiries", exact: true })
      .click();
    await page
      .getByRole("button", {
        name: new RegExp(`Inquiry ${syntheticLead.slice(0, 8)}`),
      })
      .click();
    await page
      .getByRole("button", { name: "Delete inquiry data", exact: true })
      .click();
    await page
      .getByLabel(`Enter ${syntheticLead.slice(0, 8)} to confirm`)
      .fill(syntheticLead.slice(0, 8));
    await page
      .getByRole("button", { name: "Confirm permanent deletion", exact: true })
      .click();
    await expect(page.getByRole("status")).toContainText(
      "Inquiry data deleted",
    );
    expect(
      (await request.get(`/api/staff/leads/${syntheticLead}`)).status(),
    ).toBe(404);
  } finally {
    execFileSync(
      "uv",
      [
        "run",
        "python",
        "-c",
        `import asyncio,sys,uuid
from sqlalchemy import delete
from src.db.models import StaffUser,Lead
from src.db.session import get_sessionmaker
async def main():
 async with get_sessionmaker()() as db:
  await db.execute(delete(StaffUser).where(StaffUser.id==uuid.UUID(sys.argv[1]),StaffUser.email==sys.argv[2]))
  if sys.argv[3]: await db.execute(delete(Lead).where(Lead.id==uuid.UUID(sys.argv[3])))
  await db.commit()
asyncio.run(main())`,
        id,
        email,
        syntheticLead,
      ],
      { cwd: resolve("../backend"), stdio: "pipe" },
    );
  }
});
