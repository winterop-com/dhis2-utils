"""FastMCP tool registration for the `metadata` plugin."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dhis2_client import WebMessageResponse

from dhis2_core.plugins.metadata import service
from dhis2_core.profile import resolve_profile


def register(mcp: Any) -> None:
    """Register `metadata_type_list`, `metadata_list`, `metadata_get` as MCP tools."""

    @mcp.tool()
    async def metadata_type_list(profile: str | None = None) -> list[str]:
        """List every metadata resource type the connected DHIS2 instance exposes.

        Pass `profile` to target a named profile; omit to use the default.
        """
        return await service.list_resource_types(resolve_profile(profile))

    @mcp.tool()
    async def metadata_list(
        resource: str,
        fields: str = "id,name",
        filters: list[str] | None = None,
        root_junction: str | None = None,
        order: list[str] | None = None,
        page: int | None = None,
        page_size: int | None = None,
        paging: bool | None = None,
        translate: bool | None = None,
        locale: str | None = None,
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """List instances of a metadata resource (e.g. `dataElements`, `indicators`).

        Every DHIS2 `/api/<resource>` query parameter is exposed:

        - `fields`: DHIS2 selector. Supports plain lists (`id,name`), presets
          (`:identifiable`, `:nameable`, `:owner`, `:all`), exclusions
          (`:all,!lastUpdated`), and nested selectors (`children[id,name]`).
        - `filters`: list of `property:operator:value` strings. Multiple filters
          default to AND; pass `root_junction="OR"` to OR them.
        - `order`: list of `property:asc|desc` clauses (later ones tie-break).
        - `page` + `page_size`: server-side pagination.
        - `paging=False`: return every row in one response.
        - `translate` + `locale`: return localised fields.

        `profile` selects a named profile; omit for the default.
        """
        return await service.list_metadata(
            resolve_profile(profile),
            resource,
            fields=fields,
            filters=filters,
            root_junction=root_junction,
            order=order,
            page=page,
            page_size=page_size,
            paging=paging,
            translate=translate,
            locale=locale,
        )

    @mcp.tool()
    async def metadata_get(
        resource: str,
        uid: str,
        fields: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Fetch one metadata object by UID from the named resource."""
        return await service.get_metadata(resolve_profile(profile), resource, uid, fields=fields)

    @mcp.tool()
    async def metadata_export(
        resources: list[str] | None = None,
        fields: str | None = ":owner",
        skip_sharing: bool = False,
        skip_translation: bool = False,
        skip_validation: bool = False,
        output_path: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Download a metadata bundle from `GET /api/metadata`.

        `resources` limits the export to specific types (e.g. `["dataElements",
        "indicators"]`); omit for every type DHIS2 exports by default. `fields`
        defaults to `":owner"` for a lossless round-trip; use `:identifiable`
        / `:all` / a custom selector to narrow.

        When `output_path` is provided the bundle is also written to disk as
        JSON; the tool return value is always the bundle (full content when no
        path, a summary map with `_path` when written to disk to avoid
        shipping megabytes through the MCP channel).
        """
        bundle = await service.export_metadata(
            resolve_profile(profile),
            resources=resources,
            fields=fields,
            skip_sharing=skip_sharing,
            skip_translation=skip_translation,
            skip_validation=skip_validation,
        )
        if output_path is not None:
            Path(output_path).write_text(json.dumps(bundle, indent=2), encoding="utf-8")
            summary: dict[str, Any] = {"_path": output_path, **service.summarise_bundle(bundle)}
            return summary
        return bundle

    @mcp.tool()
    async def metadata_diff(
        left_path: str,
        right_path: str | None = None,
        live: bool = False,
        ignore_fields: list[str] | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Structurally compare two metadata bundles (or one bundle vs the live instance).

        Pass `left_path` + `right_path` to diff two files on disk. Pass
        `left_path` + `live=True` (omit `right_path`) to diff the file against
        the live DHIS2 instance — only the resource types present in the
        left bundle are exported, so this stays fast on full catalogs.

        Returns the `MetadataDiff` as a dict with per-resource create / update /
        delete / unchanged counts and `ObjectChange` entries carrying UIDs,
        names, and the `changed_fields` list. `ignore_fields` extends DHIS2's
        per-instance noise defaults (lastUpdated, createdBy, access, ...).
        """
        left_bundle = json.loads(Path(left_path).read_text(encoding="utf-8"))
        if not isinstance(left_bundle, dict):
            raise TypeError(f"{left_path} must contain a bundle object")
        ignored = frozenset({*service._DEFAULT_IGNORED_FIELDS, *(ignore_fields or ())})  # noqa: SLF001
        if live == (right_path is not None):
            raise ValueError("metadata_diff requires exactly one of `right_path` or `live=True`")
        if live:
            diff = await service.diff_bundle_against_instance(
                resolve_profile(profile),
                left_bundle,
                bundle_label=left_path,
                ignored_fields=ignored,
            )
        else:
            assert right_path is not None
            right_bundle = json.loads(Path(right_path).read_text(encoding="utf-8"))
            if not isinstance(right_bundle, dict):
                raise TypeError(f"{right_path} must contain a bundle object")
            diff = service.diff_bundles(
                left_bundle,
                right_bundle,
                left_label=left_path,
                right_label=right_path,
                ignored_fields=ignored,
            )
        return diff.model_dump(exclude_none=True)

    @mcp.tool()
    async def metadata_import(
        bundle_path: str | None = None,
        bundle: dict[str, Any] | None = None,
        import_strategy: str = "CREATE_AND_UPDATE",
        atomic_mode: str = "ALL",
        dry_run: bool = False,
        identifier: str = "UID",
        skip_sharing: bool = False,
        skip_translation: bool = False,
        skip_validation: bool = False,
        merge_mode: str | None = None,
        preheat_mode: str | None = None,
        flush_mode: str | None = None,
        profile: str | None = None,
    ) -> WebMessageResponse:
        """Upload a metadata bundle via `POST /api/metadata`.

        Pass `bundle_path` for a file-on-disk (preferred for large bundles —
        keeps the MCP payload small) OR `bundle` for an inline dict. Exactly
        one of the two must be provided.

        `dry_run=True` maps to DHIS2's `importMode=VALIDATE` — the server runs
        validation + preheat without committing anything, so callers can
        pre-check a bundle before a real import. Returns the
        `WebMessageResponse` with full import report (stats, conflicts,
        error reports).
        """
        if (bundle_path is None) == (bundle is None):
            raise ValueError("metadata_import requires exactly one of `bundle_path` or `bundle`")
        if bundle_path is not None:
            loaded = json.loads(Path(bundle_path).read_text(encoding="utf-8"))
            if not isinstance(loaded, dict):
                raise TypeError(f"{bundle_path} must contain a bundle object (got {type(loaded).__name__})")
            bundle = loaded
        assert bundle is not None  # type-narrowing — the exactly-one check above guarantees this
        return await service.import_metadata(
            resolve_profile(profile),
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
