"""Typer sub-app for the `metadata` plugin (mounted under `dhis2 metadata`)."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from typing import Annotated, Any

import typer
from dhis2_client import JsonPatchOpAdapter
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table

from dhis2_core.cli_output import render_webmessage
from dhis2_core.plugins.metadata import service
from dhis2_core.plugins.metadata.models import MetadataBundle
from dhis2_core.profile import profile_from_env

app = typer.Typer(help="Inspect and list DHIS2 metadata (wraps generated CRUD resources).", no_args_is_help=True)
type_app = typer.Typer(help="Metadata resource types (the catalog).", no_args_is_help=True)
app.add_typer(type_app, name="type")
options_app = typer.Typer(help="OptionSet workflows (show / find / sync).", no_args_is_help=True)
app.add_typer(options_app, name="options")
options_attribute_app = typer.Typer(
    help="External-system code mapping on Options via Attribute values.",
    no_args_is_help=True,
)
options_app.add_typer(options_attribute_app, name="attribute")
attribute_app = typer.Typer(
    help="Cross-resource AttributeValue workflows (get / set / delete / find).",
    no_args_is_help=True,
)
app.add_typer(attribute_app, name="attribute")
program_rule_app = typer.Typer(
    help="Program rule workflows (show / vars-for / validate / where-de-is-used).",
    no_args_is_help=True,
)
app.add_typer(program_rule_app, name="program-rule")
sql_view_app = typer.Typer(
    help="SQL view workflows (list / show / execute / refresh / adhoc).",
    no_args_is_help=True,
)
app.add_typer(sql_view_app, name="sql-view")
viz_app = typer.Typer(
    help="Visualization authoring (list / show / create / clone / delete).",
    no_args_is_help=True,
)
app.add_typer(viz_app, name="viz")
dashboard_app = typer.Typer(
    help="Dashboard composition (list / show / add-item / remove-item).",
    no_args_is_help=True,
)
app.add_typer(dashboard_app, name="dashboard")
_console = Console()


@type_app.command("list")
@type_app.command("ls", hidden=True)
def type_list_command() -> None:
    """List the metadata resource types exposed by the connected DHIS2 instance."""
    names = asyncio.run(service.list_resource_types(profile_from_env()))
    if not names:
        typer.echo("no metadata types reported by this instance")
        return
    table = Table(title=f"DHIS2 metadata types ({len(names)})")
    table.add_column("resource type", style="cyan", no_wrap=True)
    for name in names:
        table.add_row(name)
    _console.print(table)


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
    rows = [_dump_for_cli(model) for model in items]
    if as_json:
        typer.echo(json.dumps(rows, indent=2))
        return
    _print_table(resource, rows, fields.split(","))


def _dump_for_cli(model: Any) -> dict[str, Any]:
    """Dump a typed generated model to a JSON-friendly dict for CLI table/JSON rendering.

    Edge-of-world carveout: the service returns typed models; CLI (like MCP)
    dumps at the boundary where the output format is JSON/table text rather
    than further Python code.
    """
    if hasattr(model, "model_dump"):
        dumped = model.model_dump(by_alias=True, exclude_none=True, mode="json")
        if isinstance(dumped, dict):
            return dumped
    if isinstance(model, dict):
        return model
    raise TypeError(f"cannot render {type(model).__name__} as a CLI row")


async def _collect_all(
    resource: str,
    *,
    fields: str,
    filters: list[str] | None,
    root_junction: str | None,
    order: list[str] | None,
    translate: bool | None,
    locale: str | None,
) -> list[BaseModel]:
    """Drain `iter_metadata` into a list for table/JSON rendering."""
    collected: list[BaseModel] = []
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

    model = asyncio.run(
        service.get_metadata(profile_from_env(), resource, uid, fields=fields),
    )
    payload = _dump_for_cli(model)
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
    resource_filter: Annotated[
        list[str] | None,
        typer.Option(
            "--filter",
            help=(
                "Per-resource filter in the form `RESOURCE:property:operator:value`. Repeatable. "
                "Example: `--filter dataElements:name:like:ANC`. "
                "Same DSL as `dhis2 metadata list --filter`, prefixed with the resource name."
            ),
        ),
    ] = None,
    resource_fields: Annotated[
        list[str] | None,
        typer.Option(
            "--resource-fields",
            help=(
                "Per-resource field selector in the form `RESOURCE:SELECTOR`. Repeatable. "
                "Overrides the global `--fields` for the named resource. "
                "Example: `--resource-fields dataElements::identifiable`."
            ),
        ),
    ] = None,
    skip_sharing: Annotated[
        bool, typer.Option("--skip-sharing", help="Exclude sharing blocks from exported objects.")
    ] = False,
    skip_translation: Annotated[bool, typer.Option("--skip-translation", help="Exclude translation blocks.")] = False,
    skip_validation: Annotated[
        bool,
        typer.Option("--skip-validation", help="Skip validation during export (matches DHIS2's server-side option)."),
    ] = False,
    check_references: Annotated[
        bool,
        typer.Option(
            "--check-references/--no-check-references",
            help=(
                "After export, walk the bundle and warn on references to UIDs not in the bundle "
                "(e.g. a dataElement's categoryCombo missing from a filtered export). On by default."
            ),
        ),
    ] = True,
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
    when `--output` is omitted. With `--check-references` (default), walks the
    exported bundle and warns on any reference to a UID not in the bundle —
    so a filtered `--resource dataElements` export doesn't silently produce a
    bundle that won't round-trip because categoryCombos / optionSets / ...
    are missing.
    """
    per_resource_filters = _parse_prefixed_multi(resource_filter or [], flag_name="--filter")
    per_resource_fields_map = _parse_prefixed_single(resource_fields or [], flag_name="--resource-fields")
    bundle = asyncio.run(
        service.export_metadata(
            profile_from_env(),
            resources=resource,
            fields=fields,
            skip_sharing=skip_sharing,
            skip_translation=skip_translation,
            skip_validation=skip_validation,
            per_resource_filters=per_resource_filters or None,
            per_resource_fields=per_resource_fields_map or None,
        )
    )
    summary = bundle.summary()
    total = bundle.total()
    payload = bundle.model_dump_json(indent=2 if pretty else None, exclude_none=True, by_alias=True)
    if output is None:
        sys.stdout.write(payload)
        sys.stdout.write("\n")
    else:
        output.write_text(payload + "\n", encoding="utf-8")
        typer.secho(f"wrote {output} ({total} objects across {len(summary)} resource types)", err=True)
    _render_bundle_summary(summary, destination=f"written to {output}" if output else "stdout")
    if check_references:
        refs = service.bundle_dangling_references(bundle)
        _render_dangling_references(refs)


def _parse_prefixed_multi(values: list[str], *, flag_name: str) -> dict[str, list[str]]:
    """Parse repeatable `RESOURCE:expr` flags into `{resource: [exprs...]}`.

    Splits on the first colon so the `property:operator:value` portion stays
    intact. Raises a Typer error on values with no colon.
    """
    parsed: dict[str, list[str]] = {}
    for raw in values:
        resource, sep, expr = raw.partition(":")
        if not sep or not resource or not expr:
            raise typer.BadParameter(
                f"{flag_name} value {raw!r} must be `RESOURCE:expr` (e.g. `dataElements:name:like:ANC`)"
            )
        parsed.setdefault(resource, []).append(expr)
    return parsed


def _parse_prefixed_single(values: list[str], *, flag_name: str) -> dict[str, str]:
    """Parse repeatable `RESOURCE:selector` flags into `{resource: selector}` (last wins)."""
    parsed: dict[str, str] = {}
    for raw in values:
        resource, sep, selector = raw.partition(":")
        if not sep or not resource or not selector:
            raise typer.BadParameter(
                f"{flag_name} value {raw!r} must be `RESOURCE:selector` (e.g. `dataElements::identifiable`)"
            )
        parsed[resource] = selector
    return parsed


