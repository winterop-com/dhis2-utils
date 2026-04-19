"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import AggregationType, FormType

if TYPE_CHECKING:
    from .attribute_value_params import AttributeValueParams
    from .category_combo_params import CategoryComboParams
    from .data_element_operand_params import DataElementOperandParams
    from .data_input_period import DataInputPeriod
    from .data_set_element_params import DataSetElementParams
    from .object_style import ObjectStyle
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation


class DataSetParamsCreatedBy(_BaseModel):
    """OpenAPI schema `DataSetParamsCreatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataSetParamsDataEntryForm(_BaseModel):
    """OpenAPI schema `DataSetParamsDataEntryForm`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataSetParamsIndicators(_BaseModel):
    """OpenAPI schema `DataSetParamsIndicators`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataSetParamsInterpretations(_BaseModel):
    """OpenAPI schema `DataSetParamsInterpretations`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataSetParamsLastUpdatedBy(_BaseModel):
    """OpenAPI schema `DataSetParamsLastUpdatedBy`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataSetParamsLegendSet(_BaseModel):
    """OpenAPI schema `DataSetParamsLegendSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataSetParamsLegendSets(_BaseModel):
    """OpenAPI schema `DataSetParamsLegendSets`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataSetParamsNotificationRecipients(_BaseModel):
    """OpenAPI schema `DataSetParamsNotificationRecipients`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataSetParamsOrganisationUnits(_BaseModel):
    """OpenAPI schema `DataSetParamsOrganisationUnits`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataSetParamsSections(_BaseModel):
    """OpenAPI schema `DataSetParamsSections`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataSetParamsWorkflow(_BaseModel):
    """OpenAPI schema `DataSetParamsWorkflow`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class DataSetParams(_BaseModel):
    """OpenAPI schema `DataSetParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    aggregationType: AggregationType
    attributeValues: list[AttributeValueParams] | None = None
    categoryCombo: CategoryComboParams | None = None
    code: str | None = None
    compulsoryDataElementOperands: list[DataElementOperandParams] | None = None
    compulsoryFieldsCompleteOnly: bool | None = None
    created: datetime | None = None
    createdBy: DataSetParamsCreatedBy | None = None
    dataElementDecoration: bool | None = None
    dataEntryForm: DataSetParamsDataEntryForm | None = None
    dataInputPeriods: list[DataInputPeriod] | None = None
    dataSetElements: list[DataSetElementParams] | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayOptions: dict[str, Any] | None = None
    displayShortName: str | None = None
    expiryDays: float
    favorite: bool | None = None
    favorites: list[str] | None = None
    fieldCombinationRequired: bool | None = None
    formName: str | None = None
    formType: FormType
    id: str | None = None
    indicators: list[DataSetParamsIndicators] | None = None
    interpretations: list[DataSetParamsInterpretations] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: DataSetParamsLastUpdatedBy | None = None
    legendSet: DataSetParamsLegendSet | None = None
    legendSets: list[DataSetParamsLegendSets] | None = None
    mobile: bool | None = None
    name: str | None = None
    noValueRequiresComment: bool | None = None
    notificationRecipients: DataSetParamsNotificationRecipients | None = None
    notifyCompletingUser: bool | None = None
    openFuturePeriods: int
    openPeriodsAfterCoEndDate: int
    organisationUnits: list[DataSetParamsOrganisationUnits] | None = None
    periodType: str | None = None
    queryMods: QueryModifiers | None = None
    renderAsTabs: bool | None = None
    renderHorizontally: bool | None = None
    sections: list[DataSetParamsSections] | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    skipOffline: bool | None = None
    style: ObjectStyle | None = None
    timelyDays: float
    translations: list[Translation] | None = None
    validCompleteOnly: bool | None = None
    version: int
    workflow: DataSetParamsWorkflow | None = None
