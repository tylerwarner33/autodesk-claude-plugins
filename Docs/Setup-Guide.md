# Setup Guide

How to install, update, verify, and remove the `autodesk-skills` plugin.

## Requirements

- Claude Code.
- Git, with access to `https://github.com/tylerwarner33/claude-plugin`.
- For the `aps-docs` skill: Python 3.9 or later on the PATH (as `python` or `python3`), and internet access.

## Install

1. Add the marketplace.

   ```
   claude plugin marketplace add tylerwarner33/claude-plugin
   ```

2. Install the plugin.

   ```
   claude plugin install autodesk-skills@tylerwarner-plugins
   ```

3. Start a new Claude Code session. Type `/autodesk-skills:` and check that `aps-docs` is in the list.

## Update

Run each command in order.

1. Fetch the latest marketplace. This does not update the plugin.

   ```
   claude plugin marketplace update tylerwarner-plugins
   ```

2. Install the new version of the plugin.

   ```
   claude plugin update autodesk-skills@tylerwarner-plugins
   ```

3. In an open session, run `/reload-plugins`.

## Verify

```
claude plugin list
```

The list must show `autodesk-skills@tylerwarner-plugins` with the version from [CHANGELOG.md](../CHANGELOG.md).

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| The marketplace cannot be added | Git cannot read the repo. Check the repo access and your git credential. |
| The skill does not show in a session | Run `/reload-plugins`, or start a new session. |
| `aps-docs` fails with "command not found" | Install Python 3.9 or later, and add it to the PATH. |
| `aps-docs` asks for permission on each command | The `allowed-tools` pattern did not match the command. Approve it once for the session, or add `Bash(python *aps_docs.py*)` to your allow rules. |
| An update does not arrive | `version` in `plugin.json` did not change. Compare it with the newest version in `CHANGELOG.md`. |

## Uninstall

```
claude plugin uninstall autodesk-skills@tylerwarner-plugins
claude plugin marketplace remove tylerwarner-plugins
```
