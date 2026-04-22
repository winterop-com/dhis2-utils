#!/usr/bin/env bash
# `dhis2 metadata search <query>` — cross-resource metadata search.
#
# One query matches on any of three axes across every enabled metadata
# resource: `id:ilike:<q>`, `code:ilike:<q>`, or `name:ilike:<q>`. Paste
# whatever you have — full UID, partial UID, business code, or name
# fragment — and get back a table of every matching object grouped by
# resource type.
#
# Three parallel `/api/metadata` calls merge into one result set (DHIS2's
# single-call `rootJunction=OR` is broken on `/api/metadata` — see BUGS.md #29).
set -euo pipefail

# --- Name fragment — the broadest pattern ----------------------------------
# Finds every DE / indicator / dashboard / viz / map / etc. whose NAME
# contains "measles". The seeded instance returns ~25 hits across 6 types.

dhis2 metadata search measles

# --- Full UID lookup -------------------------------------------------------
# Paste a UID from a log line / URL / audit trail to find the owning resource.

dhis2 metadata search s46m5MS0hxu

# --- Partial UID prefix ----------------------------------------------------
# First 3-4 characters of a UID are usually unique enough to pin the object.

dhis2 metadata search s46m

# --- Business code (case-insensitive substring) ----------------------------
# Code:ilike — useful when you have DHIS2 codes like `DE_359706` from an
# interop mapping table but don't remember the DHIS2 UID.

dhis2 metadata search DE_3597

# --- JSON output for scripting ---------------------------------------------
# Emit the full typed `SearchResults` JSON for downstream processing.

dhis2 metadata search measles --json | jq '.hits.dataElements | length'

# --- Limit per-resource page size ------------------------------------------
# Default is 50 hits per resource type. Narrow to 5 for a quick scan.

dhis2 metadata search imm --page-size 5
