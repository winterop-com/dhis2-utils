"""Typer sub-app for the `maintenance` plugin (mounted under `dhis2 maintenance`)."""

from __future__ import annotations

import asyncio
import json
from typing import Annotated, Any

import typer
from rich.console import Console
from rich.table import Table

from dhis2_core.plugins.maintenance import service
from dhis2_core.plugins.maintenance.service import SoftDeleteTarget
from dhis2_core.profile import profile_from_env

app = typer.Typer(help="DHIS2 maintenance — tasks, cache, cleanup, data-integrity.", no_args_is_help=True)

task_app = typer.Typer(help="Background-task polling (all long-running DHIS2 ops).", no_args_is_help=True)
cleanup_app = typer.Typer(help="Hard-remove soft-deleted rows (unblocks metadata deletion).", no_args_is_help=True)
dataintegrity_app = typer.Typer(help="DHIS2 data-integrity checks.", no_args_is_help=True)

app.add_typer(task_app, name="task")
app.add_typer(cleanup_app, name="cleanup")
app.add_typer(dataintegrity_app, name="dataintegrity")

_console = Console()


@task_app.command("types")
def task_types_command() -> None:
    """List every background-job type DHIS2 tracks (ANALYTICS_TABLE, DATA_INTEGRITY, ...)."""
    for name in asyncio.run(service.list_task_types(profile_from_env())):
        typer.echo(name)


@task_app.command("list")
@task_app.command("ls", hidden=True)
def task_list_command(
    task_type: Annotated[str, typer.Argument(help="Task type, e.g. ANALYTICS_TABLE.")],
) -> None:
    """List every task UID recorded for a given job type."""
    for uid in asyncio.run(service.list_task_ids(profile_from_env(), task_type)):
        typer.echo(uid)


@task_app.command("status")
def task_status_command(
    task_type: Annotated[str, typer.Argument(help="Task type, e.g. ANALYTICS_TABLE.")],
    task_uid: Annotated[str, typer.Argument(help="Task UID returned by the async POST.")],
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON instead of a table.")] = False,
) -> None:
    """Print every notification emitted by a task, oldest first."""
    notifications = asyncio.run(service.get_task_notifications(profile_from_env(), task_type, task_uid))
    if as_json:
        typer.echo(json.dumps([n.model_dump(exclude_none=True) for n in notifications], indent=2))
        return
    table = Table(title=f"{task_type}/{task_uid} ({len(notifications)} notifications)")
    for column in ("time", "level", "completed", "message"):
        table.add_column(column, overflow="fold")
    for notification in notifications:
        table.add_row(
            notification.time or "-",
            notification.level or "-",
            "*" if notification.completed else "",
            notification.message or "-",
        )
    _console.print(table)


@task_app.command("watch")
def task_watch_command(
    task_type: Annotated[str, typer.Argument(help="Task type, e.g. DATA_INTEGRITY.")],
    task_uid: Annotated[str, typer.Argument(help="Task UID returned by the async POST.")],
    interval: Annotated[float, typer.Option("--interval", help="Poll interval in seconds.")] = 2.0,
    timeout: Annotated[float | None, typer.Option("--timeout", help="Abort after N seconds (default 600).")] = 600.0,
) -> None:
    """Poll a task until it reports `completed=true`, streaming each new notification."""
    from dhis2_core.cli_task_watch import stream_task_to_stdout

    asyncio.run(
        stream_task_to_stdout(profile_from_env(), task_type, task_uid, interval=interval, timeout=timeout),
    )


@app.command("cache")
def cache_command() -> None:
    """Clear every server-side cache (Hibernate + app caches)."""
    asyncio.run(service.clear_cache(profile_from_env()))
    typer.echo("caches cleared")


@cleanup_app.command("data-values")
def cleanup_data_values_command() -> None:
    """Hard-remove soft-deleted data values from `/api/dataValueSets` imports."""
    asyncio.run(service.remove_soft_deleted(profile_from_env(), SoftDeleteTarget.DATA_VALUES))
    typer.echo("soft-deleted data values removed")


@cleanup_app.command("events")
def cleanup_events_command() -> None:
    """Hard-remove soft-deleted tracker events."""
    asyncio.run(service.remove_soft_deleted(profile_from_env(), SoftDeleteTarget.EVENTS))
    typer.echo("soft-deleted events removed")


