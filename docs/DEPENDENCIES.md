# Dependency register

## Browser verification only

These packages are development/CI dependencies. They are not copied into the
production Python image and are excluded from the Vercel source bundle.

| Package | Pinned version | License | Source | Purpose |
|---|---:|---|---|---|
| `@playwright/test` | 1.61.1 | Apache-2.0 | <https://github.com/microsoft/playwright> | Chromium navigation, keyboard and responsive checks |
| `@axe-core/playwright` | 4.12.1 | MPL-2.0 | <https://github.com/dequelabs/axe-core-npm> | Automatically detectable accessibility checks |

Review performed 2026-07-23:

- versions, licenses and repository origins confirmed from npm metadata;
- packages are pinned by `package-lock.json`;
- `npm audit` is required locally and in CI;
- Chromium is installed only in the UI-test CI job;
- automated axe checks supplement rather than replace manual accessibility
  review.

## Golos Text

The public shell uses one locally hosted variable WOFF2 family derived from the
official `googlefonts/golos-text` source. The upstream project identifies
Alexandra Korolkova and Vitaly Kuzmin as designers, Paratype as the 2019
releaser, and licenses the font under SIL Open Font License 1.1.

The exact source revision, conversion command, file size and checksum are
recorded beside the font in `src/public/static/public/fonts/README.md`.
