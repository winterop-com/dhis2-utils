-- Live SQL views over the raw DHIS2 transactional tables.
--
-- These bypass the analytics_* materialization step and query the live
-- datavalue / event / enrollment / trackedentity tables directly. They are
-- always up to date but can be slower to scan than the analytics tables.
--
-- Friendly column names join in metadata (data element name, period type,
-- org unit hierarchy, program name, etc) so the views are immediately useful
-- in SQL Lab and as Superset datasets without further transformation.
--
-- Idempotent: CREATE OR REPLACE on every run, no migration tracking needed.

-- ─── v_live_datavalue ──────────────────────────────────────────────────
-- All non-deleted aggregate data values with friendly names.
DROP VIEW IF EXISTS v_live_datavalue CASCADE;
CREATE VIEW v_live_datavalue AS
SELECT
  de.uid                                                           AS dataelement_uid,
  de.name                                                          AS dataelement,
  de.shortname                                                     AS dataelement_short,
  de.valuetype                                                     AS valuetype,
  de.aggregationtype                                               AS aggregationtype,
  de.domaintype                                                    AS domaintype,
  pt.name                                                          AS period_type,
  pe.startdate                                                     AS period_start,
  pe.enddate                                                       AS period_end,
  EXTRACT(YEAR FROM pe.startdate)::int                             AS year,
  ou.uid                                                           AS ou_uid,
  ou.name                                                          AS orgunit,
  ou.path                                                          AS ou_path,
  ou.hierarchylevel                                                AS ou_level,
  dv.value                                                         AS value_text,
  CASE
    WHEN de.valuetype IN ('NUMBER','INTEGER','INTEGER_POSITIVE',
                          'INTEGER_NEGATIVE','INTEGER_ZERO_OR_POSITIVE',
                          'PERCENTAGE','UNIT_INTERVAL')
         AND dv.value ~ '^-?[0-9]+(\.[0-9]+)?$'
    THEN dv.value::numeric
  END                                                              AS value_numeric,
  dv.created                                                       AS created,
  dv.lastupdated                                                   AS lastupdated,
  dv.followup                                                      AS followup
FROM datavalue dv
JOIN dataelement      de ON de.dataelementid       = dv.dataelementid
JOIN period           pe ON pe.periodid            = dv.periodid
JOIN periodtype       pt ON pt.periodtypeid        = pe.periodtypeid
JOIN organisationunit ou ON ou.organisationunitid  = dv.sourceid
WHERE NOT dv.deleted;

COMMENT ON VIEW v_live_datavalue IS
  'Live aggregate data values joined with dataelement, period and orgunit metadata. Bypasses the analytics_* materialization and is always current.';


-- ─── v_live_event ──────────────────────────────────────────────────────
-- All non-deleted tracker events with friendly program / stage / OU names.
-- The data element values themselves remain in the eventdatavalues JSONB
-- column; query like `eventdatavalues->>'<dataelement_uid>'` in SQL Lab.
DROP VIEW IF EXISTS v_live_event CASCADE;
CREATE VIEW v_live_event AS
SELECT
  e.uid                                AS event_uid,
  e.eventid                            AS event_id,
  p.uid                                AS program_uid,
  p.name                               AS program,
  p.type                               AS program_type,
  ps.uid                               AS programstage_uid,
  ps.name                              AS programstage,
  e.status                             AS event_status,
  en.status                            AS enrollment_status,
  en.uid                               AS enrollment_uid,
  e.occurreddate                       AS occurreddate,
  e.scheduleddate                      AS scheduleddate,
  e.completeddate                      AS completeddate,
  e.created                            AS created,
  e.lastupdated                        AS lastupdated,
  ou.uid                               AS ou_uid,
  ou.name                              AS orgunit,
  ou.path                              AS ou_path,
  ou.hierarchylevel                    AS ou_level,
  e.eventdatavalues                    AS eventdatavalues,
  (SELECT COUNT(*)::int FROM jsonb_object_keys(e.eventdatavalues)) AS datavalue_count
