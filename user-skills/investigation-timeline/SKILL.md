---
name: investigation-timeline
description: Format a correlated security-incident timeline as a stakeholder-ready artifact. Use when summarizing an investigation, preparing a case note, or handing off findings to another analyst or an incident lead.
---

# Investigation Timeline

Turn correlated events into a timeline a stakeholder can read without the analyst
present. The timeline is the deliverable of an investigation. It should stand on
its own and survive a copy into a case note.

## Format

Produce a table ordered by time, oldest first. One row per significant event, not
per raw log line. Columns:

| Column | Content |
|---|---|
| Time (UTC) | Event time in UTC, ISO 8601. Keep the whole timeline in one timezone. |
| Entity | The host, user, account, or address the event centers on. |
| Event | One terse sentence on what happened. No log dump. |
| Technique | MITRE ATT&CK technique ID when one applies, otherwise blank. |
| Source | The telemetry source or table the event came from. |
| Confidence | High, medium, or low. Be honest about inference. |

## Rules

- Defang every indicator in the timeline. Write IPs as 203[.]0[.]113[.]10 and
  URLs as hxxp:// so the artifact is safe to paste anywhere.
- Collapse noise. If twenty beacons fired, write one row that states the cadence
  and the window, not twenty rows.
- Keep each Event cell to one sentence. The detail lives in the underlying query,
  which you should be ready to show on request.
- Mark gaps. If the timeline has a hole where you expected activity, add a row
  that names the gap rather than leaving it silent.
- State the window and the data sources the timeline was built from, once, above
  the table.

## Posting to a case

When you write the timeline, or a summary of it, into a case management system,
follow the workspace rules. Keep each case comment to 200 characters or fewer,
and add a new comment rather than editing an existing one unless asked. For a
long timeline, attach or link the full table and post a short comment that points
to it.

## Example

Window: 2026-06-01 14:00 to 16:00 UTC. Sources: gold process, network, and
identity tables. Entities are fictional and addresses use the RFC 5737
documentation range.

| Time (UTC) | Entity | Event | Technique | Source | Confidence |
|---|---|---|---|---|---|
| 2026-06-01T14:02Z | WS-ENG-07 | Out-of-character parent process spawned a command shell | T1059 | gold process | High |
| 2026-06-01T14:03Z | WS-ENG-07 | Outbound beacon to 203[.]0[.]113[.]10 on a fixed cadence | T1071.001 | gold network | High |
| 2026-06-01T14:31Z | WS-FIN-02 | Same destination contacted from a second host | T1071.001 | gold network | Medium |
| 2026-06-01T15:10Z | WS-FIN-02 | Credential-access activity touching LSASS | T1003 | gold process | Medium |
| 2026-06-01T15:58Z | WS-ENG-07 | Security event log cleared | T1070.001 | gold host | High |
