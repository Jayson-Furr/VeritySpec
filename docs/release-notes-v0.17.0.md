# VeritySpec v0.17.0 Release Notes

VeritySpec v0.17.0 hardens the PyPI publishing story without enabling PyPI
publishing yet. GitHub release installation remains the canonical public install
path until the PyPI project and trusted-publishing configuration are explicitly
ready.

## Highlights

- Documented the current publishing decision: do not publish `verityspec` to
  PyPI until PyPI-side trusted publishing is configured and a maintainer
  explicitly enables publishing.
- Updated `docs/pypi.md` with the current GitHub release fallback install tag,
  PyPI-side blockers, repository-side readiness checks, and the no-token rule.
- Added tests that keep the PyPI fallback install docs aligned with the package
  version and confirm the publishing safeguards remain documented.
- Updated the release checklist so release prep verifies the PyPI fallback
  install tag alongside the README release badge, latest release text, install
  references, workspace package-version text, and release-notes link.
- Updated README, changelog, roadmap, downstream CI pins, and release
  bookkeeping for `v0.17.0`.

## Compatibility

- Package version: `0.17.0`.
- Python: `3.9` through `3.12`.
- Workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.17.0"
verity --version
```

PyPI publishing remains prepared but disabled. Keep `publish_pypi=false` unless
the PyPI project and trusted-publishing setup have been verified and publishing
has been explicitly requested.
