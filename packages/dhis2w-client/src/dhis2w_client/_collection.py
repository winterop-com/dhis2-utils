"""Internal helper — parse a DHIS2 collection envelope into typed models.

Every metadata listing endpoint follows the same wire shape: the response
is a JSON object whose top-level key is the resource plural (e.g.
`"dataElements": [...]`). Accessors used to inline `[Model.model_validate(row)
for row in raw.get("X") or [] if isinstance(row, dict)]` 18 times across the
client; centralise here so a future change to the envelope shape (say, a
wrapper key or an items-typed-as-dicts assumption) lands in one spot.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


def parse_collection[T: BaseModel](raw: dict[str, Any], key: str, model: type[T]) -> list[T]:
    """Validate `raw[key]` rows against `model`, dropping non-dict items.

    Returns `[]` when `raw[key]` is missing or not a list. Non-dict entries
    in the list are silently skipped — DHIS2 occasionally returns scalar
    placeholders (e.g. `null`) on partial / errored rows; we don't want
    `model_validate(None)` to take down the whole accessor.
    """
    rows = raw.get(key)
    if not isinstance(rows, list):
        return []
    return [model.model_validate(row) for row in rows if isinstance(row, dict)]
