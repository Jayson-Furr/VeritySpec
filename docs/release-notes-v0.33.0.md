# VeritySpec v0.33.0 Release Notes

VeritySpec v0.33.0 adds executable pack scaffold documentation fixtures that
show external pack authors a complete generated pack plus a consuming workspace
layout.

## Highlights

- Added `docs/fixtures/pack-scaffold` with a generated external pack fixture
  and a workspace that loads it through `packPaths`.
- Added documentation for the fixture layout and the commands external pack
  authors can run to validate the pack and consuming workspace.
- Added tests proving the committed pack fixture matches fresh
  `verity pack init` output.
- Added validation, strict linting, strict readiness, schema-bundle generation,
  and pack-capability-index generation coverage for the fixture workspace.
- Added CI and release-checklist smoke commands for the fixture.
- Linked the fixture from README and pack documentation.
- Updated README, pack docs, CI docs, release checklist, changelog, roadmap,
  workflow pins, downstream templates, PyPI fallback docs, and AI-agent command
  guidance.

## Compatibility

- Package version: `0.33.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.
- No workspace schema or workspace format behavior changed in this release.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.33.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
