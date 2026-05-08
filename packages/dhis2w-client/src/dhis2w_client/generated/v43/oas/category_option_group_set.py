"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType, DataDimensionType, ValueType

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .dimension_item_keywords import DimensionItemKeywords
    from .dimensional_item_object import DimensionalItemObject
    from .event_repetition import EventRepetition
    from .identifiable_object import IdentifiableObject
    from .option_set import OptionSet
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class CategoryOptionGroupSet(_BaseModel):
    """OpenAPI schema `CategoryOptionGroupSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregationType: AggregationType | None = None
    allItems: bool | None = None
    attributeValues: list[AttributeValue] | None = None
    categoryOptionGroups: list[BaseIdentifiableObject] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    dataDimension: bool | None = None
    dataDimensionType: DataDimensionType | None = None
    description: str | None = None
    dimension: str | None = None
    dimensionItemKeywords: DimensionItemKeywords | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    filter: str | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    items: list[DimensionalItemObject] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    legendSet: IdentifiableObject | None = None
    name: str | None = None
    optionSet: OptionSet | None = None
    program: IdentifiableObject | None = None
    programStage: BaseIdentifiableObject | None = None
    repetition: EventRepetition | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    translations: list[Translation] | None = None
    valueType: ValueType | None = None
