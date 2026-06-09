---
name: vibe-investigation-workflow
description: Drive a natural-language security investigation in Lakewatch from first anomaly to a scoped campaign timeline. Use when investigating suspicious host, network, identity, or process activity, triaging an alert, chasing an indicator, or building an incident timeline.
---

# Vibe Investigation Workflow

A repeatable pattern for investigating security incidents through conversation
instead of query-language syntax. The analyst speaks in entities and intent. You
carry the schema, the joins, and the time windows. The pattern is portable
beyond security, but the steps below assume Lakewatch security telemetry.

All indicator handling is governed by the workspace instructions. Before sending
any indicator to an external MCP server or tool, follow the egress permission
protocol there. Default to deny and ask first.

## The five moves

Run the investigation as five moves, in order. Each move narrows the question.

1. **Baseline first.** Before labeling anything anomalous, establish what normal
   looks like for the entity in question. "What is normal process activity for
   this host over the last 30 days" precedes "what is unusual today." The
   contrast is what makes an anomaly legible.
2. **Find the first anomaly.** Ask the cheapest, broadest question that could
   surface something out of character. Rank by deviation from baseline, not by
   raw volume. Anchor the first odd event in time.
3. **Pivot by entity.** Follow the host, user, IP, account, or hash into the next
   data source. When a process reaches out to a network destination, pivot to
   network telemetry for that destination. When a destination touches credential
   activity, pivot to identity telemetry. Carry the entity, do not restart the
   query.
4. **Force the timeline.** Stitch host, network, and identity events for the
   entities of interest into one correlated timeline across the relevant window.
   Build it before the investigation feels complete. The timeline is the artifact
   that goes to a stakeholder. Use the `investigation-timeline` skill to format it.
5. **Confirm scope last.** Once the story is clear, ask the breadth question.
   "Which other hosts contacted this destination," or "who else received this
   message." Scope is what separates a single incident from a campaign.

## Example prompt sequence

The entities below are fictional and the addresses use the RFC 5737
documentation ranges. Replace them with the entities in your case.

1. "Show me unusual process activity on host WS-ENG-07 over the last seven days,
   ranked against its 30-day baseline."
2. "When did that out-of-character parent process first spawn a command shell on
   this host?" (anchors the timeline; maps to T1059 command and scripting)
3. "What network connections left WS-ENG-07 in the five minutes after that shell
   spawned?" (a beacon to 203[.]0[.]113[.]10 surfaces; maps to T1071.001
   web-protocol C2)
4. "Which other hosts contacted 203[.]0[.]113[.]10 in the last 24 hours?" (scopes
   the blast radius, foreshadows lateral movement)
5. "Show credential-access activity on any host that talked to that destination."
   (LSASS-touching events; maps to T1003 OS credential dumping)
6. "Build a correlated timeline of everything tied to that destination across the
   environment for the last 24 hours."
7. "Which workstations received the same inbound message that started this?"
   (closes the loop to the initial vector; confirms scope)

## What good output looks like

- Each step names the table or telemetry source it drew from.
- Attacker behavior is mapped to a MITRE ATT&CK technique ID when one applies.
- Indicators are defanged in prose and in the timeline.
- Assumptions are stated. Low-confidence inferences are flagged as such, not
  presented as findings.
- The final artifact is a timeline a stakeholder can read without the analyst
  present.

## Edge cases

- If a prompt returns nothing, check the time window and the table before
  concluding the activity is absent. An empty result is often a window problem.
- If a parent-child process relationship looks suspicious but matches the
  baseline, say so. Out-of-character is the signal, not the technique alone.
- A log-clearing or indicator-removal event (T1070) is itself a detection
  signal. Treat the attempt to hide as evidence, not as a dead end.
- Some legitimate processes overlap attacker paths, for example a backup job
  writing to a path that staging also uses. Distinguish them with a contrast
  question rather than assuming.

## Framework anchors

- C2 beaconing maps to MITRE ATT&CK T1071.001. Credential access maps to T1003.
  Remote-service lateral movement maps to T1021. Indicator removal maps to T1070.
- When the initial vector is a prompt injection against an AI agent, frame it as
  OWASP LLM01 Prompt Injection and locate it in the OWASP MAESTRO agentic threat
  model rather than asserting the risk as self-evident.
