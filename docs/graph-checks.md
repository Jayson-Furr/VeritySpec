# Graph Checks

VeritySpec treats records as a directed graph. References are edges between
records.

Current graph and reference checks:

- `reference.missing`: target record does not exist.
- `reference.disallowed`: pack rules do not allow the source kind,
  relationship, and target kind.
- `reference.deprecated`: active record references a deprecated record.
- `reference.removed`: active record references a removed record.
- `graph.orphan`: non-product, non-schema record is disconnected.
- `schema.unused`: schema record has no incoming references.
- `graph.cycle`: directed reference cycle detected.

Reference issue locations include the nested field path when VeritySpec can
identify it, such as `records/api.json:responses[0].schema` or
`records/product.json:references[0].target`.

Run graph output:

```bash
verity graph examples/basic
verity graph examples/basic --format json
verity graph examples/basic --focus api.users.create
verity graph examples/basic --orphans
verity graph tests/fixtures/broken_semantics --cycles --format json
```

Run semantic validation:

```bash
verity validate examples/basic --strict
```

Future cross-workspace graph behavior should follow
[Cross-workspace dependencies](cross-workspace-dependencies.md). The current
graph checks remain local to one loaded workspace.
