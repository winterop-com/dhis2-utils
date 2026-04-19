"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import SendStrategy

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .identifiable_object import IdentifiableObject
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto
    from .user_group import UserGroup


class ValidationNotificationTemplate(_BaseModel):
    """OpenAPI schema `ValidationNotificationTemplate`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    displayMessageTemplate: str | None = None
    displayName: str | None = None
    displaySubjectTemplate: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    messageTemplate: str | None = None
    name: str | None = None
    notifyParentOrganisationUnitOnly: bool | None = None
    notifyUsersInHierarchyOnly: bool | None = None
    recipientUserGroups: list[UserGroup] | None = None
    sendStrategy: SendStrategy
    sharing: Sharing | None = None
    subjectTemplate: str | None = None
    translations: list[Translation] | None = None
    validationRules: list[IdentifiableObject] | None = None
