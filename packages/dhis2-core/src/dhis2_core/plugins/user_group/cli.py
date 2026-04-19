"""Typer sub-app for the `user-group` plugin (mounted under `dhis2 user-group`)."""

from __future__ import annotations

import asyncio
import json
from typing import Annotated, Any

import typer
from dhis2_client import ACCESS_READ_METADATA, ACCESS_READ_WRITE_METADATA, SharingBuilder
from rich.console import Console
from rich.table import Table

from dhis2_core.plugins.user_group import service
from dhis2_core.profile import profile_from_env

app = typer.Typer(help="Inspect + administer DHIS2 user groups (list, members, sharing).", no_args_is_help=True)
_console = Console()

_DEFAULT_FIELDS = "id,name,displayName,users"


@app.command("list")
@app.command("ls", hidden=True)
def list_command(
    fields: Annotated[str, typer.Option("--fields", help="DHIS2 field selector.")] = _DEFAULT_FIELDS,
    filters: Annotated[
        list[str] | None,
        typer.Option("--filter", help="Filter 'property:operator:value' (repeatable)."),
    ] = None,
    order: Annotated[
        list[str] | None,
        typer.Option("--order", help="Sort clause 'property:asc|desc' (repeatable)."),
    ] = None,
    page_size: Annotated[int | None, typer.Option("--page-size", help="Server-side page size.")] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit JSON instead of a table.")] = False,
) -> None:
    """List user groups."""
    groups = asyncio.run(
        service.list_user_groups(
            profile_from_env(),
            fields=fields,
            filters=filters,
            order=order,
            page_size=page_size,
        )
    )
    dumped = [g.model_dump(by_alias=True, exclude_none=True, mode="json") for g in groups]
    if as_json:
        typer.echo(json.dumps(dumped, indent=2))
        return
    # Render with member-count instead of dumping the full users list.
    table = Table(title=f"user groups ({len(dumped)})")
    for column in ("id", "name", "displayName", "members"):
        table.add_column(column, overflow="fold")
    for item in dumped:
        members = item.get("users") or []
        table.add_row(
            str(item.get("id") or "-"),
            str(item.get("name") or "-"),
            str(item.get("displayName") or "-"),
            str(len(members)),
        )
    _console.print(table)


@app.command("get")
def get_command(
    uid: Annotated[str, typer.Argument(help="User-group UID.")],
    fields: Annotated[str | None, typer.Option("--fields", help="DHIS2 field selector.")] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit the raw UserGroup JSON.")] = False,
) -> None:
    """Fetch one user group by UID. Prints a concise summary; `--json` for full payload."""
    group = asyncio.run(service.get_user_group(profile_from_env(), uid, fields=fields))
    if as_json:
        typer.echo(group.model_dump_json(indent=2, exclude_none=True, by_alias=True))
        return
    table = Table(title=f"user-group {group.name or group.id or '?'}", show_header=False, title_style="bold cyan")
    table.add_column("field", style="dim", overflow="fold")
    table.add_column("value", style="white", overflow="fold")
    table.add_row("id", str(group.id or "-"))
    table.add_row("name", str(group.name or "-"))
    table.add_row("displayName", str(group.displayName or "-"))
    table.add_row("code", str(group.code or "-"))
    table.add_row("created", str(group.created or "-"))
    table.add_row("lastUpdated", str(group.lastUpdated or "-"))
    members = group.users or []
    table.add_row(
        f"members ({len(members)})",
        ", ".join(_ref(u) for u in members[:10]) + (" ..." if len(members) > 10 else "") if members else "-",
    )
    managed_groups = getattr(group, "managedGroups", None) or []
    if managed_groups:
        table.add_row(f"managedGroups ({len(managed_groups)})", ", ".join(_ref(g) for g in managed_groups))
    managed_by_groups = getattr(group, "managedByGroups", None) or []
    if managed_by_groups:
        table.add_row(f"managedBy ({len(managed_by_groups)})", ", ".join(_ref(g) for g in managed_by_groups))
    _console.print(table)


@app.command("add-member")
def add_member_command(
    group_uid: Annotated[str, typer.Argument(help="User-group UID.")],
    user_uid: Annotated[str, typer.Argument(help="User UID to add.")],
) -> None:
    """Add a user to a group (POST /api/userGroups/<gid>/members/<uid>)."""
    envelope = asyncio.run(service.add_member(profile_from_env(), group_uid, user_uid))
    typer.echo(f"added {user_uid} -> {group_uid}: {envelope.httpStatus or envelope.status or 'OK'}")


