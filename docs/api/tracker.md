# Tracker reads

Typed instance models returned by `/api/tracker/*` reads: `TrackerTrackedEntity`, `TrackerEnrollment`, `TrackerEvent`, `TrackerRelationship` + nested value types + `EventStatus` / `EnrollmentStatus` StrEnums.

Tracker models are version-scoped because `/api/tracker/*` shapes drift across DHIS2 majors. Import from the version your client is pinned to: `from dhis2_client.generated.v42.tracker import TrackerBundle, TrackerEvent, ...`.

::: dhis2_client.generated.v42.tracker
