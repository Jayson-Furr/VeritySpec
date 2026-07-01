# VeritySpec v0.48.0 Release Notes

VeritySpec v0.48.0 hardens generator output contracts for accessibility and
compliance reporting. The release adds committed golden fixtures so changes to
those report shapes are reviewed intentionally.

## Highlights

- Added `tests/golden/accessibility_report/accessibility_report.json`.
- Added `tests/golden/compliance_matrix/compliance_matrix.json`.
- Added CLI-level golden comparisons for `verity generate accessibility-report`.
- Added CLI-level golden comparisons for `verity generate compliance-matrix`.
- Added library-level golden comparisons for `generate_accessibility_report`
  and `generate_compliance_matrix`.
- Kept the Next 20 roadmap populated after converting the golden-fixture item
  into the v0.48.0 sprint.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.48.0"
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
