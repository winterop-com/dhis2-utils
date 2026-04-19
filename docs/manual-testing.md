# Manual testing guide — every CLI + MCP surface in one pass

Purpose: a copy-pasteable sequence that exercises every `dhis2` CLI command and every MCP tool against a live stack. Use this when you want to sanity-check the surface after a refactor, or to track down a regression.

Assumes:
- `make dhis2-run` is up and `admin/district` works.
- You've run `make dhis2-seed` at least once so `infra/home/credentials/.env.auth` is populated.
- `uv sync --all-packages` has been run so `dhis2` is on `$PATH` (inside `.venv/bin`).

Secrets never go on argv. Every command that needs a PAT, password, or client secret reads from env vars or prompts. Load the seeded credentials into your shell once:

```bash
set -a; source infra/home/credentials/.env.auth; set +a
```

That defines the end-user credentials (`DHIS2_PAT`, `DHIS2_PASSWORD`) plus the OAuth2 client config (`DHIS2_OAUTH_CLIENT_ID`, `DHIS2_OAUTH_CLIENT_SECRET`, `DHIS2_OAUTH_REDIRECT_URI`, `DHIS2_OAUTH_SCOPES`). Admin bootstrap commands (`profile bootstrap`, `dev pat create`, `dev oauth2 client register`, `dev sample *`) read `DHIS2_ADMIN_PAT` / `DHIS2_ADMIN_PASSWORD` — those are NOT in `.env.auth`. For local testing the easiest path is:

```bash
export DHIS2_ADMIN_PASSWORD=district   # matches the seeded admin/district user
```

Report issues as you go — one line per red flag, file path + what went wrong.

---

## 0. Baseline — `dhis2 --help` should show seven namespaces

```bash
uv run dhis2 --help
```

Expect exactly seven commands: `analytics`, `data`, `dev`, `metadata`, `profile`, `route`, `system`. Any other namespace = plugin-discovery leak.

---

## 1. `profile` — config management + auth flows

```bash
# Offline commands first.
uv run dhis2 profile list
uv run dhis2 profile ls                      # hidden alias of `list`
uv run dhis2 profile show local
uv run dhis2 profile show local --secrets    # secrets visible
uv run dhis2 profile default local --verify
uv run dhis2 profile verify                  # verifies every profile
uv run dhis2 profile verify local            # single profile
uv run dhis2 profile verify local --json

# Add / rename / remove (idempotent — cleans up after itself).
# `profile add --auth pat` reads DHIS2_PAT from env.
uv run dhis2 profile add smoketest --url http://localhost:8080 --auth pat --verify
uv run dhis2 profile rename smoketest smoketest2 --verify
uv run dhis2 profile remove smoketest2

# OAuth2 login flow (opens a browser).
uv run dhis2 profile add local_oidc --auth oauth2 --from-env --default --verify
uv run dhis2 profile login local_oidc        # browser pops, complete consent
uv run dhis2 profile verify local_oidc
uv run dhis2 profile logout local_oidc       # clears tokens.sqlite row
uv run dhis2 profile verify local_oidc       # now fails until re-login

# Bootstrap — one-shot (provisions server-side credential + saves profile).
# Admin creds + client_secret come from DHIS2_ADMIN_PASSWORD / DHIS2_ADMIN_PAT
# / DHIS2_OAUTH_CLIENT_SECRET env vars; no argv secrets.
uv run dhis2 profile bootstrap fresh_oidc \
  --auth oauth2 \
  --url http://localhost:8080 \
  --admin-user admin \
  --client-id "smoketest-$(date +%s)" \
  --login
uv run dhis2 profile remove fresh_oidc

uv run dhis2 profile bootstrap fresh_pat \
  --auth pat \
  --url http://localhost:8080 \
  --admin-user admin \
  --pat-description "smoke test PAT"
uv run dhis2 profile remove fresh_pat
```

---

## 2. `system` — remote introspection

```bash
uv run dhis2 system whoami
uv run dhis2 system info
uv run dhis2 --profile local system whoami   # named-profile path
```

---

## 3. `metadata` — type catalog + instance list/get

