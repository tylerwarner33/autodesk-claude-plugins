---
name: inventor-api-traps
description: >-
  Facts about the Autodesk Inventor COM API that make .NET code fail to compile or throw at run time: members typed
  as object, casts, members that must be called as methods, iLogic through dynamic, the causes of E_FAIL and
  E_INVALIDARG, and collection quirks. Use when writing or fixing C# or VB.NET code that calls the Inventor API (an
  add-in, a plugin, a Design Automation app, or a snippet that an Inventor MCP server runs), or when such code fails
  with a COMException.
---

# Inventor API traps

Each fact here made real code fail. Confirm a member in the Inventor API reference before you use it. A compile
error for a missing member usually names a near member: read it before you guess again.

The examples are C#. A late-bound caller (ex. Python with `pywin32`) does not see the compile errors, but it sees the
same run-time errors.

## How a call runs

- Every API call runs on Inventor's main thread, also a call from another process. Inventor processes no window
  messages until the call returns. Keep each unit of work short (ex. under 10 s), and split a long loop into several
  calls.
- During an edit in place (ex. a part edited inside an assembly), `Application.ActiveEditDocument` is the document in
  edit, and `Application.ActiveDocument` is the top document. The camera of `Application.ActiveView` belongs to the
  top document.
- To make several writes one Undo step, start a transaction on the document that you write, not on the active one:

  ```csharp
  Transaction transaction = application.TransactionManager.StartTransaction((_Document)document, "Change holes");
  try
  {
      // ... the writes ...
      document.Update();
      transaction.End();
  }
  catch
  {
      transaction.Abort();
      throw;
  }
  ```

  Put `document.Update()` inside the transaction, because an `Update` after `End` makes a second step. A transaction
  started inside another one joins it. A rule that runs inside also joins it.
- A user parameter cannot take a name that is a unit (ex. `A` for ampere, `T` for tesla). `AddByExpression` then
  fails with only a COM error.

## Members typed as object

- `Parameter.Value` is `object`. Cast it: `(double)parameter.Value`. It is the database value (centimeters,
  radians). `Parameter._Value` is the same number as a `double`.
- Some definition members are `object`, ex. `RectangularPatternFeatureDefinition.XCount`. Cast them:
  `((Parameter)definition.XCount).Expression`. A direction that the pattern does not use gives the COM code
  `DISP_E_PARAMNOTFOUND` (-2147352572) as an `int`, not a parameter.
- A text or boolean parameter has no numeric value. Read its kind from
  `document.UnitsOfMeasure.GetTypeFromString(parameter.get_Units())`: `kTextUnits` or `kBooleanUnits`.
  Write a text or boolean parameter through `Value`, and a numeric one through `Expression`.

## Casts and conversions

- `PartComponentDefinition` and `AssemblyComponentDefinition` do not convert to `ComponentDefinition`. Read each
  member per type, ex. `document switch { PartDocument p => p.ComponentDefinition.WorkPoints, ... }`.
- `AddMateConstraint` returns `MateConstraint`. Use `var` or that type, not `AssemblyConstraint`.
- `Style.Copy` returns the base `Style`. Cast it, ex. to `TextStyle`.
- `DrawingDimension.Style` is not on the base type. Cast to the specific type, ex. `LinearGeneralDimension`.
- A face's range box is `face.Evaluator.RangeBox`. A planar face's plane is `(Plane)face.Geometry`.
- `IPictureDisp.Handle` from `Camera.CreateImage` overflows through `dynamic`. Read it by reflection as an `int`.

## Members that must be called as methods

When the COM getter and setter have different types, C# cannot form a property. The compiler error names the method.

| Member | Call |
| --- | --- |
| `Parameter.Units` | `parameter.get_Units()` |
| `iLogicAutomation.Rules` | `automation.get_Rules(document)` |
| `DrawingView.DrawingCurves` | `view.get_DrawingCurves(Type.Missing)` for all curves |

An indexed property is called with brackets, ex. `application.ApplicationAddIns.ItemById["{...}"]`.

## iLogic from C#

Get the automation object from the iLogic add-in, and keep it `dynamic`. The document argument of `get_Rules`,
`GetRule` and `RunRule` must be statically typed `Inventor.Document`, not `PartDocument`:

```csharp
dynamic automation = application.ApplicationAddIns.ItemById["{3BDD8D79-2179-4B11-8A5A-257B1C0263AC}"].Automation;
dynamic rules = automation.get_Rules((Document)part);
```

## Names that collide with System

With `using Inventor;`, `File`, `Path`, `Environment` and others are Inventor types. Write `System.IO.File`,
`System.IO.Path` and `System.Environment`.

## E_FAIL and E_INVALIDARG

E_FAIL (0x80004005) gives no cause. Known causes:

- A write to a document that is not modifiable: in a library path of the active project, read-only, or checked in to
  Vault. A late-bound write can give "Exception has been thrown by the target of an invocation" for the same cause.
- A member of a document that is closed. Read every fact you need before the first `Close`.
- A lazy LINQ query that runs after its document closed. Call `ToList()` before the close.
- `((Document)occurrence.Definition.Document).FullFileName` on some occurrences. Read
  `occurrence.ReferencedDocumentDescriptor.FullDocumentName` instead, and skip suppressed occurrences.
- A range box of a table on a sheet that is not active. Activate the sheet first, and restore the old one after.
- Closing a referenced part before its parent. Close drawings, then assemblies, then parts.
- `XDirectionEntity` of a suppressed pattern.

E_INVALIDARG causes:

- `UserParameters.AddByExpression` for a boolean. Use `AddByValue(name, true, UnitsTypeEnum.kBooleanUnits)`.
- `Documents.Add` with a template that is open.
- `AddWithOptions` with a model state name that does not exist. Read the names with
  `FileManager.GetModelStates` first.
- A Content Center part through `Occurrences.Add`. Insert it through the Content Center API.

## Features and their names

- `PartFeature.Delete(false, ...)` also deletes the sketch that the feature consumed. The first argument keeps the
  consumed sketch when it is `true`. Pass `true` to make the feature again from the same sketch, ex. in the other
  direction.
- A feature cannot take the name of a sketch: the rename throws `COMException`. Give each its own name, ex.
  `Hole Sketch` for the sketch and `Hole` for the feature.

## Collections

- `SubOccurrences` has no `ItemByName`.
- `CompositeiMateDefinition` has `Count` and an indexer, not an `iMateDefinitions` collection.
- `ModelState.Document` is null for the active model state. Use the document itself for that state.
- `ReplaceReference` is on `FileDescriptor` (`document.File.ReferencedFileDescriptors`), and the new file must be a
  copy of the old one. `AllReferencedDocuments` leaves out suppressed components.
- A `Balloon` leader is a tree. `Leader.RootNode` is at the balloon. Each leaf node (`ChildNodes.Count == 0`) is
  an arrowhead, and its `AttachedEntity` is the `GeometryIntent` it points at.
- Two drawing views on one sheet can have the same name.

## Related skills

- `inventor-modeling`: units, named faces, extent direction, and how to verify a geometry write.
- `inventor-drawings`: sheets, views, balloons, styles, and images.
