# Workspace Format

A VeritySpec workspace is a directory with a `verityspec.json` file and one or
more JSON record files.

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

Records may be stored as individual JSON objects, arrays of objects, or catalog
objects with a top-level `records` array.

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
