# Changelog

## Unreleased

- Clarified the README distinction between package release versions and workspace format versions.
- Added AI-agent bookkeeping rules to keep README, changelog, roadmap, release notes, install instructions, and issue or milestone state aligned.
- Opened the v0.3.0 roadmap line with Sprint 13 focused on OpenAPI path parameters and generator precision.

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
