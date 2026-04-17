# Walkthrough

Step-by-step from an empty repo to a fully working DHIS2 client with typed CRUD, system info, codegen, and Playwright-minted PATs. **Update this file every time a feature lands.**

Each step shows the exact shell command (or code snippet), what it does, and what you should expect to see.

---

## Step 1 — install the workspace

```bash
cd /Users/morteoh/dev/winterop/dhis2-utils
make install
```

Runs `uv sync --all-packages --all-extras` at the workspace root. Installs all six members in editable mode plus dev tools (ruff, mypy, pyright, pytest, respx, mkdocs-material, mkdocs-claude-theme).

Expect: ~120 packages installed.

---

## Step 2 — verify the scaffold

```bash
make lint
make test
```

- `make lint` runs `ruff format`, `ruff check --fix`, `mypy --explicit-package-bases packages`, and `pyright`. All three must pass.
- `make test` runs pytest excluding `@pytest.mark.slow` tests.

Expect: both green, ~31 unit tests passing.

---

## Step 3 — spin up a local DHIS2 (recommended)

The `infra/` directory ships a docker-compose stack. Full details in [Local DHIS2 setup](local-setup.md).

```bash
make dhis2-versions          # see what DHIS2 images you could pull
make dhis2-up DHIS2_VERSION=42
make dhis2-status            # wait for "HTTP 200" to confirm it's ready
```

Defaults to DHIS2 42, admin / district, http://localhost:8080.

Verify with an authenticated call from `dhis2-client` itself — no curl:

```bash
uv run python -c "
import asyncio
from dhis2_client import Dhis2Client, BasicAuth
async def main():
    async with Dhis2Client('http://localhost:8080', auth=BasicAuth('admin','district'), allow_version_fallback=True) as client:
        info = await client.system.info()
        print('version:', info.version)
asyncio.run(main())
"
```

Expect: `version: 2.42.x`.

---

## Step 4 — generate the versioned client

DHIS2 schemas differ by version. `dhis2-codegen` hits `/api/schemas` and emits pydantic models + typed CRUD accessors into `packages/dhis2-client/src/dhis2_client/generated/v{NN}/`.

```bash
uv run python -m dhis2_codegen \
  --url http://localhost:8080 \
  --username admin \
  --password district
```

Expect:

```
discovering http://localhost:8080
  version: 2.42.4 (→ v42)
  schemas: 119
emitting packages/dhis2-client/src/dhis2_client/generated/v42
done — generated 119 schemas ...
```

The `v42/` folder now has `__init__.py` (with `GENERATED = True`), `resources.py` (CRUD per resource), `schemas_manifest.json` (audit trail), and `models/*.py` (one pydantic model per metadata type).

---

## Step 5 — verify the generated code compiles cleanly

```bash
make lint
make test
```

Expect: still green. Generated files pass ruff + mypy + pyright without any manual touch-up.

---

## Step 6 — use the typed resources

```python
import asyncio
from dhis2_client import Dhis2Client, BasicAuth

async def main():
    async with Dhis2Client(
        base_url="http://localhost:8080",
        auth=BasicAuth("admin", "district"),
    ) as client:
        # system endpoints (hand-written)
        me = await client.system.me()
        print(me.username, me.authorities[:3] if me.authorities else [])

        # typed metadata list
        elements = await client.resources.data_elements.list(fields="id,name")
        print(f"{len(elements)} data elements")

        # typed get by UID
        if elements:
            de = await client.resources.data_elements.get(elements[0].id)
            print(de.name)

asyncio.run(main())
```

Expect: your username, first three authorities, a data-element count, and the first element's name.

---

## Step 7 — create a Personal Access Token via Playwright

Basic auth works, but PATs are better for automation. `dhis2-browser` automates the DHIS2 login UI and creates a PAT via the authenticated API in one shot.

```bash
uv run python -m dhis2_browser pat \
  --url http://localhost:8080 \
  --username admin \
  --password district \
  --name "dhis2-utils-local" \
  --expires-in-days 30 \
  --allowed-method GET \
  --allowed-method POST \
  --allowed-method PUT \
  --allowed-method DELETE
```

The browser opens (visible by default — use `--headless` to hide). You'll see the login page auto-filled and submitted. After the redirect, the command prints the new token:

```
d2p_DVWAOHXvKTkyFFp96eABNHuqg51wo0yKWgBA6L4koepU4Bj8ab
```

Save this — DHIS2 shows it only once.

---

## Step 8 — use the PAT for auth

```python
import asyncio
from dhis2_client import Dhis2Client, PatAuth

async def main():
    token = "d2p_..."
    async with Dhis2Client("http://localhost:8080", auth=PatAuth(token=token)) as client:
        me = await client.system.me()
        print(me.username)

asyncio.run(main())
```

The header sent is `Authorization: ApiToken d2p_...`. No username/password anywhere near the wire.

---

## Step 9 — run integration tests against the live instance

```bash
# optional: reuse the PAT from step 7 across test sessions
export DHIS2_LOCAL_PAT=d2p_...

make test-slow
```

