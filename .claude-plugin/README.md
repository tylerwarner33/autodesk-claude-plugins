# Marketplace manifest

This folder holds `marketplace.json`, the manifest of the `tylerwarner-autodesk` marketplace.
A marketplace is a catalog. It lists plugins and tells Claude where to fetch each one.
The plugin that this marketplace lists is in `plugins/autodesk-skills/`.

Before you edit `marketplace.json`, read `.agents/rules/plugin-manifests.md`.

## Claude documentation

| Topic | Link |
|---|---|
| Create a marketplace (start here) | <https://code.claude.com/docs/en/plugins/create-marketplace> |
| Marketplace reference: fields, plugin sources, and validation messages | <https://code.claude.com/docs/en/plugins/marketplace-reference> |
| Host and maintain a marketplace: updates, versions, and renames | <https://code.claude.com/docs/en/plugins/host-marketplace> |
| Publish and distribute a plugin | <https://code.claude.com/docs/en/plugins/publish> |
| Install and manage plugins | <https://code.claude.com/docs/en/plugins/install> |
| Manage plugins for an organization | <https://code.claude.com/docs/en/plugins/org> |
| Plugin security and trust | <https://code.claude.com/docs/en/plugins/security> |
| Plugins overview | <https://code.claude.com/docs/en/plugins/overview> |

## Validate

Run this command from the repository root:

```
claude plugin validate .
```
