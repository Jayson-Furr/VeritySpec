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
