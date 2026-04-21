#!/usr/bin/env bash
# `dhis2 maintenance ...` — background tasks, cache, soft-delete cleanup,
# data-integrity, resource-table refreshes.
#
# Every DHIS2 async operation (analytics refresh, data-integrity run, bulk
# metadata import) returns a task UID; `dhis2 maintenance task` is the
# polling surface they all feed into.
set -euo pipefail

export DHIS2_URL="${DHIS2_URL:-http://localhost:8080}"

# --- Tasks ------------------------------------------------------------------
# Enumerate every background-job type DHIS2 tracks.
dhis2 maintenance task types

# For one task type, list the recorded task UIDs.
dhis2 maintenance task list ANALYTICS_TABLE

# Pretty-print every notification emitted by one task (oldest first). The
# Rich table output wraps UIDs in border characters; `grep -oE` extracts the
# first 11-char DHIS2 UID token out of the table and we take `head -1` — safe
# because `grep` never fails the whole pipeline in a non-match (guarded by
# the conditional below).
LATEST_ANALYTICS_UID="$(dhis2 maintenance task list ANALYTICS_TABLE \
    | grep -oE "[A-Za-z][A-Za-z0-9]{10}" | head -1 || true)"
if [ -n "${LATEST_ANALYTICS_UID}" ]; then
  dhis2 maintenance task status ANALYTICS_TABLE "${LATEST_ANALYTICS_UID}"
fi

# Kick off an async op and stream its progress until `completed=true`.
# Every job-kicking command has a `--watch/-w` flag that auto-derives the
# jobType + task UID from the response and polls to completion.
dhis2 maintenance refresh analytics --last-years 1 --watch --interval 1 --timeout 120

# Lower-level: feed a known task UID to `task watch` directly.
LATEST_ANALYTICS_TASK="$(dhis2 maintenance task list ANALYTICS_TABLE \
    | grep -oE "[A-Za-z][A-Za-z0-9]{10}" | head -1 || true)"
if [ -n "${LATEST_ANALYTICS_TASK}" ]; then
  dhis2 maintenance task status ANALYTICS_TABLE "${LATEST_ANALYTICS_TASK}" >/dev/null
fi

# --- Refreshing backing tables ---------------------------------------------
# Three parallel commands — `refresh analytics` is the primary post-ingest
# workflow. The others cover niche cases.

# Full analytics star schema — `ANALYTICS_TABLE` job. `--last-years N` caps
# the rebuild to that rolling window (faster than a full refresh).
dhis2 maintenance refresh analytics --last-years 1 --watch

# Resource tables only — supporting OU / category hierarchy tables.
# Use this when OU or category metadata changed but no new data values
# landed; much faster than a full `refresh analytics` run.
dhis2 maintenance refresh resource-tables --watch

# Monitoring tables — backing data-quality / validation-rule monitoring.
# Independent of the analytics + resource tables.
dhis2 maintenance refresh monitoring --watch

# --- Cache ------------------------------------------------------------------
# Drop Hibernate + every DHIS2 app cache — useful after a config-through-SQL
# change when you want the server to re-read from disk.
dhis2 maintenance cache

# --- Soft-delete cleanup ----------------------------------------------------
# DHIS2 keeps rows soft-deleted (deleted=true) after importStrategy=DELETE.
# Soft-deleted children block parent-metadata removal (BUGS.md #2). Purge:
dhis2 maintenance cleanup data-values
dhis2 maintenance cleanup events
dhis2 maintenance cleanup enrollments
dhis2 maintenance cleanup tracked-entities

# --- Data integrity ---------------------------------------------------------
# List every built-in check (name, section, severity) — first 20.
dhis2 maintenance dataintegrity list | awk 'NR<=20'

# Kick off a summary run on one check and wait for it to finish.
dhis2 maintenance dataintegrity run orgunits_invalid_geometry --watch --interval 1 --timeout 60

# Read the summary (just `count` per check).
dhis2 maintenance dataintegrity result orgunits_invalid_geometry

# Or run + fetch details (populates `issues[]`).
dhis2 maintenance dataintegrity run orgunits_invalid_geometry --details -w --timeout 60 >/dev/null
dhis2 maintenance dataintegrity result orgunits_invalid_geometry --details --json | jq '.results'

# --- Debug flag -------------------------------------------------------------
# `--debug / -d` on the root CLI logs every HTTP request to stderr
# (method, URL, status, bytes, elapsed ms). Stdout stays clean for piping.
dhis2 -d maintenance task types 2>&1 | awk 'NR<=5'
