# Changelog

## Unreleased

## 0.77.0

- Added downstream AI-adapter drift-check guidance for sibling repositories
  that keep agent-specific Codex, Claude, ChatGPT, Gemini, Copilot, Unity AI,
  or other adapter files, including an audit checklist anchored to the
  organization AI entry-point baseline.
- Added v0.77.0 release notes and roadmap closeout.

## 0.76.0

- Added `verity generate decision-index` with JSON and Markdown output for
  product-delivery `decision.record` governance and ADR review, including
  graph-link summaries, index-gap reporting, CLI coverage, and golden
  fixtures.
- Added v0.76.0 release notes and roadmap closeout.

## 0.75.0

- Added the first Markdown `verity generate agent-context` prototype for
  product-delivery and engine agent-context exporter records, including
  validation preflight behavior, graph-linked record selection, safety
  boundaries, verification commands, CLI coverage, and a golden Markdown
  fixture.
- Added v0.75.0 release notes and roadmap closeout.

## 0.74.0

- Added Markdown output for `verity generate issue-code-catalog` so
  documentation sites and maintainers can publish stable issue-code metadata
  without hand-converting the JSON catalog.
- Added v0.74.0 release notes and roadmap closeout.

## 0.73.0

- Added parity-aware `device-smoke` validation-runner support for Unity, Godot,
  and Unreal so built artifact/runtime smoke checks can omit scanner records
  while normal scanner-backed runners still require `scannerRefs`.
- Added runtime validation graph links and evidence rules so device-smoke
  runners can prove Unity build targets, Godot export presets, and Unreal
  targets through `evidence.test`.
- Clarified that organization AI-agent entry-point baseline requirements must
  live in active entry points, not conversation history or agent-specific
  adapters.
- Added v0.73.0 release notes and roadmap closeout.

## 0.72.0

- Added a documented migration-report JSON Schema for `verity migrate` outputs
  so CI integrations can validate migration paths, impact summaries, changes,
  files written, manual follow-up, and blocked migration reports.
- Aligned the canonical AI-agent entry point with the organization-wide
  entry-point baseline for all agents.
- Added v0.72.0 release notes and roadmap closeout.

## 0.71.0

- Added parity-aware evidence reference rules so `evidence.test` can directly
  prove Unity project and scene records, Godot project and scene records, and
  Unreal project and map records.
- Added build evidence reference rules for Unity build targets, Godot export
  presets, and Unreal targets, plus executable engine examples that link
  validation runners to test evidence and build evidence to concrete
  build/export targets.
- Added v0.71.0 release notes and roadmap closeout.

## 0.70.0

- Added Markdown output for `verity generate security-report` so release
  reviewers can inspect security-control summaries, release gaps, and
  verification details as a human-readable artifact while preserving the
  existing JSON security-report contract.
- Added security-report Markdown golden fixture, CLI coverage, security pack
  generator metadata, CI/release checklist command coverage, and documentation
  for the JSON-versus-Markdown contract boundary.
- Added canonical AI-agent feedback-loop guidance and clean-on-main open-issue
  sweep guidance to reduce drift across agent-managed work.
- Added v0.70.0 release notes and roadmap closeout.

## 0.69.0

- Added a post-tag release verification checklist that records GitHub release
  asset hashes, skipped PyPI publish review, downloaded wheel smoke checks,
  public GitHub tag install smoke checks, milestone closure, and agent context
  refresh evidence.
- Added v0.69.0 release notes and roadmap closeout.

## 0.68.0

- Added an installed-pack compatibility metadata design note that defines
  supported VeritySpec version ranges, workspace format support, pack API
  levels, official extension-package lifecycle states, staged adoption, and
  no-runtime-enforcement guardrails.
- Added v0.68.0 release notes and roadmap closeout.

## 0.67.0

- Added a CLI command module decomposition design note that defines staged
  `verityspec.commands` boundaries, shared helper ownership, migration phases,
  and compatibility guardrails before larger command families expand the CLI.
- Added v0.67.0 release notes and roadmap closeout.

## 0.66.0

