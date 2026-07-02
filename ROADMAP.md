# VeritySpec Sprint Roadmap

VeritySpec matures through shippable sprints. Plan sprints as cohesive bundles
of related work sized up to roughly two weeks of development effort, while
still leaving the repository in a releasable state with tests, examples,
documentation, and CI checks updated alongside code.

The GitHub issues and milestones are the operational roadmap. This file is the
repository-level summary.

## Completed Foundation

| Sprint | Status | Focus |
|---:|---|---|
| 1 | Complete | CLI contract, version output, JSON output, stable exit codes |
| 2 | Complete | Semantic validation, reference rules, graph checks, validation reports |
| 3 | Complete | Pack manifests, pack listing, pack validation |
| 4 | Complete | Executable examples and core documentation |
| 5 | Complete | Release automation, package build checks, GitHub release workflow |
| 6 | Complete | Public package polish, badges, install guidance, PyPI preparation |
| 7 | Complete | Contract intelligence: `doctor`, `explain`, graph filters, `--fail-on` |
| 8 | Complete | PrismSpec import bridge and migration reports |

## v0.2.0

The `v0.2.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 9 | Complete | Version registry, workspace version validation, `verity migrate`, version-aware diffing |
| 10 | Complete | External pack loading through workspace `packPaths` and CLI `--pack-path` flags |
| 11 | Complete | Generator maturity, richer OpenAPI/AsyncAPI metadata, golden type/model snapshots |
| 12 | Complete | CI productization, release notes, action warning cleanup, v0.2.0 release readiness |

## Sprint 12 Priorities

Sprint 12 should finish the `v0.2.0` line by making VeritySpec easier to adopt
from downstream repositories:

- Add a reusable or copy-paste CI workflow for product-contract checks.
- Add a canonical AI-agent entry point for coding agents.
- Add a post-commit context refresh rule for AI agents.
- Add shell-discipline guidance for `zsh`, `bash`, and PowerShell command use.
- Add v0.2.0 release notes.
- Review GitHub Actions version warnings.
- Run final package build, wheel install, examples, importer, generator, and docs checks.
- Tag and publish the v0.2.0 release when the scope is complete.

## v0.3.0

The `v0.3.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 13 | Complete | OpenAPI path-parameter extraction and generator precision |
| 14 | Complete | Python nested-object model generation |
| 15 | Complete | Pack authoring scaffold |
| 16 | Complete | v0.3.0 release preparation |

## Sprint 13 Priorities

Sprint 13 should improve generated contract accuracy:

- Parse path parameters from API endpoint paths such as `/users/{userId}`.
- Emit OpenAPI path parameters with stable names, `required: true`, and schema metadata.
- Avoid duplicate parameters when endpoint records already define explicit parameters.
- Add or update fixtures and golden expectations for generator output.
- Keep README, changelog, roadmap, release notes, version references, and issue or milestone state aligned.
- Add local-verification fallback guidance for GitHub Actions billing, credit, quota, or runner outages.
- Adopt a repository branching strategy and require AI agents to follow it.
- Update generator documentation and roadmap notes.

## Sprint 14 Priorities

Sprint 14 should make generated Python models more useful:

- Generate nested dataclasses for inline object properties.
- Generate nested dataclasses for inline object schemas inside arrays.
- Preserve required and optional field semantics in nested models.
- Update generator maturity fixtures and golden Python model output.
- Keep README, changelog, roadmap, generator docs, and issue state aligned.

## Sprint 15 Priorities

Sprint 15 should make extension pack authoring easier:

- Add a CLI command for creating a local pack scaffold.
- Generate a valid pack manifest and starter schema directory.
- Include validation coverage for the generated scaffold.
- Update README, changelog, roadmap, and pack docs.

## Sprint 16 Priorities

Sprint 16 should release the completed `v0.3.0` scope:

- Promote Unreleased changelog entries into `0.3.0`.
- Bump package metadata to `0.3.0`.
- Add v0.3.0 release notes.
- Update README and install references to `v0.3.0`.
- Run local release verification and GitHub Actions.
- Tag and publish the v0.3.0 GitHub release when checks pass.
- Close the v0.3.0 milestone after release verification.

## v0.4.0

The `v0.4.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 17 | Complete | Migration chains and workspace format evolution |
| 18 | Complete | v0.4.0 release preparation |

## Sprint 17 Priorities

Sprint 17 should make workspace migration version-aware:

- Add a migration registry that reports supported workspace versions and steps.
- Add path planning for chained migrations instead of a single hard-coded target check.
- Introduce workspace format `v0.2.0` while keeping `v0.1.0` supported.
- Migrate legacy workspaces through `legacy -> v0.1.0 -> v0.2.0` by default.
- Add `verity migrate --list` for migration capability discovery.
- Update examples, docs, tests, README, changelog, roadmap, and AI-agent guidance.

## Sprint 18 Priorities

Sprint 18 should release the completed `v0.4.0` scope:

- Promote Unreleased changelog entries into `0.4.0`.
- Bump package metadata to `0.4.0`.
- Add v0.4.0 release notes.
- Update README and install references to `v0.4.0`.
- Run local release verification and GitHub Actions.
- Tag and publish the v0.4.0 GitHub release when checks pass.
- Close the v0.4.0 milestone after release verification.

## v0.5.0

The `v0.5.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 19 | Complete | Security pack foundation and security report generation |
| 20 | Complete | v0.5.0 release preparation |

## Sprint 19 Priorities

Sprint 19 should add the first security surface as a pack, not as core bloat:

- Add built-in `verity.pack.security`.
- Add a strict `security.control` record schema.
- Add security-control readiness gates and reference rules.
- Add `verity generate security-report`.
- Add an executable security example workspace.
- Update tests, CI, README, changelog, roadmap, generator docs, pack docs, and
  AI-agent guidance.

## Sprint 20 Priorities

Sprint 20 should release the completed `v0.5.0` scope:

- Promote Unreleased changelog entries into `0.5.0`.
- Bump package metadata to `0.5.0`.
- Add v0.5.0 release notes.
- Update README and install references to `v0.5.0`.
- Run local release verification and GitHub Actions.
- Tag and publish the v0.5.0 GitHub release when checks pass.
- Close the v0.5.0 milestone after release verification.

## v0.6.0

The `v0.6.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 21 | Complete | Security readiness hardening for critical controls |
| 22 | Complete | Workspace compatibility matrix across supported spec versions |
| 23 | Complete | Nested issue locations for schema, readiness, and reference errors |
| 24 | Complete | v0.6.0 release preparation |

## Sprint 21 Priorities

Sprint 21 should make release readiness stricter for critical security controls:

- Add conditional readiness rules to pack manifests.
- Keep security policy in `verity.pack.security` instead of hard-coding it into
  the core kernel.
- Fail readiness for critical `security.control` records that are not verified.
- Add a stable `security.control.critical_unverified` issue code and
  explanation.
- Update tests, README, changelog, roadmap, readiness docs, and security docs.

## Sprint 22 Priorities

Sprint 22 should keep supported workspace versions executable as fixtures
evolve:

- Add a compatibility matrix over supported workspace `specVersion` values.
- Reuse positive example and fixture workspaces to avoid parallel fixture drift.
- Verify validation, lint, and readiness for each supported workspace version.
- Update README, changelog, roadmap, and versioning documentation.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 23 Priorities

Sprint 23 should make issue output easier to act on:

- Improve nested schema validation locations.
- Point readiness issues at missing or failing readiness fields.
- Point reference issues at the relevant reference field or target entry.
- Keep validation report output aligned with improved issue locations.
- Update tests, README, changelog, roadmap, and diagnostics documentation.

## Sprint 24 Priorities

Sprint 24 should release the completed `v0.6.0` scope:

- Promote Unreleased changelog entries into `0.6.0`.
- Bump package metadata to `0.6.0`.
- Add v0.6.0 release notes.
- Update README and install references to `v0.6.0`.
- Run local release verification and GitHub Actions.
- Tag and publish the v0.6.0 GitHub release when checks pass.
- Close the v0.6.0 milestone after release verification.

## v0.7.0

The `v0.7.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 25 | Complete | Doctor report file output |
| 26 | Complete | Workspace initialization templates |
| 27 | Complete | Observability pack foundation |
| 28 | Complete | Observability report generator |
| 29 | Complete | v0.7.0 release preparation |

## Sprint 25 Priorities

Sprint 25 should make diagnostics easier to preserve in CI and local workflows:

- Add `verity doctor --report-out` for writing structured diagnostics without
  shell redirection.
- Write the same JSON payload used by `verity doctor --format json`.
- Preserve normal stdout behavior for text and JSON doctor output.
- Create parent directories for report output paths.
- Keep exit-code behavior governed by `--fail-on`.
- Update tests, README, changelog, roadmap, contract-intelligence docs, and
  AI-agent command examples.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 26 Priorities

Sprint 26 should make new workspaces executable immediately:

- Add `verity init --template` for starter workspace generation.
- Support `basic`, `api`, `cli`, `events`, and `security` templates.
- Keep default `verity init` behavior compatible by using the `basic`
  template when no template is selected.
- Generate the built-in pack list and starter records needed for validation,
  strict linting, and strict readiness.
- Refuse to initialize over existing JSON records unless `--force` is used.
- Update tests, README, changelog, roadmap, workspace docs, and AI-agent
  command examples.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 27 Priorities

Sprint 27 should add the first observability surface as a pack:

- Add built-in `verity.pack.observability`.
- Add strict schemas for telemetry, metric, dashboard, and alert records.
- Add observability readiness gates and reference rules.
- Add an executable observability example workspace.
- Add validation, lint, readiness, pack validation, and compatibility coverage.
- Update README, changelog, roadmap, pack docs, observability docs, CI, and
  AI-agent command examples.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 28 Priorities

Sprint 28 should make observability contracts reportable:

- Add `verity generate observability-report`.
- Summarize telemetry, metrics, dashboards, alerts, owners, and alert severity.
- Report release gaps such as telemetry without metrics, metrics without
  telemetry, dashboards without tracked alerts, alerts without runbooks, and
  missing owners.
- Register the generator in CLI choices, pack validation, and
  `verity.pack.observability`.
- Add tests and CI smoke coverage.
- Update README, changelog, roadmap, generator docs, observability docs, CI,
  and AI-agent command examples.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 29 Priorities

Sprint 29 should release the completed `v0.7.0` scope:

- Promote Unreleased changelog entries into `0.7.0`.
- Bump package metadata to `0.7.0`.
- Add v0.7.0 release notes.
- Update README and install references to `v0.7.0`.
- Run local release verification and GitHub Actions.
- Tag and publish the v0.7.0 GitHub release when checks pass.
- Close the v0.7.0 milestone after release verification.

## v0.8.0

The `v0.8.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 30 | Complete | Accessibility pack foundation |
| 31 | Complete | Accessibility report generator |
| 32 | Complete | v0.8.0 release preparation |

## Sprint 30 Priorities

Sprint 30 should add the first accessibility surface as a pack:

- Add built-in `verity.pack.accessibility`.
- Add a strict `accessibility.claim` record schema for claims, checks, and
  evidence.
- Add accessibility readiness gates and reference rules.
- Add an executable accessibility example workspace.
- Add validation, lint, readiness, pack validation, and compatibility coverage.
- Update README, changelog, roadmap, pack docs, accessibility docs, CI, release
  checks, and AI-agent command examples.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 31 Priorities

Sprint 31 should make accessibility contracts reportable:

- Add `verity generate accessibility-report`.
- Summarize accessibility claims by owner, standard, level, impact, and
  coverage.
- Report release gaps such as critical unverified claims, claims without
  targets, missing owners, and missing verification dates.
- Register the generator in CLI choices, pack validation, and
  `verity.pack.accessibility`.
- Add tests and CI smoke coverage.
- Update README, changelog, roadmap, generator docs, accessibility docs, CI,
  release checks, and AI-agent command examples.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 32 Priorities

Sprint 32 should release the completed `v0.8.0` scope:

- Promote Unreleased changelog entries into `0.8.0`.
- Bump package metadata to `0.8.0`.
- Add v0.8.0 release notes.
- Update README and install references to `v0.8.0`.
- Run local release verification and GitHub Actions.
- Tag and publish the v0.8.0 GitHub release when checks pass.
- Close the v0.8.0 milestone after release verification.

## v0.9.0

The `v0.9.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 33 | Complete | Compliance pack foundation |
| 34 | Complete | Compliance matrix generator |
| 35 | Complete | v0.9.0 release preparation |

## Sprint 33 Priorities

Sprint 33 should add the first compliance surface as a pack:

- Add built-in `verity.pack.compliance`.
- Add a strict `compliance.mapping` record schema for framework requirement
  mappings.
- Keep compliance mappings evidence-oriented and explicitly avoid legal,
  regulatory, audit, or certification attestation claims.
- Add compliance readiness gates, reviewed-mapping policy, and reference rules.
- Add an executable compliance example workspace that connects security,
  accessibility, and observability evidence.
- Add validation, lint, readiness, pack validation, and compatibility coverage.
- Update README, changelog, roadmap, pack docs, compliance docs, CI, release
  checks, and AI-agent command examples.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 34 Priorities

Sprint 34 should make compliance mappings reportable:

- Add `verity generate compliance-matrix`.
- Summarize compliance mappings by owner, framework, requirement, mapping type,
  coverage, and verification state.
