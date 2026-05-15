"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .data_element_operand import DataElementOperand
    from .program_data_element_dimension_item import ProgramDataElementDimensionItem
    from .program_tracked_entity_attribute_dimension_item import ProgramTrackedEntityAttributeDimensionItem
    from .reporting_rate import ReportingRate


class DataDimensionItemDataElement(_BaseModel):
    """A UID reference to a DataElement  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataDimensionItemExpressionDimensionItem(_BaseModel):
    """A UID reference to a ExpressionDimensionItem  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataDimensionItemIndicator(_BaseModel):
    """A UID reference to a Indicator  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataDimensionItemProgramIndicator(_BaseModel):
    """A UID reference to a ProgramIndicator  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataDimensionItemSubexpressionDimensionItem(_BaseModel):
    """A UID reference to a SubexpressionDimensionItem  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class DataDimensionItem(_BaseModel):
    """OpenAPI schema `DataDimensionItem`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dataDimensionItemType: (
        Literal[
            "INDICATOR",
            "DATA_ELEMENT",
            "DATA_ELEMENT_OPERAND",
            "REPORTING_RATE",
            "PROGRAM_INDICATOR",
            "PROGRAM_DATA_ELEMENT",
            "PROGRAM_ATTRIBUTE",
            "EXPRESSION_DIMENSION_ITEM",
            "SUBEXPRESSION_DIMENSION_ITEM",
            "VALIDATION_RULE",
        ]
        | None
    ) = None
    dataElement: DataDimensionItemDataElement | None = _Field(
        default=None, description="A UID reference to a DataElement  "
    )
    dataElementOperand: DataElementOperand | None = None
    expressionDimensionItem: DataDimensionItemExpressionDimensionItem | None = _Field(
        default=None, description="A UID reference to a ExpressionDimensionItem  "
    )
    indicator: DataDimensionItemIndicator | None = _Field(default=None, description="A UID reference to a Indicator  ")
    programAttribute: ProgramTrackedEntityAttributeDimensionItem | None = None
    programDataElement: ProgramDataElementDimensionItem | None = None
    programIndicator: DataDimensionItemProgramIndicator | None = _Field(
        default=None, description="A UID reference to a ProgramIndicator  "
    )
    reportingRate: ReportingRate | None = None
    subexpressionDimensionItem: DataDimensionItemSubexpressionDimensionItem | None = _Field(
        default=None, description="A UID reference to a SubexpressionDimensionItem  "
    )
