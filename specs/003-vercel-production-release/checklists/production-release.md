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
- [ ] CHK007 Command uses explicit `--prod`; plain `vercel` and plain
  `vercel deploy` are absent from the release procedure.

## Vercel project and environment isolation

- [ ] CHK008 Project and team IDs are resolved without exposing tokens.
- [ ] CHK009 Git integration and automatic Production deployment remain
  disabled.
- [ ] CHK010 Production is configured for public anonymous access.
- [ ] CHK011 Accepted Preview remains protected by Vercel Authentication.
- [ ] CHK012 A random `DJANGO_SECRET_KEY` exists only in Production scope.
- [ ] CHK013 `DEBUG=False` is verified.
- [ ] CHK014 Production indexing is disabled with `noindex, nofollow`.
- [ ] CHK015 Production variable names/scopes are recorded without values.
- [ ] CHK016 Production contains no `DATABASE_URL`, PostgreSQL credential,
  worker credential or research-server credential.
- [ ] CHK017 Preview cannot access Production-only application secrets.
- [ ] CHK018 No custom domain, paid resource, database, storage or worker is
  created.
- [ ] CHK019 Build/runtime configuration contains no migration, worker or ML
  command.

## Pre-deployment quality

- [ ] CHK020 Ruff format and lint pass.
- [ ] CHK021 mypy and pytest pass.
- [ ] CHK022 Django deployment checks pass with Production settings.
- [ ] CHK023 Migration dry-run reports no changes.
- [ ] CHK024 Python and npm dependency audits pass.
- [ ] CHK025 Local Playwright/axe suite passes.
- [ ] CHK026 Secret scan passes with redaction enabled.

## Rollback readiness

- [ ] CHK027 A prior Ready, verified Production deployment ID/SHA is recorded,
  or its absence is explicitly recorded.
- [ ] CHK028 The prior target is not an Error deployment and is not
  `dpl_DRbR6AZwZ29MMk4SH66xzeLa5A1z`.
- [ ] CHK029 The first-release containment action is explicitly approved if no
  prior known-good target exists.
- [ ] CHK030 The rollback operator, command shape and stop conditions are
  reviewed without executing them.

## Manual deployment

- [ ] CHK031 SHA and required checks are revalidated immediately before the
  command.
- [ ] CHK032 Exactly one separately authorized manual `--prod` deployment is
  started.
- [ ] CHK033 Deployment reports Production target, Ready state and the expected
  source SHA.
- [ ] CHK034 Deployment ID, immutable URL and stable URL are captured.
- [ ] CHK035 No Git integration or automatic follow-up deployment is enabled.

## Public runtime verification

- [ ] CHK036 Stable Production URL is reachable without Vercel login.
- [ ] CHK037 Preview still requires Vercel Authentication.
- [ ] CHK038 `/` redirects to `/ru/`.
- [ ] CHK039 RU/EN primary and KAN/MLP/PINN/comparison routes pass on immutable
  and stable hosts.
- [ ] CHK040 Same-entity language switching passes.
- [ ] CHK041 Localized RU/EN 404 passes.
- [ ] CHK042 CSS and Golos Text return HTTP 200.
- [ ] CHK043 Canonical and reciprocal `hreflang` use the approved stable HTTPS
  Production host.
- [ ] CHK044 Meta robots and `X-Robots-Tag` return `noindex, nofollow`.
- [ ] CHK045 `/health/live/` returns HTTP 200.
- [ ] CHK046 Database-free readiness remains honestly unavailable.
- [ ] CHK047 Compute endpoint returns HTTP 503
  `compute_node_unavailable`.
- [ ] CHK048 Security headers pass.
- [ ] CHK049 Public HTML and headers contain no sensitive values.
- [ ] CHK050 Playwright/axe RU/EN suite passes with no critical/serious finding.
- [ ] CHK051 Keyboard and no-JavaScript checks pass.
- [ ] CHK052 Mobile 320 px and desktop checks pass without horizontal overflow.
- [ ] CHK053 Browser console has no unexpected errors.
- [ ] CHK054 Cold/warm response samples show no obvious server failure.

## Logs and evidence

- [ ] CHK055 Release-window runtime logs contain no HTTP 500 cluster.
- [ ] CHK056 Redacted searches find no secret exposure.
- [ ] CHK057 Redacted searches find no migration or PostgreSQL activity.
- [ ] CHK058 Redacted searches find no worker/server activity.
- [ ] CHK059 Raw internal logs and secret values are excluded from Git and PR.
- [ ] CHK060 `docs/VERIFICATION.md` records exact SHA, deployment ID, URLs,
  date, CLI version, environment names/scopes and results.
- [ ] CHK061 Failed historical deployments remain intact as audit evidence.
- [ ] CHK062 Production stays `noindex`; auto-deploy, domain, DB and worker
  remain separate owner gates.

## Release outcome

- [ ] CHK063 Every blocking item passes and the release is accepted, or the
  rollback/containment path is executed.
- [ ] CHK064 Any rollback records both deployment IDs, reason, operator time
  and post-rollback verification.
