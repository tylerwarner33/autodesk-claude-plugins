---
name: inventor-drawings
description: >-
  How to read, measure and change Autodesk Inventor drawings through the API: sheets, views, balloons and leaders,
  drawing curves, styles and templates, and images of a sheet. Use before code measures, compares, balloons or changes
  an Inventor drawing (.idw or .dwg), or when a generated drawing looks wrong and you must find why.
---

# Inventor drawings

## Look before you judge

- Measure the sheet, not the return value: the position and the range box of each view, balloon, dimension text,
  parts list, table, and the title block. Check for overlaps, crossing leaders, and anything outside the border.
- Render the sheet, or a region of it, as an image and look at it before you tell the user that a drawing is correct.
  See "Images from code" below.
- Measure every case, not only the one in the request, before you call a layout change done.

## Balloons and leaders

- A leader is a tree: `Leader.RootNode` is at the balloon, and each leaf node (`ChildNodes.Count == 0`) is an
  arrowhead. A leader can have several branches. A leaf node's `AttachedEntity` is the `GeometryIntent` it points at.
- A balloon names a component through its BOM row. An arrowhead can land on, or near, another component, so check
  the curves near each arrowhead.
- A balloon has no range box in the API. A style that scales to its text is about 3 times the text height across.
- `Balloon.ParentView` gives the view of a balloon. `BalloonValueSets[1].ItemNumber` gives its item number.
- A balloon on a part of a sub-assembly that has its own BOM row shows the item of the sub-assembly.

## Placing balloons

- The API has no auto-balloon method. Inventor's own Auto Balloon command needs the user to select the view and the
  components.
- Build a leader from a `Point2d` for the balloon and a `GeometryIntent` last. `DrawingCurve.MidPoint` can return
  null with no exception (ex. a full circle), so use `CenterPoint` next.
- Get the curves of one component with `view.get_DrawingCurves(occurrence)`. Asking each curve for its owner is much
  slower.
- An item that has a balloon on the sheet usually needs no second balloon, so balloon the main view first.

## Sheets and views

- A sheet that is not active gives E_FAIL for the range boxes of its tables. Activate it first, and restore the
  old active sheet after.
- Two views on one sheet can have the same name. Tell them apart by their position.
- `DrawingView.Position` moves the view with its balloons and dimension text. A change of scale after the
  annotations strands them. Fit the scale once, before you annotate.
- `DrawingCurve` has no visible or hidden flag.
- `view.get_DrawingCurves(Type.Missing)` gives all curves of a view. Each curve's `ModelGeometry` has a
  `ContainingOccurrence` in an assembly view.

## Styles and templates

- When two drawings from the same process look different, compare their styles (`DrawingDocument.StylesManager`).
- A read-only style library replaces a template's layer styles at `Documents.Add`, so a template edit may not reach
  the new drawing. A host with no active project gives different results. A change to a template's local text style
  did survive `Documents.Add`, so the override is not the same for every style.
- The API cannot export a `.styxml` file. Only the Styles Editor can.
- There is no OLE object API. An OLE table in a template cannot be read or deleted.

## Images from code

A transient camera on a sheet renders it with no window: set `Camera.SceneObject` to the sheet, then use
`CreateImageWithOptions` with the option `IncludeEdits`. `Camera.SaveAsBitmap` ignores a camera change that was not
applied.

## Related skills

- `inventor-api-traps`: casts, members called as methods, and the causes of E_FAIL.
