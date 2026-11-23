# APS Glossary

Terms and acronyms that the APS documentation uses. If a term is not here, find its definition in the pages that you read.

| Term | Meaning |
|---|---|
| APS | Autodesk Platform Services. The old name is Forge. |
| ACC | Autodesk Construction Cloud. Its APIs are now in the "Forma APIs" docs (`acc_v1`). |
| BIM 360 | The construction platform before ACC. |
| Build | Autodesk Build, the construction management module of ACC (field work, cost, and more). |
| MD | The Model Derivative API. It translates design files into formats you can view (SVF, SVF2) or use. |
| DM | The Data Management API. It manages files, folders, versions, and storage (OSS, BIM 360, ACC hubs). |
| OSS | Object Storage Service. The APS cloud storage for design files (buckets and objects). |
| Hub | The top-level container in Data Management. It is an ACC, BIM 360, or Fusion account. |
| URN | A resource ID. Model Derivative uses the Base64 URL-safe form of the object or version ID. |
| SVF, SVF2 | The formats for the APS Viewer. Model Derivative makes them. |
| Manifest | The translation status and the list of outputs of a Model Derivative job. |
| Webhook | A server-to-server callback that APS sends when an event occurs (ex. `dm.version.added`). |
| 2LO, 3LO | Two-legged (app only) and three-legged (with a user) OAuth sign-in. |
| PKCE | Proof Key for Code Exchange. A 3-legged sign-in for apps that cannot keep a secret (desktop, mobile, single-page). |
| SSA | Secure Service Accounts. Server-to-server access that keeps a user context. |
| AEC | Architecture, Engineering, and Construction. |
| AECDM | The AEC Data Model API. A GraphQL API for design and construction data in ACC. |
| DX | Data Exchange. An API to exchange a part of a design between apps in a neutral format. |
| IFC | Industry Foundation Classes. An open file format to exchange BIM data. |
| RFI | Request for Information. A formal question during construction, tracked in ACC or BIM 360. |
| ACAD | AutoCAD. 2D and 3D drafting software (`.dwg` files). |
| Civil | Civil 3D. Design software for civil infrastructure. |
| Revit | BIM software for architecture, structure, and MEP (`.rvt` files). |

## Translation cost

Model Derivative charges more for a complex job. Revit (`.rvt`), IFC, and Navisworks (`.nwd`, `.nwc`) files are complex jobs. All other files are simple jobs.
