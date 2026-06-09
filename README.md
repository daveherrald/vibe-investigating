# Vibe Investigating

Genie Code configuration for running security investigations in Databricks
Lakewatch by conversation instead of query-language syntax. This repository
accompanies the Data + AI Summit 2026 talk "Vibe Investigating: Hunt Like You
Talk."

The idea is simple. A security investigation has always been a conversation an
analyst has with the data. You speak in entities and intent, a host, a user, an
address, "what is normal here, and what is not." The query language has been the
bottleneck. Genie Code in Lakewatch lets the conversation be the interface, so
this repository packages the instructions and skills that make that conversation
disciplined, safe, and repeatable.

## What is in here

The repository is organized around the four Genie Code configuration surfaces,
plus reference docs.

- **Workspace Instructions** is the org-wide policy that every analyst inherits.
  It carries the indicator-handling and data-egress rules, so investigation data
  does not leave the workspace without explicit, per-action approval.
- **User Instructions** is an example of per-analyst tuning, the output style and
  investigation method one analyst prefers.
- **Workspace Skills** are the shared investigation workflows, the five-move vibe
  investigation pattern and the Lakewatch query conventions.
- **User Skills** is a personal workflow, formatting a stakeholder-ready timeline.

## Layout

```
vibe-investigating/
├── README.md
├── LICENSE
├── docs/
│   ├── genie-code-config-model.md   # the four surfaces, exact paths, limits, MCP
│   └── best-practices.md            # instructions, skills, agent mode, MCP
├── workspace-instructions/
│   └── .assistant_workspace_instructions.md
├── user-instructions/
│   └── .assistant_instructions.md
├── workspace-skills/
│   ├── vibe-investigation-workflow/SKILL.md
│   └── lakewatch-query-conventions/SKILL.md
└── user-skills/
    └── investigation-timeline/SKILL.md
```

## The four surfaces, in one table

Genie Code is tuned through instructions and skills, each at user and workspace
scope. Full detail, with citations, is in
[docs/genie-code-config-model.md](docs/genie-code-config-model.md).

| Surface | Lives at | Scope |
|---|---|---|
| User Instructions | `/Users/<you>/.assistant_instructions.md` | You |
| Workspace Instructions | `Workspace/.assistant_workspace_instructions.md` | Everyone (admin sets it) |
| User Skills | `/Users/<you>/.assistant/skills/<name>/` | You |
| Workspace Skills | `Workspace/.assistant/skills/<name>/` | Everyone (admin sets it) |

## Install each surface

The files here keep the exact names Genie Code expects, so installation is a
copy into the matching workspace location. The simplest path is to clone this
repository into a Databricks Git folder and copy from there.

- **Workspace Instructions.** Copy
  `workspace-instructions/.assistant_workspace_instructions.md` to
  `.assistant_workspace_instructions.md` in your `Workspace/` root. Requires a
  workspace admin. Each instruction file is capped at 20,000 characters.
- **User Instructions.** Copy `user-instructions/.assistant_instructions.md` to
  `.assistant_instructions.md` in your user home, `/Users/<you>/`.
- **Workspace Skills.** Copy each folder under `workspace-skills/` into
  `Workspace/.assistant/skills/`, keeping the folder and its `SKILL.md`.
- **User Skills.** Copy each folder under `user-skills/` into
  `/Users/<you>/.assistant/skills/`.

Two related mechanisms are not files in this repository. Genie Code attaches MCP
servers through its settings UI, capped at 20 tools across all servers. Genie
Code also auto-discovers `AGENTS.md` and `CLAUDE.md` files by walking up the
directory tree from an open file.

## The safety directive

The workspace instructions enforce a default-deny posture on data egress. Genie
Code will not send an indicator, an IP, a hash, a hostname, an account, or any
other investigation artifact to an external MCP server or tool without naming
exactly what it intends to send, naming the destination, and waiting for explicit
approval. Approval covers one indicator to one destination, one time, and does not
carry forward. The reasoning is in the file itself. Looking up an indicator
against an external service is an observable act, and a premature lookup can tip
off an adversary or breach chain of custody.

## Scope and disclaimers

- This is talk material and a configuration template, not official Databricks
  documentation. It summarizes and links the official Genie Code docs, which are
  authoritative.
- The example entities, hosts, addresses, and timelines are fictional.
  Addresses use the RFC 5737 documentation ranges. Adapt every example to your
  own workspace, catalog, and schema before use.
- Lakewatch table and field names vary by workspace. Confirm them against your
  Lakewatch documentation at https://docs.lakewatch.com.

## License

Copyright 2026 Dave Herrald. Licensed under the Apache License, Version 2.0. See
[LICENSE](LICENSE).
