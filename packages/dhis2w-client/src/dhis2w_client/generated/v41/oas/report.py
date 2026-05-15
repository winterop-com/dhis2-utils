"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .relative_periods import RelativePeriods
    from .reporting_params import ReportingParams
    from .sharing import Sharing
    from .translation import Translation


class ReportCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ReportLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ReportUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ReportVisualization(_BaseModel):
    """A UID reference to a Visualization  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class Report(_BaseModel):
    """OpenAPI schema `Report`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    cacheStrategy: (
        Literal[
            "NO_CACHE",
            "CACHE_1_MINUTE",
            "CACHE_5_MINUTES",
            "CACHE_10_MINUTES",
            "CACHE_15_MINUTES",
            "CACHE_30_MINUTES",
            "CACHE_1_HOUR",
            "CACHE_6AM_TOMORROW",
            "CACHE_TWO_WEEKS",
            "RESPECT_SYSTEM_SETTING",
        ]
        | None
    ) = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ReportCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    designContent: str | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ReportLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    name: str | None = None
    relativePeriods: RelativePeriods | None = None
    reportParams: ReportingParams | None = None
    sharing: Sharing | None = None
    translations: list[Translation] | None = None
    type: Literal["JASPER_REPORT_TABLE", "JASPER_JDBC", "HTML"] | None = None
    user: ReportUser | None = _Field(default=None, description="A UID reference to a User  ")
    visualization: ReportVisualization | None = _Field(default=None, description="A UID reference to a Visualization  ")
