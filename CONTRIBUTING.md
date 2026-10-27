# Contributing to claude-plugin

This repository is the `autodesk-skills` Claude Code plugin.
Read this document before you open a pull request.

For how to write a skill, see [Docs/Contributing-Skills.md](Docs/Contributing-Skills.md).
For the review tiers, see [Docs/Security-And-Governance.md](Docs/Security-And-Governance.md).
For instructions to a coding agent that works on this repository, see [AGENTS.md](AGENTS.md).

## Before you start

- **Check the existing skills first.** A skill that is close to what you need may need a new section, not a new skill. See [Docs/Skill-Catalog.md](Docs/Skill-Catalog.md).
- **Know that each version ships.** Claude Code updates the plugin when `version` in `plugin.json` changes. A merge to `main` that does not change it reaches nobody.
- **Know the review tier.** A skill with `scripts/` or `assets/`, a hook, or an MCP server runs code on the user machine. It is tier 2. Say so in the pull request description.

## Make the change

1. Branch from `main`. Use a name that describes the change (ex. `feature/aps-auth-skill`, `fix/aps-docs-toc`).
2. Make the change. Keep the diff small: one subject for each pull request.
3. Add a new version to [CHANGELOG.md](CHANGELOG.md) and `.claude-plugin/plugin.json`. See [Changelog and version](#changelog-and-version).
4. Test the change from the repository root. The command must report no error and no warning:

   ```
   claude plugin validate .
   ```

   For a skill, also do the steps in [Testing before you submit](Docs/Contributing-Skills.md#testing-before-you-submit).

## Changelog and version

`CHANGELOG.md` is where users see what changed. Each pull request is one new version of the plugin, with one section in `CHANGELOG.md`.

1. Add a section on top of the newest one: `## [x.y.z] - <today>` (ex. `## [1.1.0] - 2026-11-02`).
2. Put each entry under one of these subsections, in this order: `Breaking`, `Added`, `Changed`, `Fixed`, `Removed`, `Security`. Write what a user sees, not how the code changed.
3. Choose the version from the newest version on `main`:

   | Your section has | Bump | Example from 1.2.1 |
   |---|---|---|
   | A `Breaking` entry | Major | 2.0.0 |
   | An `Added` entry, and no `Breaking` | Minor | 1.3.0 |
   | Only `Changed`, `Fixed`, `Removed`, or `Security` | Patch | 1.2.2 |

4. Set the same version in `"version"` in `.claude-plugin/plugin.json`.

The full format is in [.agents/rules/changelog.md](.agents/rules/changelog.md).

## Pull requests

All changes go through a pull request to `main`. Do not push to `main`.

- **Title:** say what changes, in the imperative (ex. "Add an APS authentication skill").
- **Description:** a summary, and how you tested the change. For a skill, paste a short transcript that shows the skill starting from a plain request.
- **Merge:** squash only.

## Writing style

All written content uses ASD-STE100: short sentences, one instruction for each sentence, active voice.
Use `-`, never an em dash or an en dash. Use `ex.` instead of `e.g.`.
