# Tasks: Design System + Bilingual Public Shell

**Input:** `spec.md`, `plan.md`, `research.md`, `data-model.md`,
`contracts/public-shell.md`

**Rule:** Tests for a story are written and observed failing before that story's
implementation. This file defines future work; no task is complete at the
planning checkpoint.

## Phase 1: Setup

- [ ] T001 Add pinned browser-test dependencies and scripts in `package.json` and `package-lock.json`
- [ ] T002 [P] Configure Chromium-only browser execution in `playwright.config.ts`
- [ ] T003 [P] Record Playwright and axe license/activity/security review in `docs/DEPENDENCIES.md`
- [ ] T004 Add Node lockfile audit and UI test jobs to `.github/workflows/quality.yml`

## Phase 2: Foundational — blocks all user stories

- [ ] T005 Write failing shared route, landmark and database-independence contracts in `tests/contract/test_public_routes.py`
- [ ] T006 Configure `src.public`, `LocaleMiddleware`, RU/EN settings, locale paths and context processors in `src/config/settings/base.py`
- [ ] T007 Configure `/` and locale-prefixed named routes in `src/config/urls.py` and `src/public/urls.py`
- [ ] T008 [P] Define immutable localized page, research, status, evidence, reproducibility, explanation and method fixtures in `src/public/content.py`
- [ ] T009 [P] Implement shared page metadata and same-entity locale mapping in `src/public/context_processors.py`
- [ ] T010 Create semantic base, skip link, header/navigation and footer templates in `src/public/templates/public/base.html` and `src/public/templates/public/partials/`
- [ ] T011 Translate approved design tokens and responsive primitives into `src/public/static/public/css/site.css`
- [ ] T012 [P] Verify Golos Text provenance, open-source license, Cyrillic/Latin coverage, required weights and size; vendor the approved variable WOFF2 and license in `src/public/static/public/fonts/` with a complete system fallback in `docs/DESIGN.md`
- [ ] T013 Create the Django public app skeleton in `src/public/apps.py`, `src/public/urls.py`, `src/public/views.py`, and `src/public/__init__.py`, then make the foundational contracts in `tests/contract/test_public_routes.py` pass

**Checkpoint:** Shared localized shell works without a database or worker.

## Phase 3: User Story 1 — bilingual navigation (P1)

**Goal:** All primary pages use stable RU/EN URLs and the language switch
preserves the current entity.

**Independent test:** Traverse every primary route, switch locale and continue
navigation with JavaScript disabled.

- [ ] T014 [P] [US1] Write failing locale, root-default, counterpart and unsupported-locale tests in `tests/contract/test_locale_contract.py`
- [ ] T015 [P] [US1] Write failing no-script bilingual browser journey in `tests/ui/navigation.spec.ts`
- [ ] T016 [US1] Implement localized home, Research, Methods, Knowledge Base and About views in `src/public/views.py`
- [ ] T017 [US1] Implement localized primary templates in `src/public/templates/public/pages/`
- [ ] T018 [US1] Implement same-entity RU/EN controls and optional non-overriding language preference in `src/public/templates/public/partials/language_switch.html` and `src/public/views.py`
- [ ] T019 [US1] Add `lang`, canonical, `hreflang`, localized title and description output in `src/public/templates/public/base.html`
- [ ] T020 [US1] Make `tests/contract/test_locale_contract.py` and the US1 browser journey pass

**Checkpoint:** User Story 1 is independently usable in both locales.

## Phase 4: User Story 2 — honest research separation (P1)

**Goal:** Readers can distinguish reproduced known solutions from open problems
and inspect status/evidence/reproducibility as text.

**Independent test:** Classify all demonstration cards using headings and text
with styles disabled.

- [ ] T021 [P] [US2] Write failing research collection, disclaimer and card-field tests in `tests/integration/test_public_content.py`
- [ ] T022 [P] [US2] Write failing accessible-name research checks in `tests/ui/accessibility.spec.ts`
- [ ] T023 [US2] Add reviewed RU/EN demonstration research fixtures to `src/public/content.py`
- [ ] T024 [US2] Implement separate research collections and open-problem disclaimer in `src/public/templates/public/pages/research.html`
- [ ] T025 [US2] Implement text-complete research cards and status explanations in `src/public/templates/public/partials/research_card.html`
- [ ] T026 [US2] Make research content and accessible-name tests pass without claim-language exceptions

**Checkpoint:** User Story 2 passes with CSS disabled and color removed.

## Phase 5: User Story 3 — explanation depth (P2)

**Goal:** Human, Technical and Scientific explanations preserve topic identity
and expose unavailable states.

**Independent test:** Follow every level as an ordinary link with JavaScript
disabled and confirm stable topic/section identity.

- [ ] T027 [P] [US3] Write failing level completeness, unavailable-state and stable-anchor tests in `tests/integration/test_public_content.py`
- [ ] T028 [P] [US3] Write failing no-script and keyboard level journey in `tests/ui/navigation.spec.ts`
- [ ] T029 [US3] Implement explanation-level fixtures and validation in `src/public/content.py`
- [ ] T030 [US3] Implement link-based level navigation and explicit availability in `src/public/templates/public/partials/explanation_levels.html`
- [ ] T031 [US3] Make explanation integration and browser tests pass

