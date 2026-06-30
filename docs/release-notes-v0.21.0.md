# VeritySpec v0.21.0 Release Notes

VeritySpec v0.21.0 adds structured issue location details for JSON diagnostics
so tools, CI systems, and AI agents can navigate validation and readiness
failures without parsing human-readable location strings.

## Highlights

- Added additive `locationDetails` objects to issue JSON output while
  preserving the existing formatted `location` string.
- Parsed file paths, nested field paths, field parts, JSON pointers, record
  fragments, and record indexes when available.
- Added coverage for CLI validation JSON output and generated validation
  reports.
- Kept text output stable for human diagnostics.
- Updated README, contract-intelligence docs, generator docs, changelog,
  roadmap, downstream CI pins, and release bookkeeping for `v0.21.0`.

## Compatibility

- Package version: `0.21.0`.
- Python: `3.9` through `3.12`.
- Workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.21.0"
verity --version
```

PyPI publishing remains prepared but disabled. Keep `publish_pypi=false` unless
the PyPI project and trusted-publishing setup have been verified and publishing
has been explicitly requested.
