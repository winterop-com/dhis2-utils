"""Browser plugin — Playwright-driven DHIS2 UI automation.

Mounts `dhis2 browser ...` subcommands. Library code (session + PAT minting)
lives in the separate `dhis2-browser` workspace member so API-only consumers
of `dhis2-client` never pull in Chromium. This plugin is the thin CLI +
service shell that wraps it.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from dhis2_core.plugins.browser import cli as cli_module


class _BrowserPlugin(BaseModel):
    """Plugin descriptor for Playwright-driven DHIS2 UI automation."""

    model_config = ConfigDict(frozen=True)

    name: str = "browser"
    description: str = (
        "Playwright-driven DHIS2 UI automation. Mounts `dhis2 browser ...` "
        "for workflows DHIS2 only exposes through the web UI (PAT minting "
        "today; dashboard screenshots + maintenance-app driving planned)."
    )

    def register_cli(self, app: Any) -> None:
        """Mount `dhis2 browser` on the root CLI."""
        cli_module.register(app)

    def register_mcp(self, mcp: Any) -> None:
        """No MCP tools yet — Playwright flows are CLI-only for now."""


plugin = _BrowserPlugin()
