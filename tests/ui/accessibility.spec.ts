import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";

const primaryPages = ["", "research/", "methods/", "knowledge/", "about/"];

for (const locale of ["ru", "en"]) {
  for (const path of primaryPages) {
    test(`${locale}/${path || "home"} has no serious axe violations`, async ({
      page,
    }) => {
      await page.goto(`/${locale}/${path}`);
      const results = await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"])
        .analyze();
      const blocking = results.violations.filter(({ impact }) =>
        ["critical", "serious"].includes(impact ?? ""),
      );

      expect(blocking).toEqual([]);
    });
  }
}

test("research status remains explicit in forced colors", async ({ page }) => {
  await page.emulateMedia({ forcedColors: "active" });
  await page.goto("/ru/research/");

  const cards = page.locator("[data-research-card]");
  await expect(cards).not.toHaveCount(0);
  for (const card of await cards.all()) {
    await expect(card.locator('[data-field="scientific-status"]')).toBeVisible();
    await expect(card.locator('[data-field="evidence-level"]')).toBeVisible();
    await expect(card.locator('[data-field="reproducibility"]')).toBeVisible();
  }
});
