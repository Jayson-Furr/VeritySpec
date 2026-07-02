# VeritySpec v0.71.0 Release Notes

VeritySpec v0.71.0 adds engine evidence traceability for Unity, Godot, and
Unreal workspaces. Engine examples can now model validation and build proof
directly against concrete engine records instead of routing every proof through
broader product-scope records.

## Highlights

- Added `evidence.test` `proves` rules for `unity.project`, `unity.scene`,
  `godot.project`, `godot.scene`, `unreal.project`, and `unreal.map`.
- Added `evidence.build` `proves` rules for `unity.build-target`,
  `godot.export-preset`, and `unreal.target`.
- Kept Unity validation-runner evidence parity explicit with existing Godot
  and Unreal validation-runner `producesEvidence` behavior.
- Updated `examples/unity`, `examples/godot`, and `examples/unreal` to load
  `verity.pack.evidence` and include direct test/build evidence records.
- Updated each engine example graph so validation runners produce concrete test
  evidence records.
- Documented that skipped or blocked engine checks should use
  `evidence.test.result` values such as `skipped` or `inconclusive` with the
  normal `proves` relationship, rather than downstream-only relationship names
  such as `provesGap`.
- Updated README, evidence pack docs, engine pack docs, engine/product-delivery
  guidance, changelog, roadmap, and workspace compatibility fixtures.

This release improves traceability for game and engine-tooling repositories.
It does not make legal, marketplace, platform-certification, privacy,
commercial, production-readiness, or store-review approval claims.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.71.0"
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
verity validate examples/unity
verity lint examples/unity --strict
verity readiness examples/unity --strict
verity graph examples/unity --format json > build/unity-graph.json
verity validate examples/godot
verity lint examples/godot --strict
verity readiness examples/godot --strict
verity graph examples/godot --format json > build/godot-graph.json
verity validate examples/unreal
verity lint examples/unreal --strict
verity readiness examples/unreal --strict
verity graph examples/unreal --format json > build/unreal-graph.json
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release. After the tag
workflow completes, use the post-tag release verification checklist to record
release asset hashes, skipped PyPI state, downloaded wheel smoke results,
public GitHub tag install results, closed issue and milestone evidence, and
agent context refresh evidence.
