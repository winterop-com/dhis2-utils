"""Generated DHIS2 StrEnums from /api/openapi.json. Do not edit by hand."""
# ruff: noqa: E501

from __future__ import annotations

from enum import StrEnum


class AccessLevel(StrEnum):
    """AccessLevel."""

    OPEN = "OPEN"
    AUDITED = "AUDITED"
    PROTECTED = "PROTECTED"
    CLOSED = "CLOSED"


class AggregateDataExchangePropertyNames(StrEnum):
    """AggregateDataExchangePropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    SHARING = "sharing"
    SOURCE = "source"
    TARGET = "target"
    TRANSLATIONS = "translations"


class AggregationType(StrEnum):
    """AggregationType."""

    SUM = "SUM"
    AVERAGE = "AVERAGE"
    AVERAGE_SUM_ORG_UNIT = "AVERAGE_SUM_ORG_UNIT"
    LAST = "LAST"
    LAST_AVERAGE_ORG_UNIT = "LAST_AVERAGE_ORG_UNIT"
    LAST_LAST_ORG_UNIT = "LAST_LAST_ORG_UNIT"
    LAST_IN_PERIOD = "LAST_IN_PERIOD"
    LAST_IN_PERIOD_AVERAGE_ORG_UNIT = "LAST_IN_PERIOD_AVERAGE_ORG_UNIT"
    FIRST = "FIRST"
    FIRST_AVERAGE_ORG_UNIT = "FIRST_AVERAGE_ORG_UNIT"
    FIRST_FIRST_ORG_UNIT = "FIRST_FIRST_ORG_UNIT"
    COUNT = "COUNT"
    STDDEV = "STDDEV"
    VARIANCE = "VARIANCE"
    MIN = "MIN"
    MAX = "MAX"
    MIN_SUM_ORG_UNIT = "MIN_SUM_ORG_UNIT"
    MAX_SUM_ORG_UNIT = "MAX_SUM_ORG_UNIT"
    NONE = "NONE"
    CUSTOM = "CUSTOM"
    DEFAULT = "DEFAULT"


class AnalyticsCacheTtlMode(StrEnum):
    """AnalyticsCacheTtlMode."""

    FIXED = "FIXED"
    PROGRESSIVE = "PROGRESSIVE"


class AnalyticsFavoriteType(StrEnum):
    """AnalyticsFavoriteType."""

    VISUALIZATION = "VISUALIZATION"
    EVENT_VISUALIZATION = "EVENT_VISUALIZATION"
    MAP = "MAP"
    EVENT_REPORT = "EVENT_REPORT"
    EVENT_CHART = "EVENT_CHART"
    DATASET_REPORT = "DATASET_REPORT"


class AnalyticsFinancialYearStartKey(StrEnum):
    """AnalyticsFinancialYearStartKey."""

    FINANCIAL_YEAR_APRIL = "FINANCIAL_YEAR_APRIL"
    FINANCIAL_YEAR_JULY = "FINANCIAL_YEAR_JULY"
    FINANCIAL_YEAR_OCTOBER = "FINANCIAL_YEAR_OCTOBER"


class AnalyticsOutlierDetectionAlgorithm(StrEnum):
    """AnalyticsOutlierDetectionAlgorithm."""

    Z_SCORE = "Z_SCORE"
    MIN_MAX = "MIN_MAX"
    MODIFIED_Z_SCORE = "MODIFIED_Z_SCORE"


class AnalyticsPeriodBoundaryType(StrEnum):
    """AnalyticsPeriodBoundaryType."""

    BEFORE_START_OF_REPORTING_PERIOD = "BEFORE_START_OF_REPORTING_PERIOD"
    BEFORE_END_OF_REPORTING_PERIOD = "BEFORE_END_OF_REPORTING_PERIOD"
    AFTER_START_OF_REPORTING_PERIOD = "AFTER_START_OF_REPORTING_PERIOD"
    AFTER_END_OF_REPORTING_PERIOD = "AFTER_END_OF_REPORTING_PERIOD"


class AnalyticsTableHookPropertyNames(StrEnum):
    """AnalyticsTableHookPropertyNames."""

    ACCESS = "access"
    ANALYTICSTABLETYPE = "analyticsTableType"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    PHASE = "phase"
    RESOURCETABLETYPE = "resourceTableType"
    SHARING = "sharing"
    SQL = "sql"
    TRANSLATIONS = "translations"


class AnalyticsTablePhase(StrEnum):
    """AnalyticsTablePhase."""

    RESOURCE_TABLE_POPULATED = "RESOURCE_TABLE_POPULATED"
    ANALYTICS_TABLE_POPULATED = "ANALYTICS_TABLE_POPULATED"


class AnalyticsTableType(StrEnum):
    """AnalyticsTableType."""

    DATA_VALUE = "DATA_VALUE"
    COMPLETENESS = "COMPLETENESS"
    COMPLETENESS_TARGET = "COMPLETENESS_TARGET"
    ORG_UNIT_TARGET = "ORG_UNIT_TARGET"
    VALIDATION_RESULT = "VALIDATION_RESULT"
    EVENT = "EVENT"
    ENROLLMENT = "ENROLLMENT"
    OWNERSHIP = "OWNERSHIP"
    TRACKED_ENTITY_INSTANCE_EVENTS = "TRACKED_ENTITY_INSTANCE_EVENTS"
    TRACKED_ENTITY_INSTANCE_ENROLLMENTS = "TRACKED_ENTITY_INSTANCE_ENROLLMENTS"
    TRACKED_ENTITY_INSTANCE = "TRACKED_ENTITY_INSTANCE"


class AnalyticsType(StrEnum):
    """AnalyticsType."""

    EVENT = "EVENT"
    ENROLLMENT = "ENROLLMENT"


class ApiTokenPropertyNames(StrEnum):
    """ApiTokenPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    ATTRIBUTES = "attributes"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DISPLAYNAME = "displayName"
    EXPIRE = "expire"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    SHARING = "sharing"
    TRANSLATIONS = "translations"
    TYPE = "type"
    VERSION = "version"


class ApiTokenType(StrEnum):
    """ApiTokenType."""

    PERSONAL_ACCESS_TOKEN_V1 = "PERSONAL_ACCESS_TOKEN_V1"
    PERSONAL_ACCESS_TOKEN_V2 = "PERSONAL_ACCESS_TOKEN_V2"


class AppStatus(StrEnum):
    """AppStatus."""

    OK = "OK"
    INVALID_BUNDLED_APP_OVERRIDE = "INVALID_BUNDLED_APP_OVERRIDE"
    INVALID_CORE_APP = "INVALID_CORE_APP"
    NAMESPACE_TAKEN = "NAMESPACE_TAKEN"
    NAMESPACE_INVALID = "NAMESPACE_INVALID"
    INVALID_ZIP_FORMAT = "INVALID_ZIP_FORMAT"
    MISSING_MANIFEST = "MISSING_MANIFEST"
    INVALID_MANIFEST_JSON = "INVALID_MANIFEST_JSON"
    INSTALLATION_FAILED = "INSTALLATION_FAILED"
    NOT_FOUND = "NOT_FOUND"
    MISSING_SYSTEM_BASE_URL = "MISSING_SYSTEM_BASE_URL"
    APPROVED = "APPROVED"
    PENDING = "PENDING"
    NOT_APPROVED = "NOT_APPROVED"
    DELETION_IN_PROGRESS = "DELETION_IN_PROGRESS"


class AppStorageSource(StrEnum):
    """AppStorageSource."""

    LOCAL = "LOCAL"
    JCLOUDS = "JCLOUDS"
    BUNDLED = "BUNDLED"


class AppType(StrEnum):
    """AppType."""

    APP = "APP"
    RESOURCE = "RESOURCE"
    DASHBOARD_WIDGET = "DASHBOARD_WIDGET"


class AssignedUserSelectionMode(StrEnum):
    """AssignedUserSelectionMode."""

    CURRENT = "CURRENT"
    PROVIDED = "PROVIDED"
    NONE = "NONE"
    ANY = "ANY"
    ALL = "ALL"


class AtomicMode(StrEnum):
    """AtomicMode."""

    ALL = "ALL"
    NONE = "NONE"


class AttributePropertyNames(StrEnum):
    """AttributePropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CATEGORYATTRIBUTE = "categoryAttribute"
    CATEGORYOPTIONATTRIBUTE = "categoryOptionAttribute"
    CATEGORYOPTIONCOMBOATTRIBUTE = "categoryOptionComboAttribute"
    CATEGORYOPTIONGROUPATTRIBUTE = "categoryOptionGroupAttribute"
    CATEGORYOPTIONGROUPSETATTRIBUTE = "categoryOptionGroupSetAttribute"
    CODE = "code"
    CONSTANTATTRIBUTE = "constantAttribute"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATAELEMENTATTRIBUTE = "dataElementAttribute"
    DATAELEMENTGROUPATTRIBUTE = "dataElementGroupAttribute"
    DATAELEMENTGROUPSETATTRIBUTE = "dataElementGroupSetAttribute"
    DATASETATTRIBUTE = "dataSetAttribute"
    DESCRIPTION = "description"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    DOCUMENTATTRIBUTE = "documentAttribute"
    EVENTCHARTATTRIBUTE = "eventChartAttribute"
    EVENTREPORTATTRIBUTE = "eventReportAttribute"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    INDICATORATTRIBUTE = "indicatorAttribute"
    INDICATORGROUPATTRIBUTE = "indicatorGroupAttribute"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSETATTRIBUTE = "legendSetAttribute"
    MANDATORY = "mandatory"
    MAPATTRIBUTE = "mapAttribute"
    NAME = "name"
    OBJECTTYPES = "objectTypes"
    OPTIONATTRIBUTE = "optionAttribute"
    OPTIONSET = "optionSet"
    OPTIONSETATTRIBUTE = "optionSetAttribute"
    ORGANISATIONUNITATTRIBUTE = "organisationUnitAttribute"
    ORGANISATIONUNITGROUPATTRIBUTE = "organisationUnitGroupAttribute"
    ORGANISATIONUNITGROUPSETATTRIBUTE = "organisationUnitGroupSetAttribute"
    PROGRAMATTRIBUTE = "programAttribute"
    PROGRAMINDICATORATTRIBUTE = "programIndicatorAttribute"
    PROGRAMSTAGEATTRIBUTE = "programStageAttribute"
    RELATIONSHIPTYPEATTRIBUTE = "relationshipTypeAttribute"
    SECTIONATTRIBUTE = "sectionAttribute"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    SORTORDER = "sortOrder"
    SQLVIEWATTRIBUTE = "sqlViewAttribute"
    TRACKEDENTITYATTRIBUTEATTRIBUTE = "trackedEntityAttributeAttribute"
    TRACKEDENTITYTYPEATTRIBUTE = "trackedEntityTypeAttribute"
    TRANSLATIONS = "translations"
    UNIQUE = "unique"
    USERATTRIBUTE = "userAttribute"
    USERGROUPATTRIBUTE = "userGroupAttribute"
    VALIDATIONRULEATTRIBUTE = "validationRuleAttribute"
    VALIDATIONRULEGROUPATTRIBUTE = "validationRuleGroupAttribute"
    VALUETYPE = "valueType"
    VISUALIZATIONATTRIBUTE = "visualizationAttribute"


class AuditOperationType(StrEnum):
    """AuditOperationType."""

    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    READ = "READ"
    SEARCH = "SEARCH"


class AuthorityType(StrEnum):
    """AuthorityType."""

    CREATE = "CREATE"
    DATA_CREATE = "DATA_CREATE"
    CREATE_PUBLIC = "CREATE_PUBLIC"
    CREATE_PRIVATE = "CREATE_PRIVATE"
    EXTERNALIZE = "EXTERNALIZE"
    READ = "READ"
    DATA_READ = "DATA_READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class AxisType(StrEnum):
    """AxisType."""

    DOMAIN = "DOMAIN"
    RANGE = "RANGE"


class BaseDimensionalObjectPropertyNames(StrEnum):
    """BaseDimensionalObjectPropertyNames."""

    ACCESS = "access"
    AGGREGATIONTYPE = "aggregationType"
    ALLITEMS = "allItems"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATADIMENSION = "dataDimension"
    DATADIMENSIONTYPE = "dataDimensionType"
    DESCRIPTION = "description"
    DIMENSION = "dimension"
    DIMENSIONITEMKEYWORDS = "dimensionItemKeywords"
    DIMENSIONTYPE = "dimensionType"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FILTER = "filter"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    ITEMS = "items"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    NAME = "name"
    OPTIONSET = "optionSet"
    PROGRAM = "program"
    PROGRAMSTAGE = "programStage"
    REPETITION = "repetition"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    TRANSLATIONS = "translations"
    VALUETYPE = "valueType"


class BindType(StrEnum):
    """BindType."""

    BIND_TX = "BIND_TX"
    BIND_RX = "BIND_RX"
    BIND_TRX = "BIND_TRX"


class CacheStrategy(StrEnum):
    """CacheStrategy."""

    NO_CACHE = "NO_CACHE"
    CACHE_1_MINUTE = "CACHE_1_MINUTE"
    CACHE_5_MINUTES = "CACHE_5_MINUTES"
    CACHE_10_MINUTES = "CACHE_10_MINUTES"
    CACHE_15_MINUTES = "CACHE_15_MINUTES"
    CACHE_30_MINUTES = "CACHE_30_MINUTES"
    CACHE_1_HOUR = "CACHE_1_HOUR"
    CACHE_6AM_TOMORROW = "CACHE_6AM_TOMORROW"
    CACHE_TWO_WEEKS = "CACHE_TWO_WEEKS"
    RESPECT_SYSTEM_SETTING = "RESPECT_SYSTEM_SETTING"


class Cacheability(StrEnum):
    """Cacheability."""

    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


class CategoryComboPropertyNames(StrEnum):
    """CategoryComboPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CATEGORIES = "categories"
    CATEGORYOPTIONCOMBOS = "categoryOptionCombos"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATADIMENSIONTYPE = "dataDimensionType"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    ISDEFAULT = "isDefault"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    SHARING = "sharing"
    SKIPTOTAL = "skipTotal"
    TRANSLATIONS = "translations"


class CategoryOptionComboPropertyNames(StrEnum):
    """CategoryOptionComboPropertyNames."""

    ACCESS = "access"
    AGGREGATIONTYPE = "aggregationType"
    ATTRIBUTEVALUES = "attributeValues"
    CATEGORYCOMBO = "categoryCombo"
    CATEGORYOPTIONS = "categoryOptions"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DIMENSIONITEM = "dimensionItem"
    DIMENSIONITEMTYPE = "dimensionItemType"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    IGNOREAPPROVAL = "ignoreApproval"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    LEGENDSETS = "legendSets"
    QUERYMODS = "queryMods"
    SHARING = "sharing"
    TRANSLATIONS = "translations"


class CategoryOptionGroupPropertyNames(StrEnum):
    """CategoryOptionGroupPropertyNames."""

    ACCESS = "access"
    AGGREGATIONTYPE = "aggregationType"
    ATTRIBUTEVALUES = "attributeValues"
    CATEGORYOPTIONS = "categoryOptions"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATADIMENSIONTYPE = "dataDimensionType"
    DESCRIPTION = "description"
    DIMENSIONITEM = "dimensionItem"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    GROUPSETS = "groupSets"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    LEGENDSETS = "legendSets"
    NAME = "name"
    QUERYMODS = "queryMods"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    TRANSLATIONS = "translations"


