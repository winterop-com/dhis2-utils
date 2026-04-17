"""Typer sub-app for `dhis2-codegen` — also mounted under `dhis2 codegen`."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Annotated

import typer
from dhis2_client import AuthProvider, BasicAuth, PatAuth
from rich.console import Console

from dhis2_codegen.discover import discover
from dhis2_codegen.emit import emit

app = typer.Typer(help="Generate version-aware DHIS2 client code from /api/schemas.", no_args_is_help=True)
_console = Console()


@app.command("generate")
def generate(
    url: Annotated[str, typer.Option("--url", help="Base URL of the DHIS2 instance.")],
    username: Annotated[str | None, typer.Option("--username", help="Basic-auth username.")] = None,
    password: Annotated[str | None, typer.Option("--password", help="Basic-auth password.")] = None,
    pat: Annotated[str | None, typer.Option("--pat", help="Personal Access Token.")] = None,
    output_root: Annotated[
        Path | None,
        typer.Option(
            "--output-root",
            help="Directory containing versioned subfolders; defaults to dhis2-client's generated/ folder.",
        ),
    ] = None,
) -> None:
    """Generate the client for the DHIS2 version reported by `--url`."""
    auth: AuthProvider
    if pat:
        auth = PatAuth(token=pat)
    elif username and password:
        auth = BasicAuth(username=username, password=password)
    else:
        raise typer.BadParameter("provide either --pat or --username + --password")

    target_root = output_root or _default_output_root()
    asyncio.run(_run(url=url, auth=auth, output_root=target_root))


async def _run(*, url: str, auth: AuthProvider, output_root: Path) -> None:
    _console.print(f"[bold]discovering[/bold] {url}")
    manifest = await discover(url, auth)
    destination = output_root / manifest.version_key
    _console.print(f"  version: {manifest.raw_version} (→ {manifest.version_key})")
    _console.print(f"  schemas: {len(manifest.schemas)}")
    _console.print(f"[bold]emitting[/bold] {destination}")
    emit(manifest, destination)
    _console.print(f"[green]done[/green] — generated {len(manifest.schemas)} schemas into {destination}")


def _default_output_root() -> Path:
    """Locate `packages/dhis2-client/src/dhis2_client/generated/` relative to this file."""
    here = Path(__file__).resolve()
    repo_root = here
    for _ in range(6):
        repo_root = repo_root.parent
        candidate = repo_root / "packages" / "dhis2-client" / "src" / "dhis2_client" / "generated"
        if candidate.exists():
            return candidate
    raise RuntimeError("could not locate dhis2-client generated/ directory; pass --output-root explicitly")


if __name__ == "__main__":
    app()
