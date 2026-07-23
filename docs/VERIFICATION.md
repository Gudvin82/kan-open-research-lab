# Foundation Verification

**Date:** 2026-07-23  
**Environment:** macOS, uv CPython 3.13.13, Colima 0.10.3, Docker CLI 29.6.2,
Docker Engine 29.5.2, Compose 5.3.1

**Verified commit:** `a1be6fad46a0fdd97588bb15dae9a513f72700b1`

## GitHub Actions evidence

| Workflow / job | Result | Run |
|---|---|---|
| Governance / `governance` | PASS | [30024471563](https://github.com/Gudvin82/kan-open-research-lab/actions/runs/30024471563) |
| Quality / `python` | PASS | [30024472074](https://github.com/Gudvin82/kan-open-research-lab/actions/runs/30024472074) |
| Quality / `secrets` | PASS | [30024472074](https://github.com/Gudvin82/kan-open-research-lab/actions/runs/30024472074) |

The earlier Governance run `30022711627` failed on `.env.example`; commit
`a1be6fa` corrected the overly broad path rule. The superseding run above is
green and is the evidence used for Foundation acceptance.

## Code and dependency gates

| Check | Result |
|---|---|
| `uv run ruff format --check .` | PASS, 26 files formatted |
| `uv run ruff check .` | PASS |
| `uv run mypy src` | PASS, 16 source files |
| `uv run pytest` | PASS, 14 tests |
| `manage.py makemigrations --check --dry-run` | PASS, no changes |
| `manage.py check` | PASS |
| production `manage.py check --deploy --fail-level WARNING` | PASS |
| `uv run pip-audit` | PASS, no known vulnerabilities |
| `uv lock --project research_engine --check` | PASS |

The first audit found `PYSEC-2026-1845` in pytest 8.4.2. The web lock was
updated to pytest 9.1.1; tests and audit then passed.

## Runtime contracts

- Pinned `python:3.13.5-slim-bookworm` web and worker images built.
- Pinned `postgres:17.5-alpine` started healthy.
- `/health/live/` and `/health/ready/` returned 200 with PostgreSQL available.
- With PostgreSQL stopped: liveness returned 200 and readiness returned 503.
- With worker stopped: the full web smoke check passed.
- Compute status returned typed HTTP 503 `compute_node_unavailable`.
- Worker log emitted only structured startup metadata and no secrets.
- Preview/Production database labels are fail-closed and covered by tests.

## Backup drill

`scripts/backup_db.sh` produced a custom-format dump and SHA-256 sidecar.
`scripts/restore_db.sh` verified the checksum, recreated
`kan_restore_test`, restored it and received `1` from its smoke query.
The unsafe target-name guard is covered by tests.

## Vercel inspection

- `vercel.json` parses as JSON and uses the official schema URL.
- Contract test validates the documented function fields, ASGI entrypoint and
  the absence of migration/deploy commands.
- The container build ran the same static collection boundary and copied 130
  static files; it did not run migrations during image build.
- No Vercel project was linked, no deploy was performed and no resource or
  secret was created.

The current official schema declares Draft 4 while containing newer numeric
`exclusiveMinimum` keywords, so generic Draft 4 validators cannot compile the
entire remote schema. The focused contract test covers every Vercel field used
by Foundation; provider-side build validation remains a later, separately
approved linking step.

## Secret and boundary checks

- Web dependency manifest contains no PyTorch, pykan or efficient-kan.
- Worker Compose receives neither `DJANGO_SECRET_KEY` nor database admin
  credentials and uses `network_mode: none`.
- Local Gitleaks 8.30.1 scanned the working tree (about 518 KB) and three Git
  commits with redaction enabled; no leaks were found.
- GitHub secret scanning/push protection remain enabled; PR CI adds Gitleaks.
- A plaintext database credential was found only in an external workspace
  `CLAUDE.md`. Its value was not copied to this repository, Git history, logs,
  issues or PRs. Rotation remains a mandatory blocker for connecting to that
  legacy database, worker integration and every production deployment to the
  research server. It does not block a database-free Vercel Preview or public
  shell when the credential is neither used nor supplied to Vercel.
