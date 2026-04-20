"""Typer sub-app for the `maintenance` plugin (mounted under `dhis2 maintenance`)."""

from __future__ import annotations

import asyncio
import json
from collections.abc import Callable, Coroutine
from typing import Annotated, Any

import typer
from dhis2_client import WebMessageResponse
from rich.console import Console
from rich.table import Table

from dhis2_core.plugins.maintenance import service
from dhis2_core.plugins.maintenance.service import SoftDeleteTarget
from dhis2_core.profile import Profile, profile_from_env

app = typer.Typer(
    help="DHIS2 maintenance — tasks, cache, cleanup, data-integrity, resource-table refreshes.",
    no_args_is_help=True,
)

task_app = typer.Typer(help="Background-task polling (all long-running DHIS2 ops).", no_args_is_help=True)
cleanup_app = typer.Typer(help="Hard-remove soft-deleted rows (unblocks metadata deletion).", no_args_is_help=True)
dataintegrity_app = typer.Typer(help="DHIS2 data-integrity checks.", no_args_is_help=True)
refresh_app = typer.Typer(
    help="Regenerate analytics / resource / monitoring backing tables.",
    no_args_is_help=True,
)

app.add_typer(task_app, name="task")
app.add_typer(cleanup_app, name="cleanup")
app.add_typer(dataintegrity_app, name="dataintegrity")
app.add_typer(refresh_app, name="refresh")

_console = Console()


def _colorize_level(level: str | None) -> str:
    """Color-code a notification level (INFO dim, WARN yellow, ERROR red)."""
    if not level:
        return "-"
    upper = level.upper()
    if upper in ("ERROR", "SEVERE", "FATAL"):
        return f"[red]{level}[/red]"
    if upper in ("WARN", "WARNING"):
        return f"[yellow]{level}[/yellow]"
    if upper == "INFO":
        return f"[dim]{level}[/dim]"
    return level


def _colorize_severity(severity: str | None) -> str:
    """Color-code a data-integrity check's severity."""
    if not severity:
        return "-"
    upper = severity.upper()
    if upper in ("CRITICAL", "SEVERE"):
        return f"[red]{severity}[/red]"
    if upper == "WARNING":
        return f"[yellow]{severity}[/yellow]"
    if upper == "INFO":
        return f"[dim]{severity}[/dim]"
    return severity


@task_app.command("types")
def task_types_command() -> None:
    """List every background-job type DHIS2 tracks (ANALYTICS_TABLE, DATA_INTEGRITY, ...)."""
    names = asyncio.run(service.list_task_types(profile_from_env()))
    if not names:
        typer.echo("no task types reported by this instance")
        return
    table = Table(title=f"DHIS2 task types ({len(names)})")
    table.add_column("task type", style="cyan", no_wrap=True)
    for name in names:
        table.add_row(name)
    _console.print(table)


@task_app.command("list")
@task_app.command("ls", hidden=True)
def task_list_command(
    task_type: Annotated[str, typer.Argument(help="Task type, e.g. ANALYTICS_TABLE.")],
) -> None:
    """List every task UID recorded for a given job type."""
    uids = asyncio.run(service.list_task_ids(profile_from_env(), task_type))
    if not uids:
        typer.echo(f"no {task_type} tasks recorded on this instance")
        return
    table = Table(title=f"{task_type} tasks ({len(uids)})")
    table.add_column("task UID", style="cyan", no_wrap=True)
    for uid in uids:
        table.add_row(uid)
    _console.print(table)


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
            _colorize_level(notification.level),
            "[green]done[/green]" if notification.completed else "",
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
        table.add_row(
            check.name,
            check.section or "-",
            _colorize_severity(check.severity),
            check.issuesIdType or "-",
        )
    _console.print(table)


