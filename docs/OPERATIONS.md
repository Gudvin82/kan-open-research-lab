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

## Safe local shutdown

`docker compose -f compose.yaml -f compose.worker.yaml stop` followed by
`colima stop` preserves containers, named volumes and database data. Plain
`docker compose ... down` also preserves named volumes, but removes containers
and the project network. Operators must not use `down --volumes`,
`docker volume prune` or `colima delete` during normal shutdown.

## Production connection blocker

The credential reported in the external workspace `CLAUDE.md` is not present
in this repository. It must be rotated before any connection to that legacy
database, production deployment on the research server, or worker integration.
Rotation must update the consuming service secret atomically and include a
restart/health check; Foundation does not perform or automate it.

This blocker does not apply to a database-free Vercel Preview or public shell
that neither uses nor receives that credential. Any legacy database, worker or
research-server production connection remains forbidden until rotation.