- Join mapped security controls, accessibility claims, and observability
  signals into grouped evidence.
- Report release gaps such as mappings without targets, mappings without
  evidence, reviewed-but-unverified mappings, missing mapping owners, and
  targets without owners.
- Register the generator in CLI choices, pack validation, and
  `verity.pack.compliance`.
- Add tests and CI smoke coverage.
- Update README, changelog, roadmap, generator docs, compliance docs, CI,
  release checks, and AI-agent command examples.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 35 Priorities

Sprint 35 should release the completed `v0.9.0` scope:

- Promote Unreleased changelog entries into `0.9.0`.
- Bump package metadata to `0.9.0`.
- Add v0.9.0 release notes.
- Update README and install references to `v0.9.0`.
- Run local release verification and GitHub Actions.
- Tag and publish the v0.9.0 GitHub release when checks pass.
- Close the v0.9.0 milestone after release verification.

## v0.10.0

The `v0.10.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 36 | Complete | Diff severity and breaking-change classification |
| 37 | Complete | v0.10.0 release preparation |

## Sprint 36 Priorities

Sprint 36 should make workspace diffs easier for humans, CI, and machine
clients to evaluate:

- Add machine-readable per-change severity to `verity diff --format json`.
- Add breaking-change classification for removed packs, removed records, kind
  changes, records marked removed, API endpoint method/path changes, removed
  API response status codes, and schema-object contract removals.
- Preserve existing `versions`, `packs`, `added`, `removed`, and `changed`
  fields for compatibility.
- Add `summary` and `changes` fields for machine clients.
- Update text output with severity and breaking-change summaries.
- Add focused CLI tests and CI smoke coverage.
- Update README, changelog, roadmap, versioning docs, CI docs, and AI-agent
  command examples.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 37 Priorities

Sprint 37 should release the completed `v0.10.0` scope:

- Promote Unreleased changelog entries into `0.10.0`.
- Bump package metadata to `0.10.0`.
- Add v0.10.0 release notes.
- Update README and install references to `v0.10.0`.
- Run local release verification and GitHub Actions.
- Tag and publish the v0.10.0 GitHub release when checks pass.
- Close the v0.10.0 milestone after release verification.

## v0.11.0

The `v0.11.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 38 | Complete | Migration dry-run edge fixtures |
| 39 | Complete | v0.11.0 release preparation |

## Sprint 38 Priorities

Sprint 38 should harden workspace migration dry-run coverage:

- Add committed fixtures for every supported workspace migration edge.
- Verify dry-run reports the planned migration path without writing files.
- Assert expected change records for each supported edge.
- Preserve the default legacy-to-current chained migration dry-run behavior.
- Update README, changelog, roadmap, and migration docs.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 39 Priorities

Sprint 39 should release the completed `v0.11.0` scope:

- Promote Unreleased changelog entries into `0.11.0`.
- Bump package metadata to `0.11.0`.
- Add v0.11.0 release notes.
- Update README and install references to `v0.11.0`.
- Run local release verification and GitHub Actions.
- Tag and publish the v0.11.0 GitHub release when checks pass.
- Close the v0.11.0 milestone after release verification.

## v0.12.0

The `v0.12.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 40 | Complete | Generator metadata in pack manifests |
| 41 | Complete | v0.12.0 release preparation |

## Sprint 40 Priorities

Sprint 40 should make pack generator capabilities more explicit:

- Support structured generator metadata in pack manifests.
- Preserve legacy string generator declarations for existing external packs.
- Keep `pack.generators` as a normalized ID list for compatibility.
- Expose `generatorMetadata` through `verity pack list --format json`.
- Validate structured generator IDs against known generator commands.
- Update built-in pack manifests, pack scaffolding, tests, README, changelog,
  roadmap, and generator/pack docs.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 41 Priorities

Sprint 41 should release the completed `v0.12.0` scope:

- Promote Unreleased changelog entries into `0.12.0`.
- Bump package metadata to `0.12.0`.
- Add v0.12.0 release notes.
- Update README and install references to `v0.12.0`.
- Run local release verification and GitHub Actions.
- Tag and publish the v0.12.0 GitHub release when checks pass.
- Close the v0.12.0 milestone after release verification.

## v0.13.0

The `v0.13.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 42 | Complete | Pack authoring scaffold workspace tests |
| 43 | Complete | v0.13.0 release preparation |

## Sprint 42 Priorities

Sprint 42 should prove generated pack scaffolds can be used immediately:

- Add executable coverage that runs `verity pack init` into a temporary pack
  directory.
- Generate a sample workspace that loads the scaffolded pack through
  `packPaths`.
- Validate the generated pack with `verity pack validate`.
- Validate, strict-lint, strict-readiness-check, and schema-bundle-generate
  from the sample workspace.
- Add a starter reference rule so the generated record kind can be connected
  to the workspace product contract.
- Update README, changelog, roadmap, and pack docs.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 43 Priorities

Sprint 43 should release the completed `v0.13.0` scope:

- Promote Unreleased changelog entries into `0.13.0`.
- Bump package metadata to `0.13.0`.
- Add v0.13.0 release notes.
- Update README badge, latest-release text, install references, and release
  notes link to `v0.13.0`.
- Run local release verification and GitHub Actions.
- Tag and publish the v0.13.0 GitHub release when checks pass.
- Close the v0.13.0 milestone after release verification.

## v0.14.0

The `v0.14.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 44 | Complete | Downstream GitHub Actions templates |
| 45 | Complete | v0.14.0 release preparation |

## Sprint 44 Priorities

Sprint 44 should make downstream CI adoption copyable and maintained:

- Add copyable GitHub Actions workflow templates outside `.github/workflows`
  so they do not run in this repository.
- Include reusable-workflow, local-pack, and direct-install variants.
- Align the reusable workflow default install command with the current release
  tag.
- Update downstream CI docs from inline-only examples to maintained template
  files.
- Add tests that fail when downstream templates or docs reference stale
  VeritySpec release tags.
- Update README, changelog, roadmap, and downstream CI docs.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 45 Priorities

Sprint 45 should release the completed `v0.14.0` scope:

- Promote Unreleased changelog entries into `0.14.0`.
- Bump package metadata to `0.14.0`.
- Add v0.14.0 release notes.
- Update README badge, latest-release text, install references, workspace
  package-version text, and release-notes link to `v0.14.0`.
- Update downstream CI templates, docs, and reusable workflow release pins to
  `v0.14.0`.
- Run local release verification and GitHub Actions.
- Tag and publish the v0.14.0 GitHub release when checks pass.
- Close the v0.14.0 milestone after release verification.

## v0.15.0

The `v0.15.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 46 | Complete | Golden security-report fixtures |
| 47 | Complete | v0.15.0 release preparation |

## Sprint 46 Priorities

Sprint 46 should make the security report output shape reviewable and stable:

- Add a committed golden fixture for the `examples/security`
  `security-report` generator output.
- Add direct generator coverage that compares normalized report output to the
  golden fixture.
- Add CLI generator coverage that compares normalized report output to the
  golden fixture.
- Normalize only dynamic fields: generation timestamp, absolute workspace
  path, and package version.
- Document the security-report golden coverage in generator and security-pack
  docs.
- Update README, changelog, and roadmap bookkeeping.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 47 Priorities

Sprint 47 should release the completed `v0.15.0` scope:

- Promote Unreleased changelog entries into `0.15.0`.
- Bump package metadata to `0.15.0`.
- Add v0.15.0 release notes.
- Update README badge, latest-release text, install references, workspace
  package-version text, and release-notes link to `v0.15.0`.
- Update downstream CI templates, docs, and reusable workflow release pins to
  `v0.15.0`.
- Codify the required AI operating loop and release checklist steps used for
  sprint implementation, PR verification, main verification, tagging, release
  asset checks, and roadmap upkeep.
- Run local release verification and GitHub Actions.
- Tag and publish the v0.15.0 GitHub release when checks pass.
- Close the v0.15.0 milestone after release verification.

## v0.16.0

The `v0.16.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 48 | Complete | Public contribution guidance |
| 49 | Complete | v0.16.0 release preparation |

## Sprint 48 Priorities

Sprint 48 should make public pack and schema contributions easier to propose
without weakening VeritySpec's executable-contract standard:

- Add top-level contribution guidance for the project.
- Document pack proposal expectations, including schemas, examples, tests,
  readiness gates, reference rules, generators or reports, and compatibility
  boundaries.
- Document schema-change expectations, including additive versus breaking
  changes, migration impact, generator impact, and validation fixtures.
- Add GitHub issue templates for pack proposals and schema changes.
- Link the contribution guidance from README and pack docs.
- Add executable tests that keep the contribution guidance and templates
  present and aligned.
- Update changelog and roadmap bookkeeping.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 49 Priorities

Sprint 49 should release the completed `v0.16.0` scope:

- Promote Unreleased changelog entries into `0.16.0`.
- Bump package metadata to `0.16.0`.
- Add v0.16.0 release notes.
- Update README badge, latest-release text, install references, workspace
  package-version text, and release-notes link to `v0.16.0`.
- Update downstream CI templates, docs, and reusable workflow release pins to
  `v0.16.0`.
- Run local release verification and GitHub Actions.
- Tag and publish the v0.16.0 GitHub release when checks pass.
- Close the v0.16.0 milestone after release verification.

## v0.17.0

The `v0.17.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 50 | Complete | PyPI publishing readiness |
| 51 | Complete | v0.17.0 release preparation |

## Sprint 50 Priorities

Sprint 50 should harden PyPI readiness without enabling publishing:

- Update PyPI documentation with the current GitHub release fallback install
  tag.
- Document the current publishing decision: do not publish to PyPI until
  PyPI-side trusted publishing is configured and explicitly enabled.
- Document repository-side readiness, PyPI-side blockers, and the no-token
  rule.
- Add tests that keep PyPI install fallback docs aligned with the current
  package version.
- Update README, changelog, roadmap, and release checklist bookkeeping.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 51 Priorities

Sprint 51 should release the completed `v0.17.0` scope:

- Promote Unreleased changelog entries into `0.17.0`.
- Bump package metadata to `0.17.0`.
- Add v0.17.0 release notes.
- Update README badge, latest-release text, install references, workspace
  package-version text, and release-notes link to `v0.17.0`.
- Update downstream CI templates, docs, PyPI fallback docs, and reusable
  workflow release pins to `v0.17.0`.
- Keep PyPI publishing disabled unless explicitly requested.
- Run local release verification and GitHub Actions.
- Tag and publish the v0.17.0 GitHub release when checks pass.
- Close the v0.17.0 milestone after release verification.

## v0.18.0

The `v0.18.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 52 | Complete | Roadmap-report generator |
| 53 | Complete | v0.18.0 release preparation |

## Sprint 52 Priorities

Sprint 52 should make roadmap governance machine-readable:

- Add `verity generate roadmap-report`.
- Parse `ROADMAP.md` into a structured JSON report.
- Include release milestone sections, sprint rows, active milestones, latest
  released milestone, completed sprint counts, and Next 20 planning points.
- Allow the command to read a repository directory or direct roadmap file.
- Add library and CLI coverage for the report shape.
- Update README, generator docs, changelog, and roadmap bookkeeping.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 53 Priorities

Sprint 53 should release the completed `v0.18.0` scope:

- Promote Unreleased changelog entries into `0.18.0`.
- Bump package metadata to `0.18.0`.
- Add v0.18.0 release notes.
- Update README badge, latest-release text, install references, workspace
  package-version text, and release-notes link to `v0.18.0`.
- Update downstream CI templates, docs, PyPI fallback docs, and reusable
  workflow release pins to `v0.18.0`.
- Keep PyPI publishing disabled unless explicitly requested.
- Run local release verification and GitHub Actions.
- Tag and publish the v0.18.0 GitHub release when checks pass.
- Close the v0.18.0 milestone after release verification.

## v0.19.0

The `v0.19.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 54 | Complete | Security evidence freshness checks |
| 55 | Complete | v0.19.0 release preparation |

## Sprint 54 Priorities

Sprint 54 should make security-control verification evidence freshness
executable:

- Add readiness support for date freshness checks declared by packs.
- Add optional `verification.reviewCadenceDays` to `security.control`.
- Emit `security.control.evidence_stale` when a control declares a cadence but
  lacks fresh `verification.lastVerified` evidence.
- Keep the freshness policy in the security pack manifest.
- Add tests for fresh, stale, and missing freshness evidence.
- Update README, readiness docs, security-pack docs, changelog, and roadmap
  bookkeeping.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 55 Priorities

Sprint 55 should release the completed `v0.19.0` scope:

- Promote Unreleased changelog entries into `0.19.0`.
- Bump package metadata to `0.19.0`.
- Add v0.19.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.19.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.19.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.19.0 GitHub release when checks pass.
- Close the v0.19.0 milestone after release verification.

## v0.20.0

