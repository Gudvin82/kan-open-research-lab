# Аудит репозиториев, процесса и окружения

**Дата проверки:** 2026-07-23
**Глубина VCP-аудита:** partial/strong, не full
**Режим сервера:** read-only probe; изменений нет

## Executive summary

Single-host решение заменено ADR-0002: web/admin размещаются на Vercel,
research worker — на отдельном server node, PostgreSQL — managed external.
Главные риски: зрелость/застой KAN-реализаций, сетевые trust boundaries, раздельная
совместимость Python окружений, собственная PostgreSQL queue, научный
publication workflow и изоляция worker.

Не устанавливать pykan/efficient-kan до воспроизводимого dependency spike.
Обе реализации разрешены лицензией MIT, но efficient-kan не имеет релизов и
долго не обновлялся; его следует pin по commit и считать experimental до
regression benchmark.

## Локальное окружение

| Проверка | Результат |
|---|---|
| Рабочая папка | большая общая dirty worktree; новый проект изолирован |
| System Python | 3.9.6; запрещён для проекта |
| uv | 0.11.7 |
| uv Python | CPython 3.13.13 установлен |
| Git | 2.54.0 |
| Docker/Compose | не обнаружен |
| Colima | не обнаружен; выбран владельцем |
| psql | не обнаружен |
| VCP local | clean, release v0.9.5, commit `7d8cd2b...` |
| VCP remote | та же release v0.9.5, но remote branch новее local |

Вывод: web Foundation использует uv-managed Python 3.13, local PostgreSQL —
Colima + Docker Compose. Research Python выбирается позже. Обновлять соседний
VCP checkout ради этого проекта не нужно.

### Security observation вне нового проекта

В корневом `CLAUDE.md` общей рабочей папки обнаружена plaintext-строка,
похожая на рабочие PostgreSQL credentials. Значение не переносилось в новый
проект и не использовалось. До любого push общей папки или production-работ
нужно считать credential скомпрометированным: ротировать на сервере, удалить из
проектной памяти/истории доступным безопасным способом и выполнить secret scan.
Сам файл и соседние проекты этим аудитом не изменялись.

Ротация является blocking security action до production integration. Файл с
credential не входит в новый repository; значение не переносится в issue, PR,
logs, specs или project memory.

## Сервер

- оба известных IP принимают TCP/22;
- HTTP HEAD на оба адреса завершился timeout после 8 секунд;
- одна SSH-попытка к primary завершилась timeout during banner exchange;
- команды на сервере не выполнялись, состояние CPU/RAM/disk не подтверждено.

Решение: не делать повторные частые SSH-попытки из-за локально
задокументированного риска fail2ban. Продолжать на Mac; повторить единый
read-only audit после сообщения владельца о восстановлении.

## Spec Kit

Проверена актуальная официальная release `v0.14.0` от 2026-07-23. Применяем:

```text
constitution → specify → clarify → plan → checklist → tasks
→ analyze → implement → converge
```

Spec Kit владеет feature artifacts и cross-artifact consistency. Версия должна
быть pinned в Foundation, а не устанавливаться с плавающего `main`.

## Vibe Coding Protocols

Проверены entrypoints, two-track model, spec foundation, delivery lifecycle,
release readiness, target `AGENTS.md`, CLI classification и spec-depth helper.
VCP v0.9.5 корректно позиционирует себя как local-first governance/control
layer, не замену Spec Kit и не security certification.

### Что берём

- New Project + Spec-driven Adoption path;
- architecture/project memory;
- explicit stop conditions и change intent;
- dependency/third-party intake;
- backlog linkage;
- post-task review, PR Gate, release evidence/readiness;
- честное обозначение ограничений.

### Что не копируем

- root `AGENTS.md` VCP (он предназначен для аудита самого VCP);
- весь `.vcp` catalog/cards/dashboard;
- лимиты вида «>10 files всегда остановиться» как абсолютную продуктовую
  политику — используем scoped review gates;
- hosted/marketplace/optional layers;
- дублирующие PRD/spec templates.

### Конфликт с эвристикой

`vcp_cli spec depth` выдал `spec-lite`, не распознав публичные научные
утверждения, persistence, auth и isolated execution. Ручная классификация:
governed/full-spec. Это демонстрирует, что CLI — advisory evidence, не источник
решения. ТЗ и constitution имеют приоритет.

