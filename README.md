# VeritySpec

[![CI](https://github.com/Jayson-Furr/VeritySpec/actions/workflows/ci.yml/badge.svg)](https://github.com/Jayson-Furr/VeritySpec/actions/workflows/ci.yml)
[![Release](https://img.shields.io/badge/release-v0.14.0-blue)](https://github.com/Jayson-Furr/VeritySpec/releases/tag/v0.14.0)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](pyproject.toml)
[![License](https://img.shields.io/github/license/Jayson-Furr/VeritySpec)](LICENSE)

Executable product contracts for humans, tools, and agents.

VeritySpec supersedes PrismSpec by changing the project from a broad static
schema catalog into an installable product-specification toolchain. The core
artifact is a workspace that can be validated, linted, checked for readiness,
graphed, diffed, and used to generate implementation and documentation
artifacts.

## Current Scope

Latest release: `v0.14.0`. Release history is tracked in
[CHANGELOG.md](CHANGELOG.md) and [ROADMAP.md](ROADMAP.md).

This implementation provides:

- An installable Python package with the `verity` CLI.
- A small core model: workspace, pack, schema, record, reference graph,
  validation issue, readiness gate, generator, and migration entry point.
- Built-in packs for core product records, APIs, CLIs, events, security
  controls, observability signals, accessibility claims, and compliance
  mappings.
- Pack listing, validation, and scaffolding through `verity pack`, including
  local external packs, structured generator metadata, and starter reference
  rules that make generated packs usable from sample workspaces immediately.
- Workspace initialization templates for basic, API, CLI, events, and security starter contracts.
- Structural validation with JSON Schema.
- Semantic validation for duplicate IDs, unknown kinds, missing references,
  disallowed relationships, deprecated references, removed references, orphan
  records, unused schemas, reference cycles, workspace spec versions, and
  nested issue locations.
- Readiness gates driven by pack metadata, including conditional pack rules
  for release-blocking policy.
- Generators for OpenAPI, AsyncAPI, TypeScript types, Python models, schema
  bundles, CLI reference docs, validation reports, security reports,
  observability reports, accessibility reports, and compliance matrices, with
  OpenAPI path-parameter support and snapshot-tested type/model output
  including nested Python dataclasses.
- A PrismSpec importer that produces a converted workspace and migration report.
- Workspace migration-chain planning and reporting through `verity migrate`.
- Migration dry-run fixture coverage for each supported workspace version edge.
- Fixture compatibility coverage across supported workspace format versions.
- Doctor diagnostics that can be printed to stdout or written as JSON reports.
- Downstream GitHub Actions templates and a reusable workflow for product-contract enforcement.

## Quick Start

Install the latest GitHub release:

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.14.0"
verity --version
```

PyPI publishing is prepared but not enabled yet. After publishing is enabled:

```bash
pip install verityspec
verity --version
```

For local development:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools
pip install -e .

verity --version
verity init build/init-api --template api --owner platform --force
verity validate build/init-api
verity pack list
verity pack validate
verity pack init verity.pack.features --out build/packs/features --kind feature.flag --force
verity pack validate verity.pack.features --path tests/fixtures/custom_pack
verity validate examples/basic
verity validate tests/fixtures/custom_pack_workspace
verity lint examples/basic --strict
verity readiness examples/basic --strict
verity readiness examples/security --strict
verity readiness examples/observability --strict
verity readiness examples/accessibility --strict
verity readiness examples/compliance --strict
verity doctor examples/basic
verity doctor examples/basic --report-out build/doctor-report.json
verity explain reference.missing
verity graph examples/basic
verity diff examples/basic examples/basic --format json
verity migrate --list --format json
verity migrate examples/basic --dry-run --format json
verity generate openapi examples/basic --out build/openapi.json
verity generate asyncapi examples/basic --out build/asyncapi.json
verity generate typescript examples/basic --out build/types.ts
verity generate python-models examples/basic --out build/models.py
verity generate cli-reference examples/basic --out build/cli-reference.md
verity generate validation-report examples/basic --out build/validation-report.json
verity generate security-report examples/security --out build/security-report.json
verity generate observability-report examples/observability --out build/observability-report.json
verity generate accessibility-report examples/accessibility --out build/accessibility-report.json
verity generate compliance-matrix examples/compliance --out build/compliance-matrix.json
verity generate schema-bundle examples/accessibility --out build/accessibility-schema-bundle.json
verity generate schema-bundle examples/compliance --out build/compliance-schema-bundle.json
verity generate schema-bundle tests/fixtures/custom_pack_workspace --out build/custom-schema-bundle.json
verity import prismspec tests/fixtures/prismspec_sample --out build/prismspec-import
```

Without installation, run the package directly:

```bash
PYTHONPATH=src python3 -m verityspec validate examples/basic
```

## CLI Contract

The contract-checking commands support text and JSON output:

```bash
verity validate examples/basic --format json
verity lint examples/basic --strict --format json
verity readiness examples/basic --strict --format json
verity doctor examples/basic --format json
verity doctor examples/basic --report-out build/doctor-report.json
```

`verity doctor --report-out` writes the same structured JSON diagnostics used
by `--format json` while preserving the selected stdout format.

Starter workspaces can be created with `verity init --template`. Supported
templates are `basic`, `api`, `cli`, `events`, and `security`.

Stable exit codes:

| Code | Meaning |
|---:|---|
| 0 | Success |
| 1 | Product contract failed validation, lint, readiness, or generation preflight |
| 2 | Usage error, including invalid command arguments |
| 3 | Unexpected internal error |

Minimal CI usage:

```bash
verity validate examples/basic
verity lint examples/basic --strict
verity readiness examples/basic --strict
verity diff previous-workspace current-workspace --format json
verity generate openapi examples/basic --out build/openapi.json
verity generate validation-report examples/basic --out build/validation-report.json
```

## Semantic Validation

VeritySpec validates more than JSON shape. Built-in packs declare allowed
reference relationships between record kinds, and validation checks whether the
workspace graph is coherent. Current semantic checks include:

- Missing references
- Disallowed source/relationship/target-kind combinations
- References to deprecated or removed records
- Orphan records
- Unused schemas
- Reference cycles

Validation reports can be generated as JSON:

```bash
verity generate validation-report examples/basic --out build/validation-report.json
```

## Packs

Built-in packs can be inspected and validated:

```bash
verity pack list
verity pack list --format json
verity pack validate
verity pack init verity.pack.features --out build/packs/features --kind feature.flag --force
verity pack validate verity.pack.api --format json
verity pack list --path tests/fixtures/custom_pack
verity pack validate verity.pack.features --path tests/fixtures/custom_pack
```

See [docs/packs.md](docs/packs.md) for the pack manifest contract and pack
standard, including the generated `product` to starter-kind `uses` reference
rule for sample workspaces.

Run tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Workspace Shape

Package releases and workspace format versions are intentionally separate.
VeritySpec package `v0.14.0` supports workspace formats `v0.1.0` and
`v0.2.0`. The current workspace format is `v0.2.0`.

```json
{
  "workspace": "examples.basic",
  "specVersion": "v0.2.0",
  "packs": [
    "verity.core",
    "verity.pack.api",
    "verity.pack.cli",
    "verity.pack.events"
  ],
  "packPaths": [],
  "records": [
    "records/*.json"
  ]
}
```

Records are normal JSON files. Every record has an `id`, `kind`, `name`,
`status`, and `owner`, plus fields defined by its pack.

## Examples

- [examples/basic](examples/basic/verityspec.json): combined API, CLI, and events workspace.
- [examples/api-service](examples/api-service/verityspec.json): focused API workspace.
- [examples/cli-tool](examples/cli-tool/verityspec.json): focused CLI workspace.
- [examples/events](examples/events/verityspec.json): focused event workspace.
- [examples/security](examples/security/verityspec.json): focused security-control workspace.
- [examples/observability](examples/observability/verityspec.json): focused observability workspace.
- [examples/accessibility](examples/accessibility/verityspec.json): focused accessibility-claim workspace.
- [examples/compliance](examples/compliance/verityspec.json): focused compliance-mapping workspace.
- [examples/broken](examples/broken/verityspec.json): intentionally broken validation demo.

## Documentation

- [Workspace format](docs/workspace-format.md)
- [Changelog](CHANGELOG.md)
- [AI agent entry point](AGENTS.md)
- [Roadmap](ROADMAP.md)
- [Record lifecycle](docs/record-lifecycle.md)
- [Packs](docs/packs.md)
- [Security pack](docs/security-pack.md)
- [Observability pack](docs/observability-pack.md)
- [Accessibility pack](docs/accessibility-pack.md)
- [Compliance pack](docs/compliance-pack.md)
- [Readiness](docs/readiness.md)
- [Generators](docs/generators.md)
- [Graph checks](docs/graph-checks.md)
- [Contract intelligence](docs/contract-intelligence.md)
- [Versioning and migrations](docs/versioning-and-migrations.md)
- [PrismSpec migration](docs/prismspec-migration.md)
- [CI](docs/ci.md)
- [Downstream CI](docs/downstream-ci.md)
- [Branching strategy](docs/branching.md)
- [PyPI publishing](docs/pypi.md)
- [Release checklist](docs/release-checklist.md)
- [v0.14.0 release notes](docs/release-notes-v0.14.0.md)
- [v0.13.0 release notes](docs/release-notes-v0.13.0.md)
- [v0.12.0 release notes](docs/release-notes-v0.12.0.md)
- [v0.11.0 release notes](docs/release-notes-v0.11.0.md)
- [v0.10.0 release notes](docs/release-notes-v0.10.0.md)
- [v0.9.0 release notes](docs/release-notes-v0.9.0.md)
- [v0.8.0 release notes](docs/release-notes-v0.8.0.md)
- [v0.7.0 release notes](docs/release-notes-v0.7.0.md)
- [v0.6.0 release notes](docs/release-notes-v0.6.0.md)
- [v0.5.0 release notes](docs/release-notes-v0.5.0.md)
- [v0.4.0 release notes](docs/release-notes-v0.4.0.md)
- [v0.3.0 release notes](docs/release-notes-v0.3.0.md)

## Supersession

PrismSpec established the initial product-specification vocabulary. VeritySpec
supersedes it with a smaller kernel, a pack-based architecture, executable
validation, readiness gates, graph analysis, diffing, generators, and migration
tooling.

PrismSpec remains the prototype. VeritySpec is the active implementation.