class CategoryOptionGroupSetPropertyNames(StrEnum):
    """CategoryOptionGroupSetPropertyNames."""

    ACCESS = "access"
    AGGREGATIONTYPE = "aggregationType"
    ALLITEMS = "allItems"
    ATTRIBUTEVALUES = "attributeValues"
    CATEGORYOPTIONGROUPS = "categoryOptionGroups"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATADIMENSION = "dataDimension"
    DATADIMENSIONTYPE = "dataDimensionType"
    DESCRIPTION = "description"
    DIMENSION = "dimension"
    DIMENSIONITEMKEYWORDS = "dimensionItemKeywords"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FILTER = "filter"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    ITEMS = "items"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    NAME = "name"
    OPTIONSET = "optionSet"
    PROGRAM = "program"
    PROGRAMSTAGE = "programStage"
    REPETITION = "repetition"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    TRANSLATIONS = "translations"
    VALUETYPE = "valueType"


class CategoryOptionPropertyNames(StrEnum):
    """CategoryOptionPropertyNames."""

    ACCESS = "access"
    AGGREGATIONTYPE = "aggregationType"
    ATTRIBUTEVALUES = "attributeValues"
    CATEGORIES = "categories"
    CATEGORYOPTIONCOMBOS = "categoryOptionCombos"
    CATEGORYOPTIONGROUPS = "categoryOptionGroups"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DIMENSIONITEM = "dimensionItem"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    ENDDATE = "endDate"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    ISDEFAULT = "isDefault"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    LEGENDSETS = "legendSets"
    NAME = "name"
    ORGANISATIONUNITS = "organisationUnits"
    QUERYMODS = "queryMods"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    STARTDATE = "startDate"
    STYLE = "style"
    TRANSLATIONS = "translations"


class CategoryPropertyNames(StrEnum):
    """CategoryPropertyNames."""

    ACCESS = "access"
    AGGREGATIONTYPE = "aggregationType"
    ALLITEMS = "allItems"
    ATTRIBUTEVALUES = "attributeValues"
    CATEGORYCOMBOS = "categoryCombos"
    CATEGORYOPTIONS = "categoryOptions"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATADIMENSION = "dataDimension"
    DATADIMENSIONTYPE = "dataDimensionType"
    DESCRIPTION = "description"
    DIMENSION = "dimension"
    DIMENSIONITEMKEYWORDS = "dimensionItemKeywords"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FILTER = "filter"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    ITEMS = "items"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    NAME = "name"
    OPTIONSET = "optionSet"
    PROGRAM = "program"
    PROGRAMSTAGE = "programStage"
    REPETITION = "repetition"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    TRANSLATIONS = "translations"
    VALUETYPE = "valueType"


class CompletenessMethod(StrEnum):
    """CompletenessMethod."""

    ALL_DATAVALUE = "ALL_DATAVALUE"
    AT_LEAST_ONE_DATAVALUE = "AT_LEAST_ONE_DATAVALUE"
    DO_NOT_MARK_COMPLETE = "DO_NOT_MARK_COMPLETE"


class ConstantPropertyNames(StrEnum):
    """ConstantPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    TRANSLATIONS = "translations"
    VALUE = "value"


class ContentType(StrEnum):
    """ContentType."""

    APPLICATION_JSON = "APPLICATION_JSON"
    APPLICATION_XML = "APPLICATION_XML"
    TEXT_PLAIN = "TEXT_PLAIN"
    FORM_URL_ENCODED = "FORM_URL_ENCODED"


class CsvImportClass(StrEnum):
    """CsvImportClass."""

    ORGANISATION_UNIT_GROUP_MEMBERSHIP = "ORGANISATION_UNIT_GROUP_MEMBERSHIP"
    DATA_ELEMENT_GROUP_MEMBERSHIP = "DATA_ELEMENT_GROUP_MEMBERSHIP"
    INDICATOR_GROUP_MEMBERSHIP = "INDICATOR_GROUP_MEMBERSHIP"
    DATA_ELEMENT = "DATA_ELEMENT"
    DATA_ELEMENT_GROUP = "DATA_ELEMENT_GROUP"
    CATEGORY_OPTION = "CATEGORY_OPTION"
    CATEGORY = "CATEGORY"
    CATEGORY_COMBO = "CATEGORY_COMBO"
    CATEGORY_OPTION_GROUP = "CATEGORY_OPTION_GROUP"
    ORGANISATION_UNIT = "ORGANISATION_UNIT"
    ORGANISATION_UNIT_GROUP = "ORGANISATION_UNIT_GROUP"
    VALIDATION_RULE = "VALIDATION_RULE"
    OPTION_SET = "OPTION_SET"
    OPTION_GROUP = "OPTION_GROUP"
    OPTION_GROUP_SET = "OPTION_GROUP_SET"
    OPTION_GROUP_SET_MEMBERSHIP = "OPTION_GROUP_SET_MEMBERSHIP"
    INDICATOR = "INDICATOR"


class DashboardItemPropertyNames(StrEnum):
    """DashboardItemPropertyNames."""

    ACCESS = "access"
    APPKEY = "appKey"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CONTENTCOUNT = "contentCount"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DISPLAYNAME = "displayName"
    EVENTCHART = "eventChart"
    EVENTREPORT = "eventReport"
    EVENTVISUALIZATION = "eventVisualization"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HEIGHT = "height"
    HREF = "href"
    ID = "id"
    INTERPRETATIONCOUNT = "interpretationCount"
    INTERPRETATIONLIKECOUNT = "interpretationLikeCount"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    MAP = "map"
    MESSAGES = "messages"
    NAME = "name"
    REPORTS = "reports"
    RESOURCES = "resources"
    SHAPE = "shape"
    SHARING = "sharing"
    TEXT = "text"
    TRANSLATIONS = "translations"
    TYPE = "type"
    USERS = "users"
    VISUALIZATION = "visualization"
    WIDTH = "width"
    X = "x"
    Y = "y"


class DashboardItemShape(StrEnum):
    """DashboardItemShape."""

    NORMAL = "NORMAL"
    DOUBLE_WIDTH = "DOUBLE_WIDTH"
    FULL_WIDTH = "FULL_WIDTH"


class DashboardItemType(StrEnum):
    """DashboardItemType."""

    VISUALIZATION = "VISUALIZATION"
    EVENT_VISUALIZATION = "EVENT_VISUALIZATION"
    EVENT_CHART = "EVENT_CHART"
    MAP = "MAP"
    EVENT_REPORT = "EVENT_REPORT"
    USERS = "USERS"
    REPORTS = "REPORTS"
    RESOURCES = "RESOURCES"
    TEXT = "TEXT"
    MESSAGES = "MESSAGES"
    APP = "APP"


class DashboardPropertyNames(StrEnum):
    """DashboardPropertyNames."""

    ACCESS = "access"
    ALLOWEDFILTERS = "allowedFilters"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DASHBOARDITEMS = "dashboardItems"
    DESCRIPTION = "description"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    EMBEDDED = "embedded"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    ITEMCONFIG = "itemConfig"
    ITEMCOUNT = "itemCount"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LAYOUT = "layout"
    NAME = "name"
    RESTRICTFILTERS = "restrictFilters"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    TRANSLATIONS = "translations"


class DataApprovalLevelPropertyNames(StrEnum):
    """DataApprovalLevelPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CATEGORYOPTIONGROUPSET = "categoryOptionGroupSet"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEVEL = "level"
    NAME = "name"
    ORGUNITLEVEL = "orgUnitLevel"
    ORGUNITLEVELNAME = "orgUnitLevelName"
    SHARING = "sharing"
    TRANSLATIONS = "translations"


class DataApprovalState(StrEnum):
    """DataApprovalState."""

    UNAPPROVABLE = "UNAPPROVABLE"
    UNAPPROVED_ABOVE = "UNAPPROVED_ABOVE"
    UNAPPROVED_WAITING = "UNAPPROVED_WAITING"
    UNAPPROVED_READY = "UNAPPROVED_READY"
    APPROVED_ABOVE = "APPROVED_ABOVE"
    APPROVED_HERE = "APPROVED_HERE"
    ACCEPTED_HERE = "ACCEPTED_HERE"


class DataApprovalWorkflowPropertyNames(StrEnum):
    """DataApprovalWorkflowPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CATEGORYCOMBO = "categoryCombo"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATAAPPROVALLEVELS = "dataApprovalLevels"
    DATASETS = "dataSets"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    PERIODTYPE = "periodType"
    SHARING = "sharing"
    TRANSLATIONS = "translations"


class DataDimensionItemType(StrEnum):
    """DataDimensionItemType."""

    INDICATOR = "INDICATOR"
    DATA_ELEMENT = "DATA_ELEMENT"
    DATA_ELEMENT_OPERAND = "DATA_ELEMENT_OPERAND"
    REPORTING_RATE = "REPORTING_RATE"
    PROGRAM_INDICATOR = "PROGRAM_INDICATOR"
    PROGRAM_DATA_ELEMENT = "PROGRAM_DATA_ELEMENT"
    PROGRAM_DATA_ELEMENT_OPTION = "PROGRAM_DATA_ELEMENT_OPTION"
    PROGRAM_ATTRIBUTE = "PROGRAM_ATTRIBUTE"
    PROGRAM_ATTRIBUTE_OPTION = "PROGRAM_ATTRIBUTE_OPTION"
    EXPRESSION_DIMENSION_ITEM = "EXPRESSION_DIMENSION_ITEM"
    SUBEXPRESSION_DIMENSION_ITEM = "SUBEXPRESSION_DIMENSION_ITEM"
    VALIDATION_RULE = "VALIDATION_RULE"


class DataDimensionType(StrEnum):
    """DataDimensionType."""

    DISAGGREGATION = "DISAGGREGATION"
    ATTRIBUTE = "ATTRIBUTE"


class DataElementDomain(StrEnum):
    """DataElementDomain."""

    AGGREGATE = "AGGREGATE"
    TRACKER = "TRACKER"


class DataElementGroupPropertyNames(StrEnum):
    """DataElementGroupPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATAELEMENTS = "dataElements"
    DESCRIPTION = "description"
    DIMENSIONITEM = "dimensionItem"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    GROUPSETS = "groupSets"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    LEGENDSETS = "legendSets"
    NAME = "name"
    QUERYMODS = "queryMods"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    TRANSLATIONS = "translations"


class DataElementGroupSetPropertyNames(StrEnum):
    """DataElementGroupSetPropertyNames."""

    ACCESS = "access"
    AGGREGATIONTYPE = "aggregationType"
    ALLITEMS = "allItems"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    COMPULSORY = "compulsory"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATADIMENSION = "dataDimension"
    DATADIMENSIONTYPE = "dataDimensionType"
    DATAELEMENTGROUPS = "dataElementGroups"
    DESCRIPTION = "description"
    DIMENSION = "dimension"
    DIMENSIONITEMKEYWORDS = "dimensionItemKeywords"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FILTER = "filter"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    ITEMS = "items"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    NAME = "name"
    OPTIONSET = "optionSet"
    PROGRAM = "program"
    PROGRAMSTAGE = "programStage"
    REPETITION = "repetition"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    TRANSLATIONS = "translations"
    VALUETYPE = "valueType"


class DataElementOperandPropertyNames(StrEnum):
    """DataElementOperandPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEOPTIONCOMBO = "attributeOptionCombo"
    ATTRIBUTEVALUES = "attributeValues"
    CATEGORYOPTIONCOMBO = "categoryOptionCombo"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATAELEMENT = "dataElement"
    DESCRIPTION = "description"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    HREF = "href"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    LEGENDSETS = "legendSets"
    QUERYMODS = "queryMods"
    SHARING = "sharing"
    TRANSLATIONS = "translations"


class DataElementPropertyNames(StrEnum):
    """DataElementPropertyNames."""

    ACCESS = "access"
    AGGREGATIONLEVELS = "aggregationLevels"
    AGGREGATIONTYPE = "aggregationType"
    ATTRIBUTEVALUES = "attributeValues"
    CATEGORYCOMBO = "categoryCombo"
    CODE = "code"
    COMMENTOPTIONSET = "commentOptionSet"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATAELEMENTGROUPS = "dataElementGroups"
    DATASETELEMENTS = "dataSetElements"
    DESCRIPTION = "description"
    DIMENSIONITEM = "dimensionItem"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    DOMAINTYPE = "domainType"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FIELDMASK = "fieldMask"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    LEGENDSETS = "legendSets"
    NAME = "name"
    OPTIONSET = "optionSet"
    OPTIONSETVALUE = "optionSetValue"
    QUERYMODS = "queryMods"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    STYLE = "style"
    TRANSLATIONS = "translations"
    URL = "url"
    VALUETYPE = "valueType"
    VALUETYPEOPTIONS = "valueTypeOptions"
    ZEROISSIGNIFICANT = "zeroIsSignificant"


class DataEntryFormPropertyNames(StrEnum):
    """DataEntryFormPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMAT = "format"
    HREF = "href"
    HTMLCODE = "htmlCode"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    SHARING = "sharing"
    STYLE = "style"
    TRANSLATIONS = "translations"


class DataIntegrityReportType(StrEnum):
    """DataIntegrityReportType."""

    REPORT = "REPORT"
    SUMMARY = "SUMMARY"
    DETAILS = "DETAILS"


class DataIntegritySeverity(StrEnum):
    """DataIntegritySeverity."""

    INFO = "INFO"
    WARNING = "WARNING"
    SEVERE = "SEVERE"
    CRITICAL = "CRITICAL"


class DataMergeStrategy(StrEnum):
    """DataMergeStrategy."""

    LAST_UPDATED = "LAST_UPDATED"
    DISCARD = "DISCARD"


class DataSetNotificationRecipient(StrEnum):
    """DataSetNotificationRecipient."""

    ORGANISATION_UNIT_CONTACT = "ORGANISATION_UNIT_CONTACT"
    USER_GROUP = "USER_GROUP"


