"""Plugin descriptor so `dhis2 codegen` appears when dhis2-cli discovers plugins."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from dhis2_codegen.cli import app as codegen_app


class _CodegenPlugin(BaseModel):
    """Minimal Plugin implementation for the entry-point group `dhis2.plugins`."""

    model_config = ConfigDict(frozen=True)

    name: str = "codegen"
    description: str = "Generate version-aware DHIS2 client code from /api/schemas."

    def register_cli(self, app: Any) -> None:
        """Mount the codegen Typer sub-app under `dhis2 codegen`."""
        app.add_typer(codegen_app, name=self.name, help=self.description)

    def register_mcp(self, mcp: Any) -> None:
        """No MCP surface yet — codegen is CLI-only."""
        return None


plugin = _CodegenPlugin()
