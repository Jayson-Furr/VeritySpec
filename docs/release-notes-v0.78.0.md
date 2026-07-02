# VeritySpec v0.78.0 Release Notes

VeritySpec v0.78.0 adds lifecycle-readiness engine fixture planning for the
first engine-prototype implementation slice.

## Highlights

- Added the [lifecycle-readiness engine fixture plan](lifecycle-readiness-fixture-plan.md).
- Defined the first future engine-prototype fixture slice for Unity, Godot,
  Unreal, and a transitional integration workspace.
- Documented parity expectations for engine project, runtime target, scanner,
  validation runner, agent-context exporter, and evidence records.
- Listed future executable validate, lint, readiness, and graph commands for
  each planned fixture workspace.
- Anchored fixture planning to the engine full-lifecycle design note and the
  fixture refresh guide.
- Preserved the boundary that integration workspaces remain transitional until
  first-class cross-workspace dependency resolution exists.
- Added documentation tests for the fixture plan and rotated the Next 20
  roadmap queue toward the future implementation sprint.
- Updated README, changelog, roadmap, release checklist surfaces, downstream
  workflow pins, release-integrity fixtures, and release notes.

This release does not add new engine record kinds, schemas, generators,
cross-workspace dependency resolution, dependency lockfiles, or production,
release, liveops, decommission, or archive readiness claims. The planning
surface does not make commercial, legal, privacy-law, marketplace,
platform-certification, app-store, pricing, support-SLA, or store-review
readiness claims.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.78.0"
verity --version
```

PyPI publishing is prepared but not enabled yet. GitHub release installation
remains the canonical public install path for this release.

## Verification

Release verification should include:

```bash
python -m unittest discover -s tests -v
verity pack validate
verity validate examples/basic
verity lint examples/basic --strict
verity readiness examples/basic --strict
verity generate roadmap-report . --format markdown --out build/roadmap-report.md
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release. After the tag
workflow completes, use the post-tag release verification checklist to record
release asset hashes, skipped PyPI state, downloaded wheel smoke results,
public GitHub tag install results, closed issue and milestone evidence, and
agent context refresh evidence.
