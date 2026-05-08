"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

from ._enums import DataDimensionItemType

if TYPE_CHECKING:
    from .data_element_operand_params import DataElementOperandParams
    from .data_element_params import DataElementParams
    from .expression_dimension_item_params import ExpressionDimensionItemParams
    from .indicator_params import IndicatorParams
    from .program_data_element_dimension_item_params import ProgramDataElementDimensionItemParams
    from .program_data_element_option_dimension_item_params import ProgramDataElementOptionDimensionItemParams
    from .program_indicator_params import ProgramIndicatorParams
    from .program_tracked_entity_attribute_dimension_item_params import ProgramTrackedEntityAttributeDimensionItemParams
    from .program_tracked_entity_attribute_option_dimension_item_params import (
        ProgramTrackedEntityAttributeOptionDimensionItemParams,
    )
    from .reporting_rate_params import ReportingRateParams
    from .subexpression_dimension_item_params import SubexpressionDimensionItemParams


class DataDimensionItemParams(_BaseModel):
    """OpenAPI schema `DataDimensionItemParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dataDimensionItemType: DataDimensionItemType | None = None
    dataElement: DataElementParams | None = None
    dataElementOperand: DataElementOperandParams | None = None
    expressionDimensionItem: ExpressionDimensionItemParams | None = None
    indicator: IndicatorParams | None = None
    programAttribute: ProgramTrackedEntityAttributeDimensionItemParams | None = None
    programAttributeOption: ProgramTrackedEntityAttributeOptionDimensionItemParams | None = None
    programDataElement: ProgramDataElementDimensionItemParams | None = None
    programDataElementOption: ProgramDataElementOptionDimensionItemParams | None = None
    programIndicator: ProgramIndicatorParams | None = None
    reportingRate: ReportingRateParams | None = None
    subexpressionDimensionItem: SubexpressionDimensionItemParams | None = None
