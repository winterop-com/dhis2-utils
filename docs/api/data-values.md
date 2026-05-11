# Data values (streaming import)

`DataValuesAccessor` on `Dhis2Client.data_values` — streams uploads to `POST /api/dataValueSets` without buffering the whole payload in memory. Accepts JSON / XML / CSV / ADX content types. For the small-payload case (a handful of values), use `dhis2w_core.v42.plugins.aggregate.service.push_data_values` instead.

::: dhis2w_client.data_values
