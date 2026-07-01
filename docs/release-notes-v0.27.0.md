# VeritySpec v0.27.0 Release Notes

VeritySpec v0.27.0 adds product-contract enforcement profiles for release,
strict, regulated, public API, and internal-tool workflows.

## Highlights

- Added `--profile` support to `verity validate`, `verity lint`,
  `verity readiness`, and `verity doctor`.
- Added built-in profiles: `release`, `strict`, `regulated`, `public-api`, and
  `internal-tool`.
- Added effective profile metadata to JSON output for machine clients and CI
  integrations.
- Added regulated-profile checks for required security, accessibility, and
  compliance pack coverage.
- Added public API-profile checks for API pack and `api.endpoint` record
  coverage.
- Added explainable profile issue codes for missing required packs and record
  kinds.
- Added library and CLI coverage for profile behavior, exit codes, and JSON
  output.
- Documented profile semantics and CI usage.
- Updated README, changelog, roadmap, downstream workflow pins, PyPI fallback
  docs, release checklist, and release bookkeeping for `v0.27.0`.

## Compatibility

- Package version: `0.27.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.27.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