- Added `verity pack compare` for official-extension mirror fixture checks
  that compare manifest identity, schema declarations, schema JSON content,
  readiness gates, reference rules, and generator metadata without loading the
  mirror into the active pack registry.
- Added the first official-extension mirror fixture guidance and Unity mirror
  fixture for future `verityspec-pack-unity` compatibility checks before any
  bundled-pack detach work begins.
- Added v0.66.0 release notes and roadmap closeout.

## 0.65.0

- Added `verity pack doctor` for non-throwing installed and local pack
  discovery diagnostics, including entry-point load failures, duplicate pack
  IDs, built-in collisions, and explicit local override warnings.
- Added v0.65.0 release notes and roadmap closeout.

## 0.64.0

- Added `verity generate lifecycle-readiness-report` for product-delivery,
  mobile, and liveops lifecycle gap summaries, plus an executable
  `examples/lifecycle-readiness` workspace and golden report coverage.
- Added v0.64.0 release notes and roadmap closeout.

## 0.63.0

- Added engine portfolio compatibility fixtures and documentation that validate
  Unity, Godot, Unreal, and shared exported game-core workspaces side by side
  through local readonly workspace dependencies before aggregate portfolio
  reporting is implemented.
- Added v0.63.0 release notes and roadmap closeout.

## 0.62.0

- Added a local-only workspace dependency prototype with direct readonly
  dependency declarations, dependency aliases, manifest-level exported
  records, alias-qualified reference validation, dependency-aware graph output,
  smoke fixtures, stable issue codes, and docs.
- Added v0.62.0 release notes and roadmap closeout.

## 0.61.0

- Added Markdown output for `verity generate coverage-dashboard` so
  maintainers can review cross-pack product-surface coverage as a
  human-readable release-review artifact while preserving the existing JSON
  contract.
- Added v0.61.0 release notes and roadmap closeout.

## 0.60.0

- Added deployment-target release evidence links that connect production
  deployment targets to security controls, observability dashboards,
  compliance mappings, and release evidence records with readiness,
  validation, graph, report, example, and fixture coverage.
- Added v0.60.0 release notes and roadmap closeout.

## 0.59.0

- Added profile-aware downstream CI workflow support and maintained template
  examples for release, regulated, public API, and internal-tool workspaces.
- Added v0.59.0 release notes and roadmap closeout.

## 0.58.0

- Added fixture refresh guidance for deterministic golden report regeneration,
  intentional output drift review, release-version fixture updates, and
  maintainer checklist coverage.
- Added v0.58.0 release notes and roadmap closeout.

## 0.57.0

- Added portfolio-level validation foundation guidance and an executable
  `examples/portfolio` workspace for local-only multi-workspace portfolio
  planning before aggregate reports or workspace dependency resolution.
- Added organization-wide agent reuse, work-ledger, and content-opportunity
  guidance to the canonical AI agent entry point.
- Added v0.57.0 release notes and roadmap closeout.

## 0.56.0

- Added engine full-lifecycle support design guidance for Unity, Godot,
  Unreal, shared engine library workspaces, lifecycle readiness profiles,
  evidence, liveops, decommissioning, archive records, and portfolio examples.
- Added v0.56.0 release notes and roadmap closeout.

## 0.55.0

- Added agent-context generation design guidance, architecture decision record
  docs and template, and executable AI-agent adapter drift checks.
- Added v0.55.0 release notes and roadmap closeout.

## 0.54.0

- Added machine-readable issue-code catalog generation from `verity explain`
  metadata for documentation sites and CI integrations.
- Updated future sprint planning guidance to use cohesive bundles sized up to
  roughly two weeks of development effort.
- Added v0.54.0 release notes and roadmap closeout.

## 0.53.0

- Added workspace migration impact summaries to `verity migrate --list` and
  migration reports so format upgrades call out workspace-format, record, pack,
  and generator behavior affected by the planned migration path.
- Added v0.53.0 release notes and roadmap closeout.

## 0.52.0

- Added security-report release-gap summaries for stale evidence and missing
  verification dates while preserving existing verification coverage output.
- Added v0.52.0 release notes and roadmap closeout.

