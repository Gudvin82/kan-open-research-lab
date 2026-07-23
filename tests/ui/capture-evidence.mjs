import { chromium } from "@playwright/test";
import { mkdir } from "node:fs/promises";

const baseURL =
  process.env.PLAYWRIGHT_BASE_URL ?? "http://127.0.0.1:8001";
const outputDir = "artifacts/ui-evidence";
const pages = [
  ["home", ""],
  ["research", "research/"],
  ["methods", "methods/"],
];
const viewports = {
  desktop: { width: 1440, height: 1000 },
  mobile: { width: 390, height: 844 },
};

await mkdir(outputDir, { recursive: true });
const browser = await chromium.launch();

try {
  for (const locale of ["ru", "en"]) {
    for (const [viewportName, viewport] of Object.entries(viewports)) {
      const page = await browser.newPage({ viewport });

      for (const [pageName, path] of pages) {
        await page.goto(`${baseURL}/${locale}/${path}`, {
          waitUntil: "networkidle",
        });
        await page.screenshot({
          path: `${outputDir}/${locale}-${pageName}-${viewportName}.png`,
          fullPage: true,
        });
      }

      await page.goto(`${baseURL}/${locale}/`, { waitUntil: "networkidle" });
      await page.locator(".skip-link").evaluate((element) => {
        element.setAttribute("data-evidence-visibility", element.style.visibility);
        element.style.visibility = "hidden";
      });
      await page.locator("footer").screenshot({
        path: `${outputDir}/${locale}-footer-${viewportName}.png`,
      });
      await page.close();
    }
  }
} finally {
  await browser.close();
}
