# Contributing Skills

How to author, test, and submit a skill to this repo.
A skill is part of the `autodesk-skills` Claude Code plugin. Claude Code installs a new version when `version` in `plugin.json` changes.

## Anatomy of a skill

```
skills/
└── my-skill/
    ├── SKILL.md            <- required: frontmatter + guidance
    ├── references/         <- optional: supporting docs loaded on demand
    │   └── details.md
    ├── scripts/            <- optional: code the skill runs (makes the skill tier 2)
    ├── assets/             <- optional: templates, images, data files
    └── tests/              <- required when scripts/ exists
```

A skill that runs a bundled script must reference it as `"${CLAUDE_SKILL_DIR}/scripts/<file>"`, not as a hard-coded path.
The installed folder name has the plugin version in it, so it changes with each update.

The folder name is the skill name. Do not add an `autodesk-skills-` prefix: Claude Code shows the skill `my-skill` as `/autodesk-skills:my-skill`.

`SKILL.md` frontmatter:

```yaml
---
name: my-skill
description: >-
  What the skill does AND when Claude should use it. This is the ONLY text
  Claude sees before deciding to load the skill - include trigger phrases
  the user would actually say.
allowed-tools: >-    # optional: tools pre-approved while the skill runs
  Read Grep
---
```

`allowed-tools` must be a space-separated string, not a YAML list.

Frontmatter limits:

- `name` must be the folder name: 64 characters or fewer, with only lowercase letters, digits, and single hyphens between them. It cannot contain `anthropic` or `claude`.
- `description` must have 1024 characters or fewer, with no XML tags.
- `compatibility`, if present, must have 500 characters or fewer.
- A value that contains `: ` must be quoted, or written as a `>-` block.

## Writing guidelines

- **The description is the trigger.** Claude loads a skill based on the description alone. Write it as "does X. Use when the user mentions Y or asks to Z" with concrete phrases.
- **Keep SKILL.md under ~200 lines.** Push detail into `references/*.md` files and link them. Claude reads those only when needed.
- **Be prescriptive, not encyclopedic.** State the one right way to do the task, not every possible way.
- **Show exact commands and formats.** Copy-pasteable blocks beat prose descriptions of commands.
- **Include failure guidance.** What Claude should do when a command fails prevents flailing.
- **No secrets, ever.** No tokens, keys, or connection strings. See [Security-And-Governance.md](./Security-And-Governance.md).
- **Scope tool access.** List only the tools the workflow needs in `allowed-tools`.

## Testing before you submit

1. From the repository root, start Claude Code with your working folder as the plugin. Nothing is installed:
   ```
   claude --plugin-dir .
   ```
2. Phrase a request the way a user would - do not name the skill. Confirm Claude picks it up. After each edit, run `/reload-plugins`.
3. Run the workflow end to end at least once.
4. From the repository root, run `claude plugin validate .`. It must report no error and no warning.
5. If the skill has `scripts/`, run its tests from the skill folder: `python -m unittest discover -s tests`.

## Submitting

1. Branch from `main`, add your skill under `skills/<kebab-case-name>/`.
2. Add a row to the skills table in the repo `README.md`, and a section for the skill in `Docs/Skill-Catalog.md`.
3. Add a new minor version to `CHANGELOG.md`, with the skill under `### Added`, and set the same version in `.claude-plugin/plugin.json` (see [CONTRIBUTING.md](../CONTRIBUTING.md#changelog-and-version)). A skill folder has no changelog of its own.
4. Open a PR. Describe what the skill does and paste a short transcript snippet showing it triggering correctly.
5. Read the full diff. A skill with `scripts/` or `assets/` is tier 2: say so in the PR description (see [Security-And-Governance.md](./Security-And-Governance.md#content-risk-tiers)).

To try a branch before it merges, see [Claude-Plugin-Distribution.md](./Claude-Plugin-Distribution.md#test-a-branch-before-it-merges).

## Other AI clients

The plugin is for Claude Code only. GitHub Copilot, Codex, and Cursor do not read Claude Code plugins.
Do not mirror a skill into `.github/instructions/` or any other client-specific file.
Instructions for agents that work on *this repo* are in `AGENTS.md` and `.agents/rules/` - see [Agent-Instructions.md](./Agent-Instructions.md).