```bash
# The catalog.
uv run dhis2 metadata type list
uv run dhis2 metadata type ls                # hidden alias

# Basic instance list + get.
uv run dhis2 metadata list dataElements --page-size 5
uv run dhis2 metadata list dataElements --page-size 5 --json
uv run dhis2 metadata ls dataElements --page-size 5          # alias
uv run dhis2 metadata get dataElements DEancVisit1
uv run dhis2 metadata get organisationUnits NORNorway01

# Full filter/field surface (see docs/architecture/metadata-plugin.md).
uv run dhis2 metadata list dataElements \
  --filter 'name:like:ANC' --fields 'id,name,valueType'

# Multi-filter, OR-joined.
uv run dhis2 metadata list dataElements \
  --filter 'name:like:ANC' --filter 'code:eq:DEancVisit1' --root-junction OR \
  --fields 'id,name,code'

# Ordered + paged.
uv run dhis2 metadata list organisationUnits \
  --order 'level:asc' --order 'name:asc' --page-size 5 --page 2

# `--all` streams every page server-side (ignores --page/--page-size).
uv run dhis2 metadata list dataElements --all --fields ':identifiable' --json | jq 'length'

# i18n fields.
uv run dhis2 metadata list dataElements --translate --locale fr --page-size 3
```

---

## 4. `data aggregate` — read/write aggregate data values

```bash
uv run dhis2 data aggregate get --data-set NORMonthDS1 --org-unit NOROsloProv --period 202601
uv run dhis2 data aggregate set --de DEancVisit1 --pe 202603 --ou NOROsloProv --value 88
uv run dhis2 data aggregate get --data-set NORMonthDS1 --org-unit NOROsloProv --period 202603
uv run dhis2 data aggregate delete --de DEancVisit1 --pe 202603 --ou NOROsloProv

# Bulk push from a file (create a one-value file on the fly).
# Pick a period inside the open-future window for `NORMonthDS1` — the seeded
# dataset caps future-open at 3 months. 202603 is safe when running in 2026.
cat > /tmp/dv.json <<'JSON'
{"dataValues": [{"dataElement":"DEancVisit1","period":"202603","orgUnit":"NOROsloProv","value":"77"}]}
JSON
uv run dhis2 data aggregate push /tmp/dv.json --strategy CREATE_AND_UPDATE --dry-run
uv run dhis2 data aggregate push /tmp/dv.json --strategy CREATE_AND_UPDATE
uv run dhis2 data aggregate delete --de DEancVisit1 --pe 202603 --ou NOROsloProv
```

---

## 5. `data tracker` — tracked entities, enrollments, events, relationships

The seeded e2e fixture has no tracker programs, so most of these will return `200 {}`. Verify each subcommand at least parses + dispatches cleanly.

Against a tracker-populated instance the list calls return typed pydantic models from `dhis2_client.tracker` (`TrackerEvent`, `TrackerEnrollment`, `TrackerTrackedEntity`, `TrackerRelationship`). Status fields are `StrEnum` (`EventStatus.COMPLETED`, `EnrollmentStatus.ACTIVE`, etc.). See [Typed schemas](architecture/typed-schemas.md).

`dhis2 data tracker --help` should list four top-level commands (`list`, `get`, `type`, `push`) plus three sub-typers (`enrollment`, `event`, `relationship`).

```bash
uv run dhis2 data tracker --help
uv run dhis2 data tracker list --help
uv run dhis2 data tracker get --help
uv run dhis2 data tracker type                  # empty list on seeded stack
uv run dhis2 data tracker push --help
uv run dhis2 data tracker enrollment list --help
uv run dhis2 data tracker event list --help
uv run dhis2 data tracker relationship list --help
```

Against a tracker-populated instance (e.g. `play.dhis2.org/dev`):

```bash
uv run dhis2 --profile play data tracker type                                 # discover configured types
uv run dhis2 --profile play data tracker list Person --program <PROG_UID> --page-size 5
uv run dhis2 --profile play data tracker event list --program <PROG_UID> --updated-after 2024-01-01
```

---

## 6. `analytics` — query + refresh

```bash
# All three shapes.
uv run dhis2 analytics query \
  --dim dx:DEancVisit1\;DEancVisit4 --dim pe:LAST_12_MONTHS --dim ou:NORNorway01\;LEVEL-2 --skip-meta

uv run dhis2 analytics query --shape raw \
  --dim dx:DEancVisit1 --dim pe:LAST_12_MONTHS --dim ou:NORNorway01

uv run dhis2 analytics query --shape dvs \
  --dim dx:DEancVisit1 --dim pe:LAST_12_MONTHS --dim ou:NORNorway01

# Kick off a refresh.
uv run dhis2 analytics refresh --last-years 2
```

