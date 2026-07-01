# VeritySpec v0.35.0 Release Notes

VeritySpec v0.35.0 adds the first built-in game product-contract pack:
`verity.pack.game-core`.

## Highlights

- Added built-in `verity.pack.game-core`.
- Added strict schemas for `game.product`, `game.mode`, `game.loop`, and
  `game.prototype-scope`.
- Added game-core readiness gates that require a useful game handoff shape:
  game identity, player fantasy, audience, platforms, mode links, loop links,
  prototype scope, included prototype features, and success criteria.
- Added game-core reference rules for product-to-game, product-to-mode,
  product-to-loop, product-to-prototype, mode-to-loop, and prototype validation
  relationships.
- Added executable `examples/game-core` using a Dream Extraction game concept.
- Added game-core support to cross-pack coverage dashboards and golden
  coverage fixtures.
- Added schema-bundle smoke coverage for game-core.
- Updated README, pack docs, generator docs, CI docs, release checklist,
  roadmap, changelog, workflow checks, and AI-agent guidance.
- Kept future game expansion scoped: Unity, engine, assets, liveops, evidence,
  dependencies, and portfolio behavior remain future packs or features.

## Compatibility

- Package version: `0.35.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.
- No workspace format migration is required.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.35.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
