#!/usr/bin/env bash
#
# Regenerate `packages/dhis2-client/src/dhis2_client/generated/v{N}` for each
# DHIS2 version passed (default: 40 41 42 43).
#
# For every version, spins up a fresh empty DHIS2 N via docker, waits for
# readiness, runs `dhis2-codegen generate` against it, and tears the stack
# down before moving on. The committed v42 e2e dump is swapped out for a
# 20-byte empty-gzip placeholder for the duration so DHIS2's Flyway
# migrations run cleanly on every version (loading a v42 dump into a v40
# stack would break).
#
# On exit — success, failure, or Ctrl+C — the script always restores the
# original `dhis.sql.gz` and brings the stack down, so there's no silent
# drift in the working tree.
#
# Usage:
#   infra/scripts/codegen_all_versions.sh            # default set
#   infra/scripts/codegen_all_versions.sh 42 43      # subset
#
# Expect ~8-12 minutes per version (pull + boot + schema migrate + codegen
# + teardown). Pre-pull images with `make -C infra pull DHIS2_VERSION=N`
# beforehand if you want to shave a few minutes off the first run.

set -euo pipefail

DEFAULT_VERSIONS=(40 41 42 43)
if [ "$#" -gt 0 ]; then
  VERSIONS=("$@")
else
  VERSIONS=("${DEFAULT_VERSIONS[@]}")
fi

INFRA_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$INFRA_DIR/.." && pwd)"
DUMP="$INFRA_DIR/dhis.sql.gz"
BACKUP="$INFRA_DIR/dhis.sql.gz.codegen-backup"

cleanup() {
  echo
  echo ">>> Cleaning up: stopping stack + restoring committed dump"
  make -C "$INFRA_DIR" down >/dev/null 2>&1 || true
  if [ -f "$BACKUP" ]; then
    mv -f "$BACKUP" "$DUMP"
    echo "    restored $DUMP"
  fi
}
trap cleanup EXIT INT TERM

# Swap the committed dump out for an empty placeholder. Loading a v42 dump
# into a v40 stack would fail schema migrations; empty lets DHIS2 bootstrap
# its own schema via Flyway on first start.
if [ -f "$DUMP" ] && [ ! -f "$BACKUP" ]; then
  mv "$DUMP" "$BACKUP"
  echo ">>> Backed up committed dump -> $BACKUP"
fi
printf '' | gzip -9 > "$DUMP"

FAILED=()
for v in "${VERSIONS[@]}"; do
  echo
  echo "============================================================"
  echo ">>> DHIS2 $v"
  echo "============================================================"

  if ! make -C "$INFRA_DIR" up-fresh DHIS2_VERSION="$v"; then
    echo "!!! failed to bring up DHIS2 $v (image missing from Docker Hub?)"
    FAILED+=("v$v:up")
    continue
  fi

  if ! make -C "$INFRA_DIR" wait; then
    echo "!!! v$v did not become ready in time"
    FAILED+=("v$v:wait")
    make -C "$INFRA_DIR" down >/dev/null 2>&1 || true
    continue
  fi

  echo ">>> running codegen for v$v"
  if (cd "$REPO_ROOT" && uv run dhis2-codegen generate \
        --url http://localhost:8080 --username admin --password district); then
    echo ">>> done with v$v"
  else
    echo "!!! codegen failed for v$v"
    FAILED+=("v$v:codegen")
  fi

  make -C "$INFRA_DIR" down >/dev/null 2>&1 || true
done

echo
echo "============================================================"
if [ "${#FAILED[@]}" -eq 0 ]; then
  echo ">>> All versions generated successfully: ${VERSIONS[*]}"
  exit 0
fi
echo ">>> Finished with failures: ${FAILED[*]}"
exit 1
