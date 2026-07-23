#!/usr/bin/env bash
set -euo pipefail

source_dump="${1:-}"
target_db="${RESTORE_DATABASE_NAME:-}"
if [[ -z "$source_dump" || -z "$target_db" ]]; then
  echo "Usage: RESTORE_DATABASE_NAME=kan_restore_test $0 PATH.dump" >&2
  exit 64
fi
if [[ "$target_db" != *test* && "$target_db" != *local* ]]; then
  echo "Refusing restore: target database must contain test or local" >&2
  exit 77
fi
if [[ ! -f "$source_dump" || ! -f "${source_dump}.sha256" ]]; then
  echo "Dump or checksum is missing" >&2
  exit 66
fi

shasum -a 256 -c "${source_dump}.sha256"
docker compose exec -T db dropdb --if-exists --force \
  --username="${POSTGRES_USER:-kan_local_app}" "$target_db"
docker compose exec -T db createdb \
  --username="${POSTGRES_USER:-kan_local_app}" "$target_db"
docker compose exec -T db pg_restore --exit-on-error --no-owner --no-privileges \
  --username="${POSTGRES_USER:-kan_local_app}" --dbname="$target_db" <"$source_dump"
docker compose exec -T db psql --tuples-only --no-align \
  --username="${POSTGRES_USER:-kan_local_app}" --dbname="$target_db" \
  --command="SELECT 1"
echo "Restore smoke check passed for guarded target"
