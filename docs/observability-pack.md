# Observability Pack

`verity.pack.observability` adds product observability records without
expanding the core kernel.

## Record Kinds

- `observability.telemetry`: emitted signals with a `payloadSchema`.
- `observability.metric`: measured signals with a unit and aggregation.
- `observability.dashboard`: dashboard ownership and links to displayed
  signals.
- `observability.alert`: alert ownership, severity, condition, and runbook
  metadata.

## Relationships

The pack declares these reference relationships:

- `product` `observes` `observability.dashboard`
- `observability.telemetry` `payloadSchema` `schema.object`
- `observability.metric` `derivedFrom` `observability.telemetry`
- `observability.dashboard` `displays` `observability.metric`
- `observability.dashboard` `tracks` `observability.alert`
- `observability.alert` `firesOn` `observability.metric`

## Example

```bash
verity validate examples/observability
verity lint examples/observability --strict
verity readiness examples/observability --strict
verity generate observability-report examples/observability --out build/observability-report.json
verity generate schema-bundle examples/observability --out build/observability-schema-bundle.json
```

The example workspace connects a checkout product to a reliability dashboard,
checkout success-rate metric, low-success alert, emitted telemetry signal, and
telemetry payload schema.

## Report

`observability-report` emits JSON with:

- counts for telemetry, metrics, dashboards, and alerts
- ownership and alert-severity summaries
- release gaps for telemetry without metrics, metrics without telemetry,
  dashboards without tracked alerts, alerts without runbooks, and missing
  owners
- detailed telemetry, metric, dashboard, and alert entries with connected
  targets

The `examples/observability` report and schema-bundle shapes are covered by
committed golden fixtures at `tests/golden/observability/observability_report.json`
and `tests/golden/observability/schema_bundle.json`. Tests normalize dynamic
report metadata such as generation time, package version, and local workspace
path before comparing the report fixture.
