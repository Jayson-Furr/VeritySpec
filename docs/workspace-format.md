# Workspace Format

A VeritySpec workspace is a directory with a `verityspec.json` file and one or
more JSON record files.

Create a starter workspace with:

```bash
verity init ./workspace --template api --owner platform
```

Supported templates are `basic`, `api`, `cli`, `events`, and `security`. The
generated workspaces include the built-in packs and starter records needed to
validate, lint, and pass readiness immediately.

```json
{
  "workspace": "examples.api_service",
  "specVersion": "v0.2.0",
  "packs": ["verity.core", "verity.pack.api"],
  "packPaths": [],
  "records": ["records/*.json"]
}
```

## Fields

- `workspace`: stable workspace identifier.
- `specVersion`: VeritySpec workspace format version. The current value is
  `v0.2.0`; `v0.1.0` remains supported for compatibility, and unknown future
  versions fail validation.
- `packs`: built-in pack IDs to load.
- `packPaths`: explicit local pack directories or `pack.json` files. Use `[]`
  when no external packs are used. Relative paths resolve from the workspace
  root. This field is required in `v0.2.0` workspaces.
- `records`: glob patterns, relative to the workspace root.
- `dependencies`: optional direct local workspace dependencies. This prototype
  is local-path, readonly, and direct-dependency only.
- `exports`: optional dependency-workspace export list. A workspace referenced
  as a dependency can expose record IDs that consuming workspaces may reference.

Records may be stored as individual JSON objects, arrays of objects, or catalog
objects with a top-level `records` array.

## Local Workspace Dependencies

Workspaces can declare direct local, readonly dependencies with
`dependencies`. This does not change the current workspace format version;
`v0.2.0` remains current.

```json
{
  "workspace": "studio.game.dream_extraction",
  "specVersion": "v0.2.0",
  "packs": ["verity.core", "verity.pack.unity"],
  "packPaths": [],
  "dependencies": [
    {
      "id": "studio.library.shared_unity_runtime",
      "alias": "sharedUnity",
      "version": "^1.2.0",
      "source": "../shared-unity-runtime",
      "mode": "readonly"
    }
  ],
  "records": ["records/*.json"]
}
```

Dependency declarations use these fields:

- `id`: expected workspace ID from the dependency workspace manifest.
- `alias`: local reference prefix, such as `sharedUnity`.
- `source`: local path to the dependency workspace.
- `mode`: currently only `readonly` is supported.
- `version`: optional exact or caret version constraint checked against the
  dependency workspace manifest `version`.

Consuming records can reference exported dependency records with an
alias-qualified target:

```text
sharedUnity::unity.package.save_system
```

Dependency workspaces expose records with a manifest-level `exports` array:

```json
{
  "workspace": "studio.library.shared_unity_runtime",
  "version": "1.2.0",
  "specVersion": "v0.2.0",
  "packs": ["verity.core", "verity.pack.unity"],
  "packPaths": [],
  "exports": ["unity.package.save_system"],
  "records": ["records/*.json"]
}
```

Validation checks dependency source paths, workspace IDs, version constraints,
aliases, referenced records, exported-record boundaries, deprecated or removed
dependency records, and pack reference rules. `verity graph --format json`
includes exported dependency records as alias-qualified dependency nodes.

Current dependency support intentionally excludes remote registries, Git
authentication, transitive dependency policy, lockfiles, dependency update
commands, and record-level visibility fields. See
[Cross-workspace dependencies](cross-workspace-dependencies.md) for the
longer-term design.

## Shared Record Envelope

Every record kind must require:

- `id`
- `kind`
- `name`
- `status`
- `owner`

Pack schemas can add kind-specific fields while keeping this common envelope.

See [Versioning and migrations](versioning-and-migrations.md) for
`specVersion` validation and `verity migrate` behavior.
