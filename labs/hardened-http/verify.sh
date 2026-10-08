#!/usr/bin/env bash
# Local end-to-end check. Requires docker, docker compose and curl.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FILE="$ROOT/compose.yaml"
cleanup() { docker compose -f "$FILE" down --remove-orphans >/dev/null 2>&1 || true; }
trap cleanup EXIT

python3 -m unittest discover -s "$ROOT/tests" -v
docker compose -f "$FILE" config --quiet
docker compose -f "$FILE" up --detach --build

echo "Waiting for loopback-only /health..."
for n in $(seq 1 25); do
  if curl --silent --fail --max-time 2 http://127.0.0.1:8080/health | grep -q '"status":"ok"'; then
    break
  fi
  if [ "$n" -eq 25 ]; then echo "FAIL: healthcheck"; exit 1; fi
  sleep 1
done

uid="$(docker compose -f "$FILE" exec -T web id -u)"
test "$uid" = "10001" || { echo "FAIL: wrong UID ($uid)"; exit 1; }
docker compose -f "$FILE" exec -T web sh -c 'if touch /app/security-probe 2>/dev/null; then exit 1; else exit 0; fi'
echo "PASS: health endpoint, non-root UID, read-only app dir and compose config"
