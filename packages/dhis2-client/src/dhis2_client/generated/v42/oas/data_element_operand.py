"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .legend_set import LegendSet
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class DataElementOperand(_BaseModel):
    """OpenAPI schema `DataElementOperand`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeOptionCombo: BaseIdentifiableObject | None = None
    attributeValues: list[AttributeValue] | None = None
    categoryOptionCombo: BaseIdentifiableObject | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    dataElement: BaseIdentifiableObject | None = None
    description: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    formName: str | None = None
    href: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    legendSet: LegendSet | None = None
    legendSets: list[LegendSet] | None = None
    queryMods: QueryModifiers | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