If `DHIS2_LOCAL_PAT` is unset, the `local_pat` fixture auto-mints a fresh one via Playwright (~5s), then runs destructive CRUD tests (create/update/delete a test Constant) against localhost.

Expect: ~6–8 integration tests passing (3 public play/dev tests + 1 typed end-to-end against play/dev + PAT round-trip + destructive CRUD on localhost).

---

## Step 10 — use the CLI

Both the plugin-discovery machinery and the `system` plugin are wired end-to-end. With the seeded `.env.auth` sourced, the CLI just works:

```bash
set -a; source infra/home/credentials/.env.auth; set +a

dhis2 --help
# → lists the system (builtin) and codegen (entry-point) plugins

dhis2 system whoami
# → admin (System Administrator)

dhis2 system info
# → version=2.42.4 revision=eaf4b70 name=DHIS 2

dhis2 codegen --help
# → dhis2-codegen's sub-app mounted via entry point
```

See [dhis2 CLI](architecture/cli.md) for the Typer root design and [Plugin runtime](architecture/plugins.md) for how plugins get discovered.

## Step 11 — use the MCP server

The same capabilities are available to AI agents via `dhis2-mcp`. Configure an MCP client (Claude Code, Cursor, etc.) with:

```json
{
  "mcpServers": {
    "dhis2": {
      "command": "uv",
      "args": ["run", "dhis2-mcp"],
      "env": {
        "DHIS2_URL": "http://localhost:8080",
        "DHIS2_PAT": "d2p_..."
      }
    }
  }
}
```

Restart your MCP client and ask your agent "what DHIS2 user am I authenticated as?" — it calls the `whoami` tool and reports back.

See [dhis2-mcp server](architecture/mcp.md) for tool registration mechanics and in-process testing.

## Step 12 — browse the docs

```bash
make docs-serve
```

Opens `http://127.0.0.1:8000` with the mkdocs-claude-theme site. Architecture, codegen, PAT helper, testing strategy, decisions log, and lessons learned all live under `docs/`.

---

## What's in place today

| Capability | Status | Where |
| --- | --- | --- |
| Async httpx client with pluggable auth | Done | `dhis2-client` |
| Basic / PAT / OAuth2-PKCE providers | Done | `dhis2-client/auth/` |
| Version-aware dispatch via `/api/system/info` | Done | `dhis2-client/client.py` |
| `client.system.info()` / `client.system.me()` | Done | `dhis2-client/system.py` |
| Codegen from `/api/schemas` → pydantic + CRUD | Done | `dhis2-codegen`, output in `dhis2-client/generated/` |
| Filesystem-scan version discovery | Done | `dhis2-client/generated/__init__.py` |
| Playwright-minted PATs with options (name, expiry, IP/method/referrer allowlists) | Done | `dhis2-browser/pat.py` |
| `dhis2-browser` Typer CLI (`pat`, `info`) | Done | `dhis2-browser/cli.py` |
| Plugin runtime (Protocol + built-in + entry-point discovery) | Done | `dhis2-core/plugin.py` |
| Profile resolution from environment | Done | `dhis2-core/profile.py` |
| First-party `system` plugin (CLI + MCP surfaces) | Done | `dhis2-core/plugins/system/` |
| `dhis2` CLI root with plugin mounting | Done | `dhis2-cli/main.py` |
| `dhis2-mcp` FastMCP server with plugin mounting | Done | `dhis2-mcp/server.py` |
| Local Docker stack (DHIS2 + pgAdmin + Superset) | Done | `infra/` |
| Seeded auth: 6 PAT variations + OAuth2 client | Done | `infra/scripts/seed_auth.py` |
| Tests auto-source `infra/home/credentials/.env.auth` | Done | conftest fixtures |
| Unit tests (respx, CliRunner, in-process FastMCP Client) | Done | 42 passing |
| Integration tests against play/dev + localhost | Done | 12 passing |
| Destructive CRUD round-trip tests (constants) | Done | `test_integration_local_pat.py` |
| CLI end-to-end tests (`dhis2 system whoami/info` live) | Done | `test_cli_integration.py` |
| MCP end-to-end tests (in-process client calls `whoami`/`system_info`) | Done | `test_mcp_integration.py` |
| Docs site with mkdocs-claude-theme | Done | `docs/`, nav in `mkdocs.yml` |

## What's next

| Capability | Status |
| --- | --- |
| Tracker plugin (`/api/tracker/*` — tracked entities, enrollments, events) | Not started |
| Data values plugin (`/api/dataValueSets`, `/api/dataValues`) | Not started |
| Analytics plugin + query DSL (`/api/analytics`) | Not started |
| Bulk metadata import (`/api/metadata`) | Not started |
| Profile system beyond env vars (`.dhis2/profiles.toml`, `dhis2 init`) | Not started |
| First-party plugins for metadata domains (dataElements, indicators, orgUnits, ...) | Not started (generated CRUD covers low level; CLI+MCP wrappers pending) |