FROM event e
LEFT JOIN enrollment       en ON en.enrollmentid       = e.enrollmentid
LEFT JOIN program          p  ON p.programid           = en.programid
LEFT JOIN programstage     ps ON ps.programstageid     = e.programstageid
LEFT JOIN organisationunit ou ON ou.organisationunitid = e.organisationunitid
WHERE NOT e.deleted;

COMMENT ON VIEW v_live_event IS
  'Live tracker events with program / stage / orgunit metadata. eventdatavalues column holds per-event DE values as JSONB; extract with eventdatavalues->>''<dataelement_uid>'' in SQL Lab.';


-- ─── v_live_enrollment ─────────────────────────────────────────────────
-- All non-deleted enrollments with program and orgunit metadata.
DROP VIEW IF EXISTS v_live_enrollment CASCADE;
CREATE VIEW v_live_enrollment AS
SELECT
  en.uid                               AS enrollment_uid,
  p.uid                                AS program_uid,
  p.name                               AS program,
  p.type                               AS program_type,
  te.uid                               AS trackedentity_uid,
  en.status                            AS status,
  en.enrollmentdate                    AS enrollmentdate,
  en.occurreddate                      AS occurreddate,
  en.completeddate                     AS completeddate,
  en.followup                          AS followup,
  ou.uid                               AS ou_uid,
  ou.name                              AS orgunit,
  ou.path                              AS ou_path,
  ou.hierarchylevel                    AS ou_level,
  en.created                           AS created,
  en.lastupdated                       AS lastupdated
FROM enrollment en
LEFT JOIN program          p  ON p.programid           = en.programid
LEFT JOIN trackedentity    te ON te.trackedentityid    = en.trackedentityid
LEFT JOIN organisationunit ou ON ou.organisationunitid = en.organisationunitid
WHERE NOT en.deleted;

COMMENT ON VIEW v_live_enrollment IS
  'Live enrollments with program / trackedentity / orgunit metadata.';


-- ─── v_live_trackedentity ──────────────────────────────────────────────
-- All non-deleted tracked entities with type and registering orgunit info.
DROP VIEW IF EXISTS v_live_trackedentity CASCADE;
CREATE VIEW v_live_trackedentity AS
SELECT
  te.uid                               AS trackedentity_uid,
  tet.uid                              AS trackedentitytype_uid,
  tet.name                             AS trackedentitytype,
  ou.uid                               AS ou_uid,
  ou.name                              AS orgunit,
  ou.path                              AS ou_path,
  ou.hierarchylevel                    AS ou_level,
  te.inactive                          AS inactive,
  te.potentialduplicate                AS potentialduplicate,
  te.created                           AS created,
  te.lastupdated                       AS lastupdated
FROM trackedentity te
LEFT JOIN trackedentitytype tet ON tet.trackedentitytypeid = te.trackedentitytypeid
LEFT JOIN organisationunit  ou  ON ou.organisationunitid   = te.organisationunitid
WHERE NOT te.deleted;

COMMENT ON VIEW v_live_trackedentity IS
  'Live tracked entities with type and registering orgunit metadata.';


-- ─── v_orgunit_geojson ────────────────────────────────────────────────
-- Organisation units with PostGIS geometry exported as GeoJSON Feature
-- strings. Each row is one OU whose geometry is not null. The GeoJSON
-- Feature embeds the OU uid, name, and level as properties so deck.gl
-- charts can tooltip and color by those attributes.
DROP VIEW IF EXISTS v_orgunit_geojson CASCADE;
CREATE VIEW v_orgunit_geojson AS
SELECT
  ou.uid                           AS ou_uid,
  ou.name                          AS orgunit,
  ou.hierarchylevel                AS ou_level,
  ou.path                          AS ou_path,
  jsonb_build_object(
    'type',       'Feature',
    'geometry',   ST_AsGeoJSON(ST_Simplify(ou.geometry, 0.005), 6)::jsonb,
    'properties', jsonb_build_object(
      'ou_uid',   ou.uid,
      'orgunit',  ou.name,
      'ou_level', ou.hierarchylevel
    )
  )::text                          AS geojson
FROM organisationunit ou
WHERE ou.geometry IS NOT NULL;

COMMENT ON VIEW v_orgunit_geojson IS
  'Organisation units with geometry as GeoJSON Feature strings for deck.gl map charts.';
