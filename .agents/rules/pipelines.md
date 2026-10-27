---
name: Pipelines
description: Rules for the PR validation workflow and its scripts, which decide what can merge (tier 2 content)
triggers:
  - Editing .github/workflows/ or Pipelines/
  - Changing the checks that run on every pull request
  - Changing the required status check in the "main" ruleset
globs:
  - ".github/workflows/**"
  - "Pipelines/**"
---

## Tier 2

These files decide what can merge to `main`.
Say in the pull request description that the change is tier 2 (see `Docs/Security-And-Governance.md`).

## PR validation workflow

- `.github/workflows/pr-validation.yml` runs on each pull request to `main`, and by hand (`workflow_dispatch`).
- The `main` ruleset requires the status check `Validate`, from the GitHub Actions app. That is the job `name`. If you rename the job, change the ruleset in the same pull request. Otherwise no pull request can merge.
- The ruleset also requires the branch to be up to date with `main`. The changelog check then always compares with the newest version on `main`.
- Use `pull_request`, never `pull_request_target`. A pull request from a fork must run with a read-only token and no secrets.
- Keep `permissions: contents: read`. The workflow has no secrets.
- Pin each action to a full commit SHA, with the tag in a comment (ex. `@3d3c42e... # v7.0.1`). A tag can move to other code.
- The runner image has `pwsh`, Python 3.12, and Node.js. Do not add a setup action for a tool that the image has.

## Scripts

- The checks are in `Pipelines/Scripts/`. Change the checks there, not inline, so that you can run them locally with the same result.
- The scripts write GitHub Actions workflow commands (`::error::`, `::warning::`). A script fails with exit code 1 when it wrote an error.
- `Test-SkillFrontmatter.ps1` has its own small YAML parser, so the workflow needs no module. It must report a form that it cannot read as an error, and never pass a value that it did not read. Use the case-sensitive operators (`-cmatch`, `-cne`, `-cin`) for names: `-match` and `-ne` ignore case.
- `Test-PluginManifest.ps1` fails on any `claude plugin validate` error or warning in the manifests. The plugin directory findings (ex. `ICON_MISSING`) do not fail.
- `Test-Changelog.ps1` checks the `CHANGELOG.md` format, and that its newest version is the `version` in `plugin.json`, on every run. In a pull request run it also needs exactly one new section with the next version: it compares `HEAD`, the merge commit that GitHub makes, with `HEAD^1`, the target branch. Keep `fetch-depth: 2` or more. The format is in `.agents/rules/changelog.md`.
- The Claude Code CLI version is pinned in `CLAUDE_CODE_VERSION`. Update it in a pull request, and run the checks locally with the new version first.
- Keep the forbidden character pattern the same as in `.agents/rules/documentation.md`.

## Run the checks locally

From the repository root, in PowerShell 7:

```
./Pipelines/Scripts/Test-SkillFrontmatter.ps1 -SourcesDirectory .
./Pipelines/Scripts/Test-PluginManifest.ps1 -SourcesDirectory .
./Pipelines/Scripts/Test-Changelog.ps1 -SourcesDirectory . -BaseRef origin/main
```

Run `git fetch` first, so that `origin/main` is the newest `main`.
