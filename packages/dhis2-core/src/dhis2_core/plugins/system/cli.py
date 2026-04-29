"""Typer sub-app for the `system` plugin (mounted under `dhis2 system`)."""

from __future__ import annotations

import asyncio
from typing import Annotated, Any

import typer
from dhis2_client import DhisCalendar

from dhis2_core.cli_output import DetailRow, is_json_output, render_detail
from dhis2_core.plugins.system import service
from dhis2_core.profile import profile_from_env

app = typer.Typer(help="DHIS2 system info and current-user access.", no_args_is_help=True)


@app.command("whoami")
def whoami_command() -> None:
    """Print the authenticated DHIS2 user for the current environment profile."""
    me = asyncio.run(service.whoami(profile_from_env()))
    typer.echo(f"{me.username} ({me.displayName or '-'})")


@app.command("info")
def info_command() -> None:
    """Print DHIS2 system info (version, build, analytics state, env)."""
    info = asyncio.run(service.system_info(profile_from_env()))
    if is_json_output():
        typer.echo(info.model_dump_json(indent=2, exclude_none=True, by_alias=True))
        return
    rows = [
        DetailRow("version", str(info.version or "-")),
        DetailRow("revision", str(info.revision or "-")),
        DetailRow("systemName", str(info.systemName or "-")),
        DetailRow("systemId", str(info.systemId or "-")),
        DetailRow("serverDate", str(info.serverDate or "-")),
        DetailRow("buildTime", str(info.buildTime or "-")),
        DetailRow("calendar", str(info.calendar or "-")),
        DetailRow("dateFormat", str(info.dateFormat or "-")),
        DetailRow("instanceBaseUrl", str(getattr(info, "instanceBaseUrl", None) or "-")),
        DetailRow("contextPath", str(info.contextPath or "-")),
        DetailRow("environment", str(getattr(info, "environmentVariable", None) or "-")),
        DetailRow("lastAnalyticsSuccess", str(getattr(info, "lastAnalyticsTableSuccess", None) or "-")),
        DetailRow("lastAnalyticsRuntime", str(getattr(info, "lastAnalyticsTableRuntime", None) or "-")),
        DetailRow("javaVersion", str(getattr(info, "javaVersion", None) or "-")),
        DetailRow("cpuCores", str(getattr(info, "cpuCores", None) or "-")),
    ]
    render_detail(f"system info — {info.systemName or info.systemId or '?'}", rows)


@app.command("calendar")
def calendar_command(
    value: Annotated[
        DhisCalendar | None,
        typer.Argument(
            help="When supplied, write `keyCalendar` (one of: coptic, ethiopian, "
            "gregorian, islamic, iso8601, julian, nepali, persian, thai). "
            "Omit to print the current calendar.",
        ),
    ] = None,
) -> None:
    """Print the active DHIS2 calendar, or change it when a value is supplied.

    `keyCalendar` is the system-wide calendar DHIS2 uses to interpret periods.
    The default is `iso8601`. Changing it is rare — most instances pick a
    calendar at deploy time and never touch it again.
    """
    profile = profile_from_env()
    if value is None:
        current = asyncio.run(service.get_calendar(profile))
        typer.echo(current)
        return
    asyncio.run(service.set_calendar(profile, value))
    typer.echo(f"keyCalendar set to {value.value}")


def register(root_app: Any) -> None:
    """Mount this plugin's Typer sub-app under `dhis2 system`."""
    root_app.add_typer(app, name="system", help="DHIS2 system info.")
