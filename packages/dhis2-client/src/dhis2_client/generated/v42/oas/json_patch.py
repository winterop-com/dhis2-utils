"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .add_operation import AddOperation
    from .remove_by_id_operation import RemoveByIdOperation
    from .remove_operation import RemoveOperation
    from .replace_operation import ReplaceOperation


class JsonPatch(_BaseModel):
    """OpenAPI schema `JsonPatch`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    operations: list[AddOperation | RemoveOperation | RemoveByIdOperation | ReplaceOperation] | None = None
