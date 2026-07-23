# Implementation Plan: Foundation

**Branch:** `codex/foundation` | **Date:** 2026-07-23 |
**Spec:** [spec.md](spec.md)

## Summary

Создать минимальный Django 6/PostgreSQL web на Python 3.13 с отдельным
standard-library research-worker skeleton, двумя lock-файлами, локальным
Docker Compose под Colima, безопасными health contracts, CI, backup/restore
drill и Vercel-compatible ASGI config. Production resources не создаются.

## Technical Context

**Language/Version:** web CPython 3.13; research `>=3.12,<3.14` until spike  
**Primary Dependencies:** Django 6.0, psycopg 3, WhiteNoise; worker stdlib only  
**Storage:** PostgreSQL 17 local; managed PostgreSQL deferred  
**Testing:** pytest, pytest-django, Django checks, Ruff, mypy, pip-audit  
**Target Platform:** Vercel Python Function for web; Linux server for worker;
macOS/Colima for local development  
**Project Type:** modular Django monolith plus isolated Python worker  
**Performance Goals:** dependency-failure health response under 2 seconds;
Foundation idle resource use recorded  
**Constraints:** no system Python 3.9; no ML in web; no queue; no migrations in
Vercel build; no production resources; worker ≤4 GiB RAM, ≤5 CPU, ≤256 PID  
**Scale/Scope:** one web process, one local PostgreSQL, one no-op worker

## Constitution Check

*Gate before research: PASS. Re-check after design: PASS.*

- I–IV: no scientific publication or claim is introduced.
- V: endpoints are read-only; worker is bounded and receives no web secret.
- VI: only Django/PostgreSQL/worker; no Redis/Kubernetes/vector DB.
- VII: Foundation exposes operational JSON only; UI is a later feature.
- VIII: spec, plan, checklist, tasks and verification evidence precede PR.

## Project Structure

```text
specs/001-foundation/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/health.openapi.yaml
├── checklists/requirements.md
└── tasks.md

manage.py
pyproject.toml
uv.lock
.python-version
src/
├── config/
│   ├── asgi.py
│   ├── urls.py
│   └── settings/
└── core/
    ├── logging.py
    ├── urls.py
    └── views.py
tests/
├── contract/
├── integration/
└── unit/
research_engine/
├── pyproject.toml
├── uv.lock
├── Dockerfile
└── src/kan_worker/
Dockerfile
compose.yaml
compose.worker.yaml
vercel.json
scripts/
├── backup_db.sh
├── restore_db.sh
└── smoke-check.sh
```

**Structure Decision:** root Django project remains Vercel-compatible; research
worker is a second Python project with an independent dependency graph/image.
This is the smallest trust boundary without a microservice platform.

## Delivery Phases

1. Bootstrap two deterministic Python projects.
2. Implement tested health, settings and logging contracts.
3. Add Compose isolation, backup/restore and Vercel config.
4. Run CI-equivalent, restore and resource checks; record evidence.
5. Converge against spec and open a draft PR.

## Complexity Tracking

No constitution violations require exceptions.
