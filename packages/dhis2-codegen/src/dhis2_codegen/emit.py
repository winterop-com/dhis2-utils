"""Emit pydantic models + resource classes + init stub from a SchemasManifest."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from jinja2 import Environment, PackageLoader, StrictUndefined, select_autoescape
from pydantic import BaseModel, ConfigDict

from dhis2_codegen.discover import Schema, SchemaProperty, SchemasManifest
from dhis2_codegen.mapping import python_type_for
from dhis2_codegen.names import to_class_name, to_module_name


class _Field(BaseModel):
    """One pydantic field rendered into the model template."""

    model_config = ConfigDict(frozen=True)

    name: str
    type: str
    docstring: str = ""


class _Resource(BaseModel):
    """One resource rendered into the resources template."""

    model_config = ConfigDict(frozen=True)

    class_name: str
    module_name: str
    plural: str
    attr_name: str


class _ClassDoc(BaseModel):
    """Components of a generated class's docstring."""

    model_config = ConfigDict(frozen=True)

    summary: str  # one-liner at the top of the docstring
    endpoint: str | None = None  # /api/<endpoint> for the collection
    persisted: bool = True
    metadata: bool = False


def emit(manifest: SchemasManifest, output_dir: Path) -> None:
    """Emit the generated v{NN} module at `output_dir` based on `manifest`."""
    output_dir.mkdir(parents=True, exist_ok=True)
    models_dir = output_dir / "models"
    models_dir.mkdir(exist_ok=True)

    environment = Environment(
        loader=PackageLoader("dhis2_codegen", "templates"),
        autoescape=select_autoescape(default=False),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )

    manifest_path = output_dir / "schemas_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest.model_dump(mode="json"), indent=2, sort_keys=True),
        encoding="utf-8",
    )

    resources: list[_Resource] = []
    model_template = environment.get_template("model.py.jinja")

    seen_classes: set[str] = set()
    seen_attrs: set[str] = set()
    for schema in manifest.schemas:
        if not schema.plural or not schema.metadata:
            continue
        identifier = _identifier_for(schema)
        if not identifier:
            continue
        class_name = to_class_name(identifier)
        module_name = to_module_name(identifier)
        if class_name in seen_classes:
            continue
        seen_classes.add(class_name)
        attr_name = to_module_name(schema.plural)
        if attr_name in seen_attrs:
            continue
        seen_attrs.add(attr_name)
        fields = _fields_for(schema)
        class_doc = _class_doc_for(schema, manifest.version_key)

        (models_dir / f"{module_name}.py").write_text(
            model_template.render(
                class_name=class_name,
                version_key=manifest.version_key,
                fields=fields,
                class_doc=class_doc,
            ),
            encoding="utf-8",
        )
        resources.append(
            _Resource(
                class_name=class_name,
                module_name=module_name,
                plural=schema.plural,
                attr_name=attr_name,
            )
        )

    resources.sort(key=lambda r: r.class_name)

    (output_dir / "resources.py").write_text(
        environment.get_template("resources.py.jinja").render(
            version_key=manifest.version_key,
            resources=resources,
        ),
        encoding="utf-8",
    )
    (output_dir / "__init__.py").write_text(
        environment.get_template("init.py.jinja").render(
            version_key=manifest.version_key,
            raw_version=manifest.raw_version,
        ),
        encoding="utf-8",
    )
    (models_dir / "__init__.py").write_text(
        f'"""Generated DHIS2 {manifest.version_key} pydantic models."""\n',
        encoding="utf-8",
    )

    _format_output(output_dir)


def _identifier_for(schema: Schema) -> str | None:
    """Derive a unique identifier for the schema (Java class tail, singular, or name)."""
    if schema.klass:
        tail = schema.klass.rsplit(".", 1)[-1]
        if tail:
            return tail
    if schema.singular:
        return schema.singular
    return schema.name or None


def _class_doc_for(schema: Schema, version_key: str) -> _ClassDoc:
    """Summarise a schema into the pieces the class docstring template needs."""
    label = schema.displayName or schema.singular or schema.name
    kind = "persisted metadata" if schema.persisted and schema.metadata else "DHIS2 resource"
    summary = f"DHIS2 {label} - {kind} (generated from /api/schemas at DHIS2 {version_key})."
    # DHIS2's apiEndpoint is an absolute URL pinned to whatever instance we
    # discovered against (e.g. http://localhost:8080/api/dataElements). Strip
    # the scheme+host so the generated docstring stays portable — the relative
    # path is what every DHIS2 instance exposes.
    endpoint = schema.apiEndpoint
    if endpoint and endpoint.startswith(("http://", "https://")):
        # strip scheme + host, keep the path starting with /api/...
        endpoint = "/" + endpoint.split("://", 1)[1].split("/", 1)[1] if "/" in endpoint.split("://", 1)[1] else None
    return _ClassDoc(
        summary=summary,
        endpoint=endpoint,
        persisted=schema.persisted,
        metadata=schema.metadata,
    )


def _field_description(prop: SchemaProperty) -> str:
    """Build a short description for a field, highlighting owner/writability/bounds."""
    parts: list[str] = []
    if prop.collection:
        target = (prop.itemKlass or prop.klass or "").rsplit(".", 1)[-1]
        if target:
            parts.append(f"Collection of {target}.")
    elif prop.klass and not prop.simple:
        target = prop.klass.rsplit(".", 1)[-1]
        if target:
            parts.append(f"Reference to {target}.")
    # DHIS2-specific: non-owner collections + references are the inverse side of
    # an association, and writes against them are silently ignored by the API.
    # ASCII only — the generator emits these into docstrings rendered via
    # `|tojson`, which would escape a fancy em-dash to `\u2014` (6 chars) and
    # push several already-long lines past the 120-col limit.
    if not prop.owner and (prop.collection or (prop.klass is not None and not prop.simple)):
        parts.append("Read-only (inverse side).")
    elif not prop.writable:
        parts.append("Read-only.")
    if prop.unique:
        parts.append("Unique.")
    bounds: list[str] = []
    # DHIS2 uses Double.MIN_VALUE / MAX_VALUE as "unbounded" sentinels; filter those
    # so docstrings don't leak `max=1.7976931348623157e+308` (unreadable) or `min=0`
    # (always-implied "non-negative", adds noise not signal).
    if prop.min is not None and prop.min > 0:
        bounds.append(f"min={int(prop.min) if float(prop.min).is_integer() else prop.min}")
    if prop.max is not None and prop.max < 1e18:
        bounds.append(f"max={int(prop.max) if float(prop.max).is_integer() else prop.max}")
    if bounds:
        parts.append("Length/value " + ", ".join(bounds) + ".")
    return " ".join(parts)


def _fields_for(schema: Schema) -> list[_Field]:
    """Build the pydantic field list for a single schema."""
    seen: set[str] = set()
    fields: list[_Field] = []
    for property_spec in schema.properties:
        wire_name = property_spec.fieldName or property_spec.name
        if not wire_name or wire_name in seen:
            continue
        if not wire_name.isidentifier():
            continue
        seen.add(wire_name)
        field_type = python_type_for(property_spec.model_dump())
        fields.append(
            _Field(
                name=wire_name,
                type=field_type,
                docstring=_field_description(property_spec),
            )
        )
    fields.sort(key=lambda f: f.name)
    return fields


def _format_output(output_dir: Path) -> None:
    """Run `ruff format` on the emitted files (best-effort)."""
    try:
        subprocess.run(["ruff", "format", str(output_dir)], check=False, capture_output=True)
    except FileNotFoundError:
        pass
