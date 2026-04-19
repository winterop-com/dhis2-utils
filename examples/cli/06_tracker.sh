#!/usr/bin/env bash
# Tracker API — tracked entities by type, enrollments, events, bulk import.
# Run via `uv run bash examples/cli/06_tracker.sh` so `dhis2` resolves.
# Uses the seeded Maternal Care tracker program from infra/dhis-v42.sql.gz.
#   program: eke95YJi9VS (Maternal Care, WITH_REGISTRATION)
#   stages:  b1rFlQyZFPX (ANC visit), iPwB0u9Tufl (Delivery)
#   type:    FsgEX4d3Fc5 (Person)
#   root OU: NORNorway01
set -euo pipefail

PROGRAM_UID="eke95YJi9VS"
ORG_UNIT_UID="NORNorway01"

# Discover configured TrackedEntityTypes.
dhis2 data tracker type

# List tracked entities by type — name is case-insensitive, UID works too.
# DHIS2 rejects `--program` alongside a TrackedEntityType positional (E1003).
dhis2 data tracker list Person --org-unit "$ORG_UNIT_UID" --page-size 5

# Fetch one entity by UID (pipes the first UID from the list above).
TE_UID=$(dhis2 data tracker list Person --org-unit "$ORG_UNIT_UID" --page-size 1 | jq -r '.[0].trackedEntity // empty')
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

# Bulk import a tracker bundle. See examples/client/12_tracker_lifecycle.py for
# the typed `TrackerBundle` write path via the Python client — the CLI takes
# the JSON on disk:
# dhis2 data tracker push path/to/bundle.json --strategy CREATE_AND_UPDATE --dry-run
