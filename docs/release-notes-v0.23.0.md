# VeritySpec v0.23.0 Release Notes

VeritySpec v0.23.0 adds opt-in GitHub Actions annotation output for
product-contract failures so CI logs can point maintainers directly at
validation, lint, and readiness issues.

## Highlights

- Added `--github-annotations` to `verity validate`, `verity lint`, and
  `verity readiness`.
- Emitted annotations to stderr so existing text and JSON stdout remain stable.
- Escaped workflow command data and properties for `%`, carriage returns,
  newlines, colons, and commas.
- Added validation and readiness CLI coverage proving JSON stdout remains
  parseable while annotations are emitted.
- Updated downstream CI docs and maintained templates to enable annotations
  when the installed `verity` supports the flag.
- Updated README, changelog, roadmap, downstream CI pins, PyPI fallback docs,
  and release bookkeeping for `v0.23.0`.

## Compatibility

- Package version: `0.23.0`.
- Python: `3.9` through `3.12`.
- Workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.23.0"
verity --version
```

PyPI publishing remains prepared but disabled. Keep `publish_pypi=false` unless
the PyPI project and trusted-publishing setup have been verified and publishing
has been explicitly requested.
