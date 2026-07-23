# Foundation Research

## Web runtime

**Decision:** CPython 3.13, Django 6.0, ASGI entrypoint
`src.config.asgi:application`, resolved by `uv`.

**Rationale:** Django 6 supports Python 3.12–3.14; 3.13 is already available
through `uv` and avoids the prohibited macOS system Python 3.9.

**Rejected:** system Python 3.9; Python 3.14 without need; lowering web runtime
for future ML compatibility.

## Research runtime

**Decision:** dependency-free worker with `requires-python = ">=3.12,<3.14"`
and independent lock; exact minor follows the KAN compatibility spike.

## Database

**Decision:** PostgreSQL 17 in local Compose; external TLS PostgreSQL contract
for Vercel/server. Local, Preview and Production credentials are distinct.
Preview without DB uses liveness plus unavailable readiness.

## Health

**Decision:** `/health/live/` has no dependency checks; `/health/ready/` runs
`SELECT 1` with a short failure path; compute status reports typed
unavailability until a future worker heartbeat feature.

## Static files

**Decision:** collect static during build and serve via WhiteNoise. Migrations
are never a build or Preview-startup command.

## Logging and supply chain

**Decision:** standard-library JSON logs with conservative redaction; exact
dependency locks; pinned CI actions; fixed Docker tags/digests where verified;
dependency and secret scans.

## Backup

**Decision:** custom-format `pg_dump`, SHA-256 sidecar and guarded restore into
database names containing `test` or `local`. No production schedule/storage.

## Local runtime

**Decision:** Colima and Docker CLI via Homebrew. No system security changes or
administrator-password automation.

## Deferred

Managed PostgreSQL/pooler/Preview branching, Vercel linking/domains/env values,
object storage, and exact research Python/KAN dependency matrix.
