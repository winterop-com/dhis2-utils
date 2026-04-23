# `dhis2-client` API reference

Auto-generated from the `dhis2-client` source via `mkdocstrings`. Every class, method, and function listed here is importable from `dhis2_client` (top-level re-exports) or from its module.

For prose explanations with worked examples, see the [`dhis2-client` step-by-step guide](../guides/client-tutorial.md).

## Layout

- [Client + lifecycle](client.md) — `Dhis2Client`, connect, close, raw escape hatches
- [Auth providers](auth.md) — `BasicAuth`, `PatAuth`, `OAuth2Auth`, the `AuthProvider` Protocol, `OAuth2Token`, `TokenStore`
- [Errors](errors.md) — the exception hierarchy
- [Envelopes + responses](envelopes.md) — `WebMessageResponse`, `Conflict`, `ImportCount`, `ObjectReport`, `ImportReport`
- [Route auth schemes](auth-schemes.md) — the 5-variant discriminated `AuthScheme` union
- [Sharing](sharing.md) — typed `SharingObject` + `SharingBuilder` + `get_sharing` / `apply_sharing` helpers over `/api/sharing`
- [Generated-model helpers](generated.md) — `Dhis2` enum, `available_versions`, `load`
- [OpenAPI-derived models](oas.md) — the 562+ classes emitted under `generated/v42/oas/` from `/api/openapi.json`
- [System module](system.md) — `Me`, `SystemInfo`, `SystemModule`
- [Tracker reads](tracker.md) — instance models, status enums
- [Aggregate](aggregate.md) — `DataValue`, `DataValueSet`
- [Data values (streaming)](data-values.md) — `DataValuesAccessor` on `Dhis2Client.data_values` (streaming `/api/dataValueSets` imports)
- [Analytics](analytics.md) — `Grid`, `GridHeader` (OAS-emitted) + `AnalyticsMetaData` (typed parser helper over `Grid.metaData`)
- [Analytics streaming](analytics-stream.md) — `AnalyticsAccessor` on `Dhis2Client.analytics` (chunked `/api/analytics*` downloads)
- [Maintenance](maintenance.md) — `Notification`, `DataIntegrityCheck`, `DataIntegrityResult`, `DataIntegrityReport`
- [Metadata accessor](metadata-accessor.md) — `MetadataAccessor` on `Dhis2Client.metadata` (bulk delete + multi-resource operations)
- [Customize](customize.md) — `CustomizeAccessor`, `LoginCustomization`, `CustomizationResult`
- [Files](files.md) — `FilesAccessor`, `Document`, `FileResource`, `FileResourceDomain` — documents + file-resource uploads/downloads
- [Messaging](messaging.md) — `MessagingAccessor` on `Dhis2Client.messaging` (/api/messageConversations)
- [Apps](apps.md) — `AppsAccessor` on `Dhis2Client.apps` — install / uninstall / update over `/api/apps` + `/api/appHub`
- [Validation + predictors](validation.md) — `ValidationAccessor` + `PredictorsAccessor` for the run-rules + run-predictors workflow
- [Visualizations + dashboards](visualizations.md) — `VisualizationsAccessor` + `VisualizationSpec` + `DashboardsAccessor` + `DashboardSlot` for authoring saved analytics + composing dashboards
- [Maps](maps.md) — `MapsAccessor` + `MapSpec` + `MapLayerSpec` for thematic choropleths + map composition
- [Legend sets](legend-sets.md) — `LegendSetsAccessor` + `LegendSetSpec` + `LegendSpec` — colour-range authoring attached to visualizations and maps
- [Organisation units](organisation-units.md) — `OrganisationUnitsAccessor` + `OrganisationUnitGroupsAccessor` + `OrganisationUnitGroupSetsAccessor` + `OrganisationUnitLevelsAccessor` — tree-aware reads, per-level naming, group + group-set membership
- [Data elements](data-elements.md) — `DataElementsAccessor` + `DataElementGroupsAccessor` + `DataElementGroupSetsAccessor` — aggregate + tracker DE authoring, thematic groups, analytics dimensions
- [Indicators](indicators.md) — `IndicatorsAccessor` + `IndicatorGroupsAccessor` + `IndicatorGroupSetsAccessor` — computed-ratio authoring with expression validation, per-item membership shortcuts
- [SQL views](sql-views.md) — `SqlViewsAccessor` + `SqlViewRunner` for DHIS2 `SqlView` execution workflows
- [Periods](periods.md) — `PeriodType` StrEnum
- [UIDs](uids.md) — client-side UID generator + validator
