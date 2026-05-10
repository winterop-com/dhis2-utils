"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class OrganisationUnitGroupSetDimensionOrganisationUnitGroupSet(_BaseModel):
    """A UID reference to a OrganisationUnitGroupSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitGroupSetDimensionOrganisationUnitGroups(_BaseModel):
    """A UID reference to a OrganisationUnitGroup  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class OrganisationUnitGroupSetDimension(_BaseModel):
    """OpenAPI schema `OrganisationUnitGroupSetDimension`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    organisationUnitGroupSet: OrganisationUnitGroupSetDimensionOrganisationUnitGroupSet | None = _Field(
        default=None, description="A UID reference to a OrganisationUnitGroupSet  "
    )
    organisationUnitGroups: list[OrganisationUnitGroupSetDimensionOrganisationUnitGroups] | None = None
