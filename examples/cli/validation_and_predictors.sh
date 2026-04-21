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
# Evaluate every validation rule on an org-unit subtree for a date range.
# Returns violations (cells where the rule evaluates to `false`). Synchronous —
# no `--watch`. `--persist` writes violations to /api/validationResults for
# later inspection; `--notification` fires configured notification templates.

dhis2 maintenance validation run ImspTQPwCqd \
    --start-date 2025-01-01 --end-date 2025-12-31

# Narrow to one ValidationRuleGroup:
# dhis2 maintenance validation run ImspTQPwCqd \
#     --start-date 2025-01-01 --end-date 2025-12-31 \
#     --group vrgAAA000001 --persist

# --- Persisted validation results -------------------------------------------
# Browse violations previously stored via `--persist` on a run.

dhis2 maintenance validation result list
dhis2 maintenance validation result list --ou ImspTQPwCqd --pe 202501

# Bulk-delete by filter (at least one filter required — can't wipe the whole
# table accidentally):
# dhis2 maintenance validation result delete --pe 202501

# --- Predictors -------------------------------------------------------------
# Run predictor expressions to generate data values from historical data.

# Run every predictor on the instance:
dhis2 maintenance predictors run \
    --start-date 2025-01-01 --end-date 2025-01-31

# Run one predictor:
# dhis2 maintenance predictors run \
#     --predictor predUid0001 \
#     --start-date 2025-01-01 --end-date 2025-01-31

# Run a PredictorGroup:
# dhis2 maintenance predictors run \
#     --group pgrpUid00001 \
#     --start-date 2025-01-01 --end-date 2025-01-31

# --- CRUD on validation rules + predictors ---------------------------------
# These stay on the generic metadata surface — no special plugin:
dhis2 metadata list validationRules --fields 'id,name,leftSide,rightSide'
dhis2 metadata list predictors --fields 'id,name,generator,sequentialSampleCount'
