#!/usr/bin/env bash
set -euo pipefail

target="${1:-}"
if [[ -z "$target" ]]; then
  echo "Usage: $0 PATH.dump" >&2
  exit 64
fi
if [[ -e "$target" || -e "${target}.sha256" ]]; then
  echo "Refusing to overwrite existing backup or checksum" >&2
  exit 73
fi

mkdir -p "$(dirname "$target")"
docker compose exec -T db sh -c \
  'pg_dump --format=custom --no-owner --no-privileges --username="$POSTGRES_USER" "$POSTGRES_DB"' \
  >"$target"
shasum -a 256 "$target" >"${target}.sha256"
echo "Backup and checksum created: ${target}"
