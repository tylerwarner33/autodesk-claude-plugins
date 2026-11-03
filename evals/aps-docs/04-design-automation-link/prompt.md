---
max_turns: 20
timeout_seconds: 300
allowed_tools: [Skill, "Bash(python *aps_docs.py*)", "Bash(python3 *aps_docs.py*)"]
model: sonnet
runs: 3
plugins: ["../../../plugins/autodesk-skills"]
---
Give me the APS docs link for creating a work item in Design Automation.
