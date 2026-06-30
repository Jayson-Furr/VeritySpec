# Workspace Format

A VeritySpec workspace is a directory with a `verityspec.json` file and one or
more JSON record files.

```json
{
  "workspace": "examples.api_service",
  "specVersion": "v0.1.0",
  "packs": ["verity.core", "verity.pack.api"],
  "records": ["records/*.json"]
}
```

## Fields

- `workspace`: stable workspace identifier.
- `specVersion`: VeritySpec workspace format version.
- `packs`: built-in pack IDs to load.
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