def _render_dangling_references(refs: service.DanglingReferences) -> None:
    """Print a Rich warning + per-field breakdown when the bundle has dangling references."""
    if refs.is_clean:
        _console.print(
            f"[dim]reference check: {refs.bundle_uid_count} UIDs in bundle, no dangling references.[/dim]",
            highlight=False,
        )
        return
    _console.print(
        f"[yellow]WARNING[/yellow]: {refs.total_missing} dangling reference(s) — "
        f"UIDs referenced by objects in the bundle but not present in the bundle itself.",
        highlight=False,
    )
    table = Table(show_edge=False, show_header=True, pad_edge=False)
    table.add_column("field", style="yellow")
    table.add_column("missing", justify="right")
    table.add_column("sample UIDs", overflow="fold", style="dim")
    for item in refs.items:
        sample = ", ".join(item.missing_uids[:3])
        if item.count > 3:
            sample += f" (+{item.count - 3} more)"
        table.add_row(item.field_name, str(item.count), sample)
    _console.print(table)
    _console.print(
        "[dim]Re-run with the referenced resource types added (e.g. "
        "`--resource categoryCombos --resource optionSets`) "
        "or silence this check with `--no-check-references`.[/dim]",
        highlight=False,
    )


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
    raw = json.loads(file.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise typer.BadParameter(f"{file} must contain a metadata bundle object (got {type(raw).__name__})")
    bundle = MetadataBundle.from_raw(raw)
    typer.secho(f"posting {file} → /api/metadata (dry_run={dry_run})", err=True)
    summary = bundle.summary()
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


@app.command("patch")
def patch_command(
    resource: Annotated[str, typer.Argument(help="Resource type, e.g. dataElements, indicators.")],
    uid: Annotated[str, typer.Argument(help="UID of the object to patch.")],
    file: Annotated[
        Path | None,
        typer.Option(
            "--file",
            help="JSON file with a RFC 6902 patch array. Mutually exclusive with --set/--remove.",
        ),
    ] = None,
    set_ops: Annotated[
        list[str] | None,
        typer.Option(
            "--set",
            help=(
                "Inline `replace` op as `path=value`. Repeatable. Values are JSON-decoded "
                'when they parse as JSON (`{"a":1}`, `true`, `42`) and treated as strings otherwise.'
            ),
        ),
    ] = None,
    remove_ops: Annotated[
        list[str] | None,
        typer.Option(
            "--remove",
            help="Inline `remove` op as `path`. Repeatable.",
        ),
    ] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw WebMessageResponse JSON.")] = False,
) -> None:
    """Apply an RFC 6902 JSON Patch to a metadata object (`PATCH /api/<resource>/{uid}`).

    Two input modes:

    - `--file patch.json` — full patch array on disk, one op per entry:
      `[{"op": "replace", "path": "/name", "value": "New"}, ...]`
    - `--set path=value` / `--remove path` (each repeatable) — inline shorthand
      for the common replace/remove cases. Values parse as JSON when possible
      (so `--set /valueType=INTEGER` sends a string, `--set /disabled=true`
      sends a boolean).
    """
    if (file is None) == (not set_ops and not remove_ops):
        raise typer.BadParameter("pass either --file OR --set/--remove inline ops (not both, not neither)")

    ops_raw: list[dict[str, Any]]
    if file is not None:
        parsed = json.loads(file.read_text(encoding="utf-8"))
        if not isinstance(parsed, list):
            raise typer.BadParameter(f"{file} must contain a JSON Patch array (got {type(parsed).__name__})")
        ops_raw = parsed
    else:
        ops_raw = []
        for assign in set_ops or []:
            path, sep, raw_value = assign.partition("=")
            if not sep:
                raise typer.BadParameter(f"--set value {assign!r} must be `path=value`")
            try:
                value: Any = json.loads(raw_value)
            except json.JSONDecodeError:
                value = raw_value
            ops_raw.append({"op": "replace", "path": path, "value": value})
        for path in remove_ops or []:
            ops_raw.append({"op": "remove", "path": path})

    ops = [JsonPatchOpAdapter.validate_python(op) for op in ops_raw]
    typer.secho(f"patching {resource}/{uid} ({len(ops)} op{'s' if len(ops) != 1 else ''})", err=True)
    response = asyncio.run(service.patch_metadata(profile_from_env(), resource, uid, ops))
    render_webmessage(response, as_json=as_json, action=f"patched {resource}/{uid}")


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


@app.command("diff")
def diff_command(
    left: Annotated[
        Path,
        typer.Argument(help="Left-hand bundle — the 'source of truth' you're comparing against."),
    ],
    right: Annotated[
        Path | None,
        typer.Argument(
            help="Right-hand bundle. Omit with `--live` to diff against the connected DHIS2 instance.",
        ),
    ] = None,
    live: Annotated[
        bool,
        typer.Option(
            "--live",
            help=(
                "Use the connected DHIS2 instance as the right-hand side. "
                "Exports only the resource types present in the left bundle "
                "(no full-catalog fetch). Incompatible with a positional right arg."
            ),
        ),
    ] = False,
    show_uids: Annotated[
        bool,
        typer.Option("--show-uids", help="List up to 5 offending UIDs per per-resource row."),
    ] = False,
    ignore: Annotated[
        list[str] | None,
        typer.Option(
            "--ignore",
            help=(
                "Fields to skip when deciding if an object changed. Repeatable. "
                "Defaults cover DHIS2's per-instance noise (lastUpdated, createdBy, access, ...); "
                "pass `--ignore sharing` etc. to extend."
            ),
        ),
    ] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit the typed MetadataDiff as JSON.")] = False,
) -> None:
    """Compare two metadata bundles (or one bundle against the live instance).

    Per-resource counts of create/update/delete. Objects that differ only on
    DHIS2's per-instance noise (lastUpdated, createdBy, etc.) are treated as
    unchanged by default — `--ignore` extends that list.
    """
    if (right is None) == (not live):
        raise typer.BadParameter("provide exactly one of a second positional bundle or --live")

    left_raw = json.loads(left.read_text(encoding="utf-8"))
    if not isinstance(left_raw, dict):
        raise typer.BadParameter(f"{left} is not a metadata bundle (expected a JSON object)")
    left_bundle = MetadataBundle.from_raw(left_raw)

    ignored = frozenset({*service._DEFAULT_IGNORED_FIELDS, *(ignore or ())})  # noqa: SLF001

    if live:
        profile = profile_from_env()
        typer.secho(f"exporting live instance ({profile.base_url}) to compare against {left.name} ...", err=True)
        diff = asyncio.run(
            service.diff_bundle_against_instance(
                profile,
                left_bundle,
                bundle_label=str(left),
                ignored_fields=ignored,
            )
        )
        # Swap label order so the table reads `left vs live` consistently (diff_bundle_against_instance
        # puts the instance on the left to match "what's on the instance vs what's in the file").
    else:
        right_raw = json.loads(right.read_text(encoding="utf-8"))  # type: ignore[union-attr]
        if not isinstance(right_raw, dict):
            raise typer.BadParameter(f"{right} is not a metadata bundle")
        right_bundle = MetadataBundle.from_raw(right_raw)
        diff = service.diff_bundles(
            left_bundle,
            right_bundle,
            left_label=str(left),
            right_label=str(right),
            ignored_fields=ignored,
        )

    if as_json:
        typer.echo(diff.model_dump_json(indent=2, exclude_none=True))
        return
    _render_diff(diff, show_uids=show_uids)


def _render_diff(diff: service.MetadataDiff, *, show_uids: bool) -> None:
    """Rich-render a MetadataDiff as a per-resource table + totals summary."""
    total_changed = diff.total_created + diff.total_updated + diff.total_deleted
    title = f"metadata diff — {diff.left_label} → {diff.right_label} ({total_changed} changed)"
    table = Table(title=title)
    table.add_column("resource", overflow="fold")
    table.add_column("created", justify="right", style="green")
    table.add_column("updated", justify="right", style="yellow")
    table.add_column("deleted", justify="right", style="red")
    table.add_column("unchanged", justify="right", style="dim")
    if show_uids:
        table.add_column("sample UIDs", overflow="fold", style="dim")

    for resource in diff.resources:
        if resource.total_changed == 0 and resource.unchanged_count == 0:
            continue
        row = [
            resource.resource,
            str(len(resource.created)),
            str(len(resource.updated)),
            str(len(resource.deleted)),
            str(resource.unchanged_count),
        ]
        if show_uids:
            sample = []
            for change in (*resource.created, *resource.updated, *resource.deleted)[:5]:
                label = change.name or "-"
                sample.append(f"{change.id} · {label}")
            row.append("\n".join(sample))
        table.add_row(*row)
    _console.print(table)
    summary = (
        f"[green]+{diff.total_created} created[/green] / "
        f"[yellow]~{diff.total_updated} updated[/yellow] / "
        f"[red]-{diff.total_deleted} deleted[/red] / "
        f"[dim]{diff.total_unchanged} unchanged[/dim]"
    )
    _console.print(summary)
    if diff.ignored_fields:
        _console.print(f"[dim]ignored fields: {', '.join(diff.ignored_fields)}[/dim]")


@app.command("diff-profiles")
def diff_profiles_command(
    profile_a: Annotated[str, typer.Argument(help="Name of the 'left' profile (source of truth).")],
    profile_b: Annotated[str, typer.Argument(help="Name of the 'right' profile (candidate).")],
    resources: Annotated[
        list[str] | None,
        typer.Option(
            "--resource",
            "-r",
            help=(
                "Resource type to compare (e.g. dataElements, indicators). Repeatable. "
                "Required — whole-instance diffs are almost always noise."
            ),
        ),
    ] = None,
    filters: Annotated[
        list[str] | None,
        typer.Option(
            "--filter",
            help=(
                "Per-resource filter in `resource:property:operator:value` form. Repeatable. "
                "Example: `--filter dataElements:name:like:ANC` only compares data elements whose "
                "name contains 'ANC'. Same DHIS2 filter DSL as `dhis2 metadata list --filter`."
            ),
        ),
    ] = None,
    fields: Annotated[
        str,
        typer.Option(
            "--fields",
            help=(
                "DHIS2 field selector applied on both profiles. Defaults to ':owner' — the selector "
                "DHIS2 itself uses for cross-instance imports (preserves every field needed for a "
                "faithful round-trip)."
            ),
        ),
    ] = ":owner",
    ignore: Annotated[
        list[str] | None,
        typer.Option(
            "--ignore",
            help=(
                "Additional fields to skip when deciding if an object changed. Repeatable. "
                "Defaults already cover DHIS2's per-instance noise (lastUpdated, createdBy, access, ...). "
                "Common extensions for drift checks: `--ignore sharing --ignore translations`."
            ),
        ),
    ] = None,
    show_uids: Annotated[
        bool,
        typer.Option("--show-uids", help="List up to 5 offending UIDs per per-resource row."),
    ] = False,
    exit_on_drift: Annotated[
        bool,
        typer.Option(
            "--exit-on-drift",
            help="Exit 1 when any object differs. CI-friendly (default is always exit 0).",
        ),
    ] = False,
    as_json: Annotated[
        bool, typer.Option("--json", help="Emit the typed MetadataDiff as JSON (bypasses the table).")
    ] = False,
) -> None:
    """Diff a metadata slice between two registered profiles (staging vs prod drift).

    Runs both exports in parallel, narrows to `--resource` types, optionally
    filters each resource (`--filter resource:prop:op:val`), then structurally
    diffs the two bundles ignoring DHIS2's per-instance noise
    (timestamps, createdBy, access strings, …).

    A whole-instance diff is almost never useful — staging and prod diverge on
    user accounts, org-unit assignments, and incidental settings by design. Pick
    a narrow resource slice (`-r dataElements -r indicators`), filter further
    with `--filter`, and extend `--ignore` for anything else that's expected to
    differ.

    Exit code is `0` by default regardless of drift (so operators running this
    interactively aren't tripped by per-command-exit conventions). Pass
    `--exit-on-drift` for the CI shape.
    """
    from dhis2_core.profile import UnknownProfileError, resolve_profile

    if not resources:
        raise typer.BadParameter("pass at least one --resource (see `dhis2 metadata type ls`)")

    try:
        resolved_a = resolve_profile(profile_a)
        resolved_b = resolve_profile(profile_b)
    except UnknownProfileError as exc:
        raise typer.BadParameter(str(exc)) from exc

    per_resource_filters = _parse_per_resource_filters(filters or [])
    ignored = frozenset({*service._DEFAULT_IGNORED_FIELDS, *(ignore or ())})  # noqa: SLF001

    typer.secho(
        f"exporting {','.join(resources)} from {profile_a!r} ({resolved_a.base_url}) "
        f"and {profile_b!r} ({resolved_b.base_url}) ...",
        err=True,
    )
    diff = asyncio.run(
        service.diff_profiles(
            resolved_a,
            resolved_b,
            resources=list(resources),
            left_label=profile_a,
            right_label=profile_b,
            fields=fields,
            per_resource_filters=per_resource_filters,
            ignored_fields=ignored,
        )
    )

    if as_json:
        typer.echo(diff.model_dump_json(indent=2, exclude_none=True))
    else:
        _render_diff(diff, show_uids=show_uids)

    if exit_on_drift and (diff.total_created + diff.total_updated + diff.total_deleted) > 0:
        raise typer.Exit(1)


def _parse_per_resource_filters(specs: list[str]) -> dict[str, list[str]]:
    """Parse `resource:property:operator:value` strings into a per-resource filter map.

    Only the first `:` separates resource name from the filter expression; the
    rest is forwarded verbatim to DHIS2 (it already takes `property:operator:value`
    as a single string). So `dataElements:name:like:ANC` parses to
    `{"dataElements": ["name:like:ANC"]}` — multiple filters on the same resource
    merge into the list.
    """
    parsed: dict[str, list[str]] = {}
    for spec in specs:
        if ":" not in spec:
            raise typer.BadParameter(
                f"--filter {spec!r}: expected `resource:property:operator:value` "
                "(first `:` splits the resource from the filter expression)."
            )
        resource, _, expression = spec.partition(":")
        if not resource or not expression:
            raise typer.BadParameter(
                f"--filter {spec!r}: both resource and filter expression must be non-empty.",
            )
        parsed.setdefault(resource, []).append(expression)
    return parsed


def register(root_app: Any) -> None:
    """Mount this plugin's Typer sub-app under `dhis2 metadata`."""
    root_app.add_typer(app, name="metadata", help="DHIS2 metadata inspection.")


# ---------------------------------------------------------------------------
# `dhis2 metadata options ...` — OptionSet workflow commands
# ---------------------------------------------------------------------------


@options_app.command("show")
def options_show_command(
    uid_or_code: Annotated[str, typer.Argument(help="OptionSet UID (11 chars) or business code.")],
    as_json: Annotated[bool, typer.Option("--json", help="Emit the raw OptionSet JSON.")] = False,
) -> None:
    """Show one OptionSet with its options resolved inline."""
    option_set = asyncio.run(service.show_option_set(profile_from_env(), uid_or_code))
    if option_set is None:
        typer.secho(f"no OptionSet with code/uid {uid_or_code!r}", err=True, fg=typer.colors.YELLOW)
        raise typer.Exit(1)
    if as_json:
        typer.echo(option_set.model_dump_json(indent=2, exclude_none=True))
        return
    header = (
        f"[bold]{option_set.name or '-'}[/bold]  "
        f"code=[cyan]{option_set.code or '-'}[/cyan]  "
        f"uid=[dim]{option_set.id or '-'}[/dim]  "
        f"valueType={option_set.valueType or '-'}"
    )
    _console.print(header)
    options = option_set.options or []
    if not options:
        typer.echo("  (no options)")
        return
    table = Table(title=f"options ({len(options)})")
    table.add_column("sort", justify="right", style="dim")
    table.add_column("code", style="cyan")
    table.add_column("name", overflow="fold")
    table.add_column("uid", style="dim")
    for opt in options:
        if isinstance(opt, dict):
            sort_order = opt.get("sortOrder")
            code = opt.get("code") or "-"
            name = opt.get("name") or "-"
            uid = opt.get("id") or "-"
        else:
            sort_order = getattr(opt, "sortOrder", None)
            code = getattr(opt, "code", None) or "-"
            name = getattr(opt, "name", None) or "-"
            uid = getattr(opt, "id", None) or "-"
        table.add_row(str(sort_order) if sort_order is not None else "-", code, name, uid)
    _console.print(table)


@options_app.command("find")
def options_find_command(
    set_ref: Annotated[str, typer.Option("--set", help="OptionSet UID or business code.")],
    option_code: Annotated[
        str | None,
        typer.Option("--code", help="Business code of the option to locate."),
    ] = None,
    option_name: Annotated[
        str | None,
        typer.Option("--name", help="Display name of the option (exact match)."),
    ] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit the raw Option JSON.")] = False,
) -> None:
    """Locate a single option inside a set by code or name; exit 1 if no match."""
    if (option_code is None) == (option_name is None):
        raise typer.BadParameter("exactly one of --code / --name is required")
    option = asyncio.run(
        service.find_option_in_set(
            profile_from_env(),
            option_set_uid_or_code=set_ref,
            option_code=option_code,
            option_name=option_name,
        )
    )
    if option is None:
        typer.secho("no match", err=True, fg=typer.colors.YELLOW)
        raise typer.Exit(1)
    if as_json:
        typer.echo(option.model_dump_json(indent=2, exclude_none=True))
        return
    _console.print(
        f"[cyan]{option.code or '-'}[/cyan]  {option.name or '-'!r}  "
        f"uid=[dim]{option.id or '-'}[/dim]  "
        f"sort=[dim]{option.sortOrder if option.sortOrder is not None else '-'}[/dim]"
    )


@options_app.command("sync")
def options_sync_command(
    set_ref: Annotated[str, typer.Argument(help="OptionSet UID or business code.")],
    spec_file: Annotated[
        Path,
        typer.Argument(
            help="JSON file — list of `{code, name, sort_order?}` objects.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ],
    remove_missing: Annotated[
        bool,
        typer.Option(
            "--remove-missing",
            help="Also delete options whose code isn't in the spec. Off by default — safer for partial refreshes.",
        ),
    ] = False,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Compute the diff without writing anything."),
    ] = False,
    as_json: Annotated[bool, typer.Option("--json", help="Emit the UpsertReport as JSON.")] = False,
) -> None:
    """Idempotently sync an OptionSet to match a JSON spec file.

    The spec is a JSON array of `{code, name, sort_order?}` objects. Codes
    not currently in the set get **added**; codes present but with changed
    names or sort order get **updated**; exact matches are **skipped**.
    Pass `--remove-missing` to also drop options whose code isn't in the
    spec. `--dry-run` previews the diff without writing.
    """
    from dhis2_client import OptionSpec  # noqa: PLC0415 — avoid top-level import for CLI fast-path

    raw = json.loads(spec_file.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise typer.BadParameter(f"spec file {spec_file} must contain a JSON array of objects")
    spec: list[OptionSpec] = []
    for index, entry in enumerate(raw):
        if not isinstance(entry, dict):
            raise typer.BadParameter(f"spec[{index}] is not a JSON object")
        spec.append(OptionSpec.model_validate(entry))

    report = asyncio.run(
        service.sync_option_set(
            profile_from_env(),
            option_set_uid_or_code=set_ref,
            spec=spec,
            remove_missing=remove_missing,
            dry_run=dry_run,
        )
    )
    if as_json:
        typer.echo(report.model_dump_json(indent=2))
        return
    title = "sync report (dry-run)" if dry_run else "sync report"
    table = Table(title=title)
    table.add_column("action", style="cyan")
    table.add_column("count", justify="right")
    table.add_column("codes", overflow="fold")
    for action, codes, style in (
        ("added", report.added, "green"),
        ("updated", report.updated, "yellow"),
        ("removed", report.removed, "red"),
        ("skipped", report.skipped, "dim"),
    ):
        table.add_row(f"[{style}]{action}[/{style}]", str(len(codes)), ", ".join(codes) or "-")
    _console.print(table)


# ---------------------------------------------------------------------------
# `dhis2 metadata options attribute ...` — external-system code mapping
# ---------------------------------------------------------------------------


@options_attribute_app.command("get")
def options_attribute_get_command(
    option_uid: Annotated[str, typer.Argument(help="Option UID (11 chars).")],
    attribute: Annotated[
        str,
        typer.Argument(help="Attribute UID or business code (e.g. 'SNOMED_CODE')."),
    ],
) -> None:
    """Read one attribute value off an Option; exit 1 if unset."""
    value = asyncio.run(
        service.get_option_attribute_value(
            profile_from_env(),
            option_uid=option_uid,
            attribute_code_or_uid=attribute,
        )
    )
    if value is None:
        typer.secho(f"no value for attribute {attribute!r} on {option_uid}", err=True, fg=typer.colors.YELLOW)
        raise typer.Exit(1)
    typer.echo(value)


@options_attribute_app.command("set")
def options_attribute_set_command(
    option_uid: Annotated[str, typer.Argument(help="Option UID (11 chars).")],
    attribute: Annotated[
        str,
        typer.Argument(help="Attribute UID or business code (e.g. 'SNOMED_CODE')."),
    ],
    value: Annotated[str, typer.Argument(help="New attribute value.")],
) -> None:
    """Set / replace an attribute value on an Option.

    Reads the full Option, merges the new value (replaces any prior value
    for the same attribute UID), PUTs the payload back. DHIS2's
    attribute-value list is identity-keyed by attribute UID, so this is
    idempotent — calling twice with the same value is a no-op.
    """
    asyncio.run(
        service.set_option_attribute_value(
            profile_from_env(),
            option_uid=option_uid,
            attribute_code_or_uid=attribute,
            value=value,
        )
    )
    typer.secho(f"set {attribute}={value!r} on {option_uid}", fg=typer.colors.GREEN)


@options_attribute_app.command("find")
def options_attribute_find_command(
    set_ref: Annotated[str, typer.Option("--set", help="OptionSet UID or business code.")],
    attribute: Annotated[
        str,
        typer.Option("--attribute", help="Attribute UID or business code (e.g. 'SNOMED_CODE')."),
    ],
    value: Annotated[str, typer.Option("--value", help="Attribute value to match exactly.")],
    as_json: Annotated[bool, typer.Option("--json", help="Emit the raw Option JSON.")] = False,
) -> None:
    """Reverse lookup — find the Option whose attribute matches a value.

    The killer integration helper: external systems know a SNOMED / ICD /
    LOINC code; this command returns the DHIS2 Option it maps to. Exits 1
    on miss with a stderr hint.
    """
    option = asyncio.run(
        service.find_option_by_attribute(
            profile_from_env(),
            option_set_uid_or_code=set_ref,
            attribute_code_or_uid=attribute,
            value=value,
        )
    )
    if option is None:
        typer.secho(f"no Option with {attribute}={value!r} in set {set_ref!r}", err=True, fg=typer.colors.YELLOW)
        raise typer.Exit(1)
    if as_json:
        typer.echo(option.model_dump_json(indent=2, exclude_none=True))
        return
    _console.print(
        f"[cyan]{option.code or '-'}[/cyan]  {option.name or '-'!r}  "
        f"uid=[dim]{option.id or '-'}[/dim]  "
        f"sort=[dim]{option.sortOrder if option.sortOrder is not None else '-'}[/dim]"
    )


# ---------------------------------------------------------------------------
# `dhis2 metadata attribute ...` — cross-resource AttributeValue workflows
# ---------------------------------------------------------------------------


@attribute_app.command("get")
def attribute_get_command(
    resource: Annotated[
        str,
        typer.Argument(help="Plural DHIS2 resource name (e.g. `dataElements`, `options`, `organisationUnits`)."),
    ],
    resource_uid: Annotated[str, typer.Argument(help="UID of the resource instance.")],
    attribute: Annotated[
        str,
        typer.Argument(help="Attribute UID or business code (e.g. `ICD10_CODE`)."),
    ],
) -> None:
    """Read one attribute value off any resource; exit 1 if unset."""
    value = asyncio.run(
        service.get_attribute_value(
            profile_from_env(),
            resource=resource,
            resource_uid=resource_uid,
            attribute_code_or_uid=attribute,
        )
    )
    if value is None:
        typer.secho(
            f"no value for attribute {attribute!r} on {resource}/{resource_uid}",
            err=True,
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(1)
    typer.echo(value)


@attribute_app.command("set")
def attribute_set_command(
    resource: Annotated[str, typer.Argument(help="Plural DHIS2 resource name.")],
    resource_uid: Annotated[str, typer.Argument(help="UID of the resource instance.")],
    attribute: Annotated[str, typer.Argument(help="Attribute UID or business code.")],
    value: Annotated[str, typer.Argument(help="New attribute value.")],
) -> None:
    """Set / replace one attribute value on any resource (read-merge-write)."""
    asyncio.run(
        service.set_attribute_value(
            profile_from_env(),
            resource=resource,
            resource_uid=resource_uid,
            attribute_code_or_uid=attribute,
            value=value,
        )
    )
    typer.secho(f"set {attribute}={value!r} on {resource}/{resource_uid}", fg=typer.colors.GREEN)


@attribute_app.command("delete")
def attribute_delete_command(
    resource: Annotated[str, typer.Argument(help="Plural DHIS2 resource name.")],
    resource_uid: Annotated[str, typer.Argument(help="UID of the resource instance.")],
    attribute: Annotated[str, typer.Argument(help="Attribute UID or business code.")],
) -> None:
    """Remove one attribute value from any resource; exit 0 regardless of whether it existed."""
    removed = asyncio.run(
        service.delete_attribute_value(
            profile_from_env(),
            resource=resource,
            resource_uid=resource_uid,
            attribute_code_or_uid=attribute,
        )
    )
    if removed:
        typer.secho(f"removed {attribute} on {resource}/{resource_uid}", fg=typer.colors.GREEN)
    else:
        typer.secho(
            f"no-op — {attribute} was not set on {resource}/{resource_uid}",
            fg=typer.colors.YELLOW,
        )


@attribute_app.command("find")
def attribute_find_command(
    resource: Annotated[str, typer.Argument(help="Plural DHIS2 resource name.")],
    attribute: Annotated[str, typer.Argument(help="Attribute UID or business code.")],
    value: Annotated[str, typer.Argument(help="Attribute value to match exactly.")],
    extra_filter: Annotated[
        list[str] | None,
        typer.Option(
            "--filter",
            help=("Extra DHIS2 filter constraints to narrow the search (e.g. `domainType:eq:AGGREGATE`). Repeatable."),
        ),
    ] = None,
) -> None:
    """Reverse lookup across any resource — list every UID whose attribute value matches.

    Returns UIDs only (one per line) to keep the helper generic across
    resource types. Pipe into `dhis2 metadata get <resource> <uid>` or
    `dhis2 metadata list <resource> --filter id:in:[...]` for typed
    follow-ups.
    """
    uids = asyncio.run(
        service.find_resources_by_attribute(
            profile_from_env(),
            resource=resource,
            attribute_code_or_uid=attribute,
            value=value,
            extra_filters=extra_filter,
        )
    )
    if not uids:
        typer.secho(
            f"no {resource} with {attribute}={value!r}",
            err=True,
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(1)
    for uid in uids:
        typer.echo(uid)


# ---------------------------------------------------------------------------
# `dhis2 metadata program-rule ...` — tracker business-logic workflows
# ---------------------------------------------------------------------------


@program_rule_app.command("list")
@program_rule_app.command("ls", hidden=True)
def program_rule_list_command(
    program_uid: Annotated[
        str | None,
        typer.Option("--program", help="Program UID; omit to list every rule on the instance."),
    ] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON.")] = False,
) -> None:
    """List every ProgramRule (optionally scoped to one program), sorted by priority."""
    rules = asyncio.run(service.list_program_rules(profile_from_env(), program_uid=program_uid))
    if as_json:
        typer.echo("[" + ",".join(r.model_dump_json(exclude_none=True) for r in rules) + "]")
        return
    if not rules:
        typer.echo("no program rules")
        return
    title = f"program rules ({len(rules)})"
    if program_uid is not None:
        title += f" — program {program_uid}"
    table = Table(title=title)
    table.add_column("priority", justify="right", style="dim")
    table.add_column("uid", style="cyan", no_wrap=True)
    table.add_column("name", overflow="fold")
    table.add_column("condition", overflow="fold")
    table.add_column("actions", justify="right")
    for rule in rules:
        actions = rule.programRuleActions or []
        table.add_row(
            str(rule.priority if rule.priority is not None else "-"),
            rule.id or "-",
            rule.name or "-",
            rule.condition or "-",
            str(len(actions)),
        )
    _console.print(table)


@program_rule_app.command("show")
def program_rule_show_command(
    rule_uid: Annotated[str, typer.Argument(help="ProgramRule UID.")],
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON.")] = False,
) -> None:
    """Show one ProgramRule with its condition, priority, and every action."""
    rule = asyncio.run(service.show_program_rule(profile_from_env(), rule_uid))
    if as_json:
        typer.echo(rule.model_dump_json(indent=2, exclude_none=True))
        return
    _console.print(
        f"[bold]{rule.name or '-'}[/bold]  "
        f"uid=[dim]{rule.id or '-'}[/dim]  "
        f"priority=[dim]{rule.priority if rule.priority is not None else '-'}[/dim]",
    )
    if rule.description:
        _console.print(f"  {rule.description}")
    _console.print(f"  condition: [cyan]{rule.condition or '-'}[/cyan]")
    actions = rule.programRuleActions or []
    if not actions:
        _console.print("  (no actions)")
        return
    table = Table(title=f"actions ({len(actions)})")
    table.add_column("type", style="cyan")
    table.add_column("target", overflow="fold")
    table.add_column("content / data", overflow="fold")
    for action in actions:
        if isinstance(action, dict):
            action_type = action.get("programRuleActionType") or "-"
            de_id = (action.get("dataElement") or {}).get("id") if isinstance(action.get("dataElement"), dict) else None
            tea_id = (action.get("attribute") or {}).get("id") if isinstance(action.get("attribute"), dict) else None
            content = action.get("content") or action.get("data") or "-"
        else:
            extras = getattr(action, "model_extra", None) or {}
            action_type = extras.get("programRuleActionType") or getattr(action, "programRuleActionType", None) or "-"
            de = getattr(action, "dataElement", None)
            de_id = getattr(de, "id", None) if de is not None else None
            attr = extras.get("attribute") if isinstance(extras.get("attribute"), dict) else None
            tea_id = attr.get("id") if attr else None
            content = action.content or action.data or "-"
        target = de_id or tea_id or "-"
        table.add_row(str(action_type), target, str(content))
    _console.print(table)


@program_rule_app.command("vars-for")
def program_rule_vars_for_command(
    program_uid: Annotated[str, typer.Argument(help="Program UID.")],
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON.")] = False,
) -> None:
    """List every `ProgramRuleVariable` in scope for a program, sorted by name."""
    variables = asyncio.run(service.list_program_rule_variables(profile_from_env(), program_uid))
    if as_json:
        typer.echo("[" + ",".join(v.model_dump_json(exclude_none=True) for v in variables) + "]")
        return
    if not variables:
        typer.echo("no program rule variables for this program")
        return
    table = Table(title=f"variables ({len(variables)})")
    table.add_column("name", style="cyan")
    table.add_column("source type", style="dim")
    table.add_column("target", overflow="fold")
    table.add_column("uid", style="dim", no_wrap=True)
    for var in variables:
        extras = getattr(var, "model_extra", None) or {}
        source_type = extras.get("programRuleVariableSourceType") or "-"
        de = getattr(var, "dataElement", None)
        de_id = getattr(de, "id", None) if de is not None else None
        attr = extras.get("trackedEntityAttribute") or extras.get("attribute")
        tea_id = attr.get("id") if isinstance(attr, dict) else None
        target = de_id or tea_id or "-"
        table.add_row(var.name or "-", str(source_type), target, var.id or "-")
    _console.print(table)


@program_rule_app.command("validate-expression")
def program_rule_validate_expression_command(
    expression: Annotated[str, typer.Argument(help="Program-rule condition expression.")],
    context: Annotated[
        str,
        typer.Option(
            "--context",
            help=(
                "Which DHIS2 expression parser to use: program-indicator (default), "
                "validation-rule, indicator, predictor, or generic."
            ),
        ),
    ] = "program-indicator",
) -> None:
    """Parse-check a program-rule condition expression.

    DHIS2 doesn't expose a dedicated program-rule expression validator —
    the closest is the program-indicator parser (used by default here),
    which enforces stricter `#{stage.de}` syntax than program rules
    accept. For the common `#{variableName}` shorthand program rules
    use, the PI validator flags "Invalid Program Stage / DataElement
    syntax" — not a real error, just the parser mismatch. Trust a clean
    OK as definitely valid; read the specific message on ERROR to
    distinguish parser mismatches from real syntax problems.
    """
    result = asyncio.run(
        service.validate_program_rule_expression(profile_from_env(), expression, context=context),
    )
    status_colour = "green" if result.valid else "red"
    _console.print(
        f"[{status_colour}]{result.status or '-'}[/{status_colour}]  message: {result.message or '-'}",
    )
    if result.description:
        _console.print(f"  rendered: {result.description}")
    if not result.valid:
        raise typer.Exit(1)


@program_rule_app.command("where-de-is-used")
def program_rule_where_de_is_used_command(
    data_element_uid: Annotated[str, typer.Argument(help="DataElement UID.")],
) -> None:
    """Impact analysis — list every rule whose actions reference this DataElement.

    Useful before renaming / removing a DE: catches rules that'd stop
    firing once the reference breaks. Exit 1 if nothing matches (safe
    shorthand for `grep -q` pipelines).
    """
    rules = asyncio.run(
        service.program_rules_using_data_element(profile_from_env(), data_element_uid),
    )
    if not rules:
        typer.secho(
            f"no rules reference dataElement {data_element_uid!r}",
            err=True,
            fg=typer.colors.YELLOW,
        )
        raise typer.Exit(1)
    table = Table(title=f"rules referencing {data_element_uid} ({len(rules)})")
    table.add_column("uid", style="cyan", no_wrap=True)
    table.add_column("priority", justify="right", style="dim")
    table.add_column("name", overflow="fold")
    for rule in rules:
        table.add_row(
            rule.id or "-",
            str(rule.priority if rule.priority is not None else "-"),
            rule.name or "-",
        )
    _console.print(table)


def _parse_key_value_pairs(values: list[str] | None, *, flag_name: str) -> dict[str, str]:
    """Split `key:value` CLI flags (repeated) into a flat dict. Raises typer.Exit(2) on malformed input."""
    result: dict[str, str] = {}
    if not values:
        return result
    for entry in values:
        if ":" not in entry:
            typer.secho(
                f"invalid --{flag_name} value {entry!r}: expected key:value",
                err=True,
                fg=typer.colors.RED,
            )
            raise typer.Exit(2)
        key, _, value = entry.partition(":")
        result[key.strip()] = value
    return result


def _render_sql_view_result(result: Any, *, fmt: str) -> None:
    """Render a SqlViewResult to stdout — Rich table, JSON array of dicts, or CSV."""
    import csv as _csv  # noqa: PLC0415
    import io as _io  # noqa: PLC0415

    columns = [column.name for column in result.columns]
    if fmt == "json":
        typer.echo(json.dumps(result.as_dicts(), indent=2, default=str))
        return
    if fmt == "csv":
        buffer = _io.StringIO()
        writer = _csv.writer(buffer)
        writer.writerow(columns)
        for row in result.rows:
            writer.writerow(row)
        typer.echo(buffer.getvalue().rstrip("\n"))
        return
    title = result.title or f"{len(result.rows)} rows"
    table = Table(title=title)
    for name in columns:
        table.add_column(name, overflow="fold")
    for row in result.rows:
        padded = list(row) + [None] * (len(columns) - len(row))
        table.add_row(*[("-" if cell is None else str(cell)) for cell in padded[: len(columns)]])
    _console.print(table)


@sql_view_app.command("list")
@sql_view_app.command("ls", hidden=True)
def sql_view_list_command(
    view_type: Annotated[
        str | None,
        typer.Option("--type", help="Filter by SqlViewType: VIEW, MATERIALIZED_VIEW, or QUERY."),
    ] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON.")] = False,
) -> None:
    """List every SqlView on the instance, sorted by name."""
    views = asyncio.run(service.list_sql_views(profile_from_env(), view_type=view_type))
    if as_json:
        typer.echo("[" + ",".join(v.model_dump_json(exclude_none=True) for v in views) + "]")
        return
    if not views:
        typer.echo("no SQL views")
        return
    title = f"SQL views ({len(views)})"
    if view_type is not None:
        title += f" — type {view_type}"
    table = Table(title=title)
    table.add_column("uid", style="cyan", no_wrap=True)
    table.add_column("name", overflow="fold")
    table.add_column("type", style="dim")
    table.add_column("description", overflow="fold")
    for view in views:
        table.add_row(
            view.id or "-",
            view.name or "-",
            str(view.type) if view.type is not None else "-",
            view.description or "-",
        )
    _console.print(table)


@sql_view_app.command("show")
def sql_view_show_command(
    view_uid: Annotated[str, typer.Argument(help="SqlView UID.")],
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON (includes full sqlQuery).")] = False,
) -> None:
    """Show one SqlView's metadata + its stored SQL body."""
    view = asyncio.run(service.show_sql_view(profile_from_env(), view_uid))
    if as_json:
        typer.echo(view.model_dump_json(indent=2, exclude_none=True))
        return
    _console.print(
        f"[bold]{view.name or '-'}[/bold]  uid=[dim]{view.id or '-'}[/dim]  type=[dim]{view.type or '-'}[/dim]",
    )
    if view.description:
        _console.print(f"  {view.description}")
    if view.sqlQuery:
        _console.print("  [dim]sqlQuery:[/dim]")
        for line in view.sqlQuery.splitlines() or [view.sqlQuery]:
            _console.print(f"    [cyan]{line}[/cyan]")


@sql_view_app.command("execute")
def sql_view_execute_command(
    view_uid: Annotated[str, typer.Argument(help="SqlView UID.")],
    variables: Annotated[
        list[str] | None,
        typer.Option(
            "--var",
            help=(
                "`${name}` substitution for QUERY views, in `name:value` form. Repeatable. "
                "DHIS2 strips non-alphanumeric characters from values server-side — wildcards belong in the SQL."
            ),
        ),
    ] = None,
    criteria: Annotated[
        list[str] | None,
        typer.Option(
            "--criteria",
            help="Column filter for VIEW / MATERIALIZED_VIEW results, in `column:value` form. Repeatable.",
        ),
    ] = None,
    fmt: Annotated[
        str,
        typer.Option("--format", help="Output format: table (default), json, or csv."),
    ] = "table",
) -> None:
    """Run a SqlView and render its rows as a table, JSON array, or CSV."""
    if fmt not in {"table", "json", "csv"}:
        typer.secho(f"unknown --format {fmt!r}: expected table, json, or csv", err=True, fg=typer.colors.RED)
        raise typer.Exit(2)
    var_map = _parse_key_value_pairs(variables, flag_name="var")
    criteria_map = _parse_key_value_pairs(criteria, flag_name="criteria")
    result = asyncio.run(
        service.execute_sql_view(
            profile_from_env(),
            view_uid,
            variables=var_map or None,
            criteria=criteria_map or None,
        ),
    )
    _render_sql_view_result(result, fmt=fmt)


@sql_view_app.command("refresh")
def sql_view_refresh_command(
    view_uid: Annotated[str, typer.Argument(help="SqlView UID.")],
) -> None:
    """Refresh a MATERIALIZED_VIEW or lazily create a VIEW's DB object.

    `POST /api/sqlViews/{uid}/execute` is idempotent for VIEW types — the
    first call creates the Postgres view; subsequent calls are no-ops.
    MATERIALIZED_VIEW types re-run the underlying SQL each call.
    """
    response = asyncio.run(service.refresh_sql_view(profile_from_env(), view_uid))
    render_webmessage(response, as_json=False, action="refreshed")


@sql_view_app.command("adhoc")
def sql_view_adhoc_command(
    name: Annotated[str, typer.Argument(help="Display name for the throwaway view.")],
    sql_path: Annotated[Path, typer.Argument(help=".sql file containing the query body.")],
    view_type: Annotated[
        str,
        typer.Option("--type", help="SqlViewType — QUERY (default), VIEW, or MATERIALIZED_VIEW."),
    ] = "QUERY",
    keep: Annotated[
        bool,
        typer.Option("--keep", help="Leave the view in place afterwards instead of deleting."),
    ] = False,
    variables: Annotated[
        list[str] | None,
        typer.Option("--var", help="`${name}` substitution in `name:value` form. Repeatable."),
    ] = None,
    fmt: Annotated[
        str,
        typer.Option("--format", help="Output format: table (default), json, or csv."),
    ] = "table",
) -> None:
    """Register a throwaway SqlView from a .sql file, execute once, delete it on the way out.

    Designed for iterating on SQL without leaving test metadata behind.
    Subject to DHIS2's SQL allowlist — for fully free-form queries, see
    the Postgres injector example.
    """
    if not sql_path.is_file():
        typer.secho(f"SQL file not found: {sql_path}", err=True, fg=typer.colors.RED)
        raise typer.Exit(2)
    if fmt not in {"table", "json", "csv"}:
        typer.secho(f"unknown --format {fmt!r}: expected table, json, or csv", err=True, fg=typer.colors.RED)
        raise typer.Exit(2)
    sql = sql_path.read_text()
    var_map = _parse_key_value_pairs(variables, flag_name="var")
    result = asyncio.run(
        service.adhoc_sql_view(
            profile_from_env(),
            name,
            sql,
            view_type=view_type,
            keep=keep,
            variables=var_map or None,
        ),
    )
    _render_sql_view_result(result, fmt=fmt)


def _collect_dataDimensionItem_targets(items: Any) -> list[str]:
    """Pull `dataElement.id` out of each dataDimensionItem for display."""
    uids: list[str] = []
    for entry in items or []:
        if isinstance(entry, dict):
            de = entry.get("dataElement")
            if isinstance(de, dict):
                uid = de.get("id")
                if isinstance(uid, str):
                    uids.append(uid)
            continue
        de = getattr(entry, "dataElement", None)
        if de is not None:
            uid = getattr(de, "id", None)
            if isinstance(uid, str):
                uids.append(uid)
    return uids


@viz_app.command("list")
@viz_app.command("ls", hidden=True)
def viz_list_command(
    viz_type: Annotated[
        str | None,
        typer.Option("--type", help="Filter by VisualizationType (LINE / COLUMN / PIVOT_TABLE / SINGLE_VALUE / ...)."),
    ] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON.")] = False,
) -> None:
    """List every Visualization on the instance, sorted by name."""
    vizes = asyncio.run(service.list_visualizations(profile_from_env(), viz_type=viz_type))
    if as_json:
        typer.echo("[" + ",".join(v.model_dump_json(exclude_none=True) for v in vizes) + "]")
        return
    if not vizes:
        typer.echo("no visualizations")
        return
    title = f"visualizations ({len(vizes)})"
    if viz_type is not None:
        title += f" — type {viz_type}"
    table = Table(title=title)
    table.add_column("uid", style="cyan", no_wrap=True)
    table.add_column("name", overflow="fold")
    table.add_column("type", style="dim")
    for viz in vizes:
        table.add_row(viz.id or "-", viz.name or "-", str(viz.type) if viz.type is not None else "-")
    _console.print(table)


@viz_app.command("show")
def viz_show_command(
    viz_uid: Annotated[str, typer.Argument(help="Visualization UID.")],
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON.")] = False,
) -> None:
    """Show one Visualization with axes + data dimensions + period / ou selection."""
    viz = asyncio.run(service.show_visualization(profile_from_env(), viz_uid))
    if as_json:
        typer.echo(viz.model_dump_json(indent=2, exclude_none=True))
        return
    _console.print(
        f"[bold]{viz.name or '-'}[/bold]  uid=[dim]{viz.id or '-'}[/dim]  type=[dim]{viz.type or '-'}[/dim]",
    )
    if viz.description:
        _console.print(f"  {viz.description}")
    rows = viz.rowDimensions or []
    columns = viz.columnDimensions or []
    filters = viz.filterDimensions or []
    _console.print(f"  axes: [cyan]rows={rows}  columns={columns}  filters={filters}[/cyan]")
    de_uids = _collect_dataDimensionItem_targets(viz.dataDimensionItems)
    if de_uids:
        _console.print(f"  data elements: {', '.join(de_uids)}")
    pe_uids = [p.get("id") if isinstance(p, dict) else getattr(p, "id", None) for p in (viz.periods or [])]
    if pe_uids:
        _console.print(f"  periods ({len(pe_uids)}): {', '.join(str(p) for p in pe_uids[:6])}")
    ou_uids = [o.get("id") if isinstance(o, dict) else getattr(o, "id", None) for o in (viz.organisationUnits or [])]
    if ou_uids:
        _console.print(f"  organisation units ({len(ou_uids)}): {', '.join(str(o) for o in ou_uids[:6])}")


@viz_app.command("create")
def viz_create_command(
    name: Annotated[str, typer.Option("--name", help="Display name for the new Visualization.")],
    viz_type: Annotated[
        str,
        typer.Option(
            "--type",
            help="VisualizationType: LINE, COLUMN, STACKED_COLUMN, BAR, PIVOT_TABLE, SINGLE_VALUE, etc.",
        ),
    ],
    data_element: Annotated[
        list[str],
        typer.Option("--de", help="DataElement UID (repeat for multi-DE charts)."),
    ],
    period: Annotated[
        list[str],
        typer.Option("--pe", help="Period ID (e.g. 202401, 2024Q1, 2024). Repeat for multi-period."),
    ],
    org_unit: Annotated[
        list[str],
        typer.Option("--ou", help="OrganisationUnit UID. Repeat for multi-OU."),
    ],
    description: Annotated[str | None, typer.Option("--description", help="Optional long description.")] = None,
    uid: Annotated[
        str | None, typer.Option("--uid", help="Explicit UID (11 chars). Auto-generates when omitted.")
    ] = None,
    category_dimension: Annotated[
        str | None,
        typer.Option("--category-dim", help="Override category axis: dx / pe / ou."),
    ] = None,
    series_dimension: Annotated[
        str | None,
        typer.Option("--series-dim", help="Override series dimension: dx / pe / ou."),
    ] = None,
    filter_dimension: Annotated[
        str | None,
        typer.Option("--filter-dim", help="Override filter dimension: dx / pe / ou."),
    ] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit the created viz as raw JSON.")] = False,
) -> None:
    """Create a Visualization from flags — one command, no hand-rolled JSON.

    Uses `VisualizationSpec` defaults per chart type: LINE / COLUMN / BAR /
    etc. default to rows=[pe] / columns=[ou] / filters=[dx]; PIVOT_TABLE
    defaults to rows=[ou] / columns=[pe] / filters=[dx]; SINGLE_VALUE
    collapses to columns=[dx] / filters=[pe, ou]. Override any slot with
    --category-dim / --series-dim / --filter-dim.
    """
    viz = asyncio.run(
        service.create_visualization(
            profile_from_env(),
            name=name,
            viz_type=viz_type,
            data_elements=data_element,
            periods=period,
            organisation_units=org_unit,
            description=description,
            uid=uid,
            category_dimension=category_dimension,
            series_dimension=series_dimension,
            filter_dimension=filter_dimension,
        ),
    )
    if as_json:
        typer.echo(viz.model_dump_json(indent=2, exclude_none=True))
        return
    _console.print(
        f"[green]created[/green] [cyan]{viz.id}[/cyan]  type=[dim]{viz.type}[/dim]  name={viz.name!r}",
    )
    _console.print(
        f"  axes: rows={viz.rowDimensions}  columns={viz.columnDimensions}  filters={viz.filterDimensions}",
    )


@viz_app.command("clone")
def viz_clone_command(
    source_uid: Annotated[str, typer.Argument(help="Source Visualization UID.")],
    new_name: Annotated[str, typer.Option("--new-name", help="Display name for the cloned Visualization.")],
    new_uid: Annotated[
        str | None,
        typer.Option("--new-uid", help="Explicit UID for the clone (11 chars). Auto-generates when omitted."),
    ] = None,
    new_description: Annotated[
        str | None,
        typer.Option("--new-description", help="Override the source's description on the clone."),
    ] = None,
    as_json: Annotated[bool, typer.Option("--json", help="Emit the clone as raw JSON.")] = False,
) -> None:
    """Clone an existing Visualization with a fresh UID + new name."""
    clone = asyncio.run(
        service.clone_visualization(
            profile_from_env(),
            source_uid,
            new_name=new_name,
            new_uid=new_uid,
            new_description=new_description,
        ),
    )
    if as_json:
        typer.echo(clone.model_dump_json(indent=2, exclude_none=True))
        return
    _console.print(f"[green]cloned[/green] {source_uid} -> [cyan]{clone.id}[/cyan]  name={clone.name!r}")


@viz_app.command("delete")
def viz_delete_command(
    viz_uid: Annotated[str, typer.Argument(help="Visualization UID to delete.")],
    yes: Annotated[bool, typer.Option("--yes", "-y", help="Skip the confirmation prompt.")] = False,
) -> None:
    """Delete a Visualization."""
    if not yes:
        typer.confirm(f"really delete visualization {viz_uid}?", abort=True)
    asyncio.run(service.delete_visualization(profile_from_env(), viz_uid))
    typer.echo(f"deleted visualization {viz_uid}")


@dashboard_app.command("list")
@dashboard_app.command("ls", hidden=True)
def dashboard_list_command(
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON.")] = False,
) -> None:
    """List every Dashboard on the instance, sorted by name."""
    dashboards = asyncio.run(service.list_dashboards(profile_from_env()))
    if as_json:
        typer.echo("[" + ",".join(d.model_dump_json(exclude_none=True) for d in dashboards) + "]")
        return
    if not dashboards:
        typer.echo("no dashboards")
        return
    table = Table(title=f"dashboards ({len(dashboards)})")
    table.add_column("uid", style="cyan", no_wrap=True)
    table.add_column("name", overflow="fold")
    table.add_column("description", overflow="fold")
    for d in dashboards:
        table.add_row(d.id or "-", d.name or "-", d.description or "-")
    _console.print(table)


@dashboard_app.command("show")
def dashboard_show_command(
    dashboard_uid: Annotated[str, typer.Argument(help="Dashboard UID.")],
    as_json: Annotated[bool, typer.Option("--json", help="Emit raw JSON.")] = False,
) -> None:
    """Show one Dashboard with every dashboardItem resolved inline."""
    dashboard = asyncio.run(service.show_dashboard(profile_from_env(), dashboard_uid))
    if as_json:
        typer.echo(dashboard.model_dump_json(indent=2, exclude_none=True))
        return
    _console.print(
        f"[bold]{dashboard.name or '-'}[/bold]  uid=[dim]{dashboard.id or '-'}[/dim]",
    )
    if dashboard.description:
        _console.print(f"  {dashboard.description}")
    items = list(dashboard.dashboardItems or [])
    if not items:
        _console.print("  (no items)")
        return
    table = Table(title=f"items ({len(items)})")
    table.add_column("item uid", style="cyan")
    table.add_column("type", style="dim")
    table.add_column("target", overflow="fold")
    table.add_column("slot (x,y wxh)", style="dim")
    for item in items:
        item_uid = item.id if not isinstance(item, dict) else item.get("id")
        item_type = (item.type if not isinstance(item, dict) else item.get("type")) or "-"
        if isinstance(item, dict):
            viz_ref = item.get("visualization") or {}
            target = viz_ref.get("id") if isinstance(viz_ref, dict) else "-"
        else:
            viz_ref = getattr(item, "visualization", None)
            target = getattr(viz_ref, "id", None) if viz_ref is not None else "-"
        x = (item.x if not isinstance(item, dict) else item.get("x")) or 0
        y = (item.y if not isinstance(item, dict) else item.get("y")) or 0
        w = (item.width if not isinstance(item, dict) else item.get("width")) or 0
        h = (item.height if not isinstance(item, dict) else item.get("height")) or 0
        table.add_row(str(item_uid or "-"), str(item_type), str(target or "-"), f"({x},{y} {w}x{h})")
    _console.print(table)


@dashboard_app.command("add-item")
def dashboard_add_item_command(
    dashboard_uid: Annotated[str, typer.Argument(help="Dashboard UID.")],
    visualization_uid: Annotated[
        str,
        typer.Option("--viz", help="Visualization UID to add as a dashboardItem."),
    ],
    x: Annotated[int | None, typer.Option("--x", help="Grid x coordinate (0-60). Auto-stacks when omitted.")] = None,
    y: Annotated[
        int | None, typer.Option("--y", help="Grid y coordinate. Auto-stacks below existing when omitted.")
    ] = None,
    width: Annotated[int | None, typer.Option("--width", help="Slot width (1-60). Defaults to 60 when auto.")] = None,
    height: Annotated[int | None, typer.Option("--height", help="Slot height. Defaults to 20 when auto.")] = None,
) -> None:
    """Add a Visualization item to a dashboard.

    Omit all of --x / --y / --width / --height to auto-stack below
    existing items (full width). Supply them explicitly when you need
    side-by-side tiling.
    """
    dashboard = asyncio.run(
        service.dashboard_add_item(
            profile_from_env(),
            dashboard_uid,
            visualization_uid,
            x=x,
            y=y,
            width=width,
            height=height,
        ),
    )
    item_count = len(dashboard.dashboardItems or [])
    _console.print(
        f"[green]added[/green] viz [cyan]{visualization_uid}[/cyan] to dashboard {dashboard_uid} "
        f"(now {item_count} items)",
    )


@dashboard_app.command("remove-item")
def dashboard_remove_item_command(
    dashboard_uid: Annotated[str, typer.Argument(help="Dashboard UID.")],
    item_uid: Annotated[str, typer.Argument(help="DashboardItem UID to remove.")],
) -> None:
    """Remove one dashboardItem by its UID."""
    dashboard = asyncio.run(
        service.dashboard_remove_item(profile_from_env(), dashboard_uid, item_uid),
    )
    item_count = len(dashboard.dashboardItems or [])
    _console.print(
        f"[green]removed[/green] item [cyan]{item_uid}[/cyan] from dashboard {dashboard_uid} (now {item_count} items)",
    )
