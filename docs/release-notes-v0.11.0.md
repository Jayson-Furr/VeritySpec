# VeritySpec v0.11.0 Release Notes

VeritySpec v0.11.0 hardens workspace migration coverage with committed
dry-run fixtures for supported workspace version edges.

## Highlights

- Added committed migration fixtures for legacy workspace input and `v0.1.0`
  workspace input.
- Added CLI test coverage for `legacy -> v0.1.0`, `v0.1.0 -> v0.2.0`, and the
  default `legacy -> v0.2.0` chained migration dry run.
- Verified dry-run migration reports do not write files.
- Verified expected migration path and change records for each supported edge.
- Updated README, changelog, roadmap, and migration docs for the coverage.

## Compatibility

- Package version: `0.11.0`.
- Python: `3.9` through `3.12`.
- Workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.11.0"
verity --version
```

PyPI publishing remains prepared but requires PyPI-side trusted publishing
setup before enabling `publish_pypi=true`.
