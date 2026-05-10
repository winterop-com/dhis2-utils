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
    from .sharing import Sharing
    from .translation import Translation


class PushAnalysisCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PushAnalysisDashboard(_BaseModel):
    """A UID reference to a Dashboard  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PushAnalysisLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PushAnalysisRecipientUserGroups(_BaseModel):
    """A UID reference to a UserGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PushAnalysisUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class PushAnalysis(_BaseModel):
    """OpenAPI schema `PushAnalysis`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: PushAnalysisCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    dashboard: PushAnalysisDashboard | None = _Field(default=None, description="A UID reference to a Dashboard  ")
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: PushAnalysisLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    message: str | None = None
    name: str | None = None
    recipientUserGroups: list[PushAnalysisRecipientUserGroups] | None = None
    sharing: Sharing | None = None
    title: str | None = None
    translations: list[Translation] | None = None
    user: PushAnalysisUser | None = _Field(default=None, description="A UID reference to a User  ")
