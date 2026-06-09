# Genie Code best practices for investigation work

Practices drawn from the official Databricks documentation and from Databricks
community write-ups, oriented toward security-investigation use. Sources are
listed at the bottom. Each practice traces to one of them.

## Instructions

- Stay under the 20,000-character limit per file. Content past the limit is
  ignored, so a long instruction file silently loses its tail.
- Use markdown headings and bullets as delimiters. Genie Code reads the structure.
- Put load-bearing references inline. Genie Code does not proactively fetch extra
  context that an instruction merely alludes to.
- Remember the scope split. Put org-wide policy, such as data-egress rules, in
  workspace instructions where an admin controls it and it applies to everyone.
  Put personal style and method in user instructions.
- Workspace instructions win over user instructions on conflict, so write user
  instructions to refine, not to override, the workspace policy.

## Skills

- One workflow per skill. A narrow scope helps Genie Code decide when to apply it.
- Write the `description` for matching. The name and description are the signal
  Genie Code uses to auto-load a skill in Agent mode, so state plainly what the
  skill does and when to use it.
- Separate guidance from automation. Keep prose in `SKILL.md` and put runnable
  code in a `scripts/` subfolder the skill references.
- Let Genie Code author skills. After you work through a repeatable workflow, ask
  it to capture the workflow as a skill, then edit the result.
- Treat skills as living documents and version them. Store the skills folder in a
  Databricks Git folder so changes are reviewed and tracked.
- Start a new chat thread after editing a skill. Edits do not apply to an active
  thread, and a stale skill usually means the thread predates the edit.

## Agent mode

- Give Agent mode a clear goal, the constraints, and the expected outcome, rather
  than a fully scripted list of steps. The agent plans the steps.
- Set guardrails. Cap interactive query row counts so an exploratory run does not
  scan more data than the question needs.
- Start a fresh chat per distinct task or dataset. The agent carries a decision
  tree, and assumptions from an unrelated task contaminate the next one.
- Keep the browser tab focused during a run. Switching tabs pauses the agent, and
  it resumes when you return.
- Stay in the loop. Intervene early if the agent loops or takes a wrong path.

## MCP and external tools

- Respect the 20-tool cap across all attached servers. Attach only the tools the
  investigation needs.
- Treat every external MCP call as data leaving the workspace. The egress control
  rules in this repository's workspace instructions apply. Ask before sending an
  indicator out, and prefer a defanged form.

## Sources

- Add custom instructions: https://docs.databricks.com/aws/en/genie-code/instructions
- Extend Genie Code with agent skills: https://docs.databricks.com/aws/en/genie-code/skills
- Connect Genie Code to MCP servers: https://docs.databricks.com/aws/en/genie-code/mcp
- Practical observations on working with Databricks Genie Code (Databricks Community): https://community.databricks.com/t5/mvp-articles/practical-observations-on-working-with-databricks-genie-code/td-p/151803
- Databricks Genie Code full practice guide and examples: https://medium.com/dbsql-sme-engineering/databricks-genie-code-full-practice-guide-and-examples-f3bcb13596f2
