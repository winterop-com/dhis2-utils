# Route auth schemes

The DHIS2 Route API proxies requests to upstream services. Its own auth is one of five discriminated variants. The union is typed end-to-end via `AuthScheme` + `AuthSchemeAdapter`.

::: dhis2_client.auth_schemes
