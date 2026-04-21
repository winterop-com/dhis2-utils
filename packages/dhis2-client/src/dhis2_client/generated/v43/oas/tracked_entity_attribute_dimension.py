"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .base_identifiable_object import BaseIdentifiableObject
    from .identifiable_object import IdentifiableObject


class TrackedEntityAttributeDimension(_BaseModel):
    """OpenAPI schema `TrackedEntityAttributeDimension`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attribute: BaseIdentifiableObject | None = None
    filter: str | None = None
    legendSet: IdentifiableObject | None = None
