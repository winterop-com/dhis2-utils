# `dhis2w-mcp` MCP server

`dhis2w-mcp` is a [FastMCP](https://github.com/jlowin/fastmcp) server that exposes every `dhis2w-core` plugin as a typed [Model Context Protocol](https://modelcontextprotocol.io/) tool. An AI agent (Claude Desktop, Claude Code, Cursor, or anything that speaks stdio MCP) launches it and gets 337+ typed tools — every CLI command has a matching MCP tool sharing the same typed service function.

## When to reach for it

- Driving DHIS2 from an LLM agent — "create a program with these attributes, link these org units, push a sample row."
- Building agent-assisted operations on a live DHIS2 stack where every tool call surfaces a typed result and a typed error.
- Auditing what an agent is doing against DHIS2 — every tool call is logged with its arguments.

For direct CLI use, the [CLI surface](../cli/index.md) is what you want. For Python integration, the [Python client](../client/index.md).

## Install

`dhis2w-mcp` is its own PyPI package; install as a uv tool so any MCP host can launch it from PATH:

```bash
uv tool install dhis2w-mcp
dhis2w-mcp --version
```

## Wiring it into an MCP host

### Claude Desktop / Claude Code

Add to your MCP server config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS, or `~/.config/claude-desktop/mcp_servers.json` on Linux):

```json
{
  "mcpServers": {
    "dhis2": {
      "command": "dhis2w-mcp"
    }
  }
}
```

Restart Claude Desktop / reload the MCP server panel; the agent should now see `system_info`, `system_whoami`, `metadata_*`, `data_*`, etc.

### Profile selection

The server picks its DHIS2 profile from the standard `dhis2w-core` resolution chain: walking up for `.dhis2/profiles.toml`, falling back to `~/.config/dhis2/profiles.toml`. Every MCP tool also accepts an explicit `profile: str | None` kwarg so an agent can target any configured profile per call without restarting the server.

### Active plugin tree

`dhis2w-mcp` selects a plugin tree (v41 / v42 / v43) at startup. Override per-launch with the `DHIS2_VERSION` env var:

```bash
DHIS2_VERSION=43 dhis2w-mcp
```

Call `system_server_info` from the agent to see which tree is bound + which `dhis2w-*` package versions are installed.

## Where next

- [Tutorial](tutorial.md) — your first MCP tool call from an agent.
- [Reference](../mcp-reference.md) — auto-generated catalog of every tool + parameter schema.
- [Architecture](../architecture/mcp.md) — how the FastMCP server mounts plugins, return-shape conventions.
- [Examples index](../examples.md) — Python scripts driving the in-process MCP server end-to-end.
