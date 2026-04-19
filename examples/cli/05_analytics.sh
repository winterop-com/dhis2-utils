#!/usr/bin/env bash
# Analytics queries + resource-table refresh.
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

# Trigger analytics-table regeneration (returns a task reference).
# Add --watch / -w to stream progress until completed=true.
dhis2 analytics refresh --last-years 2
dhis2 analytics refresh --last-years 2 --watch --interval 1 --timeout 300

# --debug / -d on the root CLI logs HTTP traces to stderr — combine with --watch
# to trace both the kickoff POST and every subsequent task-status poll.
dhis2 -d analytics refresh --last-years 2 --watch --interval 1 --timeout 300
