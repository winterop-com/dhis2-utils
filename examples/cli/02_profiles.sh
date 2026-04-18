#!/usr/bin/env bash
# Profile management: list, verify, show, switch.
# `add` / `remove` / `login` are shown as commented-out examples at the bottom.
set -euo pipefail

# List every profile the CLI can see across project + global TOML files.
dhis2 profile list

# Probe the default profile — GET /api/system/info + /api/me.
dhis2 profile verify

# Show the default profile (secrets redacted).
dhis2 profile show "$(dhis2 profile list --json | python3 -c "import sys,json; p=[x for x in json.load(sys.stdin) if x['is_default']][0]; print(p['name'])")"

# Other profile commands (not run by default):
# dhis2 profile add dev --url https://play.im.dhis2.org/dev --auth basic --username system --password System123
# dhis2 profile switch dev
# dhis2 profile rename dev play-dev
# dhis2 profile remove play-dev
# dhis2 profile login local_oidc   # for auth=oauth2 profiles
