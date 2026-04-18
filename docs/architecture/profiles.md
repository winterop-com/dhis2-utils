# Profiles — multi-instance DHIS2 configuration

A **profile** is a named bundle of "how to reach one DHIS2 instance" — a base URL plus credentials. You can have as many as you want, switch between them from the CLI, and target a specific one per MCP tool call.

## Where profiles live

Two TOML files, both read on every tool invocation:

| Scope | Path | When to use it |
| --- | --- | --- |
| Project | `<cwd or ancestor>/.dhis2/profiles.toml` | Instance tied to a specific project — `cd` into the dir, profile auto-applies |
| User-wide | `~/.config/dhis2/profiles.toml` | Instances you use everywhere — laptop-default, your personal play server, a production instance |

Project file wins over global for any profile name that exists in both.

Both files live under a **directory** (`.dhis2/` / `~/.config/dhis2/`), not as loose files, so we can drop other per-scope config next to them later (token store, cache DB, preferences) without moving things around.

## File shape

```toml
default = "prod"

[profiles.local]
base_url = "http://localhost:8080"
auth = "pat"
token = "d2p_..."

[profiles.play]
base_url = "https://play.im.dhis2.org/dev"
auth = "basic"
username = "system"
password = "System123"

[profiles.prod]
base_url = "https://dhis2.example.org"
auth = "pat"
token = "d2p_..."
```

The file is written with `0600` perms when created by `dhis2 profile add`. Gitignore `.dhis2/profiles.toml` — it contains secrets.

## Resolution precedence

Every tool call (CLI or MCP) resolves a profile through this chain. Highest wins:

```
1. Explicit argument             ← CLI `--profile NAME`, MCP tool arg `profile="NAME"`
2. DHIS2_PROFILE env var         ← set by MCP server config, shell export, or CLI callback
3. DHIS2_URL + DHIS2_PAT/... env ← raw env (no TOML needed) — backward compat
4. Project TOML default          ← nearest `.dhis2/profiles.toml` walking up from $PWD
5. User-wide TOML default        ← `~/.config/dhis2/profiles.toml`
6. NoProfileError                ← with a clear message telling you to run `dhis2 profile add`
```

Project overrides global for any profile name that exists in both (merged in `load_catalog()`).

## CLI

```bash
dhis2 profile list                        # see every profile (project + global) with default marker
dhis2 profile verify                      # hit /api/system/info + /api/me on every profile; one-line OK/FAIL per
dhis2 profile verify prod                 # verify just one — exit code 0 if ok, 1 if not
dhis2 profile show prod                   # pretty-print one profile (secrets redacted)
dhis2 profile show prod --secrets         # including secrets (for copy-paste debugging)

# Add a PAT-based profile to the user-wide file, make it default
dhis2 profile add prod \
  --scope global \
  --url https://dhis2.example.org \
  --auth pat --token d2p_... \
  --default

# Add a basic-auth profile to the project .dhis2/profiles.toml (scope=project is the default)
dhis2 profile add local \
  --url http://localhost:8080 \
  --auth basic --username admin --password district

dhis2 profile switch prod                 # set default = prod in project file
dhis2 profile switch prod --scope global  # set default = prod in ~/.config/dhis2/profiles.toml

dhis2 profile remove prod                 # removes from wherever it lives
```

## Global `--profile` flag

Every `dhis2` command accepts `--profile NAME` at the root:

```bash
dhis2 --profile prod system whoami
dhis2 -p staging metadata list dataElements
```

The flag sets `DHIS2_PROFILE` for the rest of the invocation, which flows through to every plugin's service call.

## MCP

**Every tool** accepts an optional `profile: str | None = None` kwarg. Agent flow:

```
1. Agent calls `list_profiles` →
   [{"name": "local", "default": false, "source": "global-toml", ...},
    {"name": "prod",  "default": true,  "source": "global-toml", ...}]

2. Agent calls `verify_profile("prod")` →
   {"ok": true, "version": "2.42.4", "username": "admin", "latency_ms": 180}

3. Agent calls any other tool targeting that profile →
   `list_metadata(resource="dataElements", profile="prod")`
   `get_data_values(data_set="X", org_unit="Y", profile="prod")`
   `query_analytics(dimensions=[...], profile="prod")`
```

If the agent omits `profile`, resolution falls through to `DHIS2_PROFILE` env (from the MCP server config), then raw env, then TOML default — same chain as the CLI.