class DataSetNotificationTemplatePropertyNames(StrEnum):
    """DataSetNotificationTemplatePropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATASETNOTIFICATIONTRIGGER = "dataSetNotificationTrigger"
    DATASETS = "dataSets"
    DELIVERYCHANNELS = "deliveryChannels"
    DISPLAYMESSAGETEMPLATE = "displayMessageTemplate"
    DISPLAYNAME = "displayName"
    DISPLAYSUBJECTTEMPLATE = "displaySubjectTemplate"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    MESSAGETEMPLATE = "messageTemplate"
    NAME = "name"
    NOTIFICATIONRECIPIENT = "notificationRecipient"
    NOTIFYPARENTORGANISATIONUNITONLY = "notifyParentOrganisationUnitOnly"
    NOTIFYUSERSINHIERARCHYONLY = "notifyUsersInHierarchyOnly"
    RECIPIENTUSERGROUP = "recipientUserGroup"
    RELATIVESCHEDULEDDAYS = "relativeScheduledDays"
    SENDSTRATEGY = "sendStrategy"
    SHARING = "sharing"
    SUBJECTTEMPLATE = "subjectTemplate"
    TRANSLATIONS = "translations"


class DataSetNotificationTrigger(StrEnum):
    """DataSetNotificationTrigger."""

    DATA_SET_COMPLETION = "DATA_SET_COMPLETION"
    SCHEDULED_DAYS = "SCHEDULED_DAYS"


class DataSetPropertyNames(StrEnum):
    """DataSetPropertyNames."""

    ACCESS = "access"
    AGGREGATIONTYPE = "aggregationType"
    ATTRIBUTEVALUES = "attributeValues"
    CATEGORYCOMBO = "categoryCombo"
    CODE = "code"
    COMPULSORYDATAELEMENTOPERANDS = "compulsoryDataElementOperands"
    COMPULSORYFIELDSCOMPLETEONLY = "compulsoryFieldsCompleteOnly"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATAELEMENTDECORATION = "dataElementDecoration"
    DATAENTRYFORM = "dataEntryForm"
    DATAINPUTPERIODS = "dataInputPeriods"
    DATASETELEMENTS = "dataSetElements"
    DESCRIPTION = "description"
    DIMENSIONITEM = "dimensionItem"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYOPTIONS = "displayOptions"
    DISPLAYSHORTNAME = "displayShortName"
    EXPIRYDAYS = "expiryDays"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FIELDCOMBINATIONREQUIRED = "fieldCombinationRequired"
    FORMNAME = "formName"
    FORMTYPE = "formType"
    HREF = "href"
    ID = "id"
    INDICATORS = "indicators"
    INTERPRETATIONS = "interpretations"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    LEGENDSETS = "legendSets"
    MOBILE = "mobile"
    NAME = "name"
    NOVALUEREQUIRESCOMMENT = "noValueRequiresComment"
    NOTIFICATIONRECIPIENTS = "notificationRecipients"
    NOTIFYCOMPLETINGUSER = "notifyCompletingUser"
    OPENFUTUREPERIODS = "openFuturePeriods"
    OPENPERIODSAFTERCOENDDATE = "openPeriodsAfterCoEndDate"
    ORGANISATIONUNITS = "organisationUnits"
    PERIODTYPE = "periodType"
    QUERYMODS = "queryMods"
    RENDERASTABS = "renderAsTabs"
    RENDERHORIZONTALLY = "renderHorizontally"
    SECTIONS = "sections"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    SKIPOFFLINE = "skipOffline"
    STYLE = "style"
    TIMELYDAYS = "timelyDays"
    TRANSLATIONS = "translations"
    VALIDCOMPLETEONLY = "validCompleteOnly"
    VERSION = "version"
    WORKFLOW = "workflow"


class DataStatisticsEventType(StrEnum):
    """DataStatisticsEventType."""

    VISUALIZATION_VIEW = "VISUALIZATION_VIEW"
    MAP_VIEW = "MAP_VIEW"
    EVENT_REPORT_VIEW = "EVENT_REPORT_VIEW"
    EVENT_CHART_VIEW = "EVENT_CHART_VIEW"
    EVENT_VISUALIZATION_VIEW = "EVENT_VISUALIZATION_VIEW"
    DASHBOARD_VIEW = "DASHBOARD_VIEW"
    PASSIVE_DASHBOARD_VIEW = "PASSIVE_DASHBOARD_VIEW"
    DATA_SET_REPORT_VIEW = "DATA_SET_REPORT_VIEW"
    TOTAL_VIEW = "TOTAL_VIEW"
    ACTIVE_USERS = "ACTIVE_USERS"


class DatePeriodType(StrEnum):
    """DatePeriodType."""

    RELATIVE = "RELATIVE"
    ABSOLUTE = "ABSOLUTE"


class DeduplicationStatus(StrEnum):
    """DeduplicationStatus."""

    ALL = "ALL"
    OPEN = "OPEN"
    INVALID = "INVALID"
    MERGED = "MERGED"


class Defaults(StrEnum):
    """Defaults."""

    INCLUDE = "INCLUDE"
    EXCLUDE = "EXCLUDE"


class DeliveryChannel(StrEnum):
    """DeliveryChannel."""

    SMS = "SMS"
    EMAIL = "EMAIL"
    HTTP = "HTTP"


class Dhis2OAuth2AuthorizationConsentPropertyNames(StrEnum):
    """Dhis2OAuth2AuthorizationConsentPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    AUTHORITIES = "authorities"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    PRINCIPALNAME = "principalName"
    REGISTEREDCLIENTID = "registeredClientId"
    SHARING = "sharing"
    TRANSLATIONS = "translations"


class Dhis2OAuth2AuthorizationPropertyNames(StrEnum):
    """Dhis2OAuth2AuthorizationPropertyNames."""

    ACCESS = "access"
    ACCESSTOKENEXPIRESAT = "accessTokenExpiresAt"
    ACCESSTOKENISSUEDAT = "accessTokenIssuedAt"
    ACCESSTOKENMETADATA = "accessTokenMetadata"
    ACCESSTOKENSCOPES = "accessTokenScopes"
    ACCESSTOKENTYPE = "accessTokenType"
    ACCESSTOKENVALUE = "accessTokenValue"
    ATTRIBUTEVALUES = "attributeValues"
    ATTRIBUTES = "attributes"
    AUTHORIZATIONCODEEXPIRESAT = "authorizationCodeExpiresAt"
    AUTHORIZATIONCODEISSUEDAT = "authorizationCodeIssuedAt"
    AUTHORIZATIONCODEMETADATA = "authorizationCodeMetadata"
    AUTHORIZATIONCODEVALUE = "authorizationCodeValue"
    AUTHORIZATIONGRANTTYPE = "authorizationGrantType"
    AUTHORIZEDSCOPES = "authorizedScopes"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DEVICECODEEXPIRESAT = "deviceCodeExpiresAt"
    DEVICECODEISSUEDAT = "deviceCodeIssuedAt"
    DEVICECODEMETADATA = "deviceCodeMetadata"
    DEVICECODEVALUE = "deviceCodeValue"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    OIDCIDTOKENCLAIMS = "oidcIdTokenClaims"
    OIDCIDTOKENEXPIRESAT = "oidcIdTokenExpiresAt"
    OIDCIDTOKENISSUEDAT = "oidcIdTokenIssuedAt"
    OIDCIDTOKENMETADATA = "oidcIdTokenMetadata"
    OIDCIDTOKENVALUE = "oidcIdTokenValue"
    PRINCIPALNAME = "principalName"
    REFRESHTOKENEXPIRESAT = "refreshTokenExpiresAt"
    REFRESHTOKENISSUEDAT = "refreshTokenIssuedAt"
    REFRESHTOKENMETADATA = "refreshTokenMetadata"
    REFRESHTOKENVALUE = "refreshTokenValue"
    REGISTEREDCLIENTID = "registeredClientId"
    SHARING = "sharing"
    STATE = "state"
    TRANSLATIONS = "translations"
    USERCODEEXPIRESAT = "userCodeExpiresAt"
    USERCODEISSUEDAT = "userCodeIssuedAt"
    USERCODEMETADATA = "userCodeMetadata"
    USERCODEVALUE = "userCodeValue"


class Dhis2OAuth2ClientPropertyNames(StrEnum):
    """Dhis2OAuth2ClientPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    AUTHORIZATIONGRANTTYPES = "authorizationGrantTypes"
    CLIENTAUTHENTICATIONMETHODS = "clientAuthenticationMethods"
    CLIENTID = "clientId"
    CLIENTIDISSUEDAT = "clientIdIssuedAt"
    CLIENTSECRET = "clientSecret"
    CLIENTSECRETEXPIRESAT = "clientSecretExpiresAt"
    CLIENTSETTINGS = "clientSettings"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    POSTLOGOUTREDIRECTURIS = "postLogoutRedirectUris"
    REDIRECTURIS = "redirectUris"
    SCOPES = "scopes"
    SHARING = "sharing"
    TOKENSETTINGS = "tokenSettings"
    TRANSLATIONS = "translations"


class DigitGroupSeparator(StrEnum):
    """DigitGroupSeparator."""

    COMMA = "COMMA"
    SPACE = "SPACE"
    NONE = "NONE"


class DimensionAttribute(StrEnum):
    """DimensionAttribute."""

    COLUMN = "COLUMN"
    ROW = "ROW"
    FILTER = "FILTER"


class DimensionItemType(StrEnum):
    """DimensionItemType."""

    DATA_ELEMENT = "DATA_ELEMENT"
    DATA_ELEMENT_OPERAND = "DATA_ELEMENT_OPERAND"
    INDICATOR = "INDICATOR"
    REPORTING_RATE = "REPORTING_RATE"
    PROGRAM_DATA_ELEMENT = "PROGRAM_DATA_ELEMENT"
    PROGRAM_DATA_ELEMENT_OPTION = "PROGRAM_DATA_ELEMENT_OPTION"
    PROGRAM_ATTRIBUTE = "PROGRAM_ATTRIBUTE"
    PROGRAM_ATTRIBUTE_OPTION = "PROGRAM_ATTRIBUTE_OPTION"
    PROGRAM_INDICATOR = "PROGRAM_INDICATOR"
    PERIOD = "PERIOD"
    ORGANISATION_UNIT = "ORGANISATION_UNIT"
    CATEGORY_OPTION = "CATEGORY_OPTION"
    OPTION_GROUP = "OPTION_GROUP"
    DATA_ELEMENT_GROUP = "DATA_ELEMENT_GROUP"
    ORGANISATION_UNIT_GROUP = "ORGANISATION_UNIT_GROUP"
    CATEGORY_OPTION_GROUP = "CATEGORY_OPTION_GROUP"
    EXPRESSION_DIMENSION_ITEM = "EXPRESSION_DIMENSION_ITEM"
    SUBEXPRESSION_DIMENSION_ITEM = "SUBEXPRESSION_DIMENSION_ITEM"


class DimensionType(StrEnum):
    """DimensionType."""

    DATA_X = "DATA_X"
    PROGRAM_DATA_ELEMENT = "PROGRAM_DATA_ELEMENT"
    PROGRAM_ATTRIBUTE = "PROGRAM_ATTRIBUTE"
    PROGRAM_INDICATOR = "PROGRAM_INDICATOR"
    DATA_COLLAPSED = "DATA_COLLAPSED"
    CATEGORY_OPTION_COMBO = "CATEGORY_OPTION_COMBO"
    ATTRIBUTE_OPTION_COMBO = "ATTRIBUTE_OPTION_COMBO"
    PERIOD = "PERIOD"
    ORGANISATION_UNIT = "ORGANISATION_UNIT"
    CATEGORY_OPTION_GROUP_SET = "CATEGORY_OPTION_GROUP_SET"
    DATA_ELEMENT_GROUP_SET = "DATA_ELEMENT_GROUP_SET"
    ORGANISATION_UNIT_GROUP_SET = "ORGANISATION_UNIT_GROUP_SET"
    ORGANISATION_UNIT_GROUP = "ORGANISATION_UNIT_GROUP"
    CATEGORY = "CATEGORY"
    OPTION_GROUP_SET = "OPTION_GROUP_SET"
    VALIDATION_RULE = "VALIDATION_RULE"
    STATIC = "STATIC"
    ORGANISATION_UNIT_LEVEL = "ORGANISATION_UNIT_LEVEL"


class DisplayDensity(StrEnum):
    """DisplayDensity."""

    COMFORTABLE = "COMFORTABLE"
    NORMAL = "NORMAL"
    COMPACT = "COMPACT"
    NONE = "NONE"


class DisplayProperty(StrEnum):
    """DisplayProperty."""

    NAME = "NAME"
    SHORTNAME = "SHORTNAME"


class DocumentPropertyNames(StrEnum):
    """DocumentPropertyNames."""

    ACCESS = "access"
    ATTACHMENT = "attachment"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CONTENTTYPE = "contentType"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DISPLAYNAME = "displayName"
    EXTERNAL = "external"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    SHARING = "sharing"
    TRANSLATIONS = "translations"
    URL = "url"


class EmbeddedProvider(StrEnum):
    """EmbeddedProvider."""

    SUPERSET = "SUPERSET"


class EndpointAction(StrEnum):
    """EndpointAction."""

    AGGREGATE = "AGGREGATE"
    QUERY = "QUERY"
    OTHER = "OTHER"


class EndpointItem(StrEnum):
    """EndpointItem."""

    EVENT = "EVENT"
    ENROLLMENT = "ENROLLMENT"
    TRACKED_ENTITY_INSTANCE = "TRACKED_ENTITY_INSTANCE"


class EnrollmentStatus(StrEnum):
    """EnrollmentStatus."""

    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class EventDataType(StrEnum):
    """EventDataType."""

    AGGREGATED_VALUES = "AGGREGATED_VALUES"
    EVENTS = "EVENTS"


class EventFilterPropertyNames(StrEnum):
    """EventFilterPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYNAME = "displayName"
    EVENTQUERYCRITERIA = "eventQueryCriteria"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    PROGRAM = "program"
    PROGRAMSTAGE = "programStage"
    SHARING = "sharing"
    TRANSLATIONS = "translations"


class EventHookPropertyNames(StrEnum):
    """EventHookPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISABLED = "disabled"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    SHARING = "sharing"
    SOURCE = "source"
    TARGETS = "targets"
    TRANSLATIONS = "translations"


class EventInterval(StrEnum):
    """EventInterval."""

    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"


class EventOutputType(StrEnum):
    """EventOutputType."""

    EVENT = "EVENT"
    ENROLLMENT = "ENROLLMENT"
    TRACKED_ENTITY_INSTANCE = "TRACKED_ENTITY_INSTANCE"


class EventStatus(StrEnum):
    """EventStatus."""

    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    VISITED = "VISITED"
    SCHEDULE = "SCHEDULE"
    OVERDUE = "OVERDUE"
    SKIPPED = "SKIPPED"


class EventVisualizationType(StrEnum):
    """EventVisualizationType."""

    COLUMN = "COLUMN"
    STACKED_COLUMN = "STACKED_COLUMN"
    BAR = "BAR"
    STACKED_BAR = "STACKED_BAR"
    LINE = "LINE"
    LINE_LIST = "LINE_LIST"
    AREA = "AREA"
    STACKED_AREA = "STACKED_AREA"
    PIE = "PIE"
    RADAR = "RADAR"
    GAUGE = "GAUGE"
    YEAR_OVER_YEAR_LINE = "YEAR_OVER_YEAR_LINE"
    YEAR_OVER_YEAR_COLUMN = "YEAR_OVER_YEAR_COLUMN"
    SINGLE_VALUE = "SINGLE_VALUE"
    PIVOT_TABLE = "PIVOT_TABLE"
    SCATTER = "SCATTER"
    BUBBLE = "BUBBLE"


class ExpressionDimensionItemPropertyNames(StrEnum):
    """ExpressionDimensionItemPropertyNames."""

    ACCESS = "access"
    AGGREGATEEXPORTATTRIBUTEOPTIONCOMBO = "aggregateExportAttributeOptionCombo"
    AGGREGATEEXPORTCATEGORYOPTIONCOMBO = "aggregateExportCategoryOptionCombo"
    AGGREGATIONTYPE = "aggregationType"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DIMENSIONITEM = "dimensionItem"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    EXPRESSION = "expression"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    LEGENDSETS = "legendSets"
    MISSINGVALUESTRATEGY = "missingValueStrategy"
    NAME = "name"
    QUERYMODS = "queryMods"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    SLIDINGWINDOW = "slidingWindow"
    TRANSLATIONS = "translations"


class ExternalMapLayerPropertyNames(StrEnum):
    """ExternalMapLayerPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    ATTRIBUTION = "attribution"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    IMAGEFORMAT = "imageFormat"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LAYERS = "layers"
    LEGENDSET = "legendSet"
    LEGENDSETURL = "legendSetUrl"
    MAPLAYERPOSITION = "mapLayerPosition"
    MAPSERVICE = "mapService"
    NAME = "name"
    SHARING = "sharing"
    TRANSLATIONS = "translations"
    URL = "url"


class FailurePolicy(StrEnum):
    """FailurePolicy."""

    PARENT = "PARENT"
    FAIL = "FAIL"
    SKIP_STAGE = "SKIP_STAGE"
    SKIP_ITEM = "SKIP_ITEM"
    SKIP_ITEM_OUTLIER = "SKIP_ITEM_OUTLIER"


