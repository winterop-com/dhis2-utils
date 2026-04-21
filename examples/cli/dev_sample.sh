#!/usr/bin/env bash
# `dhis2 dev sample ...` — inject known-good fixtures and verify end-to-end.
#
# Each sub-command walks a full lifecycle (create -> verify -> clean up) so a
# fresh DHIS2 install can be smoke-tested in one pass. Useful after:
#   - spinning up a new stack (`make dhis2-run`)
#   - rolling a config change (e.g. route.remote_servers_allowed)
#   - applying a DHIS2 version upgrade
#
# Each step prints structured PASS/FAIL lines with timings.
set -euo pipefail

export DHIS2_ADMIN_PASSWORD="${DHIS2_ADMIN_PASSWORD:-district}"
export DHIS2_URL="${DHIS2_URL:-http://localhost:8080}"

# Exercise the /api/routes integration API (create -> run -> delete).
# Proxies to httpbin.org by default; pass --url to target something else.
dhis2 dev sample route

# Write a data value, read it back, soft-delete. Uses the seeded BfMAe6Itzgt
# fixture by default (fClA2Erf6IO / PMa2VCrupOd / 202603).
dhis2 dev sample data-value

# Create a fresh PAT, call /api/me with it, delete it.
dhis2 dev sample pat --admin-user admin

# Create a throwaway OAuth2 client, verify it persists via GET, delete it.
dhis2 dev sample oauth2-client --admin-user admin

# Or: run everything in one go.
# dhis2 dev sample all --admin-user admin

# Add `--keep` to leave a fixture behind for manual inspection:
# dhis2 dev sample route --keep
# dhis2 route list      # shows SMOKE_ROUTE until you delete it
