# VeritySpec v0.7.0 Release Notes

VeritySpec v0.7.0 improves CLI ergonomics and adds the first observability
product surface.

## Highlights

- Added `verity doctor --report-out` for writing structured diagnostics to a
  JSON file while keeping normal stdout output.
- Added `verity init --template` with `basic`, `api`, `cli`, `events`, and
  `security` starter workspaces.
- Added built-in `verity.pack.observability` for telemetry, metrics,
  dashboards, and alerts.
- Added executable `examples/observability`.
- Added `verity generate observability-report` for ownership, severity,
  signal, and release-gap summaries.

## Compatibility

- Package version: `0.7.0`.
- Python: `3.9` through `3.12`.
- Workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.7.0"
verity --version
```

PyPI publishing remains prepared but requires PyPI-side trusted publishing
setup before enabling `publish_pypi=true`.
