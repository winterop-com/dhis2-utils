"""Typer sub-app for the `user` plugin (mounted under `dhis2 user`)."""

from __future__ import annotations

import asyncio
import json
from typing import Annotated, Any

import typer
from rich.console import Console
from rich.table import Table

from dhis2_core.plugins.user import service
from dhis2_core.plugins.user.service import UserInvite, UserNotFoundError
from dhis2_core.profile import profile_from_env

app = typer.Typer(help="Inspect + administer DHIS2 users (list, get, invite, reset-password).", no_args_is_help=True)
_console = Console()

_DEFAULT_FIELDS = "id,username,displayName,email,disabled,lastLogin"


@app.command("list")
@app.command("ls", hidden=True)
def list_command(
    fields: Annotated[
        str,
        typer.Option(
            "--fields",
            help=(
                "DHIS2 field selector. Supports plain lists ('id,username,email'), presets "
                "(':identifiable', ':nameable', ':owner', ':all'), and exclusions (':all,!password')."
            ),
        ),
    ] = _DEFAULT_FIELDS,
    filters: Annotated[
        list[str] | None,
        typer.Option("--filter", help="Filter 'property:operator:value' (repeatable)."),
    ] = None,
    root_junction: Annotated[
        str,
        typer.Option("--root-junction", help="Combine repeated --filter as AND (default) or OR."),
    ] = "AND",
    order: Annotated[
        list[str] | None,
        typer.Option("--order", help="Sort clause 'property:asc|desc' (repeatable)."),
    ] = None,
    page: Annotated[int | None, typer.Option("--page", help="Server-side page number (1-based).")] = None,
    page_size: Annotated[int | None, typer.Option("--page-size", help="Server-side page size (default 50).")] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON instead of a table.")] = False,
) -> None:
    """List users.

    Examples:
      dhis2 user list
      dhis2 user list --filter 'disabled:eq:true' --order 'username:asc'
      dhis2 user list --filter 'userCredentials.username:like:admin'
    """
    rj = root_junction if filters and len(filters) > 1 else None
    users = asyncio.run(
        service.list_users(
            profile_from_env(),
            fields=fields,
            filters=filters,
            root_junction=rj,
            order=order,
            page=page,
            page_size=page_size,
        )
    )
    dumped = [u.model_dump(by_alias=True, exclude_none=True, mode="json") for u in users]
    if as_json:
        typer.echo(json.dumps(dumped, indent=2))
        return
    _print_table(dumped, fields.split(","))


@app.command("get")
def get_command(
    uid_or_username: Annotated[str, typer.Argument(help="User UID (11 chars) or username.")],
    fields: Annotated[str | None, typer.Option("--fields", help="DHIS2 field selector.")] = None,
) -> None:
    """Fetch one user by UID or username; print as JSON."""
    try:
        user = asyncio.run(service.get_user(profile_from_env(), uid_or_username, fields=fields))
    except UserNotFoundError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from None
    typer.echo(user.model_dump_json(indent=2, exclude_none=True, by_alias=True))


@app.command("me")
def me_command() -> None:
    """Print the authenticated user's `/api/me` payload (authorities + profile)."""
    payload = asyncio.run(service.current_user(profile_from_env()))
    typer.echo(json.dumps(payload, indent=2))


@app.command("invite")
def invite_command(
    email: Annotated[str, typer.Argument(help="Email address for the new user (receives the invitation link).")],
    first_name: Annotated[str, typer.Option("--first-name", help="User's given name.")],
    surname: Annotated[str, typer.Option("--surname", help="User's surname.")],
    username: Annotated[
        str | None,
        typer.Option(
            "--username",
            help="Desired username. Omit to let DHIS2 derive from the email prefix.",
        ),
    ] = None,
    user_role: Annotated[
        list[str] | None,
        typer.Option("--user-role", help="User-role UID (repeatable). Grants the role on accept."),
    ] = None,
    org_unit: Annotated[
        list[str] | None,
        typer.Option("--org-unit", help="Organisation-unit UID for capture scope (repeatable)."),
    ] = None,
) -> None:
    """Create a user and send the invitation email.

    Hits POST /api/users/invite. DHIS2's configured mailer sends the link;
    the new user sets their password on accept. Prints the new user's UID.
    """
    invite = UserInvite(
        email=email,
        firstName=first_name,
        surname=surname,
        username=username,
        userRoles=[{"id": uid} for uid in (user_role or [])],
        organisationUnits=[{"id": uid} for uid in (org_unit or [])],
    )
    envelope = asyncio.run(service.invite_user(profile_from_env(), invite))
    created = envelope.created_uid
    if created:
        typer.echo(f"invited {email} -> user {created}")
    else:
        typer.echo(envelope.model_dump_json(indent=2, exclude_none=True, by_alias=True))


@app.command("reinvite")
def reinvite_command(
    uid: Annotated[str, typer.Argument(help="UID of a user who hasn't yet completed their invite.")],
) -> None:
    """Re-send the invitation email for a pending user (POST /api/users/{uid}/invite)."""
    envelope = asyncio.run(service.reinvite_user(profile_from_env(), uid))
    status = envelope.httpStatus or envelope.status or "OK"
    typer.echo(f"reinvite queued for {uid}: {status}")


@app.command("reset-password")
def reset_password_command(
    uid: Annotated[str, typer.Argument(help="UID of the user to reset.")],
) -> None:
    """Trigger DHIS2's password-reset email (POST /api/users/{uid}/reset)."""
    envelope = asyncio.run(service.reset_password(profile_from_env(), uid))
    status = envelope.httpStatus or envelope.status or "OK"
    typer.echo(f"reset link mailed for {uid}: {status}")


def _print_table(items: list[dict[str, Any]], columns: list[str]) -> None:
    """Render a rich table of users with the requested columns."""
    columns = [c.strip() for c in columns if c.strip() and not c.startswith(":")]
    if not columns:
        columns = sorted(items[0].keys()) if items else ["id"]
    table = Table(title=f"users ({len(items)} row{'s' if len(items) != 1 else ''})")
    for column in columns:
        table.add_column(column, overflow="fold")
    for item in items:
        table.add_row(*[_cell(item.get(column)) for column in columns])
    _console.print(table)


def _cell(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, (dict, list)):
        return json.dumps(value, separators=(",", ":"))
    return str(value)


def register(root_app: Any) -> None:
    """Mount this plugin's Typer sub-app under `dhis2 user`."""
    root_app.add_typer(app, name="user", help="DHIS2 user administration.")
