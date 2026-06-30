# VeritySpec Sprint Roadmap

VeritySpec matures through small, shippable sprints. Each sprint should leave
the repository in a releasable state with tests, examples, documentation, and CI
checks updated alongside code.

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

## Later Candidates

These are intentionally not committed to a release until the current milestone
is complete:

- UI, desktop, mobile, game, assets, and deployment packs.
- Downstream project templates and examples.

## Next 20 Roadmap Points

These points define the next backlog once the active roadmap is caught up. They
are planning inputs, not release commitments. Convert each point into a GitHub
issue and milestone before implementation begins.

AI agents must keep this section populated with up to 20 concrete points when
the active roadmap is caught up. The points should balance fixes,
improvements, continuation work, and expansion. When points are converted into
sprint issues or milestones, replace them with new future planning inputs so
the roadmap does not drift into an empty backlog.

1. Add pack authoring tests that verify generated scaffolds can be used by a
   sample workspace immediately.
2. Add downstream repository templates for GitHub Actions product-contract
   enforcement.
3. Add golden security-report fixtures once the report shape stabilizes.
4. Add public contribution guidance for proposing new packs and schema
   changes.
5. Review package distribution readiness for PyPI trusted publishing and
   decide whether to publish the `verityspec` package publicly.
6. Add a roadmap-report generator that emits active milestones, completed
   sprints, and future planning points for project governance.
7. Add security-control evidence freshness checks for `verification.lastVerified`
   age and review cadence.
8. Add workspace compatibility golden manifests for future format upgrades.
9. Add structured issue location fields for machine clients in addition to
   formatted location strings.
10. Add documentation command smoke tests that execute README examples to
   prevent public command drift.
11. Add CI annotation output for readiness and validation failures in GitHub
   Actions logs.
12. Add observability example golden fixtures for schema bundles and future
   report output.
13. Add report timestamp controls for deterministic golden snapshot generation.
14. Define pack boundaries for GUI, desktop, mobile, and game product surfaces
   before adding their first schemas.
15. Add product-contract profiles for release, strict, regulated, public API,
   and internal-tool enforcement modes.
16. Add a first deployment-target pack for runtime, hosting, and release
   environment contracts.
17. Add cross-pack coverage dashboards that summarize which product surfaces
   have API, CLI, event, security, accessibility, observability, and compliance
   records.
18. Add a product-impact report that expands changed records into affected
   upstream and downstream records for release review.
19. Define a local-only cross-workspace dependency design note covering
   workspace dependencies, exported records, reference resolution, and lockfile
   boundaries before implementation.
20. Add a pack capability index report that summarizes schemas, readiness
   gates, reference rules, and generators across built-in and external packs.

## Working Rule

No sprint is complete unless:

- Tests pass.
- CI passes.
- Documentation and examples match the implemented behavior.
- New behavior has at least one executable test or CLI smoke check.
- When the active roadmap has been caught up, `ROADMAP.md` keeps up to 20
  future planning points for fixing, improving, continuing, and expanding the
  project.
