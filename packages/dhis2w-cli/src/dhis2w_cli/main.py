"""Typer root for the `dhis2` CLI — discovers plugins and mounts them."""

from __future__ import annotations

import logging
import os
from importlib.metadata import PackageNotFoundError, version
from typing import Annotated

import typer
from dhis2w_core.cli_errors import run_app
from dhis2w_core.cli_output import JSON_OUTPUT
from dhis2w_core.plugin import DEFAULT_VERSION_KEY, discover_plugins, resolve_startup_version
from dhis2w_core.rich_console import STDERR_CONSOLE
from rich.logging import RichHandler


def _version_banner() -> str:
    """Multi-line banner shown for `dhis2 --version` — package version + active plugin tree.

    Surfaces which plugin tree (`v41` / `v42` / `v43`) the CLI booted with
    and where that came from in the resolution chain (`profile.version` →
    `DHIS2_VERSION` env → default). Helps debug "which DHIS2 major is
    this CLI talking to" without reading the profile by hand.
    """
    try:
        pkg_version = version("dhis2w-cli")
    except PackageNotFoundError:
        pkg_version = "unknown"
    active = resolve_startup_version()
    env_version = os.environ.get("DHIS2_VERSION", "").strip()
    if (
        env_version in {"41", "42", "43"}
        and f"v{env_version}" == active
        or env_version in {"v41", "v42", "v43"}
        and env_version == active
    ):
        source = f"DHIS2_VERSION={env_version!r} env"
    elif active == DEFAULT_VERSION_KEY:
        source = "default (no profile.version, no DHIS2_VERSION env)"
    else:
        source = "profile.version"
    return f"dhis2 {pkg_version}  (plugin tree: {active} — {source})"


def _version_callback(value: bool) -> None:
    """Eager `--version` callback — print the banner and exit."""
    if value:
        typer.echo(_version_banner())
        raise typer.Exit(0)


def _enable_debug_logging() -> None:
    """Turn on dhis2w-client HTTP traces + dhis2w-core debug logs on stderr.

    Uses `rich.logging.RichHandler` tied to the shared `STDERR_CONSOLE` so log
    lines render above any active Rich `Progress` / `Status` display instead
    of tearing through it.
    """
    handler = RichHandler(
        console=STDERR_CONSOLE,
        show_path=False,
        show_time=True,
        markup=False,
        rich_tracebacks=False,
        log_time_format="%H:%M:%S",
    )
    handler.setLevel(logging.DEBUG)
    root = logging.getLogger()
    root.addHandler(handler)
    for name in ("dhis2w_client", "dhis2w_core"):
        logging.getLogger(name).setLevel(logging.DEBUG)


def build_app() -> typer.Typer:
    """Build a fresh Typer app with every discovered plugin mounted.

    Every call returns a new app, which keeps unit tests hermetic and lets
    callers introspect the mounted surface without side effects.

    `pretty_exceptions_enable=False` so our `run_app` wrapper (invoked from
    `main()` below) sees uncaught exceptions and can render them cleanly.
    """
    app = typer.Typer(
        help="dhis2 — command-line interface for DHIS2 (discovers plugins from dhis2w-core).",
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
        debug: Annotated[
            bool,
            typer.Option(
                "--debug",
                "-d",
                help="Verbose output on stderr — HTTP method/URL/status/elapsed for every request.",
            ),
        ] = False,
        json_: Annotated[
            bool,
            typer.Option(
                "--json",
                "-j",
                help="Emit raw JSON to stdout instead of Rich tables (uniform across all commands).",
            ),
        ] = False,
        _version: Annotated[
            bool,
            typer.Option(
                "--version",
                "-V",
                help="Print the CLI version + active plugin tree and exit.",
                callback=_version_callback,
                is_eager=True,
            ),
        ] = False,
    ) -> None:
        """Set the active DHIS2 profile + optional debug logging + output mode for this invocation."""
        if profile:
            os.environ["DHIS2_PROFILE"] = profile
        if debug:
            _enable_debug_logging()
        # Always set, not just when True — `CliRunner` reuses the same
        # process across `invoke` calls, so a stale `True` from a previous
        # invocation must not leak into the next one.
        JSON_OUTPUT.set(json_)

    for plugin in discover_plugins(resolve_startup_version()):
        plugin.register_cli(app)
    return app


app = build_app()


def main() -> None:
    """Console-script entrypoint — wraps the Typer app with clean error rendering."""
    run_app(app)


if __name__ == "__main__":
    main()
