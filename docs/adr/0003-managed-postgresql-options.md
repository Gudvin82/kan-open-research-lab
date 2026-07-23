# ADR-0003: варианты managed PostgreSQL

**Статус:** proposed, решение отложено
**Дата снимка:** 2026-07-23

## Контекст

Публичная оболочка текущего этапа не использует базу данных. До появления
публикационных моделей нужно выбрать внешний managed PostgreSQL, не связывая
доступность сайта с research server и не передавая Preview-деплоям Production
credentials.

Сравнение фиксирует доступные варианты, но не выбирает провайдера, тариф,
регион и не создаёт внешние ресурсы. Цены и ограничения меняются, поэтому перед
решением требуется повторная проверка официальных условий.

## Критерии

- стоимость минимального production-профиля и превышений квот;
- доступный EU-регион и место хранения резервных копий;
- backup, point-in-time recovery и проверяемый restore;
- физическая или логическая изоляция Preview от Production;
- лимиты соединений и поддержка pooling для serverless Django;
- отдельный контролируемый запуск миграций вне Vercel build/startup.

## Кандидаты

| Критерий | Neon | Supabase |
|---|---|---|
| Модель стоимости | Free и usage-based платные планы; итог зависит от compute, storage и transfer | План организации/проекта плюс usage; дополнительные функции и branching могут тарифицироваться отдельно |
| EU-регионы | Регион выбирается при создании проекта; конкретный EU-регион и доступность через выбранную интеграцию нужно подтвердить перед заказом | Документированы Frankfurt и другие отдельные AWS-регионы ЕС; точный регион фиксируется при создании проекта |
| Backups | Retention/time travel зависит от плана; перед выбором нужно зафиксировать окно и выполнить restore drill | Ежедневные backups на платных планах; retention зависит от плана, PITR является отдельной возможностью |
| Preview isolation | Database branches и интеграция Preview документированы; ветка должна получать отдельные credentials | Preview branches документированы; они должны оставаться отдельными от Production и не наследовать production data/credentials |
| Соединения | Нужна проверка лимитов direct/pooled connections и совместимости с serverless Django | Предоставляет direct и pooled endpoints; лимиты зависят от compute/плана |
| Объём продукта | PostgreSQL-ориентированный сервис | PostgreSQL вместе с Auth, Storage, Realtime и другими сервисами, которые сейчас не требуются |

Официальные источники снимка:

- [Neon pricing](https://neon.com/pricing)
- [Neon branching](https://neon.com/docs/guides/branching-intro)
- [Supabase regions](https://supabase.com/docs/guides/platform/regions)
- [Supabase backups](https://supabase.com/docs/guides/platform/backups)
- [Supabase branching](https://supabase.com/docs/guides/deployment/branching)

## Безопасный порядок миграций

Для обоих кандидатов применяется один контракт:

1. Preview использует только отдельную пустую/обезличенную database branch и
   отдельную роль.
2. CI проверяет миграции, но Vercel build и function startup их не запускают.
3. Production migration выполняется отдельным release job после backup,
   проверки совместимости и утверждения владельцем.
4. Deployment приложения выполняется только после успешной миграции; откат
   схемы не предполагается автоматически, заранее готовится forward-fix.
5. Restore drill и максимальное допустимое время восстановления фиксируются до
   подключения production-трафика.

## Решение

Решение не принято. Neon и Supabase остаются в shortlist. Выбор возможен только
в отдельном DB-backed этапе после актуализации цен, лимитов, EU data residency,
backup/restore и оценки реального Django connection profile.

## Последствия

Текущая database-free оболочка не получает `DATABASE_URL`, не создаёт managed
PostgreSQL и не меняет deployment boundary. Внешний credential, найденный вне
репозитория, продолжает блокировать старую БД, production на research server и
worker integration, но не относится к database-free оболочке.
