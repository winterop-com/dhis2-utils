"""Typer root for the `dhis2` CLI — discovers plugins and mounts them."""

from __future__ import annotations

import typer

from dhis2_core.plugin import discover_plugins


def build_app() -> typer.Typer:
    """Build a fresh Typer app with every discovered plugin mounted.

    Every call returns a new app, which keeps unit tests hermetic and lets
    callers introspect the mounted surface without side effects.
    """
    app = typer.Typer(
        help="dhis2 — command-line interface for DHIS2 (discovers plugins from dhis2-core).",
        no_args_is_help=True,
        add_completion=False,
    )
    for plugin in discover_plugins():
        plugin.register_cli(app)
    return app


app = build_app()


if __name__ == "__main__":
    app()
