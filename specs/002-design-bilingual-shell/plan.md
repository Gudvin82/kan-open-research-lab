# Implementation Plan: Design System + Bilingual Public Shell

**Branch**: `codex/design-bilingual-shell` | **Date**: 2026-07-23 |
**Spec**: [spec.md](spec.md)

**Input**: Feature specification from
`/specs/002-design-bilingual-shell/spec.md`

## Summary

Build a server-rendered, progressively enhanced Django public shell with Russian
as the default and explicit `/ru/` and `/en/` URL spaces. The feature introduces
the approved warm-paper design tokens, shared header/navigation/footer,
localized primary pages, honest research-state cards and three explanation
levels. Curated demonstration content remains in version-controlled Python and
templates, so this stage adds neither publication models nor ML execution.

Route/semantic tests stay in pytest. A small pinned Playwright test project adds
browser, responsive and axe accessibility coverage. Vercel remains configuration
only until the owner separately approves project linking; its build performs
`collectstatic` only, Preview receives no Production database secret, and
production tracks protected `main`.

## Technical Context

**Language/Version**: Python 3.13; HTML5; CSS; minimal JavaScript only where
progressive enhancement materially improves navigation

**Primary Dependencies**: Django 6.0, WhiteNoise 6.x; development-only
Playwright Test and `@axe-core/playwright` with a pinned npm lockfile

**Storage**: No new persistent storage. Curated shell content is
version-controlled; existing PostgreSQL remains unused by public-shell routes.

**Testing**: pytest/pytest-django for route, locale, content and deployment
contracts; Playwright for keyboard, responsive and browser journeys; axe for
automatically detectable WCAG A/AA issues; manual accessibility checklist for
issues automation cannot detect

**Target Platform**: Modern evergreen browsers, keyboard and screen-reader
users, 320 px through large desktop widths; Django on local Docker and Vercel
Functions

**Project Type**: Server-rendered web application in the existing modular
Django monolith

**Performance Goals**: No page-level horizontal overflow at 320 px; core pages
usable without JavaScript or custom fonts; static-first rendering with no
database query requirement

**Constraints**: WCAG 2.2 AA target; RU source language; no machine translation
auto-publication; no ML libraries or worker calls; no automatic migrations; no
Preview access to Production DB; no Vercel/resource creation before approval

**Scale/Scope**: Five primary destinations in two locales, four method shells,
two research collections, three explanation levels and one shared shell

## Constitution Check

*GATE: Passed before Phase 0 and re-checked after Phase 1 design.*

| Principle | Plan evidence | Result |
|---|---|---|
| I. Scientific honesty | Separate reproduced/open collections, centralized text statuses and explicit open-problem disclaimer | PASS |
| II. Reproducibility | Cards expose reproducibility state; no experiment is published in this feature | PASS |
| III. Fair comparison | KAN, MLP, PINN and comparison shells use neutral summaries; no benchmark claims | PASS |
| IV. Sources and claim boundaries | RU is source, EN is reviewed, translation state is explicit; demonstration claims remain bounded | PASS |
| V. Execution safety | Public shell is read-only and performs no worker/ML execution | PASS |
| VI. Simplicity and resources | Existing Django monolith; no DB schema; one small browser-test toolchain justified by explicit UI/a11y acceptance | PASS |
| VII. Accessibility/bilingual web | Semantic HTML, no-JS core, locale-preserving links, keyboard and responsive tests | PASS |
| VIII. Spec-driven evidence | Spec, plan, checklist, tasks and analysis precede code; verification evidence is an acceptance task | PASS |

Post-design re-check: the contracts and content model introduce no database,
auth, publication-status mutation or worker boundary. Playwright/axe is the only
new dependency family and must pass license, lockfile and dependency-audit
review before adoption.

## Delivery Gates

1. This planning PR remains documentation-only and stops before implementation.
2. The owner resolves or accepts the listed open decisions.
3. Implementation begins only after the planning checkpoint is accepted.
4. A minimal real Preview must be reviewed before feature completion, but
   linking a Vercel project or creating any external/paid resource requires
   separate explicit approval.
5. Legacy database access, worker integration and production deploy to the
   research server remain blocked until the external credential is rotated.
   This does not block a database-free Vercel Preview/public shell that never
   receives or uses that credential.
6. Managed PostgreSQL is not connected in this feature. ADR-0003 must compare
   providers and be approved before a later database connection.

## Project Structure

### Documentation (this feature)

```text
specs/002-design-bilingual-shell/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── public-shell.md
├── checklists/
│   ├── requirements.md
│   └── ux-accessibility.md
└── tasks.md
```

### Planned source code (repository root)

```text
locale/
├── en/LC_MESSAGES/django.po
└── ru/LC_MESSAGES/django.po

src/
├── config/
│   ├── settings/base.py
│   └── urls.py
└── webapp/
    ├── apps.py
    ├── content.py
    ├── context_processors.py
    ├── urls.py
    ├── views.py
    ├── static/public/
    │   ├── css/site.css
    │   └── fonts/
    └── templates/lab/
        ├── base.html
        ├── partials/
        └── pages/

tests/
├── contract/
│   ├── test_public_routes.py
│   ├── test_locale_contract.py
│   └── test_vercel_config.py
├── integration/
│   └── test_public_content.py
└── ui/
    ├── accessibility.spec.ts
    ├── navigation.spec.ts
    └── responsive.spec.ts

package.json
package-lock.json
playwright.config.ts
```

**Structure Decision**: Add one `src.webapp` Django app inside the existing
monolith. Keep content, routes, templates and namespaced static assets together.
Do not create a frontend application, API, database models or worker coupling.
The Node project exists only under development/CI for browser verification.

## Complexity Tracking

No constitutional violation requires an exception. The owner approved the
pinned browser-test toolchain as development/CI-only surface; it must not ship
in the Python container or Vercel runtime.
