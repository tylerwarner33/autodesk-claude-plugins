# Evals

An eval measures uplift (Δ): the score of each case with the plugin, minus the score of the same case without it.
A high score alone proves little. A case where the plugin does not add anything shows Δ near 0.
The plugin is read-only for an eval author. Write only under `evals/`. Do not edit `plugins/` or `.claude-plugin/`. If an eval finds a problem in the plugin, file it as a follow-up.
The `evals/` folder is outside the plugin folder, so it does not install with the plugin.
For the full `claude plugin eval` reference, see <https://code.claude.com/docs/en/plugin-evals>.

## Suites

| Skill | Suite folder | Cases | Quality spec |
|---|---|---|---|
| `aps-docs` | [`aps-docs/`](aps-docs/) | 7 (5 must fire, 2 must not) | [`QUALITY-SPEC.md`](aps-docs/QUALITY-SPEC.md) |

## Layout

```
evals/
├── README.md                      (this file)
└── <skill-name>/                  (same name as plugins/autodesk-skills/skills/<skill-name>/)
    ├── QUALITY-SPEC.md            (what "good" means for the skill; the graders follow it)
    ├── BASELINE.md                (the last measured Δ; committed)
    ├── NN-<case-slug>/
    │   ├── prompt.md
    │   └── graders/<grader>.md
    └── results/<timestamp>/       (reports; local only)
```

## Commands

Run these from the repository root.

Runs that grant `Bash` need a sandbox backend. Native Windows has none, so such a run is refused. On Windows, run the commands in WSL2: see [Run on Windows (WSL2)](#run-on-windows-wsl2). On Linux or macOS, run them in a terminal.

| Task | Command |
|---|---|
| Add a suite | `claude plugin eval init --eval-dir evals/<skill-name>` |
| Run one suite | `claude plugin eval . --eval-dir evals/<skill-name> --ablation with-without --no-publish --no-scaffold --judge-model opus --allow-tools <grants>` |
| Run one case | The same command, with `--case "01-*" --runs 1` added |

The target is the repository root (`.`), not `plugins/autodesk-skills`. `--eval-dir` accepts only a folder inside the target, and `evals/` is outside the plugin. Each case names the plugin under test in its `prompt.md`:

```yaml
plugins: ["../../../plugins/autodesk-skills"]
```

The path is relative to the case folder. Add this line to each new case. Without it, no plugin loads for the case.

`--case` takes one pattern. A brace or a character class does not work.

The `init` line is from `claude plugin eval init --help`. It is not tested: `init` is an interactive interview.

### Run on Windows (WSL2)

Do not run an eval from native Windows. Any run that grants `Bash` is refused there. Use a Linux distribution in WSL2. These steps were tested with Ubuntu 22.04.

**One-time setup**

1. Install the distribution. In PowerShell: `wsl --install -d Ubuntu-22.04`. Then open it once and create the Linux user.
2. In the distribution, install the sandbox tools: `sudo apt update && sudo apt install -y bubblewrap socat`.
3. In the distribution, install Claude Code as the Claude Code setup guide says. The `claude` binary is then at `~/.local/bin/claude`.
4. Start `~/.local/bin/claude` once and log in with the same account that you use on Windows. Trust the repository folder when it asks.
5. Use the repository on the Windows drive. In WSL its path is `/mnt/c/<path to the repository>`. You do not need a second clone.

**Run a suite**

1. Write the command in a script file on the Windows drive, outside the repository (ex. in your temp folder). Start the script with `cd /mnt/c/<path to the repository>`, then the `claude plugin eval` command from the [Commands](#commands) table. Call `~/.local/bin/claude` by its full path.
2. Start the script from PowerShell: `wsl -d Ubuntu-22.04 -- bash /mnt/c/<path to the script>`.

Rules for the script:

- Do not put the `claude` command directly on the `wsl` command line. The quoted `--allow-tools` patterns can be parsed again, and the run fails.
- Do not start the script from Git Bash. It rewrites a path that starts with `/mnt/c`, and the command ends with exit code 127. Use PowerShell.
- A full run takes several minutes. In an agent session, start it as a background task.

**Problems**

| Symptom | Fix |
|---|---|
| The run is refused because no sandbox backend is available | You started it from native Windows. Start it in WSL. |
| `bwrap` or `socat` is not found | Install them: `sudo apt install -y bubblewrap socat`. |
| Runs that grant `Bash` are blocked, and `~/.docker/contexts` is a symbolic link | Replace the link with a real folder. |
| A run ends with `error` and score 0, and every case is the same | Look at the `error` field. A usage limit ("5-hour limit") ends a run before grading. Wait for the reset, delete that report folder, and run again. |
| `Exit code 1` and `Read-only file system` in the shell wrapper, with the full output of the script | Not a failure of the script. Ignore it. |

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
- Each case has the `plugins` line that names the plugin under test.
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
