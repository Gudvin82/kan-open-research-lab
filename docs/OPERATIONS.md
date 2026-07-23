# Foundation Operations

## Health semantics

- `/health/live/`: process-only, no DB/worker check.
- `/health/ready/`: PostgreSQL dependency; safe 503 on failure.
- `/api/v1/system/compute-status/`: typed 503 until a future compute feature.

Alerts must not include response bodies, DSNs or environment values.

## Vercel boundary

Foundation provides config but does not link or deploy a Vercel project.
Production, Preview and local database credentials must be distinct. Builds
collect static files only; they never execute migrations. A future gated
release job owns migration/backup/rollback sequencing.

## Worker boundary

The worker container has no network in Foundation, receives no Django secret or
database admin credential, drops all capabilities and is limited to 4 GiB RAM,
5 CPU and 256 PID. Public web never falls back to local model execution.

## Incident-safe logging

Logs are JSON and redact common secret assignments and PostgreSQL DSN userinfo.
Do not log request headers, environment dumps, private datasets or raw internal
experiment output.
