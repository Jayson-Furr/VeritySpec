# VeritySpec v0.10.0 Release Notes

VeritySpec v0.10.0 makes workspace diffs more useful for CI, release review,
and machine clients.

## Highlights

- Added machine-readable per-change severity to `verity diff --format json`.
- Added breaking-change classification for removed packs, removed records,
  record kind changes, records marked removed, API endpoint method/path
  changes, removed API response status codes, and schema-object contract
  removals.
- Preserved existing `versions`, `packs`, `added`, `removed`, and `changed`
  diff fields for compatibility.
- Added `summary` and `changes` fields for machine clients.
- Updated text diff output with severity and breaking-change summaries.
- Added CI smoke coverage and documentation for the richer diff output.

## Compatibility

- Package version: `0.10.0`.
- Python: `3.9` through `3.12`.
- Workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.10.0"
verity --version
```

PyPI publishing remains prepared but requires PyPI-side trusted publishing
setup before enabling `publish_pypi=true`.
