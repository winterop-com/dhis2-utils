# MCP tutorial

A walk through driving `dhis2w-mcp` from an LLM agent — first call, profile selection, error reading. Assumes you've already installed the server per the [introduction](index.md) and wired it into your MCP host.

## 1. Confirm the server is alive

In Claude Desktop / Claude Code, ask the agent:

> List the MCP tools you have for DHIS2.

The agent should respond with a count and a sample (analytics, apps, customize, data, doctor, files, maintenance, messaging, metadata, profile, route, system, user — 337+ tools across 13 plugin groups). If it says it has zero MCP tools, the host hasn't loaded the server — restart and check the MCP panel.

## 2. Your first call

> Call `system_server_info` and tell me which plugin tree is active.

The agent invokes the tool with no arguments. The typed response carries:

```json
{
  "active_plugin_tree": "v43",
  "active_plugin_tree_source": "DHIS2_VERSION='43' env",
  "dhis2w_core_version": "0.10.0",
  "dhis2w_mcp_version": "0.10.0",
  "dhis2w_cli_version": null
}
```

This is a process-local introspection — no DHIS2 client is opened. Useful as a smoke test before issuing version-sensitive calls.

## 3. A real DHIS2 call

> Call `system_whoami` to check the active DHIS2 user.

If the agent's default profile is correctly configured, the response is a typed `Me` object — username, displayName, authorities, OU scopes, group memberships.

If the response is an authentication error, the agent will read the typed `Dhis2ApiError` envelope (status code, message, optional WebMessage conflict list) and explain what's missing. The error shape is the same across every tool, so the agent learns it once.

## 4. Profile selection per call

> Use `metadata_program_list` with `profile="staging"` to count tracker programs on staging.

Every MCP tool accepts an optional `profile: str | None` kwarg — pass a profile name from `profiles.toml` to override the default for that one call. Lets one running MCP server target multiple DHIS2 stacks (e.g. local + staging + a play instance) without restarting.

## 5. Version-sensitive tools

The v43-only tools (`metadata_program_set_labels`, `metadata_program_set_change_log_enabled`, `metadata_program_set_enrollment_category_combo`) only register when the active plugin tree is v43. On a v42-bound server they're absent from the tool list. Call `system_server_info` first if you're unsure which tools the agent sees.

## Where next

- [Reference](../mcp-reference.md) — every tool with its parameter schema + description.
- [Architecture](../architecture/mcp.md) — return-shape conventions, error handling, profile resolution.
- [Examples](../examples.md) — Python scripts that drive the in-process MCP server end-to-end (useful for snapshot-testing agent flows).
