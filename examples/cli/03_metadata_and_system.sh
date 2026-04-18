#!/usr/bin/env bash
# Metadata inspection + UID generation.
set -euo pipefail

# What DHIS2 metadata types does this instance expose?
dhis2 metadata type list

# List data elements (first 10), pretty-printed. `list` is also aliased as `ls`.
dhis2 metadata list dataElements --limit 10

# Fetch one seeded data element by UID.
dhis2 metadata get dataElements DEancVisit1

# Fetch the Norway root OU.
dhis2 metadata get organisationUnits NORNorway01

# Generate fresh DHIS2 UIDs (11-char) via the dev tools — handy when scripting metadata creation.
dhis2 dev uid
dhis2 dev uid -n 5
