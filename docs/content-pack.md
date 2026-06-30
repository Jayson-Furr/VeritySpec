# Content Pack

`verity.pack.content` adds built-in game content records without moving economy,
progression, liveops, evidence, or engine-specific implementation behavior into
the core kernel.

## Record Kinds

- `game.content-item`: a content item contract for resources, currencies,
  weapons, armor, consumables, quest items, collectibles, cosmetics, crafting
  materials, and other item-like content.
- `game.level`: a level contract with level type, setting, objective summary,
  duration estimate, tags, and gameplay links.
- `game.loot-table`: a reward/drop table contract with weighted entries and
  item references.
- `game.content-manifest`: a versioned content manifest that groups item,
  level, and loot-table records for a prototype, vertical slice, release,
  liveops event, patch, or archive scope.

## Relationships

The pack declares these reference relationships:

- `product` `hasContentManifest` `game.content-manifest`
- `game.product` `hasContentManifest` `game.content-manifest`
- `game.content-manifest` `includesItem` `game.content-item`
- `game.content-manifest` `includesLevel` `game.level`
- `game.content-manifest` `includesLootTable` `game.loot-table`
- `game.level` `usesEncounter` `game.encounter`
- `game.level` `usesMechanic` `game.mechanic`
- `game.loot-table` `dropsItem` `game.content-item`
- `game.encounter` `rewardsLoot` `game.loot-table`
- `game.prototype-scope` `includesLevel` `game.level`
- `unity.scene` `implementsLevel` `game.level`

This scope composes with `verity.pack.game-core`, `verity.pack.gameplay`, and
optionally `verity.pack.unity`: game-core defines the product boundary,
gameplay defines mechanics and encounters, content defines item/level/reward
contracts, and Unity records can map scenes to levels.

## Readiness

Strict readiness checks require each ready content record to have enough
metadata for content review and implementation handoff:

- Content items need type, rarity, and usage.
- Levels need type, setting, objective summary, and at least one graph
  reference.
- Loot tables need type, at least one weighted entry, and at least one graph
  reference.
- Content manifests need type, scope, version, at least one content reference,
  and at least three graph references.

## Commands

```bash
verity validate examples/content
verity lint examples/content --strict
verity readiness examples/content --strict
verity graph examples/content
verity generate schema-bundle examples/content --out build/content-schema-bundle.json
```

The example workspace models the Dream Extraction game concept with one
prototype resource item, one level, one reward table, and one vertical-slice
content manifest tied back to game-core and gameplay records.
