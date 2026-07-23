# Спецификация 001: Foundation

**Статус:** draft; реализация запрещена до подтверждения Этапа 0

## Пользовательская ценность

Разработчик может на чистом локальном окружении поднять пустой, но
production-shaped Django/PostgreSQL проект, проверить health, тесты,
безопасность конфигурации и backup skeleton без установки research ML stack в
web-контейнер.

## Scope

- отдельный Git-репозиторий проекта;
- Spec Kit v0.14.0, зафиксированный по версии;
- Python-версия выбирается по совместимости поддерживаемого Django и ML
  окружений; web и worker lock-файлы раздельны;
- Django, PostgreSQL, Compose, Caddy;
- `web`, `db`, `worker`-skeleton и `proxy`; worker ещё не запускает модели;
- dev/test/prod settings;
- health/readiness endpoints;
- CI: format, lint, typing, unit tests, migrations check, dependency/secret
  scan и `check --deploy`;
- `.env.example` без секретов;
- backup/restore skeleton и runbook;
- structured logging без секретов.

## Не входит

- модели публикаций и knowledge graph;
- KAN/MLP adapters;
- очередь выполнения;
- публичная дизайн-система;
- production deployment.

## Функциональные требования

- FR-001: `docker compose up` поднимает web и PostgreSQL локально.
- FR-002: health различает жизнь процесса и готовность БД.
- FR-003: web не импортирует PyTorch, pykan или efficient-kan.
- FR-004: worker image/lock независим от web image/lock.
- FR-005: production settings fail closed без обязательных secrets/hosts.
- FR-006: публичный endpoint не раскрывает версии, stack traces и environment.
- FR-007: backup-команда создаёт проверяемый PostgreSQL dump; restore drill
  документирован и тестируется в test database.

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

## Неизвестные для clarify

- Docker Desktop или Colima на Mac;
- поддерживаемая версия Python для web и отдельная для pykan;
- Caddy или уже принятый на сервере Nginx (ADR сейчас рекомендует Caddy для
  нового изолированного deploy, но существующая инфраструктура может изменить
  решение);
- GitHub owner/repository;
- локальный портовой диапазон, чтобы не конфликтовать с другими проектами.
