"""DHIS2 v41 plugin tree for dhis2w-core.

Mirror of `dhis2w_core.v42.plugins` (today's canonical baseline). Plugin
files still import from `dhis2w_client.generated.v42` until individual
files diverge to handle v41-specific wire shapes (e.g. OAuth2 client
`cid` vs `clientId`, missing `OAuth2ClientCredentialsAuthScheme`).
"""