The `v0.20.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 56 | Complete | Workspace compatibility golden manifests |
| 57 | Complete | v0.20.0 release preparation |

## Sprint 56 Priorities

Sprint 56 should make workspace format compatibility easier to review as
future formats are added:

- Add a deterministic golden compatibility manifest for supported workspace
  formats.
- Record covered workspaces, packs, record counts, record-kind coverage, and
  expected validation/lint/readiness checks.
- Compare regenerated compatibility metadata against the golden manifest in
  tests.
- Keep the existing compatibility matrix executable across every supported
  `specVersion`.
- Update README, changelog, roadmap, and versioning docs.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 57 Priorities

Sprint 57 should release the completed `v0.20.0` scope:

- Promote Unreleased changelog entries into `0.20.0`.
- Bump package metadata to `0.20.0`.
- Add v0.20.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.20.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.20.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.20.0 GitHub release when checks pass.
- Close the v0.20.0 milestone after release verification.

## v0.21.0

The `v0.21.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 58 | Complete | Structured issue location fields |
| 59 | Complete | v0.21.0 release preparation |

## Sprint 58 Priorities

Sprint 58 should make JSON diagnostics easier for tools and agents to consume:

- Add structured issue location fields without removing formatted `location`
  strings.
- Parse file paths, record fragments, nested field paths, field parts, JSON
  pointers, and record indexes when available.
- Keep text output stable for humans.
- Add tests for CLI JSON diagnostics, validation reports, and location parsing.
- Update README, changelog, roadmap, contract-intelligence docs, and generator
  docs.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 59 Priorities

Sprint 59 should release the completed `v0.21.0` scope:

- Promote Unreleased changelog entries into `0.21.0`.
- Bump package metadata to `0.21.0`.
- Add v0.21.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.21.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.21.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.21.0 GitHub release when checks pass.
- Close the v0.21.0 milestone after release verification.

## v0.22.0

The `v0.22.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 60 | Complete | README command smoke tests |
| 61 | Complete | v0.22.0 release preparation |

## Sprint 60 Priorities

Sprint 60 should keep public command documentation executable:

- Parse README bash command examples in tests.
- Execute safe local `verity` examples in documented order.
- Rewrite `build/` output paths to temporary directories during smoke tests.
- Treat install, virtual environment, and full test-suite commands as explicit
  documentation-only skips.
- Add test coverage that fails when new README command examples are neither
  executable nor intentionally skipped.
- Update README, changelog, roadmap, and CI docs.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 61 Priorities

Sprint 61 should release the completed `v0.22.0` scope:

- Promote Unreleased changelog entries into `0.22.0`.
- Bump package metadata to `0.22.0`.
- Add v0.22.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.22.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.22.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.22.0 GitHub release when checks pass.
- Close the v0.22.0 milestone after release verification.

## v0.23.0

The `v0.23.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 62 | Complete | CI annotation output for contract failures |
| 63 | Complete | v0.23.0 release preparation |

## Sprint 62 Priorities

Sprint 62 should make product-contract failures easier to navigate in GitHub
Actions:

- Add opt-in GitHub Actions annotation output for validation, lint, and
  readiness issues.
- Preserve existing text and JSON stdout by writing annotations to stderr.
- Escape `%`, carriage returns, newlines, colons, and commas according to
  GitHub workflow command rules.
- Add validation and readiness CLI tests for annotation output.
- Add issue-level escaping coverage.
- Update README, changelog, roadmap, CI docs, downstream CI docs, and workflow
  templates.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 63 Priorities

Sprint 63 should release the completed `v0.23.0` scope:

- Promote Unreleased changelog entries into `0.23.0`.
- Bump package metadata to `0.23.0`.
- Add v0.23.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.23.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.23.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.23.0 GitHub release when checks pass.
- Close the v0.23.0 milestone after release verification.

## v0.24.0

The `v0.24.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 64 | Complete | Observability golden fixtures |
| 65 | Complete | v0.24.0 release preparation |

## Sprint 64 Priorities

Sprint 64 should add stable golden coverage for observability generated
artifacts:

- Add committed golden fixtures for the `examples/observability`
  `observability-report` output.
- Add committed golden fixtures for the `examples/observability`
  `schema-bundle` output.
- Add library and CLI tests that compare observability generator output to
  the golden fixtures.
- Normalize dynamic observability report metadata before golden comparisons.
- Update README, changelog, roadmap, generator docs, and observability pack
  docs.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 65 Priorities

Sprint 65 should release the completed `v0.24.0` scope:

- Promote Unreleased changelog entries into `0.24.0`.
- Bump package metadata to `0.24.0`.
- Add v0.24.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.24.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.24.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.24.0 GitHub release when checks pass.
- Close the v0.24.0 milestone after release verification.

## v0.25.0

The `v0.25.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 66 | Complete | Deterministic report timestamp controls |
| 67 | Complete | v0.25.0 release preparation |

## Sprint 66 Priorities

Sprint 66 should make report fixture generation deterministic:

- Add a shared generated-at helper for report generators.
- Add `verity generate --generated-at` support for JSON report artifacts.
- Validate explicit generated-at values as ISO 8601 datetimes.
- Add library and CLI tests for fixed report timestamps and invalid values.
- Update README, changelog, roadmap, and generator docs.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 67 Priorities

Sprint 67 should release the completed `v0.25.0` scope:

- Promote Unreleased changelog entries into `0.25.0`.
- Bump package metadata to `0.25.0`.
- Add v0.25.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.25.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.25.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.25.0 GitHub release when checks pass.
- Close the v0.25.0 milestone after release verification.

## Later Candidates

These are intentionally not committed to a release until the current milestone
is complete:

- UI, desktop, mobile, game, assets, and deployment packs.
- Downstream project examples.

## v0.26.0

The `v0.26.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 68 | Complete | Product-surface pack boundary design |
| 69 | Complete | v0.26.0 release preparation |

## Sprint 68 Priorities

Sprint 68 should define pack boundaries before adding new product-surface
schemas:

- Add a public design note for future GUI, desktop, mobile, and game packs.
- Clarify what belongs in product-surface packs versus cross-cutting packs.
- Document first-schema gates for these future packs.
- Link the design note from README and pack documentation.
- Add tests that keep the design note discoverable and preserve the boundary
  commitments.
- Update changelog and roadmap bookkeeping.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 69 Priorities

Sprint 69 should release the completed `v0.26.0` scope:

- Promote Unreleased changelog entries into `0.26.0`.
- Bump package metadata to `0.26.0`.
- Add v0.26.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.26.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.26.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.26.0 GitHub release when checks pass.
- Close the v0.26.0 milestone after release verification.

## v0.27.0

The `v0.27.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 70 | Complete | Product-contract enforcement profiles |
| 71 | Complete | v0.27.0 release preparation |

## Sprint 70 Priorities

Sprint 70 should add product-contract enforcement profiles:

- Add named profiles for release, strict, regulated, public API, and
  internal-tool enforcement modes.
- Expose profiles on `validate`, `lint`, `readiness`, and `doctor`.
- Include effective profile metadata in JSON output for machine clients.
- Add profile-specific checks for regulated and public API workspaces.
- Add library and CLI tests for profile behavior and exit codes.
- Document profile semantics and CI usage.
- Update README, changelog, and roadmap bookkeeping.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 71 Priorities

Sprint 71 should release the completed `v0.27.0` scope:

- Promote Unreleased changelog entries into `0.27.0`.
- Bump package metadata to `0.27.0`.
- Add v0.27.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.27.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.27.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.27.0 GitHub release when checks pass.
- Close the v0.27.0 milestone after release verification.

## v0.28.0

The `v0.28.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 72 | Complete | Deployment-target pack |
| 73 | Complete | v0.28.0 release preparation |

## Sprint 72 Priorities

Sprint 72 should add the first deployment-target pack:

- Add `verity.pack.deployment` with runtime and deployment target schemas.
- Add readiness gates for runtime, hosting, release environment, rollback,
  and production health-check coverage.
- Make deployment target runtime links resolvable through `runtimeRef`.
- Add a deployment report generator for release and operations review.
- Add an executable `examples/deployment` workspace.
- Add validation, readiness, generator, and CLI tests for deployment behavior.
- Document the deployment pack and CI usage.
- Update README, changelog, and roadmap bookkeeping.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 73 Priorities

Sprint 73 should release the completed `v0.28.0` scope:

- Promote Unreleased changelog entries into `0.28.0`.
- Bump package metadata to `0.28.0`.
- Add v0.28.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.28.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.28.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.28.0 GitHub release when checks pass.
- Close the v0.28.0 milestone after release verification.

## v0.29.0

The `v0.29.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 74 | Complete | Cross-pack coverage dashboards |
| 75 | Complete | v0.29.0 release preparation |

## Sprint 74 Priorities

Sprint 74 should add cross-pack coverage dashboards:

- Add `verity generate coverage-dashboard` for JSON product-surface coverage
  summaries.
- Track API, CLI, events, security, accessibility, observability, compliance,
  and deployment coverage across loaded workspace records.
- Include product-level surface references and release gaps for missing
  surface records or missing product surface links.
- Add a full cross-pack fixture with strict validation, lint, and readiness
  coverage.
- Add golden fixture coverage for deterministic dashboard output.
- Update CI, release checklist, generator docs, README, AGENTS, changelog, and
  roadmap bookkeeping.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 75 Priorities

Sprint 75 should release the completed `v0.29.0` scope:

- Promote Unreleased changelog entries into `0.29.0`.
- Bump package metadata to `0.29.0`.
- Add v0.29.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.29.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.29.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.29.0 GitHub release when checks pass.
- Close the v0.29.0 milestone after release verification.

## v0.30.0

The `v0.30.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 76 | Complete | Product-impact report for release-review graph analysis |
| 77 | Complete | v0.30.0 release preparation |

## Sprint 76 Priorities

Sprint 76 should add product-impact reports:

- Add `verity generate product-impact OLD NEW` for JSON release-review impact
  summaries.
- Compare baseline and current workspaces using the existing diff
  classification model.
- Expand changed, added, and removed records into upstream dependents and
  downstream dependencies through the workspace reference graph.
- Include missing-reference evidence from baseline and current graph edges.
- Include release-review summary fields for risk level, review focus, changed
  record count, impacted record count, and severity counts.
- Add deterministic baseline/current fixtures and committed golden output.
- Update CI, release checklist, generator docs, README, AGENTS, changelog, and
  roadmap bookkeeping.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 77 Priorities

Sprint 77 should release the completed `v0.30.0` scope:

- Promote Unreleased changelog entries into `0.30.0`.
- Bump package metadata to `0.30.0`.
- Add v0.30.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.30.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.30.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.30.0 GitHub release when checks pass.
- Close the v0.30.0 milestone after release verification.

## v0.31.0

The `v0.31.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 78 | Complete | Local-only cross-workspace dependency design |
| 79 | Complete | v0.31.0 release preparation |

## Sprint 78 Priorities

Sprint 78 should define the cross-workspace dependency boundary before
implementation:

- Add a design note for local-only workspace dependencies.
- Keep the first dependency phase direct, readonly, and local-path oriented.
- Distinguish packs from workspace dependencies.
- Define exported-record visibility expectations.
- Define friendly and canonical cross-workspace reference forms.
- Define resolver phases and lockfile boundaries.
- Call out dependency-aware validation, graph, diff, and impact behavior.
- Link the design note from README, pack, workspace-format, and graph docs.
- Add a documentation guard test for the key design decisions.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 79 Priorities

Sprint 79 should release the completed `v0.31.0` scope:

- Promote Unreleased changelog entries into `0.31.0`.
- Bump package metadata to `0.31.0`.
- Add v0.31.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.31.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.31.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.31.0 GitHub release when checks pass.
- Close the v0.31.0 milestone after release verification.

## v0.32.0

The `v0.32.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 80 | Complete | Pack capability index report |
| 81 | Complete | v0.32.0 release preparation |

## Sprint 80 Priorities

Sprint 80 should add a pack capability index report:

- Add `verity generate pack-capability-index`.
- Summarize loaded built-in and external packs.
- Include schema, readiness gate, conditional readiness rule, reference rule,
  and generator counts.
- Include per-pack schema, readiness, reference-rule, and generator metadata.
- Deduplicate generator capabilities across packs for registry review.
- Prove local external-pack coverage with both `packPaths` and `--pack-path`.
- Add golden output coverage for the report contract.
- Update README, generator docs, pack docs, CI examples, release checklist,
  and AI-agent command lists.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 81 Priorities

Sprint 81 should release the completed `v0.32.0` scope:

- Promote Unreleased changelog entries into `0.32.0`.
- Bump package metadata to `0.32.0`.
- Add v0.32.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.32.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.32.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.32.0 GitHub release when checks pass.
- Close the v0.32.0 milestone after release verification.

## v0.33.0

The `v0.33.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 82 | Complete | Pack scaffold documentation fixtures |
| 83 | Complete | v0.33.0 release preparation |

## Sprint 82 Priorities

Sprint 82 should add pack scaffold documentation fixtures:

- Add committed documentation fixtures for a generated external pack.
- Add a consuming workspace that loads the generated pack through `packPaths`.
- Preserve the generated `product` to starter-kind `uses` reference rule.
- Document the fixture layout and executable commands for external pack
  authors.
- Prove the committed fixture matches fresh `verity pack init` output.
- Validate, strict-lint, strict-readiness-check, schema-bundle-generate, and
  pack-capability-index-generate the consuming workspace.
- Add CI and release-checklist commands for the documentation fixture.
- Link the fixture from README and pack docs.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 83 Priorities

Sprint 83 should release the completed `v0.33.0` scope:

- Promote Unreleased changelog entries into `0.33.0`.
- Bump package metadata to `0.33.0`.
- Add v0.33.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.33.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.33.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.33.0 GitHub release when checks pass.
- Close the v0.33.0 milestone after release verification.

