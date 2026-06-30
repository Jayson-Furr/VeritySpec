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

The active milestone is `v0.5.0`.

| Sprint | Status | Focus |
|---:|---|---|
| 19 | Complete | Security pack foundation and security report generation |

## Sprint 19 Priorities

Sprint 19 should add the first security surface as a pack, not as core bloat:

- Add built-in `verity.pack.security`.
- Add a strict `security.control` record schema.
- Add security-control readiness gates and reference rules.
- Add `verity generate security-report`.
- Add an executable security example workspace.
- Update tests, CI, README, changelog, roadmap, generator docs, pack docs, and
  AI-agent guidance.

## Later Candidates

These are intentionally not committed to a release until the current milestone
is complete:

- UI, observability, accessibility, deployment, and compliance packs.
- Downstream project templates and examples.

## Next 20 Roadmap Points

These points define the next backlog once the active roadmap is caught up. They
are planning inputs, not release commitments. Convert each point into a GitHub
issue and milestone before implementation begins.

1. Release `v0.5.0` after Sprint 19 security-pack verification is complete.
2. Add a security-readiness hardening pass for unverified critical controls.
3. Add a compatibility test matrix for fixture workspaces across supported
   workspace spec versions.
4. Improve validation issue locations for nested schema, readiness, and
   reference errors.
5. Add `verity doctor --report-out` for writing diagnostics without shell
   redirection.
6. Add `verity init --template` for API, CLI, events, and security starter
   workspaces.
7. Add a first `verity.pack.observability` pack for telemetry events, metrics,
   dashboards, and alert ownership.
8. Add an observability report generator that summarizes signals, ownership,
   and release gaps.
9. Add a first `verity.pack.accessibility` pack for UI accessibility claims,
   checks, and evidence.
10. Add an accessibility report generator suitable for release review.
11. Add a first `verity.pack.compliance` pack that maps controls to frameworks
    without making legal claims.
12. Add a compliance matrix generator that joins security, accessibility, and
    observability evidence.
13. Improve `verity diff` with machine-readable change severity and breaking
    change classification.
14. Add migration dry-run fixtures for every supported workspace version edge.
15. Add generator plugin metadata so packs can advertise report capabilities
    more explicitly than a string list.
16. Add pack authoring tests that verify generated scaffolds can be used by a
    sample workspace immediately.
17. Add downstream repository templates for GitHub Actions product-contract
    enforcement.
18. Add golden security-report fixtures once the report shape stabilizes.
19. Add public contribution guidance for proposing new packs and schema
    changes.
20. Review package distribution readiness for PyPI trusted publishing and
    decide whether to publish the `verityspec` package publicly.

## Working Rule

No sprint is complete unless:

- Tests pass.
- CI passes.
- Documentation and examples match the implemented behavior.
- New behavior has at least one executable test or CLI smoke check.
