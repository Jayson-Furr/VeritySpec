# VeritySpec v0.52.0 Release Notes

VeritySpec v0.52.0 adds security-report release-gap summaries for verification
freshness.

## Highlights

- Added `summary.releaseGaps.staleEvidence` to `verity generate
  security-report` so release reviewers can identify controls whose evidence is
  older than their declared review cadence.
- Added `summary.releaseGaps.missingVerificationDates` so reports distinguish
  missing verification dates from stale evidence.
- Preserved existing `summary.criticalUnverified` behavior for downstream
  compatibility while also including it in `summary.releaseGaps`.
- Updated the committed security-report golden fixture, generator docs, README,
  changelog, and roadmap bookkeeping.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.52.0"
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
verity validate examples/security
verity lint examples/security --strict
verity readiness examples/security --strict
verity generate security-report examples/security --out build/security-report.json
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release.
