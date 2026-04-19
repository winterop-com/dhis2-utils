#!/usr/bin/env bash
# Outlier detection + tracked-entity analytics — the two remaining /api/analytics surfaces.
# Run via `uv run bash examples/cli/analytics_outlier_tracked_entities.sh`.
set -euo pipefail

# --- Outlier detection -------------------------------------------------------
# Finds data values that deviate from the historical pattern of their series.
# Z_SCORE is the default; MODIFIED_Z_SCORE is more robust when outliers already
# exist in the training data; MIN_MAX uses hard min/max bounds.
# (Upstream DHIS2 quirk: OpenAPI emits `MOD_Z_SCORE` but the server rejects it
# at runtime, accepting `MODIFIED_Z_SCORE` instead. See BUGS.md.)

echo "--- Z-score outliers in Oslo, last 12 months (threshold=2.0)"
dhis2 analytics outlier-detection \
    --data-set NORMonthDS1 \
    --org-unit NOROsloProv \
    --period LAST_12_MONTHS \
    --algorithm Z_SCORE --threshold 2.0 --max-results 5

echo
echo "--- Same query with modified Z-score (robust to existing outliers), descending"
dhis2 analytics outlier-detection \
    --data-set NORMonthDS1 --org-unit NOROsloProv --period LAST_12_MONTHS \
    --algorithm MODIFIED_Z_SCORE --threshold 3.5 --max-results 3 --sort-order DESC

# --- Tracked entity analytics ------------------------------------------------
# Line-lists tracked entities of a given type. Seeded fixture ships one TET
# "Person" (uid=FsgEX4d3Fc5) with 8 enrolled individuals.

echo
echo "--- list tracked entities of type Person under Norway (descendants), first 3"
dhis2 analytics tracked-entities query FsgEX4d3Fc5 \
    --dimension ou:NORNorway01 --ou-mode DESCENDANTS \
    --page-size 3 --asc created
