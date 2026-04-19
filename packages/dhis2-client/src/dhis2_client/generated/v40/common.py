"""Generated DHIS2 v40 shared types. Do not edit by hand."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Reference(BaseModel):
    """Minimal reference to another DHIS2 object.

    DHIS2 accepts references keyed by `id` (UID, always) or `code` when the
    containing request sets `idScheme=CODE` (or the per-kind variants like
    `dataElementIdScheme=CODE`). Writes default to `id`; some bulk imports
    prefer `code` because UIDs aren't known client-side. Both fields are
    declared; `extra="allow"` accepts `{name, ...}` on the read path too.
    """

    model_config = ConfigDict(extra="allow")

    id: str | None = None
    code: str | None = None
