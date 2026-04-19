"""Typer sub-app for the `user-role` plugin (mounted under `dhis2 user-role`)."""

from __future__ import annotations

import asyncio
import json
from typing import Annotated, Any

import typer
from rich.console import Console
from rich.table import Table

from dhis2_core.plugins.user_role import service
from dhis2_core.profile import profile_from_env

app = typer.Typer(
    help="Inspect + administer DHIS2 user roles (list, authorities, grant/revoke users).", no_args_is_help=True
)
_console = Console()

_DEFAULT_FIELDS = "id,name,displayName,authorities,users"


@app.command("list")
@app.command("ls", hidden=True)
def list_command(
    fields: Annotated[str, typer.Option("--fields", help="DHIS2 field selector.")] = _DEFAULT_FIELDS,
    filters: Annotated[list[str] | None, typer.Option("--filter", help="Filter (repeatable).")] = None,
    order: Annotated[list[str] | None, typer.Option("--order", help="Sort clause (repeatable).")] = None,
    page_size: Annotated[int | None, typer.Option("--page-size", help="Server-side page size.")] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit JSON instead of a table.")] = False,
) -> None:
    """List user roles."""
    roles = asyncio.run(
        service.list_user_roles(
            profile_from_env(),
            fields=fields,
            filters=filters,
            order=order,
            page_size=page_size,
        )
    )
    dumped = [r.model_dump(by_alias=True, exclude_none=True, mode="json") for r in roles]
    if as_json:
        typer.echo(json.dumps(dumped, indent=2))
        return
    table = Table(title=f"user roles ({len(dumped)})")
    for column in ("id", "name", "authorities", "users"):
        table.add_column(column, overflow="fold")
    for item in dumped:
        authorities = item.get("authorities") or []
        users = item.get("users") or []
        table.add_row(
            str(item.get("id") or "-"),
            str(item.get("name") or "-"),
            str(len(authorities)),
            str(len(users)),
        )
    _console.print(table)


@app.command("get")
def get_command(
    uid: Annotated[str, typer.Argument(help="User-role UID.")],
    fields: Annotated[str | None, typer.Option("--fields", help="DHIS2 field selector.")] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit the raw UserRole JSON.")] = False,
) -> None:
    """Fetch one user role by UID. Prints a concise summary; `--json` for full payload."""
    role = asyncio.run(service.get_user_role(profile_from_env(), uid, fields=fields))
    if as_json:
        typer.echo(role.model_dump_json(indent=2, exclude_none=True, by_alias=True))
        return
    table = Table(title=f"user-role {role.name or role.id or '?'}", show_header=False, title_style="bold cyan")
    table.add_column("field", style="dim", overflow="fold")
    table.add_column("value", style="white", overflow="fold")
    table.add_row("id", str(role.id or "-"))
    table.add_row("name", str(role.name or "-"))
    table.add_row("displayName", str(role.displayName or "-"))
    table.add_row("code", str(role.code or "-"))
    table.add_row("description", str(role.description or "-"))
    authorities = role.authorities or []
    preview = ", ".join(sorted(authorities)[:10])
    table.add_row(
        f"authorities ({len(authorities)})",
        preview + (" ..." if len(authorities) > 10 else "") if authorities else "-",
    )
    if authorities and len(authorities) > 10:
        table.add_row("", f"[dim](run `dhis2 user-role authorities {role.id}` to list all)[/dim]")
    users = role.users or []
    table.add_row(
        f"users ({len(users)})",
        ", ".join(_ref(u) for u in users[:10]) + (" ..." if len(users) > 10 else "") if users else "-",
    )
    _console.print(table)


@app.command("authorities")
def authorities_command(
    uid: Annotated[str, typer.Argument(help="User-role UID.")],
) -> None:
    """Print the sorted authorities carried by one role, one per line."""
    auths = asyncio.run(service.list_authorities(profile_from_env(), uid))
    for auth in auths:
        typer.echo(auth)


@app.command("add-user")
def add_user_command(
    role_uid: Annotated[str, typer.Argument(help="User-role UID.")],
    user_uid: Annotated[str, typer.Argument(help="User UID to grant the role to.")],
) -> None:
    """Grant a user a role (POST /api/userRoles/<rid>/users/<uid>)."""
    envelope = asyncio.run(service.add_user(profile_from_env(), role_uid, user_uid))
    typer.echo(f"granted role {role_uid} to {user_uid}: {envelope.httpStatus or envelope.status or 'OK'}")


@app.command("remove-user")
def remove_user_command(
    role_uid: Annotated[str, typer.Argument(help="User-role UID.")],
    user_uid: Annotated[str, typer.Argument(help="User UID to revoke the role from.")],
) -> None:
    """Revoke a role from a user (DELETE /api/userRoles/<rid>/users/<uid>)."""
    envelope = asyncio.run(service.remove_user(profile_from_env(), role_uid, user_uid))
    typer.echo(f"revoked role {role_uid} from {user_uid}: {envelope.httpStatus or envelope.status or 'OK'}")


def _cell(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, (dict, list)):
        return json.dumps(value, separators=(",", ":"))
    return str(value)


def _ref(ref: Any) -> str:
    """Format a Reference-like object as 'displayName (uid)'."""
    if ref is None:
        return "-"
    if isinstance(ref, dict):
        name = ref.get("displayName") or ref.get("name") or ref.get("username")
        uid = ref.get("id")
        return f"{name} ({uid})" if name and uid else (name or str(uid) or "?")
    name = getattr(ref, "displayName", None) or getattr(ref, "name", None) or getattr(ref, "username", None)
    uid = getattr(ref, "id", None)
    if name and uid:
        return f"{name} ({uid})"
    return str(uid) if uid else "?"


def register(root_app: Any) -> None:
    """Mount this plugin's Typer sub-app under `dhis2 user-role`."""
    root_app.add_typer(app, name="user-role", help="DHIS2 user-role administration.")
