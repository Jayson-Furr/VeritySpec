# Game Core Pack

`verity.pack.game-core` adds the first built-in game product-contract records
without moving game, engine, asset, liveops, or portfolio concepts into the
core kernel.

## Record Kinds

- `game.product`: high-level game identity, pitch, player fantasy, audience,
  platforms, source links, and references to the game mode, loop, and prototype
  records that define the first executable contract.
- `game.mode`: a playable mode contract, including mode type, player-count
  expectations, session-length metadata, and loop references.
- `game.loop`: a game loop contract with typed cadence and ordered steps.
- `game.prototype-scope`: an implementation handoff boundary for a paper,
  greybox, vertical-slice, technical, or content prototype.

## Relationships

The pack declares these reference relationships:

- `product` `describes` `game.product`
- `game.product` `hasMode` `game.mode`
- `game.product` `hasLoop` `game.loop`
- `game.product` `prototypeScope` `game.prototype-scope`
- `game.mode` `usesLoop` `game.loop`
- `game.prototype-scope` `validatesMode` `game.mode`
- `game.prototype-scope` `validatesLoop` `game.loop`

This first scope intentionally does not define Unity, Unreal, Godot, asset,
economy, progression, liveops, evidence, dependency, or portfolio records.
Those belong in later packs or workspace-dependency features.

## Readiness

Strict readiness checks require each ready game-core record to have the fields
needed for a useful early game handoff:

- game products need pitch, player fantasy, target audience, at least one
  target platform, and links to mode, loop, and prototype-scope records
- game modes need mode type, summary, and player-count bounds
- game loops need loop type, cadence, and at least one loop step
- prototype scopes need a prototype type, goal, included feature references,
  success criteria, and validation references

## Commands

```bash
verity validate examples/game-core
verity lint examples/game-core --strict
verity readiness examples/game-core --strict
verity graph examples/game-core
verity generate schema-bundle examples/game-core --out build/game-core-schema-bundle.json
```

The example workspace models a small Dream Extraction game concept with one
game product, one co-op extraction mode, one core loop, and one vertical-slice
prototype scope.