class FeatureType(StrEnum):
    """FeatureType."""

    NONE = "NONE"
    MULTI_POLYGON = "MULTI_POLYGON"
    POLYGON = "POLYGON"
    POINT = "POINT"
    SYMBOL = "SYMBOL"


class FileResourceDomain(StrEnum):
    """FileResourceDomain."""

    DATA_VALUE = "DATA_VALUE"
    PUSH_ANALYSIS = "PUSH_ANALYSIS"
    DOCUMENT = "DOCUMENT"
    MESSAGE_ATTACHMENT = "MESSAGE_ATTACHMENT"
    USER_AVATAR = "USER_AVATAR"
    ORG_UNIT = "ORG_UNIT"
    ICON = "ICON"
    JOB_DATA = "JOB_DATA"


class FileResourcePropertyNames(StrEnum):
    """FileResourcePropertyNames."""

    ACCESS = "access"
    ASSIGNED = "assigned"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CONTENTLENGTH = "contentLength"
    CONTENTMD5 = "contentMd5"
    CONTENTTYPE = "contentType"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DISPLAYNAME = "displayName"
    DOMAIN = "domain"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HASMULTIPLESTORAGEFILES = "hasMultipleStorageFiles"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    SHARING = "sharing"
    STORAGESTATUS = "storageStatus"
    TRANSLATIONS = "translations"


class FileResourceRetentionStrategy(StrEnum):
    """FileResourceRetentionStrategy."""

    NONE = "NONE"
    THREE_MONTHS = "THREE_MONTHS"
    ONE_YEAR = "ONE_YEAR"
    FOREVER = "FOREVER"


class FileResourceStorageStatus(StrEnum):
    """FileResourceStorageStatus."""

    NONE = "NONE"
    PENDING = "PENDING"
    STORED = "STORED"


class FlushMode(StrEnum):
    """FlushMode."""

    OBJECT = "OBJECT"
    AUTO = "AUTO"


class Font(StrEnum):
    """Font."""

    ARIAL = "ARIAL"
    SANS_SERIF = "SANS_SERIF"
    VERDANA = "VERDANA"
    ROBOTO = "ROBOTO"


class FontSize(StrEnum):
    """FontSize."""

    LARGE = "LARGE"
    NORMAL = "NORMAL"
    SMALL = "SMALL"


class FormType(StrEnum):
    """FormType."""

    DEFAULT = "DEFAULT"
    CUSTOM = "CUSTOM"
    SECTION = "SECTION"
    SECTION_MULTIORG = "SECTION_MULTIORG"


class GistAutoType(StrEnum):
    """GistAutoType."""

    XL = "XL"
    L = "L"
    M = "M"
    S = "S"
    XS = "XS"


class HideEmptyItemStrategy(StrEnum):
    """HideEmptyItemStrategy."""

    NONE = "NONE"
    BEFORE_FIRST = "BEFORE_FIRST"
    AFTER_LAST = "AFTER_LAST"
    BEFORE_FIRST_AFTER_LAST = "BEFORE_FIRST_AFTER_LAST"
    ALL = "ALL"


class IconType(StrEnum):
    """IconType."""

    DATA_ITEM = "DATA_ITEM"


class IconTypeFilter(StrEnum):
    """IconTypeFilter."""

    ALL = "ALL"
    CUSTOM = "CUSTOM"
    DEFAULT = "DEFAULT"


class IdentifiableObjectPropertyNames(StrEnum):
    """IdentifiableObjectPropertyNames."""

    ID = "id"


class IdentifiableProperty(StrEnum):
    """IdentifiableProperty."""

    ID = "ID"
    UID = "UID"
    UUID = "UUID"
    NAME = "NAME"
    CODE = "CODE"
    ATTRIBUTE = "ATTRIBUTE"


class ImageFileDimension(StrEnum):
    """ImageFileDimension."""

    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
    ORIGINAL = "ORIGINAL"


class ImageFormat(StrEnum):
    """ImageFormat."""

    PNG = "PNG"
    JPG = "JPG"


class ImportReportMode(StrEnum):
    """ImportReportMode."""

    FULL = "FULL"
    ERRORS = "ERRORS"
    ERRORS_NOT_OWNER = "ERRORS_NOT_OWNER"
    DEBUG = "DEBUG"


class ImportStatus(StrEnum):
    """ImportStatus."""

    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"


class ImportStrategy(StrEnum):
    """ImportStrategy."""

    CREATE = "CREATE"
    UPDATE = "UPDATE"
    CREATE_AND_UPDATE = "CREATE_AND_UPDATE"
    DELETE = "DELETE"
    SYNC = "SYNC"
    NEW_AND_UPDATES = "NEW_AND_UPDATES"
    NEW = "NEW"
    UPDATES = "UPDATES"
    DELETES = "DELETES"


class Importance(StrEnum):
    """Importance."""

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class In(StrEnum):
    """In."""

    QUERY = "query"
    PATH = "path"
    HEADER = "header"
    COOKIE = "cookie"


class Include(StrEnum):
    """Include."""

    FALSE = "FALSE"
    TRUE = "TRUE"
    AUTO = "AUTO"


class IncomingSmsPropertyNames(StrEnum):
    """IncomingSmsPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    GATEWAYID = "gatewayid"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    ORIGINATOR = "originator"
    RECEIVEDDATE = "receiveddate"
    SENTDATE = "sentdate"
    SHARING = "sharing"
    SMSENCODING = "smsencoding"
    SMSSTATUS = "smsstatus"
    TEXT = "text"
    TRANSLATIONS = "translations"


class IndicatorGroupPropertyNames(StrEnum):
    """IndicatorGroupPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    GROUPSETS = "groupSets"
    HREF = "href"
    ID = "id"
    INDICATORGROUPSET = "indicatorGroupSet"
    INDICATORS = "indicators"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    SHARING = "sharing"
    TRANSLATIONS = "translations"


class IndicatorGroupSetPropertyNames(StrEnum):
    """IndicatorGroupSetPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    COMPULSORY = "compulsory"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    INDICATORGROUPS = "indicatorGroups"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    TRANSLATIONS = "translations"


class IndicatorPropertyNames(StrEnum):
    """IndicatorPropertyNames."""

    ACCESS = "access"
    AGGREGATEEXPORTATTRIBUTEOPTIONCOMBO = "aggregateExportAttributeOptionCombo"
    AGGREGATEEXPORTCATEGORYOPTIONCOMBO = "aggregateExportCategoryOptionCombo"
    AGGREGATIONTYPE = "aggregationType"
    ANNUALIZED = "annualized"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATASETS = "dataSets"
    DECIMALS = "decimals"
    DENOMINATOR = "denominator"
    DENOMINATORDESCRIPTION = "denominatorDescription"
    DESCRIPTION = "description"
    DIMENSIONITEM = "dimensionItem"
    DISPLAYDENOMINATORDESCRIPTION = "displayDenominatorDescription"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYNUMERATORDESCRIPTION = "displayNumeratorDescription"
    DISPLAYSHORTNAME = "displayShortName"
    EXPLODEDDENOMINATOR = "explodedDenominator"
    EXPLODEDNUMERATOR = "explodedNumerator"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    INDICATORGROUPS = "indicatorGroups"
    INDICATORTYPE = "indicatorType"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    LEGENDSETS = "legendSets"
    NAME = "name"
    NUMERATOR = "numerator"
    NUMERATORDESCRIPTION = "numeratorDescription"
    QUERYMODS = "queryMods"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    STYLE = "style"
    TRANSLATIONS = "translations"
    URL = "url"


class IndicatorTypePropertyNames(StrEnum):
    """IndicatorTypePropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DISPLAYNAME = "displayName"
    FACTOR = "factor"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    NUMBER = "number"
    SHARING = "sharing"
    TRANSLATIONS = "translations"


class InterpretationPropertyNames(StrEnum):
    """InterpretationPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    COMMENTS = "comments"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATASET = "dataSet"
    DISPLAYNAME = "displayName"
    EVENTCHART = "eventChart"
    EVENTREPORT = "eventReport"
    EVENTVISUALIZATION = "eventVisualization"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LIKEDBY = "likedBy"
    LIKES = "likes"
    MAP = "map"
    MENTIONS = "mentions"
    ORGANISATIONUNIT = "organisationUnit"
    PERIOD = "period"
    SHARING = "sharing"
    TEXT = "text"
    TRANSLATIONS = "translations"
    TYPE = "type"
    VISUALIZATION = "visualization"


class JobConfigurationPropertyNames(StrEnum):
    """JobConfigurationPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CONFIGURABLE = "configurable"
    CREATED = "created"
    CREATEDBY = "createdBy"
    CRONEXPRESSION = "cronExpression"
    DELAY = "delay"
    DISPLAYNAME = "displayName"
    ENABLED = "enabled"
    ERRORCODES = "errorCodes"
    EXECUTEDBY = "executedBy"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    JOBPARAMETERS = "jobParameters"
    JOBSTATUS = "jobStatus"
    JOBTYPE = "jobType"
    LASTALIVE = "lastAlive"
    LASTEXECUTED = "lastExecuted"
    LASTEXECUTEDSTATUS = "lastExecutedStatus"
    LASTFINISHED = "lastFinished"
    LASTRUNTIMEEXECUTION = "lastRuntimeExecution"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEADERONLYJOB = "leaderOnlyJob"
    MAXDELAYEDEXECUTIONTIME = "maxDelayedExecutionTime"
    NAME = "name"
    NEXTEXECUTIONTIME = "nextExecutionTime"
    QUEUENAME = "queueName"
    QUEUEPOSITION = "queuePosition"
    SCHEDULINGTYPE = "schedulingType"
    SHARING = "sharing"
    TRANSLATIONS = "translations"
    USERUID = "userUid"


class JobProgressStatus(StrEnum):
    """JobProgressStatus."""

    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    CANCELLED = "CANCELLED"


class JobStatus(StrEnum):
    """JobStatus."""

    RUNNING = "RUNNING"
    SCHEDULED = "SCHEDULED"
    DISABLED = "DISABLED"
    COMPLETED = "COMPLETED"
    STOPPED = "STOPPED"
    FAILED = "FAILED"
    NOT_STARTED = "NOT_STARTED"


class JobType(StrEnum):
    """JobType."""

    DATA_INTEGRITY = "DATA_INTEGRITY"
    DATA_INTEGRITY_DETAILS = "DATA_INTEGRITY_DETAILS"
    RESOURCE_TABLE = "RESOURCE_TABLE"
    ANALYTICS_TABLE = "ANALYTICS_TABLE"
    CONTINUOUS_ANALYTICS_TABLE = "CONTINUOUS_ANALYTICS_TABLE"
    SINGLE_EVENT_DATA_SYNC = "SINGLE_EVENT_DATA_SYNC"
    TRACKED_ENTITY_DATA_SYNC = "TRACKED_ENTITY_DATA_SYNC"
    DATA_SYNC = "DATA_SYNC"
    META_DATA_SYNC = "META_DATA_SYNC"
    AGGREGATE_DATA_EXCHANGE = "AGGREGATE_DATA_EXCHANGE"
    SEND_SCHEDULED_MESSAGE = "SEND_SCHEDULED_MESSAGE"
    PROGRAM_NOTIFICATIONS = "PROGRAM_NOTIFICATIONS"
    MONITORING = "MONITORING"
    PUSH_ANALYSIS = "PUSH_ANALYSIS"
    HTML_PUSH_ANALYTICS = "HTML_PUSH_ANALYTICS"
    TRACKER_SEARCH_OPTIMIZATION = "TRACKER_SEARCH_OPTIMIZATION"
    PREDICTOR = "PREDICTOR"
    MATERIALIZED_SQL_VIEW_UPDATE = "MATERIALIZED_SQL_VIEW_UPDATE"
    DISABLE_INACTIVE_USERS = "DISABLE_INACTIVE_USERS"
    TEST = "TEST"
    LOCK_EXCEPTION_CLEANUP = "LOCK_EXCEPTION_CLEANUP"
    MOCK = "MOCK"
    SMS_SEND = "SMS_SEND"
    SMS_INBOUND_PROCESSING = "SMS_INBOUND_PROCESSING"
    TRACKER_IMPORT_JOB = "TRACKER_IMPORT_JOB"
    TRACKER_IMPORT_NOTIFICATION_JOB = "TRACKER_IMPORT_NOTIFICATION_JOB"
    TRACKER_IMPORT_RULE_ENGINE_JOB = "TRACKER_IMPORT_RULE_ENGINE_JOB"
    IMAGE_PROCESSING = "IMAGE_PROCESSING"
    COMPLETE_DATA_SET_REGISTRATION_IMPORT = "COMPLETE_DATA_SET_REGISTRATION_IMPORT"
    DATAVALUE_IMPORT_INTERNAL = "DATAVALUE_IMPORT_INTERNAL"
    METADATA_IMPORT = "METADATA_IMPORT"
    DATAVALUE_IMPORT = "DATAVALUE_IMPORT"
    GEOJSON_IMPORT = "GEOJSON_IMPORT"
    GML_IMPORT = "GML_IMPORT"
    HOUSEKEEPING = "HOUSEKEEPING"
    DATA_VALUE_TRIM = "DATA_VALUE_TRIM"
    DATA_SET_NOTIFICATION = "DATA_SET_NOTIFICATION"
    CREDENTIALS_EXPIRY_ALERT = "CREDENTIALS_EXPIRY_ALERT"
    DATA_STATISTICS = "DATA_STATISTICS"
    FILE_RESOURCE_CLEANUP = "FILE_RESOURCE_CLEANUP"
    ACCOUNT_EXPIRY_ALERT = "ACCOUNT_EXPIRY_ALERT"
    VALIDATION_RESULTS_NOTIFICATION = "VALIDATION_RESULTS_NOTIFICATION"
    REMOVE_USED_OR_EXPIRED_RESERVED_VALUES = "REMOVE_USED_OR_EXPIRED_RESERVED_VALUES"
    SYSTEM_VERSION_UPDATE_CHECK = "SYSTEM_VERSION_UPDATE_CHECK"


class Junction(StrEnum):
    """Junction."""

    AND = "AND"
    OR = "OR"


class JunctionType(StrEnum):
    """JunctionType."""

    AND = "AND"
    OR = "OR"


class LegendDisplayStrategy(StrEnum):
    """LegendDisplayStrategy."""

    FIXED = "FIXED"
    BY_DATA_ITEM = "BY_DATA_ITEM"


class LegendDisplayStyle(StrEnum):
    """LegendDisplayStyle."""

    FILL = "FILL"
    TEXT = "TEXT"


