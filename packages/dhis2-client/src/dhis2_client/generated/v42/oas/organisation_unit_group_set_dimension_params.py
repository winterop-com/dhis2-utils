"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .organisation_unit_group_set_params import OrganisationUnitGroupSetParams


class OrganisationUnitGroupSetDimensionParamsOrganisationUnitGroups(_BaseModel):
    """OpenAPI schema `OrganisationUnitGroupSetDimensionParamsOrganisationUnitGroups`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str


class OrganisationUnitGroupSetDimensionParams(_BaseModel):
    """OpenAPI schema `OrganisationUnitGroupSetDimensionParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    organisationUnitGroupSet: OrganisationUnitGroupSetParams | None = None
    organisationUnitGroups: list[OrganisationUnitGroupSetDimensionParamsOrganisationUnitGroups] | None = None
