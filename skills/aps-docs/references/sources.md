# APS Documentation Sources

Each API has a source ID. Give it to `aps_docs.py toc <source_id>`.
The titles and page counts were read from the live TOC files on 2026-10-27.

| Source ID | API title | Pages |
|---|---|---|
| `acc_v1` | Forma APIs (Autodesk Construction Cloud, ACC) | 525 |
| `aecdatamodel_v1` | AEC Data Model API | 196 |
| `applications_v1` | Application Management API | 14 |
| `bim360_v1` | BIM 360 API | 365 |
| `buildingconnected_v2` | BuildingConnected & TradeTapp APIs | 193 |
| `data_v2` | Data Management API | 780 |
| `dataviz_v1` | Data Visualization | 33 |
| `design-automation_v3` | Automation API (Design Automation) | 119 |
| `dx-sdk-beta_v7.2.0` | Data Exchange .NET SDK v7.2.0 | 2199 |
| `fdxgraph_v1` | Data Exchange GraphQL | 96 |
| `flow_graph_engine_v1` | Flow Graph Engine | 44 |
| `forma_v1` | Forma Site Design API (Beta) | 53 |
| `informed-design_v1` | Informed Design API (Beta) | 49 |
| `insights_v1` | Business Success Plan Reporting API | 19 |
| `mfgdataapi_v3` | Manufacturing Data Model API | 502 |
| `model-derivative_v2` | Model Derivative API | 275 |
| `oauth_v2` | Authentication (OAuth) | 63 |
| `parameters_v1` | Parameters API | 46 |
| `profile_v2` | User Profile API | 47 |
| `ssa_v1` | Secure Service Account API | 29 |
| `sustainability_v3` | Sustainability Data API | 62 |
| `tandem_v1` | Tandem Data | 56 |
| `tokenflex_v1` | Token Flex Usage Data API | 33 |
| `vaultdataapi_v2` | Vault Data API | 132 |
| `viewer_v7` | Viewer | 205 |
| `webhooks_v1` | Webhooks API | 187 |

## Which API answers the question

| The question is about | Start with |
|---|---|
| Files, folders, versions, hubs, projects, OSS buckets | `data_v2` |
| Translate a model, SVF or SVF2, derivatives, the manifest, model properties | `model-derivative_v2` |
| Show a model in a browser | `viewer_v7` |
| Tokens, scopes, 2-legged or 3-legged sign-in, PKCE | `oauth_v2` |
| Server-to-server access with user context | `ssa_v1` |
| Callbacks when something changes (all event types) | `webhooks_v1` |
| ACC issues, RFIs, submittals, cost, admin, Forms | `acc_v1` |
| BIM 360 projects and admin | `bim360_v1` |
| Run Revit, AutoCAD, Inventor, or 3ds Max in the cloud | `design-automation_v3` |
| AEC design data as GraphQL | `aecdatamodel_v1` |
| Fusion and manufacturing data as GraphQL | `mfgdataapi_v3` |
| Vault | `vaultdataapi_v2` |
| Digital twins | `tandem_v1` |

## A source that is not in the table

The ID is `<api-name>_v<major version>`, ex. `data_v2`. A beta SDK can have the full version, ex. `dx-sdk-beta_v7.2.0`.
A wrong ID returns `No TOC for source ID`. To find the ID of an API that is not listed, open its page on `aps.autodesk.com`: the path after `/en/docs/` has the API name and the version (ex. `/en/docs/data/v2/` is `data_v2`).
