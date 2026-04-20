"""Typer sub-app for the `analytics` plugin (mounted under `dhis2 analytics`)."""

from __future__ import annotations

import asyncio
import json
from typing import Annotated, Any

import typer

from dhis2_core.plugins.analytics import service
from dhis2_core.profile import profile_from_env

app = typer.Typer(help="DHIS2 analytics — aggregated queries over the analytics tables.", no_args_is_help=True)


def _print(payload: Any) -> None:
    typer.echo(json.dumps(payload, indent=2))


@app.command("query")
def query_command(
    dimension: Annotated[
        list[str],
        typer.Option(
            "--dimension", "--dim", help="Dimension string (repeatable), e.g. dx:UID, pe:LAST_12_MONTHS, ou:UID."
        ),
    ],
    shape: Annotated[
        str,
        typer.Option(
            "--shape",
            help="Response shape: `table` (default, aggregated), `raw` (/api/analytics/rawData), "
            "`dvs` (/api/analytics/dataValueSet — DataValueSet shape).",
        ),
    ] = "table",
    filter: Annotated[
        list[str] | None,
        typer.Option("--filter", help="Filter string (repeatable), same syntax as --dimension."),
    ] = None,
    aggregation_type: Annotated[
        str | None,
        typer.Option("--agg", help="SUM | AVERAGE | COUNT | MIN | MAX | AVERAGE_SUM_ORG_UNIT ..."),
    ] = None,
    output_id_scheme: Annotated[
        str | None,
        typer.Option("--output-id-scheme", help="UID | NAME | CODE | ID — how UIDs appear in the response"),
    ] = None,
    include_num_den: Annotated[
        bool, typer.Option("--num-den/--no-num-den", help="Include indicator numerator/denominator columns.")
    ] = False,
    display_property: Annotated[
        str | None, typer.Option("--display-property", help="NAME | SHORTNAME — which label to render metadata with.")
    ] = None,
    start_date: Annotated[str | None, typer.Option("--start-date")] = None,
    end_date: Annotated[str | None, typer.Option("--end-date")] = None,
    skip_meta: Annotated[bool, typer.Option("--skip-meta")] = False,
) -> None:
    """Run an analytics query. Use `--shape` to pick `table`, `raw`, or `dvs`."""
    try:
        response = asyncio.run(
            service.query_analytics(
                profile_from_env(),
                shape=shape,
                dimensions=dimension,
                filters=filter,
                aggregation_type=aggregation_type,
                output_id_scheme=output_id_scheme,
                include_num_den=include_num_den if include_num_den else None,
                display_property=display_property,
                start_date=start_date,
                end_date=end_date,
                skip_meta=skip_meta,
            )
        )
    except ValueError as exc:
        typer.secho(f"error: {exc}", err=True, fg=typer.colors.RED)
        raise typer.Exit(1) from exc
    typer.echo(response.model_dump_json(indent=2, exclude_none=True))


events_app = typer.Typer(help="Event analytics — line-lists events or aggregates them.", no_args_is_help=True)
enrollments_app = typer.Typer(help="Enrollment analytics — line-lists enrollments.", no_args_is_help=True)
app.add_typer(events_app, name="events")
app.add_typer(enrollments_app, name="enrollments")


