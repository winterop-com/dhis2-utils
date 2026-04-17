"""Version-scoped generated clients. Populated by `dhis2 codegen`."""

from __future__ import annotations

import importlib
import re
from pathlib import Path
from types import ModuleType

_VERSION_KEY_RE = re.compile(r"^v\d+$")


def available_versions() -> tuple[str, ...]:
    r"""Return the version keys that have been populated by codegen.

    Walks the `generated/` folder, imports each `v\d+` subpackage, and returns
    only the ones whose `__init__.py` set `GENERATED = True`.
    """
    here = Path(__file__).parent
    ready: list[str] = []
    for child in sorted(here.iterdir()):
        if not child.is_dir() or not _VERSION_KEY_RE.match(child.name):
            continue
        try:
            module = importlib.import_module(f"dhis2_client.generated.{child.name}")
        except ImportError:
            continue
        if getattr(module, "GENERATED", False):
            ready.append(child.name)
    return tuple(ready)


def load(version_key: str) -> ModuleType:
    """Import a specific generated version module."""
    return importlib.import_module(f"dhis2_client.generated.{version_key}")
