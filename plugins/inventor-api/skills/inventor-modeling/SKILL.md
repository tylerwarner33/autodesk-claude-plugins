---
name: inventor-modeling
description: >-
  How to write geometry in an Autodesk Inventor part or assembly through the API: named faces and the ViewCube,
  centimeters and radians, sketch-relative feature extent direction, patterns, holes, constraints, and how to verify a
  write against the model. Use before code creates or changes sketches, features, patterns, holes or constraints, or
  when a request names a face (ex. "the top face"), a direction, or units.
---

# Inventor modeling

## A named face means the ViewCube face

"The top face" means the face labeled Top on the Inventor ViewCube. The ViewCube can change per document, so read it
before you write geometry that names a face or a direction.

On an unmodified part the mapping is Top +Y, Front +Z, Right +X, so Y is up, not Z. Treat that as what to expect,
never as the answer. A Z-up guess puts the work on the Front face.

To read it, save the camera of `Application.ActiveView` (`Eye`, `Target`, `UpVector`). For each face, set
`camera.ViewOrientationType` (ex. `ViewOrientationTypeEnum.kTopViewOrientation`) and call `camera.Apply()`. The
direction from `Target` to `Eye` is the outward direction of that face. Then restore the saved camera and apply it.

## Units

Inventor stores every length in centimeters and every angle in radians, whatever the document shows. A parameter
that reads "2 in" has the value 5.08.

- Convert with `document.UnitsOfMeasure.ConvertUnits(value, UnitsTypeEnum.kInchLengthUnits, UnitsTypeEnum.kDatabaseLengthUnits)`.
- Use the document's `UnitsOfMeasure`, not the application's: only the document's resolves parameter names in an
  expression.
- Convert once at the start, so every value after it is in the user's units.

## Feature extent direction is relative to the sketch

`PartFeatureExtentDirectionEnum` is relative to the sketch's own normal, and a sketch on a face can point the other
way from the face's world normal. A cut in the wrong direction removes nothing, and Inventor reports that as
`kDriverLostHealth`, not as an error.

Never assume the direction. Create the feature, update, and check that material was removed. If nothing was cut,
delete the feature with `Delete(true, false, false)`, which keeps its sketch, and use the other direction.

## Use the feature that the request names

A hole is a `HoleFeature`, not an extrude cut of a circle. The geometry is the same, but the user edits the model
through its features.

## Make the model stable

- Dimension sketch geometry from a projected work plane, not from a body vertex or a face edge. It stays correct
  when the geometry changes.
- Base a pattern direction on a work axis, not on a feature edge. If the feature that owns the edge is suppressed,
  the pattern fails with it.
- A flush constraint with an offset can solve on either side. Test mate against flush and the sign of the offset,
  then check the position.

## Verify against the model, not the return value

An API call can succeed while the model is wrong. After every write:

1. **Update, then read the health.** Call `document.Update()`, then read `HealthStatus` of each new or changed
   feature. Anything other than `kUpToDateHealth` is a problem. A new feature with `kDriverLostHealth` has usually
   cut nothing.
2. **Check the geometry that the write was for.** Ex. count the cylindrical faces of the body
   (`face.SurfaceType == SurfaceTypeEnum.kCylinderSurface`) before and after a hole, compare
   `ComponentDefinition.MassProperties.Volume` before and after a cut, or read the count and the position of each
   element of a pattern.
3. **Only then report the work as done.**

A failed call can still change the model: read the state again before you retry.
