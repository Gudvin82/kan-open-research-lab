import { expect, test } from "@playwright/test";

const pages = [
  ["", ""],
  ["research/", "research/"],
  ["methods/", "methods/"],
  ["knowledge/", "knowledge/"],
  ["about/", "about/"],
] as const;

for (const [russianPath, englishPath] of pages) {
  test(`language switch preserves ${russianPath || "home"}`, async ({
    page,
  }) => {
    await page.context().setExtraHTTPHeaders({ "Accept-Language": "en" });
    await page.goto(`/ru/${russianPath}`);
    await page
      .getByRole("banner")
      .getByRole("link", { name: "English" })
      .click();
    await expect(page).toHaveURL(new RegExp(`/en/${englishPath}$`));
    await expect(page.locator("html")).toHaveAttribute("lang", "en");
  });
}

test("core navigation and explanation levels work without JavaScript", async ({
  browser,
}) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();

  await page.goto("/ru/methods/kan/");
  await page.getByRole("link", { name: "Технически" }).click();
  await expect(page).toHaveURL(/#technical$/);
  await expect(page.locator("#technical")).toBeVisible();
  await page
    .getByRole("navigation", { name: "Основная навигация" })
    .getByRole("link", { name: "Исследования", exact: true })
    .click();
  await expect(page).toHaveURL(/\/ru\/research\/$/);
  await context.close();
});

test("keyboard route exposes skip link and visible focus", async ({ page }) => {
  await page.goto("/ru/");
  await page.keyboard.press("Tab");
  const skipLink = page.getByRole("link", { name: "Перейти к содержанию" });
  await expect(skipLink).toBeFocused();
  await expect(skipLink).toHaveCSS("visibility", "visible");
  await skipLink.press("Enter");
  await expect(page.locator("#main-content")).toBeFocused();
});
