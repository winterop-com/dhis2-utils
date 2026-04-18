"""Typer sub-app for the `tracker` plugin (mounted under `dhis2 tracker`)."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Annotated, Any

import typer

from dhis2_core.plugins.tracker import service
from dhis2_core.profile import profile_from_env

app = typer.Typer(
    help="DHIS2 tracker API — tracked entities, enrollments, events, relationships.", no_args_is_help=True
)


def _print(payload: Any) -> None:
    typer.echo(json.dumps(payload, indent=2))


@app.command("list-tracked-entities")
def list_tracked_entities_command(
    program: Annotated[str | None, typer.Option("--program")] = None,
    tracked_entity_type: Annotated[str | None, typer.Option("--tet")] = None,
    org_unit: Annotated[str | None, typer.Option("--org-unit")] = None,
    ou_mode: Annotated[str, typer.Option("--ou-mode")] = "DESCENDANTS",
    fields: Annotated[str | None, typer.Option("--fields")] = None,
    filter: Annotated[str | None, typer.Option("--filter")] = None,
    page_size: Annotated[int, typer.Option("--page-size")] = 50,
) -> None:
    """List tracked entities (requires a tracker program)."""
    _print(
        asyncio.run(
            service.list_tracked_entities(
                profile_from_env(),
                program=program,
                tracked_entity_type=tracked_entity_type,
                org_unit=org_unit,
                ou_mode=ou_mode,
                fields=fields,
                filter=filter,
                page_size=page_size,
            )
        )
    )


@app.command("get-tracked-entity")
def get_tracked_entity_command(
    uid: Annotated[str, typer.Argument()],
    program: Annotated[str | None, typer.Option("--program")] = None,
    fields: Annotated[str | None, typer.Option("--fields")] = None,
) -> None:
    """Fetch one tracked entity by UID."""
    _print(asyncio.run(service.get_tracked_entity(profile_from_env(), uid, program=program, fields=fields)))


@app.command("list-enrollments")
def list_enrollments_command(
    program: Annotated[str | None, typer.Option("--program")] = None,
    org_unit: Annotated[str | None, typer.Option("--org-unit")] = None,
    ou_mode: Annotated[str, typer.Option("--ou-mode")] = "DESCENDANTS",
    tracked_entity: Annotated[str | None, typer.Option("--te")] = None,
    status: Annotated[str | None, typer.Option("--status", help="ACTIVE | COMPLETED | CANCELLED")] = None,
    fields: Annotated[str | None, typer.Option("--fields")] = None,
    page_size: Annotated[int, typer.Option("--page-size")] = 50,
) -> None:
    """List enrollments (tracker programs only)."""
    _print(
        asyncio.run(
            service.list_enrollments(
                profile_from_env(),
                program=program,
                org_unit=org_unit,
                ou_mode=ou_mode,
                tracked_entity=tracked_entity,
                status=status,
                fields=fields,
                page_size=page_size,
            )
        )
    )


@app.command("list-events")
def list_events_command(
    program: Annotated[str | None, typer.Option("--program")] = None,
    program_stage: Annotated[str | None, typer.Option("--program-stage")] = None,
    org_unit: Annotated[str | None, typer.Option("--org-unit")] = None,
    ou_mode: Annotated[str, typer.Option("--ou-mode")] = "DESCENDANTS",
    tracked_entity: Annotated[str | None, typer.Option("--te")] = None,
    enrollment: Annotated[str | None, typer.Option("--enrollment")] = None,
    status: Annotated[str | None, typer.Option("--status")] = None,
    occurred_after: Annotated[str | None, typer.Option("--after")] = None,
    occurred_before: Annotated[str | None, typer.Option("--before")] = None,
    fields: Annotated[str | None, typer.Option("--fields")] = None,
    page_size: Annotated[int, typer.Option("--page-size")] = 50,
) -> None:
    """List events (works with both event and tracker programs)."""
    _print(
        asyncio.run(
            service.list_events(
                profile_from_env(),
                program=program,
                program_stage=program_stage,
                org_unit=org_unit,
                ou_mode=ou_mode,
                tracked_entity=tracked_entity,
                enrollment=enrollment,
                status=status,
                occurred_after=occurred_after,
                occurred_before=occurred_before,
                fields=fields,
                page_size=page_size,
            )
        )
    )


@app.command("list-relationships")
def list_relationships_command(
    tracked_entity: Annotated[str | None, typer.Option("--te")] = None,
    enrollment: Annotated[str | None, typer.Option("--enrollment")] = None,
    event: Annotated[str | None, typer.Option("--event")] = None,
    fields: Annotated[str | None, typer.Option("--fields")] = None,
    page_size: Annotated[int, typer.Option("--page-size")] = 50,
) -> None:
    """List relationships (one of --te/--enrollment/--event required)."""
    _print(
        asyncio.run(
            service.list_relationships(
                profile_from_env(),
                tracked_entity=tracked_entity,
                enrollment=enrollment,
                event=event,
                fields=fields,
                page_size=page_size,
            )
        )
    )


@app.command("push")
def push_command(
    file: Annotated[Path, typer.Argument(help="JSON file containing the tracker bundle.")],
    import_strategy: Annotated[
        str | None, typer.Option("--strategy", help="CREATE | UPDATE | CREATE_AND_UPDATE | DELETE")
    ] = None,
    atomic_mode: Annotated[str | None, typer.Option("--atomic", help="ALL | OBJECT")] = None,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
    async_mode: Annotated[bool, typer.Option("--async")] = False,
) -> None:
    """Bulk import via POST /api/tracker."""
    bundle = json.loads(file.read_text(encoding="utf-8"))
    _print(
        asyncio.run(
            service.push_tracker(
                profile_from_env(),
                bundle,
                import_strategy=import_strategy,
                atomic_mode=atomic_mode,
                dry_run=dry_run,
                async_mode=async_mode,
            )
        )
    )


def register(root_app: Any) -> None:
    """Mount under `dhis2 tracker`."""
    root_app.add_typer(app, name="tracker", help="DHIS2 tracker.")
