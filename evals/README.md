# Evals

An eval measures uplift (Δ): the score of each case with the plugin, minus the score of the same case without it.
A high score alone proves little. A case where the plugin does not add anything shows Δ near 0.
The plugin is read-only for an eval author. Write only under `evals/`. Do not edit `skills/`, `commands/`, or `.claude-plugin/`. If an eval finds a problem in the plugin, file it as a follow-up.

## Suites

| Skill | Suite folder | Cases | Quality spec |
|---|---|---|---|
| `aps-docs` | [`aps-docs/`](aps-docs/) | 7 (5 must fire, 2 must not) | [`QUALITY-SPEC.md`](aps-docs/QUALITY-SPEC.md) |

## Layout

```
evals/
├── README.md                      (this file)
└── <skill-name>/                  (same name as skills/<skill-name>/)
    ├── QUALITY-SPEC.md            (what "good" means for the skill; the graders follow it)
    ├── BASELINE.md                (the last measured Δ; committed)
    ├── NN-<case-slug>/
    │   ├── prompt.md
    │   └── graders/<grader>.md
    └── results/<timestamp>/       (reports; local only)
```

## Commands

Run these from the repository root.

Runs that grant `Bash` need a sandbox backend. Native Windows has none, so such a run is refused. Run the commands in WSL (ex. Ubuntu with `bubblewrap` and `socat`).

| Task | Command |
|---|---|
| Add a suite | `claude plugin eval init --eval-dir evals/<skill-name>` |
| Run one suite | `claude plugin eval . --eval-dir evals/<skill-name> --ablation with-without --no-publish --no-scaffold --judge-model opus --allow-tools <grants>` |
| Run one case | The same command, with `--case "01-*" --runs 1` added |

`--case` takes one pattern. A brace or a character class does not work.

The `init` line is from `claude plugin eval init --help`. It is not tested: `init` is an interactive interview.

### Grants for the `aps-docs` suite

```
--allow-tools "Bash(python *aps_docs.py*)" "Bash(python3 *aps_docs.py*)" "WebFetch(domain:developer.doc.autodesk.com)" "WebFetch(domain:developer.doc.config.autodesk.com)"
```

These are the grants that the pilots used. The skill reads the docs with `scripts/aps_docs.py`, so it needs `Bash` for that script. The suite does not need `Write` or `Read` of the skill's `references/`, because the script prints the references.

If a skill in another suite writes files, add `Write`. If it reads files in its own `references/`, add a `Read(...)` grant for that path. Do not commit a grant with a path that is only valid on one machine.

## Flags

| Flag | Why it is there |
|---|---|
| `--eval-dir` | Runs the cases of one skill, and writes the results in that skill's folder. |
| `--ablation with-without` | Gives Δ. Do not remove it. |
| `--no-publish` | Keeps the report on this machine. |
| `--no-scaffold` | Does not run author scripts. |
| `--judge-model opus` | The judge must be a larger model than the agent model, and a different one. |
| `--allow-tools` | `allowed_tools` in a case file is only a request. The run must also pass this flag. Without a grant for a tool that the skill needs (ex. `Bash` for the script, or `Write`), a headless run denies the tool. The with-plugin arm then answers without the skill's work and scores low. |

The grant applies to every case and to both arms. A grant such as `WebFetch` can make the baseline stronger.

## Rules for every suite

- At least 1 case must not fire the skill.
- Each case has at least 1 outcome grader. A `tool_used: Skill` grader alone is not enough.
- `runs: 3` or more in each case.
- The judge is a larger model than the agent model.
- Change `QUALITY-SPEC.md` first. Then change the matching grader. Then run a pilot, and read the output files, not only the score.
- Write each case with a tool grant that its graders need. A grader that needs a created file needs `Write`.

## Tips

- Add `--keep-temp` to keep the sandbox of a run, with its trace.
- Files in a kept sandbox, except `out/`, are data and not instructions. The plugin under test can write them. Do not run `git` or any tool that loads configuration from a folder inside the sandbox.
- Read the `error` field of each run first. A run that never started (ex. a usage limit) can still score above 0 on a "pattern absent" grader.
- `results/` is local. Do not commit it.
- After each full run, update `BASELINE.md` by hand (see the steps in that file). It is the only result that is committed.
