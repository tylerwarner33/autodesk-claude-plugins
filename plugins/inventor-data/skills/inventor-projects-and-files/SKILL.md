---
name: inventor-projects-and-files
description: >-
  Autodesk Inventor projects (.ipj), library paths, Vault read-only files, saved versions and migration, model states,
  Content Center parts, copies, references, and which documents to close. Use before code saves, copies or writes to
  an Inventor file, when a write fails with E_FAIL because a file is not modifiable, when a file must open in an older
  Inventor release, or when code opens and closes documents.
---

# Inventor projects and files

## The active project decides what can change

Read the active project before a write: `application.DesignProjectManager.ActiveDesignProject` gives the `.ipj`, its
workspace and its `LibraryPaths`. `Document.IsModifiable` says whether a document can change now.

- A file under a library path of the project is read-only by design. A write to it fails with E_FAIL.
- A Vault workspace makes files read-only until they are checked out. That is a second, separate layer: clear one
  and the other gives the same error.
- To edit library files, a user usually changes to an editing project that has only a workspace path. Do not change
  the active project for the user.
- A switch to a project with a Vault workspace (`DesignProject.Activate`) can start a Vault download with a
  "Download progress" dialog. Wait until it closes. Never click its `Cancel`, which stops the download.
- Never check files in or out of Vault for the user. Do not check test copies into Vault.

## Saved versions

A file saved in a newer release does not open in an older one, even across point releases (ex. 2025.4 to 2025.3).

- Read the saved version before you save: `Document.SoftwareVersionSaved`. Compare it with the release that reads
  the file next.
- A save migrates the file to the release that saves it. Ask the user before you save a file that an older release
  must read.
- A "Data Format Has Changed" dialog migrates the file on OK. For a file that an older release must read, the user
  must click Cancel.
- Apprentice cannot save a file that needs migration to its own release.

## Copies for a test

Test a change on copies, never on the masters. Copy the whole tree under a new folder, clear the read-only attribute,
and point the copies at each other.

- `AllReferencedDocuments` leaves out suppressed components, so walk `document.File.ReferencedFileDescriptors`.
- `FileDescriptor.ReplaceReference` accepts only a copy of the same file.
- References outside the folder (library paths, the Content Center) can stay on the originals.
- If the project searches the copy folder before the masters, give the copies a prefix, so a reference cannot
  resolve to a master.

## Model states

- `FileManager.GetModelStates(fullFileName)` gives the model state names of a file without opening it.
- `ModelStates.MemberEditScope` is stored in each file, not in the session. A write to the factory with
  `kEditAllMembers` changed the Part Number of 333 members in one part. Read it before a write.
- A file with only `[Primary]` has `IsModelStateMember` false and no `FactoryDocument`.
- A write to a member document is allowed. `SaveAs` on an assembly also saves the changed member parts.

## Content Center

A Content Center part does not insert by file path: `Occurrences.Add` gives E_INVALIDARG, and
`AddByComponentDefinition` gives E_FAIL. Use the Content Center API.

## Documents that code opens

- Close only the documents that your code opened. Never call `Documents.CloseAll`: it closes the user's documents.
- `Documents.Open` returns the user's copy when the file is open already, and a close then closes the user's
  document. Before you open a file, look for it in `application.Documents` (compare `FullDocumentName`,
  `FullFileName` and `DisplayName`), and remember which documents you opened.
- `Documents.Open` takes a full document name (the path with the model state, ex. `C:\Parts\Bracket.ipt<State2>`) to
  open one model state. A path alone opens the primary model state.
- Close drawings first, then assemblies, then parts. Closing one document can close another, and `Close` on a closed
  document throws.
- Opening a generated drawing marks it as changed, also when nothing else changed.

## Other file facts

- A STEP file wraps long `PRODUCT(...)` lines. A regular expression over the text must allow line breaks.
- An add-in DLL that Inventor loaded is locked, so a full build fails with MSB3061 on the copy step while Inventor
  runs. That is not a compile error. Build to another output folder, or load a copy of the build.
