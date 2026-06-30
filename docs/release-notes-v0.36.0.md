# VeritySpec v0.36.0 Release Notes

VeritySpec v0.36.0 adds the first built-in creative-source game pack:
`verity.pack.game-assets`.

## Highlights

- Added built-in `verity.pack.game-assets`.
- Added strict schemas for `game.gdd-source`, `game.visual-identity`,
  `game.identity-image`, and `game.concept-art`.
- Added game-assets readiness gates that require traceable GDD source records,
  visual identity metadata, identity-image usage, concept-art subjects, style
  tags, and linked creative references.
- Added game-assets reference rules for product-to-visual-identity,
  game-product-to-GDD, game-product-to-visual-identity, GDD-derived records,
  visual identity asset usage, and concept-art support for game modes and
  loops.
- Added executable `examples/game-assets` using the Dream Extraction game
  concept, composed with `verity.pack.game-core`.
- Added game-assets support to cross-pack coverage dashboards and golden
  coverage fixtures.
- Added schema-bundle smoke coverage for game-assets.
- Updated README, pack docs, generator docs, readiness docs, CI docs, release
  checklist, roadmap, changelog, workflow checks, and AI-agent guidance.
- Kept future game expansion scoped: Unity, gameplay, content, liveops,
  evidence, dependencies, archive, and portfolio behavior remain future packs
  or features.

## Compatibility

- Package version: `0.36.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.
- No workspace format migration is required.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.36.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
