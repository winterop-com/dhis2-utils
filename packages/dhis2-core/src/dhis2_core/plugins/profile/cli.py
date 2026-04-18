"""Typer sub-app for the `profile` plugin (mounted under `dhis2 profile`)."""

from __future__ import annotations

import asyncio
import json
import os
from typing import Annotated, Any

import typer
from rich.console import Console
from rich.table import Table

from dhis2_core.client_context import build_auth, scope_from_resolved
from dhis2_core.oauth2_preflight import check_oauth2_server
from dhis2_core.plugins.profile import service
from dhis2_core.profile import Profile, UnknownProfileError, resolve

app = typer.Typer(
    help="Manage DHIS2 profiles (project .dhis2/profiles.toml and user-wide ~/.config/dhis2/profiles.toml).",
    no_args_is_help=True,
)
_console = Console()


@app.command("list")
def list_command(
    all_: Annotated[
        bool,
        typer.Option("--all", "-a", help="Include shadowed profiles (global entries hidden by project ones)."),
    ] = False,
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON.")] = False,
) -> None:
    """List every known profile with its source and default status."""
    summaries = service.list_profiles(include_shadowed=all_)
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
        name = f"{s['name']} [dim](shadowed)[/dim]" if s.get("shadowed") else s["name"]
        table.add_row(
            name,
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


def _run_verify(name: str) -> None:
    """Probe a profile and print a one-line OK/FAIL line; never raises."""
    result = asyncio.run(service.verify_profile(name))
    if result["ok"]:
        line = f"  verified: version={result['version']} user={result['username']} ({result['latency_ms']} ms)"
        typer.secho(line, fg=typer.colors.GREEN)
    else:
        typer.secho(f"  verify failed: {result['error']}", err=True, fg=typer.colors.YELLOW)
        typer.echo("  (profile was saved; run `dhis2 profile verify` later to re-check)")


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
    verify: Annotated[
        bool,
        typer.Option("--verify", help="Probe the instance after switching."),
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
    if verify:
        _run_verify(name)


@app.command("add")
def add_command(
    name: Annotated[str, typer.Argument()],
    base_url: Annotated[str | None, typer.Option("--url", help="DHIS2 base URL.")] = None,
    auth: Annotated[str, typer.Option("--auth", help="pat | basic | oauth2")] = "pat",
    token: Annotated[str | None, typer.Option("--token", help="PAT value (auth=pat).")] = None,
    username: Annotated[str | None, typer.Option("--username")] = None,
    password: Annotated[str | None, typer.Option("--password")] = None,
    client_id: Annotated[str | None, typer.Option("--client-id", help="OAuth2 client_id.")] = None,
    client_secret: Annotated[str | None, typer.Option("--client-secret", help="OAuth2 client_secret.")] = None,
    oauth_scope: Annotated[
        str,
        typer.Option("--scope", help="OAuth2 scope (DHIS2 only recognises `ALL`)."),
    ] = "ALL",
    redirect_uri: Annotated[
        str,
        typer.Option("--redirect-uri", help="OAuth2 redirect URI (must match the registered client)."),
    ] = "http://localhost:8765",
    from_env: Annotated[
        bool,
        typer.Option(
            "--from-env",
            help=(
                "Pull OAuth2 fields from DHIS2_OAUTH_CLIENT_ID / DHIS2_OAUTH_CLIENT_SECRET / "
                "DHIS2_OAUTH_REDIRECT_URI / DHIS2_OAUTH_SCOPES env vars (seeded .env.auth)."
            ),
        ),
    ] = False,
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
    verify: Annotated[
        bool,
        typer.Option("--verify", help="Probe /api/system/info + /api/me after saving."),
    ] = False,
) -> None:
    """Add (or upsert) a profile. Default scope is global — use --local for a project-scoped profile."""
    scope = _resolve_scope(is_global=global_scope, is_local=local_scope)
    if from_env and auth == "oauth2":
        client_id = client_id or os.environ.get("DHIS2_OAUTH_CLIENT_ID")
        client_secret = client_secret or os.environ.get("DHIS2_OAUTH_CLIENT_SECRET")
        redirect_uri = os.environ.get("DHIS2_OAUTH_REDIRECT_URI", redirect_uri)
        oauth_scope = os.environ.get("DHIS2_OAUTH_SCOPES", oauth_scope)
        base_url = base_url or os.environ.get("DHIS2_URL")
    if not base_url:
        raise typer.BadParameter("--url is required (or set DHIS2_URL + --from-env for OAuth2)")
    if auth == "pat":
        if not token:
            raise typer.BadParameter("auth=pat requires --token")
        profile = Profile(base_url=base_url, auth="pat", token=token)
    elif auth == "basic":
        if not (username and password):
            raise typer.BadParameter("auth=basic requires --username and --password")
        profile = Profile(base_url=base_url, auth="basic", username=username, password=password)
    elif auth == "oauth2":
        if not (client_id and client_secret):
            raise typer.BadParameter("auth=oauth2 requires --client-id + --client-secret (or --from-env)")
        profile = Profile(
            base_url=base_url,
            auth="oauth2",
            client_id=client_id,
            client_secret=client_secret,
            scope=oauth_scope,
            redirect_uri=redirect_uri,
        )
    else:
        raise typer.BadParameter(f"unsupported auth {auth!r}; use pat, basic, or oauth2")
    result = service.add_profile(name, profile, scope=scope, make_default=make_default)
    typer.echo(f"profile {name!r} saved to {result.path}")
    if result.shadowed_scope == "global":
        typer.secho(
            f"  warning: a profile named {name!r} also exists in the global scope; "
            "the project-scoped one will override it when you're in this directory.",
            err=True,
            fg=typer.colors.YELLOW,
        )
    elif result.shadowed_scope == "project":
        typer.secho(
            f"  warning: a profile named {name!r} also exists in a project scope; "
            "the project-scoped one will still override this global entry in that directory.",
            err=True,
            fg=typer.colors.YELLOW,
        )
    if verify:
        _run_verify(name)


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
    verify: Annotated[
        bool,
        typer.Option("--verify", help="Probe the instance after renaming."),
    ] = False,
) -> None:
    """Rename a profile in-place. Preserves scope and updates default if needed."""
    path = service.rename_profile(old_name, new_name)
    typer.echo(f"renamed {old_name!r} -> {new_name!r} in {path}")
    if verify:
        _run_verify(new_name)


@app.command("login")
def login_command(
    name: Annotated[str | None, typer.Argument(help="Profile name; omit to use the default.")] = None,
) -> None:
    """Run the OAuth2 authorization-code flow for a profile and persist its tokens.

    Opens a browser to the DHIS2 authorization endpoint, listens on the
    profile's `redirect_uri` (local FastAPI+uvicorn), exchanges the code for
    tokens, and writes them to the scope-appropriate tokens.sqlite.
    """
    resolved = resolve(name)
    if resolved.profile.auth != "oauth2":
        typer.secho(
            f"error: profile {resolved.name!r} uses auth={resolved.profile.auth!r}; "
            "login only applies to oauth2 profiles",
            err=True,
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    preflight_error = asyncio.run(check_oauth2_server(resolved.profile.base_url))
    if preflight_error is not None:
        typer.secho(f"error: {preflight_error}", err=True, fg=typer.colors.RED)
        raise typer.Exit(1)
    auth = build_auth(
        resolved.profile,
        profile_name=resolved.name,
        scope=scope_from_resolved(resolved),
    )
    typer.echo(f"opening browser for {resolved.name!r} -> {resolved.profile.base_url} ...")
    asyncio.run(auth.refresh_if_needed())
    _run_verify(resolved.name)


def register(root_app: Any) -> None:
    """Mount under `dhis2 profile`."""
    root_app.add_typer(app, name="profile", help="Manage DHIS2 profiles.")
