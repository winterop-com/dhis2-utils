#!/usr/bin/env bash
# Tracker API — tracked entities by type, enrollments, events, bulk import.
# The seeded e2e fixture only has aggregate data, so most of these will
# return empty result sets. Run against a tracker-populated instance
# (e.g. play.dhis2.org/dev) to see real output.
set -euo pipefail

# Discover configured TrackedEntityTypes (Person, Patient, Lab Sample, ...).
# dhis2 data tracker type

# List tracked entities of a given TrackedEntityType. The <type> positional
# accepts a name (case-insensitive, resolved server-side) or a UID directly.
# dhis2 data tracker list Person --program <PROGRAM_UID> --org-unit <OU> --page-size 10
# dhis2 data tracker list patient --program <PROGRAM_UID>     # case-insensitive
# dhis2 data tracker list tet01234567 --program <PROGRAM_UID> # by UID

# Fetch one tracked entity by UID (type inferred from the entity itself).
# dhis2 data tracker get <TE_UID>

# Enrollments for a program (active only).
# dhis2 data tracker enrollment list --program <PROGRAM_UID> --status ACTIVE

# Events in a program (filter by date).
# dhis2 data tracker event list --program <PROGRAM_UID> --after 2024-01-01

# Relationships from a tracked entity.
# dhis2 data tracker relationship list --te <TE_UID>

# Bulk import a tracker bundle.
# dhis2 data tracker push path/to/bundle.json --strategy CREATE_AND_UPDATE --dry-run

echo "(uncomment the commands above and supply real UIDs to try against a tracker instance)"
