# Foundation Quickstart

Prerequisites: Homebrew, `uv`, Colima, Docker CLI and Compose plugin. Do not use
`/usr/bin/python3` (3.9.6) or place real secrets in the repository.

```bash
cp .env.example .env
colima start --cpu 4 --memory 6 --disk 40
docker compose up --build --wait
curl --fail http://127.0.0.1:8000/health/live/
curl --fail http://127.0.0.1:8000/health/ready/
```

Compute status is expected to return HTTP 503:

```bash
curl --include http://127.0.0.1:8000/api/v1/system/compute-status/
```

CI-equivalent checks:

```bash
uv sync --locked --group dev
uv run ruff format --check .
uv run ruff check .
uv run mypy src
uv run pytest
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py check
```

Backup drill:

```bash
./scripts/backup_db.sh ./tmp/foundation.dump
RESTORE_DATABASE_NAME=kan_restore_test \
  ./scripts/restore_db.sh ./tmp/foundation.dump
```

Restore refuses database names without `test` or `local`.
