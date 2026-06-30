# VeritySpec v0.25.0 Release Notes

VeritySpec v0.25.0 adds deterministic timestamp controls for generated JSON
reports so golden snapshots and CI fixtures can be regenerated predictably.

## Highlights

- Added `verity generate --generated-at <ISO datetime>` for JSON report
  artifacts.
- Added shared generated-at handling across validation reports, security
  reports, observability reports, accessibility reports, compliance matrices,
  and roadmap reports.
- Added ISO 8601 validation for explicit generated-at values with clean usage
  errors for invalid input.
- Added library and CLI coverage for fixed report timestamps and invalid
  timestamp handling.
- Documented deterministic report timestamp usage in generator docs.
- Updated README, changelog, roadmap, downstream workflow pins, PyPI fallback
  docs, release checklist, and release bookkeeping for `v0.25.0`.

## Compatibility

- Package version: `0.25.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.25.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
