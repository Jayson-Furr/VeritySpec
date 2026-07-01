# VeritySpec v0.59.0 Release Notes

VeritySpec v0.59.0 adds profile-aware downstream CI support so consuming
repositories can run product-contract checks through release, regulated, public
API, and internal-tool profiles while keeping the reusable workflow pinned to a
known VeritySpec release.

## Highlights

- Added a `profile` input to the reusable downstream product-contract workflow
  and passed it through to `verity validate`, `verity lint`, `verity readiness`,
  and `verity doctor`.
- Preserved no-profile reusable workflow behavior for existing downstream
  repositories that already call the workflow without a profile.
- Added `templates/github-actions/product-contract-profiles.yml`, a maintained
  matrix example covering release, regulated, public API, and internal-tool
  workspaces.
- Documented strictness guidance for profile-aware downstream checks,
  including a non-blocking internal-tool example.
- Documented the boundary that VeritySpec profiles help organize contract
  checks but do not prove commercial, legal, privacy-law, marketplace,
  platform-certification, app-store, store-review, pricing-approval, or
  support-SLA readiness.
- Added release-integrity and downstream-template tests that keep profile-aware
  workflow pins, profile names, docs, and roadmap-report expectations aligned.
- Updated README, changelog, roadmap, release checklist, downstream workflow
  pins, evidence fixtures, and release-integrity surfaces for v0.59.0.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.59.0"
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
