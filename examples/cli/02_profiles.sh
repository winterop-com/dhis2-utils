#!/usr/bin/env bash
# Profile management: list, verify, show, default.
# `add` / `remove` / `login` / `bootstrap` are shown as commented-out examples at the bottom.
set -euo pipefail

# List every profile the CLI can see across project + global TOML files.
dhis2 profile list

# Probe the default profile — GET /api/system/info + /api/me.
dhis2 profile verify

# Show the default profile (secrets redacted).
dhis2 profile show "$(dhis2 profile list --json | python3 -c "import sys,json; p=[x for x in json.load(sys.stdin) if x['is_default']][0]; print(p['name'])")"

# Other profile commands (not run by default). Secrets never come via argv —
# pass through env vars (DHIS2_PAT / DHIS2_PASSWORD / DHIS2_OAUTH_CLIENT_SECRET)
# or enter them at the interactive prompt.
# DHIS2_PASSWORD=System123 dhis2 profile add dev --url https://play.im.dhis2.org/dev --auth basic --username system
# dhis2 profile default dev
# dhis2 profile rename dev play-dev
# dhis2 profile remove play-dev
# dhis2 profile login local_oidc           # run the OAuth2 flow for an existing oauth2 profile
# dhis2 profile bootstrap demo --auth pat --url $DHIS2_URL   # one-shot: create PAT + save profile