@dataintegrity_app.command("run")
def dataintegrity_run_command(
    check: Annotated[list[str] | None, typer.Argument(help="Check name(s); omit to run every check.")] = None,
    details: Annotated[
        bool, typer.Option("--details", help="Hit /details (populates issues[]) instead of /summary.")
    ] = False,
    slow: Annotated[
        bool,
        typer.Option(
            "--slow",
            help=(
                "Include the ~19 `isSlow` checks DHIS2 skips by default. Resolves the full "
                "check list via /api/dataIntegrity and passes every name explicitly — DHIS2 "
                "only runs a slow check when it's named in the `checks` filter."
            ),
        ),
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
    as_json: Annotated[bool, typer.Option("--json", help="Emit the raw WebMessageResponse envelope.")] = False,
) -> None:
    """Kick off a data-integrity run; with --watch, stream progress to completion."""
    from dhis2_core.cli_output import render_webmessage
    from dhis2_core.cli_task_watch import stream_task_to_stdout

    profile = profile_from_env()
    checks_to_run: list[str] | None = list(check) if check else None
    if slow and not checks_to_run:
        # Resolve every check name and pass them all — DHIS2 only runs `isSlow` checks
        # when they're named explicitly. With no name filter + slow=True we'd have no
        # effect, so we expand here.
        all_checks = asyncio.run(service.list_dataintegrity_checks(profile))
        checks_to_run = [c.name for c in all_checks if c.name]
        slow_count = sum(1 for c in all_checks if getattr(c, "isSlow", False))
        typer.secho(
            f"running all {len(checks_to_run)} checks (includes {slow_count} isSlow checks)",
            err=True,
            fg=typer.colors.YELLOW,
        )
    response = asyncio.run(service.run_dataintegrity(profile, checks=checks_to_run, details=details))
    # Heads-up about isSlow checks when the user didn't opt in + didn't name specific checks.
    if not slow and not checks_to_run:
        typer.secho(
            "note: ~19 isSlow checks skipped by default; re-run with --slow to include them.",
            err=True,
            fg=typer.colors.CYAN,
        )
    if not watch:
        render_webmessage(response, as_json=as_json)
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

    if details:
        # Details mode: include the issues (id + name) per check — that's the
        # whole point of running --details; hiding them would defeat the flag.
        table = Table(title=f"data-integrity results — details ({len(report.results)})")
        for column in ("name", "severity", "count", "issues (id · name)"):
            table.add_column(column, overflow="fold")
        for name, result in report.results.items():
            issues = result.issues or []
            # Cap to keep the table readable on wide checks.
            capped = issues[:20]
            issue_lines = [f"{item.id} · {item.name or '-'}" for item in capped]
            if len(issues) > len(capped):
                issue_lines.append(f"… ({len(issues) - len(capped)} more)")
            count = result.count if result.count is not None else len(issues)
            table.add_row(
                name,
                _colorize_severity(result.severity),
                f"[red]{count}[/red]" if count > 0 else "[green]0[/green]",
                "\n".join(issue_lines) if issue_lines else "-",
            )
        _console.print(table)
        return

    table = Table(title=f"data-integrity results ({len(report.results)})")
    for column in ("name", "severity", "count", "finishedTime"):
        table.add_column(column, overflow="fold")
    for name, result in report.results.items():
        count = result.count or 0
        table.add_row(
            name,
            _colorize_severity(result.severity),
            f"[red]{count}[/red]" if count > 0 else "[green]0[/green]",
            result.finishedTime or "-",
        )
    _console.print(table)
    # Hint when summary reports issues but no details were requested.
    non_zero = any((r.count or 0) > 0 for r in report.results.values())
    if non_zero:
        typer.secho(
            "\nhint: add --details to see the offending UIDs (requires a prior "
            "`dhis2 maintenance dataintegrity run --details`).",
            fg=typer.colors.YELLOW,
        )


@refresh_app.command("analytics")
def refresh_analytics_command(
    last_years: Annotated[int | None, typer.Option("--last-years")] = None,
    skip_resource_tables: Annotated[bool, typer.Option("--skip-resource-tables")] = False,
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
    as_json: Annotated[bool, typer.Option("--json", help="Emit the raw WebMessageResponse envelope.")] = False,
) -> None:
    """Regenerate the full analytics star schema (`/api/resourceTables/analytics`, job=`ANALYTICS_TABLE`).

    Primary workflow after pushing new data values: DHIS2's analytics queries
    read from these tables, so they must be rebuilt for fresh data to show up.
    Also refreshes resource tables unless `--skip-resource-tables` is set.
    """
    _kick_off_and_maybe_watch(
        lambda profile: service.refresh_analytics(
            profile, skip_resource_tables=skip_resource_tables, last_years=last_years
        ),
        watch=watch,
        interval=interval,
        timeout=timeout,
        as_json=as_json,
    )


@refresh_app.command("resource-tables")
def refresh_resource_tables_command(
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
    as_json: Annotated[bool, typer.Option("--json", help="Emit the raw WebMessageResponse envelope.")] = False,
) -> None:
    """Regenerate resource tables only (`/api/resourceTables`, job=`RESOURCE_TABLE`).

    Rebuilds the supporting OU / category hierarchy tables without touching
    the analytics star schema. Use when OU / category metadata changed but
    no new data values landed — faster than a full `refresh analytics` run.
    """
    _kick_off_and_maybe_watch(
        service.refresh_resource_tables,
        watch=watch,
        interval=interval,
        timeout=timeout,
        as_json=as_json,
    )


@refresh_app.command("monitoring")
def refresh_monitoring_command(
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
    as_json: Annotated[bool, typer.Option("--json", help="Emit the raw WebMessageResponse envelope.")] = False,
) -> None:
    """Regenerate monitoring tables (`/api/resourceTables/monitoring`, job=`MONITORING`).

    Rebuilds the tables backing DHIS2's data-quality / validation-rule
    monitoring. Independent of the analytics + resource tables.
    """
    _kick_off_and_maybe_watch(
        service.refresh_monitoring,
        watch=watch,
        interval=interval,
        timeout=timeout,
        as_json=as_json,
    )


def _kick_off_and_maybe_watch(
    kickoff: Callable[[Profile], Coroutine[Any, Any, WebMessageResponse]],
    *,
    watch: bool,
    interval: float,
    timeout: float | None,
    as_json: bool,
) -> None:
    """POST the kickoff + render the envelope; stream progress to completion when `watch`.

    Reused by all three refresh commands — the kickoff closure picks which
    service function + params to call.
    """
    from dhis2_core.cli_output import render_webmessage
    from dhis2_core.cli_task_watch import stream_task_to_stdout

    profile = profile_from_env()
    response = asyncio.run(kickoff(profile))
    if not watch:
        render_webmessage(response, as_json=as_json)
        return
    ref = response.task_ref()
    if ref is None:
        typer.secho("error: response has no jobType/id — nothing to watch", err=True, fg=typer.colors.RED)
        raise typer.Exit(1)
    job_type, task_uid = ref
    asyncio.run(stream_task_to_stdout(profile, job_type, task_uid, interval=interval, timeout=timeout))


def register(root_app: Any) -> None:
    """Mount under `dhis2 maintenance`."""
    root_app.add_typer(app, name="maintenance", help="DHIS2 maintenance (tasks, cache, integrity, cleanup, refresh).")
