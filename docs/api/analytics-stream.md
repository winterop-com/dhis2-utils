# Analytics streaming

`AnalyticsAccessor` on `Dhis2Client.analytics` — streaming GETs against the `/api/analytics*` endpoint family. Uses httpx's `stream()` + `aiter_bytes` to pipe the response body straight to disk without buffering the full body in memory. Counterpart to `client.data_values.stream` for the export direction.

::: dhis2_client.analytics_stream
