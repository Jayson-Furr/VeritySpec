# Packs

VeritySpec grows through packs. A pack contributes record kinds, JSON Schemas,
readiness gates, reference rules, and generator support without expanding the
core kernel.

## Manifest

Each built-in pack has a `pack.json` manifest:

```json
{
  "id": "verity.pack.api",
  "version": "0.1.0",
  "name": "VeritySpec API Pack",
  "description": "API endpoint records and OpenAPI generation support.",
  "schemas": [
    {
      "kind": "api.endpoint",
      "path": "schemas/api-endpoint.schema.json"
    }
  ],
  "readinessGates": [],
  "referenceRules": [],
  "generators": ["openapi"]
}
```

The manifest contract is defined by
`src/verityspec/schemas/pack-manifest.schema.json`.

## Pack Standard

Every pack should include:

- A valid `pack.json` manifest.
- At least one strict JSON Schema for a record kind.
- Schemas that require the shared record envelope: `id`, `kind`, `name`,
  `status`, and `owner`.
- Readiness gates for release-relevant records.
- Reference rules for relationships introduced by the pack.
- At least one useful generator or report when applicable.
- Tests and executable examples for expected behavior.

## Commands

```bash
verity pack list
verity pack list --format json
verity pack validate
verity pack validate verity.pack.api --format json
```

