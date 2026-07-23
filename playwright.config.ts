import { defineConfig, devices } from "@playwright/test";

const baseURL = process.env.PLAYWRIGHT_BASE_URL ?? "http://127.0.0.1:8001";

export default defineConfig({
  testDir: "./tests/ui",
  outputDir: "artifacts/playwright/test-results",
  reporter: [
    ["line"],
    ["html", { outputFolder: "artifacts/playwright/report", open: "never" }],
  ],
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 2 : undefined,
  use: {
    baseURL,
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
    video: "off",
  },
  webServer: process.env.PLAYWRIGHT_EXTERNAL_SERVER
    ? undefined
    : {
        command:
          "uv run python manage.py runserver 127.0.0.1:8001 --noreload",
        url: `${baseURL}/health/live/`,
        reuseExistingServer: !process.env.CI,
        timeout: 120_000,
      },
  projects: [
    {
      name: "chromium",
      use: {
        ...devices["Desktop Chrome"],
        colorScheme: "light",
      },
    },
  ],
});
