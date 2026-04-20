"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .program_category_option_mapping import ProgramCategoryOptionMapping


class ProgramCategoryMapping(_BaseModel):
    """OpenAPI schema `ProgramCategoryMapping`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    categoryId: str | None = None
    id: str | None = None
    mappingName: str | None = None
    optionMappings: list[ProgramCategoryOptionMapping] | None = None
