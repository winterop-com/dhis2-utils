"""Typer CLI for dhis2-browser — utilities that drive DHIS2 via a real browser."""

from __future__ import annotations

import asyncio
from typing import Annotated

import typer

from dhis2_browser.pat import PatOptions, create_pat

app = typer.Typer(help="Playwright-based DHIS2 utilities.", no_args_is_help=True)


@app.command("pat")
def pat_command(
    url: Annotated[str, typer.Option("--url", help="Base URL of the DHIS2 instance.")],
    username: Annotated[str, typer.Option("--username", help="Login username.")],
    password: Annotated[str, typer.Option("--password", help="Login password.")],
    name: Annotated[str | None, typer.Option("--name", help="Friendly display name for the token.")] = None,
    expires_in_days: Annotated[
        int | None,
        typer.Option("--expires-in-days", help="Token lifetime in days; omit for no expiry."),
    ] = None,
    allowed_ip: Annotated[
        list[str] | None,
        typer.Option("--allowed-ip", help="CIDR/IP allowlist entry; repeat for multiple."),
    ] = None,
    allowed_method: Annotated[
        list[str] | None,
        typer.Option("--allowed-method", help="HTTP method allowlist; repeat for each method."),
    ] = None,
    allowed_referrer: Annotated[
        list[str] | None,
        typer.Option("--allowed-referrer", help="Referer URL allowlist; repeat for each."),
    ] = None,
    headless: Annotated[
        bool,
        typer.Option(
            "--headless/--headful",
            help="Run browser headlessly (default: visible, so you can watch the flow).",
        ),
    ] = False,
) -> None:
    """Create a new PAT via Playwright and print the token value to stdout."""
    options = PatOptions(
        name=name,
        expires_in_days=expires_in_days,
        allowed_ips=allowed_ip,
        allowed_methods=allowed_method,
        allowed_referrers=allowed_referrer,
    )
    token = asyncio.run(create_pat(url, username, password, options=options, headless=headless))
    typer.echo(token)


@app.command("info")
def info_command() -> None:
    """Print the package name (placeholder so Typer uses subcommand dispatch)."""
    typer.echo("dhis2-browser — Playwright helpers for DHIS2")


if __name__ == "__main__":
    app()
