# VeritySpec v0.34.0 Release Notes

VeritySpec v0.34.0 adds a maintained downstream CI template for monorepos with
multiple VeritySpec workspaces and shared local packs.

## Highlights

- Added `templates/github-actions/product-contract-monorepo.yml`.
- Uses the existing reusable product-contract workflow instead of duplicating
  shell logic.
- Runs a matrix of workspace checks with `fail-fast: false`.
- Supports shared local pack paths and workspace-specific pack paths through
  matrix entries.
- Documents how downstream monorepos should adapt the workspace and pack-path
  matrix.
- Added tests that keep the monorepo template pinned to the current release
  tag and verify shared-pack matrix behavior.
- Moved built-in `verity.pack.game-core` to the top of the Next 20 roadmap so
  built-in pack expansion is the next product-surface direction.
- Updated README, downstream CI docs, CI docs, release checklist, changelog,
  roadmap, workflow pins, PyPI fallback docs, and AI-agent guidance.

## Compatibility

- Package version: `0.34.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.
- No workspace schema or workspace format behavior changed in this release.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.34.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
