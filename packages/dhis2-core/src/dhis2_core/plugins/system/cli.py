"""Typer sub-app for the `system` plugin (mounted under `dhis2 system`)."""

from __future__ import annotations

import asyncio
from typing import Annotated, Any

import typer

from dhis2_core.plugins.system import service
from dhis2_core.profile import profile_from_env

app = typer.Typer(help="DHIS2 system info and current-user access.", no_args_is_help=True)


@app.command("whoami")
def whoami_command() -> None:
    """Print the authenticated DHIS2 user for the current environment profile."""
    me = asyncio.run(service.whoami(profile_from_env()))
    typer.echo(f"{me.username} ({me.displayName or '-'})")


@app.command("info")
def info_command() -> None:
    """Print basic DHIS2 system info for the current environment profile."""
    info = asyncio.run(service.system_info(profile_from_env()))
    typer.echo(f"version={info.version} revision={info.revision or '-'} name={info.systemName or '-'}")


@app.command("uid")
def uid_command(
    count: Annotated[
        int,
        typer.Option("--count", "-n", min=1, max=10000, help="How many UIDs to mint."),
    ] = 1,
) -> None:
    """Mint fresh 11-char DHIS2 UIDs via `/api/system/id` — one per line."""
    codes = asyncio.run(service.generate_uids(profile_from_env(), limit=count))
    for code in codes:
        typer.echo(code)


def register(root_app: Any) -> None:
    """Mount this plugin's Typer sub-app under `dhis2 system`."""
    root_app.add_typer(app, name="system", help="DHIS2 system info.")
