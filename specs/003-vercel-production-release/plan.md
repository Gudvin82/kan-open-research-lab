# Implementation Plan: Vercel Production Release

**Branch**: `codex/003-production-release-blockers` | **Date**: 2026-07-24 |
**Spec**: [spec.md](spec.md)

**Input**: Feature specification from
`/specs/003-vercel-production-release/spec.md`

## Summary

Prepare, authorize and verify one staged Vercel Production-target deployment of
the accepted database-free Django shell from an exact protected-`main` SHA.
The deployment uses `--skip-domain`, passes the complete acceptance suite
through its immutable URL, and only then receives public traffic through an
explicit promotion. Production and Preview environments remain isolated, no
database or worker is introduced, indexing stays disabled, and Git-based
automatic deployment stays off. This release-blocker PR implements only the
fail-closed host, canonical and indexing contracts and stops before every
external mutation.

## Technical Context

**Language/Version**: Python 3.13, Django 6.0; Vercel CLI version recorded and
held constant for the release window

**Primary Dependencies**: Existing Django/WhiteNoise runtime; existing
development-only Playwright and `@axe-core/playwright`

**Storage**: None; database-free public shell

**Testing**: Ruff, mypy, pytest, Django deployment checks, npm audit,
Playwright/axe, route/header probes and redacted Vercel runtime-log queries

**Target Platform**: Vercel Python Function, Production environment, stable
Vercel-assigned URL

**Project Type**: Controlled release of the existing server-rendered Django
monolith

**Performance Goals**: No HTTP 500 during the release window; no obvious cold
start regression relative to the accepted Preview evidence

**Constraints**: Protected `main` only; explicit `--prod --skip-domain`;
immutable-URL verification before promote; public Production only after
promote; protected Preview; `DEBUG=False`; Production-only secret; no database,
worker, migration, custom domain, paid resource or indexing

**Scale/Scope**: One staged manual deployment, one explicit promotion, one
stable alias, one immutable URL, RU/EN public shell and one containment
rehearsal

## Constitution Check

*GATE: Passed for planning; must be re-checked immediately before deployment.*

| Principle | Plan evidence | Result |
|---|---|---|
| I. Scientific honesty | Release changes no scientific status or research claim | PASS |
| II. Reproducibility | Exact SHA, deployment ID, CLI version, URLs and checks are recorded | PASS |
| III. Fair comparison | No method benchmark or comparison changes | PASS |
| IV. Sources and claim boundaries | Accepted RU/EN copy is deployed unchanged | PASS |
| V. Execution safety | No worker, arbitrary execution, DB credential or server credential | PASS |
| VI. Simplicity and resources | Existing free Vercel project; no new service or paid resource | PASS |
| VII. Accessibility/bilingual web | Existing RU/EN and accessibility suite runs against Production | PASS |
| VIII. Spec-driven evidence | Spec, plan, checklist and rollback plan precede release authorization | PASS |

## Release Gates

1. Merge this planning PR only after the owner accepts the plan and resolves
   the first-release rollback decision.
2. Create a later implementation/release PR for any required configuration or
   test change; do not mix those changes into this planning checkpoint.
3. Obtain a separate explicit owner authorization immediately before any
   Production environment or deployment mutation.
4. Re-resolve protected `origin/main`, exact SHA and required checks after that
   authorization. Approval of an older SHA does not transfer automatically.
5. Use a staged CLI command with explicit Production intent and no automatic
   alias:
   `vercel deploy --prod --skip-domain --yes --scope gudvin82s-projects`.
   Plain `vercel`, plain `vercel deploy` and Production deployment without
   `--skip-domain` are forbidden.
6. Keep Git integration, automatic deployments, domains, databases, workers
   and paid resources disabled.
7. Treat a Ready staged build as provisional and private from the stable alias
   until the immutable-URL checklist passes.
8. Promote only the exact verified deployment and repeat critical checks
   through the stable alias.
9. If any critical check fails, stop and follow [rollback.md](rollback.md);
   never “fix forward” with an unreviewed second Production deployment.

## Planned Work

### Phase 1 — Preflight and configuration contracts

1. Confirm clean `main`, fetch `origin`, and record the exact release SHA.
2. Confirm branch protection and all required GitHub checks on that SHA.
3. Record the installed Vercel CLI version and revalidate flag semantics.
4. Inspect Vercel project settings without changing them:
   Git integration disabled, Preview protected, no paid resources or domains.
5. Confirm `--skip-domain`, separate `promote`, exact stable alias removal and
   restoration on the active project/plan.
6. Discover and record the exact stable Production alias from Vercel project
   metadata; never derive or guess it from the project name.
7. Inventory Preview and Production environment variable **names/scopes only**.
8. Add or refine automated contracts so Production:
   - fails closed without `DJANGO_SECRET_KEY` and allowed host configuration;
   - remains `DEBUG=False`;
   - has a deliberate `noindex, nofollow` switch enabled by default;
   - cannot receive a non-Production-labelled database URL;
   - never runs migrations or worker commands.
9. Run all local and CI checks before requesting deployment authorization.

### Phase 2 — Separately authorized environment setup

1. After separate release authorization, generate a random Production-only
   `DJANGO_SECRET_KEY` locally without printing or persisting it.
2. Depend on Vercel-provided `VERCEL_URL` and
   `VERCEL_PROJECT_PRODUCTION_URL`; do not create host or indexing environment
   variables for the first release.
