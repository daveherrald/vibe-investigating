# Genie Code configuration model

Genie Code is the agentic AI coding and data assistant inside the Databricks
workspace. It generates and runs code, builds pipelines and dashboards, debugs
errors, and works directly against Unity Catalog data, in both a conversational
Chat mode and an autonomous Agent mode. This repository configures Genie Code for
security investigation work.

This page describes the configuration surfaces and where each one lives. It
summarizes the official Databricks documentation linked at the bottom. When this
page and the official docs disagree, the official docs win.

## The configuration surfaces

Genie Code is tuned through two kinds of artifact, instructions and skills, each
at two scopes, user and workspace. MCP servers are a separate lever attached
through the UI.

| Surface | File or location | Scope | Who sets it |
|---|---|---|---|
| User Instructions | `.assistant_instructions.md` in `/Users/<username-or-email>/` | Your own interactions | The individual user |
| Workspace Instructions | `.assistant_workspace_instructions.md` in the `Workspace/` root | Everyone in the workspace | Workspace admin only |
| User Skills | `/Users/<username>/.assistant/skills/<skill-name>/` | Your own interactions | The individual user |
| Workspace Skills | `Workspace/.assistant/skills/<skill-name>/` | Everyone in the workspace | Workspace admin |

### Instructions

Instructions are persistent, plain-markdown rules that Genie Code applies to its
responses. Two facts govern how they combine.

- Genie Code generally prioritizes workspace instructions over user instructions
  when the two conflict.
- Each instruction file is capped at 20,000 characters. Anything past that limit
  is ignored.

Instructions apply to Chat, Agent mode, inline suggestions, and Suggest Fix.
They do not apply to Quick Fix or Autocomplete.

### Skills

A skill is a folder containing a required `SKILL.md` file. Skills follow the open
Agent Skills standard, so the format matches the skills used by other assistants
including Claude. The `SKILL.md` opens with YAML frontmatter carrying two fields:

```yaml
---
name: skill-name
description: A description of what this skill does and when to use it.
---
```

The markdown body holds step-by-step instructions, examples, and edge cases. A
skill folder may also contain supporting files, such as scripts the agent can run
or extra markdown referenced by relative path. A workspace skill folder looks
like this:

```
Workspace/.assistant/skills/
└── ml-workflows/
    ├── SKILL.md
    ├── training-patterns.md
    └── scripts/
        └── model-deploy.py
```

In Agent mode, Genie Code auto-loads a skill when the request matches the skill's
`description`, which is why the description should be specific about what the
skill does and when to use it. You can also force a skill with an `@` mention.
Edits to a skill do not apply to an active chat thread. Start a new thread for a
change to take effect.

### MCP servers

MCP servers extend Genie Code with external tools and data. They are attached
through the Genie Code settings panel in the UI, not through a config file in
this repository. Available server types include Unity Catalog functions, AI
Search indexes, Genie Spaces, external MCP servers reached through a Unity Catalog
connection, and custom MCP servers hosted as Databricks Apps. MCP access is
capped at 20 tools across all servers.

Because MCP is the path by which investigation data can leave the workspace, the
egress control rules in the workspace instructions of this repository govern how
Genie Code is allowed to use it.

## Repository-checked-in instructions

Separate from the four surfaces above, Genie Code auto-discovers `AGENTS.md` and
`CLAUDE.md` files. When you open a file or notebook, it walks up the directory
tree and injects any it finds, with no configuration. This is useful for
project-scoped guidance that travels with a Git folder.

A note on a known discrepancy. The Databricks personalization blog loosely
describes the auto-discovered `AGENTS.md` and `CLAUDE.md` files as "workspace
instructions." The product documentation treats them as a distinct mechanism from
the admin-managed `.assistant_workspace_instructions.md` file. This repository
follows the documentation and treats them as two different things.

## Sources

- Genie Code overview: https://docs.databricks.com/aws/en/genie-code/
- Add custom instructions: https://docs.databricks.com/aws/en/genie-code/instructions
- Extend Genie Code with agent skills: https://docs.databricks.com/aws/en/genie-code/skills
- Agent Skills overview: https://docs.databricks.com/aws/en/agent-skills/
- Connect Genie Code to MCP servers: https://docs.databricks.com/aws/en/genie-code/mcp
- Agent Skills standard: https://agentskills.io
- Personalizing Genie Code (blog): https://www.databricks.com/blog/personalizing-genie-code-instructions-skills-memory-and-mcp
- Reference skills repos: https://github.com/databricks/databricks-agent-skills and https://github.com/databricks-solutions/genie-code-skills-demo
