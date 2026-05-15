# Routes — reverse-proxy accessor

Typed helper over DHIS2's `/api/routes/{id}/run` reverse-proxy endpoint.
Accessed via `Dhis2Client.routes`.

`run(code, path)` resolves the user-set `Route.code` to its UID once via
`GET /api/routes?filter=code:eq:<code>`, caches the mapping for the rest of
the connection, and delegates the actual proxy GET to
`Dhis2Client.get_response()` so callers see the raw `httpx.Response` and
can do their own status-based handling — a 502 from the proxy means
"DHIS2 reached, downstream didn't", which is a fact health-checkers want
to report rather than an exception to raise.

`pat_options` shape, `LookupError` on missing codes, and the
`invalidate_cache()` escape hatch are documented inline below.

See also:
- Client lifecycle escape hatches (`get_response`, `skip_version_probe`): [Client](client.md)
- Reverse-proxy plugin internals (CRUD on `/api/routes`): [Route plugin](../architecture/route-plugin.md)

::: dhis2w_client.v42.routes
