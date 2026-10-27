# Setup Guide

How to install, update, verify, and remove the `autodesk-skills` plugin.
The plugin works in Claude Code, in chat on claude.ai and in the Claude desktop app, and in Cowork.

## Requirements

| Where | Requirement |
|---|---|
| All | Read access to `https://github.com/tylerwarner33/autodesk-claude-plugins`. |
| claude.ai, the desktop app, and Cowork | A Pro, Max, Team, or Enterprise plan. For the `aps-docs` skill: code execution, with network egress to `developer.doc.autodesk.com` and `developer.doc.config.autodesk.com`. |
| Claude Code | Git. For the `aps-docs` skill: Python 3.9 or later on the PATH (as `python` or `python3`), and internet access. |

## Install in claude.ai, the desktop app, and Cowork

1. Open **Customize > Plugins**.
2. Select **Add > Add marketplace**, then enter `tylerwarner33/autodesk-claude-plugins`.
3. Select the `autodesk-skills` plugin, then select **Add**.
4. Turn on code execution and network egress for the `aps-docs` skill:
   1. Open **Settings > Capabilities**.
   2. Turn on **Code execution and file creation**.
   3. Turn on network egress, and add `developer.doc.autodesk.com` and `developer.doc.config.autodesk.com` to the allowed domains (or allow all domains).
   4. Start a new chat. A setting does not change a chat that is open.
5. Type `/` in the message box, then type `autodesk-skills`. Check that `aps-docs` is in the list.

On a Team or Enterprise plan, an Owner can limit the marketplaces you can add and the network egress settings. If an option is not available, ask an Owner.
The plugin syncs to Claude Code when Claude Code is signed in to the same account. Then you do not need the Claude Code install below.

## Install in Claude Code

1. Add the marketplace.

   ```
   claude plugin marketplace add tylerwarner33/autodesk-claude-plugins
   ```

2. Install the plugin.

   ```
   claude plugin install autodesk-skills@tylerwarner-autodesk
   ```

3. Start a new Claude Code session. Type `/autodesk-skills:` and check that `aps-docs` is in the list.

## Update

### claude.ai, the desktop app, and Cowork

Open **Customize > Plugins**, open the marketplace, and select **Check for updates**. To get updates without this step, turn on **Sync automatically**.

### Claude Code

Run each command in order.

1. Fetch the latest marketplace. This does not update the plugin.

   ```
   claude plugin marketplace update tylerwarner-autodesk
   ```

2. Install the new version of the plugin.

   ```
   claude plugin update autodesk-skills@tylerwarner-autodesk
   ```

3. In an open session, run `/reload-plugins`.

## Verify

- In claude.ai or the desktop app, open **Customize > Plugins > autodesk-skills**. The version must be the newest version in [CHANGELOG.md](../CHANGELOG.md).
- In Claude Code, run `claude plugin list`. The list must show `autodesk-skills@tylerwarner-autodesk` with the newest version in [CHANGELOG.md](../CHANGELOG.md).

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

## Uninstall

In claude.ai or the desktop app, open **Customize > Plugins > autodesk-skills**, open its menu, and select **Remove**.

In Claude Code:

```
claude plugin uninstall autodesk-skills@tylerwarner-autodesk
claude plugin marketplace remove tylerwarner-autodesk
```
