# Changelog

The changes to the autodesk-agent-skills plugins and tooling that users see.
Each pull request adds one section with a new version of every plugin, so many versions can have the same date.
All plugins share one version, which is also in `plugins/<plugin>/.claude-plugin/plugin.json`. Claude updates an installed plugin when that version changes.
The newest version is first. The format is [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/): a `Breaking` entry bumps the major version, an `Added` entry the minor version, and other entries the patch version.
See [.agents/rules/changelog.md](.agents/rules/changelog.md).

## [3.0.1] - 2026-11-24

### Changed
- The skills `inventor-api-traps` and `inventor-modeling`, the Skill Catalog and the README use US spelling (ex. centimeters). ([PR #13](https://github.com/tylerwarner33/autodesk-agent-skills/pull/13))
- The PR validation check that an Inventor skill names no script helper of one MCP server also finds the helpers `ToMillimeters` and `FromMillimeters`, the new names in the Autodesk Inventor MCP Server 2.1.0. ([PR #13](https://github.com/tylerwarner33/autodesk-agent-skills/pull/13))

## [3.0.0] - 2026-11-23

### Breaking
- The plugin `autodesk-skills` is now `aps-documentation`, and its skill is now `/aps-documentation:aps-docs`. Claude Code moves your settings to the new name. Run `claude plugin marketplace update tylerwarner-autodesk`, then `claude plugin install aps-documentation@tylerwarner-autodesk` once. ([PR #12](https://github.com/tylerwarner33/autodesk-agent-skills/pull/12))
- The repository is now `tylerwarner33/autodesk-agent-skills`. The old URL redirects. Use the new name in a new install. The marketplace name `tylerwarner-autodesk` does not change. ([PR #12](https://github.com/tylerwarner33/autodesk-agent-skills/pull/12))

### Added
- The plugin `inventor-api`, with the skills `inventor-api-traps`, `inventor-modeling`, and `inventor-drawings`. ([PR #12](https://github.com/tylerwarner33/autodesk-agent-skills/pull/12))
- The plugin `inventor-ilogic`, with the skill `inventor-ilogic`. ([PR #12](https://github.com/tylerwarner33/autodesk-agent-skills/pull/12))
- The plugin `inventor-data`, with the skill `inventor-projects-and-files`. ([PR #12](https://github.com/tylerwarner33/autodesk-agent-skills/pull/12))
  - The Inventor skills come from the Autodesk Inventor MCP Server. They name only the Inventor API, so they work with any tool that drives Inventor.
- A check in the PR validation workflow: each plugin is self-contained, and an Inventor skill names no tool or script helper of one MCP server. ([PR #12](https://github.com/tylerwarner33/autodesk-agent-skills/pull/12))
- OpenAI Codex and Cursor can install the plugins. The repository is also a Codex marketplace (`.agents/plugins/marketplace.json`) and a Cursor marketplace (`.cursor-plugin/marketplace.json`), and each plugin has a Codex and a Cursor manifest. See the Setup Guide. ([PR #12](https://github.com/tylerwarner33/autodesk-agent-skills/pull/12))
- A check in the PR validation workflow: the Codex and Cursor manifests have the same plugins, names, versions, and descriptions as the Claude manifests. ([PR #12](https://github.com/tylerwarner33/autodesk-agent-skills/pull/12))

### Changed
- All plugins share one version. Each pull request sets it in every `plugin.json`. ([PR #12](https://github.com/tylerwarner33/autodesk-agent-skills/pull/12))

## [2.2.1] - 2026-11-05

### Changed
- The `README.md` in the skills folder now also links to the Agent Skills overview page.

## [2.2.0] - 2026-11-04

### Added
- A `README.md` in the marketplace folder, the plugin manifest folder, and the skills folder. Each one links to the matching page of the official Claude Code documentation.

## [2.1.2] - 2026-11-03

### Changed
- The `aps-docs` baseline now comes from a full eval run with 3 runs for each case, and not from the single-run pilot. The skill adds +0.28 to the mean score. The skill itself did not change.

## [2.1.1] - 2026-11-03

### Changed
- An installed copy of `autodesk-skills` now holds only the plugin. The repository docs, evals, and pipelines no longer install with it. The install id and the skills did not change, so you do not have to do anything.

## [2.1.0] - 2026-11-03

### Added
- An eval suite for `aps-docs` in `evals/aps-docs/`. It has 7 cases (5 must use the skill, 2 must not), a quality spec, and a baseline of the measured uplift. See `evals/README.md` for how to run it.

## [2.0.2] - 2026-11-03

### Fixed
- `aps-docs`: the skill now tells Claude to run each script call as its own command. A call that used a variable or joined commands could be denied, and then the skill answered without the live docs.

## [2.0.1] - 2026-10-28

### Changed
- The README title is now "Autodesk Claude Plugins", and the README shows badges for the Claude surfaces, the license, and the plugin version.

## [2.0.0] - 2026-10-27

### Breaking
- The marketplace is now `tylerwarner-autodesk` (it was `tylerwarner-plugins`), and the install id is `autodesk-skills@tylerwarner-autodesk`. Remove the old marketplace, then add it again:
  - `claude plugin marketplace remove tylerwarner-plugins`
  - `claude plugin marketplace add tylerwarner33/autodesk-claude-plugins`
  - `claude plugin install autodesk-skills@tylerwarner-autodesk`

### Added
- Install steps for claude.ai, the Claude desktop app, and Cowork. The plugin works on these surfaces and in Claude Code.

### Changed
- The repository is now `tylerwarner33/autodesk-claude-plugins`, a marketplace for more than one Autodesk plugin. The old URL redirects. Use the new name in a new install.
- `aps-docs` finds its script in a claude.ai chat, where `${CLAUDE_SKILL_DIR}` is not replaced. When the docs cannot be reached in chat or Cowork, it tells the user which domains to allow.

## [1.1.0] - 2026-10-27

### Added
- A PR validation workflow. It checks the skill frontmatter, the plugin manifests, the skill tests, the forbidden characters, and the changelog and version on each pull request. A pull request cannot merge until it passes.

## [1.0.1] - 2026-10-27

### Changed
- `CONTRIBUTING.md` says how a pull request gets its approval: the code owner review and the admin bypass.

## [1.0.0] - 2026-10-27

### Added
- The `autodesk-skills` plugin and the `tylerwarner-plugins` marketplace.
- The `aps-docs` skill. It answers Autodesk Platform Services questions from the live documentation, and gives portal links. It started as the `aps-docs-portal` skill from the Autodesk Platform Services `skills` repository, with these changes:
  - A Python script (standard library only) reads the docs. The skill no longer needs `curl`, `jq`, or `htmlq`, so it works on Windows without extra tools.
  - Portal links come from the table of contents, so they are correct for pages whose portal path is different from the source path.
  - The source table, the glossary, and the webhook example match the live docs on 2026-10-27.
