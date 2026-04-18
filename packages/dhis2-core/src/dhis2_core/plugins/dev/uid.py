"""`dhis2 dev uid` — generate fresh DHIS2 UIDs via /api/system/id."""

from __future__ import annotations

import asyncio
from typing import Annotated

import typer

from dhis2_core.plugins.system import service as system_service
from dhis2_core.profile import profile_from_env

app = typer.Typer(help="Generate 11-char DHIS2 UIDs.", invoke_without_command=True)


@app.callback(invoke_without_command=True)
def uid_command(
    count: Annotated[
        int,
        typer.Option("--count", "-n", min=1, max=10000, help="How many UIDs to generate."),
    ] = 1,
) -> None:
    """Generate fresh 11-char DHIS2 UIDs via `/api/system/id` — one per line."""
    codes = asyncio.run(system_service.generate_uids(profile_from_env(), limit=count))
    for code in codes:
        typer.echo(code)
