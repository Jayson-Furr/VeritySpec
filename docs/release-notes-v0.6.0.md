# VeritySpec v0.6.0 Release Notes

VeritySpec v0.6.0 hardens release readiness, expands workspace compatibility
coverage, and makes validation output easier to act on.

## Highlights

- Added conditional readiness rules to pack manifests.
- Added security readiness hardening for critical unverified
  `security.control` records.
- Added stable `security.control.critical_unverified` diagnostics.
- Added a fixture compatibility matrix across supported workspace
  `specVersion` values.
- Improved issue locations for nested schema, readiness, and reference errors.

## Compatibility

- Package version: `0.6.0`.
- Python: `3.9` through `3.12`.
- Workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.6.0"
verity --version
```

PyPI publishing remains prepared but requires PyPI-side trusted publishing
setup before enabling `publish_pypi=true`.
