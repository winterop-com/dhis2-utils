#!/usr/bin/env bash
# Aggregated analytics queries — `dhis2 analytics query`. Refreshes of the
# analytics backing tables live under `dhis2 maintenance refresh ...`
# (see maintenance.sh).
set -euo pipefail

# Aggregated analytics for Penta1 doses across all 4 Sierra Leone districts, last 12 months.
dhis2 analytics query \
  --dim dx:fClA2Erf6IO\;UOlfIjgN8X6 \
  --dim pe:LAST_12_MONTHS \
  --dim ou:ImspTQPwCqd\;LEVEL-2 \
  --skip-meta

# Same query as raw pre-aggregation rows (/api/analytics/rawData).
dhis2 analytics query --shape raw \
  --dim dx:fClA2Erf6IO \
  --dim pe:LAST_12_MONTHS \
  --dim ou:ImspTQPwCqd

# DataValueSet envelope (easy to round-trip into dataValueSets import).
dhis2 analytics query --shape dvs \
  --dim dx:fClA2Erf6IO \
  --dim pe:LAST_12_MONTHS \
  --dim ou:ImspTQPwCqd
