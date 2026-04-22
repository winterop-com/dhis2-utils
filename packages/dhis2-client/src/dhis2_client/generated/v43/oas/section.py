"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .attribute_values import AttributeValues
    from .base_identifiable_object import BaseIdentifiableObject
    from .data_element_operand import DataElementOperand
    from .identifiable_object import IdentifiableObject
    from .sharing import Sharing
    from .translation import Translation


class Section(_BaseModel):
    """OpenAPI schema `Section`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: AttributeValues | None = None
    categoryCombos: list[IdentifiableObject] | None = None
    code: str | None = None
    created: datetime | None = None
    dataElements: list[BaseIdentifiableObject] | None = None
    dataSet: BaseIdentifiableObject | None = None
    description: str | None = None
    disableDataElementAutoGroup: bool | None = None
    displayName: str | None = None
    displayOptions: dict[str, Any] | None = None
    greyedFields: list[DataElementOperand] | None = None
    href: str | None = None
    id: str | None = None
    indicators: list[BaseIdentifiableObject] | None = None
    lastUpdated: datetime | None = None
    name: str | None = None
    sharing: Sharing | None = None
    showColumnTotals: bool | None = None
    showRowTotals: bool | None = None
    sortOrder: int | None = None
    translations: list[Translation] | None = None
