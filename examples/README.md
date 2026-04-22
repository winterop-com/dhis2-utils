# dhis2-utils examples

Three parallel example trees — one per surface:

- [`client/`](client/) — `dhis2-client` Python library (low-level: you bring the auth)
- [`cli/`](cli/) — `dhis2 ...` Typer CLI (shell scripts, profile-resolved)
- [`mcp/`](mcp/) — `dhis2-mcp` FastMCP server, called in-process

Every example targets the committed e2e fixture — `make dhis2-run` ships with it out of the box, seeds auth, streams logs. Source `.env.auth` in your shell and the examples pick it up automatically.

Filenames describe what each example shows — no sequential numbering. Every domain has a script per surface where possible (e.g. `tracker_reads.*`, `analytics_query.*`, `user_administration.*`).

## Which surface should I use?

| Surface | Best for | Auth handling |
| --- | --- | --- |
| `dhis2-client` (library) | Your own Python tooling; scripts in-process | You pass `AuthProvider` explicitly (Basic, PAT, OAuth2) — no profile layer |
| `dhis2 <cmd>` (CLI) | Day-to-day dev, pipelines, human use | Reads `~/.config/dhis2/profiles.toml` + env; `dhis2 profile add/login` manages creds |
| `dhis2-mcp` (MCP) | Agents, automation over the MCP protocol | Same profile layer as the CLI; mutations intentionally not exposed |

All three hit DHIS2 via `Dhis2Client` under the hood. Pick the shape that fits your caller. See [Workspace layout](../docs/architecture/workspace.md) for the dependency arrows.

## Running

```bash
make dhis2-run                       # foreground DHIS2 + seeded auth (Ctrl+C stops)
# second terminal:
set -a; source infra/home/credentials/.env.auth; set +a

uv run python examples/client/whoami.py
bash examples/cli/whoami.sh
uv run python examples/mcp/whoami.py
```

## Client examples ([`client/`](client/))

| File | Shows | Auth |
| --- | --- | --- |
| `whoami.py` | minimal client lifecycle, `/api/me` + `/api/system/info` | PAT / Basic |
| `list_data_elements.py` | paginated raw GET with `fields=...` | PAT / Basic |
| `push_data_value.py` | bulk import to `/api/dataValueSets` | PAT / Basic |
| `oidc_login.py` | OIDC login — PKCE, FastAPI redirect receiver, SQLite token store, auto-refresh | OAuth2 / OIDC |
| `org_unit_crud.py` | OU CRUD: create, read, JSON Patch update, delete | PAT / Basic |
| `data_set_crud.py` | dataset CRUD with DE + OU assignments in one POST | PAT / Basic |
| `analytics_query.py` | `/api/analytics` query + analytics-table refresh | PAT / Basic |
| `analytics_events_enrollments.py` | `/api/analytics/events/query` + `/enrollments/query` | PAT / Basic |
| `geojson_org_units.py` | `/api/organisationUnits.geojson`, validated with `geojson-pydantic` | PAT / Basic |
| `bootstrap_zero_to_data.py` | zero-to-data: OU → user scope → DE → DS → sharing → dataValue → cleanup | PAT / Basic |
| `metadata_bulk_import.py` | `/api/metadata` bulk import with `importStrategy` / `dryRun` | PAT / Basic |
| `metadata_filter_order_paging.py` | metadata filter DSL: multi-filter OR/AND, multi-order, paging, `--all` | PAT / Basic |
| `profile_resolver.py` | using `dhis2-core`'s `open_client` to resolve a profile from Python | resolved via profile |
| `tracker_lifecycle.py` | tracker `/api/tracker` — tracked entity + enrollment + event in one atomic POST | PAT / Basic |
| `tracker_clinic_intake.py` | canonical flow via `client.tracker.register` + `add_event` + `outstanding` — tracker program | PAT / Basic |
| `tracker_event_program.py` | event-only (WITHOUT_REGISTRATION) workflow — standalone `add_event` calls | PAT / Basic |
| `metadata_search.py` | cross-resource UID / code / name search via `client.metadata.search` | PAT / Basic |
| `metadata_usage.py` | reverse lookup "what references this UID?" via `client.metadata.usage` | PAT / Basic |
| `error_handling.py` | `Dhis2ApiError` / `AuthenticationError`, WebMessage conflicts, rejected indexes | PAT / Basic |
| `indicator_crud.py` | typed `Indicator` with numerator/denominator formulas, IndicatorType reference | PAT / Basic |
| `task_polling.py` | poll `/api/system/tasks/<type>/<uid>` — the shared pattern for every async op | PAT / Basic |
| `enum_round_trip.py` | generated `StrEnum`s (`ValueType.NUMBER`, `DataElementDomain.AGGREGATE`, `PeriodType.MONTHLY`) | PAT / Basic |
| `user_administration.py` | list/get users, `/api/me`, invite + reset-password envelope shapes | PAT / Basic |
| `sharing.py` | typed `SharingBuilder` + `apply_sharing` over `/api/sharing` | PAT / Basic |
| `user_groups_and_roles.py` | user groups, user roles, authorities listing | PAT / Basic |

