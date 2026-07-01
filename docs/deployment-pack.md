# Deployment Pack

`verity.pack.deployment` adds deployment runtime and target records without
moving infrastructure concepts into the VeritySpec core kernel.

## Record Kinds

- `deployment.runtime`: runtime contract for the thing that is built or
  executed, such as a container, function, package, static bundle, binary, or
  managed-service configuration.
- `deployment.target`: release environment contract for where the runtime is
  hosted, including provider, platform, regions, release policy, rollback plan,
  production health-check coverage, and release evidence links.

## Relationships

The pack declares these reference relationships:

- `product` `deploysTo` `deployment.target`
- `deployment.target` `runtimeRef` `deployment.runtime`
- `deployment.target` `monitoredBy` `observability.dashboard`
- `deployment.target` `securedBy` `security.control`
- `deployment.target` `complianceMappedBy` `compliance.mapping`
- `deployment.target` `releaseEvidence` evidence records such as
  `evidence.ci-run`, `evidence.qa`, and `evidence.artifact`

`runtimeRef` is resolved as a first-class reference field, so missing,
deprecated, removed, or disallowed runtime links are caught by validation.
Deployment targets also expose `securityControlRefs`,
`observabilityDashboardRefs`, `complianceMappingRefs`, and
`releaseEvidenceRefs` arrays for readiness gates and deployment-report output.
Authors should keep matching explicit `references` entries so graph validation
can prove the linked records resolve.

## Production Readiness

Production deployment targets must:

- require release approval
- declare a rollback plan
- expose a health-check URL
- link at least one security control
- link at least one observability dashboard
- link at least one compliance mapping
- link at least one release evidence record

If a production target misses one of those controls, readiness emits
`deployment.target.production_release_controls_missing`. With
`verity readiness --strict`, that issue is an error.

These links record internal product-contract evidence. They do not make legal,
commercial, platform-certification, marketplace, app-store, store-review,
pricing-approval, or support-SLA claims.

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
  health checks, security links, observability links, compliance links,
  release evidence links, and owners
- per-runtime and per-target detail for release review, including linked
  security controls, observability dashboards, compliance mappings, and release
  evidence status/URI summaries

The report is intended for CI, release review, operations handoff, and
downstream deployment dashboards.