@events_app.command("query")
def events_query_command(
    program: Annotated[str, typer.Argument(help="Program UID.")],
    mode: Annotated[
        str,
        typer.Option("--mode", help="`query` (line-listed events) or `aggregate` (grouped counts)."),
    ] = "query",
    dimension: Annotated[
        list[str] | None,
        typer.Option("--dimension", "--dim", help="Dimension string (repeatable), e.g. pe:LAST_12_MONTHS, ou:UID."),
    ] = None,
    filter: Annotated[
        list[str] | None,
        typer.Option("--filter", help="Filter string (repeatable), same syntax as --dimension."),
    ] = None,
    stage: Annotated[str | None, typer.Option("--stage", help="Program stage UID to narrow events.")] = None,
    output_type: Annotated[
        str | None,
        typer.Option("--output-type", help="EVENT | ENROLLMENT | TRACKED_ENTITY_INSTANCE (row shape)."),
    ] = None,
    start_date: Annotated[str | None, typer.Option("--start-date")] = None,
    end_date: Annotated[str | None, typer.Option("--end-date")] = None,
    skip_meta: Annotated[bool, typer.Option("--skip-meta")] = False,
    page: Annotated[int | None, typer.Option("--page")] = None,
    page_size: Annotated[int | None, typer.Option("--page-size")] = None,
) -> None:
    """Run an event analytics query (`/api/analytics/events/{mode}/{program}`)."""
    try:
        response = asyncio.run(
            service.query_events(
                profile_from_env(),
                program=program,
                mode=mode,
                dimensions=dimension,
                filters=filter,
                stage=stage,
                output_type=output_type,
                start_date=start_date,
                end_date=end_date,
                skip_meta=skip_meta,
                page=page,
                page_size=page_size,
            )
        )
    except ValueError as exc:
        typer.secho(f"error: {exc}", err=True, fg=typer.colors.RED)
        raise typer.Exit(1) from exc
    typer.echo(response.model_dump_json(indent=2, exclude_none=True))


@enrollments_app.command("query")
def enrollments_query_command(
    program: Annotated[str, typer.Argument(help="Program UID.")],
    dimension: Annotated[
        list[str] | None,
        typer.Option("--dimension", "--dim", help="Dimension string (repeatable)."),
    ] = None,
    filter: Annotated[
        list[str] | None,
        typer.Option("--filter", help="Filter string (repeatable)."),
    ] = None,
    start_date: Annotated[str | None, typer.Option("--start-date")] = None,
    end_date: Annotated[str | None, typer.Option("--end-date")] = None,
    skip_meta: Annotated[bool, typer.Option("--skip-meta")] = False,
    page: Annotated[int | None, typer.Option("--page")] = None,
    page_size: Annotated[int | None, typer.Option("--page-size")] = None,
) -> None:
    """Run an enrollment analytics query (`/api/analytics/enrollments/query/{program}`)."""
    response = asyncio.run(
        service.query_enrollments(
            profile_from_env(),
            program=program,
            dimensions=dimension,
            filters=filter,
            start_date=start_date,
            end_date=end_date,
            skip_meta=skip_meta,
            page=page,
            page_size=page_size,
        )
    )
    typer.echo(response.model_dump_json(indent=2, exclude_none=True))


@app.command("outlier-detection")
def outlier_detection_command(
    data_element: Annotated[
        list[str] | None,
        typer.Option("--data-element", "--de", help="Data-element UID (repeatable)."),
    ] = None,
    data_set: Annotated[
        list[str] | None,
        typer.Option("--data-set", "--ds", help="Data-set UID (repeatable) — expanded to its dataElements."),
    ] = None,
    org_unit: Annotated[
        list[str] | None,
        typer.Option("--org-unit", "--ou", help="Org-unit UID (repeatable)."),
    ] = None,
    period: Annotated[
        str | None,
        typer.Option("--period", "--pe", help="Period identifier (e.g. LAST_12_MONTHS, 202401)."),
    ] = None,
    start_date: Annotated[str | None, typer.Option("--start-date", help="ISO date YYYY-MM-DD.")] = None,
    end_date: Annotated[str | None, typer.Option("--end-date", help="ISO date YYYY-MM-DD.")] = None,
    algorithm: Annotated[
        str | None,
        typer.Option(
            "--algorithm",
            help="Z_SCORE (default) | MODIFIED_Z_SCORE | MIN_MAX. "
            "(Upstream OAS still shows MOD_Z_SCORE but the server rejects that value — see BUGS.md.)",
        ),
    ] = None,
    threshold: Annotated[
        float | None,
        typer.Option("--threshold", help="Standard-deviation cutoff (default 3.0)."),
    ] = None,
    max_results: Annotated[
        int | None,
        typer.Option("--max-results", help="Cap the number of outliers returned (default 500)."),
    ] = None,
    order_by: Annotated[
        str | None,
        typer.Option("--order-by", help="ABS_DEV | STANDARD_DEVIATION | Z_SCORE | ..."),
    ] = None,
    sort_order: Annotated[
        str | None,
        typer.Option("--sort-order", help="ASC | DESC."),
    ] = None,
) -> None:
    """Run `/api/analytics/outlierDetection` — flag statistical anomalies in data values."""
    response = asyncio.run(
        service.query_outlier_detection(
            profile_from_env(),
            data_elements=data_element,
            data_sets=data_set,
            org_units=org_unit,
            periods=period,
            start_date=start_date,
            end_date=end_date,
            algorithm=algorithm,
            threshold=threshold,
            max_results=max_results,
            order_by=order_by,
            sort_order=sort_order,
        )
    )
    typer.echo(response.model_dump_json(indent=2, exclude_none=True))