### Why writes are CLI-only

`list_profiles`, `verify_profile`, `verify_all_profiles`, `show_profile` are exposed as MCP tools — they're read-only and safe. `add_profile`, `remove_profile`, `set_default_profile` are **deliberately not** MCP tools — letting an autonomous agent rewrite your credential files is the wrong default. Mutations go through the CLI, where a human is on the keyboard.

## Running multiple MCP servers against different profiles

Easiest way to connect one agent to several DHIS2 instances is register multiple MCP servers, each with a different env:

```json
{
  "mcpServers": {
    "dhis2-local": {
      "command": "uv", "args": ["run", "dhis2-mcp"],
      "env": { "DHIS2_PROFILE": "local" }
    },
    "dhis2-prod": {
      "command": "uv", "args": ["run", "dhis2-mcp"],
      "env": { "DHIS2_PROFILE": "prod" }
    }
  }
}
```

Each server picks up its named profile from `~/.config/dhis2/profiles.toml` via `DHIS2_PROFILE`. The agent sees two disjoint tool namespaces (`dhis2-local/whoami`, `dhis2-prod/whoami`) and picks whichever it needs.

Alternatively: register **one** MCP server and pass `profile="prod"` per tool call. Same result, different ergonomics.

## Full end-to-end: from zero to "I'm querying prod"

```bash
# 1. Add one profile, user-wide, make it default.
dhis2 profile add prod \
  --scope global \
  --url https://dhis2.example.org \
  --auth pat --token d2p_... \
  --default

# 2. Verify the auth works.
dhis2 profile verify prod
# OK prod  https://dhis2.example.org  auth=pat  version=2.42.4  user=admin  182 ms

# 3. Use it from the CLI (implicit default).
dhis2 system whoami
dhis2 metadata list dataElements --limit 10

# 4. Or target it explicitly.
dhis2 --profile prod metadata get dataElements fbfJHSPpUQD

# 5. Restart your MCP client. The agent sees `prod` via `list_profiles`
#    and calls `get_metadata(resource="dataElements", uid="...", profile="prod")`.
```

## Security

- Profile files are written with `0600` perms.
- Gitignore **`.dhis2/profiles.toml`** if you're storing a project-scoped file in a versioned repo.
- Secrets are redacted in `dhis2 profile show` unless `--secrets` is passed.
- `show_profile` MCP tool redacts unconditionally.
- No plaintext secrets appear in logs.

Planned: OS-keyring-backed storage for OAuth2 tokens (and optionally PATs) so the TOML only holds a reference, not the raw secret.

## What's not in profiles yet

- **OAuth2 end-to-end integration.** The `auth = "oauth2"` schema is accepted by the pydantic model (and the seeded `.env.auth` carries client credentials), but `dhis2-client`'s OAuth2Auth still needs to be wired into `client_context.build_auth()` for the profile pipeline. Adding it is ~10 lines when needed.
- **Per-profile token caches.** `dhis2-core/token_store.py` (SQLAlchemy+SQLite) is designed for OAuth2 tokens, lives next to the profiles file, but isn't active yet.
- **Profile import/export.** `dhis2 profile export prod > prod.toml` is a trivial add when we want to share profile shapes (without secrets) between machines.
- **Interactive `dhis2 init`.** Walks through the first-time setup, prompts for URL + auth choice, optionally mints a PAT via `dhis2-browser`. Skeleton is ready; just hasn't been implemented yet.

## Design decisions

- **Name-as-ID, not UUID.** You pick the name at creation time. Short, readable, stable. No separate identifier to remember.
- **Directories, not loose files.** `.dhis2/` at project root, `~/.config/dhis2/` user-wide. We'll drop cache DBs and token stores in there later without moving anything.
- **Project > global.** A profile named `prod` in the project wins over a global `prod`. Lets a single project override defaults without affecting other work.
- **Writes are CLI-only in MCP.** `list_profiles` / `verify_profile` / `show_profile` are read-only and safe; `add` / `remove` / `switch` stay CLI-only because agents shouldn't rewrite credential files autonomously.
- **Backward-compatible raw env.** `DHIS2_URL + DHIS2_PAT` (no TOML) still works — the resolver treats it as a synthetic profile with source `env-raw`. Useful for CI and one-off shell invocations.
