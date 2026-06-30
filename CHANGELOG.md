# Changelog

## Unreleased

- Added security-control evidence freshness readiness checks based on
  `verification.lastVerified` and `verification.reviewCadenceDays`.

## 0.18.0

- Added `verity generate roadmap-report` for JSON roadmap governance reports
  covering milestones, sprint status, and Next 20 planning points.
- Added v0.18.0 release notes and roadmap closeout.

## 0.17.0

- Added PyPI trusted-publishing readiness guidance, explicit publishing
  decision notes, and tests that keep PyPI fallback install docs aligned with
  the current release tag.
- Added v0.17.0 release notes and roadmap closeout.

## 0.16.0

- Added public contribution guidance for pack proposals, schema changes,
  issue templates, and contribution workflow expectations.
- Added v0.16.0 release notes and roadmap closeout.

## 0.15.0

- Added golden security-report fixtures and unit/CLI snapshot coverage for the
  `examples/security` report shape.
- Documented the required AI operating loop for sprint work, release prep,
  PR verification, main verification, release tagging, and roadmap upkeep.
- Added v0.15.0 release notes and roadmap closeout.

## 0.14.0

- Added maintained downstream GitHub Actions templates for reusable-workflow,
  local-pack, and direct-install product-contract checks.
- Added tests that keep downstream template and reusable-workflow release tags
  aligned with the package version.
- Added v0.14.0 release notes and roadmap closeout.

## 0.13.0

- Added pack authoring coverage proving `verity pack init` scaffolds can be
  loaded by a sample workspace for validation, strict linting, strict
  readiness, and schema-bundle generation.
- Updated `verity pack init` scaffolds to include a starter `product` to
  generated-kind `uses` reference rule.
- Added release badge bookkeeping to the AI-agent entry point and release
  checklist so README release updates include the visible badge.
- Added v0.13.0 release notes and roadmap closeout.

## 0.12.0

- Added structured generator metadata in pack manifests while preserving legacy
  string generator declarations.
- Added v0.12.0 release notes and roadmap closeout.

## 0.11.0

- Added migration dry-run fixtures and tests for each supported workspace
  version edge.
- Added v0.11.0 release notes and roadmap closeout.

## 0.10.0

- Improved `verity diff` JSON and text output with machine-readable change
  severity, breaking-change classification, and summary counts.
- Added v0.10.0 release notes and roadmap closeout.

## 0.9.0

- Added built-in `verity.pack.compliance` with `compliance.mapping` records,
  readiness gates, reference rules, documentation, CI coverage, and an
  executable compliance example.
- Added `verity generate compliance-matrix` for compliance mapping,
  framework, verification, evidence, target, and release-gap summaries.
- Added v0.9.0 release notes and roadmap closeout.

## 0.8.0

- Added built-in `verity.pack.accessibility` with `accessibility.claim`
  records, readiness gates, reference rules, documentation, CI coverage, and
  an executable accessibility example.
- Added `verity generate accessibility-report` for accessibility claim,
  ownership, verification, impact, and release-gap summaries.
- Added v0.8.0 release notes and roadmap closeout.

## 0.7.0

- Added `verity doctor --report-out` for writing structured diagnostics to a
  JSON file while preserving normal stdout output.
- Added `verity init --template` starter workspaces for basic, API, CLI,
  events, and security contracts.
- Added built-in `verity.pack.observability` with telemetry, metric,
  dashboard, and alert records plus an executable observability example.
- Added `verity generate observability-report` for observability signal,
  ownership, severity, and release-gap summaries.
- Added v0.7.0 release notes and roadmap closeout.

## 0.6.0

- Added conditional readiness rules to pack manifests.
- Added security readiness hardening so critical unverified
  `security.control` records emit `security.control.critical_unverified`.
- Added a fixture compatibility matrix across supported workspace spec
  versions.
- Improved nested issue locations for schema, readiness, and reference errors.
- Added v0.6.0 release notes and roadmap closeout.

