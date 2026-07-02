# VeritySpec v0.73.0 Release Notes

VeritySpec v0.73.0 adds parity-aware device/runtime smoke validation-runner
semantics for Unity, Godot, and Unreal engine workspaces.

## Highlights

- Added `runnerType: "device-smoke"` support for Unity, Godot, and Unreal
  validation runners.
- Allowed `device-smoke` runners to omit `scannerRefs` or declare an empty
  list when they launch a built artifact, exported artifact, packaged target,
  or physical-device runtime directly.
- Kept scanner-backed validation runners strict through schema and readiness
  checks, including a stable
  `readiness.validation_runner.scanner_refs_required` issue code.
- Added `validatesRuntime` reference rules from engine validation runners to
  Unity build targets, Godot export presets, and Unreal targets.
- Added `evidence.test` proof rules for Unity build targets, Godot export
  presets, and Unreal targets so runtime smoke results can directly prove the
  runtime artifact under test.
- Updated Unity, Godot, and Unreal executable examples with scanner-backed
  validation runners, device-smoke runtime runners, and runtime smoke evidence.
- Clarified that organization AI-agent entry-point baseline requirements must
  live in active entry points, not conversation history or agent-specific
  adapters.

This release does not add real engine execution, device orchestration, runner
scheduling, or scanner implementations. It defines the product-contract
vocabulary and validation behavior those tools can use.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.73.0"
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
verity graph examples/unity
verity validate examples/godot
verity lint examples/godot --strict
verity readiness examples/godot --strict
verity graph examples/godot
verity validate examples/unreal
verity lint examples/unreal --strict
verity readiness examples/unreal --strict
verity graph examples/unreal
verity pack compare verity.pack.unity --mirror tests/fixtures/official_extension_mirrors/verityspec-pack-unity/pack
verity explain readiness.validation_runner.scanner_refs_required --format json
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release. After the tag
workflow completes, use the post-tag release verification checklist to record
release asset hashes, skipped PyPI state, downloaded wheel smoke results,
public GitHub tag install results, closed issue and milestone evidence, and
agent context refresh evidence.
