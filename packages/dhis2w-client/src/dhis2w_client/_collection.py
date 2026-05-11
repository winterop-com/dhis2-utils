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
    return parse_rows(rows, model)


def parse_rows[T: BaseModel](rows: list[Any], model: type[T]) -> list[T]:
    """Validate already-unwrapped `rows` against `model`, dropping non-dict items.

    Sibling to `parse_collection` for sites whose row list is built by
    something other than `raw[key]` — `/api/apps` returns a bare array that
    `_unwrap_array` handles upstream, `/api/dataAnalysis/validationRulesAnalysis`
    returns either `data` or `validationResults` depending on the request
    shape. Same null-row tolerance as `parse_collection`.
    """
    return [model.model_validate(row) for row in rows if isinstance(row, dict)]
