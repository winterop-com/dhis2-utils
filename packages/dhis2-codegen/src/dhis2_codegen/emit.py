"""Emit pydantic models + resource classes + init stub from a SchemasManifest."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from jinja2 import Environment, PackageLoader, StrictUndefined, select_autoescape
from pydantic import BaseModel, ConfigDict

from dhis2_codegen.discover import Schema, SchemasManifest
from dhis2_codegen.mapping import python_type_for
from dhis2_codegen.names import to_class_name, to_module_name


class _Field(BaseModel):
    """One pydantic field rendered into the model template."""

    model_config = ConfigDict(frozen=True)

    name: str
    type: str


class _Resource(BaseModel):
    """One resource rendered into the resources template."""

    model_config = ConfigDict(frozen=True)

    class_name: str
    module_name: str
    plural: str
    attr_name: str


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

        (models_dir / f"{module_name}.py").write_text(
            model_template.render(
                class_name=class_name,
                version_key=manifest.version_key,
                fields=fields,
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
        fields.append(_Field(name=wire_name, type=field_type))
    fields.sort(key=lambda f: f.name)
    return fields


def _format_output(output_dir: Path) -> None:
    """Run `ruff format` on the emitted files (best-effort)."""
    try:
        subprocess.run(["ruff", "format", str(output_dir)], check=False, capture_output=True)
    except FileNotFoundError:
        pass
