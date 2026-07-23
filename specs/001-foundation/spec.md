# Feature Specification: Foundation

**Feature Branch:** `codex/foundation`
**Created:** 2026-07-23
**Status:** Approved after Stage 0 merge

## Context

Foundation создаёт пустой, но production-shaped каркас лаборатории. Он
поднимается на Mac без системного Python, переносится в Vercel как лёгкий
Django web и сохраняет research worker отдельным, недоступным по умолчанию
узлом. На этом этапе нет научных моделей или публичного контента.

## User Scenarios & Testing

### User Story 1 — Локальный web-каркас (Priority: P1)

Разработчик на чистом локальном окружении поднимает Django/PostgreSQL, проверяет
health, тесты, настройки безопасности и backup skeleton без research ML stack.

**Independent Test:** после `docker compose up --build` liveness отвечает 200,
readiness отвечает 200 при доступной БД, Django checks и tests проходят.

**Acceptance Scenarios:**

1. **Given** чистый clone и Colima, **When** выполнен quickstart, **Then** web и
   PostgreSQL healthy без системного Python 3.9.6.
2. **Given** web запущен, **When** PostgreSQL остановлен, **Then** liveness
   остаётся 200, readiness становится 503 и не раскрывает DSN.

### User Story 2 — Явно недоступный compute node (Priority: P1)

Пользователь получает честный typed status недоступного research node, при этом
web остаётся доступен и job не создаётся.

**Independent Test:** без worker compute endpoint возвращает 503 и стабильный
`compute_node_unavailable`, а liveness web остаётся 200.

**Acceptance Scenarios:**

1. **Given** worker не настроен, **When** запрошен compute status, **Then**
   возвращается безопасный публичный код ошибки.
2. **Given** worker остановлен, **When** проверяется liveness, **Then** web
   отвечает 200 независимо от worker.

### User Story 3 — Воспроизводимая инженерная поставка (Priority: P2)

Maintainer проверяет отдельные lock-файлы, CI/security gates,
Vercel-compatible config и backup/restore drill до Foundation PR.

**Independent Test:** CI-equivalent команды, backup/restore smoke test и
Vercel schema inspection проходят без deploy, secrets и production resources.

**Acceptance Scenarios:**

1. **Given** два Python-проекта, **When** проверяются locks, **Then** web не
   содержит ML dependencies, а worker не получает web secrets.
2. **Given** test PostgreSQL, **When** выполнены dump и restore, **Then**
   восстановленная БД проходит smoke query.
3. **Given** Vercel config без secrets, **When** выполнена schema inspection,
   **Then** migrations не являются build step.

## Edge Cases

- PostgreSQL недоступен при старте: процесс стартует, liveness работает,
  readiness безопасно возвращает 503.
- Worker отсутствует: web не пытается исполнять job локально.
- Preview без `DATABASE_URL`: разрешён документированный `preview-no-db`.
- Production settings без secret/hosts/database: startup fail closed.
- Backup target существует: script не перезаписывает его молча.
- Restore target не помечен как test/local: script отказывается работать.

## Scope

- Spec Kit v0.14.0, зафиксированный в репозитории;
- web: Python 3.13 через `uv`, Django 6.0, отдельный lock;
- research worker: отдельный skeleton/lock без KAN/MLP и без окончательного
  Python minor до compatibility spike;
- PostgreSQL через Colima + Docker Compose;
- `web`, `db`, `worker` skeleton; dev/test/prod settings;
- health/readiness, structured logging, CI, backup/restore runbook;
- Vercel-compatible config без project linking/deploy;
- worker-unavailable contract и Preview/Production DB isolation strategy.

## Out of Scope

- publication/knowledge graph models, KAN/MLP adapters и execution queue;
- публичная дизайн-система;
- production deployment, DB/storage provisioning и платные ресурсы.

## Requirements

### Functional Requirements

- **FR-001:** `docker compose up` MUST поднимать web и PostgreSQL локально.
- **FR-002:** health MUST различать жизнь процесса и готовность БД.
- **FR-003:** web MUST NOT импортировать PyTorch, pykan или efficient-kan.
- **FR-004:** worker image/lock MUST быть независим от web image/lock.
- **FR-005:** production settings MUST fail closed без обязательных
  secrets/hosts/database.
- **FR-006:** public endpoint MUST NOT раскрывать версии, stack traces,
  environment или connection details.
- **FR-007:** backup MUST создавать проверяемый PostgreSQL dump; restore drill
  MUST выполняться только в test/local database.
- **FR-008:** Vercel build/Preview MUST NOT выполнять migrations.
- **FR-009:** Preview MUST NOT использовать production DB credentials.
- **FR-010:** liveness MUST работать без worker; readiness MUST отдельно
  отражать DB.
- **FR-011:** compute status MUST сообщать `compute_node_unavailable`, не
  создавая и не запуская job.
- **FR-012:** system Python 3.9.6 MUST NOT использоваться.
- **FR-013:** structured logs MUST исключать secrets, DSN и персональные данные.
- **FR-014:** Compose MUST задавать CPU/RAM/PID/security ограничения worker.
- **FR-015:** CI MUST проверять format/lint, typing, tests, migration drift,
  dependencies, secrets и Django deployment settings.

### Success Criteria

- **SC-001:** clean clone разворачивается по quickstart не более чем за 15 минут
  после установки Colima/Docker CLI.
- **SC-002:** liveness отвечает 200 при остановленных DB и worker; readiness
  отвечает 503 не позднее 2 секунд при недоступной DB.
- **SC-003:** все обязательные CI-equivalent проверки проходят локально и в PR.
- **SC-004:** `manage.py check --deploy` не выдаёт неприемлемых warnings.
- **SC-005:** migration drift отсутствует.
- **SC-006:** восстановленная test database проходит smoke query.
- **SC-007:** Vercel config проходит schema/build inspection без deploy,
  migrations и secrets.
- **SC-008:** idle-потребление Compose измерено; worker limits не выше 4 GiB
  RAM, 5 CPU и 256 PID.

## Deferred Decisions

- managed PostgreSQL provider и Preview branching;
- public/private object storage provider;
- research Python minor после KAN compatibility spike;
- локальный порт, если 8000 конфликтует с другими проектами.
