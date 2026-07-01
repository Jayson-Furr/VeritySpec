# VeritySpec v0.38.0 Release Notes

VeritySpec v0.38.0 adds the first built-in gameplay and content implementation
packs: `verity.pack.gameplay` and `verity.pack.content`.

## Highlights

- Added built-in `verity.pack.gameplay`.
- Added strict schemas for `game.mechanic`, `game.ability`, `game.rule`, and
  `game.encounter`.
- Added gameplay readiness gates that require traceable mechanic, ability,
  rule, and encounter handoff metadata.
- Added gameplay reference rules that connect game products, modes, loops,
  prototype scopes, mechanics, abilities, rules, and encounters.
- Added executable `examples/gameplay` using the Dream Extraction concept with
  `verity.core`, `verity.pack.game-core`, and `verity.pack.gameplay`.
- Added built-in `verity.pack.content`.
- Added strict schemas for `game.content-item`, `game.level`,
  `game.loot-table`, and `game.content-manifest`.
- Added content readiness gates that require traceable content item, level,
  loot table, and manifest metadata.
- Added content reference rules that connect products, game products,
  manifests, items, levels, loot tables, gameplay encounters, prototype scopes,
  and Unity scenes.
- Added executable `examples/content` composed with game-core, gameplay,
  content, and Unity records.
- Added gameplay and content support to cross-pack coverage dashboards, schema
  bundles, example compatibility fixtures, CI checks, release checks, and
  public documentation.
- Documented the next sprint cadence: future sprints should be cohesive bundles
  of related work sized up to roughly one week of development effort.

## Compatibility

- Package version: `0.38.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.
- No workspace format migration is required.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.38.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
