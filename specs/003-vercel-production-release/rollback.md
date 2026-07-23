# Rollback Plan: First Vercel Production Release

**Status**: Draft rehearsal plan; executing rollback or containment requires
separate owner authorization unless an already-authorized release is actively
failing its blocking checks.

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

## First-release limitation

At this planning checkpoint there is no earlier healthy, verified Production
deployment. The existing Production-target attempt
`dpl_DRbR6AZwZ29MMk4SH66xzeLa5A1z` is `ERROR`, never served the application
and is not eligible for rollback.

Therefore the first public release cannot honestly promise
rollback-to-previous. Before Production authorization, the owner must approve a
containment action supported and read-only-verified for the current Vercel
project, for example:

- remove or park the public Production alias; or
- disable the faulty deployment until a reviewed correction is available.

This document does not choose, execute or pre-authorize either action. If no
containment option has been explicitly approved, the first Production
deployment remains blocked.

## Stop conditions

Stop and request owner direction when:

- there is no verified predecessor and no approved containment action;
- Vercel asks to create a paid resource or change plan;
- an action would alter Preview protection, Git integration, domain, database
  or worker configuration;
- the CLI proposes a deployment rather than an alias rollback;
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
