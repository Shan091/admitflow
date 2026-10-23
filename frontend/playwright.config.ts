import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",
  testMatch: "**/*.e2e.ts",
  workers: 1,
  timeout: 90000,
  retries: 0,
  reporter: "list",
  use: {
    baseURL: process.env.DEMO_BASE_URL || "http://127.0.0.1:3000",
    channel: "chrome",
    trace: "off",
    screenshot: "off",
  },
});
