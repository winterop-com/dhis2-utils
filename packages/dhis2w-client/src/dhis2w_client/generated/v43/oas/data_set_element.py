"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .base_identifiable_object import BaseIdentifiableObject
    from .identifiable_object import IdentifiableObject


class DataSetElement(_BaseModel):
    """OpenAPI schema `DataSetElement`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    categoryCombo: IdentifiableObject | None = None
    dataElement: BaseIdentifiableObject | None = None
    dataSet: BaseIdentifiableObject | None = None
