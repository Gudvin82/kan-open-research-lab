# Feature Specification: Vercel Production Release

**Feature Branch**: `codex/003-vercel-production-release`

**Created**: 2026-07-24

**Status**: Draft — planning checkpoint; Production is not authorized

**Input**: Prepare a controlled first Vercel Production release of the
database-free bilingual Django shell after PR #4 was visually accepted and
squash-merged into protected `main`.

## User Scenarios & Testing

### User Story 1 - Stage the accepted `main` artifact manually (Priority: P1)

The owner can authorize one manual Production-target deployment knowing that
it is built from an exact, green commit on protected `main`, receives no
automatic public alias, and can be verified before public traffic is moved.

**Why this priority**: Source identity and an explicit release action are the
primary controls separating an accepted Preview from a public release.

**Independent Test**: Before deployment, compare local `HEAD`, `origin/main`
and the recorded release SHA, confirm a clean worktree and green required
checks, then verify that `--prod --skip-domain` produces a Ready
Production-target deployment for that exact SHA without assigning the stable
public alias.

**Acceptance Scenarios**:

1. **Given** Production has been separately authorized, **When** the release
   command is prepared, **Then** it uses a clean protected `main`, a recorded
   commit SHA and explicit `--prod --skip-domain`.
2. **Given** the branch, SHA or required checks differ, **When** the preflight
   runs, **Then** deployment stops before any Vercel mutation.
3. **Given** a staged deployment is Ready, **When** it is verified, **Then**
   the stable Production alias remains unassigned until every immutable-URL
   gate passes.
4. **Given** no separate Production authorization exists, **When** this
   planning stage is accepted, **Then** no deployment occurs.

---

### User Story 2 - Serve an isolated public Production shell (Priority: P1)

A public reader can access a stable Vercel Production URL without Vercel
Authentication while Preview remains protected, and the shell operates without
PostgreSQL, migrations, worker integration or server credentials.

**Why this priority**: Public availability must not weaken environment
isolation or expand the accepted database-free architecture.

**Independent Test**: Open the stable Production URL in a signed-out browser,
verify all RU/EN routes and inspect environment metadata without secret values;
then confirm the existing Preview still requires Vercel Authentication.

**Acceptance Scenarios**:

1. **Given** a staged Production deployment passed every immutable-URL gate,
   **When** that exact deployment is explicitly promoted, **Then** an anonymous
   reader can open the stable URL.
2. **Given** the Production environment, **When** configuration is inspected,
   **Then** it contains a Production-only random `DJANGO_SECRET_KEY`,
   `DEBUG=False`, and no database, worker or server credential.
3. **Given** the Preview environment, **When** access and environment scope are
   inspected, **Then** Preview remains protected and cannot read Production
   application secrets.
4. **Given** no permanent domain or final public-content approval, **When**
   robots metadata is read, **Then** Production returns `noindex, nofollow`.

---

### User Story 3 - Verify the public release and preserve evidence (Priority: P1)

The owner can review a concise, reproducible record proving that the public
Production deployment serves the accepted bilingual shell safely.

**Why this priority**: A successful build is not sufficient release evidence;
runtime behavior, public access, security boundaries and exact provenance must
also be checked.

**Independent Test**: Run smoke, localized route, Playwright/axe,
mobile/desktop, no-JavaScript and log inspections against the immutable and
stable Production URLs, then reproduce the recorded results from
`docs/VERIFICATION.md`.

**Acceptance Scenarios**:

1. **Given** a Ready staged deployment with no public alias, **When** the
   release verification runs, **Then** RU/EN pages, method routes, localized
   404, static assets, health endpoints, canonical/hreflang, security headers
   and honest compute state are checked through its deployment-specific URL.
2. **Given** the staged deployment passes and is promoted, **When** critical
   smoke checks are repeated, **Then** the stable public alias resolves to the
   same deployment and exact SHA.
3. **Given** Production runtime logs, **When** the release window is inspected,
   **Then** HTTP 500, secret leakage, migration, PostgreSQL and worker searches
   are recorded without publishing raw sensitive logs.
4. **Given** all gates pass, **When** evidence is committed later, **Then**
   deployment ID, immutable and stable URLs, exact `main` SHA, date, CLI
   version, non-secret environment inventory and results are recorded.

---

### User Story 4 - Recover from a bad Production release (Priority: P1)

The operator can stop exposure of a faulty release and restore the most recent
known-good Production deployment without rebuilding it.

**Why this priority**: Production authorization requires a practical recovery
path and explicit stop conditions before the first public mutation.

