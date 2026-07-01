# VeritySpec v0.8.0 Release Notes

VeritySpec v0.8.0 adds the first accessibility product surface and makes
accessibility claims reportable in CI and release review.

## Highlights

- Added built-in `verity.pack.accessibility`.
- Added strict `accessibility.claim` records for accessibility claims, checks,
  and evidence.
- Added accessibility readiness gates and reference rules.
- Added executable `examples/accessibility`.
- Added `verity generate accessibility-report` for ownership, standard, level,
  impact, coverage, verification, and release-gap summaries.
- Added future roadmap planning for GUI, desktop, mobile, game, and profile
  expansion.

## Compatibility

- Package version: `0.8.0`.
- Python: `3.9` through `3.12`.
- Workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.8.0"
verity --version
```

PyPI publishing remains prepared but requires PyPI-side trusted publishing
setup before enabling `publish_pypi=true`.
