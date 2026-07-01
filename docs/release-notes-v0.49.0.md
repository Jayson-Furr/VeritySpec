# VeritySpec v0.49.0 Release Notes

VeritySpec v0.49.0 adds public external-pack review governance. The release
documents how maintainers should evaluate public pack proposals before they
become accepted, implemented, bundled, or considered for future official
extension-package work.

## Highlights

- Added `docs/external-pack-review-checklist.md`.
- Linked the checklist from README, contribution guidance, pack docs, and the
  pack proposal issue template.
- Defined maintainer gates for proposal inputs, identity, product-contract
  value, executable examples, documentation, compatibility, PR review, and
  acceptance outcomes.
- Preserved the boundary that checklist acceptance is not the same as bundling
  a pack, making it official, or detaching bundled specialized packs from the
  core package.
- Added documentation contract tests that keep the checklist discoverable and
  preserve its review boundaries.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.49.0"
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
