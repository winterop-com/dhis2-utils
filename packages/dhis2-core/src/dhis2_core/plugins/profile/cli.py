"""Typer sub-app for the `profile` plugin (mounted under `dhis2 profile`)."""

from __future__ import annotations

import asyncio
import json
from typing import Annotated, Any

import typer
from rich.console import Console
from rich.table import Table

from dhis2_core.plugins.profile import service
from dhis2_core.profile import Profile, UnknownProfileError

app = typer.Typer(
    help="Manage DHIS2 profiles (project .dhis2/profiles.toml and user-wide ~/.config/dhis2/profiles.toml).",
    no_args_is_help=True,
)
_console = Console()


@app.command("list")
def list_command(
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON.")] = False,
) -> None:
    """List every known profile with its source and default status."""
    summaries = service.list_profiles()
    if as_json:
        typer.echo(json.dumps(summaries, indent=2))
        return
    if not summaries:
        typer.echo("no profiles found — run `dhis2 profile add <name>` to create one.")
        return
    table = Table(title=f"DHIS2 profiles ({len(summaries)})")
    table.add_column("name")
    table.add_column("default")
    table.add_column("auth")
    table.add_column("base_url", overflow="fold")
    table.add_column("source")
    for s in summaries:
        table.add_row(
            s["name"],
            "*" if s["is_default"] else "",
            s["auth"],
            s["base_url"],
            s["source"],
        )
    _console.print(table)


@app.command("verify")
def verify_command(
    name: Annotated[
        str | None,
        typer.Argument(help="Profile name to verify; omit to verify all."),
    ] = None,
    as_json: Annotated[bool, typer.Option("--json")] = False,
) -> None:
    """Verify one profile or all profiles by hitting /api/system/info + /api/me."""
    if name:
        result = asyncio.run(service.verify_profile(name))
        if as_json:
            typer.echo(json.dumps(result, indent=2))
        else:
            _print_verify_row(result)
        raise typer.Exit(0 if result["ok"] else 1)

    results = asyncio.run(service.verify_all_profiles())
    if as_json:
        typer.echo(json.dumps(results, indent=2))
        raise typer.Exit(0 if all(r["ok"] for r in results) else 1)
    table = Table(title=f"DHIS2 profile verification ({len(results)})")
    table.add_column("name")
    table.add_column("ok")
    table.add_column("version")
    table.add_column("user")
    table.add_column("latency")
    table.add_column("error", overflow="fold")
    for r in results:
        table.add_row(
            r["name"],
            "yes" if r["ok"] else "NO",
            r["version"] or "-",
            r["username"] or "-",
            f"{r['latency_ms']} ms" if r["latency_ms"] is not None else "-",
            r["error"] or "",
        )
    _console.print(table)
    raise typer.Exit(0 if all(r["ok"] for r in results) else 1)


def _print_verify_row(result: dict[str, Any]) -> None:
    status = "OK" if result["ok"] else "FAIL"
    line = f"{status} {result['name']}  {result['base_url']}  auth={result['auth']}"
    if result["ok"]:
        line += f"  version={result['version']}  user={result['username']}  {result['latency_ms']} ms"
    else:
        line += f"  error: {result['error']}"
    typer.echo(line)


@app.command("show")
def show_command(
    name: Annotated[str, typer.Argument()],
    secrets: Annotated[bool, typer.Option("--secrets", help="Include sensitive values.")] = False,
) -> None:
    """Print one profile (secrets redacted by default)."""
    typer.echo(json.dumps(service.show_profile(name, include_secrets=secrets), indent=2))


def _resolve_scope(*, is_global: bool, is_local: bool, default: str = "global") -> str:
    """Translate the --global/--local flag pair into a 'global' | 'project' string."""
    if is_global and is_local:
        raise typer.BadParameter("--global and --local are mutually exclusive")
    if is_local:
        return "project"
    if is_global:
        return "global"
    return default


