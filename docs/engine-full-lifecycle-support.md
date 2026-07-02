# Engine Full-Lifecycle Support Design

VeritySpec should support Unity, Godot, and Unreal products across the whole
game and engine-tooling lifecycle without turning the core package into a broad
engine catalog. This note defines the design boundary before adding more
engine-specific record kinds, examples, generators, or readiness gates.

No schema changes are introduced by this design note. The next implementation
work should stay pack-based, parity-aware, and executable through tests and
examples.

## Goal

The goal is engine full-lifecycle support for:

- Unity, Godot, and Unreal game workspaces.
- Shared engine library workspaces.
- Engine-tooling repositories for scanners, validation runners, readiness
  dashboards, editor surfaces, and agent-context exporters.
- Integration workspaces that combine a game with shared engine libraries.
- Portfolio examples that show multiple game workspaces and shared runtime
  dependencies side by side.

The core principle remains:

```text
GitHub manages workflow. VeritySpec manages truth.
```

GitHub Issues, Projects, Milestones, Actions, and pull requests manage work.
VeritySpec manages the product contract: records, graph relationships,
readiness gates, evidence requirements, generated artifacts, and bounded agent
handoff context.

## Architecture Boundary

Core stays small. Engine lifecycle concepts belong in packs and examples:

- `verity.pack.unity` owns Unity-specific implementation and tooling records.
- `verity.pack.godot` owns Godot-specific implementation and tooling records.
- `verity.pack.unreal` owns Unreal-specific implementation and tooling records.
- `verity.pack.game-core` owns game identity, modes, loops, and prototype
  scope.
- `verity.pack.game-assets` owns GDD source, visual identity, identity images,
  and concept art references.
- `verity.pack.gameplay`, `verity.pack.content`, `verity.pack.economy`, and
  `verity.pack.progression` own playable systems, content, economy, and
  progression contracts.
- `verity.pack.mobile` and `verity.pack.liveops` own engine-neutral mobile and
  live operations lifecycle contracts.
- `verity.pack.evidence` owns proof records.
- `verity.pack.product-delivery` owns spec-driven repository delivery posture,
  readiness profiles, evidence requirements, release process, support,
  maintenance, archive, decommission, and agent-context exporter records.

Engine packs should reference these packs instead of duplicating their
concerns. A Unity project can link to a mobile app release or liveops config;
the same concept should be available to Godot and Unreal where it applies.

## Engine Parity Rule

Unity, Godot, and Unreal support should advance together where the concept is
engine-neutral or has a direct engine equivalent. When a sprint adds a Unity
record kind, readiness gate, generator surface, example capability, or
relationship rule, the same sprint should add the Godot and Unreal equivalents
or document why the equivalent does not apply.

This rule does not require identical schema fields when the engines differ. It
does require comparable product-contract coverage for games made with the
supported engines.

## Workspace Shapes

A full lifecycle engine scenario needs several workspace shapes.

### Engine Toolkit Workspace

An engine toolkit workspace describes a product such as
`VeritySpec.Unity`, `VeritySpec.Godot`, or `VeritySpec.Unreal`. It should use
engine, product-delivery, evidence, release, support, maintenance, archive, and
agent-context exporter records to describe the toolkit itself.

### Shared Engine Library Workspace

A shared engine library workspace describes reusable runtime or tooling
contracts such as save systems, telemetry clients, liveops config loaders,
localization helpers, editor tooling, scanners, and validation runners. It is a
workspace containing actual library records, not a pack.

Future cross-workspace dependency support should let game workspaces reference
exported records from a shared engine library workspace without copying those
records locally.

### Game Workspace

A game workspace describes the game product contract: creative source,
identity, loops, modes, gameplay, content, economy, progression, engine
implementation plan, mobile posture, liveops assumptions, evidence needs,
release process, maintenance policy, decommission policy, and archive policy.

### Integration Workspace

Before first-class workspace dependencies exist, integration workspaces can
combine one game workspace with one or more shared engine library workspaces.
They are a transitional validation pattern for proving references, graph
relationships, readiness gates, and generated reports in a combined context.

