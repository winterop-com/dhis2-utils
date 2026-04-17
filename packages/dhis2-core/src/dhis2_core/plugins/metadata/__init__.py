"""Metadata plugin — CLI + MCP wrappers over the generated CRUD resources."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dhis2_core.plugins.metadata import cli as cli_module
from dhis2_core.plugins.metadata import mcp as mcp_module


@dataclass(frozen=True)
class _MetadataPlugin:
    """Plugin descriptor for DHIS2 metadata inspection."""

    name: str = "metadata"
    description: str = "Inspect DHIS2 metadata (lists + get by UID, across every generated resource)."

    def register_cli(self, app: Any) -> None:
        """Mount the metadata sub-app under `dhis2 metadata`."""
        cli_module.register(app)

    def register_mcp(self, mcp: Any) -> None:
        """Register metadata listing tools on the MCP server."""
        mcp_module.register(mcp)


plugin = _MetadataPlugin()
