---
type: llm
focus: trace
weight: 1
---
Look at the trace. Compare the links in the final answer with the output of the `aps_docs.py` script calls.

1. The trace has at least one call of `aps_docs.py`.
2. Every link in the final answer that starts with `https://aps.autodesk.com` appears word for word in the output of a script call in the trace. A link that the model built by hand, or that it changed, fails this claim.
3. The answer has at least one such link.
