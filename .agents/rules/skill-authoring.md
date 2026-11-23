---
name: Skill Authoring
description: The skill folder layout and names, SKILL.md frontmatter, path variables, and how to validate and test a skill in a plugin
triggers:
  - Creating a new skill or editing any file under plugins/<plugin>/skills/
  - Editing SKILL.md frontmatter (name, description, allowed-tools, compatibility, metadata)
  - Adding scripts/, assets/, or tests/ to a skill
  - claude plugin validate reports an error or warning
globs:
  - "plugins/*/skills/**"
---

## Folder and name

- One folder per skill: `plugins/<plugin>/skills/<name>/SKILL.md`. The folder name and the `name:` field must be identical.
- Names are lowercase kebab-case, and start with the product (ex. `aps-docs`, `inventor-modeling`). Claude Code shows the plugin name as a prefix (`/inventor-api:inventor-modeling`), but other hosts and a list of skills from several sources do not. The product in the name keeps the skill clear there, and keeps it apart from a skill of an Inventor MCP server with a similar topic.
- A name says what the skill does. Do not use a name that only makes sense with the prefix (ex. `skills`).
- A skill names only the skills of its own plugin. A user can install one plugin without the others. When a fact from another plugin is needed, write it in this skill.

## Inventor skills name only the Inventor API

A skill in an `inventor-*` plugin must work with any tool that drives Inventor: an add-in, a plugin, a Design Automation app, or any Inventor MCP server.

- Name Inventor API members (ex. `PartFeature.HealthStatus`), not the tools of one MCP server (ex. `inventor_health`).
- Write the API calls in full. Do not use a script helper of one server (ex. `InTransaction`, `OpenOrReuseDocument`, `StartDeadline`).
- Confirm each new API member in the Inventor API reference before you write it.
- The steps of one server (which tool to call, what its result means) belong in that server's own skills.

`Pipelines/Scripts/Test-SkillPortability.ps1` checks the tool names, the known helpers, and the skill names of other plugins.
- Optional folders: `references/` (loaded on demand), `scripts/` (code the skill runs), `assets/` (templates, images), `tests/` (required when `scripts/` exists).

## Frontmatter

```yaml
---
name: my-skill
description: >-
  What the skill does, then "Use when ..." with the phrases a user would say.
compatibility: >-
  Only when the skill needs something beyond the agent itself (ex. Python 3.9 or later).
allowed-tools: >-
  Read Grep
---
```

- Keep to the [Agent Skills specification](https://agentskills.io/specification) fields.
- `name` has 64 characters or fewer, with only lowercase letters, digits, and single hyphens. `description` has 1024 characters or fewer, with no XML tags. `compatibility` has 500 characters or fewer.
- `allowed-tools` **must be a space-separated string**, not a YAML list.
- `allowed-tools` pre-approves tools while the skill runs. List only the tools the workflow needs. Do not pre-approve `Bash`, `Write`, or `Edit` in general.

## Paths inside a skill

Reference a bundled file as `"${CLAUDE_SKILL_DIR}/scripts/<file>"`. Never hard-code an install path.
The plugin cache folder name has the plugin version (`~/.claude/plugins/cache/tylerwarner-autodesk/<plugin>/<version>/`), so it changes with each update.
State in `SKILL.md` that `${CLAUDE_SKILL_DIR}` is the folder that holds `SKILL.md`.
Claude Code and Cowork replace `${CLAUDE_SKILL_DIR}`. Chat on claude.ai does not: it copies the skill folder into the code execution sandbox. State in `SKILL.md` that, when the placeholder is not replaced, Claude uses the path relative to the folder of `SKILL.md`.

## All surfaces

A skill must work in Claude Code, in chat (claude.ai, desktop app, mobile), and in Cowork. See `Docs/Claude-Plugin-Distribution.md#surfaces`.

- `allowed-tools` applies only in Claude Code. Do not depend on it for the skill to work.
- A script that uses the network needs network egress in chat and Cowork. Name each domain in `compatibility`, in the `Cannot reach` error guidance of `SKILL.md`, and in `Docs/Setup-Guide.md`.
- A script uses only what the chat code execution sandbox has. Prefer the Python standard library.

## Size

Keep `SKILL.md` under about 200 lines. Move field templates, long references, and troubleshooting tables into `references/*.md` and link them.
Diagrams belong in `Docs/Skill-Catalog.md`, not in `SKILL.md`.

## Validate

From the repository root:

```
claude plugin validate plugins/<plugin>
```

`validate` must report no error and no warning in the manifests and the skills. A skill change is also a new plugin version: open `.agents/rules/changelog.md`.

To test the skill in a session, load the working folder as the plugin. Nothing is installed:

```
claude --plugin-dir plugins/<plugin>
```

Ask for the task the way a user would, without the skill name, and check that the skill loads. After each edit, run `/reload-plugins`.

## In the same pull request

- Add or update the skill's row in the `README.md` skills table.
- Add or update the skill's section in `Docs/Skill-Catalog.md`.
