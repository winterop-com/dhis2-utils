# Periods

Two hand-written StrEnums covering DHIS2's period names — neither is exposed as an enum upstream (both are Java class hierarchies / 45 bare boolean fields), so we mirror them here for type-safe authoring.

- **`PeriodType`** — the 24 frequencies a `DataSet` collects data at (`Daily`, `Weekly`, `Monthly`, `Quarterly`, `Yearly`, …). Source: upstream `PeriodTypeEnum.java`.
- **`RelativePeriod`** — the 45 rolling windows a `Visualization` / `EventVisualization` / `Map` can pin itself to (`last12Months`, `thisYear`, `lastSixMonth`, …). Mirrors the field names on the generated `RelativePeriods` model at `dhis2_client.generated.v42.oas.RelativePeriods`. Used by `VisualizationSpec.relative_periods` — pass a set to emit the corresponding `relativePeriods` block on the wire.

::: dhis2_client.periods
