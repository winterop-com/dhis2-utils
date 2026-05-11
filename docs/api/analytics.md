# Analytics responses

Typed shapes for `/api/analytics` (aggregated + raw) responses.

## See also

- [Analytics streaming](analytics-stream.md) — `AnalyticsAccessor` on `Dhis2Client.analytics` covers the streaming `/api/analytics*` surface (pivots, events, enrollments, outliers) plus the simple `query(...)` call over the standard aggregate endpoint.
- [Visualizations + dashboards](visualizations.md) — every saved `Visualization` is an analytics query with a chart type + axis placement attached. Start from an analytics query you've verified, then wrap it in a `VisualizationSpec` to persist.
- [Visualizations walkthrough](../guides/visualizations.md) — end-to-end guide showing how to go from a `client.analytics.aggregate(...)` result to a saved chart + a dashboard slot.

::: dhis2w_client.v42.analytics