### Portfolio Workspace

A portfolio workspace should summarize multiple game, toolkit, and shared
library workspaces. The portfolio examples should answer questions such as which
games are prototype-ready, which games depend on a shared save system, which
games need telemetry clients, which games lack concept art, and which games
are affected by shared runtime changes.

## Lifecycle Stages

Engine-supported game workspaces should be able to progress through named
lifecycle stages instead of a single broad ready/not-ready claim:

- concept
- pre-production
- prototype
- vertical slice
- production
- release
- liveops
- maintenance
- sunset
- decommissioning
- archive

Each stage should be represented by records, relationships, readiness gates,
and evidence requirements appropriate to that maturity level.

## Readiness Profiles

Useful future readiness profiles include:

- `game-concept-complete`
- `engine-prototype-ready`
- `vertical-slice-ready`
- `engine-production-ready`
- `game-release-ready`
- `liveops-ready`
- `maintenance-ready`
- `decommission-ready`
- `archive-ready`

A workspace can pass one profile and fail another. For example, a game may be
concept-complete and prototype-ready while still failing production-ready,
release-ready, liveops-ready, and archive-ready profiles.

This is more truthful than claiming a workspace is universally ready.

## Evidence Model

Evidence should connect lifecycle claims to proof records. Useful engine and
game evidence includes:

- edit mode and play mode tests
- unit and integration tests
- CI runs and build artifacts
- scanner and validation-runner output
- QA reports and playtest reports
- screenshots and videos
- performance captures
- telemetry dashboards
- accessibility reviews
- security scans
- localization reports
- certification checklist posture
- support handoff notes
- archive manifests

Evidence records do not prove legal, privacy-law, marketplace, platform,
store-review, pricing, or certification approval. They prove that a workspace
has declared reviewable artifacts and can link them to product-contract
requirements.

## LiveOps, Maintenance, Decommissioning, And Archive

Liveops and maintenance support should be engine-neutral where possible.
Engine-specific records should connect projects to liveops configs, remote
config bounds, save migration policy, rollback plans, support categories,
analytics taxonomy, maintenance policy, decommission policy, data deletion
posture, and archive handling.

Decommissioning and archive records should make lifecycle end states explicit:
server shutdown plans, store-delisting posture, player communication posture,
support handoff, data deletion posture, final build manifests, source archive
manifests, asset archive manifests, license-review posture, telemetry shutdown
notes, and archive owner/location records.

These records should describe the contract and evidence posture. They should
not make commercial, legal, privacy-law, marketplace, platform-certification,
or store-review guarantees.

## Agent Context

Engine full-lifecycle support should feed bounded agent-context generation.
A future agent context for an engine or game task should include:

- the selected game or toolkit record
- relevant Unity, Godot, or Unreal project records
- shared engine library records in scope
- lifecycle stage and readiness profile
- evidence requirements
- generated artifacts to refresh
- records that should not drift
- verification commands expected before handoff or pull request

The generated context should point agents back to `AGENTS.md` for repository
process, shell discipline, branching, pull request, release, and bookkeeping
rules.

## First-Implementation Gate

The first implementation sprint after this design note should not try to model
every engine and lifecycle concept at once. It should choose one narrow,
executable vertical slice and include:

- matching Unity, Godot, and Unreal coverage where the concept applies
- schemas and readiness gates for any new record kinds
- reference rules that prove graph relationships
- examples or fixtures that validate, lint, pass readiness, and graph
- documentation that explains the pack boundary and non-goals
- tests for pack validation, examples, readiness, and graph behavior
- release notes and roadmap updates

Implementation should wait on first-class cross-workspace dependency support
before claiming true dependency resolution between game workspaces and shared
engine library workspaces. Until then, integration workspaces remain the
recommended transitional pattern.

The rule is explicit: integration workspaces remain the recommended transitional pattern.

The first follow-on fixture plan is documented in
`docs/lifecycle-readiness-fixture-plan.md`. That plan defines the narrow
engine-prototype readiness fixture slice that should precede broader lifecycle
implementation work.