**Independent Test**: In a non-mutating rehearsal, identify an eligible prior
Ready Production deployment, verify its ID and source SHA, and walk through the
rollback decision tree without moving aliases.

**Acceptance Scenarios**:

1. **Given** a previous verified Production deployment exists, **When** the
   current release fails post-deploy checks, **Then** aliases are rolled back to
   the recorded previous deployment and smoke checks are repeated.
2. **Given** no previous healthy Production deployment exists, **When** the
   first promoted release fails, **Then** the operator removes the exact stable
   public alias without deleting the deployment, project, Preview or logs.
3. **Given** rollback succeeds, **When** evidence is updated, **Then** the
   failed deployment, restored deployment, reason and verification results are
   documented without deleting audit history.

## Edge Cases

- The local checkout is clean but `origin/main` advanced after approval.
- Required GitHub checks were green on a parent SHA, not the release SHA.
- Vercel CLI defaults to an unexpected target when no target flag is supplied.
- `--skip-domain` is ignored or aliases a staged deployment unexpectedly.
- The Production alias differs from the immutable deployment URL.
- The stable URL redirects through an unexpected host, producing incorrect
  canonical or `hreflang` values.
- Production inherits a Preview variable or Preview can read a
  Production-scoped variable.
- Deployment is Ready but returns cold-start HTTP 500 or missing static assets.
- Health readiness correctly remains unavailable because no database exists.
- Preview Authentication is accidentally disabled while Production is opened.
- No previous healthy Production deployment exists for the first release.
- The project-owned `vercel.app` alias cannot be removed on the active plan.
- Rollback restores the alias but not the expected source SHA.
- A log query returns sensitive values that must not be pasted into Git or PR.

## Requirements

### Functional Requirements

- **FR-001**: Production MUST deploy only from protected `main`.
- **FR-002**: The release MUST bind to an exact recorded `main` commit SHA.
- **FR-003**: Local `HEAD`, `origin/main` and the release SHA MUST match before
  deployment.
- **FR-004**: The worktree MUST be clean and all required GitHub checks for the
  release SHA MUST pass.
- **FR-005**: The first Production deployment MUST be manual and use explicit
  `--prod --skip-domain`; a plain `vercel`, plain `vercel deploy` or automatic
  alias assignment is forbidden.
- **FR-006**: The Vercel CLI version and the complete non-secret command shape
  MUST be recorded.
- **FR-007**: GitHub–Vercel automatic deployment MUST remain disabled until the
  manual release is separately accepted.
- **FR-008**: Production MUST be public; Preview MUST remain protected by
  Vercel Authentication.
- **FR-009**: Production MUST use a random `DJANGO_SECRET_KEY` scoped only to
  the Production environment.
- **FR-010**: Production MUST run with `DEBUG=False`.
- **FR-011**: Production MUST NOT receive `DATABASE_URL`, PostgreSQL
  credentials, worker credentials or research-server credentials.
- **FR-012**: Build and runtime commands MUST NOT run migrations, worker
  processes or ML commands.
- **FR-013**: Production and Preview application secrets MUST remain in
  separate Vercel environment scopes.
- **FR-014**: The release MUST create no paid resource, custom domain,
  PostgreSQL service, object storage or worker integration.
- **FR-015**: A stable Vercel Production URL and immutable deployment URL MUST
  both be recorded.
- **FR-016**: Canonical and reciprocal `hreflang` URLs MUST use the approved
  HTTPS Production host.
- **FR-017**: Production MUST emit `noindex, nofollow` until permanent-domain
  and final-public-content approval is recorded.
- **FR-018**: Removing `noindex` MUST be a later explicit owner decision.
- **FR-019**: `/health/live/` MUST return HTTP 200 for a healthy web runtime.
- **FR-020**: Database-free readiness MUST remain honest and MUST NOT be
  converted to a false healthy state.
- **FR-021**: Compute status MUST remain HTTP 503
  `compute_node_unavailable` until a separate worker integration is accepted.
- **FR-022**: Production verification MUST cover root redirect, RU/EN primary
  and method routes, localized 404, CSS/font assets and language switching.
- **FR-023**: Production verification MUST include Playwright/axe,
  keyboard/no-JavaScript, 320 px mobile and desktop checks.
- **FR-024**: Security headers and absence of sensitive values in public HTML
  and headers MUST be checked.
- **FR-025**: Runtime logs MUST be searched for HTTP 500, secrets, migrations,
  PostgreSQL and worker activity during the release window.
