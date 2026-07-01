# Engine Portfolio Compatibility Fixtures

The engine portfolio compatibility fixtures prove that Unity, Godot, and
Unreal workspaces can consume the same exported game-core contract through the
local workspace dependency model introduced in `v0.62.0`.

This is a fixture and guidance layer, not an aggregate portfolio report or a
new portfolio CLI command. It keeps the current boundary explicit while giving
future portfolio-report work a deterministic scenario to build against.

## Fixture Layout

The fixture lives under `tests/fixtures/engine_portfolio`:

- `shared-game-core`: exports the engine-neutral `game.product`,
  `game.mode`, `game.loop`, and `game.prototype-scope` records.
- `unity-game`: consumes the shared game-core workspace with the
  `sharedGame` alias and maps the contract to `unity.*` records.
- `godot-game`: consumes the same shared game-core workspace and maps the
  contract to `godot.*` records.
- `unreal-game`: consumes the same shared game-core workspace and maps the
  contract to `unreal.*` records.
- `portfolio`: loads the Unity, Godot, and Unreal records side by side and
  declares the same `sharedGame` dependency so alias-qualified references
  resolve in one graph.

The shared workspace exports only the records that consumers may reference.
Engine consumers use references such as:

```text
sharedGame::game.product.engine_portfolio_baseline
```

The portfolio graph exposes the resolved exported records as dependency nodes,
for example:

```text
sharedGame::game.product.engine_portfolio_baseline
sharedGame::game.mode.engine_portfolio_session
sharedGame::game.loop.engine_portfolio_validate_ship
sharedGame::game.prototype-scope.engine_portfolio_engine_slice
```

## Local Checks

Each workspace is expected to pass the normal VeritySpec checks independently:

```bash
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
```

## Design Boundary

The fixture demonstrates local, readonly, direct workspace dependencies and
side-by-side engine records. It does not implement:

- portfolio membership discovery
- aggregate validation reports
- dependency lockfiles
- remote registries or Git dependency sources
- transitive dependency policy
- commercial, legal, marketplace, certification, or support-SLA claims

Those capabilities should build on this fixture only after their report shapes,
issue codes, and compatibility guarantees are designed and tested.

## Engine Parity

The fixture intentionally keeps Unity, Godot, and Unreal records parallel where
the concepts line up:

- one product record per engine
- one engine project record per engine
- one local engine runtime/tooling dependency record where applicable
- scanner, validation-runner, readiness-dashboard, and agent-context exporter
  records for each engine
- a portfolio workspace that references all three engine projects from one
  review surface

When future engine-pack capabilities are added for an engine-neutral concept,
the fixture should either add equivalent Unity, Godot, and Unreal coverage or
document why parity does not apply.
