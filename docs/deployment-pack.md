# Deployment Pack

`verity.pack.deployment` adds deployment runtime and target records without
moving infrastructure concepts into the VeritySpec core kernel.

## Record Kinds

- `deployment.runtime`: runtime contract for the thing that is built or
  executed, such as a container, function, package, static bundle, binary, or
  managed-service configuration.
- `deployment.target`: release environment contract for where the runtime is
  hosted, including provider, platform, regions, release policy, rollback plan,
  and production health-check coverage.

## Relationships

The pack declares these reference relationships:

- `product` `deploysTo` `deployment.target`
- `deployment.target` `runtimeRef` `deployment.runtime`
- `deployment.target` `monitoredBy` `observability.dashboard`
- `deployment.target` `securedBy` `security.control`

`runtimeRef` is resolved as a first-class reference field, so missing,
deprecated, removed, or disallowed runtime links are caught by validation.

## Production Readiness

Production deployment targets must:

- require release approval
- declare a rollback plan
- expose a health-check URL

If a production target misses one of those controls, readiness emits
`deployment.target.production_release_controls_missing`. With
`verity readiness --strict`, that issue is an error.

## Commands

```bash
verity validate examples/deployment
verity lint examples/deployment --strict
verity readiness examples/deployment --strict
verity generate deployment-report examples/deployment --out build/deployment-report.json
verity generate schema-bundle examples/deployment --out build/deployment-schema-bundle.json
```

## Deployment Report

`deployment-report` emits JSON with:

- workspace metadata
- runtime and deployment-target counts
- target counts by environment, provider, and platform
- runtime counts by runtime type
- release gaps for missing runtimes, production controls, rollback plans,
  health checks, and owners
- per-runtime and per-target detail for release review

The report is intended for CI, release review, operations handoff, and
downstream deployment dashboards.
