"""FastMCP tool registration for the `metadata` plugin."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dhis2_client import JsonPatchOpAdapter, WebMessageResponse

from dhis2_core.plugins.metadata import service
from dhis2_core.plugins.metadata.models import MetadataBundle
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

        Returns each item as a JSON-friendly dict (MCP tool return types
        serialise to JSON); the service layer returns the typed generated
        models and this wrapper dumps them at the edge.

        `profile` selects a named profile; omit for the default.
        """
        models = await service.list_metadata(
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
        return [_dump_model(model) for model in models]

    @mcp.tool()
    async def metadata_get(
        resource: str,
        uid: str,
        fields: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Fetch one metadata object by UID from the named resource."""
        model = await service.get_metadata(resolve_profile(profile), resource, uid, fields=fields)
        return _dump_model(model)

    @mcp.tool()
    async def metadata_export(
        resources: list[str] | None = None,
        fields: str | None = ":owner",
        per_resource_filters: dict[str, list[str]] | None = None,
        per_resource_fields: dict[str, str] | None = None,
        skip_sharing: bool = False,
        skip_translation: bool = False,
        skip_validation: bool = False,
        check_references: bool = True,
        output_path: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Download a metadata bundle from `GET /api/metadata`.

        `resources` limits the export to specific types (e.g. `["dataElements",
        "indicators"]`); omit for every type DHIS2 exports by default. `fields`
        defaults to `":owner"` for a lossless round-trip; use `:identifiable`
        / `:all` / a custom selector to narrow.

        `per_resource_filters` narrows an export to a subset of each resource
        using DHIS2's `?<resource>:filter=<expr>` wire format. Key is the
        resource name, value is a list of `property:operator:value` filter
        strings (same DSL as `metadata_list`'s `filters`).

        `per_resource_fields` overrides the global `fields` selector
        per-resource (`?<resource>:fields=<selector>`).

        When `output_path` is provided the bundle is written to disk as JSON
        and the tool returns a summary (per-resource counts + optional
        `dangling_references`) to avoid shipping megabytes through MCP.
        Omit `output_path` to receive the full bundle inline.

        `check_references=True` (default) walks the exported bundle and
        includes a `dangling_references` block when references point at
        UIDs not in the bundle — helps the agent decide whether to widen
        the export before committing.
        """
        bundle = await service.export_metadata(
            resolve_profile(profile),
            resources=resources,
            fields=fields,
            skip_sharing=skip_sharing,
            skip_translation=skip_translation,
            skip_validation=skip_validation,
            per_resource_filters=per_resource_filters,
            per_resource_fields=per_resource_fields,
        )
        dangling: dict[str, Any] | None = None
        if check_references:
            dangling = service.bundle_dangling_references(bundle).model_dump(exclude_none=True)
        if output_path is not None:
            Path(output_path).write_text(
                bundle.model_dump_json(indent=2, exclude_none=True, by_alias=True),
                encoding="utf-8",
            )
            summary: dict[str, Any] = {"_path": output_path, **bundle.summary()}
            if dangling is not None:
                summary["dangling_references"] = dangling
            return summary
        wire = bundle.to_wire()
        if dangling is not None:
            wire = {**wire, "_dangling_references": dangling}
        return wire

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
        left_raw = json.loads(Path(left_path).read_text(encoding="utf-8"))
        if not isinstance(left_raw, dict):
            raise TypeError(f"{left_path} must contain a bundle object")
        left_bundle = MetadataBundle.from_raw(left_raw)
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
            right_raw = json.loads(Path(right_path).read_text(encoding="utf-8"))
            if not isinstance(right_raw, dict):
                raise TypeError(f"{right_path} must contain a bundle object")
            right_bundle = MetadataBundle.from_raw(right_raw)
            diff = service.diff_bundles(
                left_bundle,
                right_bundle,
                left_label=left_path,
                right_label=right_path,
                ignored_fields=ignored,
            )
        return diff.model_dump(exclude_none=True)

    @mcp.tool()
    async def metadata_diff_profiles(
        profile_a: str,
        profile_b: str,
        resources: list[str],
        per_resource_filters: dict[str, list[str]] | None = None,
        fields: str = ":owner",
        ignore_fields: list[str] | None = None,
    ) -> dict[str, Any]:
        """Diff a narrow metadata slice between two registered profiles.

        Staging-vs-prod drift monitoring — exports `resources` from both
        profiles concurrently, optionally narrows each resource with
        `per_resource_filters` (e.g. `{"dataElements": ["name:like:ANC"]}`),
        then structurally compares the two bundles. `ignore_fields` extends
        DHIS2's per-instance noise defaults so timestamps and `createdBy`
        blocks don't dominate the drift count.

        `resources` is required — a whole-instance diff is almost always
        noise (user accounts, org-unit assignments, incidental settings
        always diverge between environments). Pick a narrow slice +
        filters + an extended ignore list instead.
        """
        ignored = frozenset({*service._DEFAULT_IGNORED_FIELDS, *(ignore_fields or ())})  # noqa: SLF001
        diff = await service.diff_profiles(
            resolve_profile(profile_a),
            resolve_profile(profile_b),
            resources=resources,
            left_label=profile_a,
            right_label=profile_b,
            fields=fields,
            per_resource_filters=per_resource_filters,
            ignored_fields=ignored,
        )
        return diff.model_dump(exclude_none=True)

    @mcp.tool()
    async def metadata_patch(
        resource: str,
        uid: str,
        ops: list[dict[str, Any]],
        profile: str | None = None,
    ) -> WebMessageResponse:
        """Apply an RFC 6902 JSON Patch to a metadata object.

        `ops` is a list of `{op, path, value?, from?}` dicts. Every standard
        RFC 6902 op is accepted (`add`, `remove`, `replace`, `test`, `move`,
        `copy`); the adapter picks the right variant by the `op` tag. Returns
        the typed `WebMessageResponse` envelope.
        """
        typed_ops = [JsonPatchOpAdapter.validate_python(op) for op in ops]
        return await service.patch_metadata(resolve_profile(profile), resource, uid, typed_ops)

    @mcp.tool()
    async def metadata_import(
        bundle_path: str | None = None,
        bundle_inline: dict[str, Any] | None = None,
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
        keeps the MCP payload small) OR `bundle_inline` for an inline JSON
        object. Exactly one of the two must be provided.

        `dry_run=True` maps to DHIS2's `importMode=VALIDATE` — the server runs
        validation + preheat without committing anything, so callers can
        pre-check a bundle before a real import. Returns the
        `WebMessageResponse` with full import report (stats, conflicts,
        error reports).
        """
        if (bundle_path is None) == (bundle_inline is None):
            raise ValueError("metadata_import requires exactly one of `bundle_path` or `bundle_inline`")
        if bundle_path is not None:
            loaded = json.loads(Path(bundle_path).read_text(encoding="utf-8"))
            if not isinstance(loaded, dict):
                raise TypeError(f"{bundle_path} must contain a bundle object (got {type(loaded).__name__})")
            raw = loaded
        else:
            assert bundle_inline is not None  # the exactly-one check guarantees this
            raw = bundle_inline
        bundle = MetadataBundle.from_raw(raw)
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

    @mcp.tool()
    async def metadata_options_show(uid_or_code: str, profile: str | None = None) -> dict[str, Any] | None:
        """Fetch one OptionSet (with options inline) by UID or business code.

        `uid_or_code` accepts either the 11-char DHIS2 UID or the
        OptionSet's business `code`. Returns None if nothing matches.
        """
        result = await service.show_option_set(resolve_profile(profile), uid_or_code)
        return _dump_model(result) if result is not None else None

    @mcp.tool()
    async def metadata_options_find(
        set_ref: str,
        option_code: str | None = None,
        option_name: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any] | None:
        """Locate one option in a set by `option_code` or `option_name`.

        Exactly one of `option_code` / `option_name` must be provided.
        `set_ref` accepts a UID or the OptionSet's business code. Returns
        None on miss.
        """
        result = await service.find_option_in_set(
            resolve_profile(profile),
            option_set_uid_or_code=set_ref,
            option_code=option_code,
            option_name=option_name,
        )
        return _dump_model(result) if result is not None else None

    @mcp.tool()
    async def metadata_options_sync(
        set_ref: str,
        spec: list[dict[str, Any]],
        *,
        remove_missing: bool = False,
        dry_run: bool = False,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Idempotent bulk sync — reconcile an OptionSet against a spec.

        `spec` is a list of `{code, name, sort_order?}` dicts. Returns a
        typed `UpsertReport` as a JSON-friendly dict: codes grouped into
        `added` / `updated` / `removed` / `skipped`.

        `remove_missing=True` also deletes options whose code isn't in
        the spec. `dry_run=True` previews without writing.
        """
        from dhis2_client import OptionSpec  # noqa: PLC0415 — keep import local to the tool body

        validated = [OptionSpec.model_validate(entry) for entry in spec]
        report = await service.sync_option_set(
            resolve_profile(profile),
            option_set_uid_or_code=set_ref,
            spec=validated,
            remove_missing=remove_missing,
            dry_run=dry_run,
        )
        return _dump_model(report)


def _dump_model(model: Any) -> dict[str, Any]:
    """Edge-of-world dump: typed pydantic model -> JSON-friendly dict for MCP tool return."""
    if hasattr(model, "model_dump"):
        dumped = model.model_dump(by_alias=True, exclude_none=True, mode="json")
        if isinstance(dumped, dict):
            return dumped
    if isinstance(model, dict):
        return model
    raise TypeError(f"cannot dump {type(model).__name__} for MCP return")