## Spec Kit ↔ VCP

| Область | Источник истины | Роль второго слоя |
|---|---|---|
| Constitution | Spec Kit | VCP проверяет governance evidence |
| Требования/clarify | Spec Kit | VCP route/spec-depth как подсказка |
| Plan/tasks | Spec Kit | VCP связывает backlog/architecture memory |
| Реализация | Spec Kit tasks | VCP change intent и review discipline |
| Cross-artifact analysis | Spec Kit analyze | VCP diagnostics дополняет repo-level gaps |
| Merge/release | VCP gates | Spec Kit acceptance/checklist как evidence |

Дублирование устраняется ссылками, а не копиями: одна constitution, один
feature spec, один task list.

## KAN dependency register

### pykan

- Repository: `KindXiaoming/pykan`
- License: MIT.
- Latest release: `v0.2.8` (2024-11-14).
- Checked head: `ecde4ec3274d3bef1ad737479cf126aed38ab530`
  (2025-01-19).
- Upstream requirements фиксируют старый/узкий стек, включая Python ≥3.9.7,
  NumPy 1.24.4, SymPy 1.11.1 и PyTorch 2.2.2.
- Сильные стороны: официальный reference, symbolic workflow, pruning/plots.
- Риски: CPU efficiency, большие notebook/docs assets, compatibility debt,
  автор прямо позиционирует код для малых scientific examples.
- Решение: **approved for isolated spike**, затем pin release/commit; не
  добавлять в web environment.

### efficient-kan

- Repository: `Blealtan/efficient-kan`
- License: MIT.
- Релизов нет.
- Checked head: `7b6ce1c87f18c8bc90c208f6b494042344216b11`
  (2024-07-03; repository pushed 2024-08-01).
- Pure PyTorch, B-spline implementation; меняет sparsification regularization
  относительно original KAN и сам отмечает необходимость дальнейших опытов.
- Сильные стороны: существенно более простой и memory-efficient path, tests.
- Риски: низкая активность, нет release, semantic differences from pykan.
- Решение: **experimental**, pin exact commit, vendor запрещён; повышение до
  approved только после tests, license notice и benchmark parity report.

### PyTorch MLP

- Обязательный внутренний baseline без стороннего KAN API.
- Архитектура, parameter budget, optimizer и training budget фиксируются до
  comparison.
- Решение: **approved conceptually**; версия PyTorch определяется общим
  research lock после compatibility spike.

## di-sukharev/vibe

Проверен как референс: Apache-2.0, Bun/Hono backend, React CSR webapp, Astro
public website, shared contracts, Compose, onboarding и тестовая дисциплина.
Текущий стек целиком не принимается: он создаст второй runtime-контур рядом с
Python research stack. Берём разделение public/private, contract thinking,
clean environment и validation patterns.

## Обязательный dependency spike перед Этапом 5

1. Создать отдельные clean environments на выбранных Python версиях.
2. Установить только pinned sources с hashes/commit.
3. Запустить upstream tests и минимальный CPU fit/predict.
4. Измерить install size, cold import, peak RAM/time.
5. Проверить save/load, deterministic seed и symbolic export.
6. Зафиксировать transitive licenses и vulnerability report.
7. Проверить единый adapter contract без сокрытия unsupported features.
8. Сохранить отчёт; не обновлять lock без regression suite.

## Решения владельца

Принято 2026-07-23:

- основной GitHub account: `Gudvin82`;
- repository: `Gudvin82/kan-open-research-lab`;
- в Git публикуются site/research source, Docker config, migrations, tests,
  docs, specs и reproducible experiment configs;
- secrets, personal data, private datasets, internal logs и heavy artifacts
  исключены;
- отдельные branches + Pull Request; deployable `main` защищён обязательным CI.
- hybrid deployment по ADR-0002;
- Colima для local containers;
- Python 3.13 для web через `uv`;
- никаких paid/prod Vercel, database или storage resources без approval.

До production остаются: ротация обнаруженного credential, финальное название,
домен, email, legal
owner/jurisdiction, code/content/data licenses, analytics, off-host backup и
retention, managed PostgreSQL/object storage providers и платный budget.
