# Vercel Production Capability Preflight

**Checked:** 2026-07-24; revalidated and executed 2026-07-29

**Mode:** Read-only. No Production environment, secret, deployment, alias,
domain, Git integration or project setting was created or changed.

The statement above describes the planning checkpoint. The separately
authorized release later completed; final evidence is in
`docs/VERIFICATION.md`.

## Project facts at the planning checkpoint

| Field | Verified value |
|---|---|
| Team | `gudvin82s-projects` |
| Plan | `hobby` |
| Project | `kan-open-research-lab` |
| Project state | `live: false` |
| Git integration | absent (`link: null`) |
| Stable project domain | `kan-open-research-lab.vercel.app` |
| Stable-domain state | verified; no Git branch binding |
| Current stable alias assignment | none |
| Accepted Preview | Ready and separately authentication-protected |

The exact stable domain was read from the current project-domain API. It was
not derived from naming convention. Other generated team/branch aliases are
not Production containment targets.

## CLI capability evidence

Installed Vercel CLI: `53.3.2`.

Read-only CLI help confirms:

- `--prod` is shorthand for `--target=production`;
- `--skip-domain` disables automatic Production promotion/aliasing and directs
  the operator to `vercel promote`;
- `vercel promote <deployment-id-or-url>` promotes an existing deployment;
- `vercel alias rm <alias> --yes` removes one alias assignment;
- `vercel alias set <deployment> <alias>` can explicitly restore an alias if a
  reviewed fallback is required.

The team API reports the Hobby plan. The current CLI and official Vercel
documentation expose deploy-without-alias, promote and alias management without
a paid-plan prerequisite. No paid resource is required by this flow.

Because the stable Production alias is currently unassigned, its removal was
not executed merely to prove the command. Immediately before a future
Production authorization, the operator MUST repeat this read-only inspection.
If the active plan or domain type no longer supports exact alias removal, the
release stops before deployment.

## Exact future command shapes

These are documentation, not authorization to execute.

### Stage Production without public alias

```text
vercel deploy --prod --skip-domain --yes \
  --scope gudvin82s-projects
```

### Promote only after immutable-URL verification

```text
vercel promote <verified-deployment-id-or-url> --yes \
  --scope gudvin82s-projects
```

### First-release containment

```text
vercel alias rm kan-open-research-lab.vercel.app --yes \
  --scope gudvin82s-projects
```

### Restore after a corrected staged deployment

```text
vercel promote <new-verified-deployment-id-or-url> --yes \
  --scope gudvin82s-projects
```

No token, secret, bypass value or environment value belongs in these commands,
Git, PR text or retained logs.

## Revalidation gate

Before separate Production authorization:

1. confirm the Vercel CLI version and help text again;
2. confirm team plan and project identity;
3. confirm Git integration remains absent;
4. confirm the exact stable domain remains verified and branch-unbound;
5. confirm it is not already assigned to an unexpected deployment;
6. confirm `--skip-domain`, promote, exact alias removal and restoration;
7. record command shapes without credentials;
8. confirm Production `noindex, nofollow` implementation and tests;
9. create no Production secret until the owner authorizes the release stage.

## Release execution addendum

The release revalidated local Vercel CLI `53.3.2`, the Hobby scope,
project/team identity, absent Git link, exact stable alias and supported
stage/promote/alias-removal command shapes.

Production source SHA
`5939d25ac40dd9e9320dcafab735d53725944e5e` was deployed with explicit
`--prod --skip-domain` as `dpl_3ExyTTVtnEVwgu5x3HcBsBegE3mD`. The stable
`kan-open-research-lab.vercel.app` alias was unassigned during immutable
verification and was promoted only after every gate passed. It now points to
that verified deployment.

No database, worker, migration, custom domain, Git integration, automatic
deployment or paid resource was added.
