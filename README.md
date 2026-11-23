# Autodesk Agent Skills

![Claude Surfaces](https://img.shields.io/badge/Claude-Code%20%7C%20claude.ai%20%7C%20Cowork-blue.svg)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Ftylerwarner33%2Fautodesk-agent-skills%2Fmain%2Fplugins%2Faps-documentation%2F.claude-plugin%2Fplugin.json&query=%24.version&label=version&color=brightgreen)](CHANGELOG.md)

Agent skills for Autodesk development, in the [Agent Skills](https://agentskills.io) format, split into plugins by focus: Autodesk Platform Services (APS) documentation, the Inventor API, Inventor iLogic, and Inventor data management.
This repository is a Claude plugin marketplace (`tylerwarner-autodesk`). Add it once, then add only the plugins that you need.
The plugins work in Claude Code, in chat on claude.ai and in the Claude desktop app, and in Cowork.
The Inventor skills name only the Inventor API, so they work with any tool that drives Inventor: an add-in, a plugin, or an Inventor MCP server.
This is a personal project. It is not made, endorsed, or supported by Autodesk.
Design: [Claude-Plugin-Distribution.md](Docs/Claude-Plugin-Distribution.md).

## Quick Start

### claude.ai, the Claude desktop app, and Cowork

1. Open **Customize > Plugins**, then select **Add > Add marketplace**.
2. Enter `tylerwarner33/autodesk-agent-skills`.
3. Add the plugins that you need (see [Plugins](#plugins)).
4. For the `aps-docs` skill, turn on code execution and allow network egress to `developer.doc.autodesk.com` and `developer.doc.config.autodesk.com`.

A plugin that you add to your account also syncs to Claude Code when Claude Code is signed in to the same account.

### Claude Code

Run these commands in a terminal. Install only the plugins that you need.

```
claude plugin marketplace add tylerwarner33/autodesk-agent-skills
claude plugin install aps-documentation@tylerwarner-autodesk
claude plugin install inventor-api@tylerwarner-autodesk
claude plugin install inventor-ilogic@tylerwarner-autodesk
claude plugin install inventor-data@tylerwarner-autodesk
```

If you installed `autodesk-skills` before version 3.0.0, it is now `aps-documentation`. Run `claude plugin marketplace update tylerwarner-autodesk`, then `claude plugin install aps-documentation@tylerwarner-autodesk` once.

To get updates, run `claude plugin marketplace update tylerwarner-autodesk`, then `claude plugin update <plugin>@tylerwarner-autodesk`, then `/reload-plugins` in a session.
Full steps and troubleshooting: [Docs/Setup-Guide.md](Docs/Setup-Guide.md).

## What's Included

### Plugins

| Plugin | Focus |
|---|---|
| `aps-documentation` | Autodesk Platform Services (APS) answers from the live documentation |
| `inventor-api` | Inventor API facts for code that drives Inventor: COM interop traps, modeling, drawings |
| `inventor-ilogic` | How iLogic rules behave when code changes a document |
| `inventor-data` | Inventor projects, Vault read-only files, saved versions, model states, copies |

### Skills

Claude loads a skill by itself when a request matches it. To start one by name, type `/<plugin>:<skill>` (ex. `/inventor-api:inventor-modeling`). In chat, type `/` and select the skill.

| Skill | Plugin | Description |
|---|---|---|
| [`aps-docs`](Docs/Skill-Catalog.md#aps-docs) | `aps-documentation` | Answer APS (Forge) questions from the live documentation: find the right API, read its pages, and give portal links. Covers Data Management, Model Derivative, Viewer, Authentication, Webhooks, ACC, BIM 360, Design Automation, and the other APS APIs. Needs Python 3.9 or later |
| [`inventor-api-traps`](Docs/Skill-Catalog.md#inventor-api-traps) | `inventor-api` | The Inventor COM API facts that make .NET code fail: members typed as `object`, casts, members called as methods, and the causes of E_FAIL and E_INVALIDARG |
| [`inventor-modeling`](Docs/Skill-Catalog.md#inventor-modeling) | `inventor-api` | Named faces and the ViewCube, centimetres and radians, sketch-relative extent direction, and how to verify a geometry write |
| [`inventor-drawings`](Docs/Skill-Catalog.md#inventor-drawings) | `inventor-api` | Sheets, views, balloons and leaders, styles and templates, and images of a sheet |
| [`inventor-ilogic`](Docs/Skill-Catalog.md#inventor-ilogic) | `inventor-ilogic` | Parameter triggers and their cost, rules off for a batch, rule text, error dialogs, and the Security Alert |
| [`inventor-projects-and-files`](Docs/Skill-Catalog.md#inventor-projects-and-files) | `inventor-data` | Projects and library paths, Vault read-only files, saved versions, model states, Content Center, copies, and which documents to close |

## Repo Structure

```
AGENTS.md                -> instructions for any coding agent that works on this repo
.agents/rules/           -> on-demand rules listed in AGENTS.md
.claude-plugin/          -> the marketplace manifest, and a README with Claude docs links
.github/                 -> CODEOWNERS (the required reviewer) and the PR validation workflow
Docs/                    -> full documentation set
evals/                   -> eval suites that measure what each skill adds (see evals/README.md)
Pipelines/Scripts/       -> the checks that the PR validation workflow runs
plugins/<plugin>/        -> one plugin: its manifest and skills. Only the plugin folder installs.
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
| [CHANGELOG.md](CHANGELOG.md) | What changed in each version of the plugins, newest first |
| [CONTRIBUTING.md](CONTRIBUTING.md) | The pull request process, and how to add a changelog entry and the next version |

## License

[MIT](LICENSE)
