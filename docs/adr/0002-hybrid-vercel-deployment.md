# ADR-0002: гибридное размещение Vercel + research server

**Статус:** accepted
**Дата:** 2026-07-23
**Заменяет:** ADR-0001 в части production deployment

## Контекст

Публичный сайт должен оставаться доступным независимо от состояния
вычислительного сервера. GitHub PR должны получать Preview Deployment, а
защищённая `main` — production deployment. Длительные KAN/MLP/PINN jobs,
PyTorch и тяжёлые артефакты не подходят для web function и остаются на
отдельном research node.

Создание платных ресурсов, production database/storage и реальный deploy
требуют отдельного подтверждения владельца.

## Решение

| Поверхность | Размещение |
|---|---|
| Django public web и admin | Vercel Python Function |
| PR Preview | Vercel Git integration |
| Production web | Vercel только из защищённой `main` |
| PostgreSQL | внешний managed PostgreSQL по TLS |
| Публичные малые артефакты | Vercel Blob или S3-compatible object storage |
| Research worker | отдельный server node |
| Heavy/private artifacts | private server/object storage, не GitHub |
| Local development | Mac, `uv`, Colima, Docker Compose |

Web использует Python 3.13 и Django 6.0 с отдельным lock-файлом. Research
Python и lock выбираются только после compatibility spike; web security
baseline не понижается ради ML dependencies.

## Trust boundaries

```text
Internet
  → Vercel edge/function (Django web/admin)
  → TLS managed PostgreSQL
  → public object storage (reviewed artifacts only)

Research server
  → TLS PostgreSQL using worker-only role
  → private artifact storage
  → reviewed export/publish boundary
```

Vercel web-role и server worker-role имеют разные credentials и минимальные
права. Worker не получает Django `SECRET_KEY`, admin session secrets, Vercel
token или production deployment credentials. Web не получает server SSH keys.

## Database environments and migrations

- Production, Preview и local используют разные databases/branches и roles.
- Preview никогда не получает production `DATABASE_URL`.
- Vercel build и Preview startup никогда автоматически не выполняют
  `migrate`.
- Schema migration выполняется отдельным gated release job с backup,
  compatibility check и rollback/forward-fix plan до production promotion.
- До выбора managed provider Foundation предоставляет только contracts,
  `.env.example` и local PostgreSQL.
- PR без выделенной Preview DB работает в `preview-no-db` режиме: liveness
  доступен, readiness возвращает unavailable без утечки connection details.

## Worker availability contract

Web хранит/получает health state вычислительного узла отдельно от собственного
health. При недоступном worker:

- публичные read-only страницы продолжают работать;
- enqueue/start возвращает typed `compute_node_unavailable`;
- admin видит время последнего heartbeat;
- задания не маскируются как запущенные;
- автоматический fallback выполнения на Vercel запрещён.

Foundation реализует только skeleton/status contract, не очередь.

## Artifacts

- Metadata и SHA-256 хранятся в PostgreSQL.
- Public artifact публикуется только после review и копируется в public bucket.
- Private/heavy artifacts остаются в private storage с retention policy.
- Object keys content-addressed; bucket listing закрыт; signed URL ограничен
  временем и scope.
- GitHub хранит только малые reproducible configs/manifests, не binary results,
  checkpoints, private datasets или raw internal logs.

## Backup boundaries

- Managed PostgreSQL: provider-native point-in-time recovery после отдельного
  выбора тарифа плюс независимый logical dump.
- Public object storage: versioning/retention и inventory checksum.
- Private research storage: отдельная off-host copy.
- GitHub не является backup базы или экспериментальных артефактов.
- Backup считается действующим только после restore drill.

Foundation создаёт local dump/restore scripts и runbook; production schedule и
storage не создаются без подтверждения владельца.

## Resource boundaries

Vercel resource limits относятся только к web function. ML imports и heavy CPU
work запрещены в web lock и deployment bundle. Для server worker сохраняется
budget ADR-0001: один job, до 3.5–4 ГБ RAM, до 5 CPU и disk watermark 10 ГБ.

## Последствия

Плюсы: web не зависит от research server, PR получают isolated Preview,
production deployment связан с `main`. Минусы: появляется сетевой trust
boundary, managed DB/object storage, connection pooling и раздельный backup.
Стоимость и provider lock-in контролируются отдельным approval gate.

## Запрещённые shortcut

- ML worker в Vercel Functions;
- Preview с production DB credentials;
- migrations из Vercel build;
- shared superuser DB role;
- public storage для private/raw artifacts;
- платный resource provisioning без подтверждения.