@cleanup_app.command("enrollments")
def cleanup_enrollments_command() -> None:
    """Hard-remove soft-deleted tracker enrollments."""
    asyncio.run(service.remove_soft_deleted(profile_from_env(), SoftDeleteTarget.ENROLLMENTS))
    typer.echo("soft-deleted enrollments removed")


@cleanup_app.command("tracked-entities")
def cleanup_tracked_entities_command() -> None:
    """Hard-remove soft-deleted tracked entities."""
    asyncio.run(service.remove_soft_deleted(profile_from_env(), SoftDeleteTarget.TRACKED_ENTITIES))
    typer.echo("soft-deleted tracked entities removed")


@dataintegrity_app.command("list")
@dataintegrity_app.command("ls", hidden=True)
def dataintegrity_list_command(
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON instead of a table.")] = False,
) -> None:
    """List every built-in data-integrity check (name, section, severity)."""
    checks = asyncio.run(service.list_dataintegrity_checks(profile_from_env()))
    if as_json:
        typer.echo(json.dumps([c.model_dump(exclude_none=True) for c in checks], indent=2))
        return
    table = Table(title=f"data-integrity checks ({len(checks)})")
    for column in ("name", "section", "severity", "issuesIdType"):
        table.add_column(column, overflow="fold")
    for check in checks:
        table.add_row(check.name, check.section or "-", check.severity or "-", check.issuesIdType or "-")
    _console.print(table)


@dataintegrity_app.command("run")
def dataintegrity_run_command(
    check: Annotated[list[str] | None, typer.Argument(help="Check name(s); omit to run every check.")] = None,
    details: Annotated[
        bool, typer.Option("--details", help="Hit /details (populates issues[]) instead of /summary.")
    ] = False,
    watch: Annotated[
        bool,
        typer.Option(
            "--watch",
            "-w",
            help="After kicking off the job, poll /api/system/tasks until it reports completed=true.",
        ),
    ] = False,
    interval: Annotated[float, typer.Option("--interval", help="Poll interval in seconds when --watch is set.")] = 2.0,
    timeout: Annotated[
        float | None, typer.Option("--timeout", help="Abort polling after N seconds (default 600).")
    ] = 600.0,
) -> None:
    """Kick off a data-integrity run; with --watch, stream progress to completion."""
    from dhis2_core.cli_task_watch import stream_task_to_stdout

    profile = profile_from_env()
    response = asyncio.run(service.run_dataintegrity(profile, checks=check, details=details))
    if not watch:
        typer.echo(response.model_dump_json(indent=2, exclude_none=True))
        return
    ref = response.task_ref()
    if ref is None:
        typer.secho("error: response has no jobType/id — nothing to watch", err=True, fg=typer.colors.RED)
        raise typer.Exit(1)
    job_type, task_uid = ref
    asyncio.run(stream_task_to_stdout(profile, job_type, task_uid, interval=interval, timeout=timeout))


@dataintegrity_app.command("result")
def dataintegrity_result_command(
    check: Annotated[list[str] | None, typer.Argument(help="Check name(s) to read; omit for all.")] = None,
    details: Annotated[
        bool, typer.Option("--details", help="Hit /details (issues[]) instead of /summary (count only).")
    ] = False,
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON instead of a table.")] = False,
) -> None:
    """Read the stored result of a completed data-integrity run (summary or details mode)."""
    coro = (
        service.get_dataintegrity_details(profile_from_env(), checks=check)
        if details
        else service.get_dataintegrity_summary(profile_from_env(), checks=check)
    )
    report = asyncio.run(coro)
    if as_json:
        typer.echo(report.model_dump_json(indent=2, exclude_none=True))
        return
    table = Table(title=f"data-integrity results ({len(report.results)})")
    for column in ("name", "severity", "count", "finishedTime"):
        table.add_column(column, overflow="fold")
    for name, result in report.results.items():
        table.add_row(
            name,
            result.severity or "-",
            str(result.count) if result.count is not None else "-",
            result.finishedTime or "-",
        )
    _console.print(table)


def register(root_app: Any) -> None:
    """Mount under `dhis2 maintenance`."""
    root_app.add_typer(app, name="maintenance", help="DHIS2 maintenance (tasks, cache, integrity, cleanup).")
