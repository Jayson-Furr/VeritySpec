# VeritySpec v0.19.0 Release Notes

VeritySpec v0.19.0 adds executable security-control evidence freshness checks
so security readiness can fail when verification evidence has drifted beyond a
declared review cadence.

## Highlights

- Added optional `verification.reviewCadenceDays` metadata to
  `security.control` records.
- Added pack-declared date freshness readiness conditions that compare
  `verification.lastVerified` against each control's review cadence.
- Added the stable `security.control.evidence_stale` issue code with
  `verity explain` support.
- Kept the freshness policy in `verity.pack.security` instead of hard-coding it
  into the core kernel.
- Added tests for fresh, stale, and missing security evidence freshness cases.
- Updated README, readiness docs, security pack docs, changelog, roadmap,
  downstream CI pins, and release bookkeeping for `v0.19.0`.

## Compatibility

- Package version: `0.19.0`.
- Python: `3.9` through `3.12`.
- Workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.19.0"
verity --version
```

PyPI publishing remains prepared but disabled. Keep `publish_pypi=false` unless
the PyPI project and trusted-publishing setup have been verified and publishing
has been explicitly requested.
