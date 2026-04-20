"""DHIS2 predictor workflow — `Dhis2Client.predictors`.

Predictors generate data values from expressions over historical data (e.g.
"3-month rolling average of X" → emit a synthetic DataElement row). This
accessor covers the *run* endpoints; CRUD for the predictor definitions
themselves lives on `client.resources.predictors` (generated).

Three run shapes DHIS2 exposes:

- `POST /api/predictors/run?startDate=YYYY-MM-DD&endDate=YYYY-MM-DD` —
  run every predictor on the instance.
- `POST /api/predictors/{uid}/run?startDate=…&endDate=…` — run one.
- `POST /api/predictorGroups/{uid}/run?startDate=…&endDate=…` — run a
  named group of predictors in one pass.

All three return a `WebMessageResponse` with a summary of predictions
written / ignored / failed; none of them kick a background job, so there's
no task to watch.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dhis2_client.envelopes import WebMessageResponse

if TYPE_CHECKING:
    from dhis2_client.client import Dhis2Client


class PredictorsAccessor:
    """`Dhis2Client.predictors` — run predictor expressions + emit data values."""

    def __init__(self, client: Dhis2Client) -> None:
        """Bind to the sharing client."""
        self._client = client

    async def run_all(self, *, start_date: str, end_date: str) -> WebMessageResponse:
        """Run every predictor on the instance for the given date range.

        Returns the summary envelope — `.import_count()` gives
        `imported / updated / ignored / deleted` counts for the emitted
        data values.
        """
        return await self._run("/api/predictors/run", start_date=start_date, end_date=end_date)

    async def run_one(self, predictor_uid: str, *, start_date: str, end_date: str) -> WebMessageResponse:
        """Run a single predictor by UID over the given date range."""
        return await self._run(
            f"/api/predictors/{predictor_uid}/run",
            start_date=start_date,
            end_date=end_date,
        )

    async def run_group(self, group_uid: str, *, start_date: str, end_date: str) -> WebMessageResponse:
        """Run every predictor in a `PredictorGroup` over the given date range."""
        return await self._run(
            f"/api/predictorGroups/{group_uid}/run",
            start_date=start_date,
            end_date=end_date,
        )

    async def _run(self, path: str, *, start_date: str, end_date: str) -> WebMessageResponse:
        """Dispatch a predictor-run POST + return the typed envelope."""
        params: dict[str, Any] = {"startDate": start_date, "endDate": end_date}
        raw = await self._client.post_raw(path, params=params)
        return WebMessageResponse.model_validate(raw)


__all__ = ["PredictorsAccessor"]
