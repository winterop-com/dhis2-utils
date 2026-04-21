"""Helpers shared between the /api/schemas emitter and the OpenAPI emitter."""

from __future__ import annotations

import contextlib
import keyword
import subprocess
from pathlib import Path


def sanitize_identifier(wire_name: str) -> tuple[str, str | None]:
    """Return `(python_name, alias_or_none)` for a wire field name.

    Pydantic keyword collisions (`from`, `class`, etc.) take a `_` suffix plus
    `Field(alias=...)` so the wire form still serialises.
    """
    if not wire_name:
        return wire_name, None
    if keyword.iskeyword(wire_name):
        return f"{wire_name}_", wire_name
    return wire_name, None


def format_output(output_dir: Path) -> None:
    """Run `ruff check --fix` then `ruff format` on the emitted files (best-effort).

    Selects `I` (import sort), `W` (whitespace), and `B033` (duplicate-value
    in set literal) — the last catches the `_submodule_names` duplicates
    multi-class modules would otherwise produce if the emitter forgets to
    dedupe. Avoid `F` — `ruff` flags `Any` as unused import when annotations
    are stringified via `from __future__ import annotations`, even though
    pydantic still evaluates them at model-schema time.
    """
    with contextlib.suppress(FileNotFoundError):
        subprocess.run(
            ["ruff", "check", "--fix", "--select", "I,W,B033", str(output_dir)],
            check=False,
            capture_output=True,
        )
        subprocess.run(["ruff", "format", str(output_dir)], check=False, capture_output=True)
