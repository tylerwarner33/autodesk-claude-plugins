---
name: Plugin Manifests
description: Rules for the Claude plugin and marketplace manifests, and for any hook or MCP server added to the plugin
triggers:
  - Editing .claude-plugin/marketplace.json or plugins/autodesk-skills/.claude-plugin/plugin.json
  - Adding a hook, an MCP server, a subagent, or a command to the plugin
  - Renaming the plugin or the marketplace
  - Editing .gitattributes
globs:
  - ".claude-plugin/**"
  - "plugins/*/.claude-plugin/**"
  - ".gitattributes"
---

## Manifests

- The repository root is the marketplace. The plugin is `plugins/autodesk-skills/`: `marketplace.json` lists it with `"source": "./plugins/autodesk-skills"`, and Claude installs only that folder. Keep files that users do not need (docs, evals, pipelines) outside `plugins/`.
- `version` in `plugin.json` is the plugin version. Users get a change only when it changes, so each pull request bumps it, with the same version on top of `CHANGELOG.md`. Open `.agents/rules/changelog.md`. Do not put a `version` in `marketplace.json`: the one in `plugin.json` wins, and 2 copies can disagree.
- Names are a contract: the marketplace `tylerwarner-autodesk` and the plugin `autodesk-skills`. Skills show as `/autodesk-skills:<skill>`, and the install id is `autodesk-skills@tylerwarner-autodesk`.
- The marketplace is for Autodesk plugins only. A plugin that is not for Autodesk goes in a different marketplace. To add a second Autodesk plugin, add `plugins/<name>/` with its own `.claude-plugin/plugin.json` and `LICENSE`, and add an entry with `"source": "./plugins/<name>"`. A rename changes `extraKnownMarketplaces` on each machine and the docs. Do it in one pull request.
- Keep MCP servers inline in `plugin.json`. A root `.mcp.json` would also be the project MCP file for each person who opens this repo.
- A plugin cannot set `statusLine` or most other settings. Its `settings.json` uses only `agent` and `subagentStatusLine`.
- `plugins/autodesk-skills/LICENSE` is a copy of the root `LICENSE`, because an installed copy has only the plugin folder. Keep the 2 files the same.
- Do not add a top-level `bin/` folder to a plugin. claude.ai and Cowork then refuse to install the plugin. Chat ignores hooks, agents, and local MCP servers. See `Docs/Claude-Plugin-Distribution.md#surfaces`.
- Reference: <https://code.claude.com/docs/en/plugins/manifest-reference>.

## Tier 2

A hook or an MCP server runs with the user's rights, outside the sandbox, and Claude Code does not ask before it runs it.
The plugin has none now. Before you add one, update `Docs/Security-And-Governance.md` and say in the pull request description that the change is tier 2.
Add a hook in `hooks/hooks.json` and start a script with `bash "${CLAUDE_PLUGIN_ROOT}/hooks/<file>.sh"`.

## Line endings

`.gitattributes` keeps `*.sh` LF. Claude Code clones with the user's git settings, and `core.autocrlf=true` is the Git for Windows default.

## Test

```
claude plugin validate .
claude plugin validate plugins/autodesk-skills
```

The first command checks the marketplace. The second checks the plugin. Each must report no error and no warning in the manifests. The `ICON_MISSING` finding is for a listing in the plugin directory, and it does not fail.
To load the working folder in a session without an install: `claude --plugin-dir plugins/autodesk-skills`, then `/reload-plugins` after each edit.
