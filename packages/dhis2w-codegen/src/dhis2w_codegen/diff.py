"""Diff two committed schemas_manifest.json files to surface upstream drift."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict

from dhis2w_codegen.discover import Schema, SchemaProperty, SchemasManifest


class _PropertyChange(BaseModel):
    """One property's before/after on a schema present in both manifests."""

    model_config = ConfigDict(frozen=True)

    name: str
    before: SchemaProperty
    after: SchemaProperty


class SchemaDiff(BaseModel):
    """Per-schema diff: added/removed properties and per-property changes."""

    model_config = ConfigDict(frozen=True)

    name: str
    added_properties: list[SchemaProperty]
    removed_properties: list[SchemaProperty]
    changed_properties: list[_PropertyChange]


class ManifestDiff(BaseModel):
    """Top-level diff between two schemas_manifest.json files."""

    model_config = ConfigDict(frozen=True)

    from_version: str
    to_version: str
    added_schemas: list[Schema]
    removed_schemas: list[Schema]
    changed_schemas: list[SchemaDiff]


def diff_manifests(before: SchemasManifest, after: SchemasManifest) -> ManifestDiff:
    """Compute the structural diff between two manifests."""
    before_by_name = {s.name: s for s in before.schemas}
    after_by_name = {s.name: s for s in after.schemas}

    added_names = sorted(after_by_name.keys() - before_by_name.keys())
    removed_names = sorted(before_by_name.keys() - after_by_name.keys())
    common_names = sorted(before_by_name.keys() & after_by_name.keys())

    changed: list[SchemaDiff] = []
    for name in common_names:
        schema_diff = _diff_schema(before_by_name[name], after_by_name[name])
        if schema_diff is not None:
            changed.append(schema_diff)

    return ManifestDiff(
        from_version=before.version_key,
        to_version=after.version_key,
        added_schemas=[after_by_name[n] for n in added_names],
        removed_schemas=[before_by_name[n] for n in removed_names],
        changed_schemas=changed,
    )


def diff_manifest_paths(before_path: Path, after_path: Path) -> ManifestDiff:
    """Load two manifests from disk and diff them."""
    before = SchemasManifest.model_validate_json(before_path.read_text(encoding="utf-8"))
    after = SchemasManifest.model_validate_json(after_path.read_text(encoding="utf-8"))
    return diff_manifests(before, after)


def render_text(diff: ManifestDiff) -> str:
    """Format a diff as a human-readable plain-text report."""
    lines: list[str] = []
    lines.append(f"Schema diff: {diff.from_version} -> {diff.to_version}")
    lines.append(
        f"  added schemas: {len(diff.added_schemas)}   "
        f"removed schemas: {len(diff.removed_schemas)}   "
        f"changed schemas: {len(diff.changed_schemas)}"
    )
    if diff.added_schemas:
        lines.append("")
        lines.append(f"## Added in {diff.to_version}")
        for s in diff.added_schemas:
            lines.append(f"  + {s.name}  ({len(s.properties)} props, klass={s.klass})")
    if diff.removed_schemas:
        lines.append("")
        lines.append(f"## Removed (only in {diff.from_version})")
        for s in diff.removed_schemas:
            lines.append(f"  - {s.name}  ({len(s.properties)} props, klass={s.klass})")
    if diff.changed_schemas:
        lines.append("")
        lines.append("## Changed")
        for sd in diff.changed_schemas:
            lines.append(f"  ~ {sd.name}")
            for prop in sd.added_properties:
                lines.append(f"      + {prop.name}  ({_summary(prop)})")
            for prop in sd.removed_properties:
                lines.append(f"      - {prop.name}  ({_summary(prop)})")
            for change in sd.changed_properties:
                deltas = _property_deltas(change.before, change.after)
                lines.append(f"      ~ {change.name}: {', '.join(deltas)}")
    return "\n".join(lines) + "\n"


def _diff_schema(before: Schema, after: Schema) -> SchemaDiff | None:
    """Build a SchemaDiff for two same-named schemas, or None if identical."""
    before_props = {p.name or p.fieldName or "": p for p in before.properties if p.name or p.fieldName}
    after_props = {p.name or p.fieldName or "": p for p in after.properties if p.name or p.fieldName}
    added_names = sorted(after_props.keys() - before_props.keys())
    removed_names = sorted(before_props.keys() - after_props.keys())
    common_names = sorted(before_props.keys() & after_props.keys())
    changes: list[_PropertyChange] = []
    for name in common_names:
        if before_props[name] != after_props[name]:
            changes.append(_PropertyChange(name=name, before=before_props[name], after=after_props[name]))
    if not added_names and not removed_names and not changes:
        return None
    return SchemaDiff(
        name=before.name,
        added_properties=[after_props[n] for n in added_names],
        removed_properties=[before_props[n] for n in removed_names],
        changed_properties=changes,
    )


def _summary(prop: SchemaProperty) -> str:
    """One-line description of a property for the report."""
    parts = [prop.propertyType or "?"]
    if prop.collection:
        parts.append("collection")
    if prop.itemKlass:
        parts.append(f"of {prop.itemKlass.split('.')[-1]}")
    return " ".join(parts)


def _property_deltas(before: SchemaProperty, after: SchemaProperty) -> list[str]:
    """Per-attribute before/after summary of a changed property."""
    deltas: list[str] = []
    for field in (
        "propertyType",
        "klass",
        "itemKlass",
        "itemPropertyType",
        "collection",
        "owner",
        "required",
        "readable",
        "writable",
        "persisted",
        "unique",
        "min",
        "max",
        "fieldName",
    ):
        b = getattr(before, field)
        a = getattr(after, field)
        if b != a:
            deltas.append(f"{field}: {b!r} -> {a!r}")
    return deltas