## 0.5.0

- Added built-in `verity.pack.security` with `security.control` records,
  readiness gates, reference rules, and an executable security example.
- Added `verity generate security-report` for JSON summaries of security
  controls, coverage, risk levels, verification state, and target records.
- Added the next 20 roadmap points for future fixes, improvements,
  continuation work, and project expansion.
- Added an AI-agent rule requiring up to 20 future roadmap points when the
  active roadmap is caught up.
- Added v0.5.0 release notes and roadmap closeout.

## 0.4.0

- Added workspace format `v0.2.0` with explicit `packPaths` declarations.
- Added migration-chain planning for `legacy -> v0.1.0 -> v0.2.0`.
- Added `verity migrate --list` to inspect supported workspace versions and migration steps.
- Kept `v0.1.0` workspaces supported while making `v0.2.0` the current format for new examples and workspaces.
- Added v0.4.0 release notes and roadmap closeout.

## 0.3.0

- Added OpenAPI path-parameter inference, explicit endpoint parameter emission, and OpenAPI golden output coverage.
- Added Python nested dataclass generation for inline object schemas and inline object array items.
- Added `verity pack init` for creating validating starter pack scaffolds.
- Added AI-agent bookkeeping rules to keep README, changelog, roadmap, release notes, install instructions, and issue or milestone state aligned.
- Added AI-agent fallback guidance for local verification when GitHub Actions is unavailable for billing, credit, quota, or runner reasons.
- Added a repository branching strategy and AI-agent requirements for branch selection and merge discipline.
- Clarified the README distinction between package release versions and workspace format versions.
- Removed PyPI-dependent README badges until the `verityspec` PyPI project is published.
- Added v0.3.0 release notes and roadmap closeout.

## 0.2.0

- Added Sprint 6 public package polish: README badges, install guidance, PyPI setup docs, and GitHub `pypi` environment preparation.
- Added Sprint 7 contract intelligence: `doctor`, `explain`, `--fail-on`, graph filters, richer validation report metadata, and CI coverage.
- Added Sprint 8 PrismSpec migration: richer PrismSpec import mappings, migration report fields, fixture coverage, migration docs, and CI smoke testing.
- Added Sprint 9 versioning and migrations: supported spec-version registry, workspace version validation issues, `verity migrate`, version-aware diff metadata, migration docs, and CI coverage.
- Added Sprint 10 external pack loading: workspace `packPaths`, `--pack-path` CLI flags, external pack list/validate support, custom pack fixtures, docs, and CI coverage.
- Added Sprint 11 generator maturity: richer OpenAPI and AsyncAPI metadata, improved TypeScript and Python type/model generation, generator maturity fixtures, golden snapshot tests, docs, and CI coverage.
- Added Sprint 12 release productization: downstream CI workflow guidance, Node 24-compatible GitHub Actions pins, v0.2.0 release notes, canonical AI-agent entry point, and final release checks.

## 0.1.0

- Initial VeritySpec CLI and Python package.
- Added executable workspace validation, linting, readiness checks, graph output, diffing, generators, and PrismSpec import reporting.
- Added built-in core, API, CLI, and events packs.
- Added executable `examples/basic` workspace and focused tests.
- Added Sprint 1 CLI contract behavior: `verity --version`, JSON output for contract-checking commands, stable exit codes, and subprocess-based CLI tests.
- Added Sprint 2 contract semantics: shared record envelope assertions, pack-declared reference rules, graph checks, semantic broken fixtures, and validation-report generation.
- Added Sprint 3 pack system foundation: pack manifest schema, `verity pack list`, `verity pack validate`, pack validation tests, and pack-standard docs.
- Added Sprint 4 examples and documentation: focused API, CLI, events, and broken workspaces plus docs for workspace format, lifecycle, readiness, generators, graph checks, and CI.
- Added Sprint 5 release automation: package build checks, tag-driven GitHub releases, PyPI publishing preparation, and release checklist.
