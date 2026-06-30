# Economy Pack

`verity.pack.economy` adds built-in game economy records without moving
progression, liveops, evidence, monetization approval, or platform-specific
store behavior into the core kernel.

## Record Kinds

- `economy.currency`: a currency or resource contract with type, unit name,
  optional code, precision, balance policy, and tags.
- `economy.source`: a source that produces a currency through gameplay,
  rewards, loot, purchases, liveops, administrative grants, systems, or another
  path.
- `economy.sink`: a spend path that consumes a currency for upgrades, stores,
  crafting, entry fees, repairs, rerolls, time skips, or another purpose.
- `economy.reward`: a reward bundle that grants currencies, content items,
  loot tables, or another target.
- `economy.offer`: an offer contract with price currency, price amount,
  reward references, availability state, and optional purchase limits.

## Relationships

The pack declares these reference relationships:

- `product` `hasEconomy` `economy.currency`
- `game.product` `hasCurrency` `economy.currency`
- `game.product` `hasEconomySource` `economy.source`
- `game.product` `hasEconomySink` `economy.sink`
- `game.product` `hasReward` `economy.reward`
- `game.product` `hasOffer` `economy.offer`
- `game.mechanic` `producesEconomySource` `economy.source`
- `game.loop` `usesEconomySink` `economy.sink`
- `game.encounter` `grantsReward` `economy.reward`
- `game.loot-table` `grantsReward` `economy.reward`
- `game.content-manifest` `includesOffer` `economy.offer`
- `game.prototype-scope` `validatesEconomy` `economy.currency`
- `economy.source` `producesCurrency` `economy.currency`
- `economy.sink` `consumesCurrency` `economy.currency`
- `economy.reward` `grantsCurrency` `economy.currency`
- `economy.reward` `grantsItem` `game.content-item`
- `economy.reward` `usesLootTable` `game.loot-table`
- `economy.offer` `pricedIn` `economy.currency`
- `economy.offer` `grantsReward` `economy.reward`
- `economy.offer` `includesItem` `game.content-item`

This scope composes with `verity.pack.game-core`, `verity.pack.gameplay`, and
`verity.pack.content`: game-core defines the product and prototype boundary,
gameplay defines mechanics and encounters, content defines items and loot
tables, and economy defines sources, sinks, rewards, and offers.

## Readiness

Strict readiness checks require each ready economy record to have enough
metadata for economy review and implementation handoff:

- Currencies need type and unit metadata.
- Sources need a currency reference, amount, and graph link.
- Sinks need a currency reference, cost, purpose, and graph link.
- Rewards need at least one grant and at least one graph link.
- Offers need price metadata, availability, at least one reward reference, and
  at least two graph links.

## Commands

```bash
verity validate examples/economy
verity lint examples/economy --strict
verity readiness examples/economy --strict
verity graph examples/economy
verity generate schema-bundle examples/economy --out build/economy-schema-bundle.json
```

The example workspace models the Dream Extraction game concept with one
resource currency, one source, one sink, one reward, one prototype offer, and
links back to game-core, gameplay, and content records.
