# KAN Open Research Lab

Предпроектная рабочая область открытой русскоязычной исследовательской и
образовательной лаборатории KAN/MLP/PINN.

Статус: **Этап 0 — предпроектный аудит**. Реализация платформы ещё не начата.

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
- [черновик спецификации Foundation](specs/001-foundation/spec.md);
- [аудит репозиториев и протоколов](docs/REPOSITORY_AUDIT.md);
- [ADR архитектуры MVP](docs/adr/0001-mvp-architecture.md);
- [модель угроз](docs/THREAT_MODEL.md);
- [направление дизайн-системы](docs/DESIGN.md);
- [концептуальная модель данных](docs/DATA_MODEL.md).

## Текущий режим

Локальная разработка на Mac. Проверка 23 июля 2026 года показала: TCP/22
целевого сервера доступен, но SSH зависает до banner; HTTP не отвечает.
Развёртывание и любые изменения сервера отложены до восстановления доступа.

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