- **FR-026**: Raw internal logs and secret values MUST NOT be committed or
  copied into the PR.
- **FR-027**: `docs/VERIFICATION.md` MUST record the deployment ID, exact
  `main` SHA, URLs, date, environment names without secret values and all
  release results.
- **FR-028**: The failed deployment
  `dpl_DRbR6AZwZ29MMk4SH66xzeLa5A1z` MUST remain as audit evidence.
- **FR-029**: Preview commands MUST continue to use explicit
  `--target preview`.
- **FR-030**: When a previous known-good deployment exists, rollback MUST
  target that recorded, verified Ready Production deployment and re-run
  critical smoke checks.
- **FR-031**: If no previous healthy Production deployment exists, the first
  release MUST remove the exact stable public alias as containment without
  deleting the deployment, project, Preview or logs.
- **FR-032**: Production deployment, rollback execution, Git integration,
  domain, database and worker mutations each remain separately authorized
  actions.
- **FR-033**: Before Production authorization, read-only preflight MUST confirm
  current-project support for `--skip-domain`, separate promotion, exact stable
  alias removal and alias restoration.
- **FR-034**: The exact intended stable Production alias MUST be discovered
  from current Vercel project metadata and MUST NOT be guessed.
- **FR-035**: Every staged Production deployment MUST pass the full acceptance
  suite through its deployment-specific URL before promotion.
- **FR-036**: Promotion MUST target the exact verified deployment ID/URL and
  MUST NOT rebuild the artifact.
- **FR-037**: Critical smoke, identity and security checks MUST repeat through
  the stable public alias immediately after promotion.
- **FR-038**: If exact alias removal is unsupported for the active plan/domain
  type, Production MUST remain blocked until Deployment Protection or a
  reviewed maintenance/parking deployment is approved.

### Key Entities

- **Release Candidate**: Exact protected-`main` SHA with clean-checkout and CI
  evidence.
- **Production Deployment**: Immutable Vercel deployment ID/URL, target,
  source SHA, state and runtime-verification record.
- **Stable Production URL**: Public Vercel alias used for user access and
  canonical metadata.
- **Environment Inventory**: Names and scopes of required variables without
  their values.
- **Known-good Deployment**: Prior Ready Production deployment that passed the
  release checklist and is eligible as a rollback target.
- **Release Evidence**: Timestamped checks, URLs, SHA, CLI version, deployment
  metadata and redacted log-query outcomes.

## Success Criteria

### Measurable Outcomes

- **SC-001**: The deployed source SHA equals the recorded protected `main` SHA
  and all required checks for that SHA are successful.
- **SC-002**: One manual Production deployment uses
  `--prod --skip-domain`; zero public aliases move before immutable-URL
  verification passes.
- **SC-003**: Exactly one explicit promotion points the stable alias to the
  verified deployment, while the accepted Preview remains protected.
- **SC-004**: 100% of required RU/EN primary and method routes pass smoke
  checks on both immutable and stable Production hosts.
- **SC-005**: The existing 24-test Playwright/axe suite passes against
  Production with no critical or serious axe findings.
- **SC-006**: Production verification finds zero HTTP 500 responses, exposed
  secrets, migration execution, PostgreSQL access or worker activity.
- **SC-007**: Production returns `noindex, nofollow`, correct HTTPS canonical
  and reciprocal RU/EN `hreflang` on every tested page.
- **SC-008**: `docs/VERIFICATION.md` contains all release provenance and
  results without secret values or raw internal logs.
- **SC-009**: The rollback rehearsal identifies either one verified eligible
  prior deployment or the explicit absence of such a target before release.

## Assumptions

- PR #4 was visually accepted and squash-merged to `main` as
  `c9362f71ca464f9ad8b4f6ec35157b7c0ffc9e53`.
- The accepted Preview remains available and protected.
- The first healthy Production deployment has no earlier known-good
  Production predecessor; first-release containment removes the exact public
  alias without deleting deployment evidence.
- Read-only preflight identified `kan-open-research-lab.vercel.app` as the
  verified, non-branch project domain intended for the stable Production alias.
- No database is required for the public shell.
- A Vercel-assigned stable URL is sufficient for this stage; a custom domain
  is outside scope.

## Explicit Exclusions

- Running a Production deployment during this planning checkpoint.
- Enabling GitHub–Vercel automatic deployments.
- Assigning or buying a custom domain.
- Creating or connecting PostgreSQL, object storage or paid resources.
- Integrating the KAN/ML worker or research server.
- Running migrations.
- Removing Preview Authentication.
- Enabling search-engine indexing.
