"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import SendStrategy

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class ValidationNotificationTemplateParamsCreatedBy(_BaseModel):
    """OpenAPI schema `ValidationNotificationTemplateParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationNotificationTemplateParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `ValidationNotificationTemplateParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationNotificationTemplateParamsRecipientUserGroups(_BaseModel):
    """OpenAPI schema `ValidationNotificationTemplateParamsRecipientUserGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationNotificationTemplateParamsValidationRules(_BaseModel):
    """OpenAPI schema `ValidationNotificationTemplateParamsValidationRules`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ValidationNotificationTemplateParams(_BaseModel):
    """OpenAPI schema `ValidationNotificationTemplateParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: ValidationNotificationTemplateParamsCreatedBy | None = None
    displayMessageTemplate: str | None = None
    displayName: str | None = None
    displaySubjectTemplate: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: ValidationNotificationTemplateParamsLastUpdatedBy | None = None
    messageTemplate: str | None = None
    name: str | None = None
    notifyParentOrganisationUnitOnly: bool | None = None
    notifyUsersInHierarchyOnly: bool | None = None
    recipientUserGroups: list[ValidationNotificationTemplateParamsRecipientUserGroups] | None = None
    sendStrategy: SendStrategy | None = None
    sharing: Sharing | None = None
    subjectTemplate: str | None = None
    translations: list[Translation] | None = None
    validationRules: list[ValidationNotificationTemplateParamsValidationRules] | None = None
