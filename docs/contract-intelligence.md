# Contract Intelligence

VeritySpec includes diagnostic commands for understanding product-contract
health and validation failures.

## Doctor

`doctor` runs validation, lint, readiness, and graph summary checks together:

```bash
verity doctor examples/basic
verity doctor examples/basic --format json
verity doctor examples/basic --report-out build/doctor-report.json
verity doctor examples/basic --fail-on warning
```

`--report-out` writes the structured doctor JSON payload to a file and creates
parent directories as needed. The selected stdout format is unchanged, so teams
can keep text diagnostics in CI logs while storing a machine-readable report.

## Explain

`explain` documents issue codes:

```bash
verity explain reference.missing
verity explain reference.disallowed --format json
verity explain --format json
```

## Fail-On

Contract-checking commands support configurable failure thresholds:

```bash
verity validate examples/basic --fail-on error
verity validate examples/basic --fail-on warning
verity lint examples/basic --strict --fail-on warning
verity readiness examples/basic --strict --fail-on warning
```

`--fail-on error` is the default. `--fail-on warning` is useful for stricter CI
environments.

## Graph Filters

```bash
verity graph examples/basic --focus api.users.create
verity graph examples/basic --orphans
verity graph tests/fixtures/broken_semantics --cycles --format json
```

Filtered graph output keeps the same `nodes` and `edges` structure as the full
graph. Cycle output also includes a `cycles` array.
