#!/usr/bin/env bash
# Metadata inspection + UID generation.
set -euo pipefail

# What DHIS2 metadata types does this instance expose?
dhis2 metadata type list

# --- List -----------------------------------------------------------------
# Default 50 rows, server-side page 1. `list` is also aliased as `ls`.
dhis2 metadata list dataElements --page-size 10

# Fields preset — `:identifiable` expands to `id,name,code,created,lastUpdated,displayName`.
# Other presets: `:nameable` (adds description), `:owner` (everything owned by the user), `:all`.
dhis2 metadata list dataElements --fields ":identifiable" --page-size 5

# Filter with the `property:operator:value` syntax. Repeat --filter for AND;
# pass --root-junction OR to OR them.
dhis2 metadata list dataElements \
  --filter "name:like:Penta" \
  --filter "code:eq:DE_PENTA1" \
  --root-junction OR \
  --fields "id,name,code"

# Order repeatable — later clauses tie-break.
dhis2 metadata list organisationUnits \
  --order "level:asc" --order "name:asc" \
  --fields "id,name,level" \
  --page-size 5

# --all streams every server-side page (paging=true + page=1,2,...).
# Useful for dumping a full catalog without knowing the total count upfront.
dhis2 metadata list indicators --all --fields ":identifiable" --json | jq 'length as $n | "\($n) indicators"'

# --- Get ------------------------------------------------------------------
# Fetch one seeded data element by UID.
dhis2 metadata get dataElements fClA2Erf6IO

# Fetch the Sierra Leone root OU.
dhis2 metadata get organisationUnits ImspTQPwCqd

# --- UIDs ------------------------------------------------------------------
# Generate fresh DHIS2 UIDs (11-char) via the dev tools — handy when scripting metadata creation.
dhis2 dev uid
dhis2 dev uid -n 5
