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


@app.command("refresh")
def refresh_command(
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
) -> None:
    """Trigger analytics-table regeneration; with --watch, stream progress to completion."""
    from dhis2_core.cli_task_watch import stream_task_to_stdout

    profile = profile_from_env()
    response = asyncio.run(
        service.refresh_analytics(profile, skip_resource_tables=skip_resource_tables, last_years=last_years),
    )
    typer.echo(response.model_dump_json(indent=2, exclude_none=True))
    if watch:
        ref = response.task_ref()
        if ref is None:
            typer.secho("error: response has no jobType/id — nothing to watch", err=True, fg=typer.colors.RED)
            raise typer.Exit(1)
        job_type, task_uid = ref
        asyncio.run(stream_task_to_stdout(profile, job_type, task_uid, interval=interval, timeout=timeout))


def register(root_app: Any) -> None:
    """Mount under `dhis2 analytics`."""
    root_app.add_typer(app, name="analytics", help="DHIS2 analytics queries.")
