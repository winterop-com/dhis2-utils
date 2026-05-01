"""Async DHIS2 API client with pluggable auth and pydantic models."""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

# PEP 562 lazy attribute resolution. Importing `dhis2_client` no longer pulls
# every submodule (and the 4k-line generated OAS module by transitive closure)
# at package init time. Submodules load on first attribute access.
_LAZY_EXPORTS: dict[str, str] = {
    # aggregate
    "DataValue": "aggregate",
    "DataValueSet": "aggregate",
    # analytics
    "AnalyticsMetaData": "analytics",
    "Grid": "analytics",
    "GridHeader": "analytics",
    # analytics_stream
    "AnalyticsAccessor": "analytics_stream",
    # apps
    "App": "apps",
    "AppHubApp": "apps",
    "AppHubVersion": "apps",
    "AppsAccessor": "apps",
    "AppSnapshotEntry": "apps",
    "AppsSnapshot": "apps",
    "AppStatus": "apps",
    "AppType": "apps",
    "RestoreOutcome": "apps",
    "RestoreSummary": "apps",
    # attribute_values
    "AttributeValuesAccessor": "attribute_values",
    # auth
    "AuthProvider": "auth.base",
    "BasicAuth": "auth.basic",
    "OAuth2Auth": "auth.oauth2",
    "OAuth2Token": "auth.oauth2",
    "TokenStore": "auth.oauth2",
    "PatAuth": "auth.pat",
    # auth_schemes
    "ApiHeadersAuthScheme": "auth_schemes",
    "ApiQueryParamsAuthScheme": "auth_schemes",
    "ApiTokenAuthScheme": "auth_schemes",
    "AuthScheme": "auth_schemes",
    "AuthSchemeAdapter": "auth_schemes",
    "HttpBasicAuthScheme": "auth_schemes",
    "OAuth2ClientCredentialsAuthScheme": "auth_schemes",
    "auth_scheme_from_route": "auth_schemes",
    # categories
    "CategoriesAccessor": "categories",
    "Category": "categories",
    # category_combo_builder
    "CategoryBuildEntry": "category_combo_builder",
    "CategoryComboBuildResult": "category_combo_builder",
    "CategoryComboBuildSpec": "category_combo_builder",
    "CategoryOptionSpec": "category_combo_builder",
    "CategorySpec": "category_combo_builder",
    "build_category_combo": "category_combo_builder",
    # category_combos
    "CategoryCombo": "category_combos",
    "CategoryCombosAccessor": "category_combos",
    # category_option_combos
    "CategoryOptionCombo": "category_option_combos",
    "CategoryOptionCombosAccessor": "category_option_combos",
    # category_option_group_sets
    "CategoryOptionGroupSet": "category_option_group_sets",
    "CategoryOptionGroupSetsAccessor": "category_option_group_sets",
    # category_option_groups
    "CategoryOptionGroup": "category_option_groups",
    "CategoryOptionGroupsAccessor": "category_option_groups",
    # category_options
    "CategoryOption": "category_options",
    "CategoryOptionsAccessor": "category_options",
    # client
    "Dhis2Client": "client",
    # customize
    "CustomizationResult": "customize",
    "CustomizeAccessor": "customize",
    "LoginCustomization": "customize",
    # dashboards
    "DashboardsAccessor": "dashboards",
    "DashboardSlot": "dashboards",
    # data_element_group_sets
    "DataElementGroupSet": "data_element_group_sets",
    "DataElementGroupSetsAccessor": "data_element_group_sets",
    # data_element_groups
    "DataElementGroup": "data_element_groups",
    "DataElementGroupsAccessor": "data_element_groups",
    # data_elements
    "DataElement": "data_elements",
    "DataElementsAccessor": "data_elements",
    # data_sets
    "DataSet": "data_sets",
    "DataSetsAccessor": "data_sets",
    # data_values
    "DataValuesAccessor": "data_values",
    # envelopes
    "Conflict": "envelopes",
    "ConflictRow": "envelopes",
    "ErrorReport": "envelopes",
    "ImportCount": "envelopes",
    "ImportReport": "envelopes",
    "ObjectReport": "envelopes",
    "Stats": "envelopes",
    "TypeReport": "envelopes",
    "WebMessageResponse": "envelopes",
    # errors
    "AuthenticationError": "errors",
    "Dhis2ApiError": "errors",
    "Dhis2ClientError": "errors",
    "OAuth2FlowError": "errors",
    "UnsupportedVersionError": "errors",
    # files
    "Document": "files",
    "FileResource": "files",
    "FileResourceDomain": "files",
    "FilesAccessor": "files",
    # generated
    "Dhis2": "generated",
    # indicator_group_sets
    "IndicatorGroupSet": "indicator_group_sets",
    "IndicatorGroupSetsAccessor": "indicator_group_sets",
    # indicator_groups
    "IndicatorGroup": "indicator_groups",
    "IndicatorGroupsAccessor": "indicator_groups",
    # indicators
    "Indicator": "indicators",
    "IndicatorsAccessor": "indicators",
    # json_patch
    "AddOp": "json_patch",
    "CopyOp": "json_patch",
    "JsonPatchOp": "json_patch",
    "JsonPatchOpAdapter": "json_patch",
    "MoveOp": "json_patch",
    "RemoveOp": "json_patch",
    "ReplaceOp": "json_patch",
    "TestOp": "json_patch",
    # legend_sets
    "Legend": "legend_sets",
    "LegendSet": "legend_sets",
    "LegendSetsAccessor": "legend_sets",
    "LegendSetSpec": "legend_sets",
    "LegendSpec": "legend_sets",
    # maintenance
    "DataIntegrityCheck": "maintenance",
    "DataIntegrityIssue": "maintenance",
    "DataIntegrityReport": "maintenance",
    "DataIntegrityResult": "maintenance",
    "IntegrityIssueRow": "maintenance",
    "JobType": "maintenance",
    "MaintenanceAccessor": "maintenance",
    "Notification": "maintenance",
    "NotificationDataType": "maintenance",
    "NotificationLevel": "maintenance",
    # maps
    "LayerKind": "maps",
    "MapLayerSpec": "maps",
    "MapsAccessor": "maps",
    "MapSpec": "maps",
    # messaging
    "MessageConversation": "messaging",
    "MessagingAccessor": "messaging",
    "Recipient": "messaging",
    # metadata
    "BulkPatchError": "metadata",
    "BulkPatchResult": "metadata",
    "BulkSharingError": "metadata",
    "BulkSharingResult": "metadata",
    "MetadataAccessor": "metadata",
    "SearchHit": "metadata",
    "SearchResults": "metadata",
    # option_sets
    "OptionSetsAccessor": "option_sets",
    "OptionSpec": "option_sets",
    "UpsertReport": "option_sets",
    # organisation_unit_group_sets
    "OrganisationUnitGroupSet": "organisation_unit_group_sets",
    "OrganisationUnitGroupSetsAccessor": "organisation_unit_group_sets",
    # organisation_unit_groups
    "OrganisationUnitGroup": "organisation_unit_groups",
    "OrganisationUnitGroupsAccessor": "organisation_unit_groups",
    # organisation_unit_levels
    "OrganisationUnitLevel": "organisation_unit_levels",
    "OrganisationUnitLevelsAccessor": "organisation_unit_levels",
    # organisation_units
    "OrganisationUnit": "organisation_units",
    "OrganisationUnitsAccessor": "organisation_units",
    # periods
    "PeriodType": "periods",
    "RelativePeriod": "periods",
    # predictor_groups
    "PredictorGroup": "predictor_groups",
    "PredictorGroupsAccessor": "predictor_groups",
    # predictors
    "Predictor": "predictors",
    "PredictorsAccessor": "predictors",
    # program_indicator_groups
    "ProgramIndicatorGroup": "program_indicator_groups",
    "ProgramIndicatorGroupsAccessor": "program_indicator_groups",
    # program_indicators
    "ProgramIndicator": "program_indicators",
    "ProgramIndicatorsAccessor": "program_indicators",
    # program_rules
    "ProgramRulesAccessor": "program_rules",
    # program_stages
    "ProgramStage": "program_stages",
    "ProgramStagesAccessor": "program_stages",
    # programs
    "Program": "programs",
    "ProgramsAccessor": "programs",
    # retry
    "RetryPolicy": "retry",
    # sections
    "Section": "sections",
    "SectionsAccessor": "sections",
    # sharing
    "ACCESS_NONE": "sharing",
    "ACCESS_READ_DATA": "sharing",
    "ACCESS_READ_METADATA": "sharing",
    "ACCESS_READ_WRITE_DATA": "sharing",
    "ACCESS_READ_WRITE_METADATA": "sharing",
    "Sharing": "sharing",
    "SharingBuilder": "sharing",
    "SharingObject": "sharing",
    "access_string": "sharing",
    "apply_sharing": "sharing",
    "get_sharing": "sharing",
    # sql_views
    "SqlViewColumn": "sql_views",
    "SqlViewResult": "sql_views",
    "SqlViewRunner": "sql_views",
    "SqlViewsAccessor": "sql_views",
    # system
    "DhisCalendar": "system",
    "DisplayRef": "system",
    "Me": "system",
    "SystemInfo": "system",
    "SystemModule": "system",
    # system_cache
    "SystemCache": "system_cache",
    # tasks
    "TaskCompletion": "tasks",
    "TaskModule": "tasks",
    "TaskTimeoutError": "tasks",
    "parse_task_ref": "tasks",
    # tracked_entity_attributes
    "TrackedEntityAttribute": "tracked_entity_attributes",
    "TrackedEntityAttributesAccessor": "tracked_entity_attributes",
    # tracked_entity_types
    "TrackedEntityType": "tracked_entity_types",
    "TrackedEntityTypesAccessor": "tracked_entity_types",
    # tracker
    "EnrollResult": "tracker",
    "EventResult": "tracker",
    "OutstandingEnrollment": "tracker",
    "RegisterResult": "tracker",
    "TrackerAccessor": "tracker",
    # uids
    "UID_ALPHABET": "uids",
    "UID_LENGTH": "uids",
    "UID_LETTERS": "uids",
    "UID_RE": "uids",
    "generate_uid": "uids",
    "generate_uids": "uids",
    "is_valid_uid": "uids",
    # validation
    "ExpressionContext": "validation",
    "ExpressionDescription": "validation",
    "ValidationAccessor": "validation",
    "ValidationAnalysisResult": "validation",
    # validation_rule_groups
    "ValidationRuleGroup": "validation_rule_groups",
    "ValidationRuleGroupsAccessor": "validation_rule_groups",
    # validation_rules
    "ValidationRule": "validation_rules",
    "ValidationRulesAccessor": "validation_rules",
    # visualizations
    "DimensionAxis": "visualizations",
    "VisualizationsAccessor": "visualizations",
    "VisualizationSpec": "visualizations",
}


