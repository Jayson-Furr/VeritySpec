# Progression Pack

`verity.pack.progression` adds built-in game progression records without
moving economy, liveops, evidence, engine, or portfolio behavior into the core
kernel.

## Record Kinds

- `progression.xp-model`: XP source, scaling model, formula, and max-level
  contract for a progression system.
- `progression.level`: level number, XP requirement, rewards, and unlocks
  within a progression track.
- `progression.unlock`: content, ability, mode, feature, reward, platform, or
  other unlock that belongs to a track.
- `progression.track`: top-level progression track that links XP models,
  levels, unlocks, and gates.
- `progression.gate`: condition that gates a level or unlock, such as XP,
  currency, content, platform, liveops, or evidence gates.

## Relationships

The pack declares reference rules for:

- `product`, `game.product`, `game.loop`, `game.mode`, and
  `game.prototype-scope` to progression tracks
- progression tracks to XP models, levels, unlocks, and gates
- levels to rewards
- unlocks to content items, abilities, and gates
- gates to unlocks, levels, currencies, and evidence requirements
- economy rewards to XP models
- liveops configs to progression tracks
- Unity, Godot, and Unreal projects to progression tracks with
  `implementsProgression`

Engine additions must keep Unity, Godot, and Unreal parity when the concept
applies. If a future engine-specific progression relationship only applies to
one engine, document that exception in the issue, docs, and tests.

## Readiness

Strict readiness checks require progression records to have enough metadata
for implementation handoff:

- XP models need source, scale model, formula, and max-level details.
- Levels need a track reference, level number, XP requirement, and at least one
  graph link.
- Unlocks need type, target, track, and at least one graph link.
- Tracks need XP model, level, unlock, and graph links.
- Gates need type, condition, track, and at least one graph link.

## Commands

```bash
verity validate examples/progression
verity lint examples/progression --strict
verity readiness examples/progression --strict
verity graph examples/progression
verity generate schema-bundle examples/progression --out build/progression-schema-bundle.json
```

The example workspace connects a game loop, gameplay ability, content item,
economy currency and reward, XP model, progression level, unlock, track, and
gate without creating graph cycles.
