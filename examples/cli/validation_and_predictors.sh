#!/usr/bin/env bash
# `dhis2 maintenance validation` + `dhis2 maintenance predictors` — run validation
# rules and predictor expressions. CRUD on the rules / predictors themselves stays
# on `dhis2 metadata list ...`.
set -euo pipefail

# --- Expression validation --------------------------------------------------
# Parse-check any DHIS2 expression + render a human description. Useful as a
# pre-save gate before creating a VR or indicator.

dhis2 maintenance validation validate-expression '#{fClA2Erf6IO}'
dhis2 maintenance validation validate-expression '#{noSuchDeUid}'

# Per-context parsers: validation-rule / indicator / predictor / program-indicator.
# Each has a different allowed-reference set on the DHIS2 side.
dhis2 maintenance validation validate-expression '#{fClA2Erf6IO} > 0' --context validation-rule

# --- Validation analysis ----------------------------------------------------
# Evaluate validation rules on an org-unit subtree for a date range. Returns
# violations (cells where the rule evaluates to `false`). Synchronous — no
# `--watch`. `--persist` writes violations to /api/validationResults for
# later inspection; `--notification` fires configured notification templates.
#
# The workspace seeds two BCG validation rules + a ValidationRuleGroup:
#   VrBCGPos001  — BCG <1y must be > 0 (catches legitimate zero-dose months)
#   VrBCGInf001  — BCG <1y == BCG >1y (sentinel — produces reliable violations)
#   VrGImmun001  — group wrapping both

# Run one group against the Sierra Leone root OU (walks the full sub-tree):
dhis2 maintenance validation run ImspTQPwCqd \
    --start-date 2024-04-01 --end-date 2024-06-30 \
    --group VrGImmun001 --max-results 10

# Run every rule on the instance (no --group):
# dhis2 maintenance validation run ImspTQPwCqd \
#     --start-date 2024-04-01 --end-date 2024-06-30 --max-results 5

# --- Persisted validation results -------------------------------------------
# Persist the sentinel rule's violations, then browse them via
# /api/validationResults:
dhis2 maintenance validation run ImspTQPwCqd \
    --start-date 2024-04-01 --end-date 2024-04-30 \
    --group VrGImmun001 --persist --max-results 5

dhis2 maintenance validation result list --ou ImspTQPwCqd --pe 202404

# Bulk-delete by filter (at least one filter required — can't wipe the whole
# table accidentally):
# dhis2 maintenance validation result delete --pe 202404

# --- Predictors -------------------------------------------------------------
# Run predictor expressions to generate data values from historical data.
#
# The workspace seeds two BCG-dose predictors + a PredictorGroup:
#   PrdAvgBCG01  — avg(#{s46m5MS0hxu.Prlt0C1RF0s}) over 3 monthly samples
#   PrdSumBCG01  — sum(#{s46m5MS0hxu.Prlt0C1RF0s}) over 3 monthly samples
#   PdGImmun001  — group wrapping both
# Seeded 2024 data covers Jan–Dec 2024 at the facility level, so any
# run window inside 2024 produces real predictions.

# Run every predictor on the instance:
dhis2 maintenance predictors run \
    --start-date 2024-04-01 --end-date 2024-06-30

# Run one predictor by UID:
dhis2 maintenance predictors run \
    --predictor PrdSumBCG01 \
    --start-date 2024-04-01 --end-date 2024-04-30

# Run a PredictorGroup:
dhis2 maintenance predictors run \
    --group PdGImmun001 \
    --start-date 2024-04-01 --end-date 2024-06-30

# --- CRUD on validation rules + predictors ---------------------------------
# These stay on the generic metadata surface — no special plugin:
dhis2 metadata list validationRules --fields 'id,name,leftSide,rightSide'
dhis2 metadata list predictors --fields 'id,name,generator,sequentialSampleCount'
