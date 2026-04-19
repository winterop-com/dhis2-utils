"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import DashboardItemShape, DashboardItemType

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class DashboardItem(_BaseModel):
    """OpenAPI schema `DashboardItem`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    appKey: str | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    contentCount: int | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    displayName: str | None = None
    eventChart: BaseIdentifiableObject | None = None
    eventReport: BaseIdentifiableObject | None = None
    eventVisualization: BaseIdentifiableObject | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    height: int | None = None
    href: str | None = None
    id: str | None = None
    interpretationCount: int | None = None
    interpretationLikeCount: int | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    map: BaseIdentifiableObject | None = None
    messages: bool | None = None
    name: str | None = None
    reports: list[BaseIdentifiableObject] | None = None
    resources: list[BaseIdentifiableObject] | None = None
    shape: DashboardItemShape | None = None
    sharing: Sharing | None = None
    text: str | None = None
    translations: list[Translation] | None = None
    type: DashboardItemType | None = None
    users: list[UserDto] | None = None
    visualization: BaseIdentifiableObject | None = None
    width: int | None = None
    x: int | None = None
    y: int | None = None