## 0.51.0

- Added Markdown output for `verity generate roadmap-report` so maintainers
  can create human-readable release-governance summaries from `ROADMAP.md`.
- Added v0.51.0 release notes and roadmap closeout.

## 0.50.0

- Added release-integrity consistency tests and documentation that keep package
  metadata, README release surfaces, release notes, downstream pins, release
  checklist examples, and evidence fixtures aligned with `__version__`.
- Added v0.50.0 release notes and roadmap closeout.

## 0.49.0

- Added an external pack maintainer review checklist that defines proposal
  inputs, identity, contract, executability, documentation, compatibility, PR
  review, and acceptance-outcome gates for public pack proposals.
- Added v0.49.0 release notes and roadmap closeout.

## 0.48.0

- Added golden fixtures and generator-level golden comparisons for
  accessibility report and compliance matrix outputs so those report contracts
  detect unintended drift.

## 0.47.0

- Added a specialized-pack separation plan that defines candidate official
  extension package names, compatibility metadata, staged detach gates,
  migration guidance, rollback criteria, and no-immediate-removal guardrails
  for game, mobile, liveops, Unity, Godot, and Unreal packs.

## 0.46.0

- Added installed-pack discovery through the `verityspec.packs` Python
  entry-point group so separately installed extension packs can be loaded by
  pack ID without manual `packPaths`, while preserving built-in packs and
  explicit local pack path precedence.

## 0.45.0

- Updated repository owner/name references after moving the canonical public
  repository to `Jason-Furr/verity-spec`, including README badges, GitHub
  install URLs, downstream workflow templates, PyPI trusted-publishing notes,
  evidence fixtures, and release-note install snippets.
- Added roadmap, README, and pack documentation guidance that makes
  specialized pack separation an explicit product goal: `verityspec` should
  remain the core contract runtime while domain-heavy game, mobile, liveops,
  Unity, Godot, and Unreal packs can eventually become official extension
  packages after installed-pack discovery, compatibility metadata, migration
  guidance, and non-breaking fixtures are in place.
- Added built-in `verity.pack.progression` with `progression.xp-model`,
  `progression.level`, `progression.unlock`, `progression.track`, and
  `progression.gate` records, readiness gates, reference rules, executable
  progression examples, graph coverage, schema-bundle coverage,
  coverage-dashboard support, CI coverage, and public docs for game
  progression contracts.
- Added built-in `verity.pack.evidence` with `evidence.test`,
  `evidence.ci-run`, `evidence.build`, `evidence.review`,
  `evidence.screenshot`, `evidence.video`, `evidence.qa`,
  `evidence.playtest`, `evidence.certification-checklist`, and
  `evidence.artifact` records, readiness gates, reference rules, executable
  evidence examples, graph coverage, schema-bundle coverage,
  coverage-dashboard support, CI coverage, public docs, and
  `verity generate evidence-report`.
- Added explicit Unity, Godot, and Unreal reference-rule parity for engine
  validation runners and readiness dashboards that produce or report evidence,
  plus engine project relationships for implementing progression tracks.

## 0.44.0

- Added built-in `verity.pack.mobile` with `mobile.app-release`,
  `mobile.store-listing`, `mobile.privacy-policy`,
  `mobile.apple-privacy-details`, `mobile.google-play-data-safety`,
  `mobile.att-consent`, `mobile.sdk-inventory`,
  `mobile.monetization-posture`, `mobile.entitlement`,
  `mobile.soft-launch`, `mobile.launch-candidate`, and
  `mobile.compatibility-matrix` records, readiness gates, reference rules,
  executable mobile examples, graph coverage, schema-bundle coverage,
  coverage-dashboard support, CI coverage, and public docs for mobile
  lifecycle contracts.
- Added built-in `verity.pack.liveops` with `liveops.config`,
  `liveops.remote-config`, `liveops.rollback-plan`,
  `liveops.analytics-taxonomy`, `liveops.support-category`,
  `liveops.save-migration-policy`, `liveops.decommission-plan`,
  `liveops.data-deletion-policy`, and `liveops.archive-handling` records,
  readiness gates, reference rules, executable liveops examples, graph
  coverage, schema-bundle coverage, coverage-dashboard support, CI coverage,
  and public docs for live operations contracts.
