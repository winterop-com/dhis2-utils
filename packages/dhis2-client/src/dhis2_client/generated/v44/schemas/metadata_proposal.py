"""Generated MetadataProposal model for DHIS2 v44. Do not edit by hand."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..common import Reference
from ..enums import MetadataProposalStatus, MetadataProposalTarget, MetadataProposalType


class MetadataProposal(BaseModel):
    """Generated model for DHIS2 `MetadataProposal`.

    DHIS2 Metadata Proposal - DHIS2 resource (generated from /api/schemas at DHIS2 v44).

    API endpoint: /dev/api/metadata/proposals.

    Field `Field(description=...)` entries flag DHIS2 semantics the bare
    type can't capture: which side of a relationship owns the link
    (writable) vs the inverse side (ignored by the API), uniqueness
    constraints, and length bounds.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    change: Any | None = Field(default=None, description="Reference to JsonNode. Read-only (inverse side).")
    comment: str | None = None
    created: datetime | None = None
    createdBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    finalised: datetime | None = None
    finalisedBy: Reference | None = Field(default=None, description="Reference to User. Read-only (inverse side).")
    id: str | None = None
    reason: str | None = None
    status: MetadataProposalStatus | None = None
    target: MetadataProposalTarget | None = None
    targetId: str | None = None
    type: MetadataProposalType | None = None
