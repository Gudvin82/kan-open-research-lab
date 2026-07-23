# Quickstart and Verification: Design System + Bilingual Public Shell

These commands reproduce the implementation and acceptance checks. Immutable
results for the tested implementation commit are recorded in
`docs/VERIFICATION.md`.

## Local server

```bash
uv sync --locked --group dev
uv run python manage.py check
uv run python manage.py runserver 127.0.0.1:8001
```

Expected:

- `/` redirects to `/ru/`;
- all routes in `contracts/public-shell.md` return useful pages;
- web pages render without PostgreSQL and without a worker.

## Python checks

```bash
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pytest
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py check --deploy --fail-level WARNING \
  --settings=src.config.settings.production
```

Expected: all pass and no migration is created for this feature.

## Browser checks

```bash
npm ci
npx playwright install --with-deps chromium
npm run test:ui
npm run capture:ui-evidence
```

Expected:

- all five primary pages pass in RU and EN;
- language switch preserves page identity;
- no critical/serious axe findings;
- 320 px and desktop journeys have no page-level overflow;
- keyboard and reduced-motion tests pass.

Automated accessibility results do not replace the manual review in
`checklists/ux-accessibility.md`.

Visual evidence is written to ignored `artifacts/ui-evidence/`; the PNG files
must not be committed.

## Vercel configuration inspection

```bash
rg -n -i 'migrate|research_engine|kan_worker|DATABASE_URL' \
  vercel.json pyproject.toml
uv run pytest tests/contract/test_vercel_config.py
```

Expected:

- no automatic migration or worker command;
- no secret value;
- build performs static collection only.

## Real Preview acceptance gate

Run only after the owner separately approves Vercel project linking:

1. Link the local checkout to the approved free Vercel project without enabling
   Git integration or automatic deployments.
2. Add a random `DJANGO_SECRET_KEY` only for Preview. Do not add
   `DATABASE_URL`, worker credentials or server credentials.
3. Build and deploy with explicit `--target preview`; never use `--prod`.
4. Test protected deployments with `vercel curl` or an automation-bypass value
   held only in process memory, never in Git, logs or browser artifacts.
5. Record the immutable deployment URL, commit SHA and results of route,
   language, accessibility and no-migration checks in `docs/VERIFICATION.md`.

No database or paid resource is required for this shell Preview.

## Safe local shutdown

```bash
docker compose -f compose.yaml -f compose.worker.yaml stop
colima stop
```

Do not use `down --volumes`, `docker volume prune` or `colima delete`.
