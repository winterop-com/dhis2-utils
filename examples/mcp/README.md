# MCP examples

Examples that connect to the `dhis2` FastMCP server in-process and call its tools. Useful both as a reference for integrating the MCP server into an agent framework and as a quick sanity-check of what tools each plugin registers.

Every example uses FastMCP's in-process `Client(server)` — no stdio transport, no subprocess. Same pattern used by `packages/dhis2-mcp/tests/*_integration.py`.

## Prerequisites

```bash
make dhis2-run                       # DHIS2 + seeded auth
set -a; source infra/home/credentials/.env.auth; set +a
```

The MCP tools read the same `DHIS2_URL` / `DHIS2_PAT` / `DHIS2_PROFILE` env contract as the CLI.

## Scripts

| File | MCP tools exercised |
|------|---------------------|
| `whoami.py` | `system_whoami`, `system_info` |
| `profile_tools.py` | `profile_list`, `profile_verify`, `profile_show` |
| `metadata.py` | `metadata_type_list`, `metadata_list`, `metadata_get` |
| `analytics_query.py` | `analytics_query`, `analytics_refresh` |
| `analytics_events_enrollments.py` | `analytics_events_query`, `analytics_enrollments_query` |
| `maintenance.py` | `maintenance_task_*`, `maintenance_dataintegrity_*`, `maintenance_cache_clear` |
| `aggregate_data_values.py` | `data_aggregate_get / set / delete` |
| `tracker_reads.py` | `data_tracker_type_list / list / event_list / enrollment_list` |
| `route_register_and_run.py` | `route_list / add / run / delete` |
| `user_administration.py` | `user_list / get / me / invite / reinvite / reset-password` |
| `sharing_and_user_groups.py` | `user_group_*`, `user_role_*` |
