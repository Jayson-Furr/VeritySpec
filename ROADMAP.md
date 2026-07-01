# VeritySpec Sprint Roadmap

VeritySpec matures through shippable sprints. Plan sprints as cohesive bundles
of related work sized up to roughly one week of development effort, while
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

## Next 20 Roadmap Points

These points define the next backlog once the active roadmap is caught up. They
are planning inputs, not release commitments. Convert each point into a GitHub
issue and milestone before implementation begins.

AI agents must keep this section populated with up to 20 concrete points when
the active roadmap is caught up. The points should balance fixes,
improvements, continuation work, and expansion. When points are converted into
sprint issues or milestones, replace them with new future planning inputs so
the roadmap does not drift into an empty backlog.

1. Add a built-in `verity.pack.product-delivery` foundation with product
   scope, project-management model, decision record, readiness profile,
   evidence requirement, release process, support policy, maintenance policy,
   scanner capability, generator capability, validation runner, editor
   surface, and agent-context exporter records plus an executable example.
2. Add a built-in `verity.pack.progression` foundation with XP, level,
   unlock, progression track, and progression gate records plus executable
   examples.
3. Add golden fixtures for accessibility and compliance report outputs after
   their report shapes stabilize.
4. Add a maintainer review checklist for accepting external packs once public
   pack proposals become common.
5. Add release-integrity consistency checks across package metadata, README,
   changelog, release notes, downstream pins, and release checklist examples.
6. Add roadmap-report human-readable Markdown output for maintainer release
   governance reviews.
7. Add security-report release gaps for stale evidence and missing
   verification dates.
8. Add workspace migration impact summaries that call out record, pack, and
   generator behavior affected by a format upgrade.
9. Add machine-readable issue-code catalog generation from `verity explain`
   metadata for docs sites and CI integrations.
10. Add an agent-context generation design note for bounded AI handoff
   artifacts before implementing generator behavior.
11. Add a Unity full-lifecycle support design note covering game workspaces,
   shared Unity library workspaces, lifecycle readiness profiles, evidence,
   liveops, decommissioning, archive records, and portfolio examples.
12. Add a portfolio-level validation design note for multi-workspace product,
   service, library, and game portfolios before implementing aggregate reports.
13. Add fixture refresh documentation for regenerating golden report outputs
   with deterministic timestamps and reviewing intentional output drift.
14. Add a public architecture decision record template for future major pack,
   generator, migration, and workspace-dependency decisions.
15. Add profile-aware downstream CI template examples for release, regulated,
   public API, and internal-tool workspaces.
16. Add deployment-target release evidence links that connect deployment
   records to security, observability, compliance, and future evidence packs.
17. Add coverage-dashboard Markdown output for maintainers who need a
   human-readable release-review artifact.
18. Add local workspace-dependency prototype fixtures for exported records,
   dependency aliases, and dependency-aware graph validation before adding
   remote registry behavior.
19. Add engine portfolio example guidance showing Unity, Godot, Unreal, and
   shared game-core workspaces side by side before implementing aggregate
   portfolio reports.
20. Add engine-pack compatibility fixtures that compare Unity, Godot, and
   Unreal examples against shared game-core records before adding
   portfolio-level engine reports.

## Working Rule

No sprint is complete unless:

- Tests pass.
- CI passes.
- Documentation and examples match the implemented behavior.
- New behavior has at least one executable test or CLI smoke check.
- When the active roadmap has been caught up, `ROADMAP.md` keeps up to 20
  future planning points for fixing, improving, continuing, and expanding the
  project.
