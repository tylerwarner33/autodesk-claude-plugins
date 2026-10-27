# claude-plugin

Agent skills for Autodesk Platform Services (APS) development.
This repository is a Claude Code plugin marketplace (`tylerwarner-plugins`) with one plugin (`autodesk-skills`), both at the repository root.
Claude Code installs the plugin straight from this GitHub repo (`tylerwarner33/claude-plugin`) and updates it when `version` in `plugin.json` changes.
See `README.md` for the overview and `Docs/` for the full documentation set.

These are the instructions for a coding agent that works on this repository (ex. Claude Code, GitHub Copilot, Codex, Cursor).
The instructions a model needs to *use* a skill are in that skill's own `SKILL.md`.

## Layout

| Path | Contents |
|---|---|
| `skills/<name>/` | One folder per skill: `SKILL.md`, and optional `references/`, `scripts/`, `assets/`, `tests/` |
| `.claude-plugin/` | `marketplace.json` and `plugin.json` |
| `.agents/rules/` | On-demand rules for agents that work on this repository (listed below) |
| `Docs/` | Documentation |
| `CHANGELOG.md` | What changed for users. One section for each pull request: `## [x.y.z] - yyyy-MM-dd`. The only changelog in the repository. |
| `CONTRIBUTING.md` | The pull request process for people |

## Working Principles

- **Everything reaches `main` through a pull request.** Branch from `main` with a name that describes the change (ex. `docs/update-setup-guide`). Never push to `main`.
- **Each version ships to every installed copy.** Claude Code updates a copy when `version` in `.claude-plugin/plugin.json` changes. Treat a change to `skills/` or `.claude-plugin/` like a code change: small diffs, and a full read of the diff before a PR.
- **No secrets anywhere.** No tokens, keys, or connection strings in skills, docs, scripts, or commits.
- **Each pull request adds the next version.** One new section on top of `CHANGELOG.md`, and the same version in `.claude-plugin/plugin.json`. Open `.agents/rules/changelog.md` for the format and the version rule.
- **Validate before a PR.** From the repository root, run `claude plugin validate .` (no error and no warning). For a skill with `scripts/`, also run `python -m unittest discover -s tests` from the skill folder.
- **Write in ASD-STE100.** Use `-`, never an em dash, and `ex.` instead of `e.g.`, in all written content.
- **The first release is 1.0.0.**

## On-Demand Rules

The rules are not loaded automatically. Before acting on a task, scan this list and open any rule whose trigger fits the request or the files about to change. If several match, open all of them.

- **`.agents/rules/changelog.md`** - Open before you create or update a pull request, or when editing `CHANGELOG.md` or the `version` in `.claude-plugin/plugin.json`.
- **`.agents/rules/skill-authoring.md`** - Open before creating or editing anything under `skills/`, including `SKILL.md` frontmatter, `allowed-tools`, `references/`, or bundled scripts, or when `claude plugin validate` reports an error.
- **`.agents/rules/plugin-manifests.md`** - Open when editing `.claude-plugin/`, `.gitattributes`, or when adding a hook, an MCP server, a subagent, or a command to the plugin, or when renaming the plugin or the marketplace.
- **`.agents/rules/documentation.md`** - Open when editing `README.md`, anything under `Docs/`, or `AGENTS.md` and `.agents/rules/` themselves.