tracked_entities_app = typer.Typer(
    help="Tracked-entity analytics — line-list TEs for a given type.",
    no_args_is_help=True,
)
app.add_typer(tracked_entities_app, name="tracked-entities")


@tracked_entities_app.command("query")
def tracked_entities_query_command(
    tracked_entity_type: Annotated[str, typer.Argument(help="TrackedEntityType UID.")],
    dimension: Annotated[
        list[str] | None,
        typer.Option("--dimension", "--dim", help="Dimension string (repeatable)."),
    ] = None,
    filter: Annotated[  # noqa: A002 — Typer needs the positional name
        list[str] | None,
        typer.Option("--filter", help="Filter string (repeatable)."),
    ] = None,
    program: Annotated[
        list[str] | None,
        typer.Option("--program", help="Program UID (repeatable) to narrow results."),
    ] = None,
    start_date: Annotated[str | None, typer.Option("--start-date")] = None,
    end_date: Annotated[str | None, typer.Option("--end-date")] = None,
    ou_mode: Annotated[
        str | None,
        typer.Option("--ou-mode", help="SELECTED | CHILDREN | DESCENDANTS | ACCESSIBLE | ALL (default SELECTED)."),
    ] = None,
    display_property: Annotated[
        str | None,
        typer.Option("--display-property", help="NAME | SHORTNAME."),
    ] = None,
    skip_meta: Annotated[bool, typer.Option("--skip-meta")] = False,
    skip_data: Annotated[bool, typer.Option("--skip-data")] = False,
    include_metadata_details: Annotated[
        bool,
        typer.Option("--include-metadata-details", help="Include nested objects in the metaData map."),
    ] = False,
    page: Annotated[int | None, typer.Option("--page")] = None,
    page_size: Annotated[int | None, typer.Option("--page-size")] = None,
    asc: Annotated[
        list[str] | None,
        typer.Option("--asc", help="Field to sort ascending (repeatable)."),
    ] = None,
    desc: Annotated[
        list[str] | None,
        typer.Option("--desc", help="Field to sort descending (repeatable)."),
    ] = None,
) -> None:
    """Line-list tracked entities via `/api/analytics/trackedEntities/query/{TET_UID}`."""
    response = asyncio.run(
        service.query_tracked_entities(
            profile_from_env(),
            tracked_entity_type=tracked_entity_type,
            dimensions=dimension,
            filters=filter,
            program=program,
            start_date=start_date,
            end_date=end_date,
            ou_mode=ou_mode,
            display_property=display_property,
            skip_meta=skip_meta,
            skip_data=skip_data,
            include_metadata_details=include_metadata_details,
            page=page,
            page_size=page_size,
            asc=asc,
            desc=desc,
        )
    )
    typer.echo(response.model_dump_json(indent=2, exclude_none=True))


def register(root_app: Any) -> None:
    """Mount under `dhis2 analytics`."""
    root_app.add_typer(app, name="analytics", help="DHIS2 analytics queries.")
