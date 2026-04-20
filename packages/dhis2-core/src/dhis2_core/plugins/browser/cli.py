"""Typer sub-app for the `browser` plugin — mounts `dhis2 browser ...`."""

from __future__ import annotations

import asyncio
from typing import Annotated, Any

import typer

from dhis2_core.plugins.browser import service


def register(app: Any) -> None:
    """Mount `dhis2 browser` on the root CLI."""
    browser_app = typer.Typer(
        help="Playwright-driven DHIS2 UI automation (needs the browser extra).",
        no_args_is_help=True,
    )
    browser_app.command("pat")(pat_command)
    app.add_typer(browser_app, name="browser")


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
    """Mint a Personal Access Token V2 via Playwright and print the token value to stdout.

    DHIS2 only returns the token value once, at creation — store it somewhere
    persistent immediately. Subsequent `GET /api/apiToken/{id}` calls return
    metadata but not the secret.
    """
    service.require_browser()
    from dhis2_browser import PatOptions  # noqa: PLC0415 — optional-extra guard

    options = PatOptions(
        name=name,
        expires_in_days=expires_in_days,
        allowed_ips=allowed_ip,
        allowed_methods=allowed_method,
        allowed_referrers=allowed_referrer,
    )
    token = asyncio.run(service.create_pat(url, username, password, options=options, headless=headless))
    typer.echo(token)
