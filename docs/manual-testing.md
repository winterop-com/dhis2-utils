# Manual testing guide — every CLI + MCP surface in one pass

Purpose: a copy-pasteable sequence that exercises every `dhis2` CLI command and every MCP tool against a live stack. Use this when you want to sanity-check the surface after a refactor, or to track down a regression.

Assumes:
- `make dhis2-run` is up and `admin/district` works.
- You've run `make dhis2-seed` at least once so `infra/home/credentials/.env.auth` is populated.
- `uv sync --all-packages` has been run so `dhis2` is on `$PATH` (inside `.venv/bin`).

Report issues as you go — one line per red flag, file path + what went wrong.

---

## 0. Baseline — `dhis2 --help` should show seven namespaces

```bash
uv run dhis2 --help
```

Expect exactly seven commands: `analytics`, `data`, `dev`, `metadata`, `profile`, `route`, `system`. If any other namespace appears, something is leaking through plugin discovery.

---

## 1. `profile` — config management + auth flows

```bash
# Offline commands first.
uv run dhis2 profile list
uv run dhis2 profile ls                      # hidden alias of `list`
uv run dhis2 profile show local
uv run dhis2 profile show local --secrets    # secrets visible
uv run dhis2 profile default local --verify
uv run dhis2 profile verify                   # verifies every profile
uv run dhis2 profile verify local             # single profile
uv run dhis2 profile verify local --json

# Add / rename / remove (idempotent — cleans up after itself).
uv run dhis2 profile add smoketest --url http://localhost:8080 --auth pat --token "$(grep DHIS2_PAT infra/home/credentials/.env.auth | head -1 | cut -d= -f2)" --verify
uv run dhis2 profile rename smoketest smoketest2 --verify
uv run dhis2 profile remove smoketest2

# OAuth2 login flow (opens a browser).
set -a; source infra/home/credentials/.env.auth; set +a
uv run dhis2 profile add local_oidc --auth oauth2 --from-env --default --verify
uv run dhis2 profile login local_oidc         # browser pops, complete consent
uv run dhis2 profile verify local_oidc
uv run dhis2 profile logout local_oidc        # clears tokens.sqlite row
uv run dhis2 profile verify local_oidc        # now fails until re-login

# Bootstrap — one-shot (registers server-side OAuth2 client + saves profile + logs in).
uv run dhis2 profile bootstrap fresh_oidc \
  --url http://localhost:8080 \
  --admin-user admin --admin-pass district \
  --client-id smoketest-$(date +%s) \
  --client-secret smoketest-secret-do-not-use \
  --login
uv run dhis2 profile remove fresh_oidc
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

# Instance list + get.
uv run dhis2 metadata list dataElements --limit 5
uv run dhis2 metadata list dataElements --limit 5 --json
uv run dhis2 metadata list dataElements --filter 'name:like:ANC' --fields 'id,name,valueType'
uv run dhis2 metadata ls dataElements --limit 5           # alias
uv run dhis2 metadata get dataElements DEancVisit1
uv run dhis2 metadata get organisationUnits NORNorway01
```

---

## 4. `data aggregate` — read/write aggregate data values

```bash
uv run dhis2 data aggregate get --data-set NORMonthDS1 --org-unit NOROsloProv --period 202601
uv run dhis2 data aggregate set --de DEancVisit1 --pe 202603 --ou NOROsloProv --value 88
uv run dhis2 data aggregate get --data-set NORMonthDS1 --org-unit NOROsloProv --period 202603
uv run dhis2 data aggregate delete --de DEancVisit1 --pe 202603 --ou NOROsloProv

# Bulk push from a file (create a one-value file on the fly).
cat > /tmp/dv.json <<'JSON'
{"dataValues": [{"dataElement":"DEancVisit1","period":"202604","orgUnit":"NOROsloProv","value":"77"}]}
JSON
uv run dhis2 data aggregate push /tmp/dv.json --strategy CREATE_AND_UPDATE --dry-run
uv run dhis2 data aggregate push /tmp/dv.json --strategy CREATE_AND_UPDATE
uv run dhis2 data aggregate delete --de DEancVisit1 --pe 202604 --ou NOROsloProv
```

---

## 5. `data tracker` — entity / enrollment / event / relationship

The seeded e2e fixture has no tracker programs, so most of these will return `200 {}`. Verify each subcommand at least parses + dispatches cleanly.

Against a tracker-populated instance, the list calls return typed pydantic models from `dhis2_client.tracker` (`TrackerEvent`, `TrackerEnrollment`, `TrackerTrackedEntity`, `TrackerRelationship`). Status fields are `StrEnum` (`EventStatus.COMPLETED`, `EnrollmentStatus.ACTIVE`, etc.). See [Typed schemas](architecture/typed-schemas.md).

```bash
uv run dhis2 data tracker --help                        # expect 5 sub-domains + push
uv run dhis2 data tracker entity --help
uv run dhis2 data tracker entity list --help
uv run dhis2 data tracker entity ls --help              # alias
uv run dhis2 data tracker enrollment list --help
uv run dhis2 data tracker event list --help
uv run dhis2 data tracker relationship list --help
uv run dhis2 data tracker push --help
```

Against a tracker-populated instance (e.g. `play.dhis2.org/dev`):

```bash
uv run dhis2 --profile play data tracker entity list --program <PROG_UID> --page-size 5
uv run dhis2 --profile play data tracker event list --program <PROG_UID> --after 2024-01-01
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

```bash
uv run dhis2 route list
uv run dhis2 route ls                      # alias

# Create a trivial route pointing at httpbin.
uv run dhis2 route add --code SMOKETEST --name "smoke test" --url https://httpbin.org/get

# Grab the UID and inspect.
UID=$(uv run dhis2 route list --fields id,code | grep -B1 SMOKETEST | head -1 | awk '{print $NF}' | tr -d '"')
uv run dhis2 route get "$UID"
uv run dhis2 route run "$UID"
uv run dhis2 route delete "$UID"
```

(If `route add` fails with 409 "route already exists", delete the old `SMOKETEST` code first.)

---

## 8. `dev` — codegen, uid, oauth2 client registration

```bash
# UID generation.
uv run dhis2 dev uid
uv run dhis2 dev uid -n 5

# Codegen — rebuilds committed schemas without touching the network.
uv run dhis2 dev codegen rebuild

# OAuth2 client registration (standalone — doesn't save a profile).
uv run dhis2 dev oauth2 client register \
  --url http://localhost:8080 --admin-user admin --admin-pass district \
  --client-id standalone-smoketest --client-secret standalone-secret
# Reverse it by deleting the client metadata UID from the output.
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
- `data_tracker_entity_list`, `data_tracker_entity_get`, `data_tracker_enrollment_list`, `data_tracker_event_list`, `data_tracker_relationship_list`, `data_tracker_push`
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
