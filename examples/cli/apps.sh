#!/usr/bin/env bash
# `dhis2 apps ...` — install / uninstall / update DHIS2 apps via /api/apps
# and the configured App Hub (/api/appHub). DHIS2 v42's Spring AS handles
# the install side; App Hub is a read-only catalog proxy.
#
# Installed apps fall into two buckets the plugin cares about:
#   - App Hub apps (`app_hub_id` set) — the main target of `update`.
#     Includes bundled core apps (Reports, Cache Cleaner, Data Visualizer,
#     etc.) — DHIS2 lets the App Hub overwrite the bundled copy in place.
#   - Side-loaded zips (no `app_hub_id`) — SKIPPED by `update --all`,
#     reinstall by running `dhis2 apps add path/to/file.zip`.
set -euo pipefail

# ---------------------------------------------------------------------------
# List + inspect
# ---------------------------------------------------------------------------

dhis2 apps list
# `ls` is a hidden alias:
#   dhis2 apps ls

# Machine-readable variant for scripting.
dhis2 apps list --json | head

# ---------------------------------------------------------------------------
# App Hub
# ---------------------------------------------------------------------------

# The configured App Hub catalog (proxied server-side). Each row carries
# a `versions` list whose ids are `dhis2 apps add <version-id>` inputs.
dhis2 apps hub-list --limit 5

# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------

# Preview mode: show which installed apps have a newer version on the App
# Hub without actually installing anything. Re-run without --dry-run to
# apply the updates.
dhis2 apps update --all --dry-run

# Update every installed app that has a newer App Hub version. Side-loaded
# zips (no `app_hub_id`) are reported as SKIPPED; bundled core apps update
# in place.
dhis2 apps update --all

# ---------------------------------------------------------------------------
# Reload (no new fetch — re-read every app from disk)
# ---------------------------------------------------------------------------

dhis2 apps reload
