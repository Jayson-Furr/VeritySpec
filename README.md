# VeritySpec

[![CI](https://github.com/Jason-Furr/verity-spec/actions/workflows/ci.yml/badge.svg)](https://github.com/Jason-Furr/verity-spec/actions/workflows/ci.yml)
[![Release](https://img.shields.io/badge/release-v0.49.0-blue)](https://github.com/Jason-Furr/verity-spec/releases/tag/v0.49.0)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](pyproject.toml)
[![License](https://img.shields.io/github/license/Jason-Furr/verity-spec)](LICENSE)

Executable product contracts for humans, tools, and agents.

VeritySpec supersedes PrismSpec by changing the project from a broad static
schema catalog into an installable product-specification toolchain. The core
artifact is a workspace that can be validated, linted, checked for readiness,
graphed, diffed, and used to generate implementation and documentation
artifacts.

## Current Scope

Latest release: `v0.49.0`. Release history is tracked in
[CHANGELOG.md](CHANGELOG.md) and [ROADMAP.md](ROADMAP.md).

This implementation provides:

- An installable Python package with the `verity` CLI.
- A small core model: workspace, pack, schema, record, reference graph,
  validation issue, readiness gate, generator, and migration entry point.
- Built-in packs for core product records, APIs, CLIs, events, security
  controls, observability signals, accessibility claims, compliance mappings,
  deployment targets, early game product contracts, and creative game asset
  contracts, Unity, Godot, and Unreal game implementation and engine-tooling
  contracts, gameplay contracts, game content contracts, and economy
  contracts, progression contracts, spec-driven product-delivery contracts,
  mobile lifecycle contracts, live operations contracts, and implementation
  evidence contracts.
- Pack listing, validation, installed-pack discovery, and scaffolding through
  `verity pack`, including local external packs, structured generator
  metadata, and starter reference rules that make generated packs usable from
  sample workspaces immediately.
- Executable pack scaffold documentation fixtures that show a generated
  external pack plus a consuming workspace layout.
- Workspace initialization templates for basic, API, CLI, events, and security starter contracts.
- Structural validation with JSON Schema.
- Semantic validation for duplicate IDs, unknown kinds, missing references,
  disallowed relationships, deprecated references, removed references, orphan
  records, unused schemas, reference cycles, workspace spec versions, and
  nested issue locations with structured JSON location details for machine
  clients.
- Readiness gates driven by pack metadata, including conditional pack rules
  for release-blocking policy and security evidence freshness.
- Product-contract enforcement profiles for release, strict, regulated,
  public API, and internal-tool workflows.
- Generators for OpenAPI, AsyncAPI, TypeScript types, Python models, schema
  bundles, CLI reference docs, validation reports, security reports,
  observability reports, accessibility reports, compliance matrices,
  deployment reports, evidence reports, cross-pack coverage dashboards,
  product-impact reports, pack capability indexes, and roadmap governance
  reports, with OpenAPI
  path-parameter support and
  snapshot-tested type/model output including nested Python dataclasses and
  deterministic timestamp controls for generated JSON reports.
- A PrismSpec importer that produces a converted workspace and migration report.
- Workspace migration-chain planning and reporting through `verity migrate`.
- Migration dry-run fixture coverage for each supported workspace version edge.
- Fixture compatibility coverage and golden compatibility manifests across
  supported workspace format versions.
- Doctor diagnostics that can be printed to stdout or written as JSON reports.
- Downstream GitHub Actions templates and a reusable workflow for
  product-contract enforcement, including monorepo matrix checks for multiple
  workspaces with shared local packs.
- Opt-in GitHub Actions annotation output for validation, lint, and readiness
  issues in CI logs.
- Golden fixture coverage for security reports, observability report/schema
  bundle output, accessibility reports, compliance matrices, evidence reports,
  and release-review reports so generator drift is reviewed intentionally.
- README command smoke tests that execute safe local CLI examples and keep
  public command snippets from drifting.
- Release-integrity consistency checks that keep package metadata, README
  release surfaces, release notes, downstream workflow pins, release checklist
  examples, and evidence fixtures aligned with the current package version.
- A canonical AI agent entry point with shell discipline, branch/PR/release
  workflow rules, CI fallback behavior, and roadmap bookkeeping requirements.
- Public contribution guidance, issue templates, and maintainer review
  checklist for pack proposals and schema changes.
- Product-surface pack boundary guidance for future GUI, desktop, and
  additional game packs, with the first narrow game and lifecycle scopes
  delivered through
  `verity.pack.game-core`, `verity.pack.game-assets`, `verity.pack.unity`,
  `verity.pack.godot`, `verity.pack.unreal`, `verity.pack.gameplay`,
  `verity.pack.content`, `verity.pack.economy`,
  `verity.pack.progression`, `verity.pack.product-delivery`,
  `verity.pack.mobile`, `verity.pack.liveops`, and `verity.pack.evidence`.
- A product direction toward a small core runtime plus official extension pack
  packages, so specialized game, mobile, liveops, Unity, Godot, and Unreal
  packs can eventually be separated from the core package after installed-pack
  discovery, compatibility metadata, migration guidance, and non-breaking
  fixtures are in place.
- Cross-workspace dependency design guidance for future local-only workspace
  dependencies, exported records, reference resolution, and lockfiles.
- PyPI trusted-publishing readiness guidance, with GitHub release installation
  retained as the canonical public install path until publishing is enabled.

## Quick Start

Install the latest GitHub release:

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.49.0"
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
verity pack validate verity.pack.features --path docs/fixtures/pack-scaffold/packs/features
verity validate examples/basic
verity validate examples/basic --profile release --format json
verity validate tests/fixtures/custom_pack_workspace
verity validate docs/fixtures/pack-scaffold/workspace
verity validate examples/game-core
verity validate examples/game-assets
verity validate examples/unity
verity graph examples/unity
verity validate examples/godot
verity graph examples/godot
verity validate examples/unreal
verity graph examples/unreal
verity validate examples/gameplay
verity validate examples/content
verity validate examples/economy
verity validate examples/progression
verity validate examples/product-delivery
verity graph examples/product-delivery
verity validate examples/mobile
verity graph examples/mobile
verity validate examples/liveops
verity graph examples/liveops
verity validate examples/evidence
verity graph examples/evidence
verity lint examples/basic --strict
verity readiness examples/basic --strict
verity doctor examples/basic --profile public-api --format json
verity readiness examples/security --strict
verity readiness examples/observability --strict
verity readiness examples/accessibility --strict
verity readiness examples/compliance --strict
verity readiness examples/deployment --strict
verity readiness examples/game-core --strict
verity readiness examples/game-assets --strict
verity readiness examples/unity --strict
verity readiness examples/godot --strict
verity readiness examples/unreal --strict
verity readiness examples/gameplay --strict
verity readiness examples/content --strict
verity readiness examples/economy --strict
verity readiness examples/progression --strict
verity readiness examples/product-delivery --strict
verity readiness examples/mobile --strict
verity readiness examples/liveops --strict
verity readiness examples/evidence --strict
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
verity generate deployment-report examples/deployment --out build/deployment-report.json
verity generate evidence-report examples/evidence --out build/evidence-report.json
verity generate schema-bundle examples/game-core --out build/game-core-schema-bundle.json
verity generate schema-bundle examples/game-assets --out build/game-assets-schema-bundle.json
verity generate schema-bundle examples/unity --out build/unity-schema-bundle.json
verity generate schema-bundle examples/godot --out build/godot-schema-bundle.json
verity generate schema-bundle examples/unreal --out build/unreal-schema-bundle.json
verity generate schema-bundle examples/gameplay --out build/gameplay-schema-bundle.json
verity generate schema-bundle examples/content --out build/content-schema-bundle.json
verity generate schema-bundle examples/economy --out build/economy-schema-bundle.json
verity generate schema-bundle examples/progression --out build/progression-schema-bundle.json
verity generate schema-bundle examples/product-delivery --out build/product-delivery-schema-bundle.json
verity generate schema-bundle examples/mobile --out build/mobile-schema-bundle.json
verity generate schema-bundle examples/liveops --out build/liveops-schema-bundle.json
verity generate schema-bundle examples/evidence --out build/evidence-schema-bundle.json
verity generate coverage-dashboard tests/fixtures/cross_pack_coverage --out build/coverage-dashboard.json
verity generate pack-capability-index tests/fixtures/custom_pack_workspace --out build/pack-capability-index.json
verity generate schema-bundle docs/fixtures/pack-scaffold/workspace --out build/pack-scaffold-schema-bundle.json
verity generate pack-capability-index docs/fixtures/pack-scaffold/workspace --out build/pack-scaffold-capability-index.json
verity generate product-impact tests/fixtures/product_impact/baseline tests/fixtures/product_impact/current --out build/product-impact.json
verity generate roadmap-report . --out build/roadmap-report.json
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
verity validate examples/basic --github-annotations
verity readiness examples/basic --strict --github-annotations
verity doctor examples/basic --format json
verity doctor examples/basic --profile public-api --format json
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
verity generate deployment-report examples/deployment --out build/deployment-report.json
verity generate evidence-report examples/evidence --out build/evidence-report.json
verity generate schema-bundle examples/game-core --out build/game-core-schema-bundle.json
verity generate schema-bundle examples/game-assets --out build/game-assets-schema-bundle.json
verity generate schema-bundle examples/unity --out build/unity-schema-bundle.json
verity generate schema-bundle examples/godot --out build/godot-schema-bundle.json
verity generate schema-bundle examples/unreal --out build/unreal-schema-bundle.json
verity generate schema-bundle examples/gameplay --out build/gameplay-schema-bundle.json
verity generate schema-bundle examples/content --out build/content-schema-bundle.json
verity generate schema-bundle examples/economy --out build/economy-schema-bundle.json
verity generate schema-bundle examples/progression --out build/progression-schema-bundle.json
verity generate schema-bundle examples/product-delivery --out build/product-delivery-schema-bundle.json
verity generate schema-bundle examples/mobile --out build/mobile-schema-bundle.json
verity generate schema-bundle examples/liveops --out build/liveops-schema-bundle.json
verity generate schema-bundle examples/evidence --out build/evidence-schema-bundle.json
verity generate coverage-dashboard tests/fixtures/cross_pack_coverage --out build/coverage-dashboard.json
verity generate pack-capability-index tests/fixtures/custom_pack_workspace --out build/pack-capability-index.json
verity generate pack-capability-index docs/fixtures/pack-scaffold/workspace --out build/pack-scaffold-capability-index.json
verity generate product-impact tests/fixtures/product_impact/baseline tests/fixtures/product_impact/current --out build/product-impact.json
verity generate roadmap-report . --out build/roadmap-report.json
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
verity pack validate verity.pack.features --path docs/fixtures/pack-scaffold/packs/features
```

See [docs/packs.md](docs/packs.md) for the pack manifest contract and pack
standard, including the generated `product` to starter-kind `uses` reference
rule for sample workspaces.
See [docs/pack-scaffold-fixtures.md](docs/pack-scaffold-fixtures.md) for a
complete generated pack and consuming workspace fixture.

Run tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Workspace Shape

Package releases and workspace format versions are intentionally separate.
VeritySpec package `v0.49.0` supports workspace formats `v0.1.0` and
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
- [examples/deployment](examples/deployment/verityspec.json): focused deployment target workspace.
- [examples/game-core](examples/game-core/verityspec.json): focused game product-contract workspace.
- [examples/game-assets](examples/game-assets/verityspec.json): focused game creative-source workspace.
- [examples/unity](examples/unity/verityspec.json): focused Unity game implementation and engine-tooling workspace.
- [examples/godot](examples/godot/verityspec.json): focused Godot game implementation and engine-tooling workspace.
- [examples/unreal](examples/unreal/verityspec.json): focused Unreal game implementation and engine-tooling workspace.
- [examples/gameplay](examples/gameplay/verityspec.json): focused gameplay mechanic and encounter workspace.
- [examples/content](examples/content/verityspec.json): focused game content manifest workspace.
- [examples/economy](examples/economy/verityspec.json): focused game economy workspace.
- [examples/progression](examples/progression/verityspec.json): focused game progression workspace.
- [examples/product-delivery](examples/product-delivery/verityspec.json): focused spec-driven product-delivery workspace.
- [examples/mobile](examples/mobile/verityspec.json): focused mobile lifecycle workspace.
- [examples/liveops](examples/liveops/verityspec.json): focused live operations workspace.
- [examples/evidence](examples/evidence/verityspec.json): focused implementation evidence workspace.
- [examples/broken](examples/broken/verityspec.json): intentionally broken validation demo.

## Documentation

- [Workspace format](docs/workspace-format.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [AI agent entry point](AGENTS.md)
- [Roadmap](ROADMAP.md)
- [Record lifecycle](docs/record-lifecycle.md)
- [Packs](docs/packs.md)
- [External pack maintainer review checklist](docs/external-pack-review-checklist.md)
- [Pack scaffold fixtures](docs/pack-scaffold-fixtures.md)
- [Product surface pack boundaries](docs/product-surface-pack-boundaries.md)
- [Engine and product-delivery pack direction](docs/engine-product-delivery-packs.md)
- [Specialized pack separation plan](docs/specialized-pack-separation.md)
- [Cross-workspace dependencies](docs/cross-workspace-dependencies.md)
- [Product contract profiles](docs/product-contract-profiles.md)
- [Security pack](docs/security-pack.md)
- [Observability pack](docs/observability-pack.md)
- [Accessibility pack](docs/accessibility-pack.md)
- [Compliance pack](docs/compliance-pack.md)
- [Deployment pack](docs/deployment-pack.md)
- [Game core pack](docs/game-core-pack.md)
- [Game assets pack](docs/game-assets-pack.md)
- [Unity pack](docs/unity-pack.md)
- [Godot pack](docs/godot-pack.md)
- [Unreal pack](docs/unreal-pack.md)
- [Gameplay pack](docs/gameplay-pack.md)
- [Content pack](docs/content-pack.md)
- [Economy pack](docs/economy-pack.md)
- [Progression pack](docs/progression-pack.md)
- [Product delivery pack](docs/product-delivery-pack.md)
- [Mobile pack](docs/mobile-pack.md)
- [LiveOps pack](docs/liveops-pack.md)
- [Evidence pack](docs/evidence-pack.md)
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
- [Release integrity checks](docs/release-integrity.md)
- [v0.49.0 release notes](docs/release-notes-v0.49.0.md)
- [v0.48.0 release notes](docs/release-notes-v0.48.0.md)
- [v0.47.0 release notes](docs/release-notes-v0.47.0.md)
- [v0.46.0 release notes](docs/release-notes-v0.46.0.md)
- [v0.45.0 release notes](docs/release-notes-v0.45.0.md)
- [v0.44.0 release notes](docs/release-notes-v0.44.0.md)
- [v0.43.0 release notes](docs/release-notes-v0.43.0.md)
- [v0.42.0 release notes](docs/release-notes-v0.42.0.md)
- [v0.41.0 release notes](docs/release-notes-v0.41.0.md)
- [v0.40.0 release notes](docs/release-notes-v0.40.0.md)
- [v0.39.0 release notes](docs/release-notes-v0.39.0.md)
- [v0.38.0 release notes](docs/release-notes-v0.38.0.md)
- [v0.37.0 release notes](docs/release-notes-v0.37.0.md)
- [v0.36.0 release notes](docs/release-notes-v0.36.0.md)
- [v0.35.0 release notes](docs/release-notes-v0.35.0.md)
- [v0.34.0 release notes](docs/release-notes-v0.34.0.md)
- [v0.33.0 release notes](docs/release-notes-v0.33.0.md)
- [v0.32.0 release notes](docs/release-notes-v0.32.0.md)
- [v0.31.0 release notes](docs/release-notes-v0.31.0.md)
- [v0.30.0 release notes](docs/release-notes-v0.30.0.md)
- [v0.29.0 release notes](docs/release-notes-v0.29.0.md)
- [v0.28.0 release notes](docs/release-notes-v0.28.0.md)
- [v0.27.0 release notes](docs/release-notes-v0.27.0.md)
- [v0.26.0 release notes](docs/release-notes-v0.26.0.md)
- [v0.25.0 release notes](docs/release-notes-v0.25.0.md)
- [v0.24.0 release notes](docs/release-notes-v0.24.0.md)
- [v0.23.0 release notes](docs/release-notes-v0.23.0.md)
- [v0.22.0 release notes](docs/release-notes-v0.22.0.md)
- [v0.21.0 release notes](docs/release-notes-v0.21.0.md)
- [v0.20.0 release notes](docs/release-notes-v0.20.0.md)
- [v0.19.0 release notes](docs/release-notes-v0.19.0.md)
- [v0.18.0 release notes](docs/release-notes-v0.18.0.md)
- [v0.17.0 release notes](docs/release-notes-v0.17.0.md)
- [v0.16.0 release notes](docs/release-notes-v0.16.0.md)
- [v0.15.0 release notes](docs/release-notes-v0.15.0.md)
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
