"""Plugin Protocol + discovery for dhis2-core.

Plugins are self-contained capability folders under `dhis2_core.plugins.*`.
Each plugin module exports a module-level `plugin` attribute conforming to
the `Plugin` Protocol. External packages may register additional plugins via
`importlib.metadata.entry_points(group="dhis2.plugins")`.
"""

from __future__ import annotations

import importlib
import pkgutil
from importlib.metadata import entry_points
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Plugin(Protocol):
    """Dual-surface plugin descriptor registered with the CLI and/or MCP."""

    name: str
    description: str

    def register_cli(self, app: Any) -> None:
        """Mount this plugin's Typer sub-app on the root CLI."""
        ...

    def register_mcp(self, mcp: Any) -> None:
        """Register this plugin's tools on the FastMCP server."""
        ...


def discover_plugins() -> list[Plugin]:
    """Discover built-in and entry-point plugins; returns `Plugin` instances."""
    plugins: list[Plugin] = []
    plugins.extend(_discover_builtins())
    plugins.extend(_discover_external())
    return plugins


def _discover_builtins() -> list[Plugin]:
    try:
        package = importlib.import_module("dhis2_core.plugins")
    except ImportError:
        return []
    found: list[Plugin] = []
    for _, name, _is_pkg in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"dhis2_core.plugins.{name}")
        plugin = getattr(module, "plugin", None)
        if plugin is not None and isinstance(plugin, Plugin):
            found.append(plugin)
    return found


def _discover_external() -> list[Plugin]:
    found: list[Plugin] = []
    for entry in entry_points(group="dhis2.plugins"):
        try:
            plugin = entry.load()
        except ImportError:
            continue
        if isinstance(plugin, Plugin):
            found.append(plugin)
    return found
