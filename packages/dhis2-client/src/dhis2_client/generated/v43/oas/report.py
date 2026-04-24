"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import CacheStrategy, ReportType

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .relative_periods import RelativePeriods
    from .reporting_params import ReportingParams
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto


class Report(_BaseModel):
    """OpenAPI schema `Report`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    cacheStrategy: CacheStrategy | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    designContent: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    name: str | None = None
    relativePeriods: RelativePeriods | None = None
    reportParams: ReportingParams | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    type: ReportType | None = None
    visualization: BaseIdentifiableObject | None = None
