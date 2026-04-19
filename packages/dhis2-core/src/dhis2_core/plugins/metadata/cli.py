"""Typer sub-app for the `metadata` plugin (mounted under `dhis2 metadata`)."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import Annotated, Any

import typer
from rich.console import Console
from rich.table import Table

from dhis2_core.cli_output import render_webmessage
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
        str,
        typer.Option(
            "--fields",
            help="DHIS2 field selector: plain ('id,name'), presets (':identifiable', ':nameable', ':owner', ':all'), "
            "nested ('children[id,name]'), or exclusions (':all,!lastUpdated').",
        ),
    ] = "id,name",
    filters: Annotated[
        list[str] | None,
        typer.Option(
            "--filter",
            help=(
                "Filter in `property:operator:value` form. Repeatable — AND'd by default, "
                "use --root-junction OR to switch."
            ),
        ),
    ] = None,
    root_junction: Annotated[
        str,
        typer.Option("--root-junction", help="Combine repeated --filter as AND (default) or OR."),
    ] = "AND",
    order: Annotated[
        list[str] | None,
        typer.Option(
            "--order",
            help="Sort clause like 'name:asc' or 'created:desc'. Repeatable (later clauses tie-break).",
        ),
    ] = None,
    page: Annotated[
        int | None,
        typer.Option("--page", help="Server-side page number (1-based). Ignored when --all is set."),
    ] = None,
    page_size: Annotated[
        int | None,
        typer.Option("--page-size", help="Server-side page size (default 50). Ignored when --all is set."),
    ] = None,
    fetch_all: Annotated[
        bool,
        typer.Option(
            "--all",
            help="Stream every page server-side (ignores --page/--page-size). Useful for dumping a full catalog.",
        ),
    ] = False,
    translate: Annotated[
        bool | None,
        typer.Option("--translate/--no-translate", help="Return server-side translations for i18n fields."),
    ] = None,
    locale: Annotated[str | None, typer.Option("--locale", help="Locale for --translate, e.g. 'fr'.")] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON instead of a table.")] = False,
) -> None:
    """List instances of a metadata resource."""
    rj = root_junction if filters and len(filters) > 1 else None
    if fetch_all:
        items = asyncio.run(
            _collect_all(
                resource,
                fields=fields,
                filters=filters,
                root_junction=rj,
                order=order,
                translate=translate,
                locale=locale,
            )
        )
    else:
        items = asyncio.run(
            service.list_metadata(
                profile_from_env(),
                resource,
                fields=fields,
                filters=filters,
                root_junction=rj,
                order=order,
                page=page,
                page_size=page_size,
                translate=translate,
                locale=locale,
            )
        )
    if as_json:
        typer.echo(json.dumps(items, indent=2))
        return
    _print_table(resource, items, fields.split(","))


async def _collect_all(
    resource: str,
    *,
    fields: str,
    filters: list[str] | None,
    root_junction: str | None,
    order: list[str] | None,
    translate: bool | None,
    locale: str | None,
) -> list[dict[str, Any]]:
    """Drain `iter_metadata` into a list for table/JSON rendering."""
    collected: list[dict[str, Any]] = []
    async for item in service.iter_metadata(
        profile_from_env(),
        resource,
        fields=fields,
        filters=filters,
        root_junction=root_junction,
        order=order,
        translate=translate,
        locale=locale,
    ):
        collected.append(item)
    return collected


@app.command("get")
def get_command(
    resource: Annotated[str, typer.Argument(help="Resource type, e.g. dataElements")],
    uid: Annotated[str, typer.Argument(help="Object UID")],
    fields: Annotated[str | None, typer.Option("--fields", help="DHIS2 fields selector.")] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit the full JSON payload instead of a summary.")] = False,
) -> None:
    """Fetch one metadata object by UID.

    Prints a concise Rich summary by default (id, name, code, common metadata +
    notable extras). Use `--json` for the full payload when debugging or
    piping into jq. Pass `--fields` to narrow what DHIS2 returns.
    """
    from dhis2_core.cli_output import DetailRow, render_detail

    payload = asyncio.run(
        service.get_metadata(profile_from_env(), resource, uid, fields=fields),
    )
    if as_json:
        typer.echo(json.dumps(payload, indent=2))
        return
    # Standard top-level identity fields (present on almost every DHIS2 resource).
    rows: list[DetailRow] = []
    for key in ("id", "name", "displayName", "shortName", "code", "description", "href", "created", "lastUpdated"):
        if key in payload:
            rows.append(DetailRow(key, _summary_cell(payload[key])))
    # Pull a few more keys if they're present + interesting (type-specific).
    extras = [
        k
        for k in (
            "valueType",
            "aggregationType",
            "domainType",
            "periodType",
            "url",
            "disabled",
            "publicAccess",
            "programType",
            "level",
            "parent",
            "openingDate",
            "closedDate",
        )
        if k in payload
    ]
    for key in extras:
        rows.append(DetailRow(key, _summary_cell(payload[key])))
    # List all other top-level keys with a compact summary.
    shown = {row.label for row in rows}
    rest = sorted(k for k in payload if k not in shown and not k.startswith("_"))
    if rest:
        rows.append(DetailRow("[dim]more keys[/dim]", ", ".join(rest)))
    render_detail(f"{resource}/{uid}", rows)


def _summary_cell(value: Any) -> str:
    """Compact cell renderer for the metadata-get summary — references as `name (id)`."""
    from dhis2_core.cli_output import format_ref, format_reflist

    if value is None:
        return "-"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (list, tuple)):
        if value and isinstance(value[0], (dict, str)):
            return format_reflist(value)
        return str(value)
    if isinstance(value, dict):
        return format_ref(value)
    return str(value)


def _print_table(resource: str, items: list[dict[str, Any]], columns: list[str]) -> None:
    columns = [c.strip() for c in columns if c.strip() and not c.startswith(":")]
    if not columns:
        # Fallback when a preset (`:identifiable`, etc.) was used — infer keys from the first row.
        columns = sorted(items[0].keys()) if items else ["id"]
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


@app.command("export")
def export_command(
    resource: Annotated[
        list[str] | None,
        typer.Option(
            "--resource",
            help="Resource type to include (repeatable). Omit for every type DHIS2 exports by default.",
        ),
    ] = None,
    fields: Annotated[
        str | None,
        typer.Option(
            "--fields",
            help="DHIS2 field selector. Defaults to ':owner' for a lossless round-trip import.",
        ),
    ] = ":owner",
    skip_sharing: Annotated[
        bool, typer.Option("--skip-sharing", help="Exclude sharing blocks from exported objects.")
    ] = False,
    skip_translation: Annotated[bool, typer.Option("--skip-translation", help="Exclude translation blocks.")] = False,
    skip_validation: Annotated[
        bool,
        typer.Option("--skip-validation", help="Skip validation during export (matches DHIS2's server-side option)."),
    ] = False,
    output: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            help="Write the bundle to this file (JSON). Omit to print to stdout.",
        ),
    ] = None,
    pretty: Annotated[bool, typer.Option("--pretty/--no-pretty", help="Indent JSON output (default: pretty).")] = True,
) -> None:
    """Download a metadata bundle from `GET /api/metadata`.

    Prints a per-resource count summary to stderr so stdout stays pipe-friendly
    when `--output` is omitted.
    """
    bundle = asyncio.run(
        service.export_metadata(
            profile_from_env(),
            resources=resource,
            fields=fields,
            skip_sharing=skip_sharing,
            skip_translation=skip_translation,
            skip_validation=skip_validation,
        )
    )
    summary = service.summarise_bundle(bundle)
    total = sum(summary.values())
    payload = json.dumps(bundle, indent=2) if pretty else json.dumps(bundle, separators=(",", ":"))
    if output is None:
        sys.stdout.write(payload)
        sys.stdout.write("\n")
    else:
        output.write_text(payload + "\n", encoding="utf-8")
        typer.secho(f"wrote {output} ({total} objects across {len(summary)} resource types)", err=True)
    _render_bundle_summary(summary, destination=f"written to {output}" if output else "stdout")


@app.command("import")
def import_command(
    file: Annotated[Path, typer.Argument(help="Path to the metadata bundle JSON.")],
    import_strategy: Annotated[
        str,
        typer.Option(
            "--strategy",
            help="CREATE | UPDATE | CREATE_AND_UPDATE | DELETE (default CREATE_AND_UPDATE).",
        ),
    ] = "CREATE_AND_UPDATE",
    atomic_mode: Annotated[
        str,
        typer.Option(
            "--atomic-mode",
            help="ALL (rollback on any failure) or NONE (commit surviving objects).",
        ),
    ] = "ALL",
    dry_run: Annotated[
        bool,
        typer.Option(
            "--dry-run",
            help="Validate + preheat without committing. Output is the import report DHIS2 would have produced.",
        ),
    ] = False,
    identifier: Annotated[
        str,
        typer.Option("--identifier", help="UID | CODE | AUTO (default UID)."),
    ] = "UID",
    skip_sharing: Annotated[bool, typer.Option("--skip-sharing")] = False,
    skip_translation: Annotated[bool, typer.Option("--skip-translation")] = False,
    skip_validation: Annotated[bool, typer.Option("--skip-validation")] = False,
    merge_mode: Annotated[
        str | None,
        typer.Option("--merge-mode", help="REPLACE (overwrite) or MERGE (patch) existing objects."),
    ] = None,
    preheat_mode: Annotated[
        str | None,
        typer.Option("--preheat-mode", help="REFERENCE (default), ALL, or NONE."),
    ] = None,
    flush_mode: Annotated[
        str | None,
        typer.Option("--flush-mode", help="AUTO (default) or OBJECT."),
    ] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw WebMessageResponse JSON.")] = False,
) -> None:
    """Upload a metadata bundle via `POST /api/metadata` and print the import report."""
    bundle = json.loads(file.read_text(encoding="utf-8"))
    if not isinstance(bundle, dict):
        raise typer.BadParameter(f"{file} must contain a metadata bundle object (got {type(bundle).__name__})")
    typer.secho(f"posting {file} → /api/metadata (dry_run={dry_run})", err=True)
    summary = service.summarise_bundle(bundle)
    if summary:
        _render_bundle_summary(summary, destination=f"source: {file}")
    response = asyncio.run(
        service.import_metadata(
            profile_from_env(),
            bundle,
            import_strategy=import_strategy,
            atomic_mode=atomic_mode,
            dry_run=dry_run,
            identifier=identifier,
            skip_sharing=skip_sharing,
            skip_translation=skip_translation,
            skip_validation=skip_validation,
            merge_mode=merge_mode,
            preheat_mode=preheat_mode,
            flush_mode=flush_mode,
        )
    )
    render_webmessage(response, as_json=as_json, action="imported")


def _render_bundle_summary(summary: dict[str, int], *, destination: str) -> None:
    """Print a Rich table of `{resource: count}` + total to stderr (keeps stdout pipe-friendly)."""
    total = sum(summary.values())
    err_console = Console(stderr=True)
    table = Table(title=f"metadata bundle ({total} objects, {destination})")
    table.add_column("resource", overflow="fold")
    table.add_column("count", justify="right")
    for resource_name in sorted(summary, key=lambda k: (-summary[k], k)):
        table.add_row(resource_name, str(summary[resource_name]))
    err_console.print(table)


def register(root_app: Any) -> None:
    """Mount this plugin's Typer sub-app under `dhis2 metadata`."""
    root_app.add_typer(app, name="metadata", help="DHIS2 metadata inspection.")
