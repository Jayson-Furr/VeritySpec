# VeritySpec v0.31.0 Release Notes

VeritySpec v0.31.0 adds cross-workspace dependency design guidance for future
local-only workspace dependency support.

## Highlights

- Added `docs/cross-workspace-dependencies.md`.
- Defined the first implementation boundary as local path, readonly, direct
  workspace dependencies.
- Clarified the distinction between packs, which define vocabulary and
  behavior, and workspaces, which contain actual product, service, game,
  library, or platform records.
- Documented exported-record visibility expectations for dependency
  workspaces.
- Documented friendly and canonical cross-workspace reference forms.
- Documented resolver phases, lockfile expectations, dependency-aware
  validation goals, graph behavior, diff behavior, and impact-report
  implications.
- Documented integration workspaces as a transitional pattern until
  first-class dependencies exist.
- Added documentation guard tests for the core design decisions.
- Updated README, pack docs, workspace-format docs, graph docs, changelog, and
  roadmap bookkeeping.

## Compatibility

- Package version: `0.31.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.
- No workspace schema, CLI, or lockfile behavior changed in this release.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.31.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