@app.command("switch")
def switch_command(
    name: Annotated[str, typer.Argument(help="Profile name to set as default.")],
    global_scope: Annotated[
        bool,
        typer.Option("--global", help="Write to ~/.config/dhis2/profiles.toml (default)."),
    ] = False,
    local_scope: Annotated[
        bool,
        typer.Option("--local", help="Write to ./.dhis2/profiles.toml instead."),
    ] = False,
) -> None:
    """Set `default = <name>` in the global (default) or project profiles.toml."""
    scope = _resolve_scope(is_global=global_scope, is_local=local_scope)
    try:
        path = service.set_default_profile(name, scope=scope)
    except UnknownProfileError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(1) from exc
    typer.echo(f"default profile in {scope} scope set to {name!r} ({path})")


@app.command("add")
def add_command(
    name: Annotated[str, typer.Argument()],
    base_url: Annotated[str, typer.Option("--url", help="DHIS2 base URL.")],
    auth: Annotated[str, typer.Option("--auth", help="pat | basic")] = "pat",
    token: Annotated[str | None, typer.Option("--token", help="PAT value (auth=pat).")] = None,
    username: Annotated[str | None, typer.Option("--username")] = None,
    password: Annotated[str | None, typer.Option("--password")] = None,
    global_scope: Annotated[
        bool,
        typer.Option(
            "--global",
            help="Save to ~/.config/dhis2/profiles.toml (default — user-wide, applies everywhere).",
        ),
    ] = False,
    local_scope: Annotated[
        bool,
        typer.Option(
            "--local",
            help="Save to ./.dhis2/profiles.toml instead (project-scoped, overrides global).",
        ),
    ] = False,
    make_default: Annotated[bool, typer.Option("--default", help="Set as default after adding.")] = False,
) -> None:
    """Add (or upsert) a profile. Default scope is global — use --local for a project-scoped profile."""
    scope = _resolve_scope(is_global=global_scope, is_local=local_scope)
    if auth == "pat":
        if not token:
            raise typer.BadParameter("auth=pat requires --token")
        profile = Profile(base_url=base_url, auth="pat", token=token)
    elif auth == "basic":
        if not (username and password):
            raise typer.BadParameter("auth=basic requires --username and --password")
        profile = Profile(base_url=base_url, auth="basic", username=username, password=password)
    else:
        raise typer.BadParameter(f"unsupported auth {auth!r}; use pat or basic")
    path = service.add_profile(name, profile, scope=scope, make_default=make_default)
    typer.echo(f"profile {name!r} saved to {path}")


@app.command("remove")
def remove_command(
    name: Annotated[str, typer.Argument()],
    global_scope: Annotated[
        bool,
        typer.Option("--global", help="Remove from ~/.config/dhis2/profiles.toml specifically."),
    ] = False,
    local_scope: Annotated[
        bool,
        typer.Option("--local", help="Remove from ./.dhis2/profiles.toml specifically."),
    ] = False,
) -> None:
    """Remove a profile. Without --global/--local, removes from whichever file holds it."""
    if global_scope and local_scope:
        raise typer.BadParameter("--global and --local are mutually exclusive")
    scope: str | None = None
    if local_scope:
        scope = "project"
    elif global_scope:
        scope = "global"
    try:
        path = service.remove_profile(name, scope=scope)
    except UnknownProfileError as exc:
        typer.echo(f"error: {exc}", err=True)
        raise typer.Exit(1) from exc
    typer.echo(f"removed {name!r} from {path}")


@app.command("rename")
def rename_command(
    old_name: Annotated[str, typer.Argument(help="Current profile name.")],
    new_name: Annotated[str, typer.Argument(help="New profile name (letters, digits, underscores).")],
) -> None:
    """Rename a profile in-place. Preserves scope and updates default if needed."""
    path = service.rename_profile(old_name, new_name)
    typer.echo(f"renamed {old_name!r} -> {new_name!r} in {path}")


def register(root_app: Any) -> None:
    """Mount under `dhis2 profile`."""
    root_app.add_typer(app, name="profile", help="Manage DHIS2 profiles.")
