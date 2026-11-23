# autodesk-agent-skills

Agent skills for Autodesk development, split into plugins by focus.
This repository is a Claude plugin marketplace (`tylerwarner-autodesk`). The marketplace is at the repository root, and each plugin is in `plugins/<plugin>/`: `aps-documentation`, `inventor-api`, `inventor-ilogic`, and `inventor-data`.
Claude Code, claude.ai, the Claude desktop app, and Cowork install a plugin straight from this GitHub repo (`tylerwarner33/autodesk-agent-skills`) and update it when `version` in its `plugin.json` changes.
The Inventor skills name only the Inventor API, so they work with any tool that drives Inventor. The steps that belong to one Inventor MCP server stay in that server's own skills.
Keep each skill working on all of these surfaces: see `Docs/Claude-Plugin-Distribution.md#surfaces`.
See `README.md` for the overview and `Docs/` for the full documentation set.

These are the instructions for a coding agent that works on this repository (ex. Claude Code, GitHub Copilot, Codex, Cursor).
The instructions a model needs to *use* a skill are in that skill's own `SKILL.md`.

## Layout

| Path | Contents |
|---|---|
| `.claude-plugin/marketplace.json` | The marketplace manifest |
| `.claude-plugin/README.md`, `plugins/<plugin>/.claude-plugin/README.md`, `plugins/<plugin>/skills/README.md` | Links to the official Claude Code documentation for that folder. Keep a link current when its page moves. |
| `plugins/<plugin>/` | One plugin. Only the plugin folder installs on a user's machine. |
| `plugins/<plugin>/.claude-plugin/plugin.json` | The plugin manifest |
| `plugins/<plugin>/skills/<name>/` | One folder per skill: `SKILL.md`, and optional `references/`, `scripts/`, `assets/`, `tests/` |
| `.github/CODEOWNERS` | The required reviewer of each pull request (see `Docs/Security-And-Governance.md`) |
| `.github/workflows/` | `pr-validation.yml`, the required checks of each pull request |
| `Pipelines/Scripts/` | The PowerShell scripts that the workflow runs. You can also run them locally. |
| `.agents/rules/` | On-demand rules for agents that work on this repository (listed below) |
| `Docs/` | Documentation |
| `evals/<skill-name>/` | The eval suite of one skill: cases, graders, and a quality spec. See `evals/README.md`. The `results/` folders are local only. |
| `CHANGELOG.md` | What changed for users. One section for each pull request: `## [x.y.z] - yyyy-MM-dd`. The only changelog in the repository. |
| `CONTRIBUTING.md` | The pull request process for people |

## Working Principles

- **Everything reaches `main` through a pull request.** Branch from `main` with a name that describes the change (ex. `docs/update-setup-guide`). Never push to `main`.
- **Each version ships to every installed copy.** Claude updates a copy when `version` in `plugins/<plugin>/.claude-plugin/plugin.json` changes. Treat a change to `plugins/` or `.claude-plugin/` like a code change: small diffs, and a full read of the diff before a PR.
- **No secrets anywhere.** No tokens, keys, or connection strings in skills, docs, scripts, or commits.
- **Each pull request adds the next version.** One new section on top of `CHANGELOG.md`, and the same version in the `plugin.json` of every plugin. All plugins share one version. Open `.agents/rules/changelog.md` for the format and the version rule.
- **Keep each plugin self-contained.** A user can install one plugin without the others, so a skill names only the skills of its own plugin. An Inventor skill names no tool or script helper of one MCP server. `Pipelines/Scripts/Test-SkillPortability.ps1` checks both.
- **Validate before a PR.** From the repository root, run `claude plugin validate .` and `claude plugin validate plugins/<plugin>` for each plugin (no error and no warning in the manifests). For a skill with `scripts/`, also run `python -m unittest discover -s tests` from the skill folder. The PR validation workflow runs these checks and more on each pull request, and a pull request cannot merge until it passes.
- **Write in ASD-STE100.** Use `-`, never an em dash, and `ex.` instead of `e.g.`, in all written content.
- **The first release is 1.0.0.**

## On-Demand Rules

The rules are not loaded automatically. Before acting on a task, scan this list and open any rule whose trigger fits the request or the files about to change. If several match, open all of them.

- **`.agents/rules/changelog.md`** - Open before you create or update a pull request, or when editing `CHANGELOG.md` or the `version` in `plugins/<plugin>/.claude-plugin/plugin.json`.
- **`.agents/rules/skill-authoring.md`** - Open before creating or editing anything under `plugins/<plugin>/skills/`, including `SKILL.md` frontmatter, `allowed-tools`, `references/`, or bundled scripts, or when `claude plugin validate` reports an error.
- **`.agents/rules/plugin-manifests.md`** - Open when editing `.claude-plugin/`, `plugins/<plugin>/.claude-plugin/`, `.gitattributes`, or when adding a hook, an MCP server, a subagent, or a command to a plugin, or when adding, renaming, or removing a plugin or renaming the marketplace.
- **`.agents/rules/documentation.md`** - Open when editing `README.md`, anything under `Docs/`, or `AGENTS.md` and `.agents/rules/` themselves.
- **`.agents/rules/pipelines.md`** - Open when editing `.github/workflows/` or `Pipelines/`, when a check in the PR validation workflow fails, or when changing the required status check in the `main` ruleset.
