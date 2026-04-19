"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .data_element_params import DataElementParams
    from .legend_set_params import LegendSetParams
    from .program_stage_params import ProgramStageParams


class TrackedEntityDataElementDimensionParams(_BaseModel):
    """OpenAPI schema `TrackedEntityDataElementDimensionParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    dataElement: DataElementParams | None = None
    filter: str | None = None
    legendSet: LegendSetParams | None = None
    programStage: ProgramStageParams | None = None
