# Genie Space: Lakewatch Research Agent

Version-controlled configuration for the **Lakewatch Research Agent** Genie Space,
the natural-language security-investigation surface that complements the Genie Code
configuration in this repo. Genie Space (AI/BI) translates questions into SQL over
Unity Catalog tables; this directory holds its deployable config.

## Files

- `lakewatch-research-agent.serialized.json` is the canonical, deployable config
  (Genie `serialized_space` v2): the table set, the general instructions, and the
  example queries. `deploy.py` reads this file. It is the source of truth.
- `general-instructions.md` and `example-queries.md` are human-readable mirrors of
  the instructions and example queries embedded in the JSON, for review and diffs.
  They are generated from the JSON, so change behavior by editing the JSON.
- `deploy.py` pushes the JSON to the live space, in place.

## What the space contains

- 30 Unity Catalog tables: 14 gold OCSF tables that hold data, 15 bronze tables
  (`microsoft_winevtlog`, the Zeek conn/dns/http/email logs, proxy, threat intel,
  email tracking, Slack, and more), and `lakewatch.internal.notables` as the
  case/notable proxy. The space is at the 30-table limit.
- General instructions encoding the investigation method, the gold and bronze
  field paths, and the active demo time-scope floor (only 2026-06-14 UTC and later).
- Ten example queries, one per investigation move, using generic placeholder
  entities (RFC 5737 documentation ranges), not lab-specific values.

## Deploy

Requires the Databricks CLI authenticated to the target workspace.

```
GENIE_SPACE_ID=01f136c1f0ae142fbb37c56981ae2354 DATABRICKS_PROFILE=DEFAULT python3 deploy.py
```

The script updates the existing space in place. The default space id targets the
DH Demo deployment; override `GENIE_SPACE_ID` and `DATABRICKS_PROFILE` for another.

## Mechanism and gotchas (Genie serialized_space v2 over REST)

- Update endpoint is `PATCH /api/2.0/genie/spaces/{id}` with a body of
  `{space_id, title, description, warehouse_id, serialized_space}`.
- `data_sources.tables` must be sorted by identifier or the proto validation
  rejects it. `deploy.py` sorts before sending.
- The etag conflict-detection rejects even a matching etag, so `deploy.py` omits
  the etag. This is safe in a single-editor workspace.
- `instructions.text_instructions` (the general instructions) is an array of
  `{id, content:[string]}`, and content elements concatenate with no separator.
  `instructions.example_question_sqls` is an array of
  `{id, question:[string], sql:[lines]}`.
- For a brand-new workspace, create the space first (for example via the Genie
  MCP import action) rather than patching a nonexistent id.

## Companion assets

- Genie Code instructions and skills for the same investigation surface live in
  `../user-instructions`, `../workspace-instructions`, `../user-skills`, and
  `../workspace-skills`. The gold OCSF field paths are kept consistent between the
  Genie Code `lakewatch-query-conventions` skill and this space.
