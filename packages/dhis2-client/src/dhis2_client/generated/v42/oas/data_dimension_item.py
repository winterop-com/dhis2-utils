"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import DataDimensionItemType

if TYPE_CHECKING:
    from .base_nameable_object import BaseNameableObject


class DataDimensionItem(_BaseModel):
    """OpenAPI schema `DataDimensionItem`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dataDimensionItemType: DataDimensionItemType
    dataElement: BaseNameableObject | None = None
    dataElementOperand: BaseNameableObject | None = None
    expressionDimensionItem: BaseNameableObject | None = None
    indicator: BaseNameableObject | None = None
    programAttribute: BaseNameableObject | None = None
    programAttributeOption: BaseNameableObject | None = None
    programDataElement: BaseNameableObject | None = None
    programDataElementOption: BaseNameableObject | None = None
    programIndicator: BaseNameableObject | None = None
    reportingRate: BaseNameableObject | None = None
    subexpressionDimensionItem: BaseNameableObject | None = None
