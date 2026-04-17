"""Destructive integration tests against local DHIS2, auth'd via Playwright-minted PAT."""

from __future__ import annotations

import secrets

import pytest
from dhis2_client import Dhis2Client, PatAuth

pytestmark = pytest.mark.slow


async def test_pat_auth_round_trip(local_url: str, local_pat: str) -> None:
    async with Dhis2Client(local_url, auth=PatAuth(token=local_pat)) as client:
        info = await client.system.info()
        assert info.version is not None
        me = await client.system.me()
        assert me.username


async def test_constant_create_update_delete_round_trip(local_url: str, local_pat: str) -> None:
    name = f"dhis2-utils-test-{secrets.token_hex(4)}"
    async with Dhis2Client(local_url, auth=PatAuth(token=local_pat)) as client:
        if not hasattr(client.resources, "constants"):
            pytest.skip("generated client has no `constants` resource")

        module = __import__(
            f"dhis2_client.generated.{client.version_key}.models.constant",
            fromlist=["Constant"],
        )
        payload = module.Constant(name=name, shortName=name[:50], value=1.5)
        create_response = await client.resources.constants.create(payload)
        uid = (create_response.get("response") or {}).get("uid")
        assert uid, f"no uid in create response: {create_response}"

        try:
            fetched = await client.resources.constants.get(uid)
            assert fetched.id == uid
            assert fetched.name == name

            fetched.value = 2.5
            await client.resources.constants.update(fetched)
            refetched = await client.resources.constants.get(uid)
            assert refetched.value == 2.5
        finally:
            await client.resources.constants.delete(uid)
