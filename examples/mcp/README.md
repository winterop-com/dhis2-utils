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
| `01_whoami.py` | `whoami`, `system_info` |
| `02_profiles.py` | `list_profiles`, `verify_profile`, `show_profile` |
| `03_metadata.py` | `list_metadata_types`, `list_metadata`, `get_metadata` |
| `04_analytics.py` | `query_analytics`, `refresh_analytics` |
