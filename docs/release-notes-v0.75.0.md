# VeritySpec v0.75.0 Release Notes

VeritySpec v0.75.0 adds the first Markdown `agent-context` generator so
product-delivery and engine exporter records can produce bounded implementation
handoff context for humans, tools, and AI coding agents.

## Highlights

- Added `verity generate agent-context WORKSPACE --record RECORD_ID --format
  markdown`.
- Supported `agent-context.exporter`, `unity.agent-context-exporter`,
  `godot.agent-context-exporter`, and `unreal.agent-context-exporter` targets.
- Selected target, included-kind, and graph-connected records into a
  deterministic Markdown artifact.
- Added safety boundaries that keep `AGENTS.md`, tests, readiness checks, and
  evidence records authoritative.
- Added verification commands to generated context so agents can refresh the
  product contract after implementation work.
- Advertised the generator in product-delivery, Unity, Godot, and Unreal pack
  metadata, including the Unity official-extension mirror.
- Added CLI coverage, library coverage, a golden Markdown fixture, README,
  generator docs, fixture-refresh guidance, release checklist updates,
  changelog, and roadmap bookkeeping.

This release does not add machine-readable JSON output for agent context, does
not make implementation-readiness claims, and does not replace repository
entry-point rules. Generated context is a bounded handoff artifact, not an
authorization to bypass normal branch, PR, test, readiness, evidence, or
release processes.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.75.0"
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
verity validate examples/product-delivery
verity lint examples/product-delivery --strict
verity readiness examples/product-delivery --strict
verity generate agent-context examples/product-delivery --record agent-context.exporter.implementation_bundle --format markdown --out build/agent-context.md
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release. After the tag
workflow completes, use the post-tag release verification checklist to record
release asset hashes, skipped PyPI state, downloaded wheel smoke results,
public GitHub tag install results, closed issue and milestone evidence, and
agent context refresh evidence.
