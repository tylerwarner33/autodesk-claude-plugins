# Setup Guide

How to install, update, verify, and remove the plugins of the `tylerwarner-autodesk` marketplace: `aps-documentation`, `inventor-api`, `inventor-ilogic`, and `inventor-data`. Install only the plugins that you need.
The plugins work in Claude Code, in chat on claude.ai and in the Claude desktop app, in Cowork, in OpenAI Codex, and in Cursor.

## Requirements

| Where | Requirement |
|---|---|
| All | Read access to `https://github.com/tylerwarner33/autodesk-agent-skills`. |
| claude.ai, the desktop app, and Cowork | A Pro, Max, Team, or Enterprise plan. For the `aps-docs` skill: code execution, with network egress to `developer.doc.autodesk.com` and `developer.doc.config.autodesk.com`. |
| Claude Code | Git. For the `aps-docs` skill: Python 3.9 or later on the PATH (as `python` or `python3`), and internet access. |
| OpenAI Codex | A Codex CLI with plugin marketplaces (`codex plugin marketplace`). For the `aps-docs` skill: the same as Claude Code. |
| Cursor | A Teams or Enterprise plan for a team marketplace, or Git for a local install. For the `aps-docs` skill: the same as Claude Code. |

## Install in claude.ai, the desktop app, and Cowork

1. Open **Customize > Plugins**.
2. Select **Add > Add marketplace**, then enter `tylerwarner33/autodesk-agent-skills`.
3. Select each plugin that you need, then select **Add**.
4. Turn on code execution and network egress for the `aps-docs` skill:
   1. Open **Settings > Capabilities**.
   2. Turn on **Code execution and file creation**.
   3. Turn on network egress, and add `developer.doc.autodesk.com` and `developer.doc.config.autodesk.com` to the allowed domains (or allow all domains).
   4. Start a new chat. A setting does not change a chat that is open.
5. Type `/` in the message box, then type the plugin name (ex. `aps-documentation`). Check that its skills are in the list (ex. `aps-docs`).

On a Team or Enterprise plan, an Owner can limit the marketplaces you can add and the network egress settings. If an option is not available, ask an Owner.
The plugins sync to Claude Code when Claude Code is signed in to the same account. Then you do not need the Claude Code install below.

## Install in Claude Code

1. Add the marketplace.

   ```
   claude plugin marketplace add tylerwarner33/autodesk-agent-skills
   ```

2. Install each plugin that you need.

   ```
   claude plugin install <plugin>@tylerwarner-autodesk
   ```

   Ex. `claude plugin install inventor-api@tylerwarner-autodesk`. The plugins are `aps-documentation`, `inventor-api`, `inventor-ilogic`, and `inventor-data`.

3. Start a new Claude Code session. Type `/<plugin>:` (ex. `/inventor-api:`) and check that its skills are in the list.

## Install in OpenAI Codex

1. Add the marketplace. Codex reads `.agents/plugins/marketplace.json` from the repository.

   ```
   codex plugin marketplace add tylerwarner33/autodesk-agent-skills
   ```

2. Start `codex` and run `/plugins`. Open the `Autodesk Agent Skills` marketplace, and install each plugin that you need.
3. Start a new session. A skill loads when a request matches its description.

To update, run `codex plugin marketplace upgrade tylerwarner-autodesk`. To remove the marketplace, run `codex plugin marketplace remove tylerwarner-autodesk`.

## Install in Cursor

Cursor reads `.cursor-plugin/marketplace.json` from the repository, and `.cursor-plugin/plugin.json` from each plugin.

- **A team (Teams or Enterprise plan):** in the Cursor dashboard, open **Plugins & MCPs**. In **Team Marketplaces**, select **Add Marketplace**, then **Import from Repo**, and paste `https://github.com/tylerwarner33/autodesk-agent-skills`. Each person then installs the plugins from **Customize**, for a project or for the user.
- **One person:** clone the repository to `~/.cursor/plugins/local/autodesk-agent-skills`, then restart Cursor or run **Developer: Reload Window**. To update, run `git pull` in that folder and reload. On an Enterprise plan, an admin must turn on **Allow Local Plugin Imports**.

## Update

### claude.ai, the desktop app, and Cowork

Open **Customize > Plugins**, open the marketplace, and select **Check for updates**. To get updates without this step, turn on **Sync automatically**.

### Claude Code

Run each command in order.

1. Fetch the latest marketplace. This does not update the plugins.

   ```
   claude plugin marketplace update tylerwarner-autodesk
   ```

2. Install the new version of each plugin.

   ```
   claude plugin update <plugin>@tylerwarner-autodesk
   ```

3. In an open session, run `/reload-plugins`.

## Verify

- In claude.ai or the desktop app, open **Customize > Plugins > <plugin>**. The version must be the newest version in [CHANGELOG.md](../CHANGELOG.md).
- In Claude Code, run `claude plugin list`. The list must show `<plugin>@tylerwarner-autodesk` with the newest version in [CHANGELOG.md](../CHANGELOG.md).

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| The marketplace cannot be added in claude.ai | The repo is private, or your organization does not allow it. For a private repo, connect GitHub and give the Claude GitHub App access to the repo. Otherwise, ask an Owner. |
| The marketplace cannot be added in Claude Code | Git cannot read the repo. Check the repo access and your git credential. |
| The skill does not show in a Claude Code session | Run `/reload-plugins`, or start a new session. |
| `aps-docs` says `Cannot reach` in chat or Cowork | Network egress does not allow the Autodesk doc domains. Add them (see step 4 of the install), then start a new chat. |
| `aps-docs` fails with "command not found" in Claude Code | Install Python 3.9 or later, and add it to the PATH. |
| `aps-docs` asks for permission on each command in Claude Code | The `allowed-tools` pattern did not match the command. Approve it once for the session, or add `Bash(python *aps_docs.py*)` to your allow rules. |
| An update does not arrive | `version` in `plugin.json` did not change. Compare it with the newest version in `CHANGELOG.md`. |
| `Plugin "autodesk-skills" not cached` | The plugin `autodesk-skills` is now `aps-documentation` (version 3.0.0). Run `claude plugin marketplace update tylerwarner-autodesk`, then `claude plugin install aps-documentation@tylerwarner-autodesk` once. |

## Uninstall

In claude.ai or the desktop app, open **Customize > Plugins > <plugin>**, open its menu, and select **Remove**.

In Claude Code:

```
claude plugin uninstall <plugin>@tylerwarner-autodesk
claude plugin marketplace remove tylerwarner-autodesk
```