def __getattr__(name: str) -> Any:
    """Lazily load attribute `name` from its source submodule on first access."""
    submodule_name = _LAZY_EXPORTS.get(name)
    if submodule_name is None:
        raise AttributeError(f"module 'dhis2_client' has no attribute {name!r}")
    module = import_module(f".{submodule_name}", __package__)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    """Expose lazy exports to `dir()` and IDE introspection."""
    return sorted(set(globals()) | set(_LAZY_EXPORTS))


if TYPE_CHECKING:
    # Eager imports for static type-checkers (mypy, pyright) and IDE autocomplete.
    # These never run at import time — TYPE_CHECKING is False outside the type-checker.
    from dhis2_client.aggregate import DataValue, DataValueSet
    from dhis2_client.analytics import AnalyticsMetaData, Grid, GridHeader
    from dhis2_client.analytics_stream import AnalyticsAccessor
    from dhis2_client.apps import (
        App,
        AppHubApp,
        AppHubVersion,
        AppsAccessor,
        AppSnapshotEntry,
        AppsSnapshot,
        AppStatus,
        AppType,
        RestoreOutcome,
        RestoreSummary,
    )
    from dhis2_client.attribute_values import AttributeValuesAccessor
    from dhis2_client.auth.base import AuthProvider
    from dhis2_client.auth.basic import BasicAuth
    from dhis2_client.auth.oauth2 import OAuth2Auth, OAuth2Token, TokenStore
    from dhis2_client.auth.pat import PatAuth
    from dhis2_client.auth_schemes import (
        ApiHeadersAuthScheme,
        ApiQueryParamsAuthScheme,
        ApiTokenAuthScheme,
        AuthScheme,
        AuthSchemeAdapter,
        HttpBasicAuthScheme,
        OAuth2ClientCredentialsAuthScheme,
        auth_scheme_from_route,
    )
    from dhis2_client.categories import CategoriesAccessor, Category
    from dhis2_client.category_combo_builder import (
        CategoryBuildEntry,
        CategoryComboBuildResult,
        CategoryComboBuildSpec,
        CategoryOptionSpec,
        CategorySpec,
        build_category_combo,
    )
    from dhis2_client.category_combos import CategoryCombo, CategoryCombosAccessor
    from dhis2_client.category_option_combos import CategoryOptionCombo, CategoryOptionCombosAccessor
    from dhis2_client.category_option_group_sets import CategoryOptionGroupSet, CategoryOptionGroupSetsAccessor
    from dhis2_client.category_option_groups import CategoryOptionGroup, CategoryOptionGroupsAccessor
    from dhis2_client.category_options import CategoryOption, CategoryOptionsAccessor
    from dhis2_client.client import Dhis2Client
    from dhis2_client.customize import CustomizationResult, CustomizeAccessor, LoginCustomization
    from dhis2_client.dashboards import DashboardsAccessor, DashboardSlot
    from dhis2_client.data_element_group_sets import DataElementGroupSet, DataElementGroupSetsAccessor
    from dhis2_client.data_element_groups import DataElementGroup, DataElementGroupsAccessor
    from dhis2_client.data_elements import DataElement, DataElementsAccessor
    from dhis2_client.data_sets import DataSet, DataSetsAccessor
    from dhis2_client.data_values import DataValuesAccessor
    from dhis2_client.envelopes import (
        Conflict,
        ConflictRow,
        ErrorReport,
        ImportCount,
        ImportReport,
        ObjectReport,
        Stats,
        TypeReport,
        WebMessageResponse,
    )
    from dhis2_client.errors import (
        AuthenticationError,
        Dhis2ApiError,
        Dhis2ClientError,
        OAuth2FlowError,
        UnsupportedVersionError,
    )
    from dhis2_client.files import Document, FileResource, FileResourceDomain, FilesAccessor
    from dhis2_client.generated import Dhis2
    from dhis2_client.indicator_group_sets import IndicatorGroupSet, IndicatorGroupSetsAccessor
    from dhis2_client.indicator_groups import IndicatorGroup, IndicatorGroupsAccessor
    from dhis2_client.indicators import Indicator, IndicatorsAccessor
    from dhis2_client.json_patch import (
        AddOp,
        CopyOp,
        JsonPatchOp,
        JsonPatchOpAdapter,
        MoveOp,
        RemoveOp,
        ReplaceOp,
        TestOp,
    )
    from dhis2_client.legend_sets import (
        Legend,
        LegendSet,
        LegendSetsAccessor,
        LegendSetSpec,
        LegendSpec,
    )
    from dhis2_client.maintenance import (
        DataIntegrityCheck,
        DataIntegrityIssue,
        DataIntegrityReport,
        DataIntegrityResult,
        IntegrityIssueRow,
        JobType,
        MaintenanceAccessor,
        Notification,
        NotificationDataType,
        NotificationLevel,
    )
    from dhis2_client.maps import LayerKind, MapLayerSpec, MapsAccessor, MapSpec
    from dhis2_client.messaging import MessageConversation, MessagingAccessor, Recipient
    from dhis2_client.metadata import (
        BulkPatchError,
        BulkPatchResult,
        BulkSharingError,
        BulkSharingResult,
        MetadataAccessor,
        SearchHit,
        SearchResults,
    )
    from dhis2_client.option_sets import OptionSetsAccessor, OptionSpec, UpsertReport
    from dhis2_client.organisation_unit_group_sets import (
        OrganisationUnitGroupSet,
        OrganisationUnitGroupSetsAccessor,
    )
    from dhis2_client.organisation_unit_groups import OrganisationUnitGroup, OrganisationUnitGroupsAccessor
    from dhis2_client.organisation_unit_levels import OrganisationUnitLevel, OrganisationUnitLevelsAccessor
    from dhis2_client.organisation_units import OrganisationUnit, OrganisationUnitsAccessor
    from dhis2_client.periods import PeriodType, RelativePeriod
    from dhis2_client.predictor_groups import PredictorGroup, PredictorGroupsAccessor
    from dhis2_client.predictors import Predictor, PredictorsAccessor
    from dhis2_client.program_indicator_groups import ProgramIndicatorGroup, ProgramIndicatorGroupsAccessor
    from dhis2_client.program_indicators import ProgramIndicator, ProgramIndicatorsAccessor
    from dhis2_client.program_rules import ProgramRulesAccessor
    from dhis2_client.program_stages import ProgramStage, ProgramStagesAccessor
    from dhis2_client.programs import Program, ProgramsAccessor
    from dhis2_client.retry import RetryPolicy
    from dhis2_client.sections import Section, SectionsAccessor
    from dhis2_client.sharing import (
        ACCESS_NONE,
        ACCESS_READ_DATA,
        ACCESS_READ_METADATA,
        ACCESS_READ_WRITE_DATA,
        ACCESS_READ_WRITE_METADATA,
        Sharing,
        SharingBuilder,
        SharingObject,
        access_string,
        apply_sharing,
        get_sharing,
    )
    from dhis2_client.sql_views import (
        SqlViewColumn,
        SqlViewResult,
        SqlViewRunner,
        SqlViewsAccessor,
    )
    from dhis2_client.system import DhisCalendar, DisplayRef, Me, SystemInfo, SystemModule
    from dhis2_client.system_cache import SystemCache
    from dhis2_client.tasks import TaskCompletion, TaskModule, TaskTimeoutError, parse_task_ref
    from dhis2_client.tracked_entity_attributes import TrackedEntityAttribute, TrackedEntityAttributesAccessor
    from dhis2_client.tracked_entity_types import TrackedEntityType, TrackedEntityTypesAccessor
    from dhis2_client.tracker import (
        EnrollResult,
        EventResult,
        OutstandingEnrollment,
        RegisterResult,
        TrackerAccessor,
    )
    from dhis2_client.uids import (
        UID_ALPHABET,
        UID_LENGTH,
        UID_LETTERS,
        UID_RE,
        generate_uid,
        generate_uids,
        is_valid_uid,
    )
    from dhis2_client.validation import (
        ExpressionContext,
        ExpressionDescription,
        ValidationAccessor,
        ValidationAnalysisResult,
    )
    from dhis2_client.validation_rule_groups import ValidationRuleGroup, ValidationRuleGroupsAccessor
    from dhis2_client.validation_rules import ValidationRule, ValidationRulesAccessor
    from dhis2_client.visualizations import DimensionAxis, VisualizationsAccessor, VisualizationSpec


