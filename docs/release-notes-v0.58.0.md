# VeritySpec v0.58.0 Release Notes

VeritySpec v0.58.0 adds fixture refresh guidance so generated report contracts,
golden fixtures, and release-version evidence fixtures can be updated
intentionally and reviewed consistently.

## Highlights

- Added `docs/fixture-refresh.md` to document deterministic golden report
  regeneration, `--generated-at` timestamp discipline, placeholder
  normalization, and intentional output drift review.
- Listed current committed golden fixtures and their regeneration commands for
  security, observability, accessibility, compliance, deployment, evidence,
  coverage dashboard, pack capability index, product-impact, issue-code
  catalog, OpenAPI, TypeScript, and Python model outputs.
- Documented release-version fixture updates for evidence records, evidence
  reports, coverage fixtures, README release surfaces, downstream pins, release
  checklist entries, and release notes.
- Linked fixture refresh guidance from README, generator docs, and the release
  checklist so maintainers can find the procedure during generator and release
  work.
- Added executable documentation tests that keep the fixture refresh guide,
  public links, release-integrity boundary, and roadmap-report expectations
  from drifting.
- Updated README, changelog, roadmap, release checklist, downstream workflow
  pins, evidence fixtures, and release-integrity surfaces for v0.58.0.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.58.0"
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