- Added explicit Unity, Godot, and Unreal reference-rule parity for mobile
  release and liveops config relationships.
- Added v0.44.0 release notes and roadmap closeout.

## 0.43.0

- Added built-in `verity.pack.product-delivery` with `product.scope`,
  `commercial.posture`, `project-management.model`, `decision.record`,
  `readiness.profile`, `evidence.requirement`, `release.process`,
  `operations.model`, `support.policy`, `maintenance.policy`,
  `archive.policy`, `decommission.policy`, `scanner.capability`,
  `generator.capability`, `validation.runner`, `editor.surface`, and
  `agent-context.exporter` records, readiness gates, reference rules, an
  executable product-delivery example, graph coverage, schema-bundle coverage,
  coverage-dashboard support, CI coverage, and public docs for spec-driven
  product-delivery repositories.
- Added v0.43.0 release notes and roadmap closeout.

## 0.42.0

- Added built-in `verity.pack.unreal` with `unreal.project`,
  `unreal.plugin`, `unreal.module`, `unreal.target`, `unreal.map`,
  `unreal.blueprint`, `unreal.data-asset`, `unreal.gameplay-tag`,
  `unreal.input-action`, `unreal.scanner`, `unreal.validation-runner`,
  `unreal.readiness-dashboard`, and `unreal.agent-context-exporter` records,
  readiness gates, reference rules, an executable Unreal game workspace
  example, graph coverage, schema-bundle coverage, and public docs for Unreal
  game implementation and engine-tooling contracts.
- Added v0.42.0 release notes and roadmap closeout.

## 0.41.0

- Added built-in `verity.pack.godot` with `godot.project`, `godot.addon`,
  `godot.shared-library`, `godot.scene`, `godot.node-contract`,
  `godot.resource`, `godot.script`, `godot.autoload`, `godot.input-action`,
  `godot.export-preset`, `godot.scanner`, `godot.validation-runner`,
  `godot.readiness-dashboard`, and `godot.agent-context-exporter` records,
  readiness gates, reference rules, an executable Godot game workspace
  example, graph coverage, schema-bundle coverage, and public docs for Godot
  game implementation and engine-tooling contracts.
- Added v0.41.0 release notes and roadmap closeout.

## 0.40.0

- Expanded built-in `verity.pack.unity` with `unity.package`,
  `unity.shared-library`, `unity.prefab`, `unity.asmdef`, `unity.scanner`,
  `unity.validation-runner`, `unity.readiness-dashboard`, and
  `unity.agent-context-exporter` records, readiness gates, reference rules,
  expanded executable Unity example, graph coverage, and public docs for Unity
  implementation and engine-tooling contracts.
- Added v0.40.0 release notes and roadmap closeout.

## 0.39.0

- Added built-in `verity.pack.economy` with `economy.currency`,
  `economy.source`, `economy.sink`, `economy.reward`, and `economy.offer`
  records, readiness gates, graph reference rules, an executable economy
  example, coverage-dashboard support, schema-bundle generation coverage, and
  public docs for economy implementation contracts.
- Added v0.39.0 release notes and roadmap closeout.

## 0.38.0

- Added built-in `verity.pack.gameplay` with `game.mechanic`,
  `game.ability`, `game.rule`, and `game.encounter` records, readiness gates,
  graph reference rules, an executable gameplay example, coverage-dashboard
  support, schema-bundle generation coverage, and public docs for gameplay
  implementation contracts.
- Added built-in `verity.pack.content` with `game.content-item`, `game.level`,
  `game.loot-table`, and `game.content-manifest` records, readiness gates,
  graph reference rules, an executable content example, coverage-dashboard
  support, schema-bundle generation coverage, and public docs for content
  implementation contracts.
- Added v0.38.0 release notes and roadmap closeout.

## 0.37.0

