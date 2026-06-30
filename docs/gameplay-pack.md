# Gameplay Pack

`verity.pack.gameplay` adds built-in gameplay design records without moving
content, engine, liveops, evidence, or portfolio lifecycle behavior into the
core kernel.

## Record Kinds

- `game.mechanic`: a player-facing or system-facing mechanic contract with
  mechanic type, summary, inputs, outputs, tuning parameters, and graph links.
- `game.ability`: an active, passive, movement, defensive, utility, or other
  ability contract with activation model, effect summary, cooldown, resource
  cost, constraints, and rule references.
- `game.rule`: a gameplay rule contract for failure, scoring, spawn, reward,
  cooldown, constraint, and other rule behavior.
- `game.encounter`: an encounter contract with type, difficulty, objective,
  location, participants, and links to mechanics, abilities, rules, and future
  content rewards.

## Relationships

The pack declares these reference relationships:

- `product` `hasGameplay` `game.mechanic`
- `game.product` `hasMechanic` `game.mechanic`
- `game.product` `hasAbility` `game.ability`
- `game.product` `hasRule` `game.rule`
- `game.product` `hasEncounter` `game.encounter`
- `game.mode` `usesMechanic` `game.mechanic`
- `game.loop` `usesMechanic` `game.mechanic`
- `game.mechanic` `enablesAbility` `game.ability`
- `game.ability` `governedBy` `game.rule`
- `game.mechanic` `governedBy` `game.rule`
- `game.encounter` `usesMechanic` `game.mechanic`
- `game.encounter` `includesAbility` `game.ability`
- `game.encounter` `governedBy` `game.rule`
- `game.prototype-scope` `validatesEncounter` `game.encounter`

This scope composes with `verity.pack.game-core`: game-core defines the game
identity, modes, loops, and prototype boundary; gameplay records define the
first executable mechanic and encounter contracts inside that boundary.

## Readiness

Strict readiness checks require each ready gameplay record to have enough
metadata for implementation handoff:

- Mechanics need type, summary, at least one input, at least one output, and at
  least one graph reference.
- Abilities need type, activation model, effect summary, and at least one
  graph reference.
- Rules need type, condition, and outcome.
- Encounters need type, difficulty, objective, at least one participant, and
  at least two graph references.

## Commands

```bash
verity validate examples/gameplay
verity lint examples/gameplay --strict
verity readiness examples/gameplay --strict
verity graph examples/gameplay
verity generate schema-bundle examples/gameplay --out build/gameplay-schema-bundle.json
```

The example workspace models the Dream Extraction game concept with one
mechanic, one ability, one rule, and one encounter tied back to game-core mode,
loop, and prototype records.
