# VeritySpec v0.53.0 Release Notes

VeritySpec v0.53.0 adds migration impact summaries for workspace format
upgrades and repair reports.

## Highlights

- Added step-level `impacts` metadata to `verity migrate --list --format json`.
- Added top-level `impactSummary` output to migration reports for planned
  migration paths and same-version repair changes.
- Impact summaries call out affected workspace-format, record, pack, and
  generator behavior without removing existing migration report fields.
- Added impact details to human-readable migration text output.
- Updated migration tests, README, versioning docs, changelog, and roadmap
  bookkeeping.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.53.0"
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
verity migrate --list --format json
verity migrate tests/fixtures/migration/legacy_workspace --dry-run --format json
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release.
