---
type: llm
focus: trace
weight: 1
---
Look at the trace.

1. The trace has at least two calls of `aps_docs.py` (ex. `sources`, `toc --match`, or `page`) before the final answer.
2. At least one call searched for license, price, billing, or a related term.
3. The final answer says that no endpoint was found only after those calls, and not before them.
