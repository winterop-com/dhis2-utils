"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import DataSetNotificationRecipient, DataSetNotificationTrigger, DeliveryChannel, SendStrategy

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .sharing import Sharing
    from .translation import Translation


class DataSetNotificationTemplateParamsCreatedBy(_BaseModel):
    """OpenAPI schema `DataSetNotificationTemplateParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataSetNotificationTemplateParamsDataSets(_BaseModel):
    """OpenAPI schema `DataSetNotificationTemplateParamsDataSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataSetNotificationTemplateParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `DataSetNotificationTemplateParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataSetNotificationTemplateParamsRecipientUserGroup(_BaseModel):
    """OpenAPI schema `DataSetNotificationTemplateParamsRecipientUserGroup`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataSetNotificationTemplateParams(_BaseModel):
    """OpenAPI schema `DataSetNotificationTemplateParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    attributeValues: list[AttributeValueParams] | None = None
    code: str | None = None
    created: datetime | None = None
    createdBy: DataSetNotificationTemplateParamsCreatedBy | None = None
    dataSetNotificationTrigger: DataSetNotificationTrigger
    dataSets: list[DataSetNotificationTemplateParamsDataSets] | None = None
    deliveryChannels: list[DeliveryChannel] | None = None
    displayMessageTemplate: str | None = None
    displayName: str | None = None
    displaySubjectTemplate: str | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DataSetNotificationTemplateParamsLastUpdatedBy | None = None
    messageTemplate: str | None = None
    name: str | None = None
    notificationRecipient: DataSetNotificationRecipient
    notifyParentOrganisationUnitOnly: bool | None = None
    notifyUsersInHierarchyOnly: bool | None = None
    recipientUserGroup: DataSetNotificationTemplateParamsRecipientUserGroup | None = None
    relativeScheduledDays: int | None = None
    sendStrategy: SendStrategy
    sharing: Sharing | None = None
    subjectTemplate: str | None = None
    translations: list[Translation] | None = None
