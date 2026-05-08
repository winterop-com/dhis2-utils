"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType, DataElementDomain, ValueType

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .data_set_element import DataSetElement
    from .file_type_value_options import FileTypeValueOptions
    from .identifiable_object import IdentifiableObject
    from .legend_set import LegendSet
    from .object_style import ObjectStyle
    from .option_set import OptionSet
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class DataElement(_BaseModel):
    """OpenAPI schema `DataElement`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregationLevels: list[int] | None = None
    aggregationType: AggregationType | None = None
    attributeValues: list[AttributeValue] | None = None
    categoryCombo: IdentifiableObject | None = None
    code: str | None = None
    commentOptionSet: OptionSet | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    dataElementGroups: list[BaseIdentifiableObject] | None = None
    dataSetElements: list[DataSetElement] | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayShortName: str | None = None
    domainType: DataElementDomain | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    fieldMask: str | None = None
    formName: str | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    legendSet: LegendSet | None = None
    legendSets: list[LegendSet] | None = None
    name: str | None = None
    optionSet: OptionSet | None = None
    optionSetValue: bool | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    style: ObjectStyle | None = None
    translations: list[Translation] | None = None
    url: str | None = None
    valueType: ValueType | None = None
    valueTypeOptions: FileTypeValueOptions | None = None
    zeroIsSignificant: bool | None = None
