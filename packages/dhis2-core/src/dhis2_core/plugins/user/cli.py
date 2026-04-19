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
    as_json: Annotated[bool, typer.Option("--json", help="Emit the raw User payload instead of a summary.")] = False,
) -> None:
    """Fetch one user by UID or username. Prints a concise summary; `--json` for full payload."""
    try:
        user = asyncio.run(service.get_user(profile_from_env(), uid_or_username, fields=fields))
    except UserNotFoundError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(code=1) from None
    if as_json:
        typer.echo(user.model_dump_json(indent=2, exclude_none=True, by_alias=True))
        return
    full_name = user.displayName or f"{user.firstName or ''} {user.surname or ''}".strip() or "-"
    table = Table(title=f"user {user.username or user.id or '?'}", show_header=False, title_style="bold cyan")
    table.add_column("field", style="dim", overflow="fold")
    table.add_column("value", style="white", overflow="fold")
    table.add_row("id", str(user.id or "-"))
    table.add_row("username", str(user.username or "-"))
    table.add_row("name", full_name)
    table.add_row("email", str(user.email or "-"))
    disabled = user.disabled
    table.add_row("disabled", "[red]yes[/red]" if disabled else "[green]no[/green]" if disabled is not None else "-")
    table.add_row("lastLogin", str(user.lastLogin or "-"))
    table.add_row("created", str(user.created or "-"))
    table.add_row("twoFactor", str(getattr(user, "twoFactorType", None) or "-"))
    roles = [_ref_display(r) for r in (user.userRoles or [])]
    table.add_row(f"userRoles ({len(roles)})", ", ".join(roles) if roles else "-")
    groups = [_ref_display(g) for g in (user.userGroups or [])]
    table.add_row(f"userGroups ({len(groups)})", ", ".join(groups) if groups else "-")
    org_units = [_ref_display(ou) for ou in (user.organisationUnits or [])]
    table.add_row(f"orgUnits ({len(org_units)})", ", ".join(org_units) if org_units else "-")
    authorities = getattr(user, "authorities", None) or []
    if authorities:
        table.add_row(
            f"authorities ({len(authorities)})",
            ", ".join(sorted(authorities)[:10]) + (" ..." if len(authorities) > 10 else ""),
        )
    _console.print(table)


@app.command("me")
def me_command(
    as_json: Annotated[bool, typer.Option("--json", help="Emit the raw /api/me payload.")] = False,
) -> None:
    """Print the authenticated user's `/api/me` summary. `--json` for full payload."""
    payload = asyncio.run(service.current_user(profile_from_env()))
    if as_json:
        typer.echo(json.dumps(payload, indent=2))
        return
    table = Table(
        title=f"me — {payload.get('username') or payload.get('id') or '?'}",
        show_header=False,
        title_style="bold cyan",
    )
    table.add_column("field", style="dim", overflow="fold")
    table.add_column("value", style="white", overflow="fold")
    table.add_row("id", str(payload.get("id", "-")))
    table.add_row("username", str(payload.get("username", "-")))
    table.add_row("displayName", str(payload.get("displayName", "-")))
    table.add_row("email", str(payload.get("email", "-")))
    table.add_row("firstName", str(payload.get("firstName", "-")))
    table.add_row("surname", str(payload.get("surname", "-")))
    table.add_row("lastLogin", str(payload.get("lastLogin", "-")))
    table.add_row("created", str(payload.get("created", "-")))
    authorities = payload.get("authorities") or []
    preview = ", ".join(sorted(authorities)[:10])
    table.add_row(
        f"authorities ({len(authorities)})",
        preview + (" ..." if len(authorities) > 10 else "") if authorities else "-",
    )
    org_units = payload.get("organisationUnits") or []
    ou_names = [_ref_display(ou) for ou in org_units]
    table.add_row(
        f"organisationUnits ({len(ou_names)})",
        ", ".join(ou_names) if ou_names else "-",
    )
    data_view_ous = payload.get("dataViewOrganisationUnits") or []
    table.add_row("dataViewOrgUnits", str(len(data_view_ous)))
    user_groups = payload.get("userGroups") or []
    table.add_row(
        f"userGroups ({len(user_groups)})",
        ", ".join(_ref_display(g) for g in user_groups) if user_groups else "-",
    )
    programs = payload.get("programs") or []
    program_names = [_ref_display(p) for p in programs]
    table.add_row(
        f"programs ({len(program_names)})",
        ", ".join(program_names) if program_names else "-",
    )
    _console.print(table)


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


def _ref_display(ref: Any) -> str:
    """Format a user/group/OU reference as `name (uid)` or just the UID string."""
    if ref is None:
        return "-"
    if isinstance(ref, str):
        return ref
    if isinstance(ref, dict):
        name = ref.get("displayName") or ref.get("name") or ref.get("username")
        uid = ref.get("id")
        return f"{name} ({uid})" if name and uid else (name or str(uid) or "?")
    name = getattr(ref, "displayName", None) or getattr(ref, "name", None) or getattr(ref, "username", None)
    uid = getattr(ref, "id", None)
    if name and uid:
        return f"{name} ({uid})"
    if uid:
        return str(uid)
    return "?"


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