class LegendSetPropertyNames(StrEnum):
    """LegendSetPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDS = "legends"
    NAME = "name"
    SHARING = "sharing"
    SYMBOLIZER = "symbolizer"
    TRANSLATIONS = "translations"


class LockExceptionPropertyNames(StrEnum):
    """LockExceptionPropertyNames."""

    CREATED = "created"
    DATASET = "dataSet"
    NAME = "name"
    ORGANISATIONUNIT = "organisationUnit"
    PERIOD = "period"


class LockStatus(StrEnum):
    """LockStatus."""

    LOCKED = "LOCKED"
    APPROVED = "APPROVED"
    OPEN = "OPEN"


class LoginPageLayout(StrEnum):
    """LoginPageLayout."""

    DEFAULT = "DEFAULT"
    SIDEBAR = "SIDEBAR"
    CUSTOM = "CUSTOM"


class LoginResponseStatus(StrEnum):
    """LoginResponseStatus."""

    SUCCESS = "SUCCESS"
    ACCOUNT_DISABLED = "ACCOUNT_DISABLED"
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"
    ACCOUNT_EXPIRED = "ACCOUNT_EXPIRED"
    PASSWORD_EXPIRED = "PASSWORD_EXPIRED"
    EMAIL_TWO_FACTOR_CODE_SENT = "EMAIL_TWO_FACTOR_CODE_SENT"
    INCORRECT_TWO_FACTOR_CODE_TOTP = "INCORRECT_TWO_FACTOR_CODE_TOTP"
    INCORRECT_TWO_FACTOR_CODE_EMAIL = "INCORRECT_TWO_FACTOR_CODE_EMAIL"
    REQUIRES_TWO_FACTOR_ENROLMENT = "REQUIRES_TWO_FACTOR_ENROLMENT"


class MapLayerPosition(StrEnum):
    """MapLayerPosition."""

    BASEMAP = "BASEMAP"
    OVERLAY = "OVERLAY"


class MapPropertyNames(StrEnum):
    """MapPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    BASEMAP = "basemap"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    INTERPRETATIONS = "interpretations"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    MAPVIEWS = "mapViews"
    NAME = "name"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    SUBSCRIBED = "subscribed"
    SUBSCRIBERS = "subscribers"
    TITLE = "title"
    TRANSLATIONS = "translations"
    ZOOM = "zoom"


class MapService(StrEnum):
    """MapService."""

    WMS = "WMS"
    TMS = "TMS"
    XYZ = "XYZ"
    VECTOR_STYLE = "VECTOR_STYLE"
    GEOJSON_URL = "GEOJSON_URL"
    ARCGIS_FEATURE = "ARCGIS_FEATURE"


class MapViewRenderingStrategy(StrEnum):
    """MapViewRenderingStrategy."""

    SINGLE = "SINGLE"
    SPLIT_BY_PERIOD = "SPLIT_BY_PERIOD"
    TIMELINE = "TIMELINE"


class MeDtoPropertyNames(StrEnum):
    """MeDtoPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    AUTHORITIES = "authorities"
    AVATAR = "avatar"
    BIRTHDAY = "birthday"
    CREATED = "created"
    DATASETS = "dataSets"
    DATAVIEWORGANISATIONUNITS = "dataViewOrganisationUnits"
    DISPLAYNAME = "displayName"
    EDUCATION = "education"
    EMAIL = "email"
    EMAILVERIFIED = "emailVerified"
    EMPLOYER = "employer"
    EXTERNALACCESS = "externalAccess"
    FACEBOOKMESSENGER = "facebookMessenger"
    FAVORITES = "favorites"
    FIRSTNAME = "firstName"
    GENDER = "gender"
    ID = "id"
    IMPERSONATION = "impersonation"
    INTERESTS = "interests"
    INTRODUCTION = "introduction"
    JOBTITLE = "jobTitle"
    LANGUAGES = "languages"
    LASTUPDATED = "lastUpdated"
    NAME = "name"
    NATIONALITY = "nationality"
    ORGANISATIONUNITS = "organisationUnits"
    PATTOKENS = "patTokens"
    PHONENUMBER = "phoneNumber"
    PROGRAMS = "programs"
    SETTINGS = "settings"
    SHARING = "sharing"
    SKYPE = "skype"
    SURNAME = "surname"
    TEISEARCHORGANISATIONUNITS = "teiSearchOrganisationUnits"
    TELEGRAM = "telegram"
    TRANSLATIONS = "translations"
    TWITTER = "twitter"
    TWOFACTORTYPE = "twoFactorType"
    USERACCESSES = "userAccesses"
    USERGROUPACCESSES = "userGroupAccesses"
    USERGROUPS = "userGroups"
    USERROLES = "userRoles"
    USERNAME = "username"
    WHATSAPP = "whatsApp"


class MergeMode(StrEnum):
    """MergeMode."""

    REPLACE = "REPLACE"


class MergeStrategy(StrEnum):
    """MergeStrategy."""

    MANUAL = "MANUAL"
    AUTO = "AUTO"


class MergeType(StrEnum):
    """MergeType."""

    INDICATOR_TYPE = "INDICATOR_TYPE"
    INDICATOR = "INDICATOR"
    DATA_ELEMENT = "DATA_ELEMENT"
    CATEGORY_OPTION = "CATEGORY_OPTION"
    CATEGORY_OPTION_COMBO = "CATEGORY_OPTION_COMBO"


class MessageConversationPriority(StrEnum):
    """MessageConversationPriority."""

    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class MessageConversationPropertyNames(StrEnum):
    """MessageConversationPropertyNames."""

    ACCESS = "access"
    ASSIGNEE = "assignee"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DISPLAYNAME = "displayName"
    EXTMESSAGEID = "extMessageId"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FOLLOWUP = "followUp"
    HREF = "href"
    ID = "id"
    LASTMESSAGE = "lastMessage"
    LASTSENDER = "lastSender"
    LASTSENDERFIRSTNAME = "lastSenderFirstname"
    LASTSENDERSURNAME = "lastSenderSurname"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    MESSAGECOUNT = "messageCount"
    MESSAGETYPE = "messageType"
    MESSAGES = "messages"
    PRIORITY = "priority"
    READ = "read"
    SHARING = "sharing"
    STATUS = "status"
    SUBJECT = "subject"
    TRANSLATIONS = "translations"
    USERFIRSTNAME = "userFirstname"
    USERMESSAGES = "userMessages"
    USERSURNAME = "userSurname"


class MessageConversationStatus(StrEnum):
    """MessageConversationStatus."""

    NONE = "NONE"
    OPEN = "OPEN"
    PENDING = "PENDING"
    INVALID = "INVALID"
    SOLVED = "SOLVED"


class MessageType(StrEnum):
    """MessageType."""

    PRIVATE = "PRIVATE"
    SYSTEM = "SYSTEM"
    VALIDATION_RESULT = "VALIDATION_RESULT"
    TICKET = "TICKET"
    SYSTEM_VERSION_UPDATE = "SYSTEM_VERSION_UPDATE"


class MetadataProposalPropertyNames(StrEnum):
    """MetadataProposalPropertyNames."""

    CHANGE = "change"
    COMMENT = "comment"
    CREATED = "created"
    CREATEDBY = "createdBy"
    FINALISED = "finalised"
    FINALISEDBY = "finalisedBy"
    ID = "id"
    REASON = "reason"
    STATUS = "status"
    TARGET = "target"
    TARGETID = "targetId"
    TYPE = "type"


class MetadataProposalStatus(StrEnum):
    """MetadataProposalStatus."""

    PROPOSED = "PROPOSED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    NEEDS_UPDATE = "NEEDS_UPDATE"


class MetadataProposalTarget(StrEnum):
    """MetadataProposalTarget."""

    ORGANISATION_UNIT = "ORGANISATION_UNIT"


class MetadataProposalType(StrEnum):
    """MetadataProposalType."""

    ADD = "ADD"
    UPDATE = "UPDATE"
    REMOVE = "REMOVE"


class MissingValueStrategy(StrEnum):
    """MissingValueStrategy."""

    SKIP_IF_ANY_VALUE_MISSING = "SKIP_IF_ANY_VALUE_MISSING"
    SKIP_IF_ALL_VALUES_MISSING = "SKIP_IF_ALL_VALUES_MISSING"
    NEVER_SKIP = "NEVER_SKIP"


class NormalizedOutlierMethod(StrEnum):
    """NormalizedOutlierMethod."""

    Y_RESIDUALS_LINEAR = "Y_RESIDUALS_LINEAR"


class NotificationDataType(StrEnum):
    """NotificationDataType."""

    PARAMETERS = "PARAMETERS"


class NotificationLevel(StrEnum):
    """NotificationLevel."""

    OFF = "OFF"
    DEBUG = "DEBUG"
    LOOP = "LOOP"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


class NotificationTrigger(StrEnum):
    """NotificationTrigger."""

    ENROLLMENT = "ENROLLMENT"
    COMPLETION = "COMPLETION"
    PROGRAM_RULE = "PROGRAM_RULE"
    SCHEDULED_DAYS_DUE_DATE = "SCHEDULED_DAYS_DUE_DATE"
    SCHEDULED_DAYS_INCIDENT_DATE = "SCHEDULED_DAYS_INCIDENT_DATE"
    SCHEDULED_DAYS_ENROLLMENT_DATE = "SCHEDULED_DAYS_ENROLLMENT_DATE"


class NumberType(StrEnum):
    """NumberType."""

    VALUE = "VALUE"
    ROW_PERCENTAGE = "ROW_PERCENTAGE"
    COLUMN_PERCENTAGE = "COLUMN_PERCENTAGE"


class NumberingPlanIndicator(StrEnum):
    """NumberingPlanIndicator."""

    UNKNOWN = "UNKNOWN"
    ISDN = "ISDN"
    DATA = "DATA"
    TELEX = "TELEX"
    LAND_MOBILE = "LAND_MOBILE"
    NATIONAL = "NATIONAL"
    PRIVATE = "PRIVATE"
    ERMES = "ERMES"
    INTERNET = "INTERNET"
    WAP = "WAP"


class ObjectBundleMode(StrEnum):
    """ObjectBundleMode."""

    COMMIT = "COMMIT"
    VALIDATE = "VALIDATE"


class Operator(StrEnum):
    """Operator."""

    EQUAL_TO = "equal_to"
    NOT_EQUAL_TO = "not_equal_to"
    GREATER_THAN = "greater_than"
    GREATER_THAN_OR_EQUAL_TO = "greater_than_or_equal_to"
    LESS_THAN = "less_than"
    LESS_THAN_OR_EQUAL_TO = "less_than_or_equal_to"
    COMPULSORY_PAIR = "compulsory_pair"
    EXCLUSIVE_PAIR = "exclusive_pair"


class OptionGroupPropertyNames(StrEnum):
    """OptionGroupPropertyNames."""

    ACCESS = "access"
    AGGREGATIONTYPE = "aggregationType"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DIMENSIONITEM = "dimensionItem"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    LEGENDSETS = "legendSets"
    NAME = "name"
    OPTIONSET = "optionSet"
    OPTIONS = "options"
    QUERYMODS = "queryMods"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    TRANSLATIONS = "translations"


class OptionGroupSetPropertyNames(StrEnum):
    """OptionGroupSetPropertyNames."""

    ACCESS = "access"
    AGGREGATIONTYPE = "aggregationType"
    ALLITEMS = "allItems"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATADIMENSION = "dataDimension"
    DATADIMENSIONTYPE = "dataDimensionType"
    DESCRIPTION = "description"
    DIMENSION = "dimension"
    DIMENSIONITEMKEYWORDS = "dimensionItemKeywords"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FILTER = "filter"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    ITEMS = "items"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    NAME = "name"
    OPTIONGROUPS = "optionGroups"
    OPTIONSET = "optionSet"
    PROGRAM = "program"
    PROGRAMSTAGE = "programStage"
    REPETITION = "repetition"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    TRANSLATIONS = "translations"
    VALUETYPE = "valueType"


class OptionPropertyNames(StrEnum):
    """OptionPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    OPTIONSET = "optionSet"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    SORTORDER = "sortOrder"
    STYLE = "style"
    TRANSLATIONS = "translations"


class OptionSetPropertyNames(StrEnum):
    """OptionSetPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    OPTIONS = "options"
    SHARING = "sharing"
    TRANSLATIONS = "translations"
    VALUETYPE = "valueType"
    VERSION = "version"


class Order(StrEnum):
    """Order."""

    MEAN_ABS_DEV = "MEAN_ABS_DEV"
    Z_SCORE = "Z_SCORE"


class OrganisationUnitDescendants(StrEnum):
    """OrganisationUnitDescendants."""

    SELECTED = "SELECTED"
    DESCENDANTS = "DESCENDANTS"


class OrganisationUnitGroupPropertyNames(StrEnum):
    """OrganisationUnitGroupPropertyNames."""

    ACCESS = "access"
    AGGREGATIONTYPE = "aggregationType"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    COLOR = "color"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DIMENSIONITEM = "dimensionItem"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FEATURETYPE = "featureType"
    FORMNAME = "formName"
    GEOMETRY = "geometry"
    GROUPSETS = "groupSets"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    LEGENDSETS = "legendSets"
    NAME = "name"
    ORGANISATIONUNITS = "organisationUnits"
    QUERYMODS = "queryMods"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    SYMBOL = "symbol"
    TRANSLATIONS = "translations"


class OrganisationUnitGroupSetPropertyNames(StrEnum):
    """OrganisationUnitGroupSetPropertyNames."""

    ACCESS = "access"
    AGGREGATIONTYPE = "aggregationType"
    ALLITEMS = "allItems"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    COMPULSORY = "compulsory"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATADIMENSION = "dataDimension"
    DATADIMENSIONTYPE = "dataDimensionType"
    DESCRIPTION = "description"
    DIMENSION = "dimension"
    DIMENSIONITEMKEYWORDS = "dimensionItemKeywords"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FILTER = "filter"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    INCLUDESUBHIERARCHYINANALYTICS = "includeSubhierarchyInAnalytics"
    ITEMS = "items"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    NAME = "name"
    OPTIONSET = "optionSet"
    ORGANISATIONUNITGROUPS = "organisationUnitGroups"
    PROGRAM = "program"
    PROGRAMSTAGE = "programStage"
    REPETITION = "repetition"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    TRANSLATIONS = "translations"
    VALUETYPE = "valueType"


class OrganisationUnitLevelPropertyNames(StrEnum):
    """OrganisationUnitLevelPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEVEL = "level"
    NAME = "name"
    OFFLINELEVELS = "offlineLevels"
    SHARING = "sharing"
    TRANSLATIONS = "translations"


class OrganisationUnitPropertyNames(StrEnum):
    """OrganisationUnitPropertyNames."""

    ACCESS = "access"
    ADDRESS = "address"
    AGGREGATIONTYPE = "aggregationType"
    ANCESTORS = "ancestors"
    ATTRIBUTEVALUES = "attributeValues"
    CHILDREN = "children"
    CLOSEDDATE = "closedDate"
    CODE = "code"
    COMMENT = "comment"
    CONTACTPERSON = "contactPerson"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATASETS = "dataSets"
    DESCRIPTION = "description"
    DIMENSIONITEM = "dimensionItem"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    EMAIL = "email"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    GEOMETRY = "geometry"
    HREF = "href"
    ID = "id"
    IMAGE = "image"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEAF = "leaf"
    LEGENDSET = "legendSet"
    LEGENDSETS = "legendSets"
    LEVEL = "level"
    MEMBERCOUNT = "memberCount"
    NAME = "name"
    OPENINGDATE = "openingDate"
    ORGANISATIONUNITGROUPS = "organisationUnitGroups"
    PARENT = "parent"
    PATH = "path"
    PHONENUMBER = "phoneNumber"
    PROGRAMS = "programs"
    QUERYMODS = "queryMods"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    TRANSLATIONS = "translations"
    TYPE = "type"
    URL = "url"
    USERS = "users"


class OrganisationUnitSelectionMode(StrEnum):
    """OrganisationUnitSelectionMode."""

    SELECTED = "SELECTED"
    CHILDREN = "CHILDREN"
    DESCENDANTS = "DESCENDANTS"
    ACCESSIBLE = "ACCESSIBLE"
    CAPTURE = "CAPTURE"
    ALL = "ALL"


class OutboundMessageBatchStatus(StrEnum):
    """OutboundMessageBatchStatus."""

    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    PENDING = "PENDING"
    ABORTED = "ABORTED"


