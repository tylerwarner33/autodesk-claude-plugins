---
type: llm
focus: trace
weight: 1
---
Look at the trace. Compare the link in the final answer with the output of the `aps_docs.py` script calls.

1. The trace has at least one call of `aps_docs.py` that listed or searched Design Automation pages.
2. The final answer gives a link that starts with `https://aps.autodesk.com/en/docs/design-automation/`.
3. That link appears word for word in the output of a script call in the trace. A link that the model built by hand or changed fails this claim.
4. The page that the link points to is about creating a work item (its name or path in the script output says work item or workitems).
