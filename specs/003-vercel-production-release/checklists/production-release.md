# Production Release Checklist: Vercel Public Shell

**Purpose**: Gate the first public Vercel Production release and its evidence

**Created**: 2026-07-24

**Feature**: [spec.md](../spec.md)

**Status**: Planning only; unchecked items are not authorization to execute

## Authorization and source identity

- [ ] CHK001 Separate owner approval for Production deployment is recorded.
- [ ] CHK002 Local branch is `main`, worktree is clean and `HEAD` equals
  `origin/main`.
- [ ] CHK003 Exact full release SHA is recorded.
- [ ] CHK004 Required `governance`, `python`, `secrets` and `ui` checks pass on
  that exact SHA.
- [ ] CHK005 No unreviewed commit was added after approval.
- [ ] CHK006 Installed Vercel CLI version and flag behavior are recorded.
- [ ] CHK007 Staged command uses explicit `--prod --skip-domain`; plain
  `vercel`, plain `vercel deploy` and automatic Production aliasing are absent.

## Provider capability preflight

- [ ] CHK008 Current project/plan support for `--skip-domain` is confirmed.
- [ ] CHK009 Separate `vercel promote` support is confirmed.
- [ ] CHK010 Exact stable Production alias is read from current project
  metadata and recorded without guessing.
- [ ] CHK011 The exact alias can be removed independently without deleting the
  deployment, project domain, project, Preview or logs.
- [ ] CHK012 Alias restoration through promotion of a new verified deployment
  is confirmed.
- [ ] CHK013 Exact stage, promote, containment and restoration command shapes
  are recorded without tokens or secrets.
- [ ] CHK014 Production remains `noindex`, and no Production secret or
  environment mutation is created during planning.

## Vercel project and environment isolation

- [ ] CHK015 Project and team IDs are resolved without exposing tokens.
- [ ] CHK016 Git integration and automatic Production deployment remain
  disabled.
- [ ] CHK017 Production is configured for public anonymous access.
- [ ] CHK018 Accepted Preview remains protected by Vercel Authentication.
- [ ] CHK019 A random `DJANGO_SECRET_KEY` exists only in Production scope.
- [ ] CHK020 `DEBUG=False` is verified.
- [ ] CHK021 Production indexing is disabled with `noindex, nofollow`.
- [ ] CHK022 Production variable names/scopes are recorded without values.
- [ ] CHK023 Production contains no `DATABASE_URL`, PostgreSQL credential,
  worker credential or research-server credential.
- [ ] CHK024 Preview cannot access Production-only application secrets.
- [ ] CHK025 No custom domain, paid resource, database, storage or worker is
  created.
- [ ] CHK026 Build/runtime configuration contains no migration, worker or ML
  command.

## Pre-deployment quality

- [ ] CHK027 Ruff format and lint pass.
- [ ] CHK028 mypy and pytest pass.
- [ ] CHK029 Django deployment checks pass with Production settings.
- [ ] CHK030 Migration dry-run reports no changes.
- [ ] CHK031 Python and npm dependency audits pass.
- [ ] CHK032 Local Playwright/axe suite passes.
- [ ] CHK033 Secret scan passes with redaction enabled.

## Rollback readiness

- [ ] CHK034 A prior Ready, verified Production deployment ID/SHA is recorded,
  or its absence is explicitly recorded.
- [ ] CHK035 The prior target is not an Error deployment and is not
  `dpl_DRbR6AZwZ29MMk4SH66xzeLa5A1z`.
- [ ] CHK036 First-release containment records exact alias
  `kan-open-research-lab.vercel.app` and removes only its assignment when no
  prior known-good deployment exists.
- [ ] CHK037 The rollback operator, command shape and stop conditions are
  reviewed without executing them.

## Staged Production deployment

- [ ] CHK038 SHA and required checks are revalidated immediately before the
  command.
- [ ] CHK039 Exactly one separately authorized manual
  `--prod --skip-domain` deployment is started.
- [ ] CHK040 Deployment reports Production target, Ready state and the expected
  source SHA.
- [ ] CHK041 Deployment ID and immutable URL are captured; stable Production
  alias remains unassigned.
- [ ] CHK042 No Git integration or automatic follow-up deployment is enabled.

## Immutable-URL verification

- [ ] CHK043 Deployment-specific URL is reachable for acceptance testing.
- [ ] CHK044 Preview still requires Vercel Authentication.
- [ ] CHK045 `/` redirects to `/ru/`.
- [ ] CHK046 RU/EN primary and KAN/MLP/PINN/comparison routes pass on immutable
  deployment URL.
- [ ] CHK047 Same-entity language switching passes.
- [ ] CHK048 Localized RU/EN 404 passes.
- [ ] CHK049 CSS and Golos Text return HTTP 200.
- [ ] CHK050 Canonical and reciprocal `hreflang` use
  `https://kan-open-research-lab.vercel.app` rather than the immutable host.
- [ ] CHK051 Meta robots and `X-Robots-Tag` return `noindex, nofollow`.
- [ ] CHK052 `/health/live/` returns HTTP 200.
- [ ] CHK053 Database-free readiness remains honestly unavailable.
- [ ] CHK054 Compute endpoint returns HTTP 503
  `compute_node_unavailable`.
- [ ] CHK055 Security headers pass.
- [ ] CHK056 Public HTML and headers contain no sensitive values.
- [ ] CHK057 All 24 Playwright/axe RU/EN tests pass with no critical/serious
  finding.
- [ ] CHK058 Keyboard and no-JavaScript checks pass.
- [ ] CHK059 Mobile 320 px and desktop checks pass without horizontal overflow.
- [ ] CHK060 Browser console has no unexpected errors.
- [ ] CHK061 Cold/warm response samples show no obvious server failure.

## Promotion and stable-alias verification

- [ ] CHK062 Exact stable alias is re-resolved immediately before promotion.
- [ ] CHK063 Only the verified deployment ID/URL is passed to
  `vercel promote`; no rebuild occurs.
- [ ] CHK064 Stable alias points to the verified deployment ID and source SHA.
- [ ] CHK065 Stable Production URL is publicly reachable without Vercel login.
- [ ] CHK066 Root/RU/EN smoke, canonical/`hreflang`, `noindex`, headers,
  liveness, readiness and compute state pass through the stable alias.
- [ ] CHK067 Post-promotion runtime logs contain no HTTP 500, secret,
  migration, PostgreSQL or worker signal.
- [ ] CHK068 On critical first-release failure, exact alias removal succeeds
  while deployment, project, Preview and logs remain intact.

## Logs and evidence

- [ ] CHK069 Release-window runtime logs contain no HTTP 500 cluster.
- [ ] CHK070 Redacted searches find no secret exposure.
- [ ] CHK071 Redacted searches find no migration or PostgreSQL activity.
- [ ] CHK072 Redacted searches find no worker/server activity.
- [ ] CHK073 Raw internal logs and secret values are excluded from Git and PR.
- [ ] CHK074 `docs/VERIFICATION.md` records exact SHA, deployment ID, URLs,
  date, CLI version, environment names/scopes and results.
- [ ] CHK075 Failed historical deployments remain intact as audit evidence.
- [ ] CHK076 Production stays `noindex`; auto-deploy, domain, DB and worker
  remain separate owner gates.

## Release outcome

- [ ] CHK077 Every blocking item passes and the release is accepted, or the
  rollback/containment path is executed.
- [ ] CHK078 Any rollback records both deployment IDs, reason, operator time
  and post-rollback verification.
