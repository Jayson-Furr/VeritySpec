# VeritySpec v0.24.0 Release Notes

VeritySpec v0.24.0 adds golden fixture coverage for observability generator
outputs so report and schema-bundle changes are reviewed intentionally.

## Highlights

- Added committed golden fixtures for the `examples/observability`
  `observability-report` output.
- Added committed golden fixtures for the `examples/observability`
  `schema-bundle` output.
- Added library and CLI tests that compare generated observability artifacts
  against the golden fixtures.
- Normalized dynamic observability report metadata in golden comparisons.
- Documented the observability golden fixtures in generator and observability
  pack docs.
- Updated README, changelog, roadmap, downstream workflow pins, PyPI fallback
  docs, release checklist, and release bookkeeping for `v0.24.0`.

## Compatibility

- Package version: `0.24.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.24.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