- Added built-in `verity.pack.unity` with `unity.project`,
  `unity.package-dependency`, `unity.scene`, and `unity.build-target` records,
  readiness gates, graph reference rules, an executable Unity example,
  coverage-dashboard support, schema-bundle generation coverage, and public
  docs for Unity implementation contracts.
- Added v0.37.0 release notes and roadmap closeout.

## 0.36.0

- Added built-in `verity.pack.game-assets` with `game.gdd-source`,
  `game.visual-identity`, `game.identity-image`, and `game.concept-art`
  records, readiness gates, graph reference rules, an executable game-assets
  example, coverage-dashboard support, schema-bundle generation coverage, and
  public docs for creative-source game contracts.
- Added v0.36.0 release notes and roadmap closeout.

## 0.35.0

- Added built-in `verity.pack.game-core` with `game.product`, `game.mode`,
  `game.loop`, and `game.prototype-scope` records, readiness gates, graph
  reference rules, an executable game-core example, coverage-dashboard support,
  and schema-bundle generation coverage.
- Added v0.35.0 release notes and roadmap closeout.

## 0.34.0

- Added a maintained downstream CI template for monorepos with multiple
  VeritySpec workspaces and shared local packs.
- Added v0.34.0 release notes and roadmap closeout.

## 0.33.0

- Added executable pack scaffold documentation fixtures showing a generated
  external pack and a consuming workspace layout for external pack authors.
- Added v0.33.0 release notes and roadmap closeout.

## 0.32.0

- Added `verity generate pack-capability-index` for registry reports that
  summarize loaded built-in and external pack schemas, readiness gates,
  reference rules, and generator metadata.
- Added v0.32.0 release notes and roadmap closeout.

## 0.31.0

- Added cross-workspace dependency design guidance for future local-only
  workspace dependencies, exported records, reference resolution, and
  lockfiles.
- Added v0.31.0 release notes and roadmap closeout.

## 0.30.0

- Added `verity generate product-impact` for release-review reports that
  compare two workspaces, classify changed records, and expand upstream and
  downstream reference-graph impact.
- Added v0.30.0 release notes and roadmap closeout.

## 0.29.0

- Added `verity generate coverage-dashboard` for cross-pack product-surface
  coverage summaries across API, CLI, events, security, accessibility,
  observability, compliance, and deployment records.
- Added v0.29.0 release notes and roadmap closeout.

## 0.28.0

- Added the first deployment-target pack with runtime and deployment target
  schemas, production readiness controls, an executable deployment example,
  and deployment report generation.
- Added v0.28.0 release notes and roadmap closeout.

## 0.27.0

- Added product-contract enforcement profiles for release, strict, regulated,
  public API, and internal-tool workflows.
- Added v0.27.0 release notes and roadmap closeout.

## 0.26.0

- Added product-surface pack boundary guidance for future GUI, desktop, mobile,
  and game packs before first schemas are introduced.
- Added v0.26.0 release notes and roadmap closeout.

## 0.25.0

- Added `--generated-at` for deterministic JSON report timestamps and golden
  snapshot regeneration.
- Added v0.25.0 release notes and roadmap closeout.

## 0.24.0

- Added observability report and schema-bundle golden fixtures for stable
  generator contract review.
- Added v0.24.0 release notes and roadmap closeout.

## 0.23.0

- Added opt-in GitHub Actions annotation output for validation, lint, and
  readiness issues.
- Added v0.23.0 release notes and roadmap closeout.

## 0.22.0

- Added README command smoke tests that execute safe local CLI examples with
  temporary output paths and explicit install/setup skips.
- Added v0.22.0 release notes and roadmap closeout.

## 0.21.0

- Added structured issue `locationDetails` fields for JSON diagnostics while
  preserving formatted `location` strings.
- Added v0.21.0 release notes and roadmap closeout.

## 0.20.0

- Added golden workspace compatibility manifests for supported workspace
  format coverage.
- Added v0.20.0 release notes and roadmap closeout.

## 0.19.0

- Added security-control evidence freshness readiness checks based on
  `verification.lastVerified` and `verification.reviewCadenceDays`.
- Added v0.19.0 release notes and roadmap closeout.

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
