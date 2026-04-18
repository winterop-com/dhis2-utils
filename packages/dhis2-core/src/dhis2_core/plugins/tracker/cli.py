"""Typer sub-app for the tracker domain (mounted under `dhis2 data tracker`)."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Annotated, Any

import typer

from dhis2_core.plugins.tracker import service
from dhis2_core.profile import profile_from_env

app = typer.Typer(
    help="DHIS2 tracker — tracked entities, enrollments, events, relationships.",
    no_args_is_help=True,
)
entity_app = typer.Typer(help="Tracked entities.", no_args_is_help=True)
enrollment_app = typer.Typer(help="Enrollments.", no_args_is_help=True)
event_app = typer.Typer(help="Events.", no_args_is_help=True)
relationship_app = typer.Typer(help="Relationships.", no_args_is_help=True)
app.add_typer(entity_app, name="entity")
app.add_typer(enrollment_app, name="enrollment")
app.add_typer(event_app, name="event")
app.add_typer(relationship_app, name="relationship")


def _print(payload: Any) -> None:
    """Pretty-print pydantic models or raw dicts/lists as JSON."""
    from pydantic import BaseModel

    if isinstance(payload, BaseModel):
        typer.echo(payload.model_dump_json(indent=2, exclude_none=True))
    elif isinstance(payload, list) and payload and isinstance(payload[0], BaseModel):
        items = [m.model_dump(exclude_none=True, mode="json") for m in payload]
        typer.echo(json.dumps(items, indent=2, default=str))
    else:
        typer.echo(json.dumps(payload, indent=2, default=str))


@entity_app.command("list")
@entity_app.command("ls", hidden=True)
def entity_list_command(
    program: Annotated[str | None, typer.Option("--program")] = None,
    tracked_entity_type: Annotated[str | None, typer.Option("--tet")] = None,
    tracked_entities: Annotated[
        str | None, typer.Option("--te-uids", help="Comma-separated tracked-entity UIDs to fetch directly.")
    ] = None,
    org_unit: Annotated[str | None, typer.Option("--org-unit")] = None,
    ou_mode: Annotated[str, typer.Option("--ou-mode")] = "DESCENDANTS",
    fields: Annotated[str | None, typer.Option("--fields")] = None,
    filter: Annotated[str | None, typer.Option("--filter")] = None,
    page_size: Annotated[int, typer.Option("--page-size")] = 50,
    page: Annotated[int | None, typer.Option("--page", help="1-based page number.")] = None,
    updated_after: Annotated[
        str | None, typer.Option("--updated-after", help="ISO-8601 cutoff — only TEs updated after this.")
    ] = None,
) -> None:
    """List tracked entities (requires a tracker program)."""
    _print(
        asyncio.run(
            service.list_tracked_entities(
                profile_from_env(),
                program=program,
                tracked_entity_type=tracked_entity_type,
                tracked_entities=tracked_entities,
                org_unit=org_unit,
                ou_mode=ou_mode,
                fields=fields,
                filter=filter,
                page_size=page_size,
                page=page,
                updated_after=updated_after,
            )
        )
    )


@entity_app.command("get")
def entity_get_command(
    uid: Annotated[str, typer.Argument()],
    program: Annotated[str | None, typer.Option("--program")] = None,
    fields: Annotated[str | None, typer.Option("--fields")] = None,
) -> None:
    """Fetch one tracked entity by UID."""
    _print(asyncio.run(service.get_tracked_entity(profile_from_env(), uid, program=program, fields=fields)))


@enrollment_app.command("list")
@enrollment_app.command("ls", hidden=True)
def enrollment_list_command(
    program: Annotated[str | None, typer.Option("--program")] = None,
    org_unit: Annotated[str | None, typer.Option("--org-unit")] = None,
    ou_mode: Annotated[str, typer.Option("--ou-mode")] = "DESCENDANTS",
    tracked_entity: Annotated[str | None, typer.Option("--te")] = None,
    status: Annotated[str | None, typer.Option("--status", help="ACTIVE | COMPLETED | CANCELLED")] = None,
    fields: Annotated[str | None, typer.Option("--fields")] = None,
    page_size: Annotated[int, typer.Option("--page-size")] = 50,
    page: Annotated[int | None, typer.Option("--page")] = None,
    updated_after: Annotated[str | None, typer.Option("--updated-after")] = None,
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
                page=page,
                updated_after=updated_after,
            )
        )
    )


@event_app.command("list")
@event_app.command("ls", hidden=True)
def event_list_command(
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
    page: Annotated[int | None, typer.Option("--page")] = None,
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
                page=page,
            )
        )
    )


@relationship_app.command("list")
@relationship_app.command("ls", hidden=True)
def relationship_list_command(
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
    response = asyncio.run(
        service.push_tracker(
            profile_from_env(),
            bundle,
            import_strategy=import_strategy,
            atomic_mode=atomic_mode,
            dry_run=dry_run,
            async_mode=async_mode,
        )
    )
    typer.echo(response.model_dump_json(indent=2, exclude_none=True))
