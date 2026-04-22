"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .organisation_unit_params import OrganisationUnitParams
    from .tracked_entity import TrackedEntity


class ProgramMessageRecipientsParams(_BaseModel):
    """OpenAPI schema `ProgramMessageRecipientsParams`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    emailAddresses: list[str] | None = None
    organisationUnit: OrganisationUnitParams | None = None
    phoneNumbers: list[str] | None = None
    trackedEntity: TrackedEntity | None = None
