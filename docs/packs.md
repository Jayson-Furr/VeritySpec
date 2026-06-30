# Packs

VeritySpec grows through packs. A pack contributes record kinds, JSON Schemas,
readiness gates, reference rules, and generator support without expanding the
core kernel.

Built-in packs currently include:

- `verity.core`: products and reusable object schemas.
- `verity.pack.api`: API endpoints and OpenAPI generation.
- `verity.pack.cli`: CLI commands and CLI reference generation.
- `verity.pack.events`: event messages and AsyncAPI generation.
- `verity.pack.security`: security controls and security report generation.
- `verity.pack.observability`: telemetry, metrics, dashboards, and alerts.
- `verity.pack.accessibility`: accessibility claims, checks, and evidence.
- `verity.pack.compliance`: compliance mappings and compliance matrix generation.
- `verity.pack.deployment`: deployment runtimes, targets, release policies,
  rollback plans, and deployment report generation.

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
  "generators": [
    {
      "id": "openapi",
      "name": "OpenAPI",
      "description": "Emit an OpenAPI document from API endpoint and schema records.",
      "artifactType": "api-description",
      "outputFormats": ["json"],
      "recordKinds": ["api.endpoint"]
    }
  ]
}
```

The manifest contract is defined by
`src/verityspec/schemas/pack-manifest.schema.json`.

Generator declarations may use the legacy string form, such as
`"schema-bundle"`, or the structured metadata form shown above. `verity pack
list --format json` always emits both the normalized `generators` ID list and
`generatorMetadata` for machine clients.

## Pack Standard

Every pack should include:

- A valid `pack.json` manifest.
- At least one strict JSON Schema for a record kind.
- Schemas that require the shared record envelope: `id`, `kind`, `name`,
  `status`, and `owner`.
- Readiness gates for release-relevant records.
- Conditional readiness rules for pack-specific release policy where needed.
- Reference rules for relationships introduced by the pack.
- At least one useful generator or report when applicable.
- Tests and executable examples for expected behavior.

## Commands

```bash
verity pack list
verity pack list --format json
verity pack validate
verity pack validate verity.pack.api --format json
verity pack init verity.pack.features --out build/packs/features --kind feature.flag --force
```

`verity pack init` creates a local starter pack with:

- `pack.json`
- `schemas/<kind>.schema.json`
- one strict starter record schema
- one readiness gate for the starter kind
- one `product` to starter-kind reference rule using the `uses`
  relationship
- `schema-bundle` generator metadata

The generated pack can be validated immediately:

```bash
verity pack validate verity.pack.features --path build/packs/features
```

It can also be loaded by a workspace immediately through `packPaths`. A sample
workspace should include the generated pack ID in `packs`, point `packPaths` at
the generated pack directory, and connect a `product` record to the generated
record kind with a `uses` reference.

## External Packs

Workspaces can load local packs with `packPaths`:

```json
{
  "packs": ["verity.core", "verity.pack.features"],
  "packPaths": ["../custom_pack"]
}
```

`packPaths` entries may point to a pack directory or directly to `pack.json`.
Relative paths in workspace config resolve from the workspace root.

CLI flags can also provide local packs. CLI paths resolve from the current
working directory:

```bash
verity validate ./workspace --pack-path ./packs/features
verity readiness ./workspace --strict --pack-path ./packs/features
verity generate schema-bundle ./workspace --pack-path ./packs/features --out build/schema-bundle.json
verity pack list --path ./packs/features
verity pack validate verity.pack.features --path ./packs/features
```

External packs use the same manifest schema, strict JSON Schema checks, shared
record envelope requirements, readiness gate checks, reference rule checks, and
registry collision checks as built-in packs. External pack IDs cannot shadow
built-in pack IDs.

## Contributing Packs and Schema Changes

Public pack and schema proposals should start from
[Contributing](../CONTRIBUTING.md).

Use the `Pack proposal` issue template for new packs or major pack expansions.
Use the `Schema change` issue template for new fields, required-field changes,
enum changes, reference-shape changes, deprecations, removals, and breaking
schema behavior.

Pack proposals should define the product surface, record kinds, reference
rules, readiness gates, generator or report output, executable examples, tests,
and compatibility boundaries before implementation begins.

Schema changes should explain whether the change is additive, behavioral,
deprecated, or breaking, and should include before-and-after records, migration
impact, affected generators or readiness gates, and validation fixtures.

## Future Product Surface Packs

Future GUI, desktop, mobile, and game packs should follow the boundary guidance
in [Product surface pack boundaries](product-surface-pack-boundaries.md) before
their first schemas are added.

That guidance keeps product-surface packs focused on their own domains and
prevents them from duplicating cross-cutting concerns owned by security,
accessibility, observability, compliance, release, evidence, deployment,
dependency, or portfolio packs.
