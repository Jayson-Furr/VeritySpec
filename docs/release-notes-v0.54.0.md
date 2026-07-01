# VeritySpec v0.54.0 Release Notes

VeritySpec v0.54.0 adds machine-readable issue-code catalog generation from
the canonical `verity explain` metadata.

## Highlights

- Added `verity generate issue-code-catalog` for documentation sites and CI
  integrations.
- Reused `verity explain` metadata so issue-code titles, severities,
  descriptions, and resolutions stay aligned.
- Included code, category, severity, title, description, resolution, and
  summary counts in the generated JSON.
- Kept the generator workspace-free and JSON-only.
- Added CLI tests, library tests, committed golden fixture coverage, README
  commands, generator documentation, changelog, and roadmap bookkeeping.
- Updated future sprint planning guidance to use cohesive bundles sized up to
  roughly two weeks of development effort.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.54.0"
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
verity generate issue-code-catalog --out build/issue-code-catalog.json
python -m json.tool build/issue-code-catalog.json >/dev/null
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release.
