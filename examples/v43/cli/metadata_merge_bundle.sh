#!/usr/bin/env bash
# `dhis2 metadata merge-bundle` — import a saved bundle file into a target profile.
# The bundle-source variant of `metadata merge`: instead of exporting from
# a source profile, read the bundle from disk. Useful when the bundle came
# from a saved `metadata export`, was hand-crafted, or was produced by a
# non-DHIS2 tool.
# Run via `uv run bash examples/v43/cli/metadata_merge_bundle.sh` so `dhis2` resolves.
set -euo pipefail

# 1. Save a small bundle to disk via the existing export verb.
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
BUNDLE="$TMP/data-elements.json"

dhis2 metadata export --resource dataElements --filter dataElements:name:like:Visits \
    --output "$BUNDLE"

# 2. Dry-run preview against the same instance — DHIS2 walks the bundle and
#    reports conflicts + counts without committing (importMode=VALIDATE).
dhis2 metadata merge-bundle "$DHIS2_PROFILE" "$BUNDLE" --dry-run

# 3. Apply by dropping --dry-run.
# dhis2 metadata merge-bundle prod "$BUNDLE"

# 4. Narrow the count summary to a subset of bundle keys (the import still
#    sends the whole bundle — DHIS2 controls per-resource scoping on import
#    via the bundle's own resource keys).
# dhis2 metadata merge-bundle "$DHIS2_PROFILE" "$BUNDLE" -r dataElements --dry-run
