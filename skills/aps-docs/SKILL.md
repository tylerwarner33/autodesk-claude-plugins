---
name: aps-docs
description: >-
  Answer questions about Autodesk Platform Services (APS, formerly Forge) from the
  live APS documentation: find the right API, read its table of contents and pages,
  and give portal links. Covers Data Management, Model Derivative, Viewer,
  Authentication (OAuth, PKCE, SSA), Webhooks, ACC, BIM 360, Design Automation,
  AEC Data Model, Manufacturing Data Model, Vault Data, and the other APS APIs.
  Use for every question about an APS or Forge API, even when you think you know
  the answer, because APS endpoints, scopes, and doc links change often. Ex. which
  API or endpoint to call (list hubs, projects, folders, or files; upload; translate
  a model), which scope or token type it needs, which webhook event fires, what an
  APS term means, or a link to the APS docs.
compatibility: >-
  Needs Python 3.9 or later and internet access to developer.doc.autodesk.com and
  developer.doc.config.autodesk.com. No other packages.
allowed-tools: >-
  Bash(python *aps_docs.py*)
  Bash(python3 *aps_docs.py*)
metadata:
  version: "1.0.0"
  owner: "tylerwarner33"
  origin: "https://github.com/autodesk-platform-services/skills (skills/aps-docs-portal)"
---

Answer APS questions from the live documentation, not from memory. APS changes often: endpoints, scopes, event names, and doc paths move.

`${CLAUDE_SKILL_DIR}` is the folder that holds this `SKILL.md`. Run the script as:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/aps_docs.py" <command> ...
```

If `python` is not found, use `python3`.

Read the reference files only through the script (`sources`, `glossary`, `example`). Do not open the files in `references/` with the Read tool or a shell command: the skill folder can be outside the working folder, and a direct read can stop for approval.

## Where the docs are

The APS portal (`aps.autodesk.com`) is a JavaScript app. Do not fetch it: it returns no content to scripts.
The script reads the static sources of the same content:

| Source | What it has |
|---|---|
| The TOC JSON of an API | The tree of pages. Each page has a name, a source path, and a portal path. |
| The static HTML of a page | The page content. |

## Method

### 1. Choose the API

Find the source ID with the `sources` command. It prints the source table and a second table that maps common questions to APIs:

```bash
# The rows that match a regex (case-insensitive)
python "${CLAUDE_SKILL_DIR}/scripts/aps_docs.py" sources --match "auth|token"

# The full list
python "${CLAUDE_SKILL_DIR}/scripts/aps_docs.py" sources
```

If a term in the question is not clear, look it up:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/aps_docs.py" glossary --match "aecdm|ssa"
```
A question can need more than one API (ex. a file event in ACC is a Data Management event in `webhooks_v1`).

### 2. Find the pages

```bash
# Top-level sections
python "${CLAUDE_SKILL_DIR}/scripts/aps_docs.py" toc model-derivative_v2

# The pages of one section (use a url_path from the result above)
python "${CLAUDE_SKILL_DIR}/scripts/aps_docs.py" toc model-derivative_v2 --section developers_guide

# All pages whose name or path match a regex (case-insensitive)
python "${CLAUDE_SKILL_DIR}/scripts/aps_docs.py" toc model-derivative_v2 --match "manifest|formats"
```

Each page in the result has a `source` path (to read it) and a `portal` link (to give the user).
Prefer `--match` with a few words from the question. Use `--section` to browse when the words do not match.

### 3. Read the pages

```bash
# The outline and the text
python "${CLAUDE_SKILL_DIR}/scripts/aps_docs.py" page <source path>

# Only the outline, to check a long page first
python "${CLAUDE_SKILL_DIR}/scripts/aps_docs.py" page <source path> --headings

# Only the code blocks (requests, responses, payloads)
python "${CLAUDE_SKILL_DIR}/scripts/aps_docs.py" page <source path> --code
```

`page` accepts a source path or a full `developer.doc.autodesk.com` URL. Table rows show as `cell | cell`. The text stops at 30000 characters: use `--max-chars` for more.
Read only the pages that the answer needs. A reference page (one endpoint) usually answers a "how do I call" question. A developer's guide page answers a "how does it work" question.

### 4. Answer

1. Answer the question first, in a few sentences.
2. Give the facts from the pages: the endpoint and method, the scopes, the parameters, or the event names.
3. Give the portal link of each page that you used. Copy the `portal` link from the script output. Do not build a link by hand: the portal path is often different from the source path.
4. Add a short example (ex. a `curl` request) when it helps.
5. If the docs do not answer the question, say so. Do not fill the gap from memory without saying that you did.

For a full example of the method, run `python "${CLAUDE_SKILL_DIR}/scripts/aps_docs.py" example`.

## Errors

| Message | What to do |
|---|---|
| `No TOC for source ID` | The ID is wrong. Run the `sources` command. IDs are case-sensitive and include the version (`data_v2`, not `data`). |
| `Page not found` | The docs were deployed again and the source path changed. Run `toc` again with `--refresh` to get the new path. |
| `(guessed from the source path, not found in the TOC)` after a portal link | The page is not in the TOC that the script guessed. Add `--source-id <id>` to get the exact link, or say that the link is not verified. |
| `Cannot reach` | There is no network access. Tell the user. Do not answer from memory as if from the docs. |

## Notes

- The script caches each TOC for 24 hours in the system temp folder. Add `--refresh` to read it again.
- Webhook events for all APS services are in `webhooks_v1`, under `reference/callback/<service>_events/`. File and folder events in ACC, BIM 360, and Fusion are Data Management events (`dm.version.added`, `dm.folder.added`, and others).
- ACC APIs are in the "Forma APIs" docs (`acc_v1`). `forma_v1` is a different API (Forma Site Design).
