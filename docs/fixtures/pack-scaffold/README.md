# Pack Scaffold Fixture

This fixture shows the complete output shape expected from:

```bash
verity pack init verity.pack.features --out docs/fixtures/pack-scaffold/packs/features --kind feature.flag --name "Feature Pack" --description "Feature flag records for pack scaffold documentation."
```

It also includes a consuming workspace that loads the generated pack through
`packPaths`.

```text
docs/fixtures/pack-scaffold/
  packs/
    features/
      pack.json
      schemas/
        feature-flag.schema.json
  workspace/
    verityspec.json
    records/
      product.json
      feature.checkout.json
```

Executable checks:

```bash
verity pack validate verity.pack.features --path docs/fixtures/pack-scaffold/packs/features
verity validate docs/fixtures/pack-scaffold/workspace
verity lint docs/fixtures/pack-scaffold/workspace --strict
verity readiness docs/fixtures/pack-scaffold/workspace --strict
verity generate schema-bundle docs/fixtures/pack-scaffold/workspace --out build/pack-scaffold-schema-bundle.json
verity generate pack-capability-index docs/fixtures/pack-scaffold/workspace --out build/pack-scaffold-capability-index.json
```
