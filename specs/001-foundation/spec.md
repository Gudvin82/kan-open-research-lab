# Спецификация 001: Foundation

**Статус:** approved после merge поправок Этапа 0

## Пользовательская ценность

Разработчик может на чистом локальном окружении поднять пустой, но
production-shaped Django/PostgreSQL проект, проверить health, тесты,
безопасность конфигурации и backup skeleton без установки research ML stack в
web-контейнер.

## Scope

- отдельный Git-репозиторий проекта;
- Spec Kit v0.14.0, зафиксированный по версии;
- web: Python 3.13 через `uv`, Django 6.0, отдельный lock;
- research worker: отдельный skeleton/lock без KAN/MLP и без фиксации
  окончательной Python minor до compatibility spike;
- PostgreSQL local development через Colima + Docker Compose;
- `web`, `db`, `worker` skeleton; worker ещё не запускает модели;
- dev/test/prod settings;
- health/readiness endpoints;
- CI: format, lint, typing, unit tests, migrations check, dependency/secret
  scan и `check --deploy`;
- `.env.example` без секретов;
- backup/restore skeleton и runbook;
- structured logging без секретов.
- Vercel-compatible Django entrypoint/config без project linking/deploy;
- worker-unavailable status contract;
- Preview/Production database isolation strategy.

## Не входит

- модели публикаций и knowledge graph;
- KAN/MLP adapters;
- очередь выполнения;
- публичная дизайн-система;
- production deployment.
- production DB/storage provisioning и платные Vercel resources.

## Функциональные требования

- FR-001: `docker compose up` поднимает web и PostgreSQL локально.
- FR-002: health различает жизнь процесса и готовность БД.
- FR-003: web не импортирует PyTorch, pykan или efficient-kan.
- FR-004: worker image/lock независим от web image/lock.
- FR-005: production settings fail closed без обязательных secrets/hosts.
- FR-006: публичный endpoint не раскрывает версии, stack traces и environment.
- FR-007: backup-команда создаёт проверяемый PostgreSQL dump; restore drill
  документирован и тестируется в test database.
- FR-008: Vercel build/Preview не выполняет migrations.
- FR-009: Preview не может использовать production DB credentials.
- FR-010: web liveness работает без worker; readiness отдельно отражает DB.
- FR-011: compute status сообщает `compute_node_unavailable`, не запуская job.
- FR-012: system Python 3.9.6 не используется.

## Acceptance criteria

- чистый clone разворачивается по README;
- все обязательные CI checks проходят;
- `manage.py check --deploy` не имеет неприемлемых предупреждений;
- web продолжает отвечать при остановленном worker;
- worker не получает Django secret key и admin credentials;
- Compose содержит CPU/RAM/PID/security ограничения как минимум в production
  override;
- migration drift отсутствует;
- восстановленная тестовая БД проходит smoke-check;
- фактическое потребление ресурсов измерено и внесено в ADR.
- Vercel configuration проходит schema/build inspection без deploy и secrets.
- отсутствие worker не делает public web unavailable.

## Неизвестные для clarify

- конкретный managed PostgreSQL provider и Preview branching;
- public/private object storage provider;
- research Python minor после KAN compatibility spike;
- локальный портовой диапазон, чтобы не конфликтовать с другими проектами.
