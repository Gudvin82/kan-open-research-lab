# Implementation Plan: Vercel Production Release

**Branch**: `codex/003-vercel-production-release` | **Date**: 2026-07-24 |
**Spec**: [spec.md](spec.md)

**Input**: Feature specification from
`/specs/003-vercel-production-release/spec.md`

## Summary

Prepare, authorize and verify one manual public Vercel Production deployment of
the accepted database-free Django shell from an exact protected-`main` SHA.
Production and Preview environments remain isolated, no database or worker is
introduced, indexing stays disabled, and Git-based automatic deployment stays
off. This planning PR stops before every external mutation.

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

**Constraints**: Protected `main` only; explicit `--prod`; public Production;
protected Preview; `DEBUG=False`; Production-only secret; no database, worker,
migration, custom domain, paid resource or indexing

**Scale/Scope**: One manual deployment, one stable alias, one immutable URL,
RU/EN public shell and one rollback rehearsal

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
5. Use a CLI command with explicit Production intent:
   `vercel deploy --prod --yes --scope gudvin82s-projects`.
   Plain `vercel` and plain `vercel deploy` are forbidden.
6. Keep Git integration, automatic deployments, domains, databases, workers
   and paid resources disabled.
7. Treat a Ready build as provisional until the complete Production checklist
   passes.
8. If any critical check fails, stop and follow [rollback.md](rollback.md);
   never “fix forward” with an unreviewed second Production deployment.

## Planned Work

### Phase 1 — Preflight and configuration contracts

1. Confirm clean `main`, fetch `origin`, and record the exact release SHA.
2. Confirm branch protection and all required GitHub checks on that SHA.
3. Record the installed Vercel CLI version and revalidate flag semantics.
4. Inspect Vercel project settings without changing them:
   Git integration disabled, Preview protected, no paid resources or domains.
5. Inventory Preview and Production environment variable **names/scopes only**.
6. Add or refine automated contracts so Production:
   - fails closed without `DJANGO_SECRET_KEY` and allowed host configuration;
   - remains `DEBUG=False`;
   - has a deliberate `noindex, nofollow` switch enabled by default;
   - cannot receive a non-Production-labelled database URL;
   - never runs migrations or worker commands.
7. Run all local and CI checks before requesting deployment authorization.

### Phase 2 — Separately authorized environment setup

1. Generate a random Production-only `DJANGO_SECRET_KEY` locally without
   printing or persisting it.
2. Add only the minimum Production variables through the Vercel secret store:
   `DJANGO_SECRET_KEY`, settings module/host values if required, and the
   explicit indexing-disabled flag.
3. Confirm no `DATABASE_URL`, database label, worker/server credential or
   Preview secret is in Production scope.
4. Confirm Production variables are not available to Preview.
5. Record variable names and scopes only.

### Phase 3 — Manual Production deployment

1. Re-check the SHA and CI immediately before deployment.
2. Run exactly one manual deployment with explicit `--prod`.
3. Record command shape, CLI version, deployment ID, immutable URL, stable
   Production URL, target, state and reported source SHA.
4. Do not enable Git integration or make another deployment automatically.

### Phase 4 — Runtime acceptance

1. Verify anonymous public access to Production and authenticated protection
   of Preview.
2. Run smoke checks against both immutable and stable Production URLs:
   root redirect, RU/EN primary pages, method pages, localized 404, CSS/font,
   language switching, canonical and `hreflang`.
3. Verify health/liveness, honest database-free readiness and
   `compute_node_unavailable`.
4. Verify security headers, `noindex, nofollow`, and absence of sensitive data
   from HTML and headers.
5. Run Playwright/axe for RU/EN, keyboard/no-JavaScript, 320 px and desktop.
6. Inspect redacted runtime-log queries for HTTP 500, secrets, migrations,
   PostgreSQL and worker activity.
7. Compare cold/warm samples with Preview evidence as an observation, not SLA.

### Phase 5 — Evidence and release decision

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
  known-good Production target. The owner must choose and approve the
  first-release containment behavior before deployment. Until then, Production
  is blocked even if every other check is green.

## Project Structure

### Documentation in this planning checkpoint

```text
specs/003-vercel-production-release/
├── spec.md
├── plan.md
├── rollback.md
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

**Structure Decision**: The planning PR adds documentation only. Any runtime or
test changes discovered by the plan belong to a later reviewed release PR
before Production authorization.

## Planning Decisions

- Use `--prod` as the explicit Vercel Production target flag documented by the
  installed CLI; never rely on CLI defaults.
- Use the Vercel-assigned stable URL for this stage; custom domain is deferred.
- Keep Production `noindex, nofollow` until a separate permanent-domain and
  content-indexing decision.
- Verify the same immutable artifact through both immutable and stable URLs.
- Do not enable automatic deployment as part of the first manual release.
- Do not delete failed deployments; deployment history is audit evidence.

## Open Decision

**First-release containment when no previous healthy Production deployment
exists.** Vercel rollback-to-previous requires an eligible earlier Ready
Production deployment, and none currently exists. Before authorizing the first
release, the owner must select a containment action supported by the verified
Vercel project controls, such as immediately removing/parking the public alias
or disabling the faulty deployment. This planning PR intentionally does not
perform or pre-authorize either mutation.

## Complexity Tracking

No constitutional exception is requested.
