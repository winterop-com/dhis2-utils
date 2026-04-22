"""Typer sub-app for `dhis2 apps` — install / uninstall / update DHIS2 apps."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Annotated, Any

import typer
from rich.console import Console
from rich.table import Table

from dhis2_core.plugins.apps import service
from dhis2_core.plugins.apps.models import UpdateOutcome, UpdateSummary
from dhis2_core.profile import profile_from_env

app = typer.Typer(
    help="DHIS2 apps — install / uninstall / update via /api/apps + /api/appHub.",
    no_args_is_help=True,
)
_console = Console()


@app.command("list")
@app.command("ls", hidden=True)
def list_command(
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON instead of a table.")] = False,
) -> None:
    """List every installed app (`GET /api/apps`)."""
    apps = asyncio.run(service.list_apps(profile_from_env()))
    if as_json:
        typer.echo("[" + ",".join(a.model_dump_json(exclude_none=True) for a in apps) + "]")
        return
    if not apps:
        typer.echo("no apps installed")
        return
    table = Table(title=f"DHIS2 apps ({len(apps)})")
    table.add_column("key", style="cyan", no_wrap=True)
    table.add_column("name", overflow="fold")
    table.add_column("version", justify="right")
    table.add_column("type")
    table.add_column("bundled", justify="center")
    table.add_column("hub id", style="dim", overflow="fold")
    for row in apps:
        table.add_row(
            row.key or "-",
            row.displayName or row.name or "-",
            row.version or "-",
            str(row.appType or "-"),
            "[green]yes[/green]" if row.bundled else "[dim]no[/dim]",
            row.app_hub_id or "-",
        )
    _console.print(table)


@app.command("add")
def add_command(
    source: Annotated[
        str,
        typer.Argument(
            help=(
                "Either a path to a local `.zip` (installs via /api/apps) "
                "or an App Hub version id (installs via /api/appHub/{versionId})."
            ),
        ),
    ],
) -> None:
    """Install an app from a local zip or an App Hub version id.

    Auto-dispatches based on whether `source` is an existing file on disk:
    file → multipart upload to `/api/apps`; otherwise → POST to
    `/api/appHub/{source}`. DHIS2 overwrites an existing install of the
    same app in both paths.
    """
    candidate = Path(source)
    profile = profile_from_env()
    if candidate.is_file():
        asyncio.run(service.install_from_file(profile, candidate))
        typer.echo(f"installed from file: {candidate.name}")
    else:
        asyncio.run(service.install_from_hub(profile, source))
        typer.echo(f"installed from App Hub version {source}")


@app.command("remove")
@app.command("rm", hidden=True)
def remove_command(
    key: Annotated[str, typer.Argument(help="App key (folder name) from `apps list`.")],
    yes: Annotated[bool, typer.Option("--yes", "-y", help="Skip the confirmation prompt.")] = False,
) -> None:
    """Uninstall an app by key (`DELETE /api/apps/{key}`)."""
    if not yes and not typer.confirm(f"remove installed app {key!r}?", default=False):
        raise typer.Exit(0)
    asyncio.run(service.uninstall(profile_from_env(), key))
    typer.echo(f"removed {key}")


@app.command("update")
def update_command(
    key: Annotated[str | None, typer.Argument(help="App key; omit with --all to update every app.")] = None,
    all_apps: Annotated[bool, typer.Option("--all", help="Update every installed app.")] = False,
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            "--check",
            help=(
                "Show what would change without installing — report the newer hub "
                "version for every app with an update available, tagged AVAILABLE."
            ),
        ),
    ] = False,
    as_json: Annotated[bool, typer.Option("--json", help="Emit the summary as JSON.")] = False,
) -> None:
    """Update one app or every installed app to its latest App Hub version.

    Apps without an `app_hub_id` (typically side-loaded zips) are reported
    as `SKIPPED` — they're not installable via the hub. Bundled core apps
    (`bundled=True`) still carry an `app_hub_id` and can be updated in
    place, so they're treated like any other hub-updatable app. With
    `--dry-run` (alias `--check`), every available update prints as
    `AVAILABLE` and no install call is made, so you can preview the delta
    first.
    """
    profile = profile_from_env()
    if all_apps and key:
        raise typer.BadParameter("pass either a key or --all, not both")
    if not all_apps and not key:
        raise typer.BadParameter("pass a key, or use --all to update every app")
    if all_apps:
        summary = asyncio.run(service.update_all(profile, dry_run=dry_run))
        if as_json:
            typer.echo(summary.model_dump_json(exclude_none=True))
            return
        _render_summary(summary, dry_run=dry_run)
        return
    assert key is not None  # guarded above
    outcome = asyncio.run(service.update_one(profile, key, dry_run=dry_run))
    if as_json:
        typer.echo(outcome.model_dump_json(exclude_none=True))
        return
    _render_summary(UpdateSummary(outcomes=[outcome]), dry_run=dry_run)


@app.command("reload")
def reload_command() -> None:
    """Ask DHIS2 to re-read every app from disk (`PUT /api/apps`)."""
    asyncio.run(service.reload_apps(profile_from_env()))
    typer.echo("apps reloaded from disk")


@app.command("hub-list")
def hub_list_command(
    search: Annotated[
        str | None,
        typer.Option(
            "--search",
            "-s",
            help="Case-insensitive substring filter on name + description (client-side).",
        ),
    ] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON instead of a table.")] = False,
    limit: Annotated[int, typer.Option("--limit", help="Cap the number of rows shown.")] = 50,
) -> None:
    """List apps available in the configured App Hub (`GET /api/appHub`).

    Pass `--search <query>` to filter the catalog by app name or
    description substring. The filter runs client-side — DHIS2's
    `/api/appHub` proxy doesn't expose a server-side query parameter
    on v42, so the full catalog is fetched and filtered after.
    """
    hub = asyncio.run(service.hub_list(profile_from_env(), query=search))
    hub = hub[:limit]
    if as_json:
        typer.echo("[" + ",".join(a.model_dump_json(exclude_none=True) for a in hub) + "]")
        return
    if not hub:
        suffix = f" matching {search!r}" if search else ""
        typer.echo(f"App Hub returned no apps{suffix}")
        return
    title_suffix = f" matching {search!r}" if search else ""
    table = Table(title=f"DHIS2 App Hub ({len(hub)} shown{title_suffix})")
    table.add_column("id", style="cyan", overflow="fold")
    table.add_column("name", overflow="fold")
    table.add_column("type")
    table.add_column("versions", justify="right")
    for row in hub:
        table.add_row(
            row.id or "-",
            row.name or "-",
            row.app_type or "-",
            str(len(row.versions)),
        )
    _console.print(table)


@app.command("hub-url")
def hub_url_command(
    set_url: Annotated[
        str | None,
        typer.Option(
            "--set",
            help="Point this DHIS2 instance at a different App Hub (writes the `keyAppHubUrl` system setting).",
        ),
    ] = None,
    clear: Annotated[
        bool,
        typer.Option(
            "--clear",
            help="Clear the `keyAppHubUrl` setting so DHIS2 reverts to its default hub.",
        ),
    ] = False,
) -> None:
    """Read or write DHIS2's configured App Hub URL (`keyAppHubUrl` system setting).

    The App Hub is open source (https://github.com/dhis2/app-hub); teams
    running a self-hosted hub can point DHIS2 at it by setting this.
    Pass `--set <url>` to update, `--clear` to revert to DHIS2's
    hard-coded default (typically `https://apps.dhis2.org/api`).
    """
    if set_url and clear:
        raise typer.BadParameter("--set and --clear are mutually exclusive")
    profile = profile_from_env()
    if clear:
        asyncio.run(service.set_hub_url(profile, None))
        typer.echo("cleared keyAppHubUrl — DHIS2 will use its default App Hub")
        return
    if set_url:
        asyncio.run(service.set_hub_url(profile, set_url))
        typer.echo(f"keyAppHubUrl -> {set_url}")
        return
    current = asyncio.run(service.get_hub_url(profile))
    if current is None:
        typer.echo("keyAppHubUrl: <not set>  (DHIS2 is using its default App Hub)")
    else:
        typer.echo(f"keyAppHubUrl: {current}")


def _render_summary(summary: UpdateSummary, *, dry_run: bool = False) -> None:
    """Print an update-outcome table + totals footer."""
    if not summary.outcomes:
        typer.echo("no apps to update")
        return
    title = "available updates (dry run)" if dry_run else "update summary"
    table = Table(title=title)
    table.add_column("key", style="cyan", no_wrap=True)
    table.add_column("name", overflow="fold")
    table.add_column("from", justify="right")
    table.add_column("to", justify="right")
    table.add_column("status")
    table.add_column("reason", style="dim", overflow="fold")
    for outcome in summary.outcomes:
        table.add_row(
            outcome.key,
            outcome.name,
            outcome.from_version or "-",
            outcome.to_version or "-",
            _color_status(outcome.status),
            outcome.reason or "",
        )
    _console.print(table)
    if dry_run:
        typer.echo(
            f"totals: available={summary.available} up-to-date={summary.up_to_date} "
            f"skipped={summary.skipped} failed={summary.failed}  "
            "(re-run without --dry-run to install)",
        )
    else:
        typer.echo(
            f"totals: updated={summary.updated} up-to-date={summary.up_to_date} "
            f"skipped={summary.skipped} failed={summary.failed}",
        )


def _color_status(status: str) -> str:
    """Colourize the status column for readable terminal output."""
    return {
        "UPDATED": f"[green bold]{status}[/green bold]",
        "AVAILABLE": f"[green]{status}[/green]",
        "UP_TO_DATE": f"[dim]{status}[/dim]",
        "SKIPPED": f"[yellow]{status}[/yellow]",
        "FAILED": f"[red bold]{status}[/red bold]",
    }.get(status, status)


def register(parent_app: Any) -> None:
    """Mount `dhis2 apps` on the root CLI."""
    parent_app.add_typer(app, name="apps", help="DHIS2 apps — /api/apps + /api/appHub.")


__all__ = ["register", "UpdateOutcome"]
