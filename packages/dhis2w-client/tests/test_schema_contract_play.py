"""Live-schema contract tests against play.im.dhis2.org.

Pulls one real instance of each major resource from `dev-2-42` and
`dev-2-43` and runs it through the matching generated pydantic model.
Catches DHIS2 ship-day API drift the day it lands — if a field type
changes, a new required field appears, or an enum gains a constant we
don't know about, the model_validate call below raises and this test
fails.

Marked `@pytest.mark.contract` so it runs in a dedicated CI job
(`.github/workflows/contract.yml`) and not as part of `make test`.
The play instances are public; the only failure mode tied to network
is an instance being down — those skip rather than fail.

Adding more resources: append a `(accessor_name, model_name)` pair to
RESOURCES. The accessor_name is the attribute on `client.resources`;
the model_name is informational (used in the parametrize id).
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Any

import httpx
import pytest
from dhis2w_client import BasicAuth, Dhis2Client

# Each (accessor, model_name) pair represents one schema we want to keep
# in sync with the live DHIS2 wire shape. Picking ~25 covers the most-used
# corners of /api/* without spamming play.
RESOURCES: list[tuple[str, str]] = [
    ("attributes", "Attribute"),
    ("categories", "Category"),
    ("category_combos", "CategoryCombo"),
    ("category_option_combos", "CategoryOptionCombo"),
    ("category_options", "CategoryOption"),
    ("dashboards", "Dashboard"),
    ("data_element_groups", "DataElementGroup"),
    ("data_elements", "DataElement"),
    ("data_sets", "DataSet"),
    ("indicator_groups", "IndicatorGroup"),
    ("indicators", "Indicator"),
    ("legend_sets", "LegendSet"),
    ("maps", "Map"),
    ("option_sets", "OptionSet"),
    ("organisation_unit_groups", "OrganisationUnitGroup"),
    ("organisation_unit_levels", "OrganisationUnitLevel"),
    ("organisation_units", "OrganisationUnit"),
    ("predictors", "Predictor"),
    ("program_indicators", "ProgramIndicator"),
    ("program_rules", "ProgramRule"),
    ("program_stages", "ProgramStage"),
    ("programs", "Program"),
    ("sql_views", "SqlView"),
    ("tracked_entity_attributes", "TrackedEntityAttribute"),
    ("user_groups", "UserGroup"),
    ("user_roles", "UserRole"),
    ("users", "User"),
    ("validation_rules", "ValidationRule"),
    ("visualizations", "Visualization"),
]

PLAY_URLS = {
    "v42": "https://play.im.dhis2.org/dev-2-42",
    "v43": "https://play.im.dhis2.org/dev-2-43",
}


async def _make_client(url: str) -> AsyncIterator[Dhis2Client]:
    """Connect to a play instance, skipping the test if it's unreachable."""
    client = Dhis2Client(url, auth=BasicAuth(username="admin", password="district"), allow_version_fallback=True)
    try:
        try:
            await client.connect()
        except httpx.HTTPError as exc:
            pytest.skip(f"play instance {url} unreachable: {exc}")
        yield client
    finally:
        await client.close()


@pytest.fixture
async def play_v42_client() -> AsyncIterator[Dhis2Client]:
    """Yield a connected client for `dev-2-42`, skipping if the host is down."""
    async for client in _make_client(PLAY_URLS["v42"]):
        yield client


@pytest.fixture
async def play_v43_client() -> AsyncIterator[Dhis2Client]:
    """Yield a connected client for `dev-2-43`, skipping if the host is down."""
    async for client in _make_client(PLAY_URLS["v43"]):
        yield client


async def _assert_resource_validates(client: Dhis2Client, accessor_name: str) -> None:
    """Pull one row of `accessor_name` and assert the typed model parses it.

    Skipping rather than failing when the accessor doesn't exist on the
    live version (e.g. v43 drops something we still test for v42) keeps
    the test honest about what's been verified vs not.
    """
    accessor: Any = getattr(client.resources, accessor_name, None)
    if accessor is None:
        pytest.skip(f"client.resources has no `{accessor_name}` attribute on this DHIS2 version")

    rows = await accessor.list(page_size=1, fields="*")
    if not rows:
        pytest.skip(f"play instance has zero `{accessor_name}` rows")

    # `list(fields="*")` returned a typed model already — if it parsed cleanly
    # the contract holds. Hit `get()` too to exercise the single-instance path
    # since it can have different fields than the listing path.
    sample_id = rows[0].id
    if not sample_id:
        pytest.skip(f"first `{accessor_name}` row had no id")
    fetched = await accessor.get(sample_id, fields="*")
    assert fetched is not None, f"GET /api/.../{sample_id} returned None"


@pytest.mark.contract
@pytest.mark.parametrize(("accessor_name", "model_name"), RESOURCES, ids=[m for _, m in RESOURCES])
async def test_v42_schema_contract(
    play_v42_client: Dhis2Client,
    accessor_name: str,
    model_name: str,  # noqa: ARG001 — used as parametrize id
) -> None:
    """Generated v42 model still validates one live row from play."""
    await _assert_resource_validates(play_v42_client, accessor_name)


@pytest.mark.contract
@pytest.mark.parametrize(("accessor_name", "model_name"), RESOURCES, ids=[m for _, m in RESOURCES])
async def test_v43_schema_contract(
    play_v43_client: Dhis2Client,
    accessor_name: str,
    model_name: str,  # noqa: ARG001 — used as parametrize id
) -> None:
    """Generated v43 model still validates one live row from play."""
    await _assert_resource_validates(play_v43_client, accessor_name)
