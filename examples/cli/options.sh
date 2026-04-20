#!/usr/bin/env bash
# OptionSet + Option workflows via `dhis2 metadata`.
# Two layers: the generic list/get surface (works for every resource) and
# the workflow-specific `metadata options show / find / sync` commands.
set -euo pipefail

# --- Workflow commands (dhis2 metadata options) ----------------------------
# Show one OptionSet with its options resolved inline. Accepts a UID or
# the set's business code — whichever you happen to have in hand.

dhis2 metadata options show VACCINE_TYPE
dhis2 metadata options show OsVaccType1 --json

# Pinpoint a single option inside a set by code (or by display name):
dhis2 metadata options find --set VACCINE_TYPE --code BCG
dhis2 metadata options find --set OsVaccType1 --name Measles

# Idempotent bulk sync from a JSON spec file. Spec is an array of
# `{code, name, sort_order?}` objects. `--dry-run` prints the diff
# without touching DHIS2; `--remove-missing` deletes options whose
# code isn't in the spec (off by default — safer for partial refreshes).

cat > /tmp/vaccine-spec.json <<'JSON'
[
  {"code": "BCG", "name": "BCG"},
  {"code": "MEASLES", "name": "Measles vaccine"},
  {"code": "POLIO", "name": "Polio"},
  {"code": "DPT", "name": "DPT"},
  {"code": "HEPB", "name": "Hepatitis B"},
  {"code": "HPV", "name": "HPV vaccine"}
]
JSON

dhis2 metadata options sync VACCINE_TYPE /tmp/vaccine-spec.json --dry-run
dhis2 metadata options sync VACCINE_TYPE /tmp/vaccine-spec.json

# Rollback to the original 5 options — remove HPV with --remove-missing,
# restore MEASLES to its original name:
cat > /tmp/vaccine-rollback.json <<'JSON'
[
  {"code": "BCG", "name": "BCG"},
  {"code": "MEASLES", "name": "Measles"},
  {"code": "POLIO", "name": "Polio"},
  {"code": "DPT", "name": "DPT"},
  {"code": "HEPB", "name": "Hepatitis B"}
]
JSON
dhis2 metadata options sync VACCINE_TYPE /tmp/vaccine-rollback.json --remove-missing

# --- Generic metadata surface (works for every resource) -------------------

dhis2 metadata list optionSets --fields 'id,code,name,valueType'
dhis2 metadata list optionSets \
    --filter 'code:eq:VACCINE_TYPE' \
    --fields 'id,code,name,valueType,options[id,code,name,sortOrder]'

# Every option in one set (server-side filter + sort-order):
dhis2 metadata list options \
    --filter 'optionSet.id:eq:OsVaccType1' \
    --order 'sortOrder:asc' \
    --fields 'id,code,name,sortOrder'

# Export a set as a metadata bundle — useful for moving between instances:
dhis2 metadata export \
    --resource optionSets \
    --resource options \
    --filter 'optionSets:code:eq:VACCINE_TYPE' \
    --output /tmp/vaccine-type.json

# dhis2 metadata import /tmp/vaccine-type.json --dry-run
