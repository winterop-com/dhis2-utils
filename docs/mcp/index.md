# `dhis2w-mcp` MCP server

`dhis2w-mcp` is a [FastMCP](https://github.com/jlowin/fastmcp) server that exposes every `dhis2w-core` plugin as a typed [Model Context Protocol](https://modelcontextprotocol.io/) tool. An AI agent (Claude Desktop, Claude Code, Cursor, Continue, Cline, or anything that speaks stdio MCP) launches it and gets 337+ typed tools — every CLI command has a matching MCP tool sharing the same typed service function.

## When to reach for it

- Driving DHIS2 from an LLM agent — "create a program with these attributes, link these org units, push a sample row."
- Building agent-assisted operations on a live DHIS2 stack where every tool call surfaces a typed result and a typed error.
- Auditing what an agent is doing against DHIS2 — every tool call is logged with its arguments.

For direct CLI use, the [CLI surface](../cli/index.md) is what you want. For Python integration, the [Python client](../client/index.md).

## Install

Two install paths depending on whether you want the binary on your global `PATH` or pinned inside a project.

### Global (laptop-wide) — recommended for AI host integration

`uv tool install` puts the `dhis2w-mcp` binary into uv's tool bin directory (which lives on `PATH` after `uv tool update-shell`). Every MCP host on your laptop can launch it without knowing where it's installed.

```bash
uv tool install dhis2w-mcp
dhis2w-mcp --version
```

Update later:

```bash
uv tool upgrade dhis2w-mcp                 # latest
uv tool install --reinstall dhis2w-mcp==0.10.1   # pin a specific version
uv tool uninstall dhis2w-mcp               # remove
```

If `dhis2w-mcp` isn't on `PATH` after install, run `uv tool update-shell` once and restart your terminal.

### One-shot via `uvx` (no install)

To launch the server without persisting it on disk (good for trying a single agent session):

```bash
uvx dhis2w-mcp
```

Each `uvx` invocation re-creates a temporary environment, so it's slower than the `uv tool install` path. Use `uv tool install` for daily use.

### Local-to-a-project (pinning a specific version)

When you want the server pinned in a project's `uv.lock` (e.g. a dev tools project that wraps your DHIS2 agent flows):

```bash
uv add --dev dhis2w-mcp
uv run dhis2w-mcp --version
```

The host launches it as `uv run --directory /path/to/project dhis2w-mcp` (see the host-specific configs below).

### From the workspace checkout (developing dhis2w-mcp itself)

If you cloned `dhis2-utils` to hack on the server:

```bash
git clone git@github.com:winterop-com/dhis2w-utils.git
cd dhis2w-utils
make install                               # uv sync --all-packages
uv run dhis2w-mcp --version
```

Host configs point at `uv run --directory <repo-path> dhis2w-mcp`.

## Wiring it into an AI host

The same `dhis2w-mcp` binary plugs into every MCP-aware host. Pick yours below.

### Claude Desktop

Config file location:

| Platform | Path |
| --- | --- |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

Open the file (create it if it doesn't exist) and add:

```json
{
  "mcpServers": {
    "dhis2": {
      "command": "dhis2w-mcp"
    }
  }
}
```

Quit + reopen Claude Desktop. The MCP server tray shows a green dot next to "dhis2"; click it to see the 337+ tools the agent has access to.

To pass extra env vars (e.g. pin the plugin tree or active profile):

```json
{
  "mcpServers": {
    "dhis2": {
      "command": "dhis2w-mcp",
      "env": {
        "DHIS2_VERSION": "43",
        "DHIS2_PROFILE": "staging"
      }
    }
  }
}
```

If you installed locally to a project, point the host at `uv run`:

```json
{
  "mcpServers": {
    "dhis2": {
      "command": "uv",
      "args": ["run", "--directory", "/Users/you/dev/your-agent-project", "dhis2w-mcp"]
    }
  }
}
```

### Claude Code

`claude` (the CLI) reads MCP servers from `~/.claude.json` (per-user) or `.claude/mcp_servers.json` (per-project). The shape is the same as Claude Desktop:

```bash
claude mcp add dhis2 dhis2w-mcp
# or, manually:
cat >> ~/.claude.json <<'JSON'
{
  "mcpServers": {
    "dhis2": { "command": "dhis2w-mcp" }
  }
}
JSON
```

Restart the Claude Code session (`exit` + relaunch) to pick up the new server.

### Cursor

In Cursor settings -> MCP -> "Edit config", add the same JSON block as Claude Desktop. Cursor stores it at `~/.cursor/mcp.json`.

### Continue / Cline / generic stdio hosts

Any MCP host that supports stdio takes:

```
command: dhis2w-mcp
args:    []
env:     { ... optional ... }
```

Drop those into the host's MCP config UI / file. If the host wants the full path to the binary, `uv tool which dhis2w-mcp` prints it.

## Verifying the wiring

In the agent, ask:

> Call `system_server_info` and show me the result.

The response should carry:

```json
{
  "active_plugin_tree": "v43",
  "active_plugin_tree_source": "default (no profile.version, no DHIS2_VERSION env)",
  "dhis2w_core_version": "0.10.0",
  "dhis2w_mcp_version": "0.10.0"
}
```

If the agent says it has zero MCP tools, the host hasn't loaded the server — check the MCP panel / log for the start-up error.

## Profile selection

The server picks its DHIS2 profile from the standard `dhis2w-core` resolution chain: walking up for `.dhis2/profiles.toml`, falling back to `~/.config/dhis2/profiles.toml`. Every MCP tool also accepts an explicit `profile: str | None` kwarg so an agent can target any configured profile per call without restarting the server.

## Active plugin tree

`dhis2w-mcp` selects a plugin tree (v41 / v42 / v43) at startup. Override per-launch with the `DHIS2_VERSION` env var:

```bash
DHIS2_VERSION=43 dhis2w-mcp
```

In a host config, set it under the `env:` block (see Claude Desktop example above). Call `system_server_info` from the agent to see which tree is bound + which `dhis2w-*` package versions are installed.

## Where next

- [Tutorial](tutorial.md) — your first MCP tool call from an agent.
- [Reference](../mcp-reference.md) — auto-generated catalog of every tool + parameter schema.
- [Architecture](../architecture/mcp.md) — how the FastMCP server mounts plugins, return-shape conventions.
- [Examples index](../examples.md) — Python scripts driving the in-process MCP server end-to-end.
