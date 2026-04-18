#!/usr/bin/env bash
# Aggregate data values — read, write a single value, bulk push from a file.
set -euo pipefail

# Fetch values for Oslo in Jan 2026 (from the seeded dump). DHIS2 requires at least one
# data-scope filter (dataSet, DE, or DEG); we use the seeded monthly data set NORMonthDS1.
dhis2 aggregate get --data-set NORMonthDS1 --org-unit NOROsloProv --period 202601

# Narrow by data element group if you have one configured.
# dhis2 aggregate get --deg SOME_DEG_UID --period 202601

# Write a single value.
dhis2 aggregate set --de DEancVisit1 --pe 202603 --ou NOROsloProv --value 88

# Delete that value back out.
dhis2 aggregate delete --de DEancVisit1 --pe 202603 --ou NOROsloProv

# Bulk push from a JSON file (list of dataValues or a dataValueSets envelope).
# dhis2 aggregate push path/to/values.json --strategy CREATE_AND_UPDATE --dry-run
