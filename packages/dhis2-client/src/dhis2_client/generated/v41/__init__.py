"""Generated DHIS2 v41 client. Produced by `dhis2 codegen`.

Re-exports every pydantic resource schema so callers can write:

    from dhis2_client.generated.v41 import DataElement, OrganisationUnit

instead of the full `.schemas.<module>` path. Typed CRUD sits on `Resources`
(accessed via `client.resources.<plural>` once the client is connected).
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

from .schemas import (
    AggregateDataExchange,
    AnalyticsTableHook,
    ApiToken,
    Attribute,
    Category,
    CategoryCombo,
    CategoryOption,
    CategoryOptionCombo,
    CategoryOptionGroup,
    CategoryOptionGroupSet,
    Constant,
    Dashboard,
    DataApprovalLevel,
    DataApprovalWorkflow,
    DataElement,
    DataElementGroup,
    DataElementGroupSet,
    DataEntryForm,
    DataSet,
    DataSetNotificationTemplate,
    Document,
    EventChart,
    EventFilter,
    EventHook,
    EventReport,
    EventVisualization,
    ExpressionDimensionItem,
    ExternalMapLayer,
    Indicator,
    IndicatorGroup,
    IndicatorGroupSet,
    IndicatorType,
    JobConfiguration,
    LegendSet,
    Map,
    MapView,
    OAuth2Client,
    Option,
    OptionGroup,
    OptionGroupSet,
    OptionSet,
    OrganisationUnit,
    OrganisationUnitGroup,
    OrganisationUnitGroupSet,
    OrganisationUnitLevel,
    Predictor,
    PredictorGroup,
    Program,
    ProgramIndicator,
    ProgramIndicatorGroup,
    ProgramNotificationTemplate,
    ProgramRule,
    ProgramRuleAction,
    ProgramRuleVariable,
    ProgramSection,
    ProgramStage,
    ProgramStageSection,
    ProgramStageWorkingList,
    PushAnalysis,
    RelationshipType,
    Report,
    Route,
    Section,
    SMSCommand,
    SqlView,
    TrackedEntityAttribute,
    TrackedEntityFilter,
    TrackedEntityType,
    User,
    UserGroup,
    UserRole,
    ValidationNotificationTemplate,
    ValidationRule,
    ValidationRuleGroup,
    Visualization,
)


# Lazy Resources re-export (PEP 562). Importing this package no longer
# pulls dhis2_client.client (and the cycle through categories /
# envelopes / oas) at import time. Resources loads on first attribute
# access -- including the getattr(self._generated, "Resources") lookup
# in Dhis2Client.connect.
def __getattr__(name: str) -> Any:
    if name == "Resources":
        value = import_module(".resources", __package__).Resources
        globals()[name] = value
        return value
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


if TYPE_CHECKING:
    from .resources import Resources

GENERATED = True
VERSION_KEY = "v41"
RAW_VERSION = "2.41.8"

__all__ = [
    "GENERATED",
    "RAW_VERSION",
    "Resources",
    "VERSION_KEY",
    "AggregateDataExchange",
    "AnalyticsTableHook",
    "ApiToken",
    "Attribute",
    "Category",
    "CategoryCombo",
    "CategoryOption",
    "CategoryOptionCombo",
    "CategoryOptionGroup",
    "CategoryOptionGroupSet",
    "Constant",
    "Dashboard",
    "DataApprovalLevel",
    "DataApprovalWorkflow",
    "DataElement",
    "DataElementGroup",
    "DataElementGroupSet",
    "DataEntryForm",
    "DataSet",
    "DataSetNotificationTemplate",
    "Document",
    "EventChart",
    "EventFilter",
    "EventHook",
    "EventReport",
    "EventVisualization",
    "ExpressionDimensionItem",
    "ExternalMapLayer",
    "Indicator",
    "IndicatorGroup",
    "IndicatorGroupSet",
    "IndicatorType",
    "JobConfiguration",
    "LegendSet",
    "Map",
    "MapView",
    "OAuth2Client",
    "Option",
    "OptionGroup",
    "OptionGroupSet",
    "OptionSet",
    "OrganisationUnit",
    "OrganisationUnitGroup",
    "OrganisationUnitGroupSet",
    "OrganisationUnitLevel",
    "Predictor",
    "PredictorGroup",
    "Program",
    "ProgramIndicator",
    "ProgramIndicatorGroup",
    "ProgramNotificationTemplate",
    "ProgramRule",
    "ProgramRuleAction",
    "ProgramRuleVariable",
    "ProgramSection",
    "ProgramStage",
    "ProgramStageSection",
    "ProgramStageWorkingList",
    "PushAnalysis",
    "RelationshipType",
    "Report",
    "Route",
    "SMSCommand",
    "Section",
    "SqlView",
    "TrackedEntityAttribute",
    "TrackedEntityFilter",
    "TrackedEntityType",
    "User",
    "UserGroup",
    "UserRole",
    "ValidationNotificationTemplate",
    "ValidationRule",
    "ValidationRuleGroup",
    "Visualization",
]
