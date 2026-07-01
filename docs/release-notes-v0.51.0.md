# VeritySpec v0.51.0 Release Notes

VeritySpec v0.51.0 adds human-readable Markdown output for roadmap governance
reports.

## Highlights

- Added `--format markdown` support to `verity generate roadmap-report`.
- Kept JSON as the default roadmap-report output format and preserved the
  existing JSON contract.
- Included version metadata, summary counts, latest released milestone, active
  milestones, recent milestone and sprint context, and Next 20 roadmap points
  in the Markdown report.
- Rejected Markdown output for generator artifacts that do not support it.
- Updated README command examples, generator docs, changelog, roadmap
  bookkeeping, and tests for the new output format.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.51.0"
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
wheel, uploads artifacts, and creates the GitHub release.
