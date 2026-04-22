"""Generated OpenAPI-derived pydantic models. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict as _ConfigDict
from pydantic import Field as _Field

from ._enums import Status

if TYPE_CHECKING:
    from .api_token_creation_response import ApiTokenCreationResponse
    from .error_reports_web_message_response import ErrorReportsWebMessageResponse
    from .file_resource_web_message_response import FileResourceWebMessageResponse
    from .geo_json_import_report import GeoJsonImportReport
    from .import_count_web_message_response import ImportCountWebMessageResponse
    from .import_report_web_message_response import ImportReportWebMessageResponse
    from .import_summaries import ImportSummaries
    from .import_summary import ImportSummary
    from .import_type_summary import ImportTypeSummary
    from .job_configuration_web_message_response import JobConfigurationWebMessageResponse
    from .merge_web_response import MergeWebResponse
    from .metadata_sync_summary import MetadataSyncSummary
    from .object_report_web_message_response import ObjectReportWebMessageResponse
    from .prediction_summary import PredictionSummary
    from .software_update_response import SoftwareUpdateResponse
    from .tracker_job_web_message_response import TrackerJobWebMessageResponse


class WebMessage(_BaseModel):
    """OpenAPI schema `WebMessage`."""

    model_config = _ConfigDict(extra="allow", populate_by_name=True, defer_build=True)

    code: int | None = None
    devMessage: str | None = None
    errorCode: str | None = None
    httpStatus: str | None = None
    httpStatusCode: int | None = None
    message: str | None = None
    response: dict[str, Any] | None = None
    status: Status | None = None
