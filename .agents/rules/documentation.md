---
name: Documentation
description: Writing style, which documents to update together, and how to write agent instructions and rules for this repository
triggers:
  - Editing README.md or any file under Docs/
  - Editing AGENTS.md or a file under .agents/rules/
  - Adding, renaming, or removing a skill (the README and Skill Catalog change too)
globs:
  - "README.md"
  - "CONTRIBUTING.md"
  - "Docs/**"
  - "AGENTS.md"
  - ".agents/rules/**"
---

## Writing style

- ASD-STE100: short sentences, one instruction per sentence, active voice.
- Use `-`, never an em dash or an en dash. Use `ex.` instead of `e.g.`.
- Tables for comparisons and reference data; numbered lists for steps.
- Commands in fenced code blocks, ready to copy.

Check a change for forbidden characters:

```
LC_ALL=C.UTF-8 grep -rnP '\x{2014}|\x{2013}|(?<!`)e\.g\.' README.md CHANGELOG.md CONTRIBUTING.md Docs/*.md AGENTS.md .agents skills
```

A match right after a backtick is allowed: it is a rule that names the forbidden text (ex. "instead of `e.g.`").
The PR validation workflow runs the same check. Keep the 2 patterns the same.

## Documents that change together

| When you change | Also update |
|---|---|
| Anything, in any pull request | `CHANGELOG.md` (see `.agents/rules/changelog.md`) |
| The pull request process | `CONTRIBUTING.md`, `.agents/rules/changelog.md` |
| A skill's purpose or name | `README.md` skills table, `Docs/Skill-Catalog.md` |
| The plugin or the marketplace | `README.md`, `Docs/Claude-Plugin-Distribution.md`, `Docs/Setup-Guide.md` |
| The repository layout | `README.md` repo structure, `AGENTS.md` layout table |
| A document's name, or a new document | `README.md` documentation table |
| A review tier | `Docs/Security-And-Governance.md`, `CONTRIBUTING.md` |
| A check in the PR validation workflow | `.agents/rules/pipelines.md`, `CONTRIBUTING.md` |

## Agent instructions and rules

This repository follows its own standard in `Docs/Agent-Instructions.md`:

- `AGENTS.md` is the only root instruction file. Do not add a `CLAUDE.md` or `CLAUDE.local.md` - Claude Code then stops reading `AGENTS.md`.
- Each rule is a file in `.agents/rules/` with `name`, `description`, `triggers`, and `globs` frontmatter.
- No client loads `.agents/rules/` by itself. Every rule must have an entry in the `AGENTS.md` "On-Demand Rules" list, with a trigger that says when to open it.
- Keep `AGENTS.md` to facts every session needs. Move detail that matters only for some files into a rule.
