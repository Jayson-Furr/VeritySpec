# VeritySpec v0.61.0 Release Notes

VeritySpec v0.61.0 adds Markdown output for the cross-pack coverage dashboard
so maintainers can review product-surface coverage without opening JSON while
keeping the existing JSON report as the machine-readable contract.

## Highlights

- Added `--format markdown` support to `verity generate coverage-dashboard`.
- Preserved the existing coverage-dashboard JSON output for CI and downstream
  tooling.
- Added a human-readable Markdown report with summary, release-gap,
  surface-coverage, and product-reference tables.
- Added an explicit non-claims boundary to the Markdown report for legal,
  commercial, privacy-law, platform-certification, marketplace, app-store,
  store-review, pricing-approval, and support-SLA claims.
- Updated bundled pack generator metadata so coverage-dashboard support
  advertises JSON and Markdown output consistently.
- Added CLI, library, golden-fixture, README, changelog, roadmap, CI,
  generator, pack, fixture-refresh, and release-checklist coverage.

The Markdown report is an internal release-review artifact. It does not make
legal, commercial, privacy-law, platform-certification, marketplace,
app-store, store-review, pricing-approval, or support-SLA claims.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.61.0"
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
