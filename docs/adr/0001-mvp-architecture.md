# ADR-0001: архитектура MVP

**Статус:** superseded by ADR-0002
**Дата:** 2026-07-23

## Контекст

Нужны публичный двуязычный контентный сайт, закрытый admin workflow,
воспроизводимые CPU-эксперименты и строгая изоляция исполнения. Целевой сервер:
8 vCPU, 11 ГБ RAM (около 6 ГБ доступно), 96 ГБ disk (около 35 ГБ свободно),
без GPU. Поддерживает проект один владелец.

## Решение

- модульный Django-монолит с server-rendered templates;
- HTMX только для локальных интеракций, не как обязательная runtime-основа;
- PostgreSQL как БД, FTS и очередь через `FOR UPDATE SKIP LOCKED`;
- отдельный Python research worker и отдельный dependency lock/image;
- один worker job одновременно;
- локальные content-addressed artifacts с checksum и backup;
- Caddy как предпочтительный proxy нового изолированного deploy; Nginx
  допустим при интеграции в существующую серверную конфигурацию;
- Compose для локального и single-host production;
- GitHub Actions для CI;
- внутренний adapter contract для MLP, pykan и efficient-kan.

## Границы модулей

```text
public web/admin
  → content/publications/knowledge/search
  → research control plane (definitions, queue, review)
  → PostgreSQL

isolated worker
  → claims one allowlisted job
  → research_engine adapters
  → writes metrics/logs/artifacts through constrained interfaces
```

Web не импортирует ML-движки. Worker не имеет web secret, admin session key и
публичного upload path.

## Resource budget до smoke-test

| Компонент | RAM | CPU |
|---|---:|---:|
| web | 0.75 ГБ target, 1 ГБ limit | 1.5 |
| PostgreSQL | 0.75 ГБ target, 1 ГБ limit | 1 |
| worker | 3.5 ГБ limit | 5 |
| proxy/служебное | до 0.3 ГБ | 0.25 |
| системный резерв | не менее 1 ГБ | — |

Новый job блокируется при свободном диске ниже 10 ГБ. Артефакты получают
первичный бюджет 10 ГБ и policy-based retention.

## Отклонённые альтернативы

- Bun/Hono + React + Astro из `di-sukharev/vibe`: добавляет второй backend
  stack без пользы для MVP; берём только идеи контрактов, onboarding и тестов.
- Celery/Redis: лишний сервис при одном worker.
- Kubernetes: несоразмерен одному серверу.
- vector DB/RAG/local LLM: нет доказанной необходимости.
- публичные notebooks/code runner: нарушает модель угроз.
- один Python environment для web и ML: блокирует независимые security updates.

## Последствия

Плюсы: один основной язык, простое сопровождение, сильная транзакционная
модель, минимальный JS, отделённый риск ML. Минусы: очередь требует собственной
корректной реализации, тяжёлые расчёты ограничены одним host, будущий remote
runner потребует подписанного import protocol.

## Проверка решения

Foundation должен измерить cold start, idle RAM, DB RAM, response latency и
поведение web при 4 ГБ worker load. Изменение budget или добавление сервиса
требует нового ADR.

## Замена решения

После решения владельца использовать Vercel single-host deployment больше не
является целевой production-архитектурой. Сохранённые здесь ограничения worker
и server resource budget остаются входными данными для ADR-0002.
