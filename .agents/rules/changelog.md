---
name: Changelog
description: How each pull request adds a new plugin version to CHANGELOG.md and plugin.json, and the format
triggers:
  - Before you create or update a pull request
  - Editing CHANGELOG.md, or the version in a plugins/<plugin>/.claude-plugin/, .codex-plugin/, or .cursor-plugin/ plugin.json
globs:
  - "CHANGELOG.md"
  - "plugins/*/.claude-plugin/plugin.json"
  - "plugins/*/.codex-plugin/plugin.json"
  - "plugins/*/.cursor-plugin/plugin.json"
---

## Why each pull request adds a version

Each pull request is one new version of every plugin. All plugins share one version, so a user never has to compare versions across plugins. The version is in these places, and they must be the same:

- The newest section of `CHANGELOG.md`, where users see what changed.
- `"version"` in `plugins/<plugin>/.claude-plugin/plugin.json`, `.codex-plugin/plugin.json` and `.cursor-plugin/plugin.json` of **every** plugin. Claude updates an installed plugin only when this value changes. A merge that does not change it reaches nobody.

A plugin that did not change also gets the new version. Its users get an update with no change, which does no harm.

A change that users do not see (ex. a docs fix) is still a patch version with a short entry.
Many pull requests can merge on the same day. Each one has its own version.

## Format

```markdown
## [1.3.0] - 2026-10-20

### Added
- A new skill, option, or document. ([PR #12](https://github.com/tylerwarner33/autodesk-agent-skills/pull/12))

### Fixed
- A defect that is corrected. ([PR #12](https://github.com/tylerwarner33/autodesk-agent-skills/pull/12))

## [1.2.1] - 2026-10-20
```

| Rule | Detail |
|---|---|
| Section heading | `## [x.y.z] - yyyy-MM-dd`, one section for each pull request. The newest version is first. A date is not newer than the date above it, and not in the future. |
| Subsections | Only these, in this order: `Breaking`, `Added`, `Changed`, `Fixed`, `Removed`, `Security`. Leave out a subsection that has no entry. Do not write "None." |
| Entry | One `- ` line for each change. Write what the user sees, not how the code changed. A second line of detail is an indented sub-item. |
| PR link | End each entry with `([PR #<id>](<URL>))`. The PR number is known only after the PR exists: add the link in a second commit, or leave it out. |
| Writing style | ASD-STE100, as in the rest of the repository. Use the skill names without a prefix. |

## Which version

The subsections of your section decide the version. Start from the newest version on `main`:

| Your section has | Bump | Example from 1.2.1 |
|---|---|---|
| A `Breaking` entry | Major | 2.0.0 |
| An `Added` entry, and no `Breaking` | Minor | 1.3.0 |
| Only `Changed`, `Fixed`, `Removed`, or `Security` | Patch | 1.2.2 |

| Subsection | Use for |
|---|---|
| `Breaking` | A user must do something (ex. use a new skill name). Say what to do. |
| `Added` | A new skill, option, or document. |
| `Changed` | A change of behavior in something that exists. |
| `Fixed` | A defect that is corrected. |
| `Removed` | Something that no longer exists. |
| `Security` | A change that closes a risk. |

## Steps

1. Find the newest version on `main`: the first `## [` heading in `CHANGELOG.md`.
2. Write your entries in a new section on top of it. Choose the version from the table above, and use today's date.
3. Set the same version in `"version"` in the 3 manifests (`.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`) of every plugin.
4. After you create the pull request, add the PR link to each entry (optional).

When another pull request merges first, merge the latest `main` into your branch, put your section on top of the other one, and compute your version again.

The PR validation workflow checks these rules on each pull request (see `.agents/rules/pipelines.md`).

## One changelog

`CHANGELOG.md` at the repository root is the only changelog. Do not add a changelog to a skill folder. Name the skill in the entry instead.