**Checkpoint:** User Story 3 works with zero client-side scripting.

## Phase 6: User Story 4 — methods and project context (P2)

**Goal:** Useful neutral shells exist for KAN, MLP, PINN, comparisons and all
primary project destinations.

**Independent test:** Traverse header/footer and method routes in both locales;
every route has useful bounded copy or an honest empty state.

- [ ] T032 [P] [US4] Write failing method-route and neutral-copy tests in `tests/contract/test_public_routes.py`
- [ ] T033 [P] [US4] Write failing header/footer link coverage in `tests/ui/navigation.spec.ts`
- [ ] T034 [US4] Add reviewed neutral KAN, MLP, PINN and comparison summaries to `src/public/content.py`
- [ ] T035 [US4] Implement method index/detail and useful empty-state templates in `src/public/templates/public/pages/methods.html` and `src/public/templates/public/pages/method_detail.html`
- [ ] T036 [US4] Complete mission, grouped navigation, GitHub, language and disclaimer footer content in `src/public/templates/public/partials/footer.html`
- [ ] T037 [US4] Make method and navigation coverage pass in RU and EN and assert that unapproved contact, legal, cookie and analytics links are absent

**Checkpoint:** User Story 4 establishes the complete public information shell.

## Phase 7: User Story 5 — accessibility and responsive behavior (P2)

**Goal:** Primary journeys preserve meaning and operability across abilities and
target widths.

**Independent test:** Complete the primary journey at 320 px and desktop with
keyboard only, reduced motion and automated WCAG scans.

- [ ] T038 [P] [US5] Write failing axe scans for five RU and five EN primary pages in `tests/ui/accessibility.spec.ts`
- [ ] T039 [P] [US5] Write failing 320 px overflow, long-label and desktop checks in `tests/ui/responsive.spec.ts`
- [ ] T040 [US5] Refine landmarks, focus, touch targets, contrast, high-contrast and reduced-motion CSS in `src/public/templates/public/` and `src/public/static/public/css/site.css`
- [ ] T041 [US5] Make axe scans pass with no critical/serious violations and without broad rule exclusions
- [ ] T042 [US5] Make responsive journeys pass without page-level horizontal overflow
- [ ] T043 [US5] Complete manual keyboard, 200% zoom, screen-reader landmarks, forced-colors and reduced-motion review in `specs/002-design-bilingual-shell/checklists/ux-accessibility.md`

**Checkpoint:** User Story 5 has automated and manual evidence.

## Phase 8: Deployment safety and acceptance

- [ ] T044 [P] Expand no-migration, no-worker and Preview environment contracts in `tests/contract/test_vercel_config.py`
- [ ] T045 [P] Draft managed PostgreSQL comparison in `docs/adr/0003-managed-postgresql-options.md` without selecting or provisioning a provider
- [ ] T046 Confirm the server still reports `compute_node_unavailable` publicly and perform no worker integration in `tests/contract/test_compute_status.py`
- [ ] T047 Run Ruff, mypy, pytest, Django checks, npm audit and Playwright checks from `specs/002-design-bilingual-shell/quickstart.md`
- [ ] T048 Capture RU/EN desktop/mobile visual review and scientific-copy review evidence in `docs/VERIFICATION.md`
- [ ] T049 Obtain separate owner approval before linking Vercel or creating any external/paid resource
- [ ] T050 After T049 only, configure Vercel `main` as Production, isolate Preview variables, perform a real minimal PR Preview and record immutable URL/SHA evidence in `docs/VERIFICATION.md`
- [ ] T051 Run Spec Kit analysis/convergence and resolve every blocking finding before marking the implementation PR ready

## Dependencies and execution order

- Phase 1 precedes Phase 2; Phase 2 blocks every user story.
- US1 and US2 are the P1 slice. Both can start after Phase 2 but share content and
  templates, so the default execution order is US1 then US2.
- US3 depends on the method/page shell from US1; US4 consumes the explanation
  component from US3.
- US5 validates the combined shell and follows US1–US4.
- T049 is an explicit authority gate. T050 cannot start without it.
- The current implementation authorization stops after T048; T049–T050 remain
  intentionally unstarted.
- No task connects PostgreSQL, changes the server or integrates the ML worker.

## Parallel opportunities

- T002 and T003 use independent files.
- T008, T009 and T012 can proceed beside shared template work after routes are
  fixed.
- Test-authoring tasks marked `[P]` target separate files and precede their
  implementation.
- T044 and T045 are independent documentation/contract work.

## Implementation strategy

Deliver the smallest independently useful slice as Foundation + US1 + US2:
bilingual navigation with the scientific-honesty boundary. Then add explanation
levels, method/project context and accessibility convergence. Keep the public
runtime database-free throughout this feature. Stop again for explicit owner
approval before any real Vercel project linkage.
