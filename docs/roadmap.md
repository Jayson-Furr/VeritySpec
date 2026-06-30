# Roadmap

VeritySpec is being built in public sprints. The GitHub issues and milestones
are the operational roadmap; this document summarizes the same plan for readers
who start in the repository.

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

The active milestone is `v0.2.0`.

| Sprint | Status | Focus |
|---:|---|---|
| 9 | Complete | Version registry, workspace version validation, `verity migrate`, version-aware diffing |
| 10 | Complete | External pack loading through workspace `packPaths` and CLI `--pack-path` flags |
| 11 | Complete | Generator maturity, richer OpenAPI/AsyncAPI metadata, golden type/model snapshots |
| 12 | In progress | CI productization, release notes, action warning cleanup, v0.2.0 release readiness |

## Next Priorities

Sprint 12 should finish the `v0.2.0` line by making VeritySpec easier to adopt
from downstream repositories:

- Add a reusable or copy-paste CI workflow for product-contract checks.
- Add v0.2.0 release notes.
- Review GitHub Actions version warnings.
- Run final package build, wheel install, examples, importer, generator, and docs checks.
- Tag and publish the v0.2.0 release when the scope is complete.

## Later Candidates

These are intentionally not committed to a release until the current milestone
is complete:

- OpenAPI path-parameter extraction.
- More complete Python nested-object model generation.
- Pack authoring scaffolds.
- Migration chains beyond `v0.1.0`.
- UI, security, observability, accessibility, deployment, and compliance packs.
- Downstream project templates and examples.

