# Security and Governance

This repo distributes content that shapes what an AI agent does on each machine that installs it.
It is a small supply chain, and it is governed like one.

## Threat model

| Threat | Vector | Mitigation |
|---|---|---|
| Malicious or careless skill content (prompt injection) | A skill instructs Claude to exfiltrate data, run destructive commands, or weaken review habits | PR-only changes to `main`, small diffs, skills treated as code |
| Malicious or careless hook or MCP server | A hook or MCP server runs a command on each machine, without a prompt | Tier 2 review. The plugin has no hook or MCP server now. |
| Careless bundled script | A script in a skill runs on each machine when Claude follows the skill | Tier 2 review and tests. The `aps-docs` script uses only the Python standard library, reads only public Autodesk doc URLs, and writes only its TOC cache in the system temp folder. |
| Credential leakage | Tokens committed to skills or docs | The no-secrets policy (below) |
| Compromised account | Direct push of malicious content | Branch protection on `main` (below) |

## Content risk tiers

| Tier | Content | Risk | Review bar |
|---|---|---|---|
| 1 | Skills (`skills/**/SKILL.md`, references) | Influences Claude's behavior; no direct execution | Read the full diff |
| 2 | The plugin manifests, hooks, an MCP server, and scripts or assets bundled in a skill (`skills/*/scripts/**`, `skills/*/assets/**`) | Arbitrary command execution on the machine. Hooks and an MCP server run with the user's rights, outside the sandbox, without a prompt. | Read the full diff, run the tests, say "tier 2" in the PR description |

A skill with a `scripts/` folder is tier 2 as a whole, because its `SKILL.md` tells Claude to run those scripts.
A binary asset (ex. a `.docx` template) cannot be reviewed in a diff, so the skill must also contain the script that builds it, and a PR must change both together.

## Repository controls (GitHub)

Set these on the `main` branch (Settings > Branches, or a ruleset):

- Require a pull request before merge.
- Block force pushes and branch deletion.
- Allow squash merge only.

## No-secrets policy

- Never commit tokens, API keys, connection strings, or client secrets - in skills, configs, scripts, or docs.
- A skill that shows API usage must read credentials from the environment, not from a file in the repo.
- If a secret lands in history: rotate it immediately, then scrub history. Rotation is the fix; scrubbing is cleanup.

## Incident response

If bad content ships to `main`:

1. Revert the commit on `main` (`git revert`), and bump the version so that installed copies update.
2. Run `claude plugin update autodesk-skills@tylerwarner-plugins` on each machine that installed it, and restart Claude Code. To stop the plugin until the revert is in, run `claude plugin disable autodesk-skills@tylerwarner-plugins`.
3. If the content was tier 2, review recent transcripts for unexpected behavior.
4. Find how it passed review, and tighten the control.
