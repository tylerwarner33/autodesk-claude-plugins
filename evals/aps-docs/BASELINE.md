# Baseline: aps-docs

The last measured uplift (Δ) of the `aps-docs` skill. Compare each new run with this file.
Δ = the score with the plugin, minus the score without it. A case that must not fire shows Δ 0 when the result is correct.

## Current baseline

This baseline comes from the first full run: 3 runs for each case and each arm, 42 runs in all.

| Field | Value |
|---|---|
| Plugin version | 2.1.1 |
| Date | 2026-11-03 |
| Claude Code version | 2.1.317 |
| Runs per case | 3 |
| Agent model | sonnet |
| Judge model | opus |
| Grants | `Bash(python *aps_docs.py*)`, `Bash(python3 *aps_docs.py*)`, `WebFetch(domain:developer.doc.autodesk.com)`, `WebFetch(domain:developer.doc.config.autodesk.com)` |
| Run errors | None (42 of 42 runs have an empty `error` field) |
| Duration | 950 seconds |
| Cost | $7.23 for the agent runs, $4.62 for the judge |

| Case | With plugin | Without plugin | Δ | Note |
|---|---|---|---|---|
| 01-acc-file-webhooks | 1.00 | 0.43 | +0.57 | |
| 02-list-hubs-scope | 0.78 | 0.33 | +0.44 | 1 of 3 with-plugin runs scored 0.33. See "Open finding". |
| 03-translate-svf2 | 1.00 | 0.78 | +0.22 | The `answer-quality` grader failed in 2 of 3 runs without the plugin. |
| 04-design-automation-link | 1.00 | 0.67 | +0.33 | The Δ comes only from the `link-copied-from-script` grader, which cannot pass without the skill. |
| 05-gap-license-price | 1.00 | 0.60 | +0.40 | The Δ comes only from the `searched-docs-first` grader, which cannot pass without the skill. The `honest-gap` grader passed in both arms. |
| 06-neg-generic-pkce | 1.00 | 1.00 | 0.00 | Must not fire. Correct. |
| 07-neg-autocad-array | 1.00 | 1.00 | 0.00 | Must not fire. Correct. |
| **Mean** | **0.97** | **0.69** | **+0.28** | |

### Open finding

Run 3 of 3 with the plugin for `02-list-hubs-scope` failed the `answer-quality` and `matches-docs-in-trace` graders (all 3 judge votes). The answer first said that the endpoint needs a three-legged token, and then listed the two-legged token as valid. The other 2 runs passed.
One run in 3 is not enough to say that the skill regressed. Run the case again before you act on it.

## How to read it

- A drop in Δ for a case, from one plugin version to the next, shows a regression.
- A change smaller than the noise of the run count is not a result. With 3 runs per case, do not act on a difference of one run.
- Do not compare numbers from runs with a different judge model, different grants, or different runs per case.
- The `searched-docs-first` and link-from-script graders pass only with the skill. They guard against a regression. They do not measure answer quality.

## History

One row for each full run. Add a new row on top. Git keeps the older version of this file.

| Plugin version | Date | Runs per case | Mean Δ | Agent cost | Note |
|---|---|---|---|---|---|
| 2.1.1 | 2026-11-03 | 3 | +0.28 | $7.23 | First full run. One with-plugin run of case 02 failed. |
| 2.0.2 | 2026-11-03 | 1 | +0.33 | $2.45 | Pilot. |

## How to update

1. Run the suite with the command in [`../README.md`](../README.md), with `runs: 3` or more.
2. Read the `error` field of each run first. Do not use a report that has a run error.
3. Replace the "Current baseline" tables with the new numbers.
4. Add one row to "History".
5. Do not commit the report, the traces, or any local path.
