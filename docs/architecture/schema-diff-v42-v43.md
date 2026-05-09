# Schema diff: v42 -> v43

Reference of every schema change between DHIS2 2.42 and 2.43 as seen by `dhis2w-client`'s codegen. Two sources of truth:

- **`/api/schemas`** drives `dhis2w_client.generated.v{N}.schemas` (and the `client.resources.X` accessors). Run `dhis2 dev codegen diff v42 v43` to regenerate the schema-side diff.
- **`/api/openapi.json`** drives `dhis2w_client.generated.v{N}.oas` (the request/response shapes used by tracker, auth schemes, data-value imports, etc.). Diff is a plain `ls` comparison of the two `oas/` trees — there is no dedicated CLI command for it yet.

If you only care about the workable patterns ("how do I read this v43 field"), jump to [Working with version-specific types](versioning.md#working-with-version-specific-types) in the versioning page. This page is the lookup index.

## Snapshot

| Source | Added | Removed | Changed |
| --- | ---: | ---: | ---: |
| `/api/schemas` (resource models) | 0 | 3 | 40 |
| `/api/openapi.json` (OAS payload models) | 20 | 23 | n/a |

The OAS "removals" are mostly internal `*Params` DTOs that v43 collapsed; the OAS "additions" are mostly new request/response models for data-value change-logs, the tracker event split, and a few date-time primitives. Both are listed in full below.

## Schemas-side: removed resources

These three resources are gone in v43. Anyone calling the matching `client.resources.X` accessor on a v43 instance will get `AttributeError`.

| Schema | Class on the server | Notes |
| --- | --- | --- |
| `dataInputPeriods` | `org.hisp.dhis.dataset.DataInputPeriod` | Folded into `dataSet.dataInputPeriods` inline; no top-level resource. |
| `externalFileResource` | `org.hisp.dhis.fileresource.ExternalFileResource` | Use the `externalAccess` field on `fileResource` directly. |
| `pushanalysis` | `org.hisp.dhis.pushanalysis.PushAnalysis` | Push-analysis is removed in v43. |

## Schemas-side: breaking shape changes

The six places where a v42-typed pydantic model **cannot parse** v43 wire data, or vice versa. If a hand-written helper in `dhis2w-client` is pinned to v42 (most are), these are the schemas where parsing fails on a v43 instance.

| Schema | Field | v42 wire shape | v43 wire shape |
| --- | --- | --- | --- |
| `dashboardItem` | `user` / `users` | `Reference \| None`, fieldName `user` | `list[User]`, fieldName renamed to `users` |
| `dashboardItem` | `code` / `id` | `IDENTIFIER` (max 50, unique) | `TEXT` (max 255, not unique); `id` becomes required |
| `trackedEntityAttribute` | `favorite` / `favorites` | `bool`, fieldName `favorite` | `list[str]` (set of usernames), fieldName renamed to `favorites` |
| `section` | `user` | `Reference \| None` | removed entirely |
| `program` | `favorite` | `list[str]` | removed entirely |
| `legend` | most fields | full identifiable-object surface | almost everything removed (see "Legend collapse" below) |

### Legend collapse

`legend` lost ~20 fields in v43 — `access`, `attributeValues`, `code`, `color`, `created`, `createdBy`, `displayName`, `endValue`, `favorite`, `href`, `id`, `image`, `lastUpdated`, `lastUpdatedBy`, `name`, `sharing`, `startValue`, `translation`, `user` — and gained `set`, `showKey`, `strategy`, `style`. This is the largest single-schema delta. Treat `legend` as effectively rebuilt across versions.

## Schemas-side: pure additions

New fields only present in v43. v42-pinned models lose them at typed-access time but they round-trip through `model_extra` because every generated model uses `ConfigDict(extra="allow")`.

| Schema | New fields |
| --- | --- |
| `dashboardItem` | `displayText` |
| `dataApprovalLevel` | `translations` (replaces `translation`) |
| `dataApprovalWorkflow` | `translations` (replaces `translation`) |
| `eventChart` | `fixColumnHeaders`, `fixRowHeaders`, `hideEmptyColumns` |
| `eventReport` | `fixColumnHeaders`, `fixRowHeaders`, `hideEmptyColumns` |
| `eventVisualization` | `fixColumnHeaders`, `fixRowHeaders`, `hideEmptyColumns` |
| `indicatorGroupSet` | `displayDescription`, `displayShortName` |
| `legendSet` | `translations` (replaces `translation`) |
| `map` | `basemaps` (collection of `Basemap`, see OAS below) |
| `mapView` | `eventCoordinateFieldFallback` |
| `program` | `displayEnrollmentsLabel`, `displayEventsLabel`, `displayProgramStagesLabel`, `enableChangeLog`, `enrollmentCategoryCombo`, `enrollmentsLabel`, `eventsLabel`, `programStagesLabel` |
| `programRuleAction` | `legendSet`, `priority` |
| `programStage` | `displayEventsLabel`, `eventsLabel` |
| `trackedEntityAttribute` | `blockedSearchOperators`, `minCharactersToSearch`, `preferredSearchOperator`, `skipAnalytics`, `trigramIndexable`, `trigramIndexed` |
| `trackedEntityType` | `displayTrackedEntityTypesLabel`, `enableChangeLog`, `trackedEntityTypesLabel` |
| `userGroup` | `description` |

## Schemas-side: dropped fields (per resource)

Fields removed in v43, beyond the breaking-shape and resource removals above. Most are the `favorite: bool` per-user flag being yanked from a long list of resources — DHIS2 moved the favouriting model server-side. These fields will simply be missing on v43-parsed models; reading them on a v42-pinned model against v43 wire data raises `AttributeError`.

| Schema | Removed fields |
| --- | --- |
| `access` | `externalize` |
| `categoryCombo` | `favorite` |
| `categoryOption` | `aggregationType`, `dimensionItem`, `dimensionItemType`, `favorite`, `legendSet`, `legendSets` |
| `dashboard` | `displayFormName`, `displayShortName`, `formName`, `shortName` |
| `dashboardItem` | `displayName`, `favorite` |
| `dataApprovalLevel` | `favorite`, `translation` |
| `dataApprovalWorkflow` | `favorite`, `translation` |
| `indicatorGroup` | `favorite` |
| `indicatorGroupSet` | `favorite` |
| `legendSet` | `favorite`, `translation` |
| `optionSet` | `favorite` |
| `programTrackedEntityAttribute` | `skipIndividualAnalytics` |
| `section` | `favorite`, `user` |
| `sharing` | `external` |

## Schemas-side: bound shifts (informational)

DHIS2 v43 tightened a lot of `description` bounds (max 2_147_483_647 -> 255), promoted several `id` / `code` fields from `IDENTIFIER` to `TEXT`, and downgraded `href` from `URL` to `TEXT`. None of these affect pydantic parsing — pydantic doesn't enforce DHIS2's `min`/`max`/`propertyType` metadata bounds — but they show up in the full diff if you grep for `propertyType` or `max:`. They are not listed individually here. See the appendix or run the `diff` CLI for the per-field detail.

## OAS-side: additions

New OAS-derived models in `dhis2w_client.generated.v43.oas` that were not in v42. Most are tracker / data-value / dimensional-object DTOs that v43 split out, plus a few date-time primitives.

| Model | Likely role |
| --- | --- |
| `Basemap` | Backing model for `Map.basemaps` |
| `DataExportValue` | Aggregate data export response item |
| `DataValueCategoryParams`, `DataValuePostParams` | Aggregate data-value request DTOs |
| `DataValueChangelogEntry` | Backing model for `/api/dataValues/audit` change-log responses |
| `DimensionalItemObjectParams`, `DimensionalObjectParams`, `IdentifiableObjectParams` | Generic query-param DTOs that replace older `Base*` and per-resource `*Params` shapes |
| `Event` | Tracker event base shape |
| `IsoChronology`, `LocalDate` | Java-time primitives surfaced by the OAS now (replace ad-hoc string fields in v42) |
| `ProgramNotificationInstance`, `ProgramNotificationTemplateSnapshot` | Program-notification tracking shapes |
| `SectionRenderingObject`, `ValueTypeRenderingObject` | Form-rendering object shapes |
| `SystemCapability` | New `/api/system/capabilities` response item |
| `TrackedEntity` | Tracker tracked-entity payload (replaces v42's `TrackedEntity` import path; the old name was different) |
| `TrackerEventParams` | Tracker event query DTO |
| `TrackerSingleEvent`, `TrackerTrackerEvent` | The split between event-program "single" events and tracker-program "tracker" events — v43 separates them where v42 had one shared shape |

## OAS-side: removals

Models present in v42 that are gone in v43. Mostly internal `*Params` DTOs the OAS no longer emits separately, plus the push-analysis cluster.

| Removed model | Notes |
| --- | --- |
| `AnalyticsPeriodBoundaryParams` | Inlined |
| `BaseDimensionalItemObject`, `BaseDimensionalObject`, `BaseDimensionalObjectParams` | Replaced by the `Identifiable*Params` cluster |
| `DataEntryFormParams` | Inlined |
| `DataValueAuditDto`, `DataValueCategoryDto`, `DataValueDto` | Replaced by the new `DataValue*Params` / `DataValueChangelogEntry` cluster |
| `EventDataValue`, `EventParams` | Replaced by `Event` / `TrackerEventParams` |
| `IndicatorTypeParams`, `LegendParams`, `RelationshipParams`, `UserRoleParams` | Inlined |
| `PotentialDuplicateParams` | Inlined |
| `PushAnalysis`, `PushAnalysisJobParameters`, `PushAnalysisParams` | Push-analysis is removed (matches the schemas-side `pushanalysis` removal) |
| `TrackedEntityAttributeValueParams`, `TrackedEntityParams`, `TrackedEntityProgramOwnerParams` | Inlined |
| `TrackerEvent` | Renamed to `TrackerTrackerEvent` (or `TrackerSingleEvent` for event-program events) |
| `TrigramSummary` | Removed |

## Field renames (the ones that matter)

The two cases where a v42 field has a v43 counterpart under a different name. Both are in the breaking-shape table above; surfacing here as a lookup index:

| Schema | v42 field | v43 field | Notes |
| --- | --- | --- | --- |
| `dashboardItem` | `user` (singular `Reference`) | `users` (`list[User]`) | Wire fieldName is `users` in v43. |
| `trackedEntityAttribute` | `favorite` (singular `bool`) | `favorites` (`list[str]`) | Wire fieldName is `favorites` in v43; values are usernames. |
| `eventChart`, `eventReport`, `eventVisualization`, `mapView` | `period` collection (fieldName `periods`) | `period` collection (fieldName `persistedPeriods`) | The Python attribute name does not change — the wire fieldName does. Pydantic alias handles round-trip via the generator. |

## Reproducing this diff

```bash
# Schemas-side
uv run dhis2 dev codegen diff v42 v43

# OAS-side (no CLI; plain ls comparison)
diff \
  <(ls packages/dhis2w-client/src/dhis2w_client/generated/v42/oas/ | grep -v __pycache__) \
  <(ls packages/dhis2w-client/src/dhis2w_client/generated/v43/oas/)
```

## Appendix: complete schemas-side diff

Raw output of `dhis2 dev codegen diff v42 v43`. Reproduced verbatim so the field-by-field bound shifts are searchable in the docs site.

```text
Schema diff: v42 -> v43
  added schemas: 0   removed schemas: 3   changed schemas: 40

## Removed (only in v42)
  - dataInputPeriods  (3 props, klass=org.hisp.dhis.dataset.DataInputPeriod)
  - externalFileResource  (19 props, klass=org.hisp.dhis.fileresource.ExternalFileResource)
  - pushanalysis  (20 props, klass=org.hisp.dhis.pushanalysis.PushAnalysis)

## Changed
  ~ access
      - externalize  (BOOLEAN)
  ~ attribute
      ~ valueType:
  ~ category
      ~ valueType:
  ~ categoryCombo
      - favorite  (BOOLEAN)
      ~ href: propertyType: 'URL' -> 'TEXT', max: 1.7976931348623157e+308 -> 2147483647.0
      ~ translation: max: 255.0 -> 1.7976931348623157e+308
  ~ categoryOption
      - aggregationType  (CONSTANT)
      - dimensionItem  (TEXT)
      - dimensionItemType  (CONSTANT)
      - favorite  (BOOLEAN)
      - legendSet  (REFERENCE)
      - legendSets  (COLLECTION collection of LegendSet)
      ~ description: min: 1.0 -> 0.0, max: 2147483647.0 -> 255.0
      ~ href: propertyType: 'URL' -> 'TEXT', max: 1.7976931348623157e+308 -> 2147483647.0
      ~ shortName: min: 1.0 -> 0.0
      ~ translation: max: 255.0 -> 1.7976931348623157e+308
  ~ categoryOptionGroupSet
      ~ valueType:
  ~ dashboard
      - displayFormName  (TEXT)
      - displayShortName  (TEXT)
      - formName  (TEXT)
      - shortName  (TEXT)
      ~ description: min: 1.0 -> 0.0, max: 2147483647.0 -> 255.0
      ~ translation: max: 255.0 -> 1.7976931348623157e+308
  ~ dashboardItem
      + displayText  (TEXT)
      - displayName  (TEXT)
      - favorite  (BOOLEAN)
      ~ code: propertyType: 'IDENTIFIER' -> 'TEXT', unique: True -> False, max: 50.0 -> 255.0
      ~ created: required: False -> True
      ~ href: propertyType: 'URL' -> 'TEXT', max: 1.7976931348623157e+308 -> 2147483647.0
      ~ id: propertyType: 'IDENTIFIER' -> 'TEXT', required: False -> True, min: 11.0 -> 0.0
      ~ lastUpdated: required: False -> True
      ~ name: min: 1.0 -> 0.0
      ~ translation: max: 255.0 -> 1.7976931348623157e+308
      ~ user: propertyType: 'REFERENCE' -> 'COLLECTION', klass: 'org.hisp.dhis.user.User' -> 'java.util.List', itemKlass: None -> 'org.hisp.dhis.user.User', itemPropertyType: None -> 'REFERENCE', collection: False -> True, owner: False -> True, persisted: False -> True, min: None -> 0.0, max: None -> 1.7976931348623157e+308, fieldName: 'user' -> 'users'
  ~ dataApprovalLevel
      + translations  (COLLECTION collection of Translation)
      - favorite  (BOOLEAN)
      - translation  (COLLECTION collection of Translation)
      ~ href: propertyType: 'URL' -> 'TEXT', max: 1.7976931348623157e+308 -> 2147483647.0
      ~ name: min: 1.0 -> 0.0
      ~ orgUnitLevel: min: 0.0 -> -2147483648.0
  ~ dataApprovalWorkflow
      + translations  (COLLECTION collection of Translation)
      - favorite  (BOOLEAN)
      - translation  (COLLECTION collection of Translation)
      ~ code: propertyType: 'IDENTIFIER' -> 'TEXT'
      ~ href: propertyType: 'URL' -> 'TEXT', max: 1.7976931348623157e+308 -> 2147483647.0
      ~ name: min: 1.0 -> 0.0
  ~ dataElement
      ~ valueType:
  ~ dataElementGroupSet
      ~ valueType:
  ~ eventChart
      + fixColumnHeaders  (BOOLEAN)
      + fixRowHeaders  (BOOLEAN)
      + hideEmptyColumns  (BOOLEAN)
      ~ period: itemPropertyType: 'REFERENCE' -> 'COMPLEX', fieldName: 'periods' -> 'persistedPeriods'
  ~ eventReport
      + fixColumnHeaders  (BOOLEAN)
      + fixRowHeaders  (BOOLEAN)
      + hideEmptyColumns  (BOOLEAN)
      ~ period: itemPropertyType: 'REFERENCE' -> 'COMPLEX', fieldName: 'periods' -> 'persistedPeriods'
  ~ eventVisualization
      + fixColumnHeaders  (BOOLEAN)
      + fixRowHeaders  (BOOLEAN)
      + hideEmptyColumns  (BOOLEAN)
      ~ period: itemPropertyType: 'REFERENCE' -> 'COMPLEX', fieldName: 'periods' -> 'persistedPeriods'
  ~ identifiableObject
      ~ domain:
  ~ indicatorGroup
      - favorite  (BOOLEAN)
      ~ description: max: 2147483647.0 -> 255.0
      ~ href: propertyType: 'URL' -> 'TEXT', max: 1.7976931348623157e+308 -> 2147483647.0
      ~ name: unique: False -> True
      ~ translation: max: 255.0 -> 1.7976931348623157e+308
  ~ indicatorGroupSet
      + displayDescription  (TEXT)
      + displayShortName  (TEXT)
      - favorite  (BOOLEAN)
      ~ description: max: 2147483647.0 -> 255.0
      ~ href: propertyType: 'URL' -> 'TEXT', max: 1.7976931348623157e+308 -> 2147483647.0
      ~ translation: max: 255.0 -> 1.7976931348623157e+308
  ~ interpretation
      ~ period: propertyType: 'REFERENCE' -> 'COMPLEX', min: None -> 0.0, max: None -> 255.0
  ~ legend
      + set  (REFERENCE)
      + showKey  (BOOLEAN)
      + strategy  (CONSTANT)
      + style  (CONSTANT)
      - access  (COMPLEX)
      - attributeValues  (COMPLEX)
      - code  (IDENTIFIER)
      - color  (TEXT)
      - created  (DATE)
      - createdBy  (REFERENCE)
      - displayName  (TEXT)
      - endValue  (NUMBER)
      - favorite  (BOOLEAN)
      - href  (URL)
      - id  (IDENTIFIER)
      - image  (TEXT)
      - lastUpdated  (DATE)
      - lastUpdatedBy  (REFERENCE)
      - name  (TEXT)
      - sharing  (COMPLEX)
      - startValue  (NUMBER)
      - translation  (COLLECTION collection of Translation)
      - user  (REFERENCE)
  ~ legendSet
      + translations  (COLLECTION collection of Translation)
      - favorite  (BOOLEAN)
      - translation  (COLLECTION collection of Translation)
      ~ code: propertyType: 'IDENTIFIER' -> 'TEXT', unique: True -> False
      ~ href: propertyType: 'URL' -> 'TEXT', max: 1.7976931348623157e+308 -> 2147483647.0
      ~ name: min: 1.0 -> 0.0
  ~ map
      + basemaps  (COLLECTION collection of Basemap)
  ~ mapView
      + eventCoordinateFieldFallback  (TEXT)
      ~ period: itemPropertyType: 'REFERENCE' -> 'COMPLEX', fieldName: 'periods' -> 'persistedPeriods'
  ~ optionGroupSet
      ~ valueType:
  ~ optionSet
      - favorite  (BOOLEAN)
      ~ description: max: 2147483647.0 -> 255.0
      ~ href: propertyType: 'URL' -> 'TEXT', max: 1.7976931348623157e+308 -> 2147483647.0
      ~ translation: max: 255.0 -> 1.7976931348623157e+308
      ~ valueType:
      ~ version: required: False -> True
  ~ organisationUnitGroupSet
      ~ valueType:
  ~ program
      + displayEnrollmentsLabel  (TEXT)
      + displayEventsLabel  (TEXT)
      + displayProgramStagesLabel  (TEXT)
      + enableChangeLog  (BOOLEAN)
      + enrollmentCategoryCombo  (REFERENCE)
      + enrollmentsLabel  (TEXT)
      + eventsLabel  (TEXT)
      + programStagesLabel  (TEXT)
      - favorite  (COLLECTION collection of String)
      ~ description: max: 2147483647.0 -> 255.0
      ~ enrollmentDateLabel: max: 2147483647.0 -> 255.0
      ~ enrollmentLabel: max: 2147483647.0 -> 255.0
      ~ eventLabel: max: 2147483647.0 -> 255.0
      ~ followUpLabel: max: 2147483647.0 -> 255.0
      ~ formName: max: 2147483647.0 -> 255.0
      ~ href: propertyType: 'URL' -> 'TEXT', max: 1.7976931348623157e+308 -> 2147483647.0
      ~ incidentDateLabel: max: 2147483647.0 -> 255.0
      ~ noteLabel: max: 2147483647.0 -> 255.0
      ~ orgUnitLabel: max: 2147483647.0 -> 255.0
      ~ programStageLabel: max: 2147483647.0 -> 255.0
      ~ relationshipLabel: max: 2147483647.0 -> 255.0
      ~ trackedEntityAttributeLabel: max: 2147483647.0 -> 255.0
      ~ translation: max: 255.0 -> 1.7976931348623157e+308
      ~ userRole: owner: False -> True
  ~ programDataElement
      ~ valueType:
  ~ programRuleAction
      + legendSet  (REFERENCE)
      + priority  (INTEGER)
      ~ programRuleActionType:
  ~ programRuleVariable
      ~ valueType:
  ~ programStage
      + displayEventsLabel  (TEXT)
      + eventsLabel  (TEXT)
      ~ description: min: 2.0 -> 1.0
  ~ programTrackedEntityAttribute
      - skipIndividualAnalytics  (BOOLEAN)
      ~ valueType:
  ~ section
      - favorite  (BOOLEAN)
      - user  (REFERENCE)
      ~ code: propertyType: 'IDENTIFIER' -> 'TEXT', min: 0.0 -> 1.0
      ~ description: max: 2147483647.0 -> 255.0
      ~ id: propertyType: 'IDENTIFIER' -> 'TEXT', required: False -> True
      ~ showColumnTotals: required: False -> True
      ~ showRowTotals: required: False -> True
      ~ translation: max: 255.0 -> 1.7976931348623157e+308
  ~ sharing
      - external  (BOOLEAN)
  ~ trackedEntityAttribute
      + blockedSearchOperators  (COLLECTION collection of QueryOperator)
      + minCharactersToSearch  (INTEGER)
      + preferredSearchOperator  (CONSTANT)
      + skipAnalytics  (BOOLEAN)
      + trigramIndexable  (BOOLEAN)
      + trigramIndexed  (BOOLEAN)
      ~ favorite: propertyType: 'BOOLEAN' -> 'COLLECTION', klass: 'java.lang.Boolean' -> 'java.util.Set', itemKlass: None -> 'java.lang.String', itemPropertyType: None -> 'TEXT', collection: False -> True, writable: False -> True, min: None -> 0.0, max: None -> 1.7976931348623157e+308, fieldName: 'favorite' -> 'favorites'
      ~ valueType:
  ~ trackedEntityType
      + displayTrackedEntityTypesLabel  (TEXT)
      + enableChangeLog  (BOOLEAN)
      + trackedEntityTypesLabel  (TEXT)
  ~ trackedEntityTypeAttribute
      ~ valueType:
  ~ userGroup
      + description  (TEXT)
  ~ validationResult
      ~ period: propertyType: 'REFERENCE' -> 'COMPLEX', min: None -> 0.0, max: None -> 1.7976931348623157e+308
  ~ visualization
      ~ period: itemPropertyType: 'REFERENCE' -> 'COMPLEX', fieldName: 'periods' -> 'persistedPeriods'
```