---

## 7. `route` — integration routes

`dhis2 route list` emits JSON, so use `jq` to pull fields out.

```bash
uv run dhis2 route list
uv run dhis2 route ls                      # alias

# Create a trivial route pointing at httpbin. `route add` without --file is a
# guided interactive wizard — for scripted/automated use pass a JSON spec.
cat > /tmp/route.json <<'JSON'
{"code":"SMOKETEST","name":"smoke test","url":"https://httpbin.org/get"}
JSON
uv run dhis2 route add --file /tmp/route.json

# Grab the UID with jq and inspect. UID is a bash readonly; use ROUTE_UID.
ROUTE_UID=$(uv run dhis2 route list | jq -r '.[] | select(.code=="SMOKETEST") | .id')
uv run dhis2 route get "$ROUTE_UID"
uv run dhis2 route run "$ROUTE_UID"
uv run dhis2 route delete "$ROUTE_UID"
```

(If `route add` fails with 409 "route already exists", delete the old `SMOKETEST` code first.)

---

## 8. `dev` — codegen, uid, pat, oauth2, sample fixtures

```bash
# UID generation.
uv run dhis2 dev uid
uv run dhis2 dev uid -n 5

# Codegen — rebuilds committed schemas without touching the network.
uv run dhis2 dev codegen rebuild

# PAT provisioning (reads DHIS2_ADMIN_PAT / DHIS2_ADMIN_PASSWORD from env).
uv run dhis2 dev pat create --url http://localhost:8080 --admin-user admin \
  --description "smoke test PAT"

# OAuth2 client registration (admin creds + client_secret via env only).
uv run dhis2 dev oauth2 client register \
  --url http://localhost:8080 --admin-user admin \
  --client-id "standalone-$(date +%s)"

# Sample fixtures — each creates, verifies, cleans up (unless --keep).
uv run dhis2 dev sample route
uv run dhis2 dev sample data-value
uv run dhis2 dev sample pat
uv run dhis2 dev sample oauth2-client
uv run dhis2 dev sample all
```

---

## 9. MCP — every tool via `fastmcp.Client` in-process

Run `examples/mcp/0{1..4}_*.py` to exercise the four example scripts. Or run this quick enumeration:

```bash
uv run python - <<'PY'
import asyncio
from fastmcp import Client
from dhis2_mcp.server import build_server

async def main():
    async with Client(build_server()) as c:
        tools = await c.list_tools()
        for t in sorted(tools, key=lambda x: x.name):
            print(f"  {t.name}")
asyncio.run(main())
PY
```

Expected tool names:

- `system_whoami`, `system_info`
- `profile_list`, `profile_verify`, `profile_verify_all`, `profile_show`
- `metadata_type_list`, `metadata_list`, `metadata_get`
- `analytics_query`, `analytics_refresh`
- `data_aggregate_get`, `data_aggregate_push`, `data_aggregate_set`, `data_aggregate_delete`
- `data_tracker_list`, `data_tracker_get`, `data_tracker_type_list`, `data_tracker_push`
- `data_tracker_enrollment_list`, `data_tracker_event_list`, `data_tracker_relationship_list`
- `route_list`, `route_get`, `route_add`, `route_update`, `route_patch`, `route_delete`, `route_run`

Anything missing = regression in plugin wiring.

---

## 10. Error paths worth hitting

```bash
# Bad profile name.
uv run dhis2 profile show does_not_exist                # expect non-zero, informative

# login on a non-oauth2 profile.
uv run dhis2 profile login local                        # expect "login only applies to oauth2"

# Invalid analytics shape.
uv run dhis2 analytics query --shape garbage --dim dx:x --dim pe:y --dim ou:z

# Route run against a non-existent UID.
uv run dhis2 route run fake1234uid
```

---

## Reporting

Format issues as:

```
[cli|mcp] <command path>: <what went wrong>
  <paste of the actual output / stack trace>
```

Drop them into a scratch file or comment on the PR — easier to triage in batch than one-by-one.
