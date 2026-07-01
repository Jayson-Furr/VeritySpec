# VeritySpec v0.20.0 Release Notes

VeritySpec v0.20.0 adds golden workspace compatibility manifests so supported
workspace format coverage can be reviewed as a stable contract before future
format upgrades.

## Highlights

- Added `tests/golden/workspace_compatibility/manifest.json` as the committed
  expected compatibility surface.
- Recorded the current workspace format, supported workspace formats, required
  checks, covered workspaces, pack coverage, record counts, record-kind
  coverage, and compatibility variants.
- Added test coverage that compares regenerated compatibility metadata against
  the golden manifest.
- Kept the existing matrix that validates, lints, and checks readiness for
  positive workspaces across every supported `specVersion`.
- Updated README, changelog, roadmap, versioning docs, downstream CI pins, and
  release bookkeeping for `v0.20.0`.

## Compatibility

- Package version: `0.20.0`.
- Python: `3.9` through `3.12`.
- Workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.20.0"
verity --version
```

PyPI publishing remains prepared but disabled. Keep `publish_pypi=false` unless
the PyPI project and trusted-publishing setup have been verified and publishing
has been explicitly requested.
