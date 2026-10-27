# Worked Example

Question: "What webhooks fire when a file changes in ACC?"

The commands below show the method. The results are an example from 2026-10-27. Always read the live docs: event names and paths change.
In the commands, `aps_docs.py` is `"${CLAUDE_SKILL_DIR}/scripts/aps_docs.py"`.

## 1. Choose the API

"Webhook" and "file changes" point to `webhooks_v1` (see `sources.md`). ACC files are stored by Data Management, so the events are Data Management events.

## 2. Find the pages

```bash
python aps_docs.py toc webhooks_v1 --match "data_management_events/"
```

The result lists one page for each event, with its source path and portal link:

```
- dm.version.added
  source: forge-webhooks-webhooks-api-documentation-master-116/webhooks/v1/reference/callback/data_management_events/dm.version.added.html
  portal: https://aps.autodesk.com/en/docs/webhooks/v1/reference/events/data_management_events/dm.version.added/
```

The portal path (`reference/events/`) is not the source path (`reference/callback/`). Use the portal link that the script gives. Do not build it by hand.

## 3. Read the pages

```bash
python aps_docs.py page forge-webhooks-webhooks-api-documentation-master-116/webhooks/v1/reference/callback/data_management_events/dm.version.added.html --headings
python aps_docs.py page forge-webhooks-webhooks-api-documentation-master-116/webhooks/v1/reference/callback/data_management_events/dm.version.added.html
```

Read the outline first on a long page. Then read the full text, or `--code` for the payload example.

## 4. Answer

- Name the events that answer the question. On 2026-10-27, the file events were `dm.version.added`, `dm.version.modified`, `dm.version.deleted`, `dm.version.moved`, and `dm.version.copied`, and the folder events were `dm.folder.added`, `dm.folder.modified`, `dm.folder.deleted`, and `dm.folder.moved`.
- Say what each event means, from the page text.
- Give the portal link of each page that you used.
- Add a short example if it helps, ex. the request that creates the webhook (`POST /webhooks/v1/systems/data/events/dm.version.added/hooks`), from the reference pages.