__all__ = [
    "ACCESS_NONE",
    "ACCESS_READ_DATA",
    "ACCESS_READ_METADATA",
    "ACCESS_READ_WRITE_DATA",
    "ACCESS_READ_WRITE_METADATA",
    "AddOp",
    "AnalyticsAccessor",
    "AnalyticsMetaData",
    "ApiHeadersAuthScheme",
    "ApiQueryParamsAuthScheme",
    "ApiTokenAuthScheme",
    "App",
    "AppHubApp",
    "AppHubVersion",
    "AppSnapshotEntry",
    "AppStatus",
    "AppType",
    "AppsAccessor",
    "AppsSnapshot",
    "AttributeValuesAccessor",
    "AuthProvider",
    "AuthScheme",
    "AuthSchemeAdapter",
    "AuthenticationError",
    "BasicAuth",
    "BulkPatchError",
    "BulkPatchResult",
    "BulkSharingError",
    "BulkSharingResult",
    "CategoriesAccessor",
    "Category",
    "CategoryBuildEntry",
    "CategoryCombo",
    "CategoryComboBuildResult",
    "CategoryComboBuildSpec",
    "CategoryCombosAccessor",
    "CategoryOption",
    "CategoryOptionCombo",
    "CategoryOptionCombosAccessor",
    "CategoryOptionGroup",
    "CategoryOptionSpec",
    "CategorySpec",
    "CategoryOptionGroupSet",
    "CategoryOptionGroupSetsAccessor",
    "CategoryOptionGroupsAccessor",
    "CategoryOptionsAccessor",
    "Conflict",
    "ConflictRow",
    "CopyOp",
    "CustomizationResult",
    "CustomizeAccessor",
    "DashboardSlot",
    "DashboardsAccessor",
    "DataElement",
    "DataElementGroup",
    "DataElementGroupSet",
    "DataElementGroupSetsAccessor",
    "DataElementGroupsAccessor",
    "DataElementsAccessor",
    "DataIntegrityCheck",
    "DataIntegrityIssue",
    "DataIntegrityReport",
    "DataIntegrityResult",
    "DataSet",
    "DataSetsAccessor",
    "DataValue",
    "DataValueSet",
    "DataValuesAccessor",
    "Dhis2",
    "Dhis2ApiError",
    "Dhis2Client",
    "Dhis2ClientError",
    "DhisCalendar",
    "DimensionAxis",
    "DisplayRef",
    "Document",
    "EnrollResult",
    "ErrorReport",
    "EventResult",
    "ExpressionContext",
    "ExpressionDescription",
    "FileResource",
    "FileResourceDomain",
    "FilesAccessor",
    "Grid",
    "GridHeader",
    "HttpBasicAuthScheme",
    "ImportCount",
    "ImportReport",
    "Indicator",
    "IndicatorGroup",
    "IndicatorGroupSet",
    "IndicatorGroupSetsAccessor",
    "IndicatorGroupsAccessor",
    "IndicatorsAccessor",
    "IntegrityIssueRow",
    "JobType",
    "JsonPatchOp",
    "JsonPatchOpAdapter",
    "LayerKind",
    "Legend",
    "LegendSet",
    "LegendSetSpec",
    "LegendSetsAccessor",
    "LegendSpec",
    "LoginCustomization",
    "MaintenanceAccessor",
    "MapLayerSpec",
    "MapSpec",
    "MapsAccessor",
    "Me",
    "MessageConversation",
    "MessagingAccessor",
    "MetadataAccessor",
    "MoveOp",
    "Notification",
    "NotificationDataType",
    "NotificationLevel",
    "OAuth2Auth",
    "OAuth2ClientCredentialsAuthScheme",
    "OAuth2FlowError",
    "OAuth2Token",
    "ObjectReport",
    "OptionSetsAccessor",
    "OptionSpec",
    "OrganisationUnit",
    "OrganisationUnitGroup",
    "OrganisationUnitGroupSet",
    "OrganisationUnitGroupSetsAccessor",
    "OrganisationUnitGroupsAccessor",
    "OrganisationUnitLevel",
    "OrganisationUnitLevelsAccessor",
    "OrganisationUnitsAccessor",
    "OutstandingEnrollment",
    "PatAuth",
    "PeriodType",
    "Predictor",
    "PredictorGroup",
    "PredictorGroupsAccessor",
    "PredictorsAccessor",
    "ProgramIndicator",
    "ProgramIndicatorGroup",
    "ProgramIndicatorGroupsAccessor",
    "ProgramIndicatorsAccessor",
    "Program",
    "ProgramRulesAccessor",
    "ProgramStage",
    "ProgramStagesAccessor",
    "ProgramsAccessor",
    "Recipient",
    "RegisterResult",
    "RelativePeriod",
    "RestoreOutcome",
    "RestoreSummary",
    "RemoveOp",
    "ReplaceOp",
    "RetryPolicy",
    "SearchHit",
    "SearchResults",
    "Section",
    "SectionsAccessor",
    "Sharing",
    "SharingBuilder",
    "SharingObject",
    "SqlViewColumn",
    "SqlViewResult",
    "SqlViewRunner",
    "SqlViewsAccessor",
    "Stats",
    "SystemCache",
    "SystemInfo",
    "SystemModule",
    "TaskCompletion",
    "TaskModule",
    "TaskTimeoutError",
    "TestOp",
    "TokenStore",
    "TrackedEntityAttribute",
    "TrackedEntityAttributesAccessor",
    "TrackedEntityType",
    "TrackedEntityTypesAccessor",
    "TrackerAccessor",
    "TypeReport",
    "UID_ALPHABET",
    "UID_LENGTH",
    "UID_LETTERS",
    "UID_RE",
    "UnsupportedVersionError",
    "UpsertReport",
    "ValidationAccessor",
    "ValidationAnalysisResult",
    "ValidationRule",
    "ValidationRuleGroup",
    "ValidationRuleGroupsAccessor",
    "ValidationRulesAccessor",
    "VisualizationSpec",
    "VisualizationsAccessor",
    "WebMessageResponse",
    "access_string",
    "apply_sharing",
    "auth_scheme_from_route",
    "build_category_combo",
    "generate_uid",
    "generate_uids",
    "get_sharing",
    "is_valid_uid",
    "parse_task_ref",
]
