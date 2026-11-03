---
type: llm
focus: trace
weight: 1
---
Look at the trace. Compare the final answer with the page text that `aps_docs.py` printed.

1. The trace has at least one call of `aps_docs.py` that read a page about listing hubs.
2. Each scope that the final answer names appears in the page text in the trace.
3. The token type that the final answer states (2-legged, 3-legged, or both) agrees with the page text in the trace. If the page text does not say which token type to use, the answer must say that it is not stated.