## v0.34.0

The `v0.34.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 84 | Complete | Monorepo downstream CI templates |
| 85 | Complete | v0.34.0 release preparation |

## Sprint 84 Priorities

Sprint 84 should make downstream CI adoption clearer for monorepos:

- Add a maintained GitHub Actions template for monorepos with multiple
  VeritySpec workspaces.
- Use the existing reusable product-contract workflow instead of duplicating
  shell logic.
- Support shared local pack paths and workspace-specific pack paths through a
  matrix.
- Document how downstream repositories should adapt the matrix entries.
- Add tests that keep the monorepo template pinned to the current release tag.
- Update README, changelog, roadmap, CI docs, downstream CI docs, release
  checklist, and AI-agent guidance.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 85 Priorities

Sprint 85 should release the completed `v0.34.0` scope:

- Promote Unreleased changelog entries into `0.34.0`.
- Bump package metadata to `0.34.0`.
- Add v0.34.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.34.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.34.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.34.0 GitHub release when checks pass.
- Close the v0.34.0 milestone after release verification.

## v0.35.0

The `v0.35.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 86 | Complete | Game-core pack foundation |
| 87 | Complete | v0.35.0 release preparation |

## Sprint 86 Priorities

Sprint 86 should add the first narrow built-in game product-surface pack:

- Add built-in `verity.pack.game-core`.
- Add strict schemas for `game.product`, `game.mode`, `game.loop`, and
  `game.prototype-scope`.
- Add game-core readiness gates and reference rules.
- Add an executable `examples/game-core` workspace.
- Add game-core coverage to cross-pack coverage dashboards.
- Update tests, CI, README, changelog, roadmap, pack docs, generator docs,
  release checklist, and AI-agent guidance.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 87 Priorities

Sprint 87 should release the completed `v0.35.0` scope:

- Promote Unreleased changelog entries into `0.35.0`.
- Bump package metadata to `0.35.0`.
- Add v0.35.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.35.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.35.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.35.0 GitHub release when checks pass.
- Close the v0.35.0 milestone after release verification.

## v0.36.0

The `v0.36.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 88 | Complete | Game-assets pack foundation |
| 89 | Complete | v0.36.0 release preparation |

## Sprint 88 Priorities

Sprint 88 should add the first narrow built-in creative-source game pack:

- Add built-in `verity.pack.game-assets`.
- Add strict schemas for `game.gdd-source`, `game.visual-identity`,
  `game.identity-image`, and `game.concept-art`.
- Add game-assets readiness gates and reference rules that connect GDD,
  identity, and concept-art records to game-core records.
- Add an executable `examples/game-assets` workspace.
- Add game-assets coverage to cross-pack coverage dashboards.
- Update tests, CI, README, changelog, roadmap, pack docs, generator docs,
  release checklist, and AI-agent guidance.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 89 Priorities

Sprint 89 should release the completed `v0.36.0` scope:

- Promote Unreleased changelog entries into `0.36.0`.
- Bump package metadata to `0.36.0`.
- Add v0.36.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.36.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.36.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.36.0 GitHub release when checks pass.
- Close the v0.36.0 milestone after release verification.

## v0.37.0

The `v0.37.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 90 | Complete | Unity pack foundation |
| 91 | Complete | v0.37.0 release preparation |

## Sprint 90 Priorities

Sprint 90 should add the first narrow built-in Unity implementation pack:

- Add built-in `verity.pack.unity`.
- Add strict schemas for `unity.project`, `unity.package-dependency`,
  `unity.scene`, and `unity.build-target`.
- Add Unity readiness gates and reference rules that connect Unity projects to
  package dependencies, scenes, and build targets.
- Add an executable `examples/unity` workspace.
- Add Unity coverage to cross-pack coverage dashboards.
- Update tests, CI, README, changelog, roadmap, pack docs, generator docs,
  release checklist, and AI-agent guidance.
- Keep the next-20 planning backlog populated after converting this item.

## Sprint 91 Priorities

Sprint 91 should release the completed `v0.37.0` scope:

- Promote Unreleased changelog entries into `0.37.0`.
- Bump package metadata to `0.37.0`.
- Add v0.37.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.37.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.37.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.37.0 GitHub release when checks pass.
- Close the v0.37.0 milestone after release verification.

## v0.38.0

The `v0.38.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 92 | Complete | Gameplay and content pack foundations |
| 93 | Complete | v0.38.0 release preparation |

## Sprint 92 Priorities

Sprint 92 is the first larger bundled implementation sprint for the next
game-domain expansion:

- Add built-in `verity.pack.gameplay`.
- Add strict schemas for `game.mechanic`, `game.ability`, `game.rule`, and
  `game.encounter`.
- Add built-in `verity.pack.content`.
- Add strict schemas for `game.content-item`, `game.level`, `game.loot-table`,
  and `game.content-manifest`.
- Add readiness gates and reference rules that connect gameplay mechanics,
  abilities, rules, encounters, content items, levels, loot tables, manifests,
  game-core records, and Unity scene records where appropriate.
- Add executable `examples/gameplay` and `examples/content` workspaces.
- Add gameplay and content coverage to cross-pack coverage dashboards.
- Update tests, CI, README, changelog, roadmap, pack docs, generator docs,
  readiness docs, release checklist, and AI-agent guidance in one bundled
  sprint.
- Keep the next-20 planning backlog populated after converting the gameplay
  item.

## Sprint 93 Priorities

Sprint 93 should release the completed `v0.38.0` scope:

- Promote Unreleased changelog entries into `0.38.0`.
- Bump package metadata to `0.38.0`.
- Add v0.38.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.38.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.38.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.38.0 GitHub release when checks pass.
- Close the v0.38.0 milestone after release verification.

## v0.39.0

The `v0.39.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 94 | Complete | Economy pack foundation |
| 95 | Complete | v0.39.0 release preparation |

## Sprint 94 Priorities

Sprint 94 is a week-sized bundled sprint for the first economy product surface:

- Add built-in `verity.pack.economy`.
- Add strict schemas for `economy.currency`, `economy.source`,
  `economy.sink`, `economy.reward`, and `economy.offer`.
- Add readiness gates and reference rules that connect game products,
  gameplay mechanics, content manifests, loot tables, currencies, sources,
  sinks, rewards, and offers.
- Add executable `examples/economy` workspace.
- Add economy coverage to cross-pack coverage dashboards.
- Update tests, CI, README, changelog, roadmap, pack docs, generator docs,
  readiness docs, release checklist, and AI-agent guidance in one bundled
  sprint.
- Keep the next-20 planning backlog populated after converting the economy
  item.

## Sprint 95 Priorities

Sprint 95 should release the completed `v0.39.0` scope:

- Promote Unreleased changelog entries into `0.39.0`.
- Bump package metadata to `0.39.0`.
- Add v0.39.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.39.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.39.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.39.0 GitHub release when checks pass.
- Close the v0.39.0 milestone after release verification.

## v0.40.0

The `v0.40.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 96 | Complete | Engine and product-delivery pack roadmap |
| 97 | Complete | Unity engine-tooling expansion foundation |
| 98 | Complete | v0.40.0 release preparation |

## Sprint 96 Priorities

Sprint 96 is a week-sized planning and foundation sprint for engine tooling and
spec-driven product delivery:

- Add public design documentation for future Unity expansion, Godot pack,
  Unreal pack, and product-delivery pack support.
- Document the intended model that GitHub manages workflow while VeritySpec
  manages product-contract truth.
- Capture future record-kind candidates for Unity, Godot, Unreal, and
  spec-driven product-delivery repositories.
- State implementation acceptance criteria for future built-in packs:
  schemas, readiness gates where useful, reference rules, examples, docs, and
  tests.
- Explain that these packs support engine-tooling repositories and
  spec-driven product management without making commercial, legal,
  marketplace-readiness, certification, or similar claims.
- Keep the pack-based architecture explicit: core stays small.
- Refresh the next-20 planning backlog around larger cohesive implementation
  sprints.

## Sprint 97 Priorities

Sprint 97 implements the first larger engine-tooling expansion for the built-in
Unity pack:

- Add a selected Unity vertical slice: `unity.package`,
  `unity.shared-library`, `unity.prefab`, `unity.asmdef`, `unity.scanner`,
  `unity.validation-runner`, `unity.readiness-dashboard`, and
  `unity.agent-context-exporter`.
- Add strict schemas, readiness gates where useful, reference rules,
  executable examples, docs, and tests.
- Update the Unity example so it passes validation, strict linting, strict
  readiness, and graph checks.
- Keep core small and preserve pack-based architecture.
- Avoid commercial, legal, marketplace-readiness, certification, or similar
  claims.

## Sprint 98 Priorities

Sprint 98 releases the completed `v0.40.0` scope:

- Promote Unreleased changelog entries into `0.40.0`.
- Bump package metadata to `0.40.0`.
- Add v0.40.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.40.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.40.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.40.0 GitHub release when checks pass.
- Close the v0.40.0 milestone after release verification.

## v0.41.0

The `v0.41.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 99 | Complete | Godot engine and game workspace pack foundation |
| 100 | Complete | v0.41.0 release preparation |

## Sprint 99 Priorities

Sprint 99 implements the next built-in engine and game-workspace pack
foundation:

- Add built-in `verity.pack.godot`.
- Add strict schemas for `godot.project`, `godot.addon`,
  `godot.shared-library`, `godot.scene`, `godot.node-contract`,
  `godot.resource`, `godot.script`, `godot.autoload`,
  `godot.input-action`, `godot.export-preset`, `godot.scanner`,
  `godot.validation-runner`, `godot.readiness-dashboard`, and
  `godot.agent-context-exporter`.
- Add readiness gates and reference rules that connect Godot game projects,
  addons, shared libraries, scenes, nodes, resources, scripts, autoloads,
  input actions, export presets, scanners, validation runners, dashboards, and
  agent-context exporters.
- Add an executable `examples/godot` game workspace that composes with
  game-core records without moving game design into the core kernel.
- Add Godot coverage to cross-pack coverage dashboards and schema-bundle
  generation.
- Update tests, CI, README, changelog, roadmap, pack docs, generator docs,
  readiness docs, release checklist, and AI-agent guidance in one bundled
  sprint.
- Keep the next-20 planning backlog populated after converting the Godot item.
- Avoid commercial, legal, marketplace-readiness, certification, or similar
  claims.

## Sprint 100 Priorities

Sprint 100 releases the completed `v0.41.0` scope:

- Promote Unreleased changelog entries into `0.41.0`.
- Bump package metadata to `0.41.0`.
- Add v0.41.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.41.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.41.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.41.0 GitHub release when checks pass.
- Close the v0.41.0 milestone after release verification.

## v0.42.0

The `v0.42.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 101 | Complete | Unreal engine and game workspace pack foundation |
| 102 | Complete | v0.42.0 release preparation |

## Sprint 101 Priorities

Sprint 101 implements the next built-in engine and game-workspace pack
foundation:

- Add built-in `verity.pack.unreal`.
- Add strict schemas for `unreal.project`, `unreal.plugin`,
  `unreal.module`, `unreal.target`, `unreal.map`, `unreal.blueprint`,
  `unreal.data-asset`, `unreal.gameplay-tag`, `unreal.input-action`,
  `unreal.scanner`, `unreal.validation-runner`,
  `unreal.readiness-dashboard`, and `unreal.agent-context-exporter`.
- Add readiness gates and reference rules that connect Unreal game projects,
  plugins, modules, targets, maps, Blueprints, data assets, gameplay tags,
  input actions, scanners, validation runners, dashboards, and agent-context
  exporters.
- Add an executable `examples/unreal` game workspace that composes with
  game-core records without moving game design into the core kernel.
- Add Unreal coverage to cross-pack coverage dashboards and schema-bundle
  generation.
- Update tests, CI, README, changelog, roadmap, pack docs, generator docs,
  readiness docs, release checklist, and AI-agent guidance in one bundled
  sprint.
- Keep the next-20 planning backlog populated after converting the Unreal
  item.
- Avoid commercial, legal, marketplace-readiness, certification, or similar
  claims.

## Sprint 102 Priorities

Sprint 102 releases the completed `v0.42.0` scope:

- Promote Unreleased changelog entries into `0.42.0`.
- Bump package metadata to `0.42.0`.
- Add v0.42.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.42.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.42.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.42.0 GitHub release when checks pass.
- Close the v0.42.0 milestone after release verification.

## v0.43.0

The `v0.43.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 103 | Complete | Product-delivery pack foundation for downstream rebuild blockers |
| 104 | Complete | v0.43.0 release preparation and verification |

## Sprint 103 Priorities

Sprint 103 implemented the first built-in product-delivery and
project-management vocabulary needed by downstream spec-driven repositories:

- Added built-in `verity.pack.product-delivery`.
- Added strict schemas for `product.scope`, `commercial.posture`,
  `project-management.model`, `decision.record`, `readiness.profile`,
  `evidence.requirement`, `release.process`, `operations.model`,
  `support.policy`, `maintenance.policy`, `archive.policy`,
  `decommission.policy`, `scanner.capability`, `generator.capability`,
  `validation.runner`, `editor.surface`, and `agent-context.exporter`.
- Added readiness gates and reference rules that connect product scope,
  commercial posture, GitHub-native project management, decision records,
  evidence requirements, release/support/maintenance/operations/archive
  policies, scanners, generators, validation runners, editor surfaces, and
  agent-context exporters.
