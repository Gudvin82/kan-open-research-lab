# Production Release Checklist: Vercel Public Shell

**Purpose**: Gate the first public Vercel Production release and its evidence

**Created**: 2026-07-24

**Feature**: [spec.md](../spec.md)

**Status**: Completed 2026-07-29; conditional containment items were evaluated
but not triggered because the promoted release remained healthy

## Authorization and source identity

- [x] CHK001 Separate owner approval for Production deployment is recorded.
- [x] CHK002 Local branch is `main`, worktree is clean and `HEAD` equals
  `origin/main`.
- [x] CHK003 Exact full release SHA is recorded.
- [x] CHK004 Required `governance`, `python`, `secrets` and `ui` checks pass on
  that exact SHA.
- [x] CHK005 No unreviewed commit was added after approval.
- [x] CHK006 Installed Vercel CLI version and flag behavior are recorded.
- [x] CHK007 Staged command uses explicit `--prod --skip-domain`; plain
  `vercel`, plain `vercel deploy` and automatic Production aliasing are absent.

## Provider capability preflight

- [x] CHK008 Current project/plan support for `--skip-domain` is confirmed.
- [x] CHK009 Separate `vercel promote` support is confirmed.
- [x] CHK010 Exact stable Production alias is read from current project
  metadata and recorded without guessing.
- [x] CHK011 The exact alias can be removed independently without deleting the
  deployment, project domain, project, Preview or logs.
- [x] CHK012 Alias restoration through promotion of a new verified deployment
  is confirmed.
- [x] CHK013 Exact stage, promote, containment and restoration command shapes
  are recorded without tokens or secrets.
- [x] CHK014 Production remains `noindex`, and no Production secret or
  environment mutation is created during planning.

## Vercel project and environment isolation

- [x] CHK015 Project and team IDs are resolved without exposing tokens.
- [x] CHK016 Git integration and automatic Production deployment remain
  disabled.
- [x] CHK017 Production is configured for public anonymous access.
- [x] CHK018 Accepted Preview remains protected by Vercel Authentication.
- [x] CHK019 A random `DJANGO_SECRET_KEY` exists only in Production scope.
- [x] CHK020 `DEBUG=False` is verified.
- [x] CHK021 Production indexing is disabled with `noindex, nofollow`.
- [x] CHK022 Production variable names/scopes are recorded without values.
- [x] CHK023 Production contains no `DATABASE_URL`, PostgreSQL credential,
  worker credential or research-server credential.
- [x] CHK024 Preview cannot access Production-only application secrets.
- [x] CHK025 No custom domain, paid resource, database, storage or worker is
  created.
- [x] CHK026 Build/runtime configuration contains no migration, worker or ML
  command.

## Pre-deployment quality

- [x] CHK027 Ruff format and lint pass.
- [x] CHK028 mypy and pytest pass.
- [x] CHK029 Django deployment checks pass with Production settings.
- [x] CHK030 Migration dry-run reports no changes.
- [x] CHK031 Python and npm dependency audits pass.
- [x] CHK032 Local Playwright/axe suite passes.
- [x] CHK033 Secret scan passes with redaction enabled.

## Rollback readiness

- [x] CHK034 A prior Ready, verified Production deployment ID/SHA is recorded,
  or its absence is explicitly recorded.
- [x] CHK035 The prior target is not an Error deployment and is not
  `dpl_DRbR6AZwZ29MMk4SH66xzeLa5A1z`.
- [x] CHK036 First-release containment records exact alias
  `kan-open-research-lab.vercel.app` and removes only its assignment when no
  prior known-good deployment exists.
- [x] CHK037 The rollback operator, command shape and stop conditions are
  reviewed without executing them.

## Staged Production deployment

- [x] CHK038 SHA and required checks are revalidated immediately before the
  command.
- [x] CHK039 Exactly one separately authorized manual
  `--prod --skip-domain` deployment is started.
- [x] CHK040 Deployment reports Production target, Ready state and the expected
  source SHA.
- [x] CHK041 Deployment ID and immutable URL are captured; stable Production
  alias remains unassigned.
- [x] CHK042 No Git integration or automatic follow-up deployment is enabled.

## Immutable-URL verification

- [x] CHK043 Deployment-specific URL is reachable for acceptance testing.
- [x] CHK044 Preview still requires Vercel Authentication.
- [x] CHK045 `/` redirects to `/ru/`.
- [x] CHK046 RU/EN primary and KAN/MLP/PINN/comparison routes pass on immutable
  deployment URL.
- [x] CHK047 Same-entity language switching passes.
- [x] CHK048 Localized RU/EN 404 passes.
- [x] CHK049 CSS and Golos Text return HTTP 200.
- [x] CHK050 Canonical and reciprocal `hreflang` use
  `https://kan-open-research-lab.vercel.app` rather than the immutable host.
- [x] CHK051 Meta robots and `X-Robots-Tag` return `noindex, nofollow`.
- [x] CHK052 `/health/live/` returns HTTP 200.
- [x] CHK053 Database-free readiness remains honestly unavailable.
- [x] CHK054 Compute endpoint returns HTTP 503
  `compute_node_unavailable`.
- [x] CHK055 Security headers pass.
- [x] CHK056 Public HTML and headers contain no sensitive values.
- [x] CHK057 All 24 Playwright/axe RU/EN tests pass with no critical/serious
  finding.
- [x] CHK058 Keyboard and no-JavaScript checks pass.
- [x] CHK059 Mobile 320 px and desktop checks pass without horizontal overflow.
- [x] CHK060 Browser console has no unexpected errors.
- [x] CHK061 Cold/warm response samples show no obvious server failure.

## Promotion and stable-alias verification

- [x] CHK062 Exact stable alias is re-resolved immediately before promotion.
- [x] CHK063 Only the verified deployment ID/URL is passed to
  `vercel promote`; no rebuild occurs.
- [x] CHK064 Stable alias points to the verified deployment ID and source SHA.
- [x] CHK065 Stable Production URL is publicly reachable without Vercel login.
- [x] CHK066 Root/RU/EN smoke, canonical/`hreflang`, `noindex`, headers,
  liveness, readiness and compute state pass through the stable alias.
- [x] CHK067 Post-promotion runtime logs contain no HTTP 500, secret,
  migration, PostgreSQL or worker signal.
- [x] CHK068 Not triggered: no critical post-promotion failure occurred.
  Exact alias-removal capability and the non-destructive command shape were
  confirmed during preflight.

## Logs and evidence

- [x] CHK069 Release-window runtime logs contain no HTTP 500 cluster.
- [x] CHK070 Redacted searches find no secret exposure.
- [x] CHK071 Redacted searches find no migration or PostgreSQL activity.
- [x] CHK072 Redacted searches find no worker/server activity.
- [x] CHK073 Raw internal logs and secret values are excluded from Git and PR.
- [x] CHK074 `docs/VERIFICATION.md` records exact SHA, deployment ID, URLs,
  date, CLI version, environment names/scopes and results.
- [x] CHK075 Failed historical deployments remain intact as audit evidence.
- [x] CHK076 Production stays `noindex`; auto-deploy, domain, DB and worker
  remain separate owner gates.

## Release outcome

- [x] CHK077 Every blocking item passes and the release is accepted, or the
  rollback/containment path is executed.
- [x] CHK078 Not triggered: the release required no rollback. The rollback
  evidence contract remains recorded for future releases.
