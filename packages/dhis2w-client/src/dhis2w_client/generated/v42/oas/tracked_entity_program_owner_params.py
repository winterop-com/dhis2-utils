"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict

if TYPE_CHECKING:
    from .organisation_unit_params import OrganisationUnitParams
    from .program_params import ProgramParams
    from .tracked_entity_params import TrackedEntityParams


class TrackedEntityProgramOwnerParams(_BaseModel):
    """OpenAPI schema `TrackedEntityProgramOwnerParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    organisationUnit: OrganisationUnitParams | None = None
    program: ProgramParams | None = None
    trackedEntityInstance: TrackedEntityParams | None = None
