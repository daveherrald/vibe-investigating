---
name: lakewatch-query-conventions
description: Conventions for querying Lakewatch security telemetry, covering the bronze, silver, and gold medallion layers, OCSF-normalized gold tables, and Databricks SQL pipe syntax. Use when writing, reviewing, or explaining SQL against Lakewatch tables.
---

# Lakewatch Query Conventions

Conventions for querying Lakewatch security data so that results stay consistent
and readable. Lakewatch organizes telemetry on a medallion architecture and
normalizes detection-ready data to the Open Cybersecurity Schema Framework
(OCSF). Consult the Lakewatch documentation at https://docs.lakewatch.com for the
exact catalog, schema, and table names provisioned in your workspace.

## Choose the right layer

- **Bronze** holds raw, source-shaped events with minimal transformation. Query
  bronze when you need a field that normalization dropped, or when you are
  validating ingestion. Source-specific field access often goes through a
  semi-structured column, so expect to extract and cast.
- **Silver** holds parsed and enriched events. Query silver for cleaned,
  typed fields when you do not need full cross-source normalization.
- **Gold** holds OCSF-normalized events. Prefer gold for investigation. It gives
  you stable entity fields across sources, which is what makes entity pivots
  work without per-source schema knowledge.

Default to gold for entity-driven investigation. Drop to silver or bronze only
when gold does not carry the field you need.

## OCSF gold field access

Gold tables expose OCSF objects as structs. Reach nested fields with dot
notation. Common entity fields, by OCSF object:

- Process (the subject process): `process.cmd_line`, `process.name`,
  `process.pid`. The parent process is `actor.process.name` and
  `actor.process.cmd_line`, not `process.parent_process` (that field is an
  untyped VARIANT in the gold schema).
- Device or host: `device.hostname`, `device.ip`, `device.os.name`
- Source and destination endpoints: `src_endpoint.ip`, `src_endpoint.port`,
  `dst_endpoint.ip`, `dst_endpoint.port`
- Network bytes: `traffic.bytes_out`, `traffic.bytes_in`
- Actor or identity: `actor.user.name`, `actor.user.uid`, and the initiating
  process `actor.process.name`
- File: `file.name`, `file.path`, `file.hashes`

Confirm the exact object and field for a given event class against the OCSF
schema at https://schema.ocsf.io and the Lakewatch docs, since field presence
depends on the event class.

## Use pipe syntax

Write queries in Databricks SQL pipe syntax. It reads top to bottom in the order
the data flows, which matches how an investigation reasons.

```sql
FROM lakewatch.gold.process_activity
|> WHERE device.hostname = 'WS-ENG-07'
|> WHERE time >= current_timestamp() - INTERVAL 7 DAYS
|> AGGREGATE count(*) AS events GROUP BY actor.process.name AS parent_process, process.name AS process
|> ORDER BY events DESC
|> LIMIT 50
```

## Always bound the time window

Every query bounds its time range. An unbounded scan over security telemetry is
slow and expensive, and it rarely answers an investigative question better than a
bounded one. Filter on the top-level `time` column for the window the
investigation cares about, and order by `time` when you present a sequence.

## Keep development queries small

While exploring, cap row counts (for example `LIMIT 1000`) so an interactive
query does not scan more than the question needs. Widen the window or the limit
only once the query shape is right.

## Reference

- Lakewatch documentation: https://docs.lakewatch.com
- OCSF schema browser: https://schema.ocsf.io
- Databricks SQL pipe syntax: https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-syntax-qry-select-pipe
