# Changelog

The changes to the claude-plugin skills and tooling that users see.
Each pull request adds one section with a new version of the `autodesk-skills` plugin, so many versions can have the same date.
The version is also in `.claude-plugin/plugin.json`. Claude Code updates an installed plugin when that version changes.
The newest version is first. The format is [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/): a `Breaking` entry bumps the major version, an `Added` entry the minor version, and other entries the patch version.
See [.agents/rules/changelog.md](.agents/rules/changelog.md).

## [1.0.1] - 2026-10-27

### Changed
- `CONTRIBUTING.md` and `Docs/Security-And-Governance.md` say that a pull request can merge with rebase or squash. Rebase keeps each commit of a stacked pull request on `main`.

## [1.0.0] - 2026-10-27

### Added
- The `autodesk-skills` plugin and the `tylerwarner-plugins` marketplace.
- The `aps-docs` skill. It answers Autodesk Platform Services questions from the live documentation, and gives portal links. It started as the `aps-docs-portal` skill from the Autodesk Platform Services `skills` repository, with these changes:
  - A Python script (standard library only) reads the docs. The skill no longer needs `curl`, `jq`, or `htmlq`, so it works on Windows without extra tools.
  - Portal links come from the table of contents, so they are correct for pages whose portal path is different from the source path.
  - The source table, the glossary, and the webhook example match the live docs on 2026-10-27.