- Added an executable example workspace for a spec-driven product repository
  that follows: GitHub manages workflow; VeritySpec manages truth.
- Updated tests, CI, README, changelog, roadmap, pack docs, generator docs,
  readiness docs, release checklist, and AI-agent guidance in one bundled
  sprint.
- Recorded the remaining missing lifecycle/mobile/liveops/privacy/evidence kinds
  after this sprint so downstream rebuilds can either proceed or knowingly
  accept a listed gap.
- Kept Unity, Godot, and Unreal engine-specific additions equivalent where the
  concept applies; document explicit exceptions in issues, docs, and tests.
- Avoided commercial, legal, marketplace-readiness, privacy-law,
  app-store-certification, platform-certification, or similar claims.

## Sprint 104 Priorities

Sprint 104 prepares and verifies the v0.43.0 release:

- Verified local tests, pack validation, example validation, graph checks,
  schema-bundle generation, coverage-dashboard generation, package build,
  `twine check`, and installed-wheel smoke tests.
- Confirmed README badges, install tag, latest-release text, changelog,
  roadmap, release notes, downstream workflow pins, and release checklist
  references align to the intended release.
- Cut and verify the v0.43.0 GitHub release if CI is green.
- If hosted checks are unavailable because of billing, quota, credits, or
  platform availability, verify equivalent checks locally and continue with a
  clear PR/release note.

## v0.44.0

The `v0.44.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 105 | Complete | Mobile lifecycle, privacy/store posture, and liveops foundation |
| 106 | Complete | v0.44.0 release preparation and verification |

## Sprint 105 Priorities

Sprint 105 implemented the next built-in lifecycle vocabulary needed by
downstream game repositories and engine-tooling products without making legal,
app-store, platform-certification, privacy-law, or marketplace guarantees:

- Added built-in `verity.pack.mobile` with app release lifecycle, app-store
  metadata/readiness posture, privacy policy evidence references, Apple privacy
  detail records, Google Play Data Safety posture records, ATT/consent
  readiness posture, third-party SDK inventory, ads/IAP monetization posture,
  remove-ads entitlement, soft launch readiness, launch-candidate readiness,
  and compatibility matrices.
- Added built-in `verity.pack.liveops` with liveops configuration, remote
  config bounds, rollback, analytics taxonomy, support categories,
  save-data/schema migration policy, decommissioning, data deletion posture,
  and archive handling.
- Included strict schemas, readiness gates, reference rules, executable
  examples, graph coverage, schema-bundle checks, CI coverage, README/docs,
  changelog, roadmap, release checklist, and AI-agent guidance.
- Kept Unity, Godot, and Unreal parity for engine-adjacent lifecycle concepts
  by adding equivalent `targetsMobileRelease` and `usesLiveOpsConfig` project
  reference rules for all three engine packs.
- Preserved the current non-claim posture: VeritySpec can model readiness
  evidence and decision records, but downstream teams own legal, privacy,
  platform, marketplace, and store-review approvals.

## Sprint 106 Priorities

Sprint 106 prepares and verifies the v0.44.0 release:

- Promoted Unreleased changelog entries into `0.44.0`.
- Bumped package metadata to `0.44.0`.
- Added v0.44.0 release notes.
- Updated README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.44.0`.
- Updated downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.44.0`.
- Ran local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.44.0 GitHub release when checks pass.
- Close the v0.44.0 milestone after release verification.

## v0.45.0

The `v0.45.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 107 | Complete | Progression and evidence pack foundations |
| 108 | Complete | v0.45.0 release preparation and verification |

## Sprint 107 Priorities

Sprint 107 should add the next built-in game/product delivery vocabulary needed
by downstream game, engine-tooling, and implementation-readiness workspaces:

- Add a built-in `verity.pack.progression` foundation with XP, level, unlock,
  progression track, and progression gate records plus executable examples.
- Add a built-in evidence pack foundation for test, CI, build, review,
  screenshot, video, QA, playtest, certification-checklist, and artifact
  evidence records plus an evidence report.
- Include strict schemas, readiness gates, reference rules, executable
  examples, graph coverage, schema-bundle checks, CI coverage, README/docs,
  changelog, roadmap, release checklist, and AI-agent guidance.
- Keep game, engine, mobile, liveops, and product-delivery records connected
  through references instead of expanding core or duplicating pack ownership.
- Preserve the current non-claim posture: VeritySpec can model evidence and
  readiness requirements, but downstream teams own legal, privacy,
  marketplace, platform, certification, support, and store-review approvals.

Sprint 107 delivery added built-in `verity.pack.progression` and
`verity.pack.evidence`, executable progression and evidence examples,
`evidence-report` generation, cross-pack coverage-dashboard support, schema
bundle checks, CI coverage, public docs, changelog entries, release notes, and
AI-agent guidance.

## Sprint 108 Priorities

Sprint 108 prepares and verifies the v0.45.0 release:

- Promote Unreleased changelog entries into `0.45.0`.
- Bump package metadata to `0.45.0`.
- Confirm v0.45.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.45.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.45.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.45.0 GitHub release when checks pass.
- Close the v0.45.0 milestone after release verification.

## v0.46.0

The `v0.46.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 109 | Complete | Installed-pack discovery foundation |
| 110 | Complete | v0.46.0 release preparation and verification |

## Sprint 109 Priorities

Sprint 109 should add the first stable installed-pack discovery contract needed
before specialized packs can move into official extension packages:

- Add a Python package entry-point group for VeritySpec packs.
- Discover installed packs by pack ID while preserving bundled built-in packs.
- Keep explicit local `packPaths`, `--pack-path`, and `verity pack --path`
  precedence over installed packs with the same ID.
- Include installed packs in `verity pack list`, `verity pack validate`,
  workspace validation, readiness, generators, and pack capability indexes.
- Add tests that simulate installed pack entry points without requiring a
  published package.
- Update docs, README, changelog, roadmap, release notes, and AI-agent context
  where relevant.
- Keep separation of existing built-in packs out of scope until compatibility
  metadata, migration guidance, and non-breaking fixtures exist.

Sprint 109 delivery added the `verityspec.packs` Python entry-point group,
installed pack loading by pack ID, source-aware pack summaries, installed-pack
counts in pack capability indexes, local pack path precedence over installed
packs, simulated entry-point tests, release notes, and public pack
documentation. Existing built-in packs remain bundled.

## Sprint 110 Priorities

Sprint 110 prepares and verifies the v0.46.0 release:

- Promote Unreleased changelog entries into `0.46.0`.
- Bump package metadata to `0.46.0`.
- Confirm v0.46.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.46.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.46.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.46.0 GitHub release when checks pass.
- Close the v0.46.0 milestone after release verification.

## v0.47.0

The `v0.47.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 111 | Complete | Specialized-pack separation plan |
| 112 | Complete | v0.47.0 release preparation and verification |

## Sprint 111 Priorities

Sprint 111 defines the first specialized-pack separation plan before any
runtime removal or packaging split:

- Document candidate official extension package names for game, mobile,
  liveops, Unity, Godot, and Unreal packs while preserving existing pack IDs
  and record kinds.
- Define required runtime gates: installed-pack discovery, compatibility
  metadata, official registry policy, detach gating, parity tests, migration
  guidance, and rollback criteria.
- Keep bundled specialized packs available until installed official extension
  packages can prove compatibility and behavior parity.
- Link the plan from README, pack docs, and engine/product-delivery guidance.
- Add documentation contract tests that keep the plan discoverable and preserve
  the no-immediate-removal boundary.
- Update changelog, roadmap, and AI-agent guidance.

Sprint 111 delivery added a public specialized-pack separation plan, candidate
official package names, compatibility metadata and detach-gate requirements,
migration guidance, rollback criteria, public docs links, AI-agent guidance,
and documentation contract tests. Runtime pack separation remains out of scope
until those gates are implemented and proven.

## Sprint 112 Priorities

Sprint 112 prepares and verifies the v0.47.0 release:

- Promote Unreleased changelog entries into `0.47.0`.
- Bump package metadata to `0.47.0`.
- Confirm v0.47.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.47.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.47.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.47.0 GitHub release when checks pass.
- Close the v0.47.0 milestone after release verification.

## v0.48.0

The `v0.48.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 113 | Complete | Accessibility and compliance report golden fixtures |
| 114 | Complete | v0.48.0 release preparation and verification |

## Sprint 113 Priorities

Sprint 113 adds golden fixture coverage for report generators that previously
had shape checks but no committed output contracts:

- Add committed golden outputs for `verity generate accessibility-report`.
- Add committed golden outputs for `verity generate compliance-matrix`.
- Compare CLI-generated outputs to the golden fixtures after normalizing
  volatile fields.
- Compare library-generated report outputs to the same golden fixtures.
- Update changelog and roadmap bookkeeping.

Sprint 113 delivery added committed golden outputs for accessibility reports
and compliance matrices, CLI-level golden comparisons, library-level golden
comparisons, changelog updates, and Next 20 roadmap bookkeeping.

## Sprint 114 Priorities

Sprint 114 prepares and verifies the v0.48.0 release:

- Promote Unreleased changelog entries into `0.48.0`.
- Bump package metadata to `0.48.0`.
- Add v0.48.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.48.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.48.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.48.0 GitHub release when checks pass.
- Close the v0.48.0 milestone after release verification.

## v0.49.0

The `v0.49.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 115 | Complete | External pack maintainer review checklist |
| 116 | Complete | v0.49.0 release preparation and verification |

## Sprint 115 Priorities

Sprint 115 adds a maintainer-facing checklist for reviewing public external
pack proposals:

- Document proposal inputs required before implementation work begins.
- Define identity, contract, executability, documentation, compatibility, PR
  review, and acceptance-outcome gates.
- Link the checklist from README, pack docs, contribution guidance, and the
  pack proposal issue template.
- Add documentation contract tests that keep the checklist discoverable and
  preserve the review boundaries.
- Update changelog and roadmap bookkeeping.
- Keep runtime pack loading, compatibility enforcement, and specialized-pack
  detachment out of scope for this sprint.

Sprint 115 delivery added the external pack maintainer review checklist,
linked it from README, contribution guidance, pack docs, and the pack proposal
issue template, and added documentation contract tests for the checklist's
review boundaries.

## Sprint 116 Priorities

Sprint 116 prepares and verifies the v0.49.0 release:

- Promote Unreleased changelog entries into `0.49.0`.
- Bump package metadata to `0.49.0`.
- Add v0.49.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.49.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.49.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.49.0 GitHub release when checks pass.
- Close the v0.49.0 milestone after release verification.

## v0.50.0

The `v0.50.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 117 | Complete | Release-integrity consistency checks |
| 118 | Complete | v0.50.0 release preparation and verification |

## Sprint 117 Priorities

Sprint 117 adds test-backed release-integrity checks for public version
bookkeeping:

- Read the current package version from `pyproject.toml` and
  `src/verityspec/__init__.py`.
- Verify README release badge, latest-release text, GitHub install command,
  package-version text, and release-notes link match the current version.
- Verify CHANGELOG and current release notes match the current version.
- Verify downstream CI pins, PyPI fallback docs, reusable workflow defaults,
  release checklist tag examples, and maintained GitHub Actions templates match
  the current version.
- Verify evidence fixtures and golden release artifact references match the
  current version.
- Document the release-integrity checks and link them from README and the
  release checklist.
- Update changelog and roadmap bookkeeping.

Sprint 117 delivery added test-backed release-integrity checks, documentation,
README links, release-checklist guidance, and evidence fixture coverage so
public version surfaces are verified against the package version.

## Sprint 118 Priorities

Sprint 118 prepares and verifies the v0.50.0 release:

- Promote Unreleased changelog entries into `0.50.0`.
- Bump package metadata to `0.50.0`.
- Add v0.50.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.50.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.50.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.50.0 GitHub release when checks pass.
- Close the v0.50.0 milestone after release verification.

## v0.51.0

The `v0.51.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 119 | Complete | Roadmap-report Markdown output |
| 120 | Complete | v0.51.0 release preparation and verification |

## Sprint 119 Priorities

Sprint 119 adds Markdown output for roadmap governance reports:

- Add `--format markdown` support to `verity generate roadmap-report`.
- Keep JSON as the default roadmap-report output format and preserve the
  existing JSON contract.
- Include version metadata, summary counts, latest released milestone, active
  milestones, recent milestone and sprint context, and Next 20 roadmap points
  in the Markdown report.
- Reject Markdown output for generator artifacts that do not support it.
- Update tests, README, generator docs, changelog, and roadmap bookkeeping.
- Keep the Next 20 roadmap planning section populated after converting this
  item into sprint work.

Sprint 119 delivery added Markdown output for roadmap governance reports,
preserved JSON as the default report contract, rejected unsupported Markdown
generator requests, included active/recent milestone and Next 20 planning
context in generated Markdown, and updated tests, README commands, generator
docs, changelog, and roadmap bookkeeping.

## Sprint 120 Priorities

Sprint 120 prepares and verifies the v0.51.0 release:

- Promote Unreleased changelog entries into `0.51.0`.
- Bump package metadata to `0.51.0`.
- Add v0.51.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.51.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.51.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.51.0 GitHub release when checks pass.
- Close the v0.51.0 milestone after release verification.

## v0.52.0

