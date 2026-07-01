# VeritySpec v0.64.0 Release Notes

VeritySpec v0.64.0 adds lifecycle readiness gap reporting for workspaces that
combine product-delivery, mobile, and liveops records. The release turns the
existing lifecycle vocabulary into a generated review artifact without moving
specialized product-surface behavior into the core runtime.

## Highlights

- Added `verity generate lifecycle-readiness-report`.
- Added `examples/lifecycle-readiness`, an executable cross-pack workspace
  that loads `verity.pack.product-delivery`, `verity.pack.mobile`, and
  `verity.pack.liveops`.
- Added report stages for implementation-ready, soft-launch, launch-candidate,
  remote-config, rollback, support, save-migration, decommission,
  data-deletion, and archive-review coverage.
- Added gap entries for missing record kinds, non-ready records, and missing
  owners.
- Added lifecycle report generator metadata to the product-delivery, mobile,
  and liveops pack manifests.
- Added library tests, CLI tests, golden output, fixture-refresh guidance,
  README command coverage, compatibility-manifest coverage, and release
  checklist coverage.

The lifecycle readiness report summarizes VeritySpec record coverage, lifecycle
gaps, and record status only. It does not assert commercial, legal,
privacy-law, marketplace, app-store, platform-certification, live-service,
support, or archival readiness.

This release does not add Markdown lifecycle report output, lifecycle report
JSON Schema documentation, external approval workflow integration, store
submission automation, privacy-law review automation, support SLA enforcement,
or archive certification.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.64.0"
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
verity validate examples/lifecycle-readiness
verity lint examples/lifecycle-readiness --strict
verity readiness examples/lifecycle-readiness --strict
verity graph examples/lifecycle-readiness
verity generate lifecycle-readiness-report examples/lifecycle-readiness --out build/lifecycle-readiness-report.json
python -m json.tool build/lifecycle-readiness-report.json >/dev/null
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release.
