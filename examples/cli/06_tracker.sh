#!/usr/bin/env bash
# Tracker API — tracked entities, enrollments, events, bulk import.
# The seeded e2e fixture only has aggregate data, so most of these will
# return empty result sets. Run against a tracker-populated instance
# (e.g. play.dhis2.org/dev) to see real output.
set -euo pipefail

# List tracked entities (requires a tracker program UID).
# dhis2 tracker list-tracked-entities --program <PROGRAM_UID> --page-size 10

# Fetch one tracked entity.
# dhis2 tracker get-tracked-entity <TE_UID> --program <PROGRAM_UID>

# Enrollments for a program (active only).
# dhis2 tracker list-enrollments --program <PROGRAM_UID> --status ACTIVE

# Events in a program (filter by date).
# dhis2 tracker list-events --program <PROGRAM_UID> --after 2024-01-01

# Relationships from a tracked entity.
# dhis2 tracker list-relationships --te <TE_UID>

# Bulk import a tracker bundle.
# dhis2 tracker push path/to/bundle.json --strategy CREATE_AND_UPDATE --dry-run

echo "(uncomment the commands above and supply real UIDs to try against a tracker instance)"
