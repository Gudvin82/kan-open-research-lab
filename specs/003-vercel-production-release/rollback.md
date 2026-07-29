# Rollback Plan: First Vercel Production Release

**Status**: Rehearsed and retained for future releases. The first controlled
release succeeded without containment or rollback.

## Objective

Restore the last verified, immutable Production deployment without rebuilding
or introducing unreviewed code. Preserve failed deployments and logs as audit
evidence while preventing continued public exposure of a faulty release.

## Rollback triggers

Rollback or first-release containment is required when any of these occurs:

- Production source SHA differs from the approved protected-`main` SHA;
- repeated HTTP 500 or unusable cold starts;
- root, RU/EN primary routes or static assets fail;
- canonical/`hreflang` points at Preview or an unapproved host;
- Preview protection or Production public-access policy is wrong;
- a secret or sensitive value appears in HTML, headers or logs;
- any migration, PostgreSQL connection, worker or server activity occurs;
- security headers or `noindex, nofollow` fail;
- critical/serious accessibility regression blocks primary navigation;
- the deployment target is not unambiguously Production.

## Preconditions

Before the release command:

1. List recent Production deployments read-only.
2. Identify the latest deployment that is:
   - `READY`;
   - previously verified and recorded in `docs/VERIFICATION.md`;
   - associated with an accepted source SHA;
   - reachable through the expected Production project.
3. Record its immutable deployment ID and SHA as
   `<previous-ready-production-deployment-id>` and
   `<previous-ready-production-sha>`.
4. Confirm it is not the failed historical deployment
   `dpl_DRbR6AZwZ29MMk4SH66xzeLa5A1z`.
5. Rehearse the command shape without executing it.

If any identity is ambiguous, stop. Deployment names, aliases and project slugs
must not be guessed.

## Standard rollback when a known-good predecessor exists

1. Stop further deployments and configuration changes.
2. Capture the faulty deployment ID, source SHA, stable URL, failing check and
   time without copying secret values or raw logs.
3. Verify the predecessor is still `READY`.
4. Repoint Production using the exact verified predecessor:

   ```text
   vercel rollback <previous-ready-production-deployment-id> \
     --scope gudvin82s-projects
   ```

   The concrete command must be checked against the pinned CLI version before
   execution. Never substitute a branch name, mutable alias or Error
   deployment.
5. Confirm the stable Production alias resolves to the predecessor deployment
   and expected SHA.
6. Re-run critical checks:
   - anonymous stable-URL access;
   - `/` to `/ru/`;
   - RU/EN home, research and methods;
   - CSS/font assets;
   - canonical/`hreflang` and `noindex, nofollow`;
   - liveness, honest readiness and `compute_node_unavailable`;
   - security headers;
   - runtime HTTP 500 scan.
7. Record the faulty and restored deployment IDs, reason, time and check
   results in `docs/VERIFICATION.md`.
8. Leave the faulty deployment in history; do not delete audit evidence.

## First-release containment

At this planning checkpoint there is no earlier healthy, verified Production
deployment. The existing Production-target attempt
`dpl_DRbR6AZwZ29MMk4SH66xzeLa5A1z` is `ERROR`, never served the application
and is not eligible for rollback.

The selected containment is removal of the exact stable public alias:

```text
vercel alias rm kan-open-research-lab.vercel.app \
  --yes --scope gudvin82s-projects
```

The command removes the alias assignment only. It MUST NOT be replaced with
`vercel remove`, project-domain deletion or deployment deletion.

First-release containment procedure:

1. Stop promotion and every further deployment/configuration action.
2. Record the faulty deployment ID/SHA, failing check and time.
3. Reconfirm that
   `kan-open-research-lab.vercel.app` resolves to the faulty deployment.
4. Remove that exact alias assignment using the reviewed command above.
5. Confirm the public alias no longer routes to the faulty deployment.
6. Confirm the immutable deployment and logs remain available for audit.
7. Confirm the accepted Preview and project remain intact.
8. Correct code/configuration through a new PR.
9. Create a new staged Production deployment with `--prod --skip-domain`.
10. Repeat the complete immutable-URL suite.
11. Restore public service only by explicitly promoting the new verified
    deployment:

    ```text
    vercel promote <new-verified-deployment-id-or-url> \
      --yes --scope gudvin82s-projects
    ```

12. Repeat critical checks through the stable alias and record all evidence.

If preflight cannot prove that the exact alias is safely removable on the
active plan/domain type, do not deploy. Report the available alternative:
Deployment Protection or a separately reviewed maintenance/parking deployment.

## Current known-good Production baseline

After the successful 2026-07-29 release, future releases have one verified
rollback candidate:

- deployment ID: `dpl_3ExyTTVtnEVwgu5x3HcBsBegE3mD`;
- source SHA: `5939d25ac40dd9e9320dcafab735d53725944e5e`;
- immutable URL:
  `https://kan-open-research-aartziwfe-gudvin82s-projects.vercel.app`;
- stable alias: `https://kan-open-research-lab.vercel.app`;
- state at verification: Production / Ready / `iad1`.

Future rollback must re-inspect this deployment before use and repeat the
critical public checks after any alias movement.

## Stop conditions

Stop and request owner direction when:

- exact alias ownership or removability is not confirmed;
- Vercel asks to create a paid resource or change plan;
- an action would alter Preview protection, Git integration, domain, database
  or worker configuration;
- the CLI proposes deleting a deployment/project/domain rather than removing
  one alias assignment;
- the target deployment ID/SHA cannot be proven;
- rollback would expose a secret or require placing one in a command/log;
- rollback succeeds technically but critical smoke checks still fail.

## Evidence rules

Record only:

- deployment IDs and public URLs;
- exact source SHAs;
- timestamps and operator-approved reason;
- command shape without tokens or secret values;
- summarized/redacted check outcomes.

Do not commit Vercel tokens, bypass values, environment values, raw internal
logs, cookies, request dumps or private headers.
