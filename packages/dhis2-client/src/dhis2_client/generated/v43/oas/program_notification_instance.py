"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

if TYPE_CHECKING:
    from .base_identifiable_object import BaseIdentifiableObject
    from .identifiable_object import IdentifiableObject
    from .program_notification_template_snapshot import ProgramNotificationTemplateSnapshot


class ProgramNotificationInstance(_BaseModel):
    """OpenAPI schema `ProgramNotificationInstance`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    code: str | None = None
    enrollment: IdentifiableObject | None = None
    event: BaseIdentifiableObject | None = None
    programNotificationTemplateId: int | None = None
    programNotificationTemplateSnapshot: ProgramNotificationTemplateSnapshot | None = None
    scheduledAt: datetime | None = None
    sentAt: datetime | None = None
