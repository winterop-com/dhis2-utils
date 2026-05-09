# dhis2w-cli

Typer console script `dhis2` for working with DHIS2 instances from the shell. Discovers plugins from `dhis2w-core` — sixteen top-level domains covering metadata, data, analytics, tracker, users, routes, files, messaging, apps, doctor, and developer tools.

## Install

```bash
# Drops `dhis2` on $PATH
uv tool install dhis2w-cli

# With Playwright UI automation (browser screenshots, OIDC login, PAT minting)
uv tool install 'dhis2w-cli[browser]'
playwright install chromium    # one-time, after the install above

# Update later
uv tool upgrade dhis2w-cli
```

Or run on demand without installing:

```bash
uvx --from dhis2w-cli dhis2 --help
```

## Configure

The CLI reads a profile from `.dhis2/profiles.toml` (project) or `~/.config/dhis2/profiles.toml` (user). One-shot bootstrap:

```bash
dhis2 profile bootstrap mywork
```

Or set env vars and skip the profile system entirely:

```bash
export DHIS2_URL=https://dhis2.example.org
export DHIS2_PAT=d2p_...
dhis2 system info
```

## Surface

```
dhis2 analytics    DHIS2 analytics queries.
dhis2 apps         DHIS2 apps — /api/apps + /api/appHub.
dhis2 browser      Playwright UI automation (only with [browser] extra).
dhis2 data         DHIS2 data values (aggregate + tracker).
dhis2 dev          Developer/operator tools.
dhis2 doctor       Probe a DHIS2 instance for known gotchas + requirements.
dhis2 files        Manage DHIS2 documents + file resources.
dhis2 maintenance  DHIS2 maintenance (tasks, cache, integrity, cleanup, refresh).
dhis2 messaging    DHIS2 internal messaging.
dhis2 metadata     DHIS2 metadata inspection.
dhis2 profile      Manage DHIS2 profiles.
dhis2 route        DHIS2 integration routes.
dhis2 system       DHIS2 system info.
dhis2 user         DHIS2 user administration.
dhis2 user-group   DHIS2 user-group administration.
dhis2 user-role    DHIS2 user-role administration.
```

`dhis2 --help` for the full tree; `dhis2 <group> --help` for each.

## Documentation

Full CLI reference: https://winterop-com.github.io/dhis2w-utils/cli-reference/.

`dhis2w-cli` is one member of the [`dhis2w-utils`](https://github.com/winterop-com/dhis2w-utils) workspace. The MCP server (`dhis2w-mcp`) exposes the same plugin surface as MCP tools.
