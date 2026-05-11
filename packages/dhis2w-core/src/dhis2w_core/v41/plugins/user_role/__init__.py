"""User-role plugin — list, get, authorities, grant/revoke users."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from dhis2w_core.v41.plugins.user_role import cli as cli_module
from dhis2w_core.v41.plugins.user_role import mcp as mcp_module


class _UserRolePlugin(BaseModel):
    """Plugin descriptor for the DHIS2 user-role administration surface."""

    model_config = ConfigDict(frozen=True)

    name: str = "user-role"
    description: str = "List + administer DHIS2 user roles (authorities, user membership)."

    def register_cli(self, app: Any) -> None:
        """Mount the user-role sub-app under `dhis2 user-role`."""
        cli_module.register(app)

    def register_mcp(self, mcp: Any) -> None:
        """Register user-role tools on the MCP server."""
        mcp_module.register(mcp)


plugin = _UserRolePlugin()
