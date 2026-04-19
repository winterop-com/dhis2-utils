"""Customize plugin — brand + theme a DHIS2 instance.

CLI is mounted under `dhis2 dev customize` (see `plugins/dev/cli.py`),
alongside the other rarely-run setup utilities (`dev pat`, `dev oauth2`,
`dev sample`, `dev codegen`). MCP tools are registered at the top level
(`customize_*`) since MCP has no nested-namespace convention.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from dhis2_core.plugins.customize import mcp as mcp_module


class _CustomizePlugin(BaseModel):
    """Plugin descriptor for DHIS2 branding + theming."""

    model_config = ConfigDict(frozen=True)

    name: str = "customize"
    description: str = (
        "DHIS2 branding + theming: login-page logos, system-setting copy, CSS stylesheet. "
        "Applies preset directories so `dhis2 dev customize apply DIR` re-brands an instance."
    )

    def register_cli(self, app: Any) -> None:
        """CLI is mounted by the `dev` plugin under `dhis2 dev customize`; no top-level mount."""
        return None

    def register_mcp(self, mcp: Any) -> None:
        """Register `customize_*` tools on the MCP server."""
        mcp_module.register(mcp)


plugin = _CustomizePlugin()
