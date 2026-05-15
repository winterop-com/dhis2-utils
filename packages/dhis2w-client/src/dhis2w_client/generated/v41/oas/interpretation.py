"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .access import Access
    from .attribute_value import AttributeValue
    from .mention import Mention
    from .sharing import Sharing
    from .translation import Translation


class InterpretationComments(_BaseModel):
    """A UID reference to a InterpretationComment  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class InterpretationCreatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class InterpretationDataSet(_BaseModel):
    """A UID reference to a DataSet  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class InterpretationEventChart(_BaseModel):
    """A UID reference to a EventChart  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class InterpretationEventReport(_BaseModel):
    """A UID reference to a EventReport  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class InterpretationEventVisualization(_BaseModel):
    """A UID reference to a EventVisualization  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class InterpretationLastUpdatedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class InterpretationLikedBy(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class InterpretationMap(_BaseModel):
    """A UID reference to a Map  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class InterpretationOrganisationUnit(_BaseModel):
    """A UID reference to a OrganisationUnit  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class InterpretationUser(_BaseModel):
    """A UID reference to a User  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class InterpretationVisualization(_BaseModel):
    """A UID reference to a Visualization  ."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    id: str | None = None


class Interpretation(_BaseModel):
    """OpenAPI schema `Interpretation`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    access: Access | None = None
    attributeValues: list[AttributeValue] | None = None
    code: str | None = None
    comments: list[InterpretationComments] | None = None
    created: datetime | None = None
    createdBy: InterpretationCreatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    dataSet: InterpretationDataSet | None = _Field(default=None, description="A UID reference to a DataSet  ")
    displayName: str | None = None
    eventChart: InterpretationEventChart | None = _Field(default=None, description="A UID reference to a EventChart  ")
    eventReport: InterpretationEventReport | None = _Field(
        default=None, description="A UID reference to a EventReport  "
    )
    eventVisualization: InterpretationEventVisualization | None = _Field(
        default=None, description="A UID reference to a EventVisualization  "
    )
    favorite: bool | None = None
    favorites: list[str] | None = None
    href: str | None = None
    id: str | None = None
    lastUpdated: datetime | None = None
    lastUpdatedBy: InterpretationLastUpdatedBy | None = _Field(default=None, description="A UID reference to a User  ")
    likedBy: list[InterpretationLikedBy] | None = None
    likes: int | None = None
    map: InterpretationMap | None = _Field(default=None, description="A UID reference to a Map  ")
    mentions: list[Mention] | None = None
    organisationUnit: InterpretationOrganisationUnit | None = _Field(
        default=None, description="A UID reference to a OrganisationUnit  "
    )
    period: str | None = None
    sharing: Sharing | None = None
    text: str | None = None
    translations: list[Translation] | None = None
    type: (
        Literal["VISUALIZATION", "EVENT_VISUALIZATION", "MAP", "EVENT_REPORT", "EVENT_CHART", "DATASET_REPORT"] | None
    ) = None
    user: InterpretationUser | None = _Field(default=None, description="A UID reference to a User  ")
    visualization: InterpretationVisualization | None = _Field(
        default=None, description="A UID reference to a Visualization  "
    )
