#!/usr/bin/env bash
# Analytics queries + resource-table refresh.
set -euo pipefail

# Aggregated analytics for ANC visits across all 4 Norway fylker, last 12 months.
dhis2 analytics query \
  --dim dx:DEancVisit1\;DEancVisit4 \
  --dim pe:LAST_12_MONTHS \
  --dim ou:NORNorway01\;LEVEL-2 \
  --skip-meta

# Same query as raw table (DHIS2's rawData endpoint).
dhis2 analytics raw \
  --dim dx:DEancVisit1 \
  --dim pe:LAST_12_MONTHS \
  --dim ou:NORNorway01

# DataValueSet shape (easy to round-trip into dataValueSets import).
dhis2 analytics data-value-set \
  --dim dx:DEancVisit1 \
  --dim pe:LAST_12_MONTHS \
  --dim ou:NORNorway01

# Trigger analytics-table regeneration (returns a task reference).
dhis2 analytics refresh --last-years 2
