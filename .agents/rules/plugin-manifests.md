---
name: Plugin Manifests
description: Rules for the Claude plugin and marketplace manifests, for adding, renaming or removing a plugin, and for any hook or MCP server added to a plugin
triggers:
  - Editing .claude-plugin/marketplace.json or plugins/<plugin>/.claude-plugin/plugin.json
  - Adding a hook, an MCP server, a subagent, or a command to a plugin
  - Adding, renaming, or removing a plugin, or renaming the marketplace
  - Editing .gitattributes
globs:
  - ".claude-plugin/**"
  - "plugins/*/.claude-plugin/**"
  - ".gitattributes"
---

## Manifests

- The repository root is the marketplace. Each plugin is `plugins/<plugin>/`: `marketplace.json` lists it with `"source": "./plugins/<plugin>"`, and Claude installs only that folder. Keep files that users do not need (docs, evals, pipelines) outside `plugins/`.
- `version` in `plugin.json` is the plugin version. All plugins share one version. Users get a change only when it changes, so each pull request bumps it in every `plugin.json`, with the same version on top of `CHANGELOG.md`. Open `.agents/rules/changelog.md`. Do not put a `version` in `marketplace.json`: the one in `plugin.json` wins, and 2 copies can disagree.
- Names are a contract: the marketplace `tylerwarner-autodesk`, and the plugins `aps-documentation`, `inventor-api`, `inventor-ilogic`, and `inventor-data`. Skills show as `/<plugin>:<skill>`, and the install id is `<plugin>@tylerwarner-autodesk`.
- Split plugins by focus, as `<product>-<area>` (ex. `inventor-ilogic`). Do not add a `-skills` suffix: the plugin name is the slash prefix of each skill, and a plugin can later also hold a hook or an MCP server.
- The marketplace is for Autodesk plugins only. A plugin that is not for Autodesk goes in a different marketplace. To add an Autodesk plugin, add `plugins/<name>/` with its own `.claude-plugin/plugin.json` (with the shared version), `.claude-plugin/README.md`, `skills/README.md`, and `LICENSE`, and add an entry with `"source": "./plugins/<name>"`.

## Rename or remove a plugin

A plugin name is the install id on each machine, so a rename breaks each install. Do it only when the name is wrong, and in one pull request:

1. Move the folder (`git mv plugins/<old> plugins/<new>`) and change `name` in its `plugin.json`.
2. Add an entry to the top-level `renames` map in `marketplace.json`: `"<old>": "<new>"`. For a removed plugin, use `"<old>": null`. Treat the map as append-only history: never edit or delete an entry. For a second rename, add a new entry, because Claude Code follows the chain from the oldest name.
3. Add a `Breaking` entry to `CHANGELOG.md`. Claude Code moves the settings to the new name, but a user of a marketplace from git must run `claude plugin install <new>@tylerwarner-autodesk` once.
4. Change every doc, rule, and eval that names the old plugin. Leave the old name in the `CHANGELOG.md` history and in `evals/*/results/`.

A rename of the marketplace changes `extraKnownMarketplaces` on each machine, and no `renames` map exists for it. Do not rename the marketplace.
Reference: <https://code.claude.com/docs/en/plugins/host-marketplace>.
- Keep MCP servers inline in `plugin.json`. A root `.mcp.json` would also be the project MCP file for each person who opens this repo.
- A plugin cannot set `statusLine` or most other settings. Its `settings.json` uses only `agent` and `subagentStatusLine`.
- `plugins/<plugin>/LICENSE` is a copy of the root `LICENSE`, because an installed copy has only the plugin folder. Keep the 2 files the same.
- Do not add a top-level `bin/` folder to a plugin. claude.ai and Cowork then refuse to install the plugin. Chat ignores hooks, agents, and local MCP servers. See `Docs/Claude-Plugin-Distribution.md#surfaces`.
- Reference: <https://code.claude.com/docs/en/plugins/manifest-reference>.

## Tier 2

A hook or an MCP server runs with the user's rights, outside the sandbox, and Claude Code does not ask before it runs it.
No plugin has one now. Before you add one, update `Docs/Security-And-Governance.md` and say in the pull request description that the change is tier 2.
Add a hook in `hooks/hooks.json` and start a script with `bash "${CLAUDE_PLUGIN_ROOT}/hooks/<file>.sh"`.

## Line endings

`.gitattributes` keeps `*.sh` LF. Claude Code clones with the user's git settings, and `core.autocrlf=true` is the Git for Windows default.

## Test

```
claude plugin validate .
claude plugin validate plugins/<plugin>
```

The first command checks the marketplace. The second checks one plugin: run it for each plugin. Each must report no error and no warning in the manifests. The `ICON_MISSING` finding is for a listing in the plugin directory, and it does not fail.
To load the working folder in a session without an install: `claude --plugin-dir plugins/<plugin>`, then `/reload-plugins` after each edit.