The `v0.52.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 121 | Complete | Security-report release evidence gaps |
| 122 | Complete | v0.52.0 release preparation and verification |

## Sprint 121 Priorities

Sprint 121 adds security-report release gaps for verification freshness:

- Add `summary.releaseGaps.staleEvidence` to `verity generate security-report`.
- Add `summary.releaseGaps.missingVerificationDates` to `verity generate
  security-report`.
- Preserve existing `summary.criticalUnverified` behavior for downstream
  compatibility.
- Cover the new release-gap fields with library tests, CLI assertions, and the
  committed security-report golden fixture.
- Update README, generator docs, changelog, roadmap bookkeeping, and Next 20
  planning.

Sprint 121 delivery added `summary.releaseGaps` to security reports with
critical unverified, stale evidence, and missing verification-date lists;
preserved the existing `summary.criticalUnverified` field; updated the
security-report golden fixture; and refreshed README, generator docs,
changelog, roadmap, and Next 20 bookkeeping.

## Sprint 122 Priorities

Sprint 122 prepares and verifies the v0.52.0 release:

- Promote Unreleased changelog entries into `0.52.0`.
- Bump package metadata to `0.52.0`.
- Add v0.52.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.52.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.52.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.52.0 GitHub release when checks pass.
- Close the v0.52.0 milestone after release verification.

## v0.53.0

The `v0.53.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 123 | Complete | Workspace migration impact summaries |
| 124 | Complete | v0.53.0 release preparation and verification |

## Sprint 123 Priorities

Sprint 123 adds migration impact summaries for workspace format upgrades:

- Add step-level impact metadata to `verity migrate --list --format json`.
- Add top-level `impactSummary` output to migration reports for planned paths
  and same-version repair changes.
- Call out workspace-format, record, pack, and generator behavior affected by
  supported migration steps.
- Preserve existing migration report fields for downstream compatibility.
- Cover the impact-summary contract with CLI tests and migration fixtures.
- Update README, migration docs, changelog, roadmap bookkeeping, and Next 20
  planning.

Sprint 123 delivery added step-level migration impacts to migration capability
output, added top-level `impactSummary` output to migration reports, included
impact details in text output, preserved existing report fields, and refreshed
CLI tests, README, migration docs, changelog, roadmap, and Next 20 planning.

## Sprint 124 Priorities

Sprint 124 prepares and verifies the v0.53.0 release:

- Promote Unreleased changelog entries into `0.53.0`.
- Bump package metadata to `0.53.0`.
- Add v0.53.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.53.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.53.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.53.0 GitHub release when checks pass.
- Close the v0.53.0 milestone after release verification.

## v0.54.0

The `v0.54.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 125 | Complete | Issue-code catalog generation |
| 126 | Complete | v0.54.0 release preparation and verification |

## Sprint 125 Priorities

Sprint 125 adds machine-readable issue-code catalog output:

- Add `verity generate issue-code-catalog`.
- Reuse canonical `verity explain` metadata instead of duplicating issue-code
  definitions.
- Include code, category, severity, title, description, resolution, and summary
  counts.
- Keep the generator workspace-free and JSON-only.
- Add deterministic tests and committed golden fixture coverage.
- Update README, generator docs, changelog, roadmap bookkeeping, and Next 20
  planning.

Sprint 125 delivery added `verity generate issue-code-catalog`, reused
canonical `verity explain` metadata, emitted stable JSON with code, category,
severity, title, description, resolution, and summary counts, rejected workspace
paths and non-JSON output, and refreshed CLI tests, library tests, golden
fixtures, README, generator docs, changelog, roadmap, and Next 20 planning.

## Sprint 126 Priorities

Sprint 126 prepares and verifies the v0.54.0 release:

- Promote Unreleased changelog entries into `0.54.0`.
- Bump package metadata to `0.54.0`.
- Add v0.54.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.54.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.54.0`.
- Update future sprint sizing guidance to use cohesive bundles up to roughly
  two weeks of development effort.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.54.0 GitHub release when checks pass.
- Close the v0.54.0 milestone after release verification.

## v0.55.0

The `v0.55.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 127 | Complete | Agent-context and AI governance foundation |
| 128 | Complete | v0.55.0 release preparation and verification |

## Sprint 127 Priorities

Sprint 127 is a two-week-sized governance and design sprint:

- Add an agent-context generation design note for bounded AI handoff
  artifacts before implementing generator behavior.
- Add an architecture decision record process and reusable template for major
  pack, generator, migration, workspace-dependency, and AI-agent decisions.
- Add executable AI-agent adapter drift checks that keep `CODEX.md`,
  `CLAUDE.md`, `GEMINI.md`, and `CHATGPT.md` as thin pointers to `AGENTS.md`.
- Link the new docs from README and keep adapter policy discoverable from the
  canonical agent entry point.
- Update changelog, roadmap, and Next 20 planning.

Sprint 127 delivery added the agent-context generation design note, ADR
process documentation, ADR template, README links, changelog and roadmap
bookkeeping, and executable tests that keep AI-agent adapter files as thin
pointers to `AGENTS.md`.

## Sprint 128 Priorities

Sprint 128 prepares and verifies the v0.55.0 release:

- Promote Unreleased changelog entries into `0.55.0`.
- Bump package metadata to `0.55.0`.
- Add v0.55.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.55.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.55.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.55.0 GitHub release when checks pass.
- Close the v0.55.0 milestone after release verification.

## v0.56.0

The `v0.56.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 129 | Complete | Engine full-lifecycle support design |
| 130 | Complete | v0.56.0 release preparation and verification |

## Sprint 129 Priorities

Sprint 129 is a two-week-sized design sprint:

- Add public design guidance for Unity, Godot, and Unreal game workspaces
  across concept, prototype, production, release, liveops, maintenance,
  decommissioning, and archive stages.
- Cover shared engine library workspaces, integration workspaces, portfolio
  examples, lifecycle readiness profiles, evidence, liveops, decommissioning,
  and archive records.
- Preserve engine parity expectations and pack/core boundaries without making
  commercial, legal, privacy-law, marketplace, platform-certification, or
  store-review claims.
- Link the new design note from README and keep the design boundary
  executable through documentation tests.
- Update changelog, roadmap, and Next 20 planning.

Sprint 129 delivery added engine full-lifecycle support design guidance for
Unity, Godot, Unreal, shared engine library workspaces, engine toolkit
workspaces, game workspaces, integration workspaces, portfolio examples,
lifecycle stages, readiness profiles, evidence, liveops, decommissioning,
archive, agent-context boundaries, README links, changelog and roadmap
bookkeeping, and executable documentation tests.

## Sprint 130 Priorities

Sprint 130 prepares and verifies the v0.56.0 release:

- Promote Unreleased changelog entries into `0.56.0`.
- Bump package metadata to `0.56.0`.
- Add v0.56.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.56.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist, and
  workflow release pins to `v0.56.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.56.0 GitHub release when checks pass.
- Close the v0.56.0 milestone after release verification.

## v0.57.0

The `v0.57.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 131 | Complete | Multi-workspace portfolio validation foundation |
| 132 | Complete | v0.57.0 release preparation and verification |

## Sprint 131 Priorities

Sprint 131 is a two-week-sized portfolio validation foundation sprint:

- Add a portfolio-level validation design note for multi-workspace product,
  service, library, game, engine-toolkit, shared-library, integration, and
  portfolio workspaces before implementing aggregate reports.
- Add an executable `examples/portfolio` workspace that uses built-in
  product-delivery records to model local-only portfolio validation posture.
- Document engine portfolio guidance for Unity, Godot, Unreal, game-core,
  game-assets, product-delivery, evidence, mobile, and liveops workspaces
  without adding a portfolio CLI command or dependency resolver.
- Define transitional fixture expectations for integration workspaces,
  exported-record examples, dependency aliases, readiness summaries, evidence
  summaries, impact warnings, and future aggregate report boundaries.
- Preserve the boundary that portfolio records do not make commercial, legal,
  privacy-law, marketplace, platform-certification, app-store, pricing,
  store-review, or support-SLA claims.
- Link the new docs and example from README, add executable documentation and
  example tests, and keep changelog, roadmap, and Next 20 planning aligned.

Sprint 131 delivery added portfolio-level validation foundation guidance,
`examples/portfolio`, README links, changelog and roadmap bookkeeping, an
updated workspace compatibility manifest, and executable tests that keep the
portfolio guidance, example, and roadmap report from drifting.

## Sprint 132 Priorities

Sprint 132 prepares and verifies the v0.57.0 release:

- Promote Unreleased changelog entries into `0.57.0`.
- Bump package metadata to `0.57.0`.
- Add v0.57.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.57.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist,
  workflow release pins, and evidence fixtures to `v0.57.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.57.0 GitHub release when checks pass.
- Close the v0.57.0 milestone after release verification.

## v0.58.0

The `v0.58.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 133 | Complete | Fixture refresh documentation and golden drift review |
| 134 | Complete | v0.58.0 release preparation and verification |

## Sprint 133 Priorities

Sprint 133 is a two-week-sized fixture refresh documentation sprint:

- Add public fixture refresh documentation for regenerating golden report
  outputs with deterministic timestamps.
- Document current golden fixture locations, regeneration commands, placeholder
  normalization, and JSON formatting review.
- Define intentional output drift review before committed golden fixtures are
  updated.
- Capture release-version fixture update rules for evidence, coverage,
  README, downstream pins, release notes, and release checklist surfaces.
- Add a maintainer checklist for fixture refresh PRs and release prep.
- Link the new guidance from README, generator docs, and release checklist.
- Add executable documentation tests and keep changelog, roadmap, and Next 20
  planning aligned.

Sprint 133 delivery added fixture refresh guidance, README/generator/release
checklist links, deterministic timestamp and placeholder-normalization
instructions, release-version fixture update guidance, changelog and roadmap
bookkeeping, and executable documentation tests that keep the guide and roadmap
report from drifting.

## Sprint 134 Priorities

Sprint 134 prepares and verifies the v0.58.0 release:

- Promote Unreleased changelog entries into `0.58.0`.
- Bump package metadata to `0.58.0`.
- Add v0.58.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.58.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist,
  workflow release pins, and evidence fixtures to `v0.58.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.58.0 GitHub release when checks pass.
- Close the v0.58.0 milestone after release verification.

## v0.59.0

The `v0.59.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 135 | Complete | Profile-aware downstream CI template examples |
| 136 | Complete | v0.59.0 release preparation and verification |

## Sprint 135 Priorities

Sprint 135 is a two-week-sized downstream CI profile sprint:

- Add a `profile` input to the reusable product-contract workflow.
- Pass the selected profile through to `verity validate`, `verity lint`,
  `verity readiness`, and `verity doctor` while keeping no-profile downstream
  behavior compatible.
- Add a maintained profile-aware GitHub Actions template covering release,
  regulated, public API, and internal-tool workspace examples.
- Document how downstream repositories should choose profiles without making
  commercial, legal, privacy-law, marketplace, platform-certification,
  app-store, store-review, pricing-approval, or support-SLA claims.
- Add tests that keep profile-aware templates pinned to the current release
  tag and verify profile names, reusable workflow wiring, docs, and roadmap
  report expectations.
- Keep README, changelog, release checklist, ROADMAP, and Next 20 planning
  aligned.

Sprint 135 delivery added profile-aware reusable downstream workflow support,
a maintained profile matrix template, downstream documentation for release,
regulated, public API, and internal-tool checks, explicit non-claims guidance,
and tests that keep profile wiring, template pins, docs, and roadmap report
expectations aligned.

## Sprint 136 Priorities

Sprint 136 prepares and verifies the v0.59.0 release:

- Promote Unreleased changelog entries into `0.59.0`.
- Bump package metadata to `0.59.0`.
- Add v0.59.0 release notes.
- Update README release badge, latest-release text, install tag,
  package-version text, and release-notes link to `v0.59.0`.
- Update downstream CI templates, PyPI fallback docs, release checklist,
  workflow release pins, and evidence fixtures to `v0.59.0`.
- Run local release verification, package build checks, `twine check`, wheel
  smoke tests, and GitHub Actions.
- Tag and publish the v0.59.0 GitHub release when checks pass.
- Close the v0.59.0 milestone after release verification.

## v0.60.0

The `v0.60.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 137 | Complete | Deployment-target release evidence links |

## Sprint 137 Priorities

Sprint 137 completed a two-week-sized deployment evidence sprint:

- Add release evidence link fields to `deployment.target` records for security
  controls, observability dashboards, compliance mappings, and evidence
  records.
- Extend production deployment readiness so release controls include linked
  security, observability, compliance, and evidence records.
- Add deployment-owned reference rules that keep cross-pack links graph-valid
  without moving those surfaces into core.
- Update `examples/deployment` and cross-pack coverage fixtures so deployment
  evidence links validate, lint, pass readiness, and appear in graph output.
- Extend `verity generate deployment-report` with linked evidence/control
  summaries and release-gap fields.
- Add tests for report output, readiness gaps, missing references, golden
  fixture drift, and example compatibility.
- Update README, changelog, deployment pack docs, ROADMAP, and Next 20
  planning.

## v0.61.0

The `v0.61.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 138 | Complete | Coverage-dashboard Markdown output |

## Sprint 138 Priorities

Sprint 138 completed a two-week-sized coverage-dashboard Markdown sprint:

- Add Markdown output to `verity generate coverage-dashboard` for maintainers
  who need a human-readable release-review artifact.
