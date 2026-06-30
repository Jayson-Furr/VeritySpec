# VeritySpec v0.22.0 Release Notes

VeritySpec v0.22.0 adds executable README command smoke tests so public CLI
examples stay aligned with the package behavior as the command surface grows.

## Highlights

- Added tests that parse README bash command examples and execute safe local
  `verity` commands in documented order.
- Rewrote README `build/` output paths to temporary directories during smoke
  tests so documentation checks do not dirty the repository.
- Treated install, virtual environment, and full test-suite commands as
  explicit documentation-only skips.
- Added coverage that fails when new README command examples are neither
  executable nor intentionally skipped.
- Updated README, CI docs, changelog, roadmap, downstream CI pins, PyPI
  fallback docs, and release bookkeeping for `v0.22.0`.

## Compatibility

- Package version: `0.22.0`.
- Python: `3.9` through `3.12`.
- Workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.22.0"
verity --version
```

PyPI publishing remains prepared but disabled. Keep `publish_pypi=false` unless
the PyPI project and trusted-publishing setup have been verified and publishing
has been explicitly requested.
