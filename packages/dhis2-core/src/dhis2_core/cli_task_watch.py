"""Shared CLI helper — stream a DHIS2 background-task's notifications to stdout.

Used by every `--watch` flag across plugins (analytics refresh, maintenance
dataintegrity run, future async ops). Pointed at one `(job_type, task_uid)`,
reads the `/api/system/tasks/{type}/{uid}` feed via
`maintenance.service.watch_task` and prints each notification on a single
line as it arrives. Exits on the first `completed=true` row; raises
`TimeoutError` if `timeout` elapses first.
"""

from __future__ import annotations

import typer

from dhis2_core.plugins.maintenance import service as maintenance_service
from dhis2_core.profile import Profile


async def stream_task_to_stdout(
    profile: Profile,
    job_type: str,
    task_uid: str,
    *,
    interval: float = 2.0,
    timeout: float | None = 600.0,
) -> None:
    """Poll `/api/system/tasks/{job_type}/{task_uid}` and print each notification."""
    typer.echo(f"watching {job_type}/{task_uid} (interval={interval}s, timeout={timeout}s)")
    async for notification in maintenance_service.watch_task(
        profile, job_type, task_uid, interval=interval, timeout=timeout
    ):
        marker = "[x]" if notification.completed else "[ ]"
        level = notification.level or "-"
        time = notification.time or "?"
        message = notification.message or "-"
        typer.echo(f"{time:<24}  {level:<5} {marker} {message}")
