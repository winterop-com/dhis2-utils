#!/usr/bin/env bash
# Metadata inspection + system UID minting.
set -euo pipefail

# What DHIS2 metadata types does this instance expose?
dhis2 metadata types

# List data elements (first 10), pretty-printed.
dhis2 metadata list dataElements --page-size 10

# Fetch one seeded data element by UID.
dhis2 metadata get dataElements DEancVisit1

# Fetch the Norway root OU.
dhis2 metadata get organisationUnits NORNorway01

# Mint a fresh DHIS2 UID (11-char) — handy when scripting metadata creation.
dhis2 system uid
dhis2 system uid -n 5
