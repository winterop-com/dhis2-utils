#!/usr/bin/env bash
# Aggregated analytics queries — `dhis2 analytics query`. Refreshes of the
# analytics backing tables live under `dhis2 maintenance refresh ...`
# (see maintenance.sh).
set -euo pipefail

# Aggregated analytics for ANC visits across all 4 Norway fylker, last 12 months.
dhis2 analytics query \
  --dim dx:DEancVisit1\;DEancVisit4 \
  --dim pe:LAST_12_MONTHS \
  --dim ou:NORNorway01\;LEVEL-2 \
  --skip-meta

# Same query as raw pre-aggregation rows (/api/analytics/rawData).
dhis2 analytics query --shape raw \
  --dim dx:DEancVisit1 \
  --dim pe:LAST_12_MONTHS \
  --dim ou:NORNorway01

# DataValueSet envelope (easy to round-trip into dataValueSets import).
dhis2 analytics query --shape dvs \
  --dim dx:DEancVisit1 \
  --dim pe:LAST_12_MONTHS \
  --dim ou:NORNorway01