- Preserve the existing JSON coverage-dashboard contract for CI and downstream
  tooling.
- Keep coverage-dashboard metadata, CLI format handling, golden fixtures, and
  unsupported-format errors deterministic and tested.
- Document that coverage-dashboard Markdown is an internal release-review
  artifact and does not make legal, commercial, privacy-law,
  platform-certification, marketplace, app-store, store-review,
  pricing-approval, or support-SLA claims.
- Update README, changelog, generator docs, CI docs, release checklist,
  fixture-refresh guidance, ROADMAP, and Next 20 planning.

## v0.62.0

The `v0.62.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 139 | Complete | Local workspace dependency prototype |

## Sprint 139 Priorities

Sprint 139 made the first cross-workspace dependency behavior executable while
keeping the boundary local, readonly, and direct:

- Add optional workspace `dependencies` support for local path dependencies.
- Resolve alias-qualified references such as
  `sharedUnity::unity.package.save_system`.
- Validate dependency source paths, workspace IDs, versions, aliases, missing
  dependency records, and manifest-level exported-record boundaries.
- Include exported dependency records and dependency metadata in graph JSON
  output.
- Add positive and negative fixtures for a Unity game workspace consuming a
  shared Unity runtime workspace.
- Keep lockfiles, remote registries, Git authentication, transitive dependency
  behavior, and record-level visibility fields out of this first prototype.
- Update tests, README, workspace-format docs, graph docs, cross-workspace
  dependency docs, versioning docs, changelog, ROADMAP, and issue-code
  catalog fixtures.

## v0.63.0

The `v0.63.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 140 | Complete | Engine portfolio compatibility fixtures |

## Sprint 140 Priorities

Sprint 140 completed a two-week-sized engine portfolio compatibility sprint:

- Add local-only fixtures that show Unity, Godot, Unreal, and a shared
  exported game-core workspace side by side.
- Use the local readonly workspace dependency model with a shared dependency
  alias instead of introducing a portfolio resolver or report command.
- Prove that each fixture workspace passes validation, strict lint, strict
  readiness, and graph checks.
- Document the fixture boundary, command set, engine parity expectation, and
  non-claims before aggregate portfolio-report work begins.
- Link the fixture from README and portfolio validation guidance.
- Keep changelog, ROADMAP, tests, and Next 20 planning aligned.

Sprint 140 delivery added local Unity, Godot, Unreal, shared game-core, and
portfolio fixture workspaces under `tests/fixtures/engine_portfolio`, documented
the dependency-alias and engine-parity boundary, linked the fixture from README
and portfolio guidance, and added regression coverage for validation, strict
lint, strict readiness, graph nodes, graph edges, and roadmap report
bookkeeping.

## v0.64.0

The `v0.64.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 141 | Complete | Lifecycle readiness gap reports |

## Sprint 141 Priorities

Sprint 141 completed a two-week-sized lifecycle readiness report sprint:

- Added a product-delivery, mobile, and liveops lifecycle readiness gap report
  for implementation-ready, soft-launch, launch-candidate, remote-config,
  rollback, support, save-migration, decommission, data-deletion, and
  archive-review summaries.
- Kept the report as a VeritySpec record coverage and gap artifact, without
  making commercial, legal, privacy-law, marketplace, app-store,
  platform-certification, live-service, support, or archival readiness claims.
- Added an executable cross-pack `examples/lifecycle-readiness` workspace.
- Advertised the generator from the relevant product-delivery, mobile, and
  liveops pack metadata without moving the behavior into the small core.
- Added CLI, library, golden fixture, example compatibility, and pack validation
  coverage.
- Updated README, generator docs, pack docs, CI guidance, release checklist,
  fixture-refresh guidance, changelog, roadmap, and canonical AI-agent
  commands.

Sprint 141 delivery added `verity generate lifecycle-readiness-report`, a
cross-pack lifecycle readiness example, product-delivery/mobile/liveops
generator metadata, committed golden output, compatibility-manifest coverage,
claim-boundary documentation, and release-bookkeeping updates for the v0.64.0
release.

## v0.65.0

The `v0.65.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 142 | Complete | Installed-pack health diagnostics |

## Sprint 142 Priorities

Sprint 142 completed a two-week-sized installed-pack diagnostics sprint:

- Added a public `verity pack doctor` command that reports pack discovery health
  without aborting on the first installed or local pack failure.
- Reported installed `verityspec.packs` entry-point load failures, missing or
  invalid manifests, entry-point name mismatches, duplicate installed pack IDs,
  and installed pack IDs that collide with built-in packs.
- Reported local external pack path failures, invalid manifests, duplicate local
  pack IDs, and local pack IDs that collide with built-in packs.
- Explained explicit local override behavior where `packPaths`, `--pack-path`,
  or `verity pack --path` entries take precedence over installed packs with
  the same ID.
- Kept existing strict pack loading behavior compatible for `verity pack list`,
  `verity pack validate`, workspace validation, readiness, graph, and
  generator commands.
- Updated tests, README, pack docs, CI guidance, release checklist, changelog,
  roadmap bookkeeping, and canonical AI-agent commands.
- Kept bundled specialized packs in place; this sprint is diagnostic
  groundwork for future official extension packages, not a detach sprint.

Sprint 142 delivery added `verity pack doctor`, installed/local pack discovery
health reports with text and JSON output, stable issue-code explanations,
issue-code catalog fixture coverage, external-pack review guidance, release
checklist coverage, and release-bookkeeping updates for the v0.65.0 release.

## v0.66.0

The `v0.66.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 143 | Complete | Official-extension package compatibility fixtures |

## Sprint 143 Priorities

Sprint 143 completed a two-week-sized official-extension compatibility
fixture sprint:

- Add a `verity pack compare <pack-id> --mirror <path>` command that compares a
  loaded source pack with a mirror pack path without loading the mirror into
  the active registry.
- Add an official-extension mirror fixture for `verityspec-pack-unity` that
  preserves the bundled `verity.pack.unity` manifest, schemas, readiness gates,
  reference rules, and generator metadata.
- Prove that mirror comparison detects drift in manifest identity, schema
  declarations, schema JSON content, readiness gates, reference rules, and
  generator metadata.
- Document the fixture contract, command set, acceptance gate, and non-goals
  before any bundled pack detach sprint begins.
- Preserve existing built-in pack collision protection. This sprint must not
  detach bundled packs, publish official extension packages, or allow arbitrary
  installed packages to shadow built-in pack IDs.
- Update tests, README, pack docs, CI guidance, release checklist, changelog,
  roadmap bookkeeping, and canonical AI-agent commands.

Sprint 143 delivery added `verity pack compare`, text and JSON official-extension
mirror reports, stable mirror issue-code explanations, a Unity mirror fixture
for future `verityspec-pack-unity` compatibility checks, documentation for the
fixture contract and non-goals, CI/release-checklist guidance, README command
coverage, and release-bookkeeping updates for the v0.66.0 release.

## v0.67.0

The `v0.67.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 144 | Complete | CLI command module decomposition design |

## Sprint 144 Priorities

Sprint 144 completed a two-week-sized CLI command module decomposition
design sprint:

- Add a public CLI command module decomposition design note before larger
  dependency, portfolio, lifecycle, and agent-context command families expand
  the CLI.
- Define proposed `verityspec.commands` module boundaries, command
  registration flow, shared output/error helpers, migration phases, and
  compatibility guardrails.
- Preserve current runtime behavior. This sprint must not move command
  implementations, change public command names, change arguments, change
  output formats, change exit codes, or introduce a new CLI framework.
- Link the design note from README and relevant developer docs.
- Add tests that keep the design note discoverable and preserve the non-goal
  boundary.
- Update changelog and roadmap bookkeeping.

Sprint 144 delivery added the CLI command module decomposition design note,
README and developer-doc links, regression tests for discoverability,
compatibility surfaces, and non-goals, next-roadmap rotation, and
release-bookkeeping updates for the v0.67.0 release.

## v0.68.0

The `v0.68.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 145 | Complete | Installed-pack compatibility metadata design |

## Sprint 145 Priorities

Sprint 145 should complete a two-week-sized installed-pack compatibility
metadata design sprint:

- Add a public installed-pack compatibility metadata design note before
  runtime enforcement, official extension package publication, or bundled-pack
  detach gates are implemented.
- Define the proposed metadata shape for supported VeritySpec versions,
  workspace format versions, pack API level, and official extension-package
  lifecycle states.
- Document discovery and source-precedence interaction with `verityspec.packs`,
  local `packPaths`, built-in pack ID reservation, and future official detach
  gates.
- Define staged adoption, validation intent, migration/rollback posture, and
  non-goals that preserve current runtime behavior.
- Link the design note from README, pack distribution docs, specialized-pack
  separation guidance, official-extension fixture guidance, ADR guidance, and
  branching guidance.
- Add tests that keep the design note discoverable and preserve the
  no-runtime-enforcement boundary.
- Update changelog and roadmap bookkeeping.

Sprint 145 delivery added the installed-pack compatibility metadata design
note, README and pack architecture links, staged adoption guidance, official
extension-package lifecycle states, regression tests for discoverability and
runtime non-goals, next-roadmap rotation, and release-bookkeeping updates for
the v0.68.0 release.

## v0.69.0

The `v0.69.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 146 | Complete | Release automation guidance artifact |

## Sprint 146 Priorities

Sprint 146 should complete a two-week-sized release automation guidance
sprint:

- Add a single post-tag release verification checklist artifact for maintainers
  and AI agents.
- Document GitHub release workflow evidence after tag pushes.
- Document GitHub release asset verification, including wheel and source
  distribution hashes.
- Document the expected skipped PyPI publish state when PyPI publishing has
  not been explicitly requested.
- Document downloaded wheel and public GitHub tag install smoke tests.
- Document issue and milestone closure evidence after public release
  verification.
- Link the checklist from README, release checklist, release-integrity, CI, and
  branching guidance.
- Add tests that keep the checklist discoverable and preserve the required
  evidence categories.
- Update changelog and roadmap bookkeeping.

Sprint 146 delivery added the post-tag release verification checklist,
README and release-process links, release-integrity coverage for the new
current-tag checklist surface, regression tests for required evidence
categories, next-roadmap rotation, and release-bookkeeping updates for the
v0.69.0 release.

## v0.70.0

The `v0.70.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 147 | Complete | Security-report Markdown output |

## Sprint 147 Priorities

Sprint 147 should complete a two-week-sized security-report Markdown sprint:

- Add Markdown output to `verity generate security-report` for maintainers who
  need a human-readable release-review artifact.
- Preserve the existing JSON security-report contract for CI, downstream
  tooling, and golden fixture consumers.
- Include generated-at, VeritySpec version, workspace metadata, summary
  counts, coverage counts, risk counts, release gaps, and per-control
  verification details in the Markdown report.
- Keep stale evidence, missing verification dates, and critical unverified
  controls visible in the release-gap table.
- Update security pack generator metadata to advertise both JSON and Markdown
  output formats.
- Add CLI, library, and golden fixture coverage for the Markdown output.
- Update README, generator docs, security-pack docs, CI guidance, release
  checklist, fixture-refresh docs, and agent command references.
- Keep the Markdown output framed as an internal release-review artifact
  without legal, compliance, privacy-law, security-certification,
  penetration-test, marketplace, app-store, platform-certification,
  pricing-approval, support-SLA, or production-readiness claims.
- Update changelog and roadmap bookkeeping.

Sprint 147 delivery added security-report Markdown output, JSON contract
preservation, security pack generator metadata for JSON and Markdown, CLI,
library, and golden Markdown coverage, CI and release-checklist command
coverage, README and docs updates, canonical agent feedback-loop guidance,
clean-on-main open-issue sweep guidance, next-roadmap rotation, and
release-bookkeeping updates for the v0.70.0 release.

## v0.71.0

The `v0.71.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 148 | Complete | Engine evidence traceability |

## Sprint 148 Priorities

Sprint 148 should complete a two-week-sized engine evidence traceability
sprint:

- Add parity-aware evidence reference rules so test evidence can directly
  prove Unity project and scene records, Godot project and scene records, and
  Unreal project and map records.
- Add build evidence reference rules so build evidence can directly prove
  Unity build-target records, Godot export-preset records, and Unreal target
  records.
- Keep Unity validation-runner evidence parity explicit with Godot and Unreal
  validation-runner `producesEvidence` behavior.
- Update the Unity, Godot, and Unreal executable examples with evidence
  records that prove concrete engine implementation and build/export records.
- Document that skipped or inconclusive engine checks should use
  `evidence.test.result` with the normal `proves` relationship instead of
  downstream-only relationship names such as `provesGap`.
- Update README, engine pack docs, evidence docs, changelog, roadmap, tests,
  and release bookkeeping.

Sprint 148 delivery added parity-aware engine evidence reference rules,
executable Unity/Godot/Unreal evidence examples, validation-runner evidence
links, workspace compatibility manifest updates, README and pack docs updates,
next-roadmap preservation, and release-bookkeeping updates for the v0.71.0
release.

## v0.72.0