class OutboundSmsPropertyNames(StrEnum):
    """OutboundSmsPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATE = "date"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    MESSAGE = "message"
    NAME = "name"
    RECIPIENTS = "recipients"
    SENDER = "sender"
    SHARING = "sharing"
    STATUS = "status"
    SUBJECT = "subject"
    TRANSLATIONS = "translations"


class OutboundSmsStatus(StrEnum):
    """OutboundSmsStatus."""

    OUTBOUND = "OUTBOUND"
    SENT = "SENT"
    ERROR = "ERROR"
    PENDING = "PENDING"
    SCHEDULED = "SCHEDULED"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"


class OutlierDetectionAlgorithm(StrEnum):
    """OutlierDetectionAlgorithm."""

    Z_SCORE = "Z_SCORE"
    MIN_MAX = "MIN_MAX"
    MOD_Z_SCORE = "MOD_Z_SCORE"
    INVALID_NUMERIC = "INVALID_NUMERIC"


class OutlierMethod(StrEnum):
    """OutlierMethod."""

    IQR = "IQR"
    STANDARD_Z_SCORE = "STANDARD_Z_SCORE"
    MODIFIED_Z_SCORE = "MODIFIED_Z_SCORE"


class ParserType(StrEnum):
    """ParserType."""

    KEY_VALUE_PARSER = "KEY_VALUE_PARSER"
    ALERT_PARSER = "ALERT_PARSER"
    UNREGISTERED_PARSER = "UNREGISTERED_PARSER"
    TRACKED_ENTITY_REGISTRATION_PARSER = "TRACKED_ENTITY_REGISTRATION_PARSER"
    PROGRAM_STAGE_DATAENTRY_PARSER = "PROGRAM_STAGE_DATAENTRY_PARSER"
    EVENT_REGISTRATION_PARSER = "EVENT_REGISTRATION_PARSER"


class PeriodTypeEnum(StrEnum):
    """PeriodTypeEnum."""

    BI_MONTHLY = "BI_MONTHLY"
    BI_WEEKLY = "BI_WEEKLY"
    DAILY = "DAILY"
    FINANCIAL_APRIL = "FINANCIAL_APRIL"
    FINANCIAL_JULY = "FINANCIAL_JULY"
    FINANCIAL_NOV = "FINANCIAL_NOV"
    FINANCIAL_SEP = "FINANCIAL_SEP"
    FINANCIAL_OCT = "FINANCIAL_OCT"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    QUARTERLY_NOV = "QUARTERLY_NOV"
    SIX_MONTHLY_APRIL = "SIX_MONTHLY_APRIL"
    SIX_MONTHLY_NOV = "SIX_MONTHLY_NOV"
    SIX_MONTHLY = "SIX_MONTHLY"
    TWO_YEARLY = "TWO_YEARLY"
    WEEKLY = "WEEKLY"
    WEEKLY_SATURDAY = "WEEKLY_SATURDAY"
    WEEKLY_SUNDAY = "WEEKLY_SUNDAY"
    WEEKLY_THURSDAY = "WEEKLY_THURSDAY"
    WEEKLY_WEDNESDAY = "WEEKLY_WEDNESDAY"
    YEARLY = "YEARLY"


class Position(StrEnum):
    """Position."""

    START = "START"
    END = "END"


class PredictionStatus(StrEnum):
    """PredictionStatus."""

    SUCCESS = "SUCCESS"
    ERROR = "ERROR"


class PredictorGroupPropertyNames(StrEnum):
    """PredictorGroupPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    PREDICTORS = "predictors"
    SHARING = "sharing"
    TRANSLATIONS = "translations"


class PredictorPropertyNames(StrEnum):
    """PredictorPropertyNames."""

    ACCESS = "access"
    ANNUALSAMPLECOUNT = "annualSampleCount"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    GENERATOR = "generator"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    ORGANISATIONUNITDESCENDANTS = "organisationUnitDescendants"
    ORGANISATIONUNITLEVELS = "organisationUnitLevels"
    OUTPUT = "output"
    OUTPUTCOMBO = "outputCombo"
    PERIODTYPE = "periodType"
    PREDICTORGROUPS = "predictorGroups"
    SAMPLESKIPTEST = "sampleSkipTest"
    SEQUENTIALSAMPLECOUNT = "sequentialSampleCount"
    SEQUENTIALSKIPCOUNT = "sequentialSkipCount"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    TRANSLATIONS = "translations"


class PreheatIdentifier(StrEnum):
    """PreheatIdentifier."""

    UID = "UID"
    CODE = "CODE"


class PreheatMode(StrEnum):
    """PreheatMode."""

    REFERENCE = "REFERENCE"
    ALL = "ALL"
    NONE = "NONE"


class ProgramDataElementDimensionItemPropertyNames(StrEnum):
    """ProgramDataElementDimensionItemPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATAELEMENT = "dataElement"
    DESCRIPTION = "description"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    PROGRAM = "program"
    QUERYMODS = "queryMods"
    SHARING = "sharing"
    TRANSLATIONS = "translations"
    VALUETYPE = "valueType"


class ProgramIndicatorGroupPropertyNames(StrEnum):
    """ProgramIndicatorGroupPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    PROGRAMINDICATORS = "programIndicators"
    SHARING = "sharing"
    TRANSLATIONS = "translations"


class ProgramIndicatorPropertyNames(StrEnum):
    """ProgramIndicatorPropertyNames."""

    ACCESS = "access"
    AGGREGATEEXPORTATTRIBUTEOPTIONCOMBO = "aggregateExportAttributeOptionCombo"
    AGGREGATEEXPORTCATEGORYOPTIONCOMBO = "aggregateExportCategoryOptionCombo"
    AGGREGATEEXPORTDATAELEMENT = "aggregateExportDataElement"
    AGGREGATIONTYPE = "aggregationType"
    ANALYTICSPERIODBOUNDARIES = "analyticsPeriodBoundaries"
    ANALYTICSTYPE = "analyticsType"
    ATTRIBUTECOMBO = "attributeCombo"
    ATTRIBUTEVALUES = "attributeValues"
    CATEGORYCOMBO = "categoryCombo"
    CATEGORYMAPPINGIDS = "categoryMappingIds"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DECIMALS = "decimals"
    DESCRIPTION = "description"
    DIMENSIONITEM = "dimensionItem"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYINFORM = "displayInForm"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    EXPRESSION = "expression"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FILTER = "filter"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    LEGENDSETS = "legendSets"
    NAME = "name"
    ORGUNITFIELD = "orgUnitField"
    PROGRAM = "program"
    PROGRAMINDICATORGROUPS = "programIndicatorGroups"
    QUERYMODS = "queryMods"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    STYLE = "style"
    TRANSLATIONS = "translations"


class ProgramMessagePropertyNames(StrEnum):
    """ProgramMessagePropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DELIVERYCHANNELS = "deliveryChannels"
    DISPLAYNAME = "displayName"
    ENROLLMENT = "enrollment"
    EVENT = "event"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    MESSAGESTATUS = "messageStatus"
    NAME = "name"
    NOTIFICATIONTEMPLATE = "notificationTemplate"
    PROCESSEDDATE = "processedDate"
    RECIPIENTS = "recipients"
    SHARING = "sharing"
    STORECOPY = "storeCopy"
    SUBJECT = "subject"
    TEXT = "text"
    TRANSLATIONS = "translations"


class ProgramMessageStatus(StrEnum):
    """ProgramMessageStatus."""

    SENT = "SENT"
    FAILED = "FAILED"
    SCHEDULED = "SCHEDULED"
    OUTBOUND = "OUTBOUND"


class ProgramNotificationRecipient(StrEnum):
    """ProgramNotificationRecipient."""

    TRACKED_ENTITY_INSTANCE = "TRACKED_ENTITY_INSTANCE"
    ORGANISATION_UNIT_CONTACT = "ORGANISATION_UNIT_CONTACT"
    USERS_AT_ORGANISATION_UNIT = "USERS_AT_ORGANISATION_UNIT"
    USER_GROUP = "USER_GROUP"
    PROGRAM_ATTRIBUTE = "PROGRAM_ATTRIBUTE"
    DATA_ELEMENT = "DATA_ELEMENT"
    WEB_HOOK = "WEB_HOOK"


class ProgramNotificationTemplatePropertyNames(StrEnum):
    """ProgramNotificationTemplatePropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DELIVERYCHANNELS = "deliveryChannels"
    DISPLAYMESSAGETEMPLATE = "displayMessageTemplate"
    DISPLAYNAME = "displayName"
    DISPLAYSUBJECTTEMPLATE = "displaySubjectTemplate"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    MESSAGETEMPLATE = "messageTemplate"
    NAME = "name"
    NOTIFICATIONRECIPIENT = "notificationRecipient"
    NOTIFICATIONTRIGGER = "notificationTrigger"
    NOTIFYPARENTORGANISATIONUNITONLY = "notifyParentOrganisationUnitOnly"
    NOTIFYUSERSINHIERARCHYONLY = "notifyUsersInHierarchyOnly"
    RECIPIENTDATAELEMENT = "recipientDataElement"
    RECIPIENTPROGRAMATTRIBUTE = "recipientProgramAttribute"
    RECIPIENTUSERGROUP = "recipientUserGroup"
    RELATIVESCHEDULEDDAYS = "relativeScheduledDays"
    SENDREPEATABLE = "sendRepeatable"
    SHARING = "sharing"
    SUBJECTTEMPLATE = "subjectTemplate"
    TRANSLATIONS = "translations"


class ProgramRuleActionEvaluationEnvironment(StrEnum):
    """ProgramRuleActionEvaluationEnvironment."""

    WEB = "WEB"
    ANDROID = "ANDROID"


class ProgramRuleActionEvaluationTime(StrEnum):
    """ProgramRuleActionEvaluationTime."""

    ON_DATA_ENTRY = "ON_DATA_ENTRY"
    ON_COMPLETE = "ON_COMPLETE"
    ALWAYS = "ALWAYS"


class ProgramRuleActionPropertyNames(StrEnum):
    """ProgramRuleActionPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CONTENT = "content"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATA = "data"
    DATAELEMENT = "dataElement"
    DISPLAYCONTENT = "displayContent"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LOCATION = "location"
    NAME = "name"
    OPTION = "option"
    OPTIONGROUP = "optionGroup"
    PROGRAMINDICATOR = "programIndicator"
    PROGRAMRULE = "programRule"
    PROGRAMRULEACTIONEVALUATIONENVIRONMENTS = "programRuleActionEvaluationEnvironments"
    PROGRAMRULEACTIONEVALUATIONTIME = "programRuleActionEvaluationTime"
    PROGRAMRULEACTIONTYPE = "programRuleActionType"
    PROGRAMSTAGE = "programStage"
    PROGRAMSTAGESECTION = "programStageSection"
    SHARING = "sharing"
    TEMPLATEUID = "templateUid"
    TRACKEDENTITYATTRIBUTE = "trackedEntityAttribute"
    TRANSLATIONS = "translations"


class ProgramRuleActionType(StrEnum):
    """ProgramRuleActionType."""

    DISPLAYTEXT = "DISPLAYTEXT"
    DISPLAYKEYVALUEPAIR = "DISPLAYKEYVALUEPAIR"
    HIDEFIELD = "HIDEFIELD"
    HIDESECTION = "HIDESECTION"
    HIDEPROGRAMSTAGE = "HIDEPROGRAMSTAGE"
    ASSIGN = "ASSIGN"
    SHOWWARNING = "SHOWWARNING"
    WARNINGONCOMPLETE = "WARNINGONCOMPLETE"
    SHOWERROR = "SHOWERROR"
    ERRORONCOMPLETE = "ERRORONCOMPLETE"
    CREATEEVENT = "CREATEEVENT"
    SETMANDATORYFIELD = "SETMANDATORYFIELD"
    SENDMESSAGE = "SENDMESSAGE"
    SCHEDULEMESSAGE = "SCHEDULEMESSAGE"
    HIDEOPTION = "HIDEOPTION"
    SHOWOPTIONGROUP = "SHOWOPTIONGROUP"
    HIDEOPTIONGROUP = "HIDEOPTIONGROUP"


class ProgramRulePropertyNames(StrEnum):
    """ProgramRulePropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CONDITION = "condition"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    PRIORITY = "priority"
    PROGRAM = "program"
    PROGRAMRULEACTIONS = "programRuleActions"
    PROGRAMSTAGE = "programStage"
    SHARING = "sharing"
    TRANSLATIONS = "translations"


class ProgramRuleVariablePropertyNames(StrEnum):
    """ProgramRuleVariablePropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATAELEMENT = "dataElement"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    PROGRAM = "program"
    PROGRAMRULEVARIABLESOURCETYPE = "programRuleVariableSourceType"
    PROGRAMSTAGE = "programStage"
    SHARING = "sharing"
    TRACKEDENTITYATTRIBUTE = "trackedEntityAttribute"
    TRANSLATIONS = "translations"
    USECODEFOROPTIONSET = "useCodeForOptionSet"
    VALUETYPE = "valueType"


class ProgramRuleVariableSourceType(StrEnum):
    """ProgramRuleVariableSourceType."""

    DATAELEMENT_NEWEST_EVENT_PROGRAM_STAGE = "DATAELEMENT_NEWEST_EVENT_PROGRAM_STAGE"
    DATAELEMENT_NEWEST_EVENT_PROGRAM = "DATAELEMENT_NEWEST_EVENT_PROGRAM"
    DATAELEMENT_CURRENT_EVENT = "DATAELEMENT_CURRENT_EVENT"
    DATAELEMENT_PREVIOUS_EVENT = "DATAELEMENT_PREVIOUS_EVENT"
    CALCULATED_VALUE = "CALCULATED_VALUE"
    TEI_ATTRIBUTE = "TEI_ATTRIBUTE"


class ProgramSectionPropertyNames(StrEnum):
    """ProgramSectionPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    PROGRAM = "program"
    RENDERTYPE = "renderType"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    SORTORDER = "sortOrder"
    STYLE = "style"
    TRACKEDENTITYATTRIBUTES = "trackedEntityAttributes"
    TRANSLATIONS = "translations"


class ProgramStagePropertyNames(StrEnum):
    """ProgramStagePropertyNames."""

    ACCESS = "access"
    ALLOWGENERATENEXTVISIT = "allowGenerateNextVisit"
    ATTRIBUTEVALUES = "attributeValues"
    AUTOGENERATEEVENT = "autoGenerateEvent"
    BLOCKENTRYFORM = "blockEntryForm"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATAENTRYFORM = "dataEntryForm"
    DESCRIPTION = "description"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYDUEDATELABEL = "displayDueDateLabel"
    DISPLAYEVENTLABEL = "displayEventLabel"
    DISPLAYEXECUTIONDATELABEL = "displayExecutionDateLabel"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYGENERATEEVENTBOX = "displayGenerateEventBox"
    DISPLAYNAME = "displayName"
    DISPLAYPROGRAMSTAGELABEL = "displayProgramStageLabel"
    DISPLAYSHORTNAME = "displayShortName"
    DUEDATELABEL = "dueDateLabel"
    ENABLEUSERASSIGNMENT = "enableUserAssignment"
    EVENTLABEL = "eventLabel"
    EXECUTIONDATELABEL = "executionDateLabel"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FEATURETYPE = "featureType"
    FORMNAME = "formName"
    FORMTYPE = "formType"
    GENERATEDBYENROLLMENTDATE = "generatedByEnrollmentDate"
    HIDEDUEDATE = "hideDueDate"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    MINDAYSFROMSTART = "minDaysFromStart"
    NAME = "name"
    NEXTSCHEDULEDATE = "nextScheduleDate"
    NOTIFICATIONTEMPLATES = "notificationTemplates"
    OPENAFTERENROLLMENT = "openAfterEnrollment"
    PERIODTYPE = "periodType"
    PREGENERATEUID = "preGenerateUID"
    PROGRAM = "program"
    PROGRAMSTAGEDATAELEMENTS = "programStageDataElements"
    PROGRAMSTAGELABEL = "programStageLabel"
    PROGRAMSTAGESECTIONS = "programStageSections"
    REFERRAL = "referral"
    REMINDCOMPLETED = "remindCompleted"
    REPEATABLE = "repeatable"
    REPORTDATETOUSE = "reportDateToUse"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    SORTORDER = "sortOrder"
    STANDARDINTERVAL = "standardInterval"
    STYLE = "style"
    TRANSLATIONS = "translations"
    VALIDATIONSTRATEGY = "validationStrategy"


