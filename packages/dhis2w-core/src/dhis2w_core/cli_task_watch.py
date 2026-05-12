"""Shared CLI helper — render a DHIS2 background-task's notifications with Rich.

Used by every `--watch` flag across plugins (analytics refresh, maintenance
dataintegrity run, future async ops). Pointed at one `(job_type, task_uid)`,
reads the `/api/system/tasks/{type}/{uid}` feed via
`maintenance.service.watch_task` and renders each notification as a coloured
line (by level) above an animated spinner showing total elapsed time.
Writes to stderr so stdout stays usable for piping the job-kickoff JSON.
Exits on the first `completed=true` row; raises `TimeoutError` if `timeout`
elapses first.
"""

from __future__ import annotations

from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from dhis2w_core.profile import Profile
from dhis2w_core.rich_console import STDERR_CONSOLE
from dhis2w_core.v42.plugins.maintenance import service as maintenance_service

_LEVEL_STYLE: dict[str, str] = {
    "INFO": "cyan",
    "WARN": "yellow",
    "WARNING": "yellow",
    "ERROR": "red bold",
    "LOOP": "magenta",
    "DEBUG": "dim",
}


async def stream_task_to_stdout(
    profile: Profile,
    job_type: str,
    task_uid: str,
    *,
    interval: float = 2.0,
    timeout: float | None = 600.0,
) -> None:
    """Poll `/api/system/tasks/{job_type}/{task_uid}` and render with Rich."""
    STDERR_CONSOLE.print(f"[bold cyan]watching[/] [bold]{job_type}/{task_uid}[/]  [dim]interval={interval}s[/]")
    final_message: str | None = None
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeElapsedColumn(),
        console=STDERR_CONSOLE,
        transient=True,
    ) as progress:
        task_row = progress.add_task("polling...", total=None)
        async for notification in maintenance_service.watch_task(
            profile, job_type, task_uid, interval=interval, timeout=timeout
        ):
            level = (notification.level or "INFO").upper()
            style = _LEVEL_STYLE.get(level, "white")
            marker = "[x]" if notification.completed else "[ ]"
            message = notification.message or "-"
            progress.console.print(f"  {level:<5} {marker} {message}", style=style, markup=False)
            progress.update(task_row, description=message)
            if notification.completed:
                final_message = message
                break
    summary = final_message or "task completed"
    STDERR_CONSOLE.print(f"[bold green]done[/]  [dim]{job_type}/{task_uid}[/]  {summary}")
