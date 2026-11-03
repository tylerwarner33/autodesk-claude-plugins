---
type: llm
focus: last_message
weight: 1
---
Grade the final answer against these claims. Every claim must be true.

1. The answer gives the HTTP method and the path of the call that lists hubs.
2. The answer names the scope `data:read`. The docs page lists it as the required scope.
3. The answer states which token types the call accepts, and it does not contradict the docs. The Get Hubs page (read on 2026-11-03) says the call accepts a two-legged token, a three-legged token, or a Secure Service Account (SSA) token, and that user context is optional. The claim FAILS if the answer says a two-legged token is not accepted or not enough, or says that only a three-legged token works. The claim also fails if the answer leaves the token type out.
4. The answer gives at least one link that starts with `https://aps.autodesk.com/en/docs/`.
5. The direct answer (scope and token type) comes first, in the first three sentences, before any detail or example.
