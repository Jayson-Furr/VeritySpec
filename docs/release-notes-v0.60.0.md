# VeritySpec v0.60.0 Release Notes

VeritySpec v0.60.0 adds deployment-target release evidence links so production
deployment targets can point to the security, observability, compliance, and
evidence records that support release review.

## Highlights

- Added `securityControlRefs`, `observabilityDashboardRefs`,
  `complianceMappingRefs`, and `releaseEvidenceRefs` to `deployment.target`
  records.
- Extended production deployment readiness so production targets require
  approval, rollback, health-check coverage, and linked security,
  observability, compliance, and release evidence records.
- Added deployment-owned reference rules for release evidence links while
  keeping security, observability, compliance, and evidence behavior in their
  own packs.
- Extended `verity generate deployment-report` with linked control, dashboard,
  compliance mapping, and release evidence summaries.
- Updated `examples/deployment` with executable security, observability,
  compliance, and evidence records.
- Refreshed deployment report, issue-code catalog, workspace compatibility,
  and cross-pack coverage fixtures.
- Updated README, changelog, roadmap, CI docs, generator docs, pack docs,
  downstream workflow pins, and release-integrity surfaces for v0.60.0.

These links record internal product-contract evidence. They do not make legal,
commercial, privacy-law, platform-certification, marketplace, app-store,
store-review, pricing-approval, or support-SLA claims.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.60.0"
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