The `v0.72.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 149 | Complete | Migration-report JSON Schema documentation |

## Sprint 149 Priorities

Sprint 149 should complete a two-week-sized migration-report schema
documentation sprint:

- Add a public migration-report JSON Schema for `verity migrate --format json`
  and `verity migrate --report-out` outputs.
- Document stable fields for migration paths, impact summaries, changes,
  files written, manual follow-up, and blocked migration reports.
- Validate real successful, dry-run, report-out, future-version blocked,
  unsupported-target blocked, and no-path blocked reports against the schema.
- Link the schema documentation from README, workspace-format docs, and
  versioning/migration docs.
- Keep runtime migration behavior unchanged unless tests reveal a documented
  report field is missing.
- Update changelog, roadmap bookkeeping, and Next 20 planning.

Sprint 149 delivery added a public migration-report JSON Schema, schema
documentation for workspace migration reports, blocked-report exit-code
guidance, CI and README links, executable schema validation tests for real
successful and blocked `verity migrate` outputs, next-roadmap rotation, and
release-bookkeeping updates for the v0.72.0 release. It also aligned the
canonical AI-agent entry point with the organization-wide entry-point baseline
so VeritySpec agents preserve the same patterns/glossary, work-ledger,
context-refresh, and approval-gate discipline used across the organization.

## v0.73.0

The `v0.73.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 150 | Complete | Device/runtime smoke validation runners |

## Sprint 150 Priorities

Sprint 150 should complete a two-week-sized engine validation-runner semantics
sprint:

- Add a parity-aware `device-smoke` validation-runner mode for Unity, Godot,
  and Unreal records.
- Allow `device-smoke` runners to omit `scannerRefs` or use an empty
  `scannerRefs` list when they validate a built artifact or physical-device
  runtime directly.
- Keep scanner-backed runner types strict: non-device-smoke validation runners
  must still declare scanner references.
- Add runtime validation graph links from engine validation runners to Unity
  build targets, Godot export presets, and Unreal targets.
- Add test-evidence proof rules and executable Unity, Godot, and Unreal
  examples for runtime smoke validation.
- Update engine pack docs, readiness docs, README, changelog, tests, golden
  fixtures, and release bookkeeping.

Sprint 150 delivery added parity-aware `device-smoke` validation-runner
semantics for Unity, Godot, and Unreal, preserving strict scanner references
for scanner-backed runner types while allowing direct runtime smoke checks to
omit scanner records. It also added runtime validation graph links, test
evidence proof rules, executable engine examples, readiness and pack docs,
issue-code explanations, Unity official-extension mirror alignment, and an
explicit AI entry-point baseline clarification for all organization agents.

## v0.74.0

The `v0.74.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 151 | Complete | Issue-code catalog Markdown output |

## Sprint 151 Priorities

Sprint 151 should add documentation-site-friendly issue-code catalog output
without changing the existing JSON contract:

- Add `--format markdown` support for `verity generate issue-code-catalog`.
- Keep `issue-code-catalog` as a no-workspace generator and continue rejecting
  workspace paths.
- Preserve JSON as the machine-readable issue-code catalog contract.
- Add a Markdown renderer with release metadata, summary counts, severity and
  category tables, and issue-code rows.
- Add CLI coverage, library coverage, and a golden Markdown fixture.
- Update README, generator docs, fixture-refresh docs, release checklist,
  changelog, roadmap bookkeeping, and release notes.

Sprint 151 delivery added Markdown output for `verity generate
issue-code-catalog`, preserving JSON as the machine-readable contract while
giving documentation sites, maintainers, CI diagnostics, and agent workflows a
human-readable issue-code catalog with release metadata, summary counts,
severity and category tables, and issue-code rows. It also kept
`issue-code-catalog` workspace-free, added CLI and library coverage, added a
golden Markdown fixture, updated generator and fixture-refresh docs, and
aligned README, release checklist, changelog, roadmap, and release notes for
the v0.74.0 release.

## v0.75.0

The `v0.75.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 152 | Complete | Agent-context generator prototype |

## Sprint 152 Priorities

Sprint 152 should add the first bounded agent-context generator prototype:

- Add `verity generate agent-context WORKSPACE --record RECORD_ID --format
  markdown`.
- Support `agent-context.exporter`, `unity.agent-context-exporter`,
  `godot.agent-context-exporter`, and `unreal.agent-context-exporter` target
  records.
- Use existing workspace loading, pack loading, semantic validation, and graph
  behavior without inventing records or silently ignoring validation errors.
- Emit a deterministic Markdown handoff with workspace identity, target
  exporter metadata, relevant records, graph links, generated artifacts,
  deprecated or removed selected records, safety boundaries, and verification
  commands.
- Preserve `AGENTS.md` as the canonical repository entry point and avoid
  overstating agent autonomy, implementation correctness, or readiness.
- Add CLI coverage, library coverage, a golden Markdown fixture, README,
  generator docs, fixture-refresh guidance, release checklist coverage,
  changelog, and roadmap bookkeeping.

Sprint 152 delivery added the first Markdown `verity generate agent-context`
prototype for product-delivery and engine agent-context exporter records. It
uses existing workspace loading, pack loading, validation, and graph behavior;
fails on validation errors; selects target, included-kind, and graph-connected
records; emits safety boundaries and verification commands; advertises the
generator in product-delivery, Unity, Godot, and Unreal pack metadata; adds the
Unity official-extension mirror update; and includes CLI, library, golden
fixture, README, docs, release checklist, changelog, roadmap, and release-note
bookkeeping for v0.75.0.

## v0.76.0

The `v0.76.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 153 | Complete | Decision-record index generator |

## Sprint 153 Priorities

Sprint 153 should complete a two-week-sized decision-index generator sprint:

- Add `verity generate decision-index WORKSPACE` for product-delivery
  `decision.record` records.
- Support JSON and Markdown output for ADR and governance review.
- Summarize decision records by decision status, record lifecycle status,
  decision type, and owner.
- Include decision graph links, supersession metadata, references, and index
  gaps for accepted decisions without `decidedAt`, proposed decisions,
  superseded decisions, and decisions with no graph links.
- Register the generator in `verity.pack.product-delivery` metadata and pack
  validation.
- Add CLI coverage, library coverage, golden JSON and Markdown fixtures,
  README, generator docs, ADR docs, product-delivery docs, fixture-refresh
  guidance, release checklist coverage, changelog, and roadmap bookkeeping.

Sprint 153 delivery added `verity generate decision-index` for
product-delivery `decision.record` records. It emits deterministic JSON and
Markdown reports for ADR and governance review, summarizes decisions by
decision status, record status, decision type, and owner, includes graph-link
and supersession details, reports index gaps for accepted, proposed,
superseded, and orphaned decisions, advertises the generator in
`verity.pack.product-delivery`, and includes CLI, library, golden fixture,
README, generator docs, ADR docs, product-delivery docs, fixture-refresh
guidance, release checklist, changelog, roadmap, and release-note bookkeeping
for v0.76.0.

## v0.77.0

The `v0.77.0` milestone is released.

| Sprint | Status | Focus |
|---:|---|---|
| 154 | Complete | Downstream AI-adapter drift-check guidance |

## Sprint 154 Priorities

Sprint 154 should document downstream AI-adapter drift checks for sibling
repositories that maintain agent-specific adapter files:

- Add guidance for keeping `CODEX.md`, `CLAUDE.md`, `CHATGPT.md`,
  `GEMINI.md`, `UNITY_AI.md`, `.github/copilot-instructions.md`, and similar
  files as thin pointers to the canonical repository `AGENTS.md`.
- Anchor the guidance to
  `organization-patterns/patterns/ai-entry-point-baseline.md`.
- Provide a practical audit checklist for sibling repositories.
- Preserve the boundary that adapters must not contain independent branch,
  test, release, VeritySpec, product, or approval policy.
- Add documentation tests, README links, changelog, and roadmap bookkeeping.

Sprint 154 delivery added downstream AI-adapter drift-check guidance for
sibling repositories. The new guide keeps Codex, Claude, ChatGPT, Gemini,
Unity AI, GitHub Copilot, and similar adapter files as thin pointers to
`AGENTS.md`, anchors the audit checklist to the organization
`ai-entry-point-baseline` pattern, documents review commands and boundaries,
expands adapter governance tests to include Unity AI and GitHub Copilot
adapters, links the guide from the README, and keeps changelog, roadmap, and
release-note bookkeeping aligned for v0.77.0.

## Product Goal: Core Runtime and Official Extension Packs

VeritySpec should evolve toward a smaller core runtime plus official extension
pack packages. The `verityspec` package should remain the executable contract
engine: CLI, workspace loading, schema validation, semantic validation,
readiness, graphing, diffing, migration, generator dispatch, pack validation,
and external-pack discovery.

Broad product-contract packs can stay close to the core while their behavior is
still stabilizing. Domain-heavy packs such as game, mobile, liveops, Unity,
Godot, and Unreal should eventually be separable into official extension
packages once VeritySpec has a stable installed-pack discovery contract, pack
compatibility metadata, migration guidance, and downstream workspace fixtures
that prove separated packs behave the same as bundled packs.

This is a product direction, not an immediate removal plan. Existing bundled
packs should remain available until the extension-pack architecture can support
users without manual `packPaths` or workspace breakage.

## Next 20 Roadmap Points

These points define the next backlog once the active roadmap is caught up. They
are planning inputs, not release commitments. Convert each point into a GitHub
issue and milestone before implementation begins.

AI agents must keep this section populated with up to 20 concrete points when
the active roadmap is caught up. The points should balance fixes,
improvements, continuation work, and expansion. When points are converted into
sprint issues or milestones, replace them with new future planning inputs so
the roadmap does not drift into an empty backlog.

1. Add lifecycle-readiness fixture planning for the first engine
    implementation slice after the engine full-lifecycle design note is
    reviewed, with Unity, Godot, and Unreal parity expectations documented up
    front.
2. Add portfolio report JSON contract planning after the portfolio validation
    foundation is reviewed, including workspace inventory, validation status,
    readiness status, impact warnings, evidence gaps, and agent-context refresh
    needs.
3. Add golden-fixture refresh automation planning after fixture refresh
    documentation is adopted, including dry-run diff summaries, generator
    allowlists, placeholder preservation, and maintainer approval gates before
    any rewrite command ships.
4. Add downstream CI profile artifact guidance for preserving validation
    reports, doctor reports, graph outputs, and profile-specific evidence
    bundles across release, regulated, public API, and internal-tool workflows.
5. Add deployment-report Markdown output after linked release evidence fields
    stabilize so operations and release reviewers can read deployment evidence
    summaries without opening JSON.
6. Add evidence-report Markdown output for implementation and release proof
    review once evidence-report JSON fields stabilize.
7. Add dependency lockfile planning and a deterministic local
    `verity deps lock` prototype after local dependency validation and graph
    semantics stabilize.
8. Add dependency-aware product-impact planning for local workspace
    dependencies so future impact reports can explain which consuming
    workspaces and engine records are affected by exported shared-contract
    changes.
9. Add lifecycle-readiness report Markdown output or JSON Schema
    documentation after the JSON lifecycle report contract stabilizes, so
    release reviewers and downstream CI integrations can consume the report
    without depending on ad hoc interpretation.
10. Add installed-pack diagnostics JSON Schema documentation after
    `verity pack doctor` stabilizes, so CI systems and future official
    extension package mirrors can consume pack-health reports without ad hoc
    interpretation.
11. Add official-extension mirror fixture expansion planning for game, mobile,
    liveops, Godot, and Unreal packs after the Unity mirror comparison
    contract stabilizes.
12. Add a first low-risk CLI command movement sprint after the CLI command
    module decomposition design note is reviewed, starting with `verity
    explain` or `verity diff` and proving unchanged parser, output, and
    exit-code behavior.
13. Add optional installed-pack compatibility diagnostics planning after the
    metadata design note is reviewed, including JSON issue shape, warning
    severity, package-version range parsing, workspace-format matching, and
    built-in fallback behavior.
14. Add release evidence bundle planning after post-tag release verification
    guidance is adopted, including a machine-readable summary shape that can
    preserve workflow URLs, release asset hashes, install smoke results,
    closed issue and milestone IDs, and CI fallback decisions.
15. Add expanded security-report Markdown fixture scenarios after the initial
    Markdown output is adopted, covering critical unverified controls, stale
    evidence, missing verification dates, and empty security-control
    workspaces.
16. Add PrismSpec importer migration-report JSON Schema documentation after the
    workspace migration-report schema is adopted, clearly distinguishing
    historical importer reports from workspace format migration reports.
17. Add issue-code catalog JSON Schema documentation after Markdown publishing
    support is adopted, so documentation sites and CI integrations can validate
    the machine-readable catalog contract explicitly.
18. Add agent-context JSON output planning after the Markdown prototype
    stabilizes, including a machine-readable contract shape for records, graph
    links, safety boundaries, verification commands, and future downstream CI
    integrations.
19. Add decision-index JSON Schema documentation after the JSON and Markdown
    decision-index outputs stabilize, so ADR dashboards, docs sites, and
    downstream CI can validate the machine-readable decision index contract.
20. Add AI entry-point drift report planning after downstream adapter guidance
    is adopted, including adapter inventory, baseline coverage, drift
    findings, and follow-up issue recommendations for sibling repositories.

## Working Rule

No sprint is complete unless:

- Tests pass.
- CI passes.
- Documentation and examples match the implemented behavior.
- New behavior has at least one executable test or CLI smoke check.
- When the active roadmap has been caught up, `ROADMAP.md` keeps up to 20
  future planning points for fixing, improving, continuing, and expanding the
  project.
