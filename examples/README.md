# dhis2-utils examples

Three parallel example trees — one per surface:

- [`client/`](client/) — `dhis2-client` Python library (low-level: you bring the auth)
- [`cli/`](cli/) — `dhis2 ...` Typer CLI (shell scripts, profile-resolved)
- [`mcp/`](mcp/) — `dhis2-mcp` FastMCP server, called in-process

Every example targets the committed e2e fixture — `make dhis2-run` ships with it out of the box, seeds auth, streams logs. Source `.env.auth` in your shell and the examples pick it up automatically.

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

uv run python examples/client/01_whoami.py
bash examples/cli/01_whoami.sh
uv run python examples/mcp/01_whoami.py
```

## Client examples ([`client/`](client/))

| File | Shows | Auth |
| --- | --- | --- |
| `01_whoami.py` | minimal client lifecycle, `/api/me` + `/api/system/info` | PAT / Basic |
| `02_list_data_elements.py` | paginated raw GET with `fields=...` | PAT / Basic |
| `03_push_data_value.py` | bulk import to `/api/dataValueSets` | PAT / Basic |
| `04_oidc_login.py` | OIDC login — PKCE, FastAPI redirect receiver, SQLite token store, auto-refresh | OAuth2 / OIDC |
| `05_org_unit_crud.py` | OU CRUD: create, read, JSON Patch update, delete | PAT / Basic |
| `06_data_set_crud.py` | dataset CRUD with DE + OU assignments in one POST | PAT / Basic |
| `07_analytics.py` | `/api/analytics` query + analytics-table refresh | PAT / Basic |
| `08_geojson.py` | `/api/organisationUnits.geojson`, validated with `geojson-pydantic` | PAT / Basic |
| `09_bootstrap.py` | zero-to-data: OU -> user scope -> DE -> DS -> sharing -> dataValue -> cleanup | PAT / Basic |
| `10_metadata_bulk_import.py` | `/api/metadata` bulk import with `importStrategy` / `dryRun` | PAT / Basic |
| `11_profile.py` | using `dhis2-core`'s `open_client` to resolve a profile from Python | resolved via profile |

## CLI examples ([`cli/`](cli/))

| File | Commands |
| --- | --- |
| `01_whoami.sh` | `dhis2 system whoami`, `dhis2 system info` |
| `02_profiles.sh` | `dhis2 profile list / verify / show` |
| `03_metadata_and_system.sh` | `dhis2 metadata type list`, `dhis2 metadata list / get`, `dhis2 dev uid` |
| `04_aggregate_data.sh` | `dhis2 data aggregate get / set / delete / push` |
| `05_analytics.sh` | `dhis2 analytics query [--shape table\|raw\|dvs] / refresh` |
| `06_tracker.sh` | `dhis2 data tracker {entity\|enrollment\|event\|relationship} list`, `data tracker push` |
| `07_oidc_login.sh` | `dhis2 profile add --auth oauth2 --from-env`, `dhis2 profile login` |
| `08_routes.sh` | `dhis2 route list / add / get / run / delete` |
| `09_dev_pat.sh` | `dhis2 dev pat create` (with `-q` for $(capture)) |
| `10_dev_sample.sh` | `dhis2 dev sample route / data-value / pat / oauth2-client / all` |

## MCP examples ([`mcp/`](mcp/))

| File | Tools |
| --- | --- |
| `01_whoami.py` | `system_whoami`, `system_info` |
| `02_profiles.py` | `profile_list`, `profile_verify`, `profile_show` (read-only by design) |
| `03_metadata.py` | `metadata_type_list`, `metadata_list`, `metadata_get` |
| `04_analytics.py` | `analytics_query`, `analytics_refresh` |

## Environment

- `DHIS2_URL` — default `http://localhost:8080`
- `DHIS2_PAT` — a Personal Access Token
- `DHIS2_USERNAME`, `DHIS2_PASSWORD` — Basic auth fallback
- `DHIS2_OAUTH_CLIENT_ID` / `_SECRET` / `_REDIRECT_URI` / `_SCOPES` — for the OIDC example
- `DHIS2_PROFILE` — pick a named profile from `profiles.toml` without hardcoding creds
