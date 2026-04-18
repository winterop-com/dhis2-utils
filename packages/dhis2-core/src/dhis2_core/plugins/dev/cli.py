"""Typer sub-app for `dhis2 dev` — codegen, uid, oauth2 + PAT provisioning."""

from __future__ import annotations

import asyncio
import os
from typing import Annotated, Any

import typer
from dhis2_codegen.cli import app as codegen_app

from dhis2_core.oauth2_registration import build_admin_auth, register_oauth2_client
from dhis2_core.pat_registration import register_pat
from dhis2_core.plugins.system import service as system_service
from dhis2_core.profile import profile_from_env

app = typer.Typer(help="Developer/operator tools.", no_args_is_help=True)
app.add_typer(codegen_app, name="codegen", help="Generate version-aware DHIS2 client code from /api/schemas.")

oauth2_app = typer.Typer(help="Manage DHIS2 OAuth2 clients on the server (admin ops).", no_args_is_help=True)
oauth2_client_app = typer.Typer(help="OAuth2 client registrations at /api/oAuth2Clients.", no_args_is_help=True)
oauth2_app.add_typer(oauth2_client_app, name="client")
app.add_typer(oauth2_app, name="oauth2")

pat_app = typer.Typer(help="Personal Access Tokens — provision PATs on DHIS2.", no_args_is_help=True)
app.add_typer(pat_app, name="pat")


def _resolve_admin_auth(admin_user: str | None) -> Any:
    """Build an admin auth provider from env + prompt — NEVER from argv secrets."""
    admin_pat = os.environ.get("DHIS2_ADMIN_PAT")
    admin_pass = os.environ.get("DHIS2_ADMIN_PASSWORD")
    if not admin_pat and not admin_pass:
        if admin_user or typer.confirm("Bootstrap with username+password? (no = PAT)", default=True):
            if not admin_user:
                admin_user = typer.prompt("Admin username", default="admin")
            admin_pass = typer.prompt("Admin password", hide_input=True)
        else:
            admin_pat = typer.prompt("Admin PAT", hide_input=True)
    return build_admin_auth(pat=admin_pat, username=admin_user, password=admin_pass)


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
    url: Annotated[str | None, typer.Option("--url", help="DHIS2 base URL (also: DHIS2_URL env).")] = None,
    admin_user: Annotated[str | None, typer.Option("--admin-user")] = None,
    client_id: Annotated[str, typer.Option("--client-id")] = "dhis2-utils-local",
    redirect_uri: Annotated[str, typer.Option("--redirect-uri")] = "http://localhost:8765",
    scope: Annotated[str, typer.Option("--scope")] = "ALL",
    display_name: Annotated[str | None, typer.Option("--name")] = None,
) -> None:
    """Register an OAuth2 client on DHIS2 via POST /api/oAuth2Clients.

    Secrets (admin credentials, client_secret) come from env or interactive
    prompt — never argv.

    Prints `client_id` + metadata UID so they can be piped into
    `dhis2 profile add --auth oauth2 ...`. For a one-shot bootstrap (register
    + save profile + log in) use `dhis2 profile bootstrap` instead.
    """
    resolved_url: str = url or os.environ.get("DHIS2_URL") or typer.prompt("DHIS2 base URL")
    admin_auth = _resolve_admin_auth(admin_user)
    client_secret = os.environ.get("DHIS2_OAUTH_CLIENT_SECRET") or typer.prompt(
        f"New client_secret for {client_id!r}", hide_input=True
    )
    creds = asyncio.run(
        register_oauth2_client(
            base_url=resolved_url,
            admin_auth=admin_auth,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            display_name=display_name,
        )
    )
    typer.echo(f"registered oauth2 client at {resolved_url}")
    typer.echo(f"  uid={creds.uid}")
    typer.echo(f"  client_id={creds.client_id}")
    typer.echo(f"  redirect_uri={creds.redirect_uri}")
    typer.echo(f"  scope={creds.scope}")
    typer.secho(
        "  client_secret not echoed — export as DHIS2_OAUTH_CLIENT_SECRET or use profile add", fg=typer.colors.YELLOW
    )


@pat_app.command("create")
def pat_create_command(
    url: Annotated[str | None, typer.Option("--url", help="DHIS2 base URL (also: DHIS2_URL env).")] = None,
    admin_user: Annotated[str | None, typer.Option("--admin-user")] = None,
    description: Annotated[str | None, typer.Option("--description")] = None,
    expires_in_days: Annotated[int | None, typer.Option("--expires-in-days")] = None,
    allowed_ip: Annotated[
        list[str] | None,
        typer.Option("--allowed-ip", help="IP allowlist entry; repeat for multiple."),
    ] = None,
    allowed_method: Annotated[
        list[str] | None,
        typer.Option("--allowed-method", help="HTTP method allowlist; repeat for each method."),
    ] = None,
    allowed_referrer: Annotated[
        list[str] | None,
        typer.Option("--allowed-referrer", help="Referer allowlist entry; repeat for multiple."),
    ] = None,
    quiet: Annotated[
        bool,
        typer.Option("--quiet", "-q", help="Print only the PAT value, suitable for $(command substitution)."),
    ] = False,
) -> None:
    """Create a DHIS2 Personal Access Token via POST /api/apiToken.

    Admin creds come from env or prompt (never argv). The PAT value is only
    returned once by DHIS2 — capture it here and pipe into a profile:

        export DHIS2_PAT=$(dhis2 dev pat create --url $URL -q)
        dhis2 profile add local --url $URL --auth pat

    Or use `dhis2 profile bootstrap --auth pat` for a one-shot setup.
    """
    resolved_url: str = url or os.environ.get("DHIS2_URL") or typer.prompt("DHIS2 base URL")
    admin_auth = _resolve_admin_auth(admin_user)
    creds = asyncio.run(
        register_pat(
            base_url=resolved_url,
            admin_auth=admin_auth,
            description=description,
            expires_in_days=expires_in_days,
            allowed_ips=allowed_ip,
            allowed_methods=allowed_method,
            allowed_referrers=allowed_referrer,
        )
    )
    if quiet:
        typer.echo(creds.token)
    else:
        typer.echo(f"registered PAT at {resolved_url}")
        typer.echo(f"  uid={creds.uid}")
        if creds.description:
            typer.echo(f"  description={creds.description}")
        typer.echo(f"  token={creds.token}")
        typer.secho(
            "  this value is shown ONCE by DHIS2 — save it now (export DHIS2_PAT=... or profile add)",
            fg=typer.colors.YELLOW,
        )


def register(root_app: Any) -> None:
    """Mount under `dhis2 dev`."""
    root_app.add_typer(app, name="dev", help="Developer/operator tools.")