## CLI examples ([`cli/`](cli/))

| File | Commands |
| --- | --- |
| `whoami.sh` | `dhis2 system whoami`, `dhis2 system info` |
| `profile_list_verify.sh` | `dhis2 profile list / verify / show` |
| `metadata_list_get.sh` | `dhis2 metadata type list`, `dhis2 metadata list / get`, `dhis2 dev uid` |
| `aggregate_data_values.sh` | `dhis2 data aggregate get / set / delete / push` |
| `analytics_query.sh` | `dhis2 analytics query [--shape table\|raw\|dvs] / refresh` |
| `tracker_reads.sh` | `dhis2 data tracker type`, `list <TET>`, `get <uid>`, `{enrollment,event,relationship} list`, `push` |
| `tracker_register_and_followup.sh` | `dhis2 data tracker register / event create / outstanding` — tracker-program clinic intake |
| `tracker_event_program.sh` | `dhis2 data tracker event create --program EVTsupVis01` — event-only flow |
| `metadata_search.sh` | `dhis2 metadata search` — full UID / partial UID / code / name / `--resource` / `--fields` / `--exact` |
| `profile_oidc_login.sh` | `dhis2 profile add --auth oauth2 --from-env`, `dhis2 profile login` |
| `route_register_and_run.sh` | `dhis2 route list / add / get / run / delete` (all 5 auth types) |
| `dev_pat.sh` | `dhis2 dev pat create` (`-q` for capture) |
| `dev_sample.sh` | `dhis2 dev sample route / data-value / pat / oauth2-client / all` |
| `dev_codegen.sh` | `dhis2 dev codegen generate / rebuild / oas-rebuild` |
| `maintenance.sh` | `dhis2 maintenance task types/list/status/watch`, `cache`, `cleanup`, `dataintegrity list/run/result` |
| `user_administration.sh` | `dhis2 user list / get / me / invite / reinvite / reset-password` |
| `user_groups_and_roles.sh` | `dhis2 user-group {list,get,add-member,sharing-get,sharing-grant-user}`, `dhis2 user-role {list,get,authorities,add-user}` |

## MCP examples ([`mcp/`](mcp/))

| File | Tools |
| --- | --- |
| `whoami.py` | `system_whoami`, `system_info` |
| `profile_tools.py` | `profile_list`, `profile_verify`, `profile_show` (read-only by design) |
| `metadata.py` | `metadata_type_list`, `metadata_list`, `metadata_get` |
| `analytics_query.py` | `analytics_query`, `analytics_refresh` |
| `analytics_events_enrollments.py` | `analytics_events_query`, `analytics_enrollments_query` |
| `maintenance.py` | `maintenance_task_types`, `maintenance_dataintegrity_*`, `maintenance_cache_clear` |
| `aggregate_data_values.py` | `data_aggregate_get / set / delete` |
| `tracker_reads.py` | `data_tracker_type_list`, `data_tracker_list`, `data_tracker_event_list` |
| `tracker_workflow.py` | `data_tracker_register`, `data_tracker_event_create`, `data_tracker_outstanding` |
| `metadata_search.py` | `metadata_search` — cross-resource UID / code / name lookup |
| `metadata_usage.py` | `metadata_usage` — reverse reference lookup |
| `route_register_and_run.py` | `route_list`, `route_add`, `route_run`, `route_delete` |
| `user_administration.py` | `user_list / get / me / invite / reinvite / reset-password` |
| `sharing_and_user_groups.py` | `user_group_list / get / sharing_get`, `user_role_list / authorities` |

## Environment

- `DHIS2_URL` — default `http://localhost:8080`
- `DHIS2_PAT` — a Personal Access Token
- `DHIS2_USERNAME`, `DHIS2_PASSWORD` — Basic auth fallback
- `DHIS2_OAUTH_CLIENT_ID` / `_SECRET` / `_REDIRECT_URI` / `_SCOPES` — for the OIDC example
- `DHIS2_PROFILE` — pick a named profile from `profiles.toml` without hardcoding creds
