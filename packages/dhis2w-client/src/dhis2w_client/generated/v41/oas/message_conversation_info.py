"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict


class MessageConversationInfoAttachments(_BaseModel):
    """A UID reference to a FileResource  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MessageConversationInfoOrganisationUnits(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MessageConversationInfoUserGroups(_BaseModel):
    """A UID reference to a UserGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MessageConversationInfoUsers(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MessageConversationInfo(_BaseModel):
    """OpenAPI schema `MessageConversationInfo`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attachments: list[MessageConversationInfoAttachments] | None = None
    organisationUnits: list[MessageConversationInfoOrganisationUnits] | None = None
    subject: str | None = None
    text: str | None = None
    userGroups: list[MessageConversationInfoUserGroups] | None = None
    users: list[MessageConversationInfoUsers] | None = None
