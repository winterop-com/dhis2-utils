"""Typer root for the `dhis2` CLI — discovers plugins and mounts them."""

from __future__ import annotations

import os
from typing import Annotated

import typer
from dhis2_core.cli_errors import run_app
from dhis2_core.plugin import discover_plugins


def build_app() -> typer.Typer:
    """Build a fresh Typer app with every discovered plugin mounted.

    Every call returns a new app, which keeps unit tests hermetic and lets
    callers introspect the mounted surface without side effects.

    `pretty_exceptions_enable=False` so our `run_app` wrapper (invoked from
    `main()` below) sees uncaught exceptions and can render them cleanly.
    """
    app = typer.Typer(
        help="dhis2 — command-line interface for DHIS2 (discovers plugins from dhis2-core).",
        no_args_is_help=True,
        add_completion=False,
        pretty_exceptions_enable=False,
    )

    @app.callback()
    def _root(
        profile: Annotated[
            str | None,
            typer.Option(
                "--profile",
                "-p",
                help="DHIS2 profile name (overrides DHIS2_PROFILE env + TOML default).",
            ),
        ] = None,
    ) -> None:
        """Set the active DHIS2 profile for this invocation."""
        if profile:
            os.environ["DHIS2_PROFILE"] = profile

    for plugin in discover_plugins():
        plugin.register_cli(app)
    return app


app = build_app()


def main() -> None:
    """Console-script entrypoint — wraps the Typer app with clean error rendering."""
    run_app(app)


if __name__ == "__main__":
    main()
