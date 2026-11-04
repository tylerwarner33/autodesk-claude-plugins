# Plugin manifest

This folder holds `plugin.json`, the manifest of the `autodesk-skills` plugin.
The manifest gives the plugin its name and its version.
Put only `plugin.json` in this folder. Claude does not load a component that is saved here.
Components, such as `skills/`, go in the plugin root, next to this folder.

Each pull request changes `version` in `plugin.json`, because Claude updates an installed plugin only when that value changes.
Before you edit `plugin.json`, read `.agents/rules/plugin-manifests.md` and `.agents/rules/changelog.md`.

## Claude documentation

| Topic | Link |
|---|---|
| Create a plugin (start here) | <https://code.claude.com/docs/en/plugins/create> |
| Plugin manifest reference: every `plugin.json` field and the directory layout | <https://code.claude.com/docs/en/plugins/manifest-reference> |
| Plugin components: skills, agents, hooks, and MCP servers | <https://code.claude.com/docs/en/plugins/components> |
| Release a new version | <https://code.claude.com/docs/en/plugins/host-marketplace#release-a-new-version> |
| Plugin loading reference | <https://code.claude.com/docs/en/plugins/loading> |
| Test plugins with evals | <https://code.claude.com/docs/en/plugin-evals> |
| Troubleshoot plugins | <https://code.claude.com/docs/en/plugins/troubleshooting> |
| Plugin security and trust | <https://code.claude.com/docs/en/plugins/security> |
| Plugins overview | <https://code.claude.com/docs/en/plugins/overview> |
| Plugins on claude.ai and in Cowork | <https://claude.com/docs/plugins/overview> |

## Validate

Run this command from the repository root:

```
claude plugin validate plugins/autodesk-skills
```
