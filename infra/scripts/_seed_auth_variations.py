"""PAT variations seeded by `seed_auth.py`. Edit to add or change PAT shapes.

Each entry drives one POST to `/api/apiToken`. The `suffix` becomes the env-var
suffix in the written `.env.auth` (e.g. `DEFAULT` → `DHIS2_PAT_DEFAULT`). All
tokens are created by the admin user and link to that user automatically.
"""

from __future__ import annotations

from typing import Any

PAT_VARIATIONS: list[dict[str, Any]] = [
    {
        "suffix": "DEFAULT",
        "description": "no restrictions, no expiry — the baseline PAT",
        "payload": {"attributes": [], "type": "PERSONAL_ACCESS_TOKEN_V2"},
    },
    {
        "suffix": "READ_ONLY",
        "description": "GET only",
        "payload": {
            "type": "PERSONAL_ACCESS_TOKEN_V2",
            "attributes": [{"type": "MethodAllowedList", "allowedMethods": ["GET"]}],
        },
    },
    {
        "suffix": "WRITE",
        "description": "full CRUD verb allowlist",
        "payload": {
            "type": "PERSONAL_ACCESS_TOKEN_V2",
            "attributes": [
                {
                    "type": "MethodAllowedList",
                    "allowedMethods": ["GET", "POST", "PUT", "PATCH", "DELETE"],
                }
            ],
        },
    },
    {
        "suffix": "SHORT_EXPIRY",
        "description": "expires in 1 day — exercise refresh/expired-handling",
        "payload": {
            "type": "PERSONAL_ACCESS_TOKEN_V2",
            "attributes": [],
            "_inject_expiry_days": 1,  # runner turns this into absolute `expire` ms at POST time
        },
    },
    {
        "suffix": "LOCAL_ONLY",
        "description": "IP allowlist restricted to loopback (DHIS2 wants plain IPs, not CIDR)",
        "payload": {
            "type": "PERSONAL_ACCESS_TOKEN_V2",
            "attributes": [{"type": "IpAllowedList", "allowedIps": ["127.0.0.1", "::1"]}],
        },
    },
    {
        "suffix": "REFERRER_BOUND",
        "description": "referrer allowlist for https://example.com (DHIS2 rejects http+port+localhost)",
        "payload": {
            "type": "PERSONAL_ACCESS_TOKEN_V2",
            "attributes": [{"type": "RefererAllowedList", "allowedReferrers": ["https://example.com"]}],
        },
    },
]
