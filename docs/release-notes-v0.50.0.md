# VeritySpec v0.50.0 Release Notes

VeritySpec v0.50.0 adds test-backed release-integrity checks for public
version and release bookkeeping.

## Highlights

- Added release-integrity tests that compare package metadata with README
  release surfaces, CHANGELOG entries, release notes, downstream workflow pins,
  PyPI fallback install guidance, release checklist tag examples, and evidence
  fixture artifact versions.
- Added release-integrity documentation and linked it from README and the
  release checklist.
- Updated the release checklist to require the release-integrity test before
  tagging.
- Kept the release workflow behavior unchanged: GitHub release installation
  remains the canonical public install path until PyPI trusted publishing is
  configured and intentionally enabled.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.50.0"
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
