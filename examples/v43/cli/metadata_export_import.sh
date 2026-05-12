#!/usr/bin/env bash
# `dhis2 metadata export` + `dhis2 metadata import` — cross-instance round-trip.
# Run via `uv run bash examples/v43/cli/metadata_export_import.sh` so the `dhis2` entry resolves.
set -euo pipefail

tmp=$(mktemp -d)
trap "rm -rf $tmp" EXIT

echo "--- export a narrow slice: dataElements + indicatorTypes"
dhis2 metadata export \
    --resource dataElements \
    --resource indicatorTypes \
    --fields ":owner" \
    --output "$tmp/slice.json"

echo
echo "--- bundle summary:"
python3 -c "import json; d=json.load(open('$tmp/slice.json')); [print(f'  {k}: {len(v)}') for k,v in d.items() if isinstance(v, list)]"

echo
echo "--- dry-run import against the source instance (idempotent check)"
dhis2 metadata import "$tmp/slice.json" --dry-run

echo
echo "--- export the full catalog (lossless :owner fields) to a bigger bundle"
dhis2 metadata export --output "$tmp/full.json"
python3 -c "import json; d=json.load(open('$tmp/full.json')); print(f'full bundle: {sum(len(v) for v in d.values() if isinstance(v, list))} objects across {sum(1 for v in d.values() if isinstance(v, list))} resource types')"

# Real import (without --dry-run) would create/update objects:
# dhis2 metadata import "$tmp/full.json" --strategy CREATE_AND_UPDATE --atomic-mode ALL
