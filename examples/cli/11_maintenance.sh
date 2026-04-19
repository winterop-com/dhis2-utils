#!/usr/bin/env bash
# `dhis2 maintenance ...` — background tasks, cache, soft-delete cleanup, data-integrity.
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

# Pretty-print every notification emitted by one task (oldest first).
LATEST_ANALYTICS_UID="$(dhis2 maintenance task list ANALYTICS_TABLE | head -1)"
if [ -n "${LATEST_ANALYTICS_UID}" ]; then
  dhis2 maintenance task status ANALYTICS_TABLE "${LATEST_ANALYTICS_UID}"
fi

# Kick off an async op and stream its progress until `completed=true`.
# (Analytics refresh + watch — real example of the task/watch pattern.)
REFRESH_TASK_UID="$(dhis2 analytics refresh --last-years 1 | jq -r '.response.id')"
dhis2 maintenance task watch ANALYTICS_TABLE "${REFRESH_TASK_UID}" --interval 1 --timeout 120

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
# List every built-in check (name, section, severity).
dhis2 maintenance dataintegrity list | head -20

# Kick off a summary run on one check; returns a task UID under .response.id.
DI_TASK_UID="$(dhis2 maintenance dataintegrity run orgunits_invalid_geometry | jq -r '.response.id')"

# Poll it to completion.
dhis2 maintenance task watch DATA_INTEGRITY "${DI_TASK_UID}" --interval 1 --timeout 60

# Read the summary (just `count` per check).
dhis2 maintenance dataintegrity result orgunits_invalid_geometry

# Or run + fetch details (populates `issues[]`).
dhis2 maintenance dataintegrity run orgunits_invalid_geometry --details >/dev/null
dhis2 maintenance dataintegrity result orgunits_invalid_geometry --details --json | jq '.results'
