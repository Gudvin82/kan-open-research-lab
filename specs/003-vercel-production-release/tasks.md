# Tasks: Vercel Production Release

**Input:** `spec.md`, `plan.md`, `preflight.md`, `rollback.md`,
`checklists/production-release.md`

**Authority gate:** These tasks are a future execution plan. Production
environment mutation, secret creation, deployment, promotion and containment
remain forbidden until the owner gives a separate Production authorization.

## Phase 1: Setup and revalidation

- [ ] T001 Re-read current Vercel CLI deploy, promote and alias capabilities
  and update `specs/003-vercel-production-release/preflight.md`
- [ ] T002 Re-resolve the team plan, project identity, Git-link state and exact
  stable domain in `specs/003-vercel-production-release/preflight.md`
- [ ] T003 Confirm the stable alias can be removed/restored without deleting
  deployment evidence and record the result in
  `specs/003-vercel-production-release/preflight.md`
- [ ] T004 Reconcile every preflight result with
  `specs/003-vercel-production-release/checklists/production-release.md`

## Phase 2: Foundational release contracts

- [x] T005 [P] Add exact validated Vercel Production hosts, stable canonical
  base selection and fail-closed `noindex, nofollow` settings in
  `src/config/settings/production.py` and `src/config/public_urls.py`
- [x] T006 [P] Replace Preview-specific robots handling with deny-by-default
  Preview/Production indexing behavior in
  `src/webapp/middleware.py`
- [x] T007 [P] Extend Production environment-isolation and migration-free
  contracts in `tests/contract/test_vercel_config.py`
- [x] T008 [P] Add Production settings tests for secret, hosts, `DEBUG=False`,
  noindex and database labels in `tests/unit/test_settings.py`
- [x] T009 Validate staged-deployment canonical/`hreflang` behavior for the
  stable Production host in `tests/contract/test_public_routes.py`
- [x] T010 Run local Python, Django, dependency, UI and secret checks and
  record pre-deployment results in `docs/VERIFICATION.md`

**Checkpoint:** The accepted shell is release-safe before any Vercel mutation.

## Phase 3: User Story 1 — staged protected-`main` deployment (P1)

**Goal:** Produce one Ready Production-target deployment from an exact green
protected-`main` SHA without assigning the stable public alias.

**Independent test:** Deployment metadata reports the approved SHA and
Production target while `kan-open-research-lab.vercel.app` remains unassigned.

- [ ] T011 [US1] Obtain separate Production authorization and record the gate
  in `specs/003-vercel-production-release/checklists/production-release.md`
- [ ] T012 [US1] Resolve clean local `main`, `origin/main`, exact SHA and green
  required checks in `docs/VERIFICATION.md`
- [ ] T013 [US1] Create only the minimum Production-scoped variables after
  authorization and record names/scopes without values in
  `docs/VERIFICATION.md`
- [ ] T014 [US1] Run one explicit `--prod --skip-domain` deployment and record
  command shape, CLI version, deployment ID and immutable URL in
  `docs/VERIFICATION.md`
- [ ] T015 [US1] Confirm Ready state, exact source SHA, Production target and
  absent stable-alias assignment in `docs/VERIFICATION.md`

**Checkpoint:** A staged Production artifact exists, but public traffic has not
moved.

## Phase 4: User Story 3 — immutable-URL verification (P1)

**Goal:** Prove the staged artifact safe through its deployment-specific URL
before promotion.

**Independent test:** The complete release suite passes against the immutable
URL and the stable alias is still unassigned.

- [ ] T016 [P] [US3] Run RU/EN primary, method, 404, static/font and locale
  smoke checks and record them in `docs/VERIFICATION.md`
- [ ] T017 [P] [US3] Verify canonical/`hreflang`, `noindex`, security headers,
  liveness, readiness and compute state in `docs/VERIFICATION.md`
- [ ] T018 [P] [US3] Run all 24 Playwright/axe, keyboard, no-JavaScript,
  mobile and desktop checks and record them in `docs/VERIFICATION.md`
- [ ] T019 [P] [US3] Run redacted HTTP 500, secret, migration, PostgreSQL and
  worker log searches and record summaries in `docs/VERIFICATION.md`