class ProgramStageSectionPropertyNames(StrEnum):
    """ProgramStageSectionPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATAELEMENTS = "dataElements"
    DESCRIPTION = "description"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    PROGRAMINDICATORS = "programIndicators"
    PROGRAMSTAGE = "programStage"
    RENDERTYPE = "renderType"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    SORTORDER = "sortOrder"
    STYLE = "style"
    TRANSLATIONS = "translations"


class ProgramStageWorkingListPropertyNames(StrEnum):
    """ProgramStageWorkingListPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    PROGRAM = "program"
    PROGRAMSTAGE = "programStage"
    PROGRAMSTAGEQUERYCRITERIA = "programStageQueryCriteria"
    SHARING = "sharing"
    TRANSLATIONS = "translations"


class ProgramType(StrEnum):
    """ProgramType."""

    WITH_REGISTRATION = "WITH_REGISTRATION"
    WITHOUT_REGISTRATION = "WITHOUT_REGISTRATION"


class PropertyType(StrEnum):
    """PropertyType."""

    IDENTIFIER = "IDENTIFIER"
    TEXT = "TEXT"
    NUMBER = "NUMBER"
    INTEGER = "INTEGER"
    BOOLEAN = "BOOLEAN"
    USERNAME = "USERNAME"
    EMAIL = "EMAIL"
    PASSWORD = "PASSWORD"
    URL = "URL"
    DATE = "DATE"
    PHONENUMBER = "PHONENUMBER"
    GEOLOCATION = "GEOLOCATION"
    COLOR = "COLOR"
    CONSTANT = "CONSTANT"
    COMPLEX = "COMPLEX"
    COLLECTION = "COLLECTION"
    REFERENCE = "REFERENCE"
    DEFAULT = "DEFAULT"


class ProtectionType(StrEnum):
    """ProtectionType."""

    NONE = "NONE"
    HIDDEN = "HIDDEN"
    RESTRICTED = "RESTRICTED"


class PushAnalysisPropertyNames(StrEnum):
    """PushAnalysisPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DASHBOARD = "dashboard"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    MESSAGE = "message"
    NAME = "name"
    RECIPIENTUSERGROUPS = "recipientUserGroups"
    SHARING = "sharing"
    TITLE = "title"
    TRANSLATIONS = "translations"


class RegressionType(StrEnum):
    """RegressionType."""

    NONE = "NONE"
    LINEAR = "LINEAR"
    POLYNOMIAL = "POLYNOMIAL"
    LOESS = "LOESS"


class RelationshipEntity(StrEnum):
    """RelationshipEntity."""

    TRACKED_ENTITY_INSTANCE = "TRACKED_ENTITY_INSTANCE"
    PROGRAM_INSTANCE = "PROGRAM_INSTANCE"
    PROGRAM_STAGE_INSTANCE = "PROGRAM_STAGE_INSTANCE"


class RelationshipTypePropertyNames(StrEnum):
    """RelationshipTypePropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    BIDIRECTIONAL = "bidirectional"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYFROMTONAME = "displayFromToName"
    DISPLAYNAME = "displayName"
    DISPLAYTOFROMNAME = "displayToFromName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FROMCONSTRAINT = "fromConstraint"
    FROMTONAME = "fromToName"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    REFERRAL = "referral"
    SHARING = "sharing"
    TOCONSTRAINT = "toConstraint"
    TOFROMNAME = "toFromName"
    TRANSLATIONS = "translations"


class RelativePeriodEnum(StrEnum):
    """RelativePeriodEnum."""

    TODAY = "TODAY"
    YESTERDAY = "YESTERDAY"
    LAST_3_DAYS = "LAST_3_DAYS"
    LAST_7_DAYS = "LAST_7_DAYS"
    LAST_14_DAYS = "LAST_14_DAYS"
    LAST_30_DAYS = "LAST_30_DAYS"
    LAST_60_DAYS = "LAST_60_DAYS"
    LAST_90_DAYS = "LAST_90_DAYS"
    LAST_180_DAYS = "LAST_180_DAYS"
    THIS_MONTH = "THIS_MONTH"
    LAST_MONTH = "LAST_MONTH"
    THIS_BIMONTH = "THIS_BIMONTH"
    LAST_BIMONTH = "LAST_BIMONTH"
    THIS_QUARTER = "THIS_QUARTER"
    LAST_QUARTER = "LAST_QUARTER"
    THIS_SIX_MONTH = "THIS_SIX_MONTH"
    LAST_SIX_MONTH = "LAST_SIX_MONTH"
    WEEKS_THIS_YEAR = "WEEKS_THIS_YEAR"
    MONTHS_THIS_YEAR = "MONTHS_THIS_YEAR"
    BIMONTHS_THIS_YEAR = "BIMONTHS_THIS_YEAR"
    QUARTERS_THIS_YEAR = "QUARTERS_THIS_YEAR"
    THIS_YEAR = "THIS_YEAR"
    MONTHS_LAST_YEAR = "MONTHS_LAST_YEAR"
    QUARTERS_LAST_YEAR = "QUARTERS_LAST_YEAR"
    LAST_YEAR = "LAST_YEAR"
    LAST_5_YEARS = "LAST_5_YEARS"
    LAST_10_YEARS = "LAST_10_YEARS"
    LAST_12_MONTHS = "LAST_12_MONTHS"
    LAST_6_MONTHS = "LAST_6_MONTHS"
    LAST_3_MONTHS = "LAST_3_MONTHS"
    LAST_6_BIMONTHS = "LAST_6_BIMONTHS"
    LAST_4_QUARTERS = "LAST_4_QUARTERS"
    LAST_2_SIXMONTHS = "LAST_2_SIXMONTHS"
    THIS_FINANCIAL_YEAR = "THIS_FINANCIAL_YEAR"
    LAST_FINANCIAL_YEAR = "LAST_FINANCIAL_YEAR"
    LAST_5_FINANCIAL_YEARS = "LAST_5_FINANCIAL_YEARS"
    LAST_10_FINANCIAL_YEARS = "LAST_10_FINANCIAL_YEARS"
    THIS_WEEK = "THIS_WEEK"
    LAST_WEEK = "LAST_WEEK"
    THIS_BIWEEK = "THIS_BIWEEK"
    LAST_BIWEEK = "LAST_BIWEEK"
    LAST_4_WEEKS = "LAST_4_WEEKS"
    LAST_4_BIWEEKS = "LAST_4_BIWEEKS"
    LAST_12_WEEKS = "LAST_12_WEEKS"
    LAST_52_WEEKS = "LAST_52_WEEKS"


class ReportPropertyNames(StrEnum):
    """ReportPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CACHESTRATEGY = "cacheStrategy"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESIGNCONTENT = "designContent"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    RELATIVEPERIODS = "relativePeriods"
    REPORTPARAMS = "reportParams"
    SHARING = "sharing"
    TRANSLATIONS = "translations"
    TYPE = "type"
    VISUALIZATION = "visualization"


class ReportType(StrEnum):
    """ReportType."""

    JASPER_REPORT_TABLE = "JASPER_REPORT_TABLE"
    JASPER_JDBC = "JASPER_JDBC"
    HTML = "HTML"


class ReportingRateMetric(StrEnum):
    """ReportingRateMetric."""

    REPORTING_RATE = "REPORTING_RATE"
    REPORTING_RATE_ON_TIME = "REPORTING_RATE_ON_TIME"
    ACTUAL_REPORTS = "ACTUAL_REPORTS"
    ACTUAL_REPORTS_ON_TIME = "ACTUAL_REPORTS_ON_TIME"
    EXPECTED_REPORTS = "EXPECTED_REPORTS"


class ResourceTableType(StrEnum):
    """ResourceTableType."""

    ORG_UNIT_STRUCTURE = "ORG_UNIT_STRUCTURE"
    DATA_SET_ORG_UNIT_CATEGORY = "DATA_SET_ORG_UNIT_CATEGORY"
    CATEGORY_OPTION_COMBO_NAME = "CATEGORY_OPTION_COMBO_NAME"
    DATA_ELEMENT_GROUP_SET_STRUCTURE = "DATA_ELEMENT_GROUP_SET_STRUCTURE"
    INDICATOR_GROUP_SET_STRUCTURE = "INDICATOR_GROUP_SET_STRUCTURE"
    ORG_UNIT_GROUP_SET_STRUCTURE = "ORG_UNIT_GROUP_SET_STRUCTURE"
    CATEGORY_STRUCTURE = "CATEGORY_STRUCTURE"
    DATA_ELEMENT_STRUCTURE = "DATA_ELEMENT_STRUCTURE"
    DATA_SET = "DATA_SET"
    PERIOD_STRUCTURE = "PERIOD_STRUCTURE"
    DATE_PERIOD_STRUCTURE = "DATE_PERIOD_STRUCTURE"
    DATA_ELEMENT_CATEGORY_OPTION_COMBO = "DATA_ELEMENT_CATEGORY_OPTION_COMBO"
    DATA_APPROVAL_REMAP_LEVEL = "DATA_APPROVAL_REMAP_LEVEL"
    DATA_APPROVAL_MIN_LEVEL = "DATA_APPROVAL_MIN_LEVEL"
    TEI_RELATIONSHIP_COUNT = "TEI_RELATIONSHIP_COUNT"


class RoutePropertyNames(StrEnum):
    """RoutePropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    AUTH = "auth"
    AUTHORITIES = "authorities"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISABLED = "disabled"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HEADERS = "headers"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    RESPONSETIMEOUTSECONDS = "responseTimeoutSeconds"
    SHARING = "sharing"
    TRANSLATIONS = "translations"
    URL = "url"


class SMSCommandPropertyNames(StrEnum):
    """SMSCommandPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CODEVALUESEPARATOR = "codeValueSeparator"
    COMPLETENESSMETHOD = "completenessMethod"
    CREATED = "created"
    CREATEDBY = "createdBy"
    CURRENTPERIODUSEDFORREPORTING = "currentPeriodUsedForReporting"
    DATASET = "dataset"
    DEFAULTMESSAGE = "defaultMessage"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    MORETHANONEORGUNITMESSAGE = "moreThanOneOrgUnitMessage"
    NAME = "name"
    NOUSERMESSAGE = "noUserMessage"
    PARSERTYPE = "parserType"
    PROGRAM = "program"
    PROGRAMSTAGE = "programStage"
    RECEIVEDMESSAGE = "receivedMessage"
    SEPARATOR = "separator"
    SHARING = "sharing"
    SMSCODES = "smsCodes"
    SPECIALCHARACTERS = "specialCharacters"
    SUCCESSMESSAGE = "successMessage"
    TRANSLATIONS = "translations"
    USERGROUP = "userGroup"
    WRONGFORMATMESSAGE = "wrongFormatMessage"


class SchedulingType(StrEnum):
    """SchedulingType."""

    CRON = "CRON"
    FIXED_DELAY = "FIXED_DELAY"
    ONCE_ASAP = "ONCE_ASAP"


class SectionPropertyNames(StrEnum):
    """SectionPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CATEGORYCOMBOS = "categoryCombos"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATAELEMENTS = "dataElements"
    DATASET = "dataSet"
    DESCRIPTION = "description"
    DISABLEDATAELEMENTAUTOGROUP = "disableDataElementAutoGroup"
    DISPLAYNAME = "displayName"
    DISPLAYOPTIONS = "displayOptions"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    GREYEDFIELDS = "greyedFields"
    HREF = "href"
    ID = "id"
    INDICATORS = "indicators"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    SHARING = "sharing"
    SHOWCOLUMNTOTALS = "showColumnTotals"
    SHOWROWTOTALS = "showRowTotals"
    SORTORDER = "sortOrder"
    TRANSLATIONS = "translations"


class SendStrategy(StrEnum):
    """SendStrategy."""

    COLLECTIVE_SUMMARY = "COLLECTIVE_SUMMARY"
    SINGLE_NOTIFICATION = "SINGLE_NOTIFICATION"


class SmsMessageEncoding(StrEnum):
    """SmsMessageEncoding."""

    ENC7BIT = "ENC7BIT"
    ENC8BIT = "ENC8BIT"
    ENCUCS2 = "ENCUCS2"
    ENCCUSTOM = "ENCCUSTOM"


class SmsMessageStatus(StrEnum):
    """SmsMessageStatus."""

    INCOMING = "INCOMING"
    PROCESSING = "PROCESSING"
    UNHANDLED = "UNHANDLED"
    FAILED = "FAILED"
    PROCESSED = "PROCESSED"
    SENT = "SENT"


class SortDirection(StrEnum):
    """SortDirection."""

    ASC = "ASC"
    DESC = "DESC"


class SortOrder(StrEnum):
    """SortOrder."""

    ASC = "ASC"
    DESC = "DESC"


class SqlViewPropertyNames(StrEnum):
    """SqlViewPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CACHESTRATEGY = "cacheStrategy"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    SHARING = "sharing"
    SQLQUERY = "sqlQuery"
    TRANSLATIONS = "translations"
    TYPE = "type"
    UPDATEJOBID = "updateJobId"


class SqlViewType(StrEnum):
    """SqlViewType."""

    VIEW = "VIEW"
    MATERIALIZED_VIEW = "MATERIALIZED_VIEW"
    QUERY = "QUERY"


class Status(StrEnum):
    """Status."""

    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"


class TargetType(StrEnum):
    """TargetType."""

    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"


class TextAlign(StrEnum):
    """TextAlign."""

    LEFT = "LEFT"
    CENTER = "CENTER"
    RIGHT = "RIGHT"


class TextMode(StrEnum):
    """TextMode."""

    AUTO = "AUTO"
    CUSTOM = "CUSTOM"


class ThematicMapType(StrEnum):
    """ThematicMapType."""

    CHOROPLETH = "CHOROPLETH"
    BUBBLE = "BUBBLE"


class TotalAggregationType(StrEnum):
    """TotalAggregationType."""

    NONE = "NONE"
    SUM = "SUM"
    AVERAGE = "AVERAGE"


class TrackedEntityAttributePropertyNames(StrEnum):
    """TrackedEntityAttributePropertyNames."""

    ACCESS = "access"
    AGGREGATIONTYPE = "aggregationType"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CONFIDENTIAL = "confidential"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DIMENSIONITEM = "dimensionItem"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYINLISTNOPROGRAM = "displayInListNoProgram"
    DISPLAYNAME = "displayName"
    DISPLAYONVISITSCHEDULE = "displayOnVisitSchedule"
    DISPLAYSHORTNAME = "displayShortName"
    EXPRESSION = "expression"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FIELDMASK = "fieldMask"
    FORMNAME = "formName"
    GENERATED = "generated"
    HREF = "href"
    ID = "id"
    INHERIT = "inherit"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEGENDSET = "legendSet"
    LEGENDSETS = "legendSets"
    NAME = "name"
    OPTIONSET = "optionSet"
    OPTIONSETVALUE = "optionSetValue"
    ORGUNITSCOPE = "orgunitScope"
    PATTERN = "pattern"
    QUERYMODS = "queryMods"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    SKIPSYNCHRONIZATION = "skipSynchronization"
    SORTORDERINLISTNOPROGRAM = "sortOrderInListNoProgram"
    SORTORDERINVISITSCHEDULE = "sortOrderInVisitSchedule"
    STYLE = "style"
    TRANSLATIONS = "translations"
    UNIQUE = "unique"
    VALUETYPE = "valueType"


class TrackedEntityFilterPropertyNames(StrEnum):
    """TrackedEntityFilterPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYNAME = "displayName"
    ENROLLMENTCREATEDPERIOD = "enrollmentCreatedPeriod"
    ENROLLMENTSTATUS = "enrollmentStatus"
    ENTITYQUERYCRITERIA = "entityQueryCriteria"
    EVENTFILTERS = "eventFilters"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FOLLOWUP = "followup"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    PROGRAM = "program"
    SHARING = "sharing"
    SORTORDER = "sortOrder"
    STYLE = "style"
    TRANSLATIONS = "translations"


