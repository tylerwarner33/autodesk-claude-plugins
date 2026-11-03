# Quality Spec: aps-docs

This file says what a good answer from the `aps-docs` skill is. The graders follow it.
Change this file first. Then change the matching grader. Then run a pilot.

## Purpose of the skill

A user asks a question about an Autodesk Platform Services (APS, formerly Forge) API.
The skill reads the live APS documentation with `scripts/aps_docs.py` and answers with real portal links.
Claude without the skill answers from memory and gives no verified links. The gap between the two is the uplift (Δ) that the suite measures.

## A good answer

- It gives the direct answer in the first one or two sentences. Detail, a table, or an example can follow.
- It names the specific facts that the question needs: the HTTP method and path, the scope, the token types, or the event names.
- It gives at least one `https://aps.autodesk.com/en/docs/...` portal link for a page that it used. The link comes word for word from the script output.
- It picks the right API. Ex. a file event in ACC is a Data Management event in the Webhooks API.
- It adds a short `curl` example only when the question asks how to call something.
- It is honest about gaps. If the docs do not cover the question, the answer says so and does not invent an endpoint.

## A bad answer

- A wrong or old endpoint, scope, token type, or event name that is stated with confidence. A fact that is checked against the live docs and does not match fails, even when the answer says it is from memory.
- A portal link that the model built by hand. Source-path links (`/reference/callback/`, `.html`) are a sign of this.
- The wrong API for the question.
- No link to the APS docs on a question about an APS API.
- An answer from memory when the script could have run (ex. because a `Bash` call was denied).
- Over-trigger: the skill fires on a question that is not about APS.

## Failure modes to guard, in order of how much a user notices

1. A wrong or missing portal link.
2. A wrong API on a question that uses more than one API.
3. A stale scope or token fact from memory.
4. Over-trigger on a near-miss topic.
5. A long answer that has no direct answer first.

## Cases

| Case | Shape | What it checks |
|---|---|---|
| `01-acc-file-webhooks` | Cross-API routing | ACC file events are Data Management events in the Webhooks API |
| `02-list-hubs-scope` | Scope lookup | The scope and the accepted token types match the live Get Hubs page |
| `03-translate-svf2` | How-to with a request | The Model Derivative job request, with a docs link |
| `04-design-automation-link` | Link request | The link is copied from the script output |
| `05-gap-license-price` | Honest gap | The answer says there is no such endpoint, after it searched the docs |
| `06-neg-generic-pkce` | Must not fire | Generic OAuth with no APS |
| `07-neg-autocad-array` | Must not fire | An Autodesk product question that is not APS |

## Limits of this suite

- The with-plugin arm reads live docs. A fact that a grader names (ex. `dm.version.added`, or the token types of Get Hubs) can go stale. The grader for case 02 names the date on which the page was read (2026-11-03).
- The grader `searched-docs-first` (case 05) cannot pass without the skill, because the script is part of the skill. It is a regression guard for the skill, not a measure of answer quality.
- The simple text checks (weight 0.5) pass in both arms on some cases. They do not change Δ. They are a fixed backup for the judge.
- The without-plugin arm has the same `WebFetch` grant as the with-plugin arm. In the pilots it did not use it.
