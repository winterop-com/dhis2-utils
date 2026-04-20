"""Typer sub-app for the `doctor` plugin — mounted as `dhis2 doctor`."""

from __future__ import annotations

import asyncio
from typing import Annotated, Any

import typer
from rich.console import Console
from rich.table import Table

from dhis2_core.plugins.doctor import service
from dhis2_core.profile import profile_from_env

app = typer.Typer(
    help="Probe a DHIS2 instance for known upstream gotchas + workspace requirements.",
    no_args_is_help=False,
    invoke_without_command=True,
)
_console = Console()


_STATUS_STYLES: dict[str, str] = {
    "pass": "green",
    "warn": "yellow",
    "fail": "red",
    "skip": "dim",
}
# Rich interprets `[x]` as a style tag; wrap in a leading/trailing space + use filled-out words
# to avoid triggering the markup parser while still reading clean.
_STATUS_MARKS: dict[str, str] = {
    "pass": "PASS",
    "warn": "WARN",
    "fail": "FAIL",
    "skip": "SKIP",
}


@app.callback(invoke_without_command=True)
def run_command(
    ctx: typer.Context,
    as_json: Annotated[bool, typer.Option("--json", help="Emit the report as JSON instead of a table.")] = False,
) -> None:
    """Run every probe against the resolved profile's instance."""
    if ctx.invoked_subcommand is not None:
        return
    report = asyncio.run(service.run_doctor(profile_from_env()))
    if as_json:
        typer.echo(report.model_dump_json(indent=2, exclude_none=True))
        raise typer.Exit(code=1 if report.fail_count else 0)

    table = Table(title=f"dhis2 doctor — {report.base_url} (DHIS2 {report.dhis2_version or '?'})")
    table.add_column("probe", overflow="fold")
    table.add_column("status", justify="center", no_wrap=True)
    table.add_column("message", overflow="fold")
    table.add_column("bugs", no_wrap=True, style="dim")
    for probe in report.probes:
        mark = _STATUS_MARKS.get(probe.status, probe.status)
        style = _STATUS_STYLES.get(probe.status, "white")
        table.add_row(probe.name, f"[{style}]{mark}[/{style}]", probe.message, probe.bugs_ref or "")
    _console.print(table)

    summary = (
        f"[green]{report.pass_count} pass[/green] / "
        f"[yellow]{report.warn_count} warn[/yellow] / "
        f"[red]{report.fail_count} fail[/red] / "
        f"[dim]{report.skip_count} skip[/dim] "
        f"({len(report.probes)} probes)"
    )
    _console.print(summary)
    if report.fail_count:
        raise typer.Exit(code=1)


def register(root_app: Any) -> None:
    """Mount under `dhis2 doctor`."""
    root_app.add_typer(app, name="doctor", help="Probe a DHIS2 instance for known gotchas + requirements.")
