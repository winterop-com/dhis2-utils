"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class TrackedEntityProgramOwnerOrganisationUnit(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityProgramOwnerProgram(_BaseModel):
    """A UID reference to a Program  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityProgramOwnerTrackedEntityInstance(_BaseModel):
    """A UID reference to a TrackedEntity  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class TrackedEntityProgramOwner(_BaseModel):
    """OpenAPI schema `TrackedEntityProgramOwner`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    organisationUnit: TrackedEntityProgramOwnerOrganisationUnit | None = _Field(
        default=None, description="A UID reference to a OrganisationUnit  "
    )
    program: TrackedEntityProgramOwnerProgram | None = _Field(
        default=None, description="A UID reference to a Program  "
    )
    trackedEntityInstance: TrackedEntityProgramOwnerTrackedEntityInstance | None = _Field(
        default=None, description="A UID reference to a TrackedEntity  "
    )
