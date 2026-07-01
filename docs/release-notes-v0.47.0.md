# VeritySpec v0.47.0 Release Notes

VeritySpec v0.47.0 adds the first public specialized-pack separation plan. It
does not remove bundled packs; it defines the gates required before any
domain-heavy pack can become an official extension package safely.

## Highlights

- Added `docs/specialized-pack-separation.md`.
- Defined candidate official extension package names for game, mobile,
  liveops, Unity, Godot, and Unreal packs.
- Preserved existing pack IDs and record kinds as the compatibility target for
  future package splits.
- Documented compatibility metadata, official detach gates, parity tests,
  migration guidance, and rollback criteria.
- Linked the plan from README, pack documentation, engine/product-delivery
  guidance, and AI-agent operating rules.
- Added documentation contract tests that keep the plan discoverable and
  preserve the no-immediate-removal boundary.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.47.0"
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
