# claude-plugin

Claude Code skills for Autodesk Platform Services (APS) development.
This repository is a Claude Code plugin marketplace (`tylerwarner-plugins`) with one plugin (`autodesk-skills`), both at the repository root.
This is a personal project. It is not made, endorsed, or supported by Autodesk.
Design: [Claude-Plugin-Distribution.md](Docs/Claude-Plugin-Distribution.md).

## Quick Start

Run these commands in a terminal.

```
claude plugin marketplace add tylerwarner33/claude-plugin
claude plugin install autodesk-skills@tylerwarner-plugins
```

To get updates, run `claude plugin marketplace update tylerwarner-plugins`, then `claude plugin update autodesk-skills@tylerwarner-plugins`, then `/reload-plugins` in a session.
Full steps and troubleshooting: [Docs/Setup-Guide.md](Docs/Setup-Guide.md).

## What's Included

### Skills

Claude loads a skill by itself when a request matches it. To start one by name, type `/autodesk-skills:<skill>`.

| Skill | Description |
|---|---|
| [`aps-docs`](Docs/Skill-Catalog.md#aps-docs) | Answer APS (Forge) questions from the live documentation: find the right API, read its pages, and give portal links. Covers Data Management, Model Derivative, Viewer, Authentication, Webhooks, ACC, BIM 360, Design Automation, and the other APS APIs. Needs Python 3.9 or later |

## Repo Structure

```
AGENTS.md                -> instructions for any coding agent that works on this repo
.agents/rules/           -> on-demand rules listed in AGENTS.md
.claude-plugin/          -> the marketplace and plugin manifests
Docs/                    -> full documentation set
skills/                  -> agent skills (one folder per skill)
```

## Documentation

| Document | Contents |
|---|---|
| [Skill-Catalog.md](Docs/Skill-Catalog.md) | Per-skill documentation and source links |
| [Setup-Guide.md](Docs/Setup-Guide.md) | Install, update, verify, troubleshoot, uninstall |
| [Claude-Plugin-Distribution.md](Docs/Claude-Plugin-Distribution.md) | The plugin marketplace design, updates, and testing a branch |
| [Contributing-Skills.md](Docs/Contributing-Skills.md) | How to author, test, and submit a skill |
| [Security-And-Governance.md](Docs/Security-And-Governance.md) | Risk tiers, repository controls, and incident response |
| [Agent-Instructions.md](Docs/Agent-Instructions.md) | The standard for `AGENTS.md` and on-demand rules, across AI clients |
| [CHANGELOG.md](CHANGELOG.md) | What changed in each plugin version, newest first |
| [CONTRIBUTING.md](CONTRIBUTING.md) | The pull request process, and how to add a changelog entry and the next version |

## License

[MIT](LICENSE)
