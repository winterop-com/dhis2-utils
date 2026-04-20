#!/usr/bin/env bash
# OptionSet + Option workflows via the generic `dhis2 metadata` surface.
# Covers what the CLI supports today — workflow-specific commands
# (`dhis2 metadata options show / find / sync`) land in the next PR.
set -euo pipefail

# --- Listing + filtering ----------------------------------------------------
# Every DHIS2 filter form works against the generic list endpoint.

dhis2 metadata list optionSets --fields 'id,code,name,valueType'
dhis2 metadata list optionSets \
    --filter 'code:eq:VACCINE_TYPE' \
    --fields 'id,code,name,valueType,options[id,code,name,sortOrder]'

# Every option in one set (server-side filter + sort-order):
dhis2 metadata list options \
    --filter 'optionSet.id:eq:OsVaccType1' \
    --order 'sortOrder:asc' \
    --fields 'id,code,name,sortOrder'

# Pinpoint one option by business code — filter + fields selector = cheap lookup:
dhis2 metadata list options \
    --filter 'code:eq:BCG' \
    --filter 'optionSet.id:eq:OsVaccType1' \
    --fields 'id,code,name,sortOrder'

# --- Fetch one set with full detail -----------------------------------------
dhis2 metadata get optionSets OsVaccType1 \
    --fields 'id,code,name,valueType,options[id,code,name,sortOrder]'

# --- Export / import a set as a metadata bundle ----------------------------
# Useful for moving an OptionSet between DHIS2 instances:
dhis2 metadata export \
    --resource optionSets \
    --resource options \
    --filter 'optionSets:code:eq:VACCINE_TYPE' \
    --output /tmp/vaccine-type.json

# dhis2 metadata import /tmp/vaccine-type.json --dry-run

# --- Workflow commands (coming in next PR) ---------------------------------
# The upcoming `dhis2 metadata options` sub-app layers integration-grade
# helpers over the generic surface above:
#
#   dhis2 metadata options show VACCINE_TYPE
#   dhis2 metadata options find --set VACCINE_TYPE --code BCG
#   dhis2 metadata options sync VACCINE_TYPE spec.json --remove-missing --dry-run
#
# Until then, use the library helpers (`client.option_sets.upsert_options`)
# — see examples/client/options_integration.py for the same patterns.
