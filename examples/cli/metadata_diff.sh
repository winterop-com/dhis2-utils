#!/usr/bin/env bash
# `dhis2 metadata diff` — structural comparison between two bundles, or one
# bundle vs the live instance. Useful before a tricky `metadata import` to
# preview exactly which objects get created / updated / deleted.
set -euo pipefail

# Export the live catalog (small slice for demo speed).
uv run dhis2 metadata export \
    --resource dataElements \
    --resource indicators \
    --output /tmp/baseline.json

cp /tmp/baseline.json /tmp/candidate.json

# Mutate the candidate bundle: rename one element, add a fake new one,
# drop an existing one. `jq` is assumed available for the worked demo.
jq '.dataElements[0].name = "RENAMED IN CANDIDATE"
    | .dataElements += [{"id":"fakenewid01","name":"Fake new","shortName":"Fake","valueType":"TEXT","domainType":"AGGREGATE","aggregationType":"NONE"}]
    | .dataElements = (.dataElements | del(.[1]))' \
    /tmp/baseline.json > /tmp/candidate.json

echo "--- plain table diff"
uv run dhis2 metadata diff /tmp/baseline.json /tmp/candidate.json

echo ""
echo "--- with offending UIDs"
uv run dhis2 metadata diff /tmp/baseline.json /tmp/candidate.json --show-uids

echo ""
echo "--- JSON envelope (pipe to jq for programmatic use)"
uv run dhis2 metadata diff /tmp/baseline.json /tmp/candidate.json --json | jq '.resources[] | {resource, created: (.created | length), updated: (.updated | length), deleted: (.deleted | length)}'

echo ""
echo "--- live: baseline.json vs the running instance (should be 0 changes)"
uv run dhis2 metadata diff /tmp/baseline.json --live
