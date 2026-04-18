#!/usr/bin/env bash
# OIDC login flow — the CLI path.
# Mirrors examples/client/04_oidc_login.py but everything happens through
# `dhis2 profile add` + `dhis2 profile login`, no Python needed.
set -euo pipefail

# Source the seeded OAuth2 client creds into env.
set -a; source infra/home/credentials/.env.auth; set +a

# Create an oauth2 profile. --from-env pulls the DHIS2_OAUTH_* values
# and stamps them into ~/.config/dhis2/profiles.toml.
dhis2 profile add local_oidc --auth oauth2 --from-env --default

# Drive the authorization-code + PKCE flow. Opens your default browser,
# DHIS2's login page authenticates the user, capture the redirect,
# exchange for tokens, persist into ~/.config/dhis2/tokens.sqlite.
dhis2 profile login local_oidc

# Prove it worked — every subsequent `dhis2 ...` call reuses the cached
# access token (refreshing silently when near expiry).
dhis2 profile verify local_oidc
dhis2 system whoami --profile local_oidc
