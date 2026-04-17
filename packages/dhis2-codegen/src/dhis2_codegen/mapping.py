"""DHIS2 schema property types → Python type strings for code emission."""

from __future__ import annotations

from typing import Any

_PRIMITIVE_TYPES: dict[str, str] = {
    "TEXT": "str",
    "IDENTIFIER": "str",
    "CONSTANT": "str",
    "EMAIL": "str",
    "URL": "str",
    "PHONENUMBER": "str",
    "COLOR": "str",
    "PASSWORD": "str",
    "GEOLOCATION": "str",
    "BOOLEAN": "bool",
    "INTEGER": "int",
    "NUMBER": "float",
    "DATE": "datetime",
    "DATETIME": "datetime",
}


def python_type_for(property_spec: dict[str, Any]) -> str:
    """Return the Python type expression for a single DHIS2 schema property.

    Reference types fall back to `Reference`; collections return `list[T]`;
    unknown types become `Any`. All outputs assume the importing module has
    `Reference`, `Any`, `datetime`, and `Literal` in scope.
    """
    property_type = str(property_spec.get("propertyType") or "")
    collection = bool(property_spec.get("collection"))

    inner = _resolve_inner(property_type, property_spec)
    if collection:
        return f"list[{inner}]"
    return inner


def _resolve_inner(property_type: str, property_spec: dict[str, Any]) -> str:
    if property_type in _PRIMITIVE_TYPES:
        return _PRIMITIVE_TYPES[property_type]
    if property_type == "CONSTANT" and property_spec.get("constants"):
        options = ", ".join(f'"{c}"' for c in property_spec["constants"])
        return f"Literal[{options}]"
    if property_type == "REFERENCE":
        return "Reference"
    if property_type == "IDENTIFIER":
        return "str"
    if property_type == "COMPLEX":
        # Real DHIS2 responses for COMPLEX fields vary (sometimes dict, sometimes [], sometimes [{}]).
        # Trust the server and let `model_config = extra="allow"` preserve the payload.
        return "Any"
    return "Any"
