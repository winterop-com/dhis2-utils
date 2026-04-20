# `dhis2` CLI: step-by-step tutorial

A narrative walkthrough of the `dhis2` command-line interface. Every block is copy-pasteable; by the end you will have inspected, changed, exported, diffed, and re-imported DHIS2 metadata, plus kicked off an analytics refresh and administered a user.

For the exhaustive list of every command and flag, see the [CLI reference](../cli-reference.md). For runnable examples per topic, see the [examples index](../examples.md).

- [Prerequisites](#prerequisites)
- [Install + profile setup](#install-profile-setup)
- [Your first call: `whoami`](#your-first-call-whoami)
- [Inspecting metadata](#inspecting-metadata)
- [Changing metadata: patch vs import](#changing-metadata-patch-vs-import)
- [Cross-instance workflows: export + diff + import](#cross-instance-workflows-export-diff-import)
- [Running analytics + watching jobs](#running-analytics-watching-jobs)
- [Administering users + groups + roles](#administering-users-groups-roles)
- [Probing instance health: `dhis2 doctor`](#probing-instance-health-dhis2-doctor)
- [Global flags: `--profile` and `--debug`](#global-flags-profile-and-debug)
- [Where to go next](#where-to-go-next)

## Prerequisites

- Python 3.13+ with `uv` installed.
- A reachable DHIS2 v42+ instance. Local: `make dhis2-run` (starts DHIS2 + Postgres + seeds auth). Remote: your own install or `https://play.im.dhis2.org/stable-2-42`.
- Credentials — a Personal Access Token (PAT), Basic auth, or OAuth2 client config. `make dhis2-run` writes PATs to `infra/home/credentials/.env.auth`.

## Install + profile setup

The CLI ships with every workspace member. From a checkout:

```bash
uv sync
source .venv/bin/activate   # so `dhis2` resolves without `uv run` prefix
```

Profiles are how the CLI knows *where* to talk and *how* to authenticate. Create one that targets your local instance:

```bash
# Load the seeded PAT into env so it never hits argv or the TOML file
set -a; source infra/home/credentials/.env.auth; set +a

dhis2 profile add local --url http://localhost:8080 --auth pat --default --verify
```

The `--verify` flag makes a quick `/api/me` call so you know the profile works before you leave the command. `--default` marks this as the default so you can skip `--profile` on every call.

You can also target via env without a profile at all — the CLI will fall back to `DHIS2_URL` + `DHIS2_PAT` / `DHIS2_USERNAME` + `DHIS2_PASSWORD`.

Useful profile commands:

```bash
dhis2 profile list                          # show every registered profile
dhis2 profile verify                        # re-check the default profile
dhis2 profile verify local --json           # machine-readable verify
dhis2 profile show local                    # sanitised TOML dump (secrets redacted)
```

## Your first call: `whoami`

Prove the profile works:

```bash
dhis2 system whoami
# admin (admin admin)

dhis2 system info
# version: 2.42.4
# revision: abc1234
# systemName: DHIS2 Play
# ...
```

Every subsequent command reuses the same profile resolution.

## Inspecting metadata

Metadata is DHIS2's term for the "dictionary" — data elements, indicators, datasets, organisation units, programs, etc. List the resource types the instance exposes:

```bash
dhis2 metadata type list
# aggregateDataExchanges
# analyticsTableHooks
# ...
# 139 types available
```

List instances of any type, with the full DHIS2 query surface:

```bash
# Top 5 by name
dhis2 metadata list dataElements --order "name:asc" --page-size 5

# Filter (repeatable, AND by default):
dhis2 metadata list dataElements \
  --filter "valueType:eq:INTEGER_POSITIVE" \
  --filter "domainType:eq:AGGREGATE"

# OR multiple filters:
dhis2 metadata list dataElements \
  --filter "name:like:ANC" --filter "code:eq:DEancVisit1" --root-junction OR

# Dump the whole catalog server-side (no paging):
dhis2 metadata list indicators --all --fields ":identifiable"
```

Fetch a single object:

```bash
dhis2 metadata get dataElements DEancVisit1
# ┌────────────────────┬─────────────────────────────────┐
# │ id                 │ DEancVisit1                     │
# │ name               │ ANC 1st visit                   │
# │ shortName          │ ANC1ST                          │
# │ valueType          │ INTEGER_POSITIVE                │
# │ ...                │ ...                             │
# └────────────────────┴─────────────────────────────────┘

# JSON for debugging / piping:
dhis2 metadata get dataElements DEancVisit1 --json | jq '.valueType'
```

For library-code use, see `examples/client/list_data_elements.py` — same result through the Python typed accessor.

## Changing metadata: patch vs import

**Patch** is for targeted, single-object updates — change a name or toggle a flag. It uses RFC 6902 JSON Patch, so it's surgical:

```bash
# Inline: replace + remove in one call. Values JSON-decode automatically.
dhis2 metadata patch dataElements DEancVisit1 \
  --set '/description=Updated via CLI' \
  --set '/zeroIsSignificant=false' \
  --remove '/legacyField'

# File-based for full RFC 6902 expressiveness:
cat > patch.json <<'JSON'
[
  {"op": "replace", "path": "/name", "value": "New name"},
  {"op": "copy", "path": "/shortName", "from": "/name"},
  {"op": "test", "path": "/valueType", "value": "INTEGER"}
]
JSON
dhis2 metadata patch dataElements DEancVisit1 --file patch.json
```

**Import** is for bulk metadata — upload a whole bundle at once, typically after editing an exported file. Use the `--dry-run` flag to preview:

```bash
dhis2 metadata import bundle.json --dry-run        # preview: parses + validates, nothing persists
dhis2 metadata import bundle.json                  # real import
```

See [metadata plugin docs](../architecture/metadata-plugin.md) for every import flag (`--strategy`, `--atomic-mode`, `--identifier`, etc.) mapped to DHIS2's wire-level options.

## Cross-instance workflows: export + diff + import

The canonical "copy metadata from A to B" pattern:

```bash
# 1. Export a filtered slice from profile A. `:owner` is DHIS2's own full-fidelity selector.
dhis2 --profile staging metadata export \
  --resource dataElements --resource indicators \
  --filter "dataElements:name:like:ANC" \
  --output anc-bundle.json

# 2. Check what's dangling — references to UIDs not in the bundle.
#    (The export already warned you; this is just inspection.)
cat anc-bundle.json | jq '.dataElements[0].categoryCombo'

# 3. Diff against the target before committing anything.
dhis2 --profile prod metadata diff anc-bundle.json --live --show-uids

# 4. Dry-run import on the target to catch server-side validation issues.
dhis2 --profile prod metadata import anc-bundle.json --dry-run

# 5. Real import.
dhis2 --profile prod metadata import anc-bundle.json
```

`metadata diff` also works bundle-vs-bundle (both positional args) for comparing two exports without hitting DHIS2 at all.

The full pipeline is in `examples/cli/metadata_round_trip.sh` — the script applies a jq transformation between export and import, showing the story end-to-end.

## Running analytics + watching jobs

DHIS2 analytics lives in pre-computed tables. Refresh them + query:

```bash
# Refresh in the background (takes minutes on a full instance)
dhis2 analytics refresh

# Refresh and block until done, streaming progress:
dhis2 analytics refresh --watch

# Query aggregated analytics:
dhis2 analytics query \
  --dimension "dx:DEancVisit1" \
  --dimension "pe:LAST_12_MONTHS" \
  --dimension "ou:NORNorway01"

# Outlier detection on a data scope:
dhis2 analytics outlier-detection \
  --data-set NORMonthDS1 --org-unit NOROsloProv --algorithm MODIFIED_Z_SCORE
```

`--watch` is the standard pattern for any DHIS2 command that kicks off a background job. It polls DHIS2's `/api/system/tasks/<type>/<uid>` and renders a Rich progress bar until the job completes or errors. Same flag works on `maintenance dataintegrity run --watch` and other slow operations.

## Administering users + groups + roles

Read and write the user surface:

```bash
# Read
dhis2 user list --filter "disabled:eq:false" --page-size 10
dhis2 user get admin                                    # by username
dhis2 user me                                           # the authenticated user
dhis2 user me --json                                    # full /api/me payload

# Invite a new user (DHIS2 emails them a signup link)
dhis2 user invite new.user@example.com \
  --first-name New --surname User \
  --user-role ROLEuidHere \
  --org-unit OUuidHere

# Password reset (mails the user a link)
dhis2 user reset-password <uid>
```

Groups and roles have their own plugins:

```bash
# User groups
dhis2 user-group list
dhis2 user-group add-member <group-uid> <user-uid>
dhis2 user-group sharing-grant-user <group-uid> <user-uid> --metadata-write

# User roles (authorities, not DHIS2's "roles" = groups)
dhis2 user-role list
dhis2 user-role authorities <role-uid>              # inspect which authorities the role grants
dhis2 user-role add-user <role-uid> <user-uid>      # grant role to user
```

## Probing instance health: `dhis2 doctor`

One read-only command, roughly 100 checks — 20 metadata-health probes + 81 DHIS2 data-integrity checks + every BUGS.md tripwire. Run it on any DHIS2 instance before integrating with it:

```bash
dhis2 doctor                            # all probes; fail on any fail/warn
dhis2 doctor --category metadata        # just the metadata probes
dhis2 doctor --category integrity       # DHIS2's built-in data-integrity scan
dhis2 doctor --category bugs            # known-bug tripwires only
dhis2 doctor --slow                     # include the isSlow DHIS2 checks (full coverage)
dhis2 doctor --json                     # machine-readable output for CI
```

Use it in CI as a gate before running migrations or imports — non-zero exit when there are any `fail` probes. See [doctor plugin](../architecture/doctor-plugin.md) for the full probe list.

## Global flags: `--profile` and `--debug`

Two flags on the root `dhis2` app (**before** the subcommand):

```bash
# Override the active profile for one call
dhis2 --profile prod metadata list dataElements

# Short form
dhis2 -p staging user list
```

```bash
# Verbose HTTP trace on stderr — method, URL, status, bytes, elapsed
dhis2 -d system whoami
# 10:54:05  dhis2_client.http         GET http://localhost:8080/api/system/info -> 200 (2165 bytes, 9ms)
# 10:54:05  dhis2_client.http         GET http://localhost:8080/api/me -> 200 (2760 bytes, 17ms)
# admin (admin admin)
```

Debug output lands on stderr so stdout stays pipe-friendly — you can still `dhis2 -d metadata list dataElements --json > out.json` and get clean JSON.

## Where to go next

- **Full command reference**: [CLI reference](../cli-reference.md) — every subcommand, every flag, auto-generated from the Typer app so it never drifts.
- **Runnable examples**: [examples index](../examples.md) — 22 CLI + 28 Python + 17 MCP scripts organised by feature.
- **Library usage**: [`dhis2-client` tutorial](client-tutorial.md) — when you want to drive DHIS2 from Python instead of the shell.
- **Plugin architecture**: [overview](../architecture/overview.md) — how plugins, profiles, auth providers, and codegen fit together.

The CLI is intentionally thin — every command ends up in a plugin's `service.py`, and the same service layer is what the FastMCP server exposes as tools. If you find the CLI missing a flag you expect, it's almost always a service-layer parameter that just needs wiring to a Typer option — see `packages/dhis2-core/src/dhis2_core/plugins/<plugin>/cli.py` for the pattern.
