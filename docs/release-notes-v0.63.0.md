# VeritySpec v0.63.0 Release Notes

VeritySpec v0.63.0 adds engine portfolio compatibility fixtures that show
Unity, Godot, Unreal, and a shared exported game-core workspace side by side.
The release builds directly on the v0.62.0 local workspace dependency
prototype without introducing an aggregate portfolio-report command yet.

## Highlights

- Added a shared game-core fixture workspace that exports a game product, mode,
  loop, and prototype-scope contract.
- Added Unity, Godot, and Unreal game workspaces that consume the same shared
  game-core contract through the `sharedGame` dependency alias.
- Added a portfolio fixture workspace that loads the three engine workspaces
  side by side and exposes the shared exported records in dependency-aware
  graph output.
- Added regression tests for fixture validation, strict lint, strict readiness,
  dependency graph nodes, dependency graph edges, README links, and portfolio
  documentation links.
- Added engine portfolio compatibility documentation that defines the fixture
  boundary, local check commands, engine parity expectations, and non-claims.
- Updated README, changelog, roadmap, and roadmap report expectations for the
  v0.63.0 release.

This release does not add portfolio membership discovery, aggregate portfolio
reports, dependency lockfiles, remote registries, transitive dependency policy,
or commercial, legal, marketplace, certification, app-store, pricing-approval,
or support-SLA claims.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.63.0"
verity --version
```

PyPI publishing is prepared but not enabled yet. GitHub release installation
remains the canonical public install path for this release.

## Verification

Release verification should include:

```bash
python -m unittest discover -s tests -v
verity pack validate
verity validate examples/basic
verity lint examples/basic --strict
verity readiness examples/basic --strict
verity validate tests/fixtures/engine_portfolio/shared-game-core
verity lint tests/fixtures/engine_portfolio/shared-game-core --strict
verity readiness tests/fixtures/engine_portfolio/shared-game-core --strict
verity validate tests/fixtures/engine_portfolio/unity-game
verity lint tests/fixtures/engine_portfolio/unity-game --strict
verity readiness tests/fixtures/engine_portfolio/unity-game --strict
verity validate tests/fixtures/engine_portfolio/godot-game
verity lint tests/fixtures/engine_portfolio/godot-game --strict
verity readiness tests/fixtures/engine_portfolio/godot-game --strict
verity validate tests/fixtures/engine_portfolio/unreal-game
verity lint tests/fixtures/engine_portfolio/unreal-game --strict
verity readiness tests/fixtures/engine_portfolio/unreal-game --strict
verity validate tests/fixtures/engine_portfolio/portfolio
verity lint tests/fixtures/engine_portfolio/portfolio --strict
verity readiness tests/fixtures/engine_portfolio/portfolio --strict
verity graph tests/fixtures/engine_portfolio/portfolio --format json
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release.
