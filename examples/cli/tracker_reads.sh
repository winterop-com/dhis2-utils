#!/usr/bin/env bash
# Tracker API — tracked entities by type, enrollments, events, bulk import.
# Run via `uv run bash examples/cli/tracker_reads.sh` so `dhis2` resolves.
# Uses the seeded Child Programme tracker program from infra/dhis-v42.sql.gz.
#   program:        IpHINAT79UW  (Child Programme, WITH_REGISTRATION)
#   TET:            nEenWmSyUEp  (Person (Play))
#   stages:         A03MvHHogjR  (Birth), ZzYYXq4fJie  (Baby Postnatal)
#   event program:  EVTsupVis01  (Supervision visit, WITHOUT_REGISTRATION)
#   root OU:        ImspTQPwCqd
#
# The authoring verbs — register / enroll / event create / outstanding —
# live in `tracker_register_and_followup.sh` and `tracker_event_program.sh`.
# This script is scoped to READ paths.
set -euo pipefail

PROGRAM_UID="IpHINAT79UW"
ORG_UNIT_UID="ImspTQPwCqd"

# Discover configured TrackedEntityTypes.
dhis2 data tracker type

# List tracked entities by type. The seeded fixture ships a "Person (Play)"
# TET (UID nEenWmSyUEp). Name lookups are case-insensitive; UID works too.
# DHIS2 rejects `--program` alongside a TrackedEntityType positional (E1003).
dhis2 data tracker list "Person (Play)" --org-unit "$ORG_UNIT_UID" --page-size 5

# Fetch one entity by UID (pipes the first UID from the list above).
TE_UID=$(dhis2 data tracker list "Person (Play)" --org-unit "$ORG_UNIT_UID" --page-size 1 --json | jq -r '.[0].trackedEntity // empty')
if [ -n "$TE_UID" ]; then
  dhis2 data tracker get "$TE_UID"
fi

# Enrollments for the program. `--ou-mode ACCESSIBLE` skips the explicit OU
# filter and uses every unit in the caller's capture scope — matches the
# seeded admin user's scope without extra wiring.
dhis2 data tracker enrollment list --program "$PROGRAM_UID" --ou-mode ACCESSIBLE --status ACTIVE --page-size 5

# Events in the program (same OU-mode trick).
dhis2 data tracker event list --program "$PROGRAM_UID" --ou-mode ACCESSIBLE --page-size 5

# Relationships from a tracked entity (will be empty for the seeded fixture —
# no relationship types are defined on the seeded Person type).
if [ -n "$TE_UID" ]; then
  dhis2 data tracker relationship list --te "$TE_UID" || true
fi

# Bulk import a tracker bundle. See examples/client/tracker_lifecycle.py for
# the typed `TrackerBundle` write path via the Python client — the CLI takes
# the JSON on disk:
# dhis2 data tracker push path/to/bundle.json --strategy CREATE_AND_UPDATE --dry-run
