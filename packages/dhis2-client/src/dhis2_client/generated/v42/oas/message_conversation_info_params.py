"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class MessageConversationInfoParamsAttachments(_BaseModel):
    """OpenAPI schema `MessageConversationInfoParamsAttachments`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MessageConversationInfoParamsOrganisationUnits(_BaseModel):
    """OpenAPI schema `MessageConversationInfoParamsOrganisationUnits`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MessageConversationInfoParamsUserGroups(_BaseModel):
    """OpenAPI schema `MessageConversationInfoParamsUserGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MessageConversationInfoParamsUsers(_BaseModel):
    """OpenAPI schema `MessageConversationInfoParamsUsers`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class MessageConversationInfoParams(_BaseModel):
    """OpenAPI schema `MessageConversationInfoParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attachments: list[MessageConversationInfoParamsAttachments] | None = None
    organisationUnits: list[MessageConversationInfoParamsOrganisationUnits] | None = None
    subject: str | None = None
    text: str | None = None
    userGroups: list[MessageConversationInfoParamsUserGroups] | None = None
    users: list[MessageConversationInfoParamsUsers] | None = None
