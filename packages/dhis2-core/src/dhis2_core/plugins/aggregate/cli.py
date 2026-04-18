"""Typer sub-app for aggregate data values (mounted under `dhis2 data aggregate`)."""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Annotated, Any

import typer

from dhis2_core.plugins.aggregate import service
from dhis2_core.profile import profile_from_env

app = typer.Typer(
    help="Aggregate data values — DHIS2 /api/dataValueSets and /api/dataValues.",
    no_args_is_help=True,
)


@app.command("get")
def get_command(
    data_set: Annotated[str | None, typer.Option("--data-set", help="DataSet UID.")] = None,
    period: Annotated[str | None, typer.Option("--period", help="Period (e.g. 202401, 2024W12, 2024).")] = None,
    start_date: Annotated[str | None, typer.Option("--start-date", help="ISO date (YYYY-MM-DD).")] = None,
    end_date: Annotated[str | None, typer.Option("--end-date", help="ISO date (YYYY-MM-DD).")] = None,
    org_unit: Annotated[str | None, typer.Option("--org-unit", help="OrganisationUnit UID.")] = None,
    children: Annotated[bool, typer.Option("--children", help="Include descendants of org_unit.")] = False,
    data_element_group: Annotated[
        str | None,
        typer.Option("--data-element-group", "--deg", help="DataElementGroup UID (narrows to its member DEs)."),
    ] = None,
    limit: Annotated[int | None, typer.Option("--limit", help="Max rows to include in output.")] = None,
) -> None:
    """Fetch a data value set."""
    payload = asyncio.run(
        service.get_data_values(
            profile_from_env(),
            data_set=data_set,
            period=period,
            start_date=start_date,
            end_date=end_date,
            org_unit=org_unit,
            children=children,
            data_element_group=data_element_group,
            limit=limit,
        )
    )
    typer.echo(json.dumps(payload, indent=2))


@app.command("push")
def push_command(
    file: Annotated[Path, typer.Argument(help="Path to a JSON file containing a dataValues array or envelope.")],
    data_set: Annotated[str | None, typer.Option("--data-set")] = None,
    period: Annotated[str | None, typer.Option("--period")] = None,
    org_unit: Annotated[str | None, typer.Option("--org-unit")] = None,
    dry_run: Annotated[bool, typer.Option("--dry-run")] = False,
    import_strategy: Annotated[
        str | None, typer.Option("--strategy", help="CREATE | UPDATE | CREATE_AND_UPDATE | DELETE")
    ] = None,
) -> None:
    """Bulk push data values from a JSON file."""
    loaded: Any = json.loads(file.read_text(encoding="utf-8"))
    if isinstance(loaded, list):
        data_values = loaded
    elif isinstance(loaded, dict) and isinstance(loaded.get("dataValues"), list):
        data_values = loaded["dataValues"]
        data_set = data_set or loaded.get("dataSet")
        period = period or loaded.get("period")
        org_unit = org_unit or loaded.get("orgUnit")
    else:
        raise typer.BadParameter("file must contain a dataValues array or an envelope with dataValues[]")

    response = asyncio.run(
        service.push_data_values(
            profile_from_env(),
            data_values,
            data_set=data_set,
            period=period,
            org_unit=org_unit,
            dry_run=dry_run,
            import_strategy=import_strategy,
        )
    )
    typer.echo(json.dumps(response, indent=2))


@app.command("set")
def set_command(
    data_element: Annotated[
        str, typer.Option("--data-element", "--de", prompt="DataElement UID", help="DataElement UID.")
    ],
    period: Annotated[str, typer.Option("--period", "--pe", prompt="Period", help="Period (e.g. 202401).")],
    org_unit: Annotated[
        str, typer.Option("--org-unit", "--ou", prompt="OrganisationUnit UID", help="OrganisationUnit UID.")
    ],
    value: Annotated[str, typer.Option("--value", prompt="Value", help="The value to set (as a string).")],
    category_option_combo: Annotated[str | None, typer.Option("--coc", help="CategoryOptionCombo UID.")] = None,
    attribute_option_combo: Annotated[
        str | None, typer.Option("--aoc", help="AttributeOptionCombo UID (category-combo attributes).")
    ] = None,
    comment: Annotated[str | None, typer.Option("--comment")] = None,
) -> None:
    """Set a single data value."""
    response = asyncio.run(
        service.set_data_value(
            profile_from_env(),
            data_element=data_element,
            period=period,
            org_unit=org_unit,
            value=value,
            category_option_combo=category_option_combo,
            attribute_option_combo=attribute_option_combo,
            comment=comment,
        )
    )
    typer.echo(json.dumps(response, indent=2))


@app.command("delete")
def delete_command(
    data_element: Annotated[str, typer.Option("--data-element", "--de", prompt="DataElement UID")],
    period: Annotated[str, typer.Option("--period", "--pe", prompt="Period")],
    org_unit: Annotated[str, typer.Option("--org-unit", "--ou", prompt="OrganisationUnit UID")],
    category_option_combo: Annotated[str | None, typer.Option("--coc")] = None,
    attribute_option_combo: Annotated[str | None, typer.Option("--aoc")] = None,
) -> None:
    """Delete a single data value."""
    response = asyncio.run(
        service.delete_data_value(
            profile_from_env(),
            data_element=data_element,
            period=period,
            org_unit=org_unit,
            category_option_combo=category_option_combo,
            attribute_option_combo=attribute_option_combo,
        )
    )
    typer.echo(json.dumps(response, indent=2))
