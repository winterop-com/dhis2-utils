"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .attribute_values import AttributeValues
    from .data_element_operand_params import DataElementOperandParams
    from .data_set_params import DataSetParams
    from .sharing import Sharing
    from .translation import Translation


class SectionParamsDataElements(_BaseModel):
    """OpenAPI schema `SectionParamsDataElements`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SectionParamsIndicators(_BaseModel):
    """OpenAPI schema `SectionParamsIndicators`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class SectionParams(_BaseModel):
    """OpenAPI schema `SectionParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: AttributeValues | None = None
    code: str | None = None
    created: datetime | None = None
    dataElements: list[SectionParamsDataElements] | None = None
    dataSet: DataSetParams | None = None
    description: str | None = None
    disableDataElementAutoGroup: bool | None = None
    displayName: str | None = None
    displayOptions: dict[str, Any] | None = None
    greyedFields: list[DataElementOperandParams] | None = None
    id: str | None = None
    indicators: list[SectionParamsIndicators] | None = None
    lastUpdated: datetime | None = None
    name: str | None = None
    sharing: Sharing | None = None
    showColumnTotals: bool | None = None
    showRowTotals: bool | None = None
    sortOrder: int | None = None
    translations: list[Translation] | None = None
