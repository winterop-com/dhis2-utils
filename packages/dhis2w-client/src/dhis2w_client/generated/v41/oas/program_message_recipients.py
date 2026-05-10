"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field


class ProgramMessageRecipientsOrganisationUnit(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramMessageRecipientsTrackedEntity(_BaseModel):
    """A UID reference to a TrackedEntity  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class ProgramMessageRecipients(_BaseModel):
    """OpenAPI schema `ProgramMessageRecipients`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    emailAddresses: list[str] | None = None
    organisationUnit: ProgramMessageRecipientsOrganisationUnit | None = _Field(
        default=None, description="A UID reference to a OrganisationUnit  "
    )
    phoneNumbers: list[str] | None = None
    trackedEntity: ProgramMessageRecipientsTrackedEntity | None = _Field(
        default=None, description="A UID reference to a TrackedEntity  "
    )
