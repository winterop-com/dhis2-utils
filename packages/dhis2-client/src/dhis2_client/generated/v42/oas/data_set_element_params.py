"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .category_combo_params import CategoryComboParams
    from .data_element_params import DataElementParams
    from .data_set_params import DataSetParams


class DataSetElementParams(_BaseModel):
    """OpenAPI schema `DataSetElementParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    categoryCombo: CategoryComboParams | None = None
    dataElement: DataElementParams | None = None
    dataSet: DataSetParams | None = None
