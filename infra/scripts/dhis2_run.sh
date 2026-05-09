#!/usr/bin/env bash
#
# One-shot foreground DHIS2 runner:
#   1. start stack detached (so we can run the seed against a live instance)
#   2. block until /api/me responds
#   3. mint PATs + OAuth2 client into infra/home/credentials/.env.auth
#   4. stream logs — feels foreground
#   5. trap Ctrl+C so it tears the stack down on exit (no orphan containers)

set -euo pipefail

DHIS2_VERSION="${DHIS2_VERSION:-43}"
DHIS2_URL="${DHIS2_URL:-http://localhost:8080}"
DHIS2_USER="${DHIS2_USER:-admin}"
DHIS2_PASS="${DHIS2_PASS:-district}"

cd "$(dirname "$0")/.."
INFRA_DIR="$(pwd)"
COMPOSE=(docker compose -f compose.yml -f compose.pgadmin.yml)

cleanup() {
  echo
  echo ">>> Stopping DHIS2 stack ..."
  (cd "$INFRA_DIR" && DHIS2_VERSION="$DHIS2_VERSION" "${COMPOSE[@]}" down)
}
trap cleanup INT TERM

echo ">>> Starting DHIS2 $DHIS2_VERSION stack (detached) ..."
DHIS2_VERSION="$DHIS2_VERSION" "${COMPOSE[@]}" up -d --remove-orphans

echo ">>> Waiting for DHIS2 readiness ..."
make -C "$INFRA_DIR" wait DHIS2_URL="$DHIS2_URL" DHIS2_USER="$DHIS2_USER" DHIS2_PASS="$DHIS2_PASS"

echo ">>> Seeding PATs + OAuth2 client ..."
make -C "$INFRA_DIR" seed DHIS2_URL="$DHIS2_URL" DHIS2_USER="$DHIS2_USER" DHIS2_PASS="$DHIS2_PASS"

echo ">>> Ready. Streaming logs (Ctrl+C to stop the stack)."
DHIS2_VERSION="$DHIS2_VERSION" "${COMPOSE[@]}" logs -f dhis2 postgresql analytics-trigger
