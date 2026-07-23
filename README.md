# KAN Open Research Lab

Предпроектная рабочая область открытой русскоязычной исследовательской и
образовательной лаборатории KAN/MLP/PINN.

Статус: **Foundation принят; Design System + Bilingual Public Shell находится
в draft PR реализации**.

**Основной репозиторий:** <https://github.com/Gudvin82/kan-open-research-lab>

## Миссия

Публиковать понятные и воспроизводимые вычислительные исследования, честно
отделяя известное знание, численное приближение, эмпирическую закономерность,
гипотезу и доказательство.

## Источник требований

- `TZ_KAN_Open_Research_Lab.md`, версия 1.0 от 21 июля 2026 года;
- исходный язык продукта — русский, обязательный второй язык — английский;
- до Foundation обязательны constitution, ADR, threat model, data model,
  repository audit и DESIGN direction.

## Принятый процесс

```text
Spec Kit: constitution → specify → clarify → plan → checklist → tasks
          → analyze → implement → converge

VCP:      intake/route → backlog/architecture memory → review evidence
          → PR Gate → release readiness
```

Spec Kit является источником структуры требований и планирования. Vibe Coding
Protocols (VCP) используется как дополнительный локальный слой контроля,
проверок и доказательств. ТЗ имеет приоритет над обоими.

## Что находится в репозитории сейчас

- [constitution](.specify/memory/constitution.md);
- [спецификация Этапа 0](specs/000-preproject-audit/spec.md);
- [утверждённая спецификация Foundation](specs/001-foundation/spec.md);
- [план и задачи Foundation](specs/001-foundation/plan.md);
- [спецификация bilingual public shell](specs/002-design-bilingual-shell/spec.md);
- [план и задачи bilingual public shell](specs/002-design-bilingual-shell/plan.md);
- [аудит репозиториев и протоколов](docs/REPOSITORY_AUDIT.md);
- [исходный single-host ADR](docs/adr/0001-mvp-architecture.md);
- [действующий hybrid deployment ADR](docs/adr/0002-hybrid-vercel-deployment.md);
- [модель угроз](docs/THREAT_MODEL.md);
- [направление дизайн-системы](docs/DESIGN.md);
- [концептуальная модель данных](docs/DATA_MODEL.md).

## Текущий режим

Локальная разработка выполняется на Mac через `uv` и Colima. Публичный Django
web/admin проектируется для Vercel; Preview создаются из PR, production — только
из защищённой `main`. Текущая оболочка database-free. Будущий PostgreSQL будет
внешним управляемым сервисом, но его выбор и production provisioning запрещены
без отдельного подтверждения владельца.

Research worker, PyTorch и длительные эксперименты на Vercel не выполняются.
Worker размещается отдельно только после самостоятельного этапа интеграции.
Факт доступности сервера не означает готовность worker control plane. Пока
интеграция не выполнена, публичный сайт продолжает работать и показывает
`compute_node_unavailable`.

## Локальный запуск публичной оболочки

Оболочка не требует PostgreSQL, worker или JavaScript:

```bash
uv sync --locked --group dev
uv run python manage.py runserver 127.0.0.1:8001
```

`/` перенаправляет на русский `/ru/`; английская версия доступна по `/en/`.
Команды Python- и browser-проверок находятся в
[quickstart этапа](specs/002-design-bilingual-shell/quickstart.md).

## Локальный запуск Foundation stack

Требуются Homebrew, `uv`, Colima, Docker CLI и Compose plugin. Системный
`/usr/bin/python3` 3.9.6 не используется.

```bash
cp .env.example .env
colima start --cpu 4 --memory 6 --disk 40
docker compose up --build --detach --wait
./scripts/smoke-check.sh
```

Worker запускается отдельно и не влияет на доступность web:

```bash
docker compose -f compose.yaml -f compose.worker.yaml up --build --detach worker
```

Полные команды проверок и backup drill находятся в
[Foundation quickstart](specs/001-foundation/quickstart.md).

## GitHub workflow

- `main` должна оставаться развёртываемой;
- содержательные изменения выполняются в отдельных ветках через Pull Request;
- merge разрешён только после обязательных CI-проверок и review;
- source, migrations, tests, specs, docs и воспроизводимые конфигурации
  экспериментов хранятся в Git;
- secrets, персональные данные, приватные datasets, внутренние logs и тяжёлые
  artifacts в Git не добавляются.

## Заблокировано до решения владельца

- финальное название и домен;
- публичный email и юридический владелец;
- лицензии кода, текстов и данных;
- политика аналитики/cookie;
- внешнее backup-хранилище и сроки хранения артефактов.
- конкретный managed PostgreSQL и object storage;
- production Vercel project и любые платные ресурсы.