class TrackedEntityTypePropertyNames(StrEnum):
    """TrackedEntityTypePropertyNames."""

    ACCESS = "access"
    ALLOWAUDITLOG = "allowAuditLog"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FEATURETYPE = "featureType"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    MAXTEICOUNTTORETURN = "maxTeiCountToReturn"
    MINATTRIBUTESREQUIREDTOSEARCH = "minAttributesRequiredToSearch"
    NAME = "name"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    STYLE = "style"
    TRACKEDENTITYTYPEATTRIBUTES = "trackedEntityTypeAttributes"
    TRANSLATIONS = "translations"


class TrackerAtomicMode(StrEnum):
    """TrackerAtomicMode."""

    ALL = "ALL"
    OBJECT = "OBJECT"


class TrackerBundleMode(StrEnum):
    """TrackerBundleMode."""

    COMMIT = "COMMIT"
    VALIDATE = "VALIDATE"


class TrackerBundleReportMode(StrEnum):
    """TrackerBundleReportMode."""

    FULL = "FULL"
    ERRORS = "ERRORS"
    WARNINGS = "WARNINGS"


class TrackerFlushMode(StrEnum):
    """TrackerFlushMode."""

    OBJECT = "OBJECT"
    AUTO = "AUTO"


class TrackerIdScheme(StrEnum):
    """TrackerIdScheme."""

    UID = "UID"
    CODE = "CODE"
    NAME = "NAME"
    ATTRIBUTE = "ATTRIBUTE"


class TrackerImportStrategy(StrEnum):
    """TrackerImportStrategy."""

    CREATE = "CREATE"
    UPDATE = "UPDATE"
    CREATE_AND_UPDATE = "CREATE_AND_UPDATE"
    DELETE = "DELETE"


class TrackerStatus(StrEnum):
    """TrackerStatus."""

    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"


class TrackerType(StrEnum):
    """TrackerType."""

    TRACKED_ENTITY = "TRACKED_ENTITY"
    ENROLLMENT = "ENROLLMENT"
    EVENT = "EVENT"
    RELATIONSHIP = "RELATIONSHIP"


class Transform(StrEnum):
    """Transform."""

    AUTO = "AUTO"
    NONE = "NONE"
    IS_EMPTY = "IS_EMPTY"
    IS_NOT_EMPTY = "IS_NOT_EMPTY"
    SIZE = "SIZE"
    MEMBER = "MEMBER"
    NOT_MEMBER = "NOT_MEMBER"
    IDS = "IDS"
    ID_OBJECTS = "ID_OBJECTS"
    PLUCK = "PLUCK"
    FROM = "FROM"


class TwoFactorType(StrEnum):
    """TwoFactorType."""

    NOT_ENABLED = "NOT_ENABLED"
    TOTP_ENABLED = "TOTP_ENABLED"
    EMAIL_ENABLED = "EMAIL_ENABLED"
    ENROLLING_TOTP = "ENROLLING_TOTP"
    ENROLLING_EMAIL = "ENROLLING_EMAIL"


class TypeOfNumber(StrEnum):
    """TypeOfNumber."""

    UNKNOWN = "UNKNOWN"
    INTERNATIONAL = "INTERNATIONAL"
    NATIONAL = "NATIONAL"
    NETWORK_SPECIFIC = "NETWORK_SPECIFIC"
    SUBSCRIBER_NUMBER = "SUBSCRIBER_NUMBER"
    ALPHANUMERIC = "ALPHANUMERIC"
    ABBREVIATED = "ABBREVIATED"


class UserGroupPropertyNames(StrEnum):
    """UserGroupPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    MANAGEDBYGROUPS = "managedByGroups"
    MANAGEDGROUPS = "managedGroups"
    NAME = "name"
    SHARING = "sharing"
    TRANSLATIONS = "translations"
    USERS = "users"


class UserInvitationStatus(StrEnum):
    """UserInvitationStatus."""

    NONE = "NONE"
    ALL = "ALL"
    EXPIRED = "EXPIRED"


class UserOrgUnitType(StrEnum):
    """UserOrgUnitType."""

    DATA_CAPTURE = "DATA_CAPTURE"
    DATA_OUTPUT = "DATA_OUTPUT"
    TEI_SEARCH = "TEI_SEARCH"


class UserPropertyNames(StrEnum):
    """UserPropertyNames."""

    ACCESS = "access"
    ACCOUNTEXPIRY = "accountExpiry"
    ATTRIBUTEVALUES = "attributeValues"
    AVATAR = "avatar"
    BIRTHDAY = "birthday"
    CATDIMENSIONCONSTRAINTS = "catDimensionConstraints"
    CODE = "code"
    COGSDIMENSIONCONSTRAINTS = "cogsDimensionConstraints"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DATAVIEWMAXORGANISATIONUNITLEVEL = "dataViewMaxOrganisationUnitLevel"
    DATAVIEWORGANISATIONUNITS = "dataViewOrganisationUnits"
    DISABLED = "disabled"
    DISPLAYNAME = "displayName"
    EDUCATION = "education"
    EMAIL = "email"
    EMAILVERIFICATIONTOKEN = "emailVerificationToken"
    EMAILVERIFIED = "emailVerified"
    EMPLOYER = "employer"
    EXTERNALAUTH = "externalAuth"
    FACEBOOKMESSENGER = "facebookMessenger"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FIRSTNAME = "firstName"
    GENDER = "gender"
    HREF = "href"
    ID = "id"
    INTERESTS = "interests"
    INTRODUCTION = "introduction"
    INVITATION = "invitation"
    JOBTITLE = "jobTitle"
    LANGUAGES = "languages"
    LASTCHECKEDINTERPRETATIONS = "lastCheckedInterpretations"
    LASTLOGIN = "lastLogin"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LDAPID = "ldapId"
    NAME = "name"
    NATIONALITY = "nationality"
    OPENID = "openId"
    ORGANISATIONUNITS = "organisationUnits"
    PASSWORD = "password"
    PASSWORDLASTUPDATED = "passwordLastUpdated"
    PHONENUMBER = "phoneNumber"
    SELFREGISTERED = "selfRegistered"
    SETTINGS = "settings"
    SHARING = "sharing"
    SKYPE = "skype"
    SURNAME = "surname"
    TEISEARCHORGANISATIONUNITS = "teiSearchOrganisationUnits"
    TELEGRAM = "telegram"
    TRANSLATIONS = "translations"
    TWITTER = "twitter"
    USERGROUPS = "userGroups"
    USERROLES = "userRoles"
    USERNAME = "username"
    VERIFIEDEMAIL = "verifiedEmail"
    WELCOMEMESSAGE = "welcomeMessage"
    WHATSAPP = "whatsApp"


class UserRolePropertyNames(StrEnum):
    """UserRolePropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    AUTHORITIES = "authorities"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    RESTRICTIONS = "restrictions"
    SHARING = "sharing"
    TRANSLATIONS = "translations"
    USERS = "users"


class ValidationMode(StrEnum):
    """ValidationMode."""

    FULL = "FULL"
    FAIL_FAST = "FAIL_FAST"
    SKIP = "SKIP"


class ValidationNotificationTemplatePropertyNames(StrEnum):
    """ValidationNotificationTemplatePropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DISPLAYMESSAGETEMPLATE = "displayMessageTemplate"
    DISPLAYNAME = "displayName"
    DISPLAYSUBJECTTEMPLATE = "displaySubjectTemplate"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    MESSAGETEMPLATE = "messageTemplate"
    NAME = "name"
    NOTIFYPARENTORGANISATIONUNITONLY = "notifyParentOrganisationUnitOnly"
    NOTIFYUSERSINHIERARCHYONLY = "notifyUsersInHierarchyOnly"
    RECIPIENTUSERGROUPS = "recipientUserGroups"
    SENDSTRATEGY = "sendStrategy"
    SHARING = "sharing"
    SUBJECTTEMPLATE = "subjectTemplate"
    TRANSLATIONS = "translations"
    VALIDATIONRULES = "validationRules"


class ValidationRuleGroupPropertyNames(StrEnum):
    """ValidationRuleGroupPropertyNames."""

    ACCESS = "access"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DISPLAYNAME = "displayName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    HREF = "href"
    ID = "id"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    NAME = "name"
    SHARING = "sharing"
    TRANSLATIONS = "translations"
    VALIDATIONRULES = "validationRules"


class ValidationRulePropertyNames(StrEnum):
    """ValidationRulePropertyNames."""

    ACCESS = "access"
    AGGREGATEEXPORTATTRIBUTEOPTIONCOMBO = "aggregateExportAttributeOptionCombo"
    AGGREGATEEXPORTCATEGORYOPTIONCOMBO = "aggregateExportCategoryOptionCombo"
    AGGREGATIONTYPE = "aggregationType"
    ATTRIBUTEVALUES = "attributeValues"
    CODE = "code"
    CREATED = "created"
    CREATEDBY = "createdBy"
    DESCRIPTION = "description"
    DIMENSIONITEM = "dimensionItem"
    DIMENSIONITEMTYPE = "dimensionItemType"
    DISPLAYDESCRIPTION = "displayDescription"
    DISPLAYFORMNAME = "displayFormName"
    DISPLAYINSTRUCTION = "displayInstruction"
    DISPLAYNAME = "displayName"
    DISPLAYSHORTNAME = "displayShortName"
    FAVORITE = "favorite"
    FAVORITES = "favorites"
    FORMNAME = "formName"
    HREF = "href"
    ID = "id"
    IMPORTANCE = "importance"
    INSTRUCTION = "instruction"
    LASTUPDATED = "lastUpdated"
    LASTUPDATEDBY = "lastUpdatedBy"
    LEFTSIDE = "leftSide"
    LEGENDSET = "legendSet"
    LEGENDSETS = "legendSets"
    NAME = "name"
    NOTIFICATIONTEMPLATES = "notificationTemplates"
    OPERATOR = "operator"
    ORGANISATIONUNITLEVELS = "organisationUnitLevels"
    PERIODTYPE = "periodType"
    QUERYMODS = "queryMods"
    RIGHTSIDE = "rightSide"
    SHARING = "sharing"
    SHORTNAME = "shortName"
    SKIPFORMVALIDATION = "skipFormValidation"
    TRANSLATIONS = "translations"
    VALIDATIONRULEGROUPS = "validationRuleGroups"


class ValidationStrategy(StrEnum):
    """ValidationStrategy."""

    ON_COMPLETE = "ON_COMPLETE"
    ON_UPDATE_AND_INSERT = "ON_UPDATE_AND_INSERT"


class ValueType(StrEnum):
    """ValueType."""

    TEXT = "TEXT"
    LONG_TEXT = "LONG_TEXT"
    MULTI_TEXT = "MULTI_TEXT"
    LETTER = "LETTER"
    PHONE_NUMBER = "PHONE_NUMBER"
    EMAIL = "EMAIL"
    BOOLEAN = "BOOLEAN"
    TRUE_ONLY = "TRUE_ONLY"
    DATE = "DATE"
    DATETIME = "DATETIME"
    TIME = "TIME"
    NUMBER = "NUMBER"
    UNIT_INTERVAL = "UNIT_INTERVAL"
    PERCENTAGE = "PERCENTAGE"
    INTEGER = "INTEGER"
    INTEGER_POSITIVE = "INTEGER_POSITIVE"
    INTEGER_NEGATIVE = "INTEGER_NEGATIVE"
    INTEGER_ZERO_OR_POSITIVE = "INTEGER_ZERO_OR_POSITIVE"
    TRACKER_ASSOCIATE = "TRACKER_ASSOCIATE"
    USERNAME = "USERNAME"
    COORDINATE = "COORDINATE"
    ORGANISATION_UNIT = "ORGANISATION_UNIT"
    REFERENCE = "REFERENCE"
    AGE = "AGE"
    URL = "URL"
    FILE_RESOURCE = "FILE_RESOURCE"
    IMAGE = "IMAGE"
    GEOJSON = "GEOJSON"


class ValueTypeRenderingType(StrEnum):
    """ValueTypeRenderingType."""

    DEFAULT = "DEFAULT"
    DROPDOWN = "DROPDOWN"
    VERTICAL_RADIOBUTTONS = "VERTICAL_RADIOBUTTONS"
    HORIZONTAL_RADIOBUTTONS = "HORIZONTAL_RADIOBUTTONS"
    VERTICAL_CHECKBOXES = "VERTICAL_CHECKBOXES"
    HORIZONTAL_CHECKBOXES = "HORIZONTAL_CHECKBOXES"
    SHARED_HEADER_RADIOBUTTONS = "SHARED_HEADER_RADIOBUTTONS"
    ICONS_AS_BUTTONS = "ICONS_AS_BUTTONS"
    SPINNER = "SPINNER"
    ICON = "ICON"
    TOGGLE = "TOGGLE"
    VALUE = "VALUE"
    SLIDER = "SLIDER"
    LINEAR_SCALE = "LINEAR_SCALE"
    AUTOCOMPLETE = "AUTOCOMPLETE"
    QR_CODE = "QR_CODE"
    BAR_CODE = "BAR_CODE"
    GS1_DATAMATRIX = "GS1_DATAMATRIX"
    CANVAS = "CANVAS"


class VersionType(StrEnum):
    """VersionType."""

    BEST_EFFORT = "BEST_EFFORT"
    ATOMIC = "ATOMIC"


class ViewMode(StrEnum):
    """ViewMode."""

    EXECUTOR = "EXECUTOR"
    RECEIVER = "RECEIVER"


class VisualizationType(StrEnum):
    """VisualizationType."""

    COLUMN = "COLUMN"
    STACKED_COLUMN = "STACKED_COLUMN"
    BAR = "BAR"
    STACKED_BAR = "STACKED_BAR"
    LINE = "LINE"
    AREA = "AREA"
    STACKED_AREA = "STACKED_AREA"
    PIE = "PIE"
    RADAR = "RADAR"
    GAUGE = "GAUGE"
    YEAR_OVER_YEAR_LINE = "YEAR_OVER_YEAR_LINE"
    YEAR_OVER_YEAR_COLUMN = "YEAR_OVER_YEAR_COLUMN"
    SCATTER = "SCATTER"
    BUBBLE = "BUBBLE"
    SINGLE_VALUE = "SINGLE_VALUE"
    PIVOT_TABLE = "PIVOT_TABLE"
    OUTLIER_TABLE = "OUTLIER_TABLE"
