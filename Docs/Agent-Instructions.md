# Agent Instructions

How this repository gives instructions to AI coding agents, so that one set of files works in Claude Code, GitHub Copilot, Codex, Cursor, and other clients.

## Two files, two jobs

| File | Read | Holds |
|---|---|---|
| `AGENTS.md` | At the start of each session | The facts that every task needs, and the list of rules with their triggers |
| `.agents/rules/<topic>.md` | Only when its trigger fits the task | The detail for one topic |

`AGENTS.md` is an open convention that most coding agents read (see [agents.md](https://agents.md/)).
No client reads `.agents/rules/` by itself. An agent opens a rule only because the list in `AGENTS.md` tells it to. So each rule needs an entry in that list.

## Why not CLAUDE.md

Claude Code reads `AGENTS.md` only when the project has no `CLAUDE.md` or `CLAUDE.local.md`. A `CLAUDE.md` in this repo would hide `AGENTS.md` from Claude Code, and other clients would not read it.
If Claude-only text is ever necessary, put it in a `CLAUDE.md` whose first line is `@AGENTS.md`. That line imports the shared file.
Do not use a symlink in place of the import. On Windows, a symlink needs extra rights, and git can check it out as a plain text file.

## Writing a trigger

A trigger says exactly when to open the rule. Name files, folders, commands, or kinds of request:

- Good: "Open when editing anything under `skills/`."
- Bad: "Open when relevant."

## Rule file format

```markdown
---
name: Skill Authoring
description: One line that says what the rule covers
triggers:
  - Creating or editing a file under skills/
globs:
  - "skills/**"
---

The rule text.
```

| Field | Use |
|---|---|
| `name` | A short title |
| `description` | One line |
| `triggers` | When to open the rule. Use the same words in the `AGENTS.md` list. |
| `globs` | The files that the rule is about. People and agents read it. No client enforces it. |

Keep one topic in each rule. Put history and measurements in `Docs/`, not in a rule.

## Check

Start a new Claude Code session in the repo and run `/memory`. `AGENTS.md` must be in the list.

## References

- [Claude Code memory and AGENTS.md](https://code.claude.com/docs/en/memory)
- [agents.md](https://agents.md/)
