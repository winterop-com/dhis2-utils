"""Unit tests for the OpenAPI emitter — feeds in minimal specs and inspects output."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from dhis2_codegen.oas_emit import emit_from_openapi


def _run_emitter(tmp_path: Path, spec: dict[str, Any]) -> Path:
    """Write `spec` to disk and run the emitter against it."""
    openapi_path = tmp_path / "openapi.json"
    openapi_path.write_text(json.dumps(spec), encoding="utf-8")
    emit_from_openapi(openapi_path, tmp_path, version_key="vtest", raw_version="2.42.0")
    return tmp_path / "oas"


def test_emitter_produces_importable_module(tmp_path: Path) -> None:
    """Emitted `oas/` module imports cleanly and exposes one pydantic class per schema."""
    spec = {
        "components": {
            "schemas": {
                "Color": {
                    "type": "string",
                    "enum": ["RED", "GREEN", "BLUE"],
                },
                "Point": {
                    "type": "object",
                    "required": ["x"],
                    "properties": {
                        "x": {"type": "number"},
                        "y": {"type": "number"},
                        "colour": {"$ref": "#/components/schemas/Color"},
                    },
                },
            }
        }
    }
    oas_dir = _run_emitter(tmp_path, spec)
    sys.path.insert(0, str(tmp_path))
    try:
        import importlib

        if "oas" in sys.modules:
            del sys.modules["oas"]
        module = importlib.import_module("oas")
        assert hasattr(module, "Color"), "enum not re-exported"
        assert hasattr(module, "Point"), "object not re-exported"
        point_cls = module.Point
        instance = point_cls.model_validate({"x": 1, "y": 2, "colour": "RED"})
        assert instance.x == 1
        assert instance.colour == module.Color.RED
    finally:
        sys.path.remove(str(tmp_path))
    assert (oas_dir / "_enums.py").exists()
    assert (oas_dir / "point.py").exists()


def test_emitter_renames_builtin_shadows(tmp_path: Path) -> None:
    """`Warning` (Python builtin) becomes `DHIS2Warning` so pydantic doesn't clash."""
    spec = {
        "components": {
            "schemas": {
                "Warning": {
                    "type": "object",
                    "properties": {"msg": {"type": "string"}},
                },
            }
        }
    }
    oas_dir = _run_emitter(tmp_path, spec)
    init_src = (oas_dir / "__init__.py").read_text()
    assert "DHIS2Warning" in init_src
    assert "from .warning import Warning" not in init_src


def test_emitter_flattens_uid_aliases(tmp_path: Path) -> None:
    """UID_* wrappers flatten to plain `str` at field sites (no import needed)."""
    spec = {
        "components": {
            "schemas": {
                "UID_Thing": {
                    "type": "string",
                    "pattern": "^[a-z]{11}$",
                    "maxLength": 11,
                    "minLength": 11,
                },
                "HasThing": {
                    "type": "object",
                    "properties": {
                        "ref": {"$ref": "#/components/schemas/UID_Thing"},
                    },
                },
            }
        }
    }
    oas_dir = _run_emitter(tmp_path, spec)
    model_src = (oas_dir / "has_thing.py").read_text()
    assert "ref: str | None" in model_src


def test_emitter_writes_manifest(tmp_path: Path) -> None:
    """`openapi_manifest.json` summarises what was emitted for deterministic review."""
    spec = {"components": {"schemas": {"One": {"type": "object", "properties": {"n": {"type": "integer"}}}}}}
    _run_emitter(tmp_path, spec)
    manifest = json.loads((tmp_path / "openapi_manifest.json").read_text())
    assert manifest["version_key"] == "vtest"
    assert "One" in manifest["emitted"]["classes"]
    assert "openapi_sha256" in manifest
