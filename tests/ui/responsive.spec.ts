import { expect, test } from "@playwright/test";

const visualPages = [
  ["home", ""],
  ["research", "research/"],
  ["methods", "methods/"],
] as const;

for (const locale of ["ru", "en"]) {
  for (const width of [320, 1440]) {
    test(`${locale} pages fit ${width}px`, async ({ page }) => {
      await page.setViewportSize({ width, height: width === 320 ? 760 : 1000 });
      for (const [, path] of visualPages) {
        await page.goto(`/${locale}/${path}`);
        const overflow = await page.evaluate(
          () =>
            document.documentElement.scrollWidth -
            document.documentElement.clientWidth,
        );
        expect(overflow).toBeLessThanOrEqual(1);
      }
    });
  }
}

test("reduced motion disables non-essential transitions", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/ru/");

  const duration = await page
    .locator(".site-header")
    .evaluate((element) => getComputedStyle(element).transitionDuration);
  expect(duration).toBe("0s");
});

test("200 percent zoom keeps mobile content usable", async ({ page }) => {
  await page.setViewportSize({ width: 640, height: 900 });
  await page.goto("/en/research/");
  await page.evaluate(() => {
    document.documentElement.style.zoom = "2";
  });

  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  const overflow = await page.evaluate(
    () =>
      document.documentElement.scrollWidth -
      document.documentElement.clientWidth,
  );
  expect(overflow).toBeLessThanOrEqual(1);
});
