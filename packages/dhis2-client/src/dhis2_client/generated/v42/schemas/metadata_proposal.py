"""Generated MetadataProposal model for DHIS2 v42. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import MetadataProposalStatus, MetadataProposalTarget, MetadataProposalType


class MetadataProposal(BaseModel):
    """Generated model for DHIS2 `MetadataProposal`.

    DHIS2 Metadata Proposal - DHIS2 resource (generated from /api/schemas at DHIS2 v42).


    API endpoint: /api/metadata/proposals.



    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    change: Any | None = Field(default=None, description="Reference to JsonNode. Length/value max=255.")

    comment: str | None = Field(default=None, description="Length/value max=255.")

    created: datetime | None = None

    createdBy: Reference | None = Field(default=None, description="Reference to User.")

    finalised: datetime | None = None

    finalisedBy: Reference | None = Field(default=None, description="Reference to User.")

    id: str | None = Field(default=None, description="Unique. Length/value min=11, max=11.")

    reason: str | None = Field(default=None, description="Length/value max=1024.")

    status: MetadataProposalStatus | None = None

    target: MetadataProposalTarget | None = None

    targetId: str | None = Field(default=None, description="Length/value max=11.")

    type: MetadataProposalType | None = None
