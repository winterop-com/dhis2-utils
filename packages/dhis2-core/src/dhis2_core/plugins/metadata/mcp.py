"""FastMCP tool registration for the `metadata` plugin."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dhis2_client import JsonPatchOpAdapter, LegendSet, WebMessageResponse

from dhis2_core.plugins.metadata import service
from dhis2_core.plugins.metadata.models import MetadataBundle
from dhis2_core.plugins.metadata.service import MergeResult
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
    async def metadata_search(
        query: str,
        page_size: int = 50,
        resource: str | None = None,
        fields: str | None = None,
        exact: bool = False,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Cross-resource text search via `/api/metadata` on id / code / name.

        Three concurrent `/api/metadata?filter=<field>:<op>:<q>` calls (one
        per match axis) merged with UID dedup. `resource` narrows to one
        DHIS2 resource plural (e.g. `dataElements`). `fields` asks DHIS2
        for extra attributes per hit (dumped to `SearchHit.extras`).
        `exact=True` switches from `ilike` to `eq`. Returns a
        `SearchResults` shape: `{query, hits: {resource: [SearchHit, ...]},
        total}`.
        """
        result = await service.search_metadata(
            resolve_profile(profile),
            query,
            page_size=page_size,
            resource=resource,
            fields=fields,
            exact=exact,
        )
        return result.model_dump()

    @mcp.tool()
    async def metadata_usage(
        uid: str,
        page_size: int = 100,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Reverse lookup — find every object that references the given UID.

        Resolves the UID's owning resource via `/api/identifiableObjects/{uid}`,
        then fans out concurrent `/api/<target>?filter=<path>:eq:<uid>` calls
        against every known reference path for that owning type
        (datasets / visualizations / maps / dashboards / program stages /
        etc., depending on the owning resource kind).

        Useful as a deletion-safety probe — any object that references the
        UID surfaces in the result. Empty result means no reference was
        found on any covered path. Returns the same `SearchResults` shape
        as `metadata_search`.
        """
        result = await service.usage_metadata(resolve_profile(profile), uid, page_size=page_size)
        return result.model_dump()

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
    async def metadata_merge(
        source_profile: str,
        target_profile: str,
        resources: list[str],
        per_resource_filters: dict[str, list[str]] | None = None,
        fields: str = ":owner",
        strategy: str = "CREATE_AND_UPDATE",
        atomic: str = "ALL",
        include_sharing: bool = False,
        dry_run: bool = False,
    ) -> MergeResult:
        """Export a metadata slice from one profile and import it into another.

        Pairs with `metadata_diff_profiles` (same resource + filter shape).
        Preview with `diff_profiles`, then apply via `merge`. `resources`
        is required — whole-instance merges overwrite user / role / org-
        unit state operators rarely want synced.

        `dry_run=True` flips target import to `importMode=VALIDATE` —
        DHIS2 walks the bundle + reports conflicts without committing.
        Use to catch cross-instance UID references before the real run.

        `include_sharing=False` (default) strips sharing blocks so
        per-instance user/group UID differences don't cause conflicts.
        """
        return await service.merge_metadata(
            resolve_profile(source_profile),
            resolve_profile(target_profile),
            resources=resources,
            per_resource_filters=per_resource_filters,
            fields=fields,
            import_strategy=strategy,
            atomic_mode=atomic,
            dry_run=dry_run,
            skip_sharing=not include_sharing,
        )

    @mcp.tool()
    async def metadata_legend_set_list(profile: str | None = None) -> list[LegendSet]:
        """List every LegendSet with its `legends` child bands resolved inline."""
        return await service.list_legend_sets(resolve_profile(profile))

    @mcp.tool()
    async def metadata_legend_set_show(uid: str, profile: str | None = None) -> LegendSet:
        """Fetch one LegendSet by UID with its colour bands resolved inline."""
        return await service.show_legend_set(resolve_profile(profile), uid)

    @mcp.tool()
    async def metadata_legend_set_create(
        name: str,
        legends: list[dict[str, Any]],
        code: str | None = None,
        uid: str | None = None,
        profile: str | None = None,
    ) -> LegendSet:
        """Create a LegendSet with ordered colour-range legends.

        Each `legends` entry is a dict with `start` (float), `end` (float),
        `color` (`#RRGGBB` or `#RRGGBBAA`), and optional `name`. `start`
        must be strictly less than `end`. POSTs via `/api/metadata` so
        the LegendSet + its Legends land atomically.
        """
        tuples: list[tuple[float, float, str, str | None]] = []
        for legend in legends:
            start = legend.get("start")
            end = legend.get("end")
            color = legend.get("color")
            if not isinstance(start, int | float) or not isinstance(end, int | float):
                raise ValueError("each legend requires numeric `start` and `end`")
            if not isinstance(color, str):
                raise ValueError("each legend requires a string `color`")
            tuples.append((float(start), float(end), color, legend.get("name")))
        return await service.create_legend_set(
            resolve_profile(profile),
            name=name,
            legends=tuples,
            uid=uid,
            code=code,
        )

    @mcp.tool()
    async def metadata_legend_set_delete(uid: str, profile: str | None = None) -> None:
        """Delete a LegendSet by UID."""
        await service.delete_legend_set(resolve_profile(profile), uid)

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
    async def metadata_options_attribute_get(
        option_uid: str,
        attribute: str,
        profile: str | None = None,
    ) -> str | None:
        """Read one attribute value off an Option; None if unset.

        `attribute` accepts the Attribute's UID or its business code (e.g.
        `SNOMED_CODE`). The code path resolves via
        `/api/attributes?filter=code:eq:...`.
        """
        return await service.get_option_attribute_value(
            resolve_profile(profile),
            option_uid=option_uid,
            attribute_code_or_uid=attribute,
        )

    @mcp.tool()
    async def metadata_options_attribute_set(
        option_uid: str,
        attribute: str,
        value: str,
        profile: str | None = None,
    ) -> None:
        """Set / replace one attribute value on an Option (read-merge-write)."""
        await service.set_option_attribute_value(
            resolve_profile(profile),
            option_uid=option_uid,
            attribute_code_or_uid=attribute,
            value=value,
        )

    @mcp.tool()
    async def metadata_options_attribute_find(
        set_ref: str,
        attribute: str,
        value: str,
        profile: str | None = None,
    ) -> dict[str, Any] | None:
        """Reverse lookup — find the Option in a set whose attribute matches a value.

        Given an external-system code (e.g. SNOMED CT `386661006`),
        returns the DHIS2 Option it maps to. Returns None on miss.
        """
        result = await service.find_option_by_attribute(
            resolve_profile(profile),
            option_set_uid_or_code=set_ref,
            attribute_code_or_uid=attribute,
            value=value,
        )
        return _dump_model(result) if result is not None else None

    @mcp.tool()
    async def metadata_attribute_get(
        resource: str,
        resource_uid: str,
        attribute: str,
        profile: str | None = None,
    ) -> str | None:
        """Read one attribute value off any resource with `attributeValues`.

        `resource` is the plural DHIS2 name (`dataElements`, `options`,
        `organisationUnits`, …). `attribute` accepts a UID or the
        Attribute's business code. None when unset.
        """
        return await service.get_attribute_value(
            resolve_profile(profile),
            resource=resource,
            resource_uid=resource_uid,
            attribute_code_or_uid=attribute,
        )

    @mcp.tool()
    async def metadata_attribute_set(
        resource: str,
        resource_uid: str,
        attribute: str,
        value: str,
        profile: str | None = None,
    ) -> None:
        """Set / replace one attribute value on any resource (read-merge-write)."""
        await service.set_attribute_value(
            resolve_profile(profile),
            resource=resource,
            resource_uid=resource_uid,
            attribute_code_or_uid=attribute,
            value=value,
        )

    @mcp.tool()
    async def metadata_attribute_delete(
        resource: str,
        resource_uid: str,
        attribute: str,
        profile: str | None = None,
    ) -> bool:
        """Remove one attribute value; True if anything was removed, False on no-op."""
        return await service.delete_attribute_value(
            resolve_profile(profile),
            resource=resource,
            resource_uid=resource_uid,
            attribute_code_or_uid=attribute,
        )

    @mcp.tool()
    async def metadata_attribute_find(
        resource: str,
        attribute: str,
        value: str,
        extra_filters: list[str] | None = None,
        profile: str | None = None,
    ) -> list[str]:
        """Reverse lookup — UIDs of every resource whose attribute value matches.

        `extra_filters` passes additional DHIS2 filter constraints through
        (e.g. `["domainType:eq:AGGREGATE"]` to narrow a DataElement lookup,
        `["optionSet.id:eq:OsVaccType1"]` to scope an Option lookup).
        """
        return await service.find_resources_by_attribute(
            resolve_profile(profile),
            resource=resource,
            attribute_code_or_uid=attribute,
            value=value,
            extra_filters=extra_filters,
        )

    @mcp.tool()
    async def metadata_program_rule_list(
        program_uid: str | None = None,
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """List every ProgramRule (optionally scoped to a program), sorted by priority."""
        rules = await service.list_program_rules(resolve_profile(profile), program_uid=program_uid)
        return [_dump_model(rule) for rule in rules]

    @mcp.tool()
    async def metadata_program_rule_show(
        rule_uid: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Show one ProgramRule with actions resolved inline."""
        rule = await service.show_program_rule(resolve_profile(profile), rule_uid)
        return _dump_model(rule)

    @mcp.tool()
    async def metadata_program_rule_vars_for(
        program_uid: str,
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """List every `ProgramRuleVariable` in scope for a program."""
        variables = await service.list_program_rule_variables(resolve_profile(profile), program_uid)
        return [_dump_model(v) for v in variables]

    @mcp.tool()
    async def metadata_program_rule_validate_expression(
        expression: str,
        context: str = "program-indicator",
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Parse-check a program-rule condition expression.

        `context` picks which DHIS2 expression parser runs —
        `program-indicator` (default, matches program-rule grammar),
        `validation-rule`, `indicator`, `predictor`, or `generic`.
        """
        result = await service.validate_program_rule_expression(
            resolve_profile(profile),
            expression,
            context=context,
        )
        return _dump_model(result)

    @mcp.tool()
    async def metadata_program_rule_where_de_is_used(
        data_element_uid: str,
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """Impact analysis — every ProgramRule whose actions reference this DataElement."""
        rules = await service.program_rules_using_data_element(
            resolve_profile(profile),
            data_element_uid,
        )
        return [_dump_model(r) for r in rules]

    @mcp.tool()
    async def metadata_sql_view_list(
        view_type: str | None = None,
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """List every SqlView on the instance (optionally filtered by `view_type`).

        `view_type` accepts `VIEW`, `MATERIALIZED_VIEW`, or `QUERY`.
        """
        views = await service.list_sql_views(resolve_profile(profile), view_type=view_type)
        return [_dump_model(v) for v in views]

    @mcp.tool()
    async def metadata_sql_view_show(
        view_uid: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Show one SqlView with its stored sqlQuery."""
        view = await service.show_sql_view(resolve_profile(profile), view_uid)
        return _dump_model(view)

    @mcp.tool()
    async def metadata_sql_view_execute(
        view_uid: str,
        variables: dict[str, str] | None = None,
        criteria: dict[str, str] | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Execute a SqlView and return its result grid as a JSON-friendly payload.

        `variables` populate `${name}` placeholders on QUERY views —
        DHIS2 strips non-alphanumeric characters from values server-side,
        so wildcards live in the SQL template.

        `criteria` filter the output of VIEW / MATERIALIZED_VIEW runs by
        column value.
        """
        result = await service.execute_sql_view(
            resolve_profile(profile),
            view_uid,
            variables=variables,
            criteria=criteria,
        )
        return _dump_model(result)

    @mcp.tool()
    async def metadata_sql_view_refresh(
        view_uid: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Refresh a MATERIALIZED_VIEW or lazily create a VIEW's DB object."""
        response = await service.refresh_sql_view(resolve_profile(profile), view_uid)
        return _dump_model(response)

    @mcp.tool()
    async def metadata_viz_list(
        viz_type: str | None = None,
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """List every Visualization on the instance (optionally filtered by type).

        `viz_type` accepts any VisualizationType — LINE, COLUMN, BAR,
        STACKED_COLUMN, STACKED_BAR, AREA, PIE, RADAR, PIVOT_TABLE,
        SINGLE_VALUE, etc.
        """
        vizes = await service.list_visualizations(resolve_profile(profile), viz_type=viz_type)
        return [_dump_model(v) for v in vizes]

    @mcp.tool()
    async def metadata_viz_show(
        viz_uid: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Show one Visualization with axes + data dimensions resolved inline."""
        viz = await service.show_visualization(resolve_profile(profile), viz_uid)
        return _dump_model(viz)

    @mcp.tool()
    async def metadata_viz_create(
        name: str,
        viz_type: str,
        data_elements: list[str],
        periods: list[str],
        organisation_units: list[str],
        description: str | None = None,
        uid: str | None = None,
        category_dimension: str | None = None,
        series_dimension: str | None = None,
        filter_dimension: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Create a Visualization from a typed VisualizationSpec.

        `viz_type` is a VisualizationType value (LINE / COLUMN /
        PIVOT_TABLE / SINGLE_VALUE / etc.). Default dimensional
        placement depends on type — LINE and friends default to time
        on the x-axis and OU as series. Override with
        `category_dimension` (x-axis), `series_dimension` (legend
        colours), `filter_dimension`.
        """
        viz = await service.create_visualization(
            resolve_profile(profile),
            name=name,
            viz_type=viz_type,
            data_elements=data_elements,
            periods=periods,
            organisation_units=organisation_units,
            description=description,
            uid=uid,
            category_dimension=category_dimension,
            series_dimension=series_dimension,
            filter_dimension=filter_dimension,
        )
        return _dump_model(viz)

    @mcp.tool()
    async def metadata_viz_clone(
        source_uid: str,
        new_name: str,
        new_uid: str | None = None,
        new_description: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Clone an existing Visualization with a fresh UID + new name."""
        clone = await service.clone_visualization(
            resolve_profile(profile),
            source_uid,
            new_name=new_name,
            new_uid=new_uid,
            new_description=new_description,
        )
        return _dump_model(clone)

    @mcp.tool()
    async def metadata_dashboard_list(profile: str | None = None) -> list[dict[str, Any]]:
        """List every Dashboard on the instance, sorted by name."""
        dashboards = await service.list_dashboards(resolve_profile(profile))
        return [_dump_model(d) for d in dashboards]

    @mcp.tool()
    async def metadata_dashboard_show(
        dashboard_uid: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Show one Dashboard with every dashboardItem resolved inline."""
        dashboard = await service.show_dashboard(resolve_profile(profile), dashboard_uid)
        return _dump_model(dashboard)

    @mcp.tool()
    async def metadata_dashboard_add_item(
        dashboard_uid: str,
        target_uid: str,
        kind: str = "visualization",
        x: int | None = None,
        y: int | None = None,
        width: int | None = None,
        height: int | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Add one metadata-backed item to a dashboard.

        `kind` selects the DashboardItem reference field on DHIS2's
        side: `"visualization"` (default), `"map"`,
        `"eventVisualization"`, `"eventChart"`, `"eventReport"`.

        Omit all of `x` / `y` / `width` / `height` to auto-stack below
        existing items (full width). Supply them explicitly for
        side-by-side tiling.
        """
        dashboard = await service.dashboard_add_item(
            resolve_profile(profile),
            dashboard_uid,
            target_uid,
            kind=kind,
            x=x,
            y=y,
            width=width,
            height=height,
        )
        return _dump_model(dashboard)

    @mcp.tool()
    async def metadata_map_list(profile: str | None = None) -> list[dict[str, Any]]:
        """List every Map on the instance, sorted by name."""
        maps = await service.list_maps(resolve_profile(profile))
        return [_dump_model(m) for m in maps]

    @mcp.tool()
    async def metadata_map_show(
        map_uid: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Show one Map with its viewport + every mapViews layer resolved inline."""
        m = await service.show_map(resolve_profile(profile), map_uid)
        return _dump_model(m)

    @mcp.tool()
    async def metadata_map_create(
        name: str,
        data_elements: list[str],
        periods: list[str],
        organisation_units: list[str],
        organisation_unit_levels: list[int],
        description: str | None = None,
        uid: str | None = None,
        longitude: float = 15.0,
        latitude: float = 0.0,
        zoom: int = 4,
        basemap: str = "openStreetMap",
        classes: int = 5,
        color_low: str = "#fef0d9",
        color_high: str = "#b30000",
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Create a single-layer thematic choropleth Map.

        `organisation_units` is usually the parent boundary (e.g.
        country root); `organisation_unit_levels` picks which
        hierarchy level the choropleth colours (e.g. [2] for
        provinces). Multi-layer maps need raw construction from the
        library side.
        """
        m = await service.create_map(
            resolve_profile(profile),
            name=name,
            data_elements=data_elements,
            periods=periods,
            organisation_units=organisation_units,
            organisation_unit_levels=organisation_unit_levels,
            description=description,
            uid=uid,
            longitude=longitude,
            latitude=latitude,
            zoom=zoom,
            basemap=basemap,
            classes=classes,
            color_low=color_low,
            color_high=color_high,
        )
        return _dump_model(m)

    @mcp.tool()
    async def metadata_map_clone(
        source_uid: str,
        new_name: str,
        new_uid: str | None = None,
        new_description: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Clone an existing Map with a fresh UID + new name."""
        clone = await service.clone_map(
            resolve_profile(profile),
            source_uid,
            new_name=new_name,
            new_uid=new_uid,
            new_description=new_description,
        )
        return _dump_model(clone)

    @mcp.tool()
    async def metadata_data_element_list(
        domain_type: str | None = None,
        page: int = 1,
        page_size: int = 50,
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """Page through DataElements. `domain_type` = `AGGREGATE` or `TRACKER`."""
        rows = await service.list_data_elements(
            resolve_profile(profile),
            domain_type=domain_type,
            page=page,
            page_size=page_size,
        )
        return [_dump_model(row) for row in rows]

    @mcp.tool()
    async def metadata_data_element_show(
        uid: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Fetch one DataElement by UID."""
        return _dump_model(await service.show_data_element(resolve_profile(profile), uid))

    @mcp.tool()
    async def metadata_data_element_create(
        name: str,
        short_name: str,
        value_type: str,
        domain_type: str = "AGGREGATE",
        aggregation_type: str = "SUM",
        category_combo_uid: str | None = None,
        option_set_uid: str | None = None,
        legend_set_uids: list[str] | None = None,
        code: str | None = None,
        form_name: str | None = None,
        description: str | None = None,
        uid: str | None = None,
        zero_is_significant: bool = False,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Create a DataElement. Omit `category_combo_uid` to use the instance default."""
        de = await service.create_data_element(
            resolve_profile(profile),
            name=name,
            short_name=short_name,
            value_type=value_type,
            domain_type=domain_type,
            aggregation_type=aggregation_type,
            category_combo_uid=category_combo_uid,
            option_set_uid=option_set_uid,
            legend_set_uids=legend_set_uids,
            code=code,
            form_name=form_name,
            description=description,
            uid=uid,
            zero_is_significant=zero_is_significant,
        )
        return _dump_model(de)

    @mcp.tool()
    async def metadata_data_element_rename(
        uid: str,
        name: str | None = None,
        short_name: str | None = None,
        form_name: str | None = None,
        description: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Partial-update the label fields on a DataElement."""
        de = await service.rename_data_element(
            resolve_profile(profile),
            uid,
            name=name,
            short_name=short_name,
            form_name=form_name,
            description=description,
        )
        return _dump_model(de)

    @mcp.tool()
    async def metadata_data_element_set_legend_sets(
        uid: str,
        legend_set_uids: list[str],
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Replace the legend-set refs on a DataElement (empty list clears)."""
        de = await service.set_data_element_legend_sets(
            resolve_profile(profile),
            uid,
            legend_set_uids=legend_set_uids,
        )
        return _dump_model(de)

    @mcp.tool()
    async def metadata_data_element_delete(
        uid: str,
        profile: str | None = None,
    ) -> None:
        """Delete a DataElement — DHIS2 rejects deletes on DEs with saved values."""
        await service.delete_data_element(resolve_profile(profile), uid)

    @mcp.tool()
    async def metadata_data_element_group_list(
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """List every DataElementGroup."""
        groups = await service.list_data_element_groups(resolve_profile(profile))
        return [_dump_model(g) for g in groups]

    @mcp.tool()
    async def metadata_data_element_group_show(
        uid: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Fetch one DataElementGroup with member + group-set refs inline."""
        return _dump_model(await service.show_data_element_group(resolve_profile(profile), uid))

    @mcp.tool()
    async def metadata_data_element_group_members(
        uid: str,
        page: int = 1,
        page_size: int = 50,
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """Page through DataElements in a group."""
        members = await service.list_data_element_group_members(
            resolve_profile(profile),
            uid,
            page=page,
            page_size=page_size,
        )
        return [_dump_model(m) for m in members]

    @mcp.tool()
    async def metadata_data_element_group_create(
        name: str,
        short_name: str,
        uid: str | None = None,
        code: str | None = None,
        description: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Create an empty DataElementGroup."""
        group = await service.create_data_element_group(
            resolve_profile(profile),
            name=name,
            short_name=short_name,
            uid=uid,
            code=code,
            description=description,
        )
        return _dump_model(group)

    @mcp.tool()
    async def metadata_data_element_group_add_members(
        uid: str,
        data_element_uids: list[str],
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Add DataElements to a group via the per-item POST shortcut."""
        group = await service.add_data_element_group_members(
            resolve_profile(profile),
            uid,
            data_element_uids=data_element_uids,
        )
        return _dump_model(group)

    @mcp.tool()
    async def metadata_data_element_group_remove_members(
        uid: str,
        data_element_uids: list[str],
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Drop DataElements from a group via the per-item DELETE shortcut."""
        group = await service.remove_data_element_group_members(
            resolve_profile(profile),
            uid,
            data_element_uids=data_element_uids,
        )
        return _dump_model(group)

    @mcp.tool()
    async def metadata_data_element_group_delete(
        uid: str,
        profile: str | None = None,
    ) -> None:
        """Delete a DataElementGroup — members stay."""
        await service.delete_data_element_group(resolve_profile(profile), uid)

    @mcp.tool()
    async def metadata_data_element_group_set_list(
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """List every DataElementGroupSet."""
        group_sets = await service.list_data_element_group_sets(resolve_profile(profile))
        return [_dump_model(gs) for gs in group_sets]

    @mcp.tool()
    async def metadata_data_element_group_set_show(
        uid: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Fetch one DataElementGroupSet by UID."""
        return _dump_model(await service.show_data_element_group_set(resolve_profile(profile), uid))

    @mcp.tool()
    async def metadata_data_element_group_set_create(
        name: str,
        short_name: str,
        uid: str | None = None,
        code: str | None = None,
        description: str | None = None,
        compulsory: bool = False,
        data_dimension: bool = True,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Create an empty DataElementGroupSet."""
        gs = await service.create_data_element_group_set(
            resolve_profile(profile),
            name=name,
            short_name=short_name,
            uid=uid,
            code=code,
            description=description,
            compulsory=compulsory,
            data_dimension=data_dimension,
        )
        return _dump_model(gs)

    @mcp.tool()
    async def metadata_data_element_group_set_add_groups(
        uid: str,
        group_uids: list[str],
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Add groups to a group set via the per-item POST shortcut."""
        gs = await service.add_data_element_group_set_groups(
            resolve_profile(profile),
            uid,
            group_uids=group_uids,
        )
        return _dump_model(gs)

    @mcp.tool()
    async def metadata_data_element_group_set_remove_groups(
        uid: str,
        group_uids: list[str],
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Drop groups from a group set via the per-item DELETE shortcut."""
        gs = await service.remove_data_element_group_set_groups(
            resolve_profile(profile),
            uid,
            group_uids=group_uids,
        )
        return _dump_model(gs)

    @mcp.tool()
    async def metadata_data_element_group_set_delete(
        uid: str,
        profile: str | None = None,
    ) -> None:
        """Delete a DataElementGroupSet — groups stay."""
        await service.delete_data_element_group_set(resolve_profile(profile), uid)

    @mcp.tool()
    async def metadata_indicator_list(
        page: int = 1,
        page_size: int = 50,
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """Page through Indicators."""
        rows = await service.list_indicators(resolve_profile(profile), page=page, page_size=page_size)
        return [_dump_model(row) for row in rows]

    @mcp.tool()
    async def metadata_indicator_show(
        uid: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Fetch one Indicator by UID."""
        return _dump_model(await service.show_indicator(resolve_profile(profile), uid))

    @mcp.tool()
    async def metadata_indicator_create(
        name: str,
        short_name: str,
        indicator_type_uid: str,
        numerator: str,
        denominator: str,
        numerator_description: str | None = None,
        denominator_description: str | None = None,
        legend_set_uids: list[str] | None = None,
        annualized: bool = False,
        decimals: int | None = None,
        code: str | None = None,
        description: str | None = None,
        uid: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Create an Indicator from numerator / denominator expressions."""
        ind = await service.create_indicator(
            resolve_profile(profile),
            name=name,
            short_name=short_name,
            indicator_type_uid=indicator_type_uid,
            numerator=numerator,
            denominator=denominator,
            numerator_description=numerator_description,
            denominator_description=denominator_description,
            legend_set_uids=legend_set_uids,
            annualized=annualized,
            decimals=decimals,
            code=code,
            description=description,
            uid=uid,
        )
        return _dump_model(ind)

    @mcp.tool()
    async def metadata_indicator_rename(
        uid: str,
        name: str | None = None,
        short_name: str | None = None,
        description: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Partial-update the label fields on an Indicator."""
        ind = await service.rename_indicator(
            resolve_profile(profile),
            uid,
            name=name,
            short_name=short_name,
            description=description,
        )
        return _dump_model(ind)

    @mcp.tool()
    async def metadata_indicator_validate_expression(
        expression: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Parse-check one numerator / denominator expression via DHIS2's validator."""
        desc = await service.validate_indicator_expression(resolve_profile(profile), expression)
        return _dump_model(desc)

    @mcp.tool()
    async def metadata_indicator_set_legend_sets(
        uid: str,
        legend_set_uids: list[str],
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Replace the legend-set refs on an Indicator."""
        ind = await service.set_indicator_legend_sets(
            resolve_profile(profile),
            uid,
            legend_set_uids=legend_set_uids,
        )
        return _dump_model(ind)

    @mcp.tool()
    async def metadata_indicator_delete(
        uid: str,
        profile: str | None = None,
    ) -> None:
        """Delete an Indicator."""
        await service.delete_indicator(resolve_profile(profile), uid)

    @mcp.tool()
    async def metadata_indicator_group_list(
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """List every IndicatorGroup."""
        groups = await service.list_indicator_groups(resolve_profile(profile))
        return [_dump_model(g) for g in groups]

    @mcp.tool()
    async def metadata_indicator_group_show(
        uid: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Fetch one IndicatorGroup with member + group-set refs."""
        return _dump_model(await service.show_indicator_group(resolve_profile(profile), uid))

    @mcp.tool()
    async def metadata_indicator_group_members(
        uid: str,
        page: int = 1,
        page_size: int = 50,
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """Page through Indicators in a group."""
        members = await service.list_indicator_group_members(
            resolve_profile(profile),
            uid,
            page=page,
            page_size=page_size,
        )
        return [_dump_model(m) for m in members]

    @mcp.tool()
    async def metadata_indicator_group_create(
        name: str,
        short_name: str,
        uid: str | None = None,
        code: str | None = None,
        description: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Create an empty IndicatorGroup."""
        group = await service.create_indicator_group(
            resolve_profile(profile),
            name=name,
            short_name=short_name,
            uid=uid,
            code=code,
            description=description,
        )
        return _dump_model(group)

    @mcp.tool()
    async def metadata_indicator_group_add_members(
        uid: str,
        indicator_uids: list[str],
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Add Indicators to a group via the per-item POST shortcut."""
        group = await service.add_indicator_group_members(
            resolve_profile(profile),
            uid,
            indicator_uids=indicator_uids,
        )
        return _dump_model(group)

    @mcp.tool()
    async def metadata_indicator_group_remove_members(
        uid: str,
        indicator_uids: list[str],
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Drop Indicators from a group via the per-item DELETE shortcut."""
        group = await service.remove_indicator_group_members(
            resolve_profile(profile),
            uid,
            indicator_uids=indicator_uids,
        )
        return _dump_model(group)

    @mcp.tool()
    async def metadata_indicator_group_delete(
        uid: str,
        profile: str | None = None,
    ) -> None:
        """Delete an IndicatorGroup — members stay."""
        await service.delete_indicator_group(resolve_profile(profile), uid)

    @mcp.tool()
    async def metadata_indicator_group_set_list(
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """List every IndicatorGroupSet."""
        group_sets = await service.list_indicator_group_sets(resolve_profile(profile))
        return [_dump_model(gs) for gs in group_sets]

    @mcp.tool()
    async def metadata_indicator_group_set_show(
        uid: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Fetch one IndicatorGroupSet by UID."""
        return _dump_model(await service.show_indicator_group_set(resolve_profile(profile), uid))

    @mcp.tool()
    async def metadata_indicator_group_set_create(
        name: str,
        short_name: str,
        uid: str | None = None,
        code: str | None = None,
        description: str | None = None,
        compulsory: bool = False,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Create an empty IndicatorGroupSet."""
        gs = await service.create_indicator_group_set(
            resolve_profile(profile),
            name=name,
            short_name=short_name,
            uid=uid,
            code=code,
            description=description,
            compulsory=compulsory,
        )
        return _dump_model(gs)

    @mcp.tool()
    async def metadata_indicator_group_set_add_groups(
        uid: str,
        group_uids: list[str],
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Add groups to an IndicatorGroupSet via the per-item POST shortcut."""
        gs = await service.add_indicator_group_set_groups(
            resolve_profile(profile),
            uid,
            group_uids=group_uids,
        )
        return _dump_model(gs)

    @mcp.tool()
    async def metadata_indicator_group_set_remove_groups(
        uid: str,
        group_uids: list[str],
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Drop groups from an IndicatorGroupSet via the per-item DELETE shortcut."""
        gs = await service.remove_indicator_group_set_groups(
            resolve_profile(profile),
            uid,
            group_uids=group_uids,
        )
        return _dump_model(gs)

    @mcp.tool()
    async def metadata_indicator_group_set_delete(
        uid: str,
        profile: str | None = None,
    ) -> None:
        """Delete an IndicatorGroupSet — groups stay."""
        await service.delete_indicator_group_set(resolve_profile(profile), uid)

    @mcp.tool()
    async def metadata_program_indicator_list(
        program_uid: str | None = None,
        page: int = 1,
        page_size: int = 50,
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """Page through ProgramIndicators, optionally scoped to one program."""
        rows = await service.list_program_indicators(
            resolve_profile(profile),
            program_uid=program_uid,
            page=page,
            page_size=page_size,
        )
        return [_dump_model(pi) for pi in rows]

    @mcp.tool()
    async def metadata_program_indicator_show(
        uid: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Fetch one ProgramIndicator by UID."""
        return _dump_model(await service.show_program_indicator(resolve_profile(profile), uid))

    @mcp.tool()
    async def metadata_program_indicator_create(
        name: str,
        short_name: str,
        program_uid: str,
        expression: str,
        analytics_type: str = "EVENT",
        filter_expression: str | None = None,
        description: str | None = None,
        aggregation_type: str | None = None,
        decimals: int | None = None,
        legend_set_uids: list[str] | None = None,
        code: str | None = None,
        uid: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Create a ProgramIndicator for a given program."""
        pi = await service.create_program_indicator(
            resolve_profile(profile),
            name=name,
            short_name=short_name,
            program_uid=program_uid,
            expression=expression,
            analytics_type=analytics_type,
            filter_expression=filter_expression,
            description=description,
            aggregation_type=aggregation_type,
            decimals=decimals,
            legend_set_uids=legend_set_uids,
            code=code,
            uid=uid,
        )
        return _dump_model(pi)

    @mcp.tool()
    async def metadata_program_indicator_rename(
        uid: str,
        name: str | None = None,
        short_name: str | None = None,
        description: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Partial-update the label fields on a ProgramIndicator."""
        pi = await service.rename_program_indicator(
            resolve_profile(profile),
            uid,
            name=name,
            short_name=short_name,
            description=description,
        )
        return _dump_model(pi)

    @mcp.tool()
    async def metadata_program_indicator_validate_expression(
        expression: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Parse-check one program-indicator expression via DHIS2's validator."""
        desc = await service.validate_program_indicator_expression(resolve_profile(profile), expression)
        return _dump_model(desc)

    @mcp.tool()
    async def metadata_program_indicator_set_legend_sets(
        uid: str,
        legend_set_uids: list[str],
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Replace the legend-set refs on a ProgramIndicator."""
        pi = await service.set_program_indicator_legend_sets(
            resolve_profile(profile),
            uid,
            legend_set_uids=legend_set_uids,
        )
        return _dump_model(pi)

    @mcp.tool()
    async def metadata_program_indicator_delete(
        uid: str,
        profile: str | None = None,
    ) -> None:
        """Delete a ProgramIndicator."""
        await service.delete_program_indicator(resolve_profile(profile), uid)

    @mcp.tool()
    async def metadata_program_indicator_group_list(
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """List every ProgramIndicatorGroup."""
        groups = await service.list_program_indicator_groups(resolve_profile(profile))
        return [_dump_model(g) for g in groups]

    @mcp.tool()
    async def metadata_program_indicator_group_show(
        uid: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Fetch one ProgramIndicatorGroup with member refs."""
        return _dump_model(await service.show_program_indicator_group(resolve_profile(profile), uid))

    @mcp.tool()
    async def metadata_program_indicator_group_members(
        uid: str,
        page: int = 1,
        page_size: int = 50,
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """Page through ProgramIndicators in a group."""
        members = await service.list_program_indicator_group_members(
            resolve_profile(profile),
            uid,
            page=page,
            page_size=page_size,
        )
        return [_dump_model(m) for m in members]

    @mcp.tool()
    async def metadata_program_indicator_group_create(
        name: str,
        short_name: str,
        uid: str | None = None,
        code: str | None = None,
        description: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Create an empty ProgramIndicatorGroup."""
        group = await service.create_program_indicator_group(
            resolve_profile(profile),
            name=name,
            short_name=short_name,
            uid=uid,
            code=code,
            description=description,
        )
        return _dump_model(group)

    @mcp.tool()
    async def metadata_program_indicator_group_add_members(
        uid: str,
        program_indicator_uids: list[str],
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Add ProgramIndicators to a group via the per-item POST shortcut."""
        group = await service.add_program_indicator_group_members(
            resolve_profile(profile),
            uid,
            program_indicator_uids=program_indicator_uids,
        )
        return _dump_model(group)

    @mcp.tool()
    async def metadata_program_indicator_group_remove_members(
        uid: str,
        program_indicator_uids: list[str],
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Drop ProgramIndicators from a group via the per-item DELETE shortcut."""
        group = await service.remove_program_indicator_group_members(
            resolve_profile(profile),
            uid,
            program_indicator_uids=program_indicator_uids,
        )
        return _dump_model(group)

    @mcp.tool()
    async def metadata_program_indicator_group_delete(
        uid: str,
        profile: str | None = None,
    ) -> None:
        """Delete a ProgramIndicatorGroup — members stay."""
        await service.delete_program_indicator_group(resolve_profile(profile), uid)

    @mcp.tool()
    async def metadata_organisation_unit_list(
        level: int | None = None,
        page: int = 1,
        page_size: int = 50,
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """Page through OrganisationUnits with parent + hierarchy columns."""
        units = await service.list_organisation_units(
            resolve_profile(profile),
            level=level,
            page=page,
            page_size=page_size,
        )
        return [_dump_model(u) for u in units]

    @mcp.tool()
    async def metadata_organisation_unit_show(
        uid: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Fetch one OrganisationUnit by UID."""
        unit = await service.show_organisation_unit(resolve_profile(profile), uid)
        return _dump_model(unit)

    @mcp.tool()
    async def metadata_organisation_unit_tree(
        root_uid: str,
        max_depth: int = 3,
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """Walk a subtree rooted at `root_uid` at bounded depth."""
        units = await service.tree_organisation_units(
            resolve_profile(profile),
            root_uid=root_uid,
            max_depth=max_depth,
        )
        return [_dump_model(u) for u in units]

    @mcp.tool()
    async def metadata_organisation_unit_create(
        parent_uid: str,
        name: str,
        short_name: str,
        opening_date: str,
        uid: str | None = None,
        code: str | None = None,
        description: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Create a child OU under `parent_uid`. `opening_date` is ISO-8601."""
        unit = await service.create_organisation_unit(
            resolve_profile(profile),
            parent_uid=parent_uid,
            name=name,
            short_name=short_name,
            opening_date=opening_date,
            uid=uid,
            code=code,
            description=description,
        )
        return _dump_model(unit)

    @mcp.tool()
    async def metadata_organisation_unit_move(
        uid: str,
        new_parent_uid: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Reparent an OU. DHIS2 recomputes `path` + `hierarchyLevel` server-side."""
        unit = await service.move_organisation_unit(
            resolve_profile(profile),
            uid=uid,
            new_parent_uid=new_parent_uid,
        )
        return _dump_model(unit)

    @mcp.tool()
    async def metadata_organisation_unit_delete(
        uid: str,
        profile: str | None = None,
    ) -> None:
        """Delete an OU — DHIS2 rejects deletes on units with children or data."""
        await service.delete_organisation_unit(resolve_profile(profile), uid)

    @mcp.tool()
    async def metadata_organisation_unit_group_list(
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """List every OrganisationUnitGroup."""
        groups = await service.list_organisation_unit_groups(resolve_profile(profile))
        return [_dump_model(g) for g in groups]

    @mcp.tool()
    async def metadata_organisation_unit_group_show(
        uid: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Fetch one OrganisationUnitGroup with member + group-set refs inline."""
        group = await service.show_organisation_unit_group(resolve_profile(profile), uid)
        return _dump_model(group)

    @mcp.tool()
    async def metadata_organisation_unit_group_members(
        uid: str,
        page: int = 1,
        page_size: int = 50,
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """Page through OUs that belong to one group."""
        members = await service.list_organisation_unit_group_members(
            resolve_profile(profile),
            uid,
            page=page,
            page_size=page_size,
        )
        return [_dump_model(m) for m in members]

    @mcp.tool()
    async def metadata_organisation_unit_group_create(
        name: str,
        short_name: str,
        uid: str | None = None,
        code: str | None = None,
        description: str | None = None,
        color: str | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Create an empty OrganisationUnitGroup."""
        group = await service.create_organisation_unit_group(
            resolve_profile(profile),
            name=name,
            short_name=short_name,
            uid=uid,
            code=code,
            description=description,
            color=color,
        )
        return _dump_model(group)

    @mcp.tool()
    async def metadata_organisation_unit_group_add_members(
        uid: str,
        ou_uids: list[str],
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Add OUs to a group via the per-item POST shortcut."""
        group = await service.add_organisation_unit_group_members(
            resolve_profile(profile),
            uid,
            ou_uids=ou_uids,
        )
        return _dump_model(group)

    @mcp.tool()
    async def metadata_organisation_unit_group_remove_members(
        uid: str,
        ou_uids: list[str],
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Drop OUs from a group via the per-item DELETE shortcut."""
        group = await service.remove_organisation_unit_group_members(
            resolve_profile(profile),
            uid,
            ou_uids=ou_uids,
        )
        return _dump_model(group)

    @mcp.tool()
    async def metadata_organisation_unit_group_delete(
        uid: str,
        profile: str | None = None,
    ) -> None:
        """Delete an OrganisationUnitGroup — members stay."""
        await service.delete_organisation_unit_group(resolve_profile(profile), uid)

    @mcp.tool()
    async def metadata_organisation_unit_group_set_list(
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """List every OrganisationUnitGroupSet."""
        group_sets = await service.list_organisation_unit_group_sets(resolve_profile(profile))
        return [_dump_model(gs) for gs in group_sets]

    @mcp.tool()
    async def metadata_organisation_unit_group_set_show(
        uid: str,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Fetch one group set with per-group member counts.

        Return shape: `{"group_set": {...}, "member_counts": {"<group_uid>": <int>}}`.
        """
        group_set, counts = await service.show_organisation_unit_group_set(resolve_profile(profile), uid)
        return {"group_set": _dump_model(group_set), "member_counts": counts}

    @mcp.tool()
    async def metadata_organisation_unit_group_set_create(
        name: str,
        short_name: str,
        uid: str | None = None,
        code: str | None = None,
        description: str | None = None,
        compulsory: bool = False,
        data_dimension: bool = True,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Create an empty OrganisationUnitGroupSet."""
        group_set = await service.create_organisation_unit_group_set(
            resolve_profile(profile),
            name=name,
            short_name=short_name,
            uid=uid,
            code=code,
            description=description,
            compulsory=compulsory,
            data_dimension=data_dimension,
        )
        return _dump_model(group_set)

    @mcp.tool()
    async def metadata_organisation_unit_group_set_add_groups(
        uid: str,
        group_uids: list[str],
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Add groups to a group set via the per-item POST shortcut."""
        group_set = await service.add_organisation_unit_group_set_groups(
            resolve_profile(profile),
            uid,
            group_uids=group_uids,
        )
        return _dump_model(group_set)

    @mcp.tool()
    async def metadata_organisation_unit_group_set_remove_groups(
        uid: str,
        group_uids: list[str],
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Drop groups from a group set via the per-item DELETE shortcut."""
        group_set = await service.remove_organisation_unit_group_set_groups(
            resolve_profile(profile),
            uid,
            group_uids=group_uids,
        )
        return _dump_model(group_set)

    @mcp.tool()
    async def metadata_organisation_unit_group_set_delete(
        uid: str,
        profile: str | None = None,
    ) -> None:
        """Delete an OrganisationUnitGroupSet — groups stay."""
        await service.delete_organisation_unit_group_set(resolve_profile(profile), uid)

    @mcp.tool()
    async def metadata_organisation_unit_level_list(
        profile: str | None = None,
    ) -> list[dict[str, Any]]:
        """List every OrganisationUnitLevel sorted by depth (1 = roots)."""
        levels = await service.list_organisation_unit_levels(resolve_profile(profile))
        return [_dump_model(row) for row in levels]

    @mcp.tool()
    async def metadata_organisation_unit_level_show(
        uid: str | None = None,
        level: int | None = None,
        profile: str | None = None,
    ) -> dict[str, Any] | None:
        """Fetch one level row — pass `uid` or `level` (numeric depth), not both."""
        if (uid is None) == (level is None):
            raise ValueError("pass exactly one of `uid` or `level`")
        if level is not None:
            row = await service.show_organisation_unit_level_by_level(resolve_profile(profile), level)
        else:
            assert uid is not None
            row = await service.show_organisation_unit_level(resolve_profile(profile), uid)
        return _dump_model(row) if row is not None else None

    @mcp.tool()
    async def metadata_organisation_unit_level_rename(
        name: str,
        uid: str | None = None,
        level: int | None = None,
        code: str | None = None,
        offline_levels: int | None = None,
        profile: str | None = None,
    ) -> dict[str, Any]:
        """Rename a level row — pass `uid` or `level` (numeric depth), not both."""
        if (uid is None) == (level is None):
            raise ValueError("pass exactly one of `uid` or `level`")
        if level is not None:
            row = await service.rename_organisation_unit_level_by_level(
                resolve_profile(profile),
                level,
                name=name,
                code=code,
                offline_levels=offline_levels,
            )
        else:
            assert uid is not None
            row = await service.rename_organisation_unit_level(
                resolve_profile(profile),
                uid,
                name=name,
                code=code,
                offline_levels=offline_levels,
            )
        return _dump_model(row)

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
