# Changelog

The changes to the claude-plugin skills and tooling that users see.
Each pull request adds one section with a new version of the `autodesk-skills` plugin, so many versions can have the same date.
The version is also in `.claude-plugin/plugin.json`. Claude Code updates an installed plugin when that version changes.
The newest version is first. The format is [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/): a `Breaking` entry bumps the major version, an `Added` entry the minor version, and other entries the patch version.
See [.agents/rules/changelog.md](.agents/rules/changelog.md).

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
