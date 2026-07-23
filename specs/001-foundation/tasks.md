# Tasks: Foundation

## Phase 1: Setup

- [X] T001 Pin web Python and dependencies in `.python-version`, `pyproject.toml`, and `uv.lock`
- [X] T002 [P] Create independent worker project in `research_engine/pyproject.toml` and `research_engine/uv.lock`
- [X] T003 [P] Complete secret/runtime exclusions in `.gitignore` and `.dockerignore`
- [X] T004 Create Django project skeleton in `manage.py` and `src/config/`

## Phase 2: Foundational

- [X] T005 Implement dev/test/production settings in `src/config/settings/`
- [X] T006 [P] Implement redacted JSON logging in `src/core/logging.py`
- [X] T007 [P] Define environment contract in `.env.example`
- [X] T008 Configure root routing and static middleware in `src/config/urls.py` and `src/config/settings/base.py`

## Phase 3: User Story 1 — Local web skeleton (P1)

**Goal:** local Django/PostgreSQL starts and reports independent liveness/readiness.

**Independent test:** Compose becomes healthy; DB stop leaves liveness 200 and readiness 503.

- [X] T009 [P] [US1] Write health contract tests in `tests/contract/test_health.py`
- [X] T010 [P] [US1] Write production fail-closed tests in `tests/unit/test_settings.py`
- [X] T011 [US1] Implement liveness and DB readiness in `src/core/views.py` and `src/core/urls.py`
- [X] T012 [US1] Create web image in `Dockerfile`
- [X] T013 [US1] Create bounded local PostgreSQL/web composition in `compose.yaml`
- [X] T014 [US1] Validate migration drift and local health in `scripts/smoke-check.sh`

## Phase 4: User Story 2 — Compute unavailable contract (P1)

**Goal:** compute status is explicit while public web availability remains independent.

**Independent test:** compute endpoint returns typed 503 and creates no job.

- [X] T015 [P] [US2] Write compute contract tests in `tests/contract/test_compute_status.py`
- [X] T016 [US2] Implement compute-unavailable endpoint in `src/core/views.py`
- [X] T017 [US2] Create no-op worker process in `research_engine/src/kan_worker/worker.py`
- [X] T018 [US2] Add worker image and bounded server override in `research_engine/Dockerfile` and `compose.worker.yaml`
- [X] T019 [US2] Verify web and worker environments are secret-isolated in `tests/integration/test_dependency_boundaries.py`

## Phase 5: User Story 3 — Reproducible delivery (P2)

**Goal:** CI, backup drill and Vercel configuration are reviewable without production resources.

**Independent test:** CI-equivalent checks, dump/restore and Vercel schema inspection pass.

- [X] T020 [P] [US3] Write backup/restore guard tests in `tests/integration/test_backup_scripts.py`
- [X] T021 [US3] Implement checked dump and guarded restore in `scripts/backup_db.sh` and `scripts/restore_db.sh`
- [X] T022 [P] [US3] Document restore and operations in `docs/BACKUP_RESTORE.md` and `docs/OPERATIONS.md`
- [X] T023 [P] [US3] Add Vercel entrypoint/build configuration in `pyproject.toml` and `vercel.json`
- [X] T024 [US3] Add quality/security workflow in `.github/workflows/quality.yml`
- [X] T025 [US3] Add repository secret scan policy in `.github/workflows/quality.yml`
- [X] T026 [US3] Update setup and architecture guidance in `README.md`

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T027 Run Ruff, mypy, pytest, Django checks and migration checks and record results in `docs/VERIFICATION.md`
- [X] T028 Run Compose health, DB failure and worker-independence scenarios from `specs/001-foundation/quickstart.md`
- [X] T029 Run backup/restore drill and record checksum/smoke evidence in `docs/VERIFICATION.md`
- [X] T030 Measure idle resource use and update `docs/adr/0002-hybrid-vercel-deployment.md`
- [X] T031 Audit repository/history for secrets and ML/web dependency leakage and record safe evidence in `docs/VERIFICATION.md`
- [X] T032 Run Spec Kit convergence and close any appended tasks in `specs/001-foundation/tasks.md`

## Dependencies

- Setup and Foundational phases block all user stories.
- US1 and US2 can proceed independently after Phase 2.
- US3 depends on US1 for a runnable database/web target.
- Polish depends on US1–US3.

## Parallel Opportunities

- T002–T003 can run beside T001 after paths are fixed.
- T006–T007 are independent.
- T009–T010 are independent tests written before implementation.
- T015 can run beside US1 implementation.
- T020, T022 and T023 touch independent files.

## Implementation Strategy

The first independently useful MVP is US1. US2 then proves the hybrid failure
boundary. US3 makes the result reproducible and PR-ready. Tests precede the
corresponding endpoint or script implementation.

## Phase 7: Convergence

- [X] T033 Enforce and test `DATABASE_ENV` separation in `src/config/settings/preview.py`, `src/config/settings/production.py`, `.env.example`, and `tests/unit/test_settings.py` per FR-009 (partial)
