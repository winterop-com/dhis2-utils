"""Typer sub-app for `dhis2 dev` — codegen, uid, oauth2 client registration."""

from __future__ import annotations

import asyncio
from typing import Annotated, Any

import typer
from dhis2_codegen.cli import app as codegen_app

from dhis2_core.oauth2_registration import build_admin_auth, register_oauth2_client
from dhis2_core.plugins.system import service as system_service
from dhis2_core.profile import profile_from_env

app = typer.Typer(help="Developer/operator tools.", no_args_is_help=True)
app.add_typer(codegen_app, name="codegen", help="Generate version-aware DHIS2 client code from /api/schemas.")

oauth2_app = typer.Typer(help="Manage DHIS2 OAuth2 clients on the server (admin ops).", no_args_is_help=True)
oauth2_client_app = typer.Typer(help="OAuth2 client registrations at /api/oAuth2Clients.", no_args_is_help=True)
oauth2_app.add_typer(oauth2_client_app, name="client")
app.add_typer(oauth2_app, name="oauth2")


@app.command("uid")
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


@oauth2_client_app.command("register")
def oauth2_client_register_command(
    url: Annotated[str, typer.Option("--url", help="DHIS2 base URL.")],
    admin_user: Annotated[str | None, typer.Option("--admin-user")] = None,
    admin_pass: Annotated[str | None, typer.Option("--admin-pass")] = None,
    admin_pat: Annotated[str | None, typer.Option("--admin-pat")] = None,
    client_id: Annotated[str, typer.Option("--client-id")] = "dhis2-utils-local",
    client_secret: Annotated[str, typer.Option("--client-secret")] = "dhis2-utils-local-secret",
    redirect_uri: Annotated[str, typer.Option("--redirect-uri")] = "http://localhost:8765",
    scope: Annotated[str, typer.Option("--scope")] = "ALL",
    display_name: Annotated[str | None, typer.Option("--name")] = None,
) -> None:
    """Register an OAuth2 client on DHIS2 via POST /api/oAuth2Clients.

    Prints the resulting `client_id`, `client_secret`, and metadata UID so
    they can be piped into `dhis2 profile add --auth oauth2 ...`. For a
    one-shot bootstrap (register + save profile + log in), use
    `dhis2 profile bootstrap` instead.
    """
    admin_auth = build_admin_auth(pat=admin_pat, username=admin_user, password=admin_pass)
    creds = asyncio.run(
        register_oauth2_client(
            base_url=url,
            admin_auth=admin_auth,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            display_name=display_name,
        )
    )
    typer.echo(f"registered oauth2 client at {url}")
    typer.echo(f"  uid={creds.uid}")
    typer.echo(f"  client_id={creds.client_id}")
    typer.echo(f"  client_secret={creds.client_secret}")
    typer.echo(f"  redirect_uri={creds.redirect_uri}")
    typer.echo(f"  scope={creds.scope}")


def register(root_app: Any) -> None:
    """Mount under `dhis2 dev`."""
    root_app.add_typer(app, name="dev", help="Developer/operator tools.")
