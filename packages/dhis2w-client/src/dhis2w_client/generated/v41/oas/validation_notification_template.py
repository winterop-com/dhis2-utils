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


class ValidationNotificationTemplateCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationNotificationTemplateLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationNotificationTemplateRecipientUserGroups(_BaseModel):
    """A UID reference to a UserGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationNotificationTemplateUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationNotificationTemplateValidationRules(_BaseModel):
    """A UID reference to a ValidationRule  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationNotificationTemplate(_BaseModel):
    """OpenAPI schema `ValidationNotificationTemplate`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ValidationNotificationTemplateCreatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    displayMessageTemplate: str | None = None
    displayName: str | None = None
    displaySubjectTemplate: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ValidationNotificationTemplateLastUpdatedBy | None = _Field(
        default=None, description="A UID reference to a User  "
    )
    messageTemplate: str | None = None
    name: str | None = None
    notifyParentOrganisationUnitOnly: bool | None = None
    notifyUsersInHierarchyOnly: bool | None = None
    recipientUserGroups: list[ValidationNotificationTemplateRecipientUserGroups] | None = None
    sendStrategy: str | None = None
    sharing: Sharing | None = None
    subjectTemplate: str | None = None
    translations: list[Translation] | None = None
    user: ValidationNotificationTemplateUser | None = _Field(default=None, description="A UID reference to a User  ")
    validationRules: list[ValidationNotificationTemplateValidationRules] | None = None