@app.command("remove-member")
def remove_member_command(
    group_uid: Annotated[str, typer.Argument(help="User-group UID.")],
    user_uid: Annotated[str, typer.Argument(help="User UID to remove.")],
) -> None:
    """Remove a user from a group (DELETE /api/userGroups/<gid>/members/<uid>)."""
    envelope = asyncio.run(service.remove_member(profile_from_env(), group_uid, user_uid))
    typer.echo(f"removed {user_uid} from {group_uid}: {envelope.httpStatus or envelope.status or 'OK'}")


@app.command("sharing-get")
def sharing_get_command(
    uid: Annotated[str, typer.Argument(help="User-group UID.")],
    as_json: Annotated[bool, typer.Option("--json", help="Emit the raw SharingObject JSON.")] = False,
) -> None:
    """Print the current sharing block for one user group. `--json` for full payload."""
    sharing = asyncio.run(service.get_group_sharing(profile_from_env(), uid))
    if as_json:
        typer.echo(sharing.model_dump_json(indent=2, exclude_none=True, by_alias=True))
        return
    table = Table(
        title=f"sharing — userGroup {sharing.name or sharing.id or '?'}",
        show_header=False,
        title_style="bold cyan",
    )
    table.add_column("field", style="dim", overflow="fold")
    table.add_column("value", style="white", overflow="fold")
    table.add_row("id", str(sharing.id or "-"))
    table.add_row("publicAccess", f"[magenta]{sharing.publicAccess or '--------'}[/magenta]")
    table.add_row("externalAccess", str(sharing.externalAccess if sharing.externalAccess is not None else "-"))
    owner = sharing.user.id if sharing.user else "-"
    table.add_row("owner", str(owner))
    user_accesses = sharing.userAccesses or []
    table.add_row(f"userAccesses ({len(user_accesses)})", "")
    for ua in user_accesses:
        label = ua.displayName or ua.username or ua.name or ua.id or "?"
        table.add_row(f"  {label}", f"[magenta]{ua.access or '--------'}[/magenta]  ({ua.id or '?'})")
    group_accesses = sharing.userGroupAccesses or []
    table.add_row(f"userGroupAccesses ({len(group_accesses)})", "")
    for ga in group_accesses:
        label = ga.displayName or ga.name or ga.id or "?"
        table.add_row(f"  {label}", f"[magenta]{ga.access or '--------'}[/magenta]  ({ga.id or '?'})")
    _console.print(table)


@app.command("sharing-grant-user")
def sharing_grant_user_command(
    group_uid: Annotated[str, typer.Argument(help="User-group UID.")],
    user_uid: Annotated[str, typer.Argument(help="User UID to grant.")],
    metadata_write: Annotated[
        bool,
        typer.Option("--metadata-write/--metadata-read", help="Grant metadata write (default) or read-only."),
    ] = True,
) -> None:
    """Grant one user access to a group (shortcut over `/api/sharing`).

    Preserves existing userAccesses/userGroupAccesses by fetching the current
    sharing block first, then appending the new grant.
    """
    profile = profile_from_env()
    current = asyncio.run(service.get_group_sharing(profile, group_uid))
    builder = SharingBuilder(
        public_access=current.publicAccess or ACCESS_READ_METADATA,
        external_access=current.externalAccess or False,
        owner_user_id=current.user.id if current.user else None,
    )
    # Replay existing grants.
    for user_access in current.userAccesses or []:
        if user_access.id and user_access.access:
            builder = builder.grant_user(user_access.id, user_access.access)
    for group_access in current.userGroupAccesses or []:
        if group_access.id and group_access.access:
            builder = builder.grant_user_group(group_access.id, group_access.access)
    # Append / overwrite the target grant.
    access = ACCESS_READ_WRITE_METADATA if metadata_write else ACCESS_READ_METADATA
    builder = builder.grant_user(user_uid, access)
    envelope = asyncio.run(service.apply_group_sharing(profile, group_uid, builder))
    typer.echo(f"granted {user_uid}:{access} on {group_uid}: {envelope.httpStatus or envelope.status or 'OK'}")


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
    """Mount this plugin's Typer sub-app under `dhis2 user-group`."""
    root_app.add_typer(app, name="user-group", help="DHIS2 user-group administration.")
