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

# Pretty-print every notification emitted by one task (oldest first). `head`
# closes stdin early, which under `set -o pipefail` kills the pipeline — use
# `awk 'NR==1; {exit}'` instead, which reads all of DHIS2's output.
LATEST_ANALYTICS_UID="$(dhis2 maintenance task list ANALYTICS_TABLE | awk 'NR==1{print;exit}')"
if [ -n "${LATEST_ANALYTICS_UID}" ]; then
  dhis2 maintenance task status ANALYTICS_TABLE "${LATEST_ANALYTICS_UID}"
fi

# Kick off an async op and stream its progress until `completed=true`.
# Every job-kicking command has a `--watch/-w` flag that auto-derives the
# jobType + task UID from the response and polls to completion.
dhis2 analytics refresh --last-years 1 --watch --interval 1 --timeout 120

# Lower-level: feed a known task UID to `task watch` directly.
LATEST_ANALYTICS_TASK="$(dhis2 maintenance task list ANALYTICS_TABLE | awk 'NR==1{print;exit}')"
dhis2 maintenance task status ANALYTICS_TABLE "${LATEST_ANALYTICS_TASK}" >/dev/null

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
