---
name: Plugin Manifests
description: Rules for the Claude plugin and marketplace manifests, and for any hook or MCP server added to the plugin
triggers:
  - Editing .claude-plugin/marketplace.json or .claude-plugin/plugin.json
  - Adding a hook, an MCP server, a subagent, or a command to the plugin
  - Renaming the plugin or the marketplace
  - Editing .gitattributes
globs:
  - ".claude-plugin/**"
  - ".gitattributes"
---

## Manifests

- The repository root is the marketplace and the plugin: `marketplace.json` lists one plugin with `"source": "."`. Keep `skills/` at the root.
- `version` in `plugin.json` is the plugin version. Users get a change only when it changes, so each pull request bumps it, with the same version on top of `CHANGELOG.md`. Open `.agents/rules/changelog.md`. Do not put a `version` in `marketplace.json`: the one in `plugin.json` wins, and 2 copies can disagree.
- Names are a contract: the marketplace `tylerwarner-autodesk` and the plugin `autodesk-skills`. Skills show as `/autodesk-skills:<skill>`, and the install id is `autodesk-skills@tylerwarner-autodesk`.
- The marketplace is for Autodesk plugins only. A plugin that is not for Autodesk goes in a different marketplace. To add a second Autodesk plugin, move each plugin into `plugins/<name>/` with its own `.claude-plugin/plugin.json`, and set each `source` to `./plugins/<name>`. The install ids do not change. A rename changes `extraKnownMarketplaces` on each machine and the docs. Do it in one pull request.
- Keep MCP servers inline in `plugin.json`. A root `.mcp.json` would also be the project MCP file for each person who opens this repo.
- A plugin cannot set `statusLine` or most other settings. Its `settings.json` uses only `agent` and `subagentStatusLine`.
- Do not add a top-level `bin/` folder. claude.ai and Cowork then refuse to install the plugin. Chat ignores hooks, agents, and local MCP servers. See `Docs/Claude-Plugin-Distribution.md#surfaces`.
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
```

`validate` must report no error and no warning.
To load the working folder in a session without an install: `claude --plugin-dir .`, then `/reload-plugins` after each edit.
