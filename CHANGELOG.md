# Changelog

The changes to the autodesk-claude-plugins skills and tooling that users see.
Each pull request adds one section with a new version of the `autodesk-skills` plugin, so many versions can have the same date.
The version is also in `.claude-plugin/plugin.json`. Claude updates an installed plugin when that version changes.
The newest version is first. The format is [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/): a `Breaking` entry bumps the major version, an `Added` entry the minor version, and other entries the patch version.
See [.agents/rules/changelog.md](.agents/rules/changelog.md).

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
