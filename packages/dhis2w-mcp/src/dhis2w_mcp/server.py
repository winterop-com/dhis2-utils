"""FastMCP server entry for dhis2w-mcp — mounts plugins from dhis2w-core."""

from __future__ import annotations

from dhis2w_core.plugin import discover_plugins
from fastmcp import FastMCP


def build_server() -> FastMCP:
    """Create the FastMCP instance with every discovered plugin registered."""
    server = FastMCP(name="dhis2")
    for plugin in discover_plugins():
        plugin.register_mcp(server)
    return server


def main() -> None:
    """Console-script entrypoint: build the server and run it over stdio."""
    build_server().run()


if __name__ == "__main__":
    main()
