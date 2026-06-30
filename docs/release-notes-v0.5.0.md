# VeritySpec v0.5.0 Release Notes

VeritySpec v0.5.0 adds the first built-in security pack and strengthens
roadmap discipline for future AI-agent work.

## Highlights

- Added built-in `verity.pack.security`.
- Added strict `security.control` records for release-relevant security
  requirements, risk levels, coverage, verification evidence, and target
  records.
- Added security-control readiness gates and reference rules.
- Added `verity generate security-report` for workspace-level security control
  summaries.
- Added executable `examples/security` coverage for validation, lint,
  readiness, and report generation.
- Added a `ROADMAP.md` section with the next 20 future planning points.
- Added an AI-agent rule requiring future roadmap planning when the active
  roadmap is caught up.

## Compatibility

- Python: 3.9 through 3.12.
- VeritySpec workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.
- Package version: `0.5.0`.

## Publishing Notes

GitHub release artifacts are built by the release workflow. PyPI publishing is
prepared but still requires PyPI-side trusted-publishing setup before
`publish_pypi=true` can be used.
