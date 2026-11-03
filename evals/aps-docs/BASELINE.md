# Baseline: aps-docs

The last measured uplift (Δ) of the `aps-docs` skill. Compare each new run with this file.
Δ = the score with the plugin, minus the score without it. A case that must not fire shows Δ 0 when the result is correct.

## Current baseline

This baseline comes from a pilot with 1 run for each case. The suite rule is `runs: 3` or more, so the numbers are noisy. Replace this file after the first full run.

| Field | Value |
|---|---|
| Plugin version | 2.0.2 |
| Date | 2026-11-03 |
| Claude Code version | 2.1.317 |
| Runs per case | 1 (pilot) |
| Agent model | sonnet |
| Judge model | opus |
| Grants | `Bash(python *aps_docs.py*)`, `Bash(python3 *aps_docs.py*)`, `WebFetch(domain:developer.doc.autodesk.com)`, `WebFetch(domain:developer.doc.config.autodesk.com)` |
| Run errors | None |
| Duration | 358 seconds |
| Cost | $2.45 for the agent runs, about $1.58 for the judge |

| Case | With plugin | Without plugin | Δ | Note |
|---|---|---|---|---|
| 01-acc-file-webhooks | 1.00 | 0.43 | +0.57 | |
| 02-list-hubs-scope | 1.00 | 0.33 | +0.67 | |
| 03-translate-svf2 | 1.00 | 0.67 | +0.33 | |
| 04-design-automation-link | 1.00 | 0.67 | +0.33 | |
| 05-gap-license-price | 1.00 | 0.60 | +0.40 | The Δ comes only from the `searched-docs-first` grader, which cannot pass without the skill. The `honest-gap` grader passed in both arms. |
| 06-neg-generic-pkce | 1.00 | 1.00 | 0.00 | Must not fire. Correct. |
| 07-neg-autocad-array | 1.00 | 1.00 | 0.00 | Must not fire. Correct. |
| **Mean** | **1.00** | **0.67** | **+0.33** | |

## How to read it

- A drop in Δ for a case, from one plugin version to the next, shows a regression.
- A change smaller than the noise of the run count is not a result. With 1 run per case, do not act on a difference of one grader.
- Do not compare numbers from runs with a different judge model, different grants, or different runs per case.
- The `searched-docs-first` and link-from-script graders pass only with the skill. They guard against a regression. They do not measure answer quality.

## History

One row for each full run. Add a new row on top. Git keeps the older version of this file.

| Plugin version | Date | Runs per case | Mean Δ | Agent cost | Note |
|---|---|---|---|---|---|
| 2.0.2 | 2026-11-03 | 1 | +0.33 | $2.45 | Pilot. No full run yet. |

## How to update

1. Run the suite with the command in [`../README.md`](../README.md), with `runs: 3` or more.
2. Read the `error` field of each run first. Do not use a report that has a run error.
3. Replace the "Current baseline" tables with the new numbers.
4. Add one row to "History".
5. Do not commit the report, the traces, or any local path.
