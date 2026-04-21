"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import AggregationType, FormType

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .base_identifiable_object import BaseIdentifiableObject
    from .data_approval_workflow import DataApprovalWorkflow
    from .data_element_operand import DataElementOperand
    from .data_entry_form import DataEntryForm
    from .data_input_period import DataInputPeriod
    from .data_set_element import DataSetElement
    from .identifiable_object import IdentifiableObject
    from .legend_set import LegendSet
    from .object_style import ObjectStyle
    from .query_modifiers import QueryModifiers
    from .sharing import Sharing
    from .translation import Translation
    from .user_dto import UserDto
    from .user_group import UserGroup


class DataSet(_BaseModel):
    """OpenAPI schema `DataSet`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    aggregationType: AggregationType | None = None
    attributeValues: list[AttributeValue] | None = None
    categoryCombo: IdentifiableObject | None = None
    code: str | None = None
    compulsoryDataElementOperands: list[DataElementOperand] | None = None
    compulsoryFieldsCompleteOnly: bool | None = None
    created: datetime | None = None
    createdBy: UserDto | None = None
    dataElementDecoration: bool | None = None
    dataEntryForm: DataEntryForm | None = None
    dataInputPeriods: list[DataInputPeriod] | None = None
    dataSetElements: list[DataSetElement] | None = None
    description: str | None = None
    dimensionItem: str | None = None
    displayDescription: str | None = None
    displayFormName: str | None = None
    displayName: str | None = None
    displayOptions: dict[str, Any] | None = None
    displayShortName: str | None = None
    expiryDays: float | None = None
    favorite: bool | None = None
    favorites: list[str] | None = None
    fieldCombinationRequired: bool | None = None
    formName: str | None = None
    formType: FormType | None = None
    href: str | None = None
    id: str | None = None
    indicators: list[BaseIdentifiableObject] | None = None
    interpretations: list[BaseIdentifiableObject] | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: UserDto | None = None
    legendSet: LegendSet | None = None
    legendSets: list[LegendSet] | None = None
    mobile: bool | None = None
    name: str | None = None
    noValueRequiresComment: bool | None = None
    notificationRecipients: UserGroup | None = None
    notifyCompletingUser: bool | None = None
    openFuturePeriods: int | None = None
    openPeriodsAfterCoEndDate: int | None = None
    organisationUnits: list[BaseIdentifiableObject] | None = None
    periodType: str | None = None
    queryMods: QueryModifiers | None = None
    renderAsTabs: bool | None = None
    renderHorizontally: bool | None = None
    sections: list[IdentifiableObject] | None = None
    sharing: Sharing | None = None
    shortName: str | None = None
    skipOffline: bool | None = None
    style: ObjectStyle | None = None
    timelyDays: float | None = None
    translations: list[Translation] | None = None
    validCompleteOnly: bool | None = None
    version: int | None = None
    workflow: DataApprovalWorkflow | None = None
