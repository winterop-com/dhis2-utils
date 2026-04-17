"""Identifier sanitization: camelCase → snake_case + Python-safe names."""

from __future__ import annotations

import keyword
import re

_CAMEL_RE = re.compile(r"(?<!^)(?=[A-Z])")


def to_snake_case(name: str) -> str:
    """Convert camelCase or PascalCase to snake_case."""
    return _CAMEL_RE.sub("_", name).lower()


def to_module_name(resource_name: str) -> str:
    """Convert a DHIS2 resource name (camelCase) into a safe module file name."""
    snake = to_snake_case(resource_name)
    if keyword.iskeyword(snake):
        return f"{snake}_"
    if not snake.isidentifier():
        return re.sub(r"[^A-Za-z0-9_]+", "_", snake)
    return snake


def to_class_name(resource_name: str) -> str:
    """Convert a DHIS2 resource name into a PascalCase class name."""
    parts = re.split(r"[_\s-]+", resource_name)
    return "".join(p[:1].upper() + p[1:] for p in parts if p)
