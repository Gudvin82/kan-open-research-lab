#!/usr/bin/env bash
set -euo pipefail

base_url="${BASE_URL:-http://127.0.0.1:8000}"

curl --fail --silent --show-error "${base_url}/health/live/" >/dev/null
curl --fail --silent --show-error "${base_url}/health/ready/" >/dev/null

status="$(curl --silent --output /dev/null --write-out '%{http_code}' \
  "${base_url}/api/v1/system/compute-status/")"
if [[ "$status" != "503" ]]; then
  echo "Expected compute status 503, got ${status}" >&2
  exit 1
fi

echo "Foundation smoke check passed"
