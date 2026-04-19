#!/usr/bin/env bash
# `dhis2 dev codegen` — regenerate the typed client from a DHIS2 instance.
# Three subcommands, two source-of-truth paths.
set -euo pipefail

export DHIS2_URL="${DHIS2_URL:-http://localhost:8080}"
export DHIS2_USERNAME="${DHIS2_USERNAME:-admin}"
export DHIS2_PASSWORD="${DHIS2_PASSWORD:-district}"

# --- /api/schemas path (metadata resources) -----------------------------------

# Online: hit a live instance and write generated/v{N}/schemas/ + enums.py +
# resources.py + schemas_manifest.json. Version is derived from /api/system/info.
dhis2 dev codegen generate --url "$DHIS2_URL" --username "$DHIS2_USERNAME" --password "$DHIS2_PASSWORD"

# Offline: re-run the emitter against every committed schemas_manifest.json.
# Useful after touching templates or the mapping logic — no network needed.
dhis2 dev codegen rebuild

# Offline, single version:
dhis2 dev codegen rebuild --manifest packages/dhis2-client/src/dhis2_client/generated/v42/schemas_manifest.json

# --- /api/openapi.json path (instance-side shapes) ----------------------------

# Offline: regenerate generated/v{N}/oas/ from each committed openapi.json.
# Covers every `components/schemas` entry — WebMessage envelopes, tracker
# read/write, DataValue, AuthScheme leaves, DataIntegrity*, SystemInfo, etc.
dhis2 dev codegen oas-rebuild

# Offline, single version — useful when iterating on oas_emit.py / its templates.
dhis2 dev codegen oas-rebuild --version v42
