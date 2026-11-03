---
max_turns: 20
timeout_seconds: 300
allowed_tools: [Skill, "Bash(python *aps_docs.py*)", "Bash(python3 *aps_docs.py*)"]
model: sonnet
runs: 3
plugins: ["../../../plugins/autodesk-skills"]
---
What webhook events fire when a file changes in ACC?
