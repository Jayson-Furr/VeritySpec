# Lifecycle-Readiness Engine Fixture Plan

This plan defines the first engine lifecycle-readiness fixture slice after the
engine full-lifecycle support design note. It is a planning artifact for the
next implementation sprint. This plan does not add schemas, runtime behavior, or new readiness claims.

The goal is to make the first engine lifecycle fixtures narrow, executable, and
parity-aware before adding more Unity, Godot, or Unreal lifecycle coverage.

## Source Inputs

This plan builds on:

- `docs/engine-full-lifecycle-support.md`
- `docs/fixture-refresh.md`
- `docs/unity-pack.md`
- `docs/godot-pack.md`
- `docs/unreal-pack.md`
- `docs/product-delivery-pack.md`
- `docs/evidence-pack.md`

The controlling principle remains:

```text
GitHub manages workflow. VeritySpec manages truth.
```

## First Fixture Slice

The first implementation slice should model engine-prototype readiness for a
small game prototype that can be represented for Unity, Godot, and Unreal with
equivalent contract coverage.

The slice should prove that a future workspace can connect:

- a `game.product` record
- a `game.prototype-scope` record
- one engine project record
- one engine validation runner
- one engine scanner
- one engine agent-context exporter
- one product-delivery readiness profile
- one product-delivery evidence requirement
- at least one evidence record proving the validation runner or prototype
  scope

The slice should not attempt production, release, liveops, mobile store,
decommission, or archive readiness. Those stages belong in later fixture
slices after the prototype fixture has stabilized.

## Planned Fixture Family

The first implementation sprint should add a small fixture family instead of a
large all-purpose example:

| Fixture | Purpose |
|---|---|
| `tests/fixtures/engine_lifecycle/unity-prototype` | Unity prototype lifecycle fixture |
| `tests/fixtures/engine_lifecycle/godot-prototype` | Godot prototype lifecycle fixture |
| `tests/fixtures/engine_lifecycle/unreal-prototype` | Unreal prototype lifecycle fixture |
| `tests/fixtures/engine_lifecycle/integration-prototype` | Transitional combined validation fixture |

The engine-specific fixtures should remain independent workspaces. The
integration fixture can combine records when graph behavior must be proven
across records that will eventually live behind workspace dependencies.

Integration workspaces remain the recommended transitional pattern until
first-class cross-workspace dependency resolution, exported-record visibility,
version constraints, and lockfiles are implemented.

## Engine Parity Expectations

The implementation sprint should keep equivalent coverage across the supported
engines:

| Contract surface | Unity | Godot | Unreal |
|---|---|---|---|
| Engine project | `unity.project` | `godot.project` | `unreal.project` |
| Prototype runtime target | `unity.build-target` | `godot.export-preset` | `unreal.target` |
| Scanner | `unity.scanner` | `godot.scanner` | `unreal.scanner` |
| Validation runner | `unity.validation-runner` | `godot.validation-runner` | `unreal.validation-runner` |
| Agent handoff | `unity.agent-context-exporter` | `godot.agent-context-exporter` | `unreal.agent-context-exporter` |
| Proof record | `evidence.test` or `evidence.build` | `evidence.test` or `evidence.build` | `evidence.test` or `evidence.build` |

If one engine cannot support a contract surface with the same fields as the
others, the implementation issue, docs, and tests should explain the reason.
Different fields are acceptable. Missing product-contract coverage is not.

## Reference And Graph Expectations

The future fixtures should prove graph relationships instead of only passing
JSON Schema validation.

Expected graph links include:

- product to prototype scope
- prototype scope to the engine project
- engine project to scanner, validation runner, and agent-context exporter
- validation runner to scanner
- validation runner or prototype scope to evidence
- readiness profile to evidence requirement
- agent-context exporter to product-delivery and engine records

The exact relationship names should use existing pack reference rules where
possible. If a needed relationship is missing, the implementation sprint should
add the rule with tests instead of weakening validation.

## Future Executable Commands

When the fixtures are implemented, each engine workspace should pass:

```bash
verity validate tests/fixtures/engine_lifecycle/unity-prototype
verity lint tests/fixtures/engine_lifecycle/unity-prototype --strict
verity readiness tests/fixtures/engine_lifecycle/unity-prototype --strict
verity graph tests/fixtures/engine_lifecycle/unity-prototype

verity validate tests/fixtures/engine_lifecycle/godot-prototype
verity lint tests/fixtures/engine_lifecycle/godot-prototype --strict
verity readiness tests/fixtures/engine_lifecycle/godot-prototype --strict
verity graph tests/fixtures/engine_lifecycle/godot-prototype

verity validate tests/fixtures/engine_lifecycle/unreal-prototype
verity lint tests/fixtures/engine_lifecycle/unreal-prototype --strict
verity readiness tests/fixtures/engine_lifecycle/unreal-prototype --strict
verity graph tests/fixtures/engine_lifecycle/unreal-prototype
```

The integration fixture should also pass:

```bash
verity validate tests/fixtures/engine_lifecycle/integration-prototype
verity lint tests/fixtures/engine_lifecycle/integration-prototype --strict
verity readiness tests/fixtures/engine_lifecycle/integration-prototype --strict
verity graph tests/fixtures/engine_lifecycle/integration-prototype
```

If the future sprint updates generated reports, the fixture refresh process in
`docs/fixture-refresh.md` applies. Generated outputs should be reviewed from
`build/`, placeholders should be preserved, and golden fixtures should change
only when an output contract intentionally changes.

## Acceptance Gates For The Implementation Sprint

The implementation sprint should not be considered complete unless:

- `verity pack validate` passes.
- Unity, Godot, and Unreal prototype fixtures validate, lint, pass readiness,
  and graph.
- The integration prototype fixture validates, lints, passes readiness, and
  graphs.
- Reference-rule tests prove the lifecycle graph relationships.
- Example or fixture tests cover all three engines.
- Any changed generated output has focused golden coverage.
- Documentation states the pack boundary, parity expectations, fixture
  commands, and non-goals.
- README, changelog, roadmap, release notes, and release checklist surfaces
  stay aligned.

## Non-Goals And Non-Claims

This plan does not add:

- new record kinds
- new schemas
- new generator output
- cross-workspace dependency resolution
- dependency lockfiles
- production-ready, release-ready, liveops-ready, decommission-ready, or
  archive-ready lifecycle claims

The planned fixtures will not prove commercial, legal, privacy-law,
marketplace, platform-certification, app-store, pricing, support-SLA, or
store-review readiness. They will only prove that VeritySpec can model and
validate the declared prototype lifecycle contract for Unity, Godot, and
Unreal in a parity-aware way.
