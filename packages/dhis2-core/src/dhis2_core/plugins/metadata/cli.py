"""Typer sub-app for the `metadata` plugin (mounted under `dhis2 metadata`)."""

from __future__ import annotations

import asyncio
import json
from typing import Annotated, Any

import typer
from rich.console import Console
from rich.table import Table

from dhis2_core.plugins.metadata import service
from dhis2_core.profile import profile_from_env

app = typer.Typer(help="Inspect and list DHIS2 metadata (wraps generated CRUD resources).", no_args_is_help=True)
type_app = typer.Typer(help="Metadata resource types (the catalog).", no_args_is_help=True)
app.add_typer(type_app, name="type")
_console = Console()


@type_app.command("list")
@type_app.command("ls", hidden=True)
def type_list_command() -> None:
    """List the metadata resource types exposed by the connected DHIS2 instance."""
    names = asyncio.run(service.list_resource_types(profile_from_env()))
    for name in names:
        typer.echo(name)
    typer.echo(f"\n{len(names)} types available")


@app.command("list")
@app.command("ls", hidden=True)
def list_command(
    resource: Annotated[str, typer.Argument(help="Resource type, e.g. dataElements, indicators")],
    fields: Annotated[
        str, typer.Option("--fields", help="DHIS2 fields selector (e.g. 'id,name,displayName').")
    ] = "id,name",
    filter: Annotated[
        str | None,
        typer.Option("--filter", help="DHIS2 filter string (e.g. 'name:like:Malaria')."),
    ] = None,
    limit: Annotated[int, typer.Option("--limit", help="Max rows to print.")] = 25,
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON instead of a table.")] = False,
) -> None:
    """List instances of a metadata resource."""
    items = asyncio.run(service.list_metadata(profile_from_env(), resource, fields=fields, filter=filter, limit=limit))
    if as_json:
        typer.echo(json.dumps(items, indent=2))
        return
    _print_table(resource, items, fields.split(","))


@app.command("get")
def get_command(
    resource: Annotated[str, typer.Argument(help="Resource type, e.g. dataElements")],
    uid: Annotated[str, typer.Argument(help="Object UID")],
    fields: Annotated[str | None, typer.Option("--fields", help="DHIS2 fields selector.")] = None,
) -> None:
    """Fetch one metadata object by UID and print it as JSON."""
    payload = asyncio.run(
        service.get_metadata(profile_from_env(), resource, uid, fields=fields),
    )
    typer.echo(json.dumps(payload, indent=2))


def _print_table(resource: str, items: list[dict[str, Any]], columns: list[str]) -> None:
    columns = [c.strip() for c in columns if c.strip()]
    table = Table(title=f"{resource} ({len(items)} row{'s' if len(items) != 1 else ''})")
    for column in columns:
        table.add_column(column, overflow="fold")
    for item in items:
        table.add_row(*[_cell(item.get(column)) for column in columns])
    _console.print(table)


def _cell(value: Any) -> str:
    if value is None:
        return "-"
    if isinstance(value, (dict, list)):
        return json.dumps(value, separators=(",", ":"))
    return str(value)


def register(root_app: Any) -> None:
    """Mount this plugin's Typer sub-app under `dhis2 metadata`."""
    root_app.add_typer(app, name="metadata", help="DHIS2 metadata inspection.")
