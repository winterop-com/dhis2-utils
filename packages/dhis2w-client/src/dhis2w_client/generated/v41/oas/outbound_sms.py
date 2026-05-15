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
    from .sharing import Sharing
    from .translation import Translation


class OutboundSmsCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OutboundSmsLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OutboundSmsUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OutboundSms(_BaseModel):
    """OpenAPI schema `OutboundSms`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: OutboundSmsCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    date: datetime | None = None
    displayName: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: OutboundSmsLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    message: str | None = None
    name: str | None = None
    recipients: list[str] | None = None
    sender: str | None = None
    sharing: Sharing | None = None
    status: Literal["OUTBOUND", "SENT", "ERROR", "PENDING", "SCHEDULED", "DELIVERED", "FAILED"] | None = None
    subject: str | None = None
    translations: list[Translation] | None = None
    user: OutboundSmsUser | None = _Field(default=None, description="A UID reference to a User  ")
