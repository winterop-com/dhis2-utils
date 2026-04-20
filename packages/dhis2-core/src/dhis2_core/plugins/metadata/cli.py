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
