# Спецификация 000: предпроектный аудит

**Статус:** утверждено с поправками; закрывается merge PR #1
**Дата:** 2026-07-23
**Spec depth:** governed/full-spec (ручное решение; эвристика VCP ошибочно
предложила spec-lite)

## Цель

Снять критические неизвестные до Foundation и зафиксировать управляемую
архитектуру, научные правила, угрозы, данные, дизайн и зависимости.

## Результаты

1. Изолированная проектная папка, не смешанная с общей dirty worktree.
2. Constitution и проектные правила для агентов.
3. Сопоставление ТЗ, Spec Kit и VCP.
4. Предварительный аудит pykan, efficient-kan и MLP baseline.
5. ADR модульного Django-монолита и отдельного worker.
6. Threat model с security gates.
7. Концептуальная ER-модель до миграций.
8. DESIGN direction до массовой вёрстки.
9. Черновая спецификация Этапа 1.
10. Зафиксированные решения владельца и stop conditions.

## Не входит

- Django-код, контейнеры, миграции и установка ML-зависимостей;
- deploy или изменение существующего сервера;
- публикация научных текстов;
- выбор домена, юридических текстов и лицензий вместо владельца.

## Критерии приёмки

- [x] ТЗ прочитано полностью.
- [x] Локальные VCP-инструкции и CLI изучены на уровне partial/strong,
  достаточном для adoption decision.
- [x] Spec Kit проверен по актуальной официальной документации.
- [x] Доступность сервера проверена read-only.
- [x] Созданы constitution, ADR, threat model, data model и DESIGN direction.
- [x] Риски и неизвестные перечислены без молчаливых решений.
- [x] Владелец определил GitHub account `Gudvin82`, PR-only workflow и
  защищённый deployable `main`.
- [x] Владелец подтвердил документы Этапа 0.
- [x] Владелец выбрал hybrid Vercel/server deployment и Colima.
- [x] Владелец дал разрешение начать Foundation после merge поправок.

## Решение по процессу

Spec Kit управляет требованиями и реализацией. VCP v0.9.5 применяется
выборочно: architecture memory, backlog linkage, change intent, review
evidence, PR Gate и release readiness. Полное копирование VCP запрещено.

## Stop conditions перед Foundation

- не утверждена архитектура или scientific governance;
- не выбран способ получить PostgreSQL локально (Docker Desktop/Colima либо
  локальный PostgreSQL);
- требуется новая внешняя интеграция без intake;
- обнаружен конфликт лицензий;
- Foundation начинает включать research engine или production deploy.
