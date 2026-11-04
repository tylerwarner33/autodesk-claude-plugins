# Skills

Each folder here is one skill of the `autodesk-skills` plugin.
A skill folder has a `SKILL.md` file, and can have `references/`, `scripts/`, `assets/`, and `tests/` folders.
The folder name and the `name:` field in `SKILL.md` must be the same.
Claude shows each skill with the plugin name as a prefix (ex. `/autodesk-skills:aps-docs`).

Before you add or edit a skill, read `.agents/rules/skill-authoring.md`.

## Claude documentation

| Topic | Link |
|---|---|
| Extend Claude with skills (start here) | <https://code.claude.com/docs/en/skills> |
| Skill frontmatter reference | <https://code.claude.com/docs/en/skills#frontmatter-reference> |
| Control who invokes a skill | <https://code.claude.com/docs/en/skills#control-who-invokes-a-skill> |
| Plugin components: skills in a plugin | <https://code.claude.com/docs/en/plugins/components#skills> |
| Test plugins with evals | <https://code.claude.com/docs/en/plugin-evals> |
| Plugin structure and testing on claude.ai and in Cowork | <https://claude.com/docs/plugins/build> |
| Agent Skills specification | <https://agentskills.io/specification> |

## Validate

Run this command from the repository root:

```
claude plugin validate plugins/autodesk-skills
```
