# Auth providers

Every auth method implements the same `AuthProvider` Protocol (`headers()` + `refresh_if_needed()`), so the rest of the client is identical regardless of what you pick.

## The Protocol

::: dhis2_client.auth.base

## Basic

::: dhis2_client.auth.basic

## Personal Access Token

::: dhis2_client.auth.pat

## OAuth2 / OIDC

::: dhis2_client.auth.oauth2
