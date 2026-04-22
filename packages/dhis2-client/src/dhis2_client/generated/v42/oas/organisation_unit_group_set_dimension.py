"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .base_identifiable_object import BaseIdentifiableObject
    from .organisation_unit_group import OrganisationUnitGroup


class OrganisationUnitGroupSetDimension(_BaseModel):
    """OpenAPI schema `OrganisationUnitGroupSetDimension`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    organisationUnitGroupSet: BaseIdentifiableObject | None = None
    organisationUnitGroups: list[OrganisationUnitGroup] | None = None
