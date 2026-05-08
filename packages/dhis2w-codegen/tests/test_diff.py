"""Tests for the schemas-manifest diff helper."""

from __future__ import annotations

from dhis2w_codegen.diff import diff_manifests, render_text
from dhis2w_codegen.discover import Schema, SchemaProperty, SchemasManifest


def _manifest(version_key: str, schemas: list[Schema]) -> SchemasManifest:
    """Build a minimal SchemasManifest for tests."""
    return SchemasManifest(raw_version=f"2.{version_key[1:]}", version_key=version_key, schemas=schemas)


def _prop(name: str, **kwargs: object) -> SchemaProperty:
    """Build a SchemaProperty with only the fields a test cares about."""
    return SchemaProperty(name=name, **kwargs)  # type: ignore[arg-type]


def test_diff_detects_added_and_removed_schemas() -> None:
    """Top-level schemas added in `after` and removed-from-`before` show up."""
    before = _manifest("v42", [Schema(name="DataElement"), Schema(name="DataInputPeriod")])
    after = _manifest("v43", [Schema(name="DataElement"), Schema(name="NewResource")])
    diff = diff_manifests(before, after)
    assert [s.name for s in diff.added_schemas] == ["NewResource"]
    assert [s.name for s in diff.removed_schemas] == ["DataInputPeriod"]
    assert diff.changed_schemas == []


def test_diff_detects_property_changes() -> None:
    """Per-schema property changes — added, removed, and modified."""
    before = _manifest(
        "v42",
        [
            Schema(
                name="UserRole",
                properties=[
                    _prop("authority", collection=True, fieldName="authoritys"),
                    _prop("name"),
                    _prop("description"),
                ],
            ),
        ],
    )
    after = _manifest(
        "v43",
        [
            Schema(
                name="UserRole",
                properties=[
                    _prop("authority", collection=True, fieldName="authorities"),  # changed
                    _prop("name"),
                    _prop("createdBy"),  # added
                    # description removed
                ],
            ),
        ],
    )
    diff = diff_manifests(before, after)
    assert diff.added_schemas == []
    assert diff.removed_schemas == []
    assert len(diff.changed_schemas) == 1
    schema_diff = diff.changed_schemas[0]
    assert schema_diff.name == "UserRole"
    assert [p.name for p in schema_diff.added_properties] == ["createdBy"]
    assert [p.name for p in schema_diff.removed_properties] == ["description"]
    assert [c.name for c in schema_diff.changed_properties] == ["authority"]


def test_diff_returns_empty_for_identical_manifests() -> None:
    """No-op diff when both manifests describe the same schemas."""
    schemas = [Schema(name="DataElement", properties=[_prop("name")])]
    diff = diff_manifests(_manifest("v42", schemas), _manifest("v43", schemas))
    assert diff.added_schemas == []
    assert diff.removed_schemas == []
    assert diff.changed_schemas == []


def test_render_text_includes_version_keys_and_counts() -> None:
    """Rendered report lists from/to versions and the per-section counts."""
    before = _manifest("v42", [Schema(name="A"), Schema(name="B")])
    after = _manifest("v43", [Schema(name="A"), Schema(name="C")])
    output = render_text(diff_manifests(before, after))
    assert "v42 -> v43" in output
    assert "added schemas: 1" in output
    assert "removed schemas: 1" in output
    assert "+ C" in output
    assert "- B" in output