3. Leave `PUBLIC_BASE_URL` and `DJANGO_ALLOWED_HOSTS` absent unless a later
   reviewed exact-host use case requires them.
4. Confirm no `DATABASE_URL`, database label, worker/server credential or
   Preview secret is in Production scope.
5. Confirm Production variables are not available to Preview.
6. Record variable names and scopes only.

### Phase 3 — Staged Production deployment

1. Re-check the SHA and CI immediately before deployment.
2. Run exactly one manual deployment with explicit
   `--prod --skip-domain`.
3. Record command shape, CLI version, deployment ID, immutable URL, target,
   state and reported source SHA.
4. Confirm the stable Production alias was not assigned.
5. Do not enable Git integration or make another deployment automatically.

### Phase 4 — Immutable-URL acceptance

1. Run smoke checks against the deployment-specific immutable URL:
   root redirect, RU/EN primary pages, method pages, localized 404, CSS/font,
   language switching, canonical and `hreflang`.
2. Verify health/liveness, honest database-free readiness and
   `compute_node_unavailable`.
3. Verify security headers, `noindex, nofollow`, and absence of sensitive data
   from HTML and headers.
4. Run all 24 Playwright/axe checks for RU/EN, keyboard/no-JavaScript, 320 px
   and desktop.
5. Inspect redacted runtime-log queries for HTTP 500, secrets, migrations,
   PostgreSQL and worker activity.
6. Compare cold/warm samples with Preview evidence as an observation, not SLA.
7. Stop without promotion if any check fails.

### Phase 5 — Explicit promotion and public verification

1. Re-resolve and record the exact stable alias immediately before promotion.
2. Promote only the verified deployment:
   `vercel promote <verified-deployment-id-or-url> --yes --scope gudvin82s-projects`.
3. Confirm the stable alias points to the same deployment ID and source SHA.
4. Verify anonymous public access to the stable alias and continued
   authentication protection of Preview.
5. Repeat root/RU/EN smoke, canonical/hreflang, `noindex`, security headers,
   liveness, honest readiness, compute state and HTTP 500 log checks through
   the stable alias.
6. If a critical check fails and no predecessor exists, remove only the exact
   stable alias per [rollback.md](rollback.md); do not delete the deployment.

### Phase 6 — Evidence and release decision

1. If all gates pass, add a Production section to `docs/VERIFICATION.md` with
   exact provenance and results.
2. Leave `noindex` enabled and Git integration disabled.
3. Keep Preview and the failed historical deployment as audit evidence.
4. Request a separate owner decision before:
   - enabling GitHub–Vercel automatic deployment from protected `main`;
   - adopting a permanent domain;
   - enabling indexing;
   - connecting a database or worker.

## Rollback Strategy

The detailed procedure is [rollback.md](rollback.md).

- Before deployment, identify the most recent **Ready and previously verified**
  Production deployment and record its ID/SHA.
- Rollback uses Vercel alias rollback to that immutable deployment without a
  rebuild, followed by critical smoke and log checks.
- The historical `dpl_DRbR6AZwZ29MMk4SH66xzeLa5A1z` is `ERROR` and is never a
  rollback candidate.
- For the first healthy Production release there is currently no prior
  known-good Production target. The selected containment is removal of the
  exact stable public alias without deleting the deployment, project, Preview
  or logs. A corrected artifact repeats staged deployment, immutable-URL
  verification and explicit promotion.

## Project Structure

### Documentation in this planning checkpoint

```text
specs/003-vercel-production-release/
├── spec.md
├── plan.md
├── convergence.md
├── preflight.md
├── rollback.md
├── tasks.md
└── checklists/
    └── production-release.md
```

### Possible later implementation files

```text
src/config/settings/production.py
src/webapp/middleware.py
tests/contract/test_vercel_config.py
tests/unit/test_settings.py
docs/VERIFICATION.md
```

**Structure Decision**: The accepted planning PR added documentation only.
The separately reviewed blocker-remediation PR owns T005–T010 runtime and test
changes and still stops before Production authorization or Vercel mutation.

## Planning Decisions

- Use `--prod --skip-domain` for staged Production and never rely on CLI
  defaults or automatic aliasing.
- Promote the exact verified deployment only after immutable-URL acceptance.
- Use the Vercel-assigned stable URL for this stage; custom domain is deferred.
- Keep Production `noindex, nofollow` until a separate permanent-domain and
  content-indexing decision.
- Verify the same immutable artifact through both immutable and stable URLs.
- Do not enable automatic deployment as part of the first manual release.
- Do not delete failed deployments; deployment history is audit evidence.
- Build Production `ALLOWED_HOSTS` only from exact, validated origins; never
  use `*` or `.vercel.app`.
- Build canonical and `hreflang` from the stable configured HTTPS origin,
  never from request Host.
- Keep indexing deny-by-default in application configuration; do not create an
  environment toggle during blocker remediation or the first release.

## Resolved Containment Decision

Read-only preflight in [preflight.md](preflight.md) identified
`kan-open-research-lab.vercel.app` as the verified, non-branch stable project
domain. The active Vercel CLI supports Production `--skip-domain`, separate
promotion, alias removal and alias restoration on the current Hobby team.

If the first promoted deployment fails and no predecessor exists, remove only
that exact public alias. Keep the deployment, project, Preview and logs. If a
later preflight finds that the exact system alias cannot be removed safely,
Production remains blocked until the owner approves Deployment Protection or a
maintenance/parking deployment.

## Complexity Tracking

No constitutional exception is requested.
