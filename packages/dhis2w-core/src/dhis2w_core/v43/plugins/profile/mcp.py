"""FastMCP tool registration for the `profile` plugin (read-only tools)."""

from __future__ import annotations

from typing import Any

from dhis2w_core.v43.plugins.profile import service


def register(mcp: Any) -> None:
    """Register read-only profile tools on the MCP server.

    Mutations (add/remove/default) are deliberately CLI-only — config changes
    via an autonomous agent are too risky.
    """

    @mcp.tool()
    async def profile_list() -> list[service.ProfileSummary]:
        """List every DHIS2 profile the server can see.

        Returns one entry per profile with name, base_url, auth kind,
        source (`project-toml` | `global-toml`), source_path, and whether
        it's the effective default. Project profiles shadow global ones
        with the same name.
        """
        return service.list_profiles()

    @mcp.tool()
    async def profile_verify(name: str) -> service.VerifyResult:
        """Verify one profile by calling /api/system/info and /api/me.

        Returns `{name, ok, base_url, auth, version, username, latency_ms, error}`.
        Useful to pick between profiles interactively — the agent can list
        then verify the likely one before calling other tools with it.
        """
        return await service.verify_profile(name)

    @mcp.tool()
    async def profile_verify_all() -> list[service.VerifyResult]:
        """Verify every known profile. Returns one result per profile."""
        return await service.verify_all_profiles()

    @mcp.tool()
    async def profile_show(name: str) -> service.ProfileView:
        """Show a profile with secrets redacted (token/password/client_secret → '***')."""
        return service.show_profile(name, include_secrets=False)