- [ ] T020 [US3] Complete immutable-URL gates CHK043–CHK061 in
  `specs/003-vercel-production-release/checklists/production-release.md`

**Checkpoint:** Only an immutable-URL-clean artifact may proceed to promotion.

## Phase 5: User Story 2 — explicit public promotion (P1)

**Goal:** Move the exact stable alias to the verified deployment without a
rebuild and verify public behavior.

**Independent test:** The public alias resolves to the verified deployment
ID/SHA and critical checks pass while Preview remains protected.

- [ ] T021 [US2] Re-resolve the exact stable alias and promotion target in
  `docs/VERIFICATION.md`
- [ ] T022 [US2] Explicitly promote only the verified deployment ID/URL and
  record the operation in `docs/VERIFICATION.md`
- [ ] T023 [P] [US2] Verify alias-to-deployment/SHA identity and anonymous
  public access in `docs/VERIFICATION.md`
- [ ] T024 [P] [US2] Repeat critical RU/EN, canonical, noindex, security,
  health and compute checks through the stable alias in
  `docs/VERIFICATION.md`
- [ ] T025 [P] [US2] Confirm Preview remains protected and run post-promotion
  redacted error/log checks in `docs/VERIFICATION.md`
- [ ] T026 [US2] Complete promotion gates CHK062–CHK067 in
  `specs/003-vercel-production-release/checklists/production-release.md`

**Checkpoint:** Production is public only after staged verification and explicit
promotion.

## Phase 6: User Story 4 — containment and recovery (P1)

**Goal:** Remove only the faulty public alias when no known-good predecessor
exists, preserving deployment and audit evidence.

**Independent test:** A read-only rehearsal proves the exact alias-removal and
restoration sequence; if containment is triggered, the immutable deployment
and logs remain while the stable alias no longer routes to it.

- [ ] T027 [US4] Rehearse exact first-release containment and stop conditions
  against `specs/003-vercel-production-release/rollback.md`
- [ ] T028 [US4] If a critical first-release failure occurs, remove only
  `kan-open-research-lab.vercel.app` and record evidence in
  `docs/VERIFICATION.md`
- [ ] T029 [US4] Confirm deployment, logs, project and Preview remain intact
  after containment in `docs/VERIFICATION.md`
- [ ] T030 [US4] Require a new PR, staged `--skip-domain` deployment and full
  immutable-URL verification before restoration in
  `specs/003-vercel-production-release/rollback.md`
- [ ] T031 [US4] Restore service only by promoting a new verified deployment
  and record post-restore checks in `docs/VERIFICATION.md`

## Phase 7: Release evidence and convergence

- [ ] T032 Complete CHK069–CHK078 and preserve redacted final evidence in
  `specs/003-vercel-production-release/checklists/production-release.md`
- [ ] T033 Update Production deployment ID, exact SHA, immutable/stable URLs,
  CLI version and results in `docs/VERIFICATION.md`
- [ ] T034 Run Spec Kit analysis and post-implementation convergence against
  `specs/003-vercel-production-release/tasks.md`
- [ ] T035 Leave Git integration, auto-deploy, custom domain, indexing,
  PostgreSQL and worker as separate owner gates in `README.md`

## Dependencies and execution order

- Phase 1 and Phase 2 precede every external mutation.
- T011 is an explicit owner authority gate; T012–T031 cannot start before it.
- US1 produces the staged artifact consumed by US3.
- US3 must pass completely before US2 promotion.
- US4 is rehearsed before deployment and executed only on a critical failure.
- Final evidence and formal convergence follow either successful promotion or
  completed containment.

## Parallel opportunities

- T005–T008 target independent settings, middleware and test files.
- T016–T019 are independent verification surfaces against the same immutable
  deployment.
- T023–T025 verify identity, public behavior and Preview/log isolation in
  parallel after promotion.

## Implementation strategy

Implement only the release contracts first. Then stage one exact `main`
artifact without aliasing, verify it completely, and promote that immutable
artifact. Never combine deployment and public traffic movement in one command.
