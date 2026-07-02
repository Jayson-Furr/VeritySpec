# VeritySpec v0.67.0 Release Notes

VeritySpec v0.67.0 adds a CLI command module decomposition design note before
larger dependency, portfolio, lifecycle, and agent-context command families
expand the `verity` command surface.

## Highlights

- Added the public [CLI command module decomposition](cli-command-modules.md)
  design note.
- Defined a future `verityspec.commands` package shape while keeping
  `verityspec.cli:main` as the stable public entry point.
- Documented command registration, shared helper ownership, staged migration
  phases, compatibility guardrails, test expectations, non-goals, and the first
  implementation gate.
- Linked the design note from README, branching guidance, and ADR guidance.
- Added tests that keep the design note discoverable and preserve the
  no-runtime-movement boundary.
- Rotated the next-20 roadmap queue after converting the design note into
  sprint 144.

This release does not move command implementations, change public command
names, change arguments, change output formats, change exit codes, introduce a
new CLI framework, add dependency/portfolio/lifecycle/agent-context commands,
or detach specialized packs.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.67.0"
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
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release.
