"""Shared CLI output helpers — concise human summaries for WebMessageResponse.

Every write/kickoff command shares the same two rendering modes:
  - default: one-line human-readable summary (stdout)
  - `--json`: raw `model_dump_json(indent=2, exclude_none=True)` for scripting

`render_webmessage` picks the right summary based on the envelope's inner
`responseType` so callers don't branch: `ImportSummary` → import counts,
`ObjectReportWebMessageResponse` → `kind verb uid`,
`JobConfigurationWebMessageResponse` → `kicked off type (task=uid)`.
"""

from __future__ import annotations

import typer
from dhis2_client import WebMessageResponse


def render_webmessage(
    envelope: WebMessageResponse,
    *,
    as_json: bool,
    action: str = "",
) -> None:
    """Print one line describing `envelope`, or the full JSON when `as_json`.

    `action` labels the user intent (`created`, `updated`, `deleted`, `set`,
    `pushed`). For kickoff envelopes (job configs) the action is ignored —
    the summary names the job type. For import-summary envelopes the action
    prefixes the import-count line (`pushed: imported=1 updated=0 ...`).
    """
    if as_json:
        typer.echo(envelope.model_dump_json(indent=2, exclude_none=True))
        return

    ref = envelope.task_ref()
    if ref is not None:
        job_type, task_uid = ref
        typer.echo(f"kicked off {job_type} (task={task_uid})")
        typer.echo(f"  poll:  dhis2 maintenance task watch {job_type} {task_uid}")
        typer.echo("  or re-run with --watch / -w to stream progress")
        return

    counts = envelope.import_count()
    if counts is not None and any((counts.imported, counts.updated, counts.ignored, counts.deleted)):
        prefix = f"{action}: " if action else ""
        typer.echo(
            f"{prefix}imported={counts.imported} updated={counts.updated} "
            f"ignored={counts.ignored} deleted={counts.deleted}"
        )
        return

    uid = envelope.created_uid
    if uid:
        verb = action or "ok"
        typer.echo(f"{verb} {uid}")
        return

    message = envelope.message or envelope.httpStatus or "ok"
    typer.echo(f"{action or 'ok'}: {message}" if action else message)
