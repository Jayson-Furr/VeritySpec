# Engine and Product-Delivery Pack Direction

This note captures VeritySpec pack direction for engine-tooling repositories,
games made with supported engines, and spec-driven product delivery. It mixes
existing pack coverage with future planning; each section states whether the
pack already exists.

The goal is to let repositories for engine integrations, editor tooling,
validation runners, scanners, dashboards, and agent handoff workflows dogfood
VeritySpec as their product-contract source of truth without relying on local
ad hoc packs.

Core principle:

```text
GitHub manages workflow. VeritySpec manages truth.
```

GitHub Issues should remain the work, decision, question, defect, readiness
gap, and evidence-request system. GitHub Projects should remain the planning
board, roadmap, portfolio view, and execution dashboard. GitHub Milestones
should remain release, sprint, or candidate boundaries. GitHub Actions should
remain the enforcement gate. Pull requests should remain the implementation and
spec-change review surface.

VeritySpec should own the structured product contract: records, relationships,
readiness gates, evidence requirements, generated artifacts, and agent context.

## Architecture Rule

Core stays small. Engine and product-delivery concepts belong in packs with
schemas, readiness gates where useful, reference rules, examples or fixtures,
docs, and tests.

These packs should support engine-tooling repositories, engine-specific game
workspaces, and spec-driven product management without making commercial,
legal, marketplace-readiness, or certification claims.

## Distribution Direction

The current engine, game, mobile, liveops, and evidence packs are bundled so
their schemas, examples, tests, and readiness rules can stabilize together with
the core contract engine. Long term, VeritySpec should separate specialized
domain packs from the core package as official extension packages.

That split should not happen by simply moving pack folders out of the
repository. The first product milestone is an installed-pack discovery and
compatibility contract that lets users install official extension packages and
load them without manual `packPaths`.

Any future separation sprint should prove that separated Unity, Godot, Unreal,
game, mobile, or liveops packs:

- validate with the same `verity pack validate` contract;
- load through installed-pack discovery and existing local `packPaths`;
- preserve the current record kind IDs, schemas, readiness gates, reference
  rules, examples, and generated artifacts;
- declare compatibility metadata for the core `verityspec` package; and
- include migration or rollback guidance for existing workspaces.

The staged product plan is maintained in
[Specialized pack separation plan](specialized-pack-separation.md). That plan
keeps the current bundled packs available until official extension packages
can prove compatibility, parity, migration, and rollback behavior. The proposed
installed-pack metadata contract is documented in
[Installed pack compatibility metadata](installed-pack-compatibility-metadata.md).

## Engine Pack Parity Rule

Future engine-specific additions should keep Unity, Godot, and Unreal coverage
equivalent where the concept applies. If VeritySpec adds a Unity-specific
record kind, readiness gate, generator surface, or executable example
capability, the same related sprint should add the Godot and Unreal
equivalents or document why a direct equivalent does not apply.

This keeps downstream engine-tooling repositories from depending on local ad
hoc packs because one supported engine has newer built-in vocabulary than the
others.

## Unity Pack Expansion

Existing pack ID: `verity.pack.unity`.

The current Unity pack covers Unity game implementation and engine-tooling
records: projects, package dependencies, packages, shared libraries, prefabs,
assembly definitions, scanners, validation runners, readiness dashboards,
agent-context exporters, scenes, and build targets. Future expansion should
stay incremental and validated.

Delivered engine-tooling record kinds include:

- `unity.package`
- `unity.shared-library`
- `unity.prefab`
- `unity.asmdef`
- `unity.scanner`
- `unity.validation-runner`
- `unity.readiness-dashboard`
- `unity.agent-context-exporter`

Useful future record kinds include:

- `unity.scriptable-object`
- `unity.addressable-group`
- `unity.input-action-map`
- `unity.platform-target`
- `unity.save-schema`
- `unity.localization-table`
- `unity.editor-window`

## Godot Pack

Existing pack ID: `verity.pack.godot`.

The current Godot pack describes Godot game implementation and engine-tooling
records for games made with Godot: projects, addons, shared libraries, scenes,
node contracts, resources, scripts, autoloads, input actions, export presets,
scanners, validation runners, readiness dashboards, and agent-context
exporters. Generic game design, gameplay, content, economy, progression,
liveops, and evidence records should still come from the game-oriented packs;
the Godot pack owns the Godot implementation boundary.

Delivered engine-tooling record kinds include:

- `godot.project`
- `godot.addon`
- `godot.shared-library`
- `godot.scene`
- `godot.node-contract`
- `godot.resource`
- `godot.script`
- `godot.autoload`
- `godot.input-action`
- `godot.export-preset`
- `godot.scanner`
- `godot.validation-runner`
- `godot.readiness-dashboard`
- `godot.agent-context-exporter`

Useful future record kinds include:

- `godot.signal`
- `godot.group`
- `godot.gdextension`
- `godot.save-schema`
- `godot.localization`
- `godot.editor-panel`

## Unreal Pack

Existing pack ID: `verity.pack.unreal`.

The current Unreal pack describes Unreal game implementation and engine-tooling
records for games made with Unreal: projects, plugins, modules, targets, maps,
Blueprints, data assets, gameplay tags, input actions, scanners, validation
runners, readiness dashboards, and agent-context exporters. Generic game
design, gameplay, content, economy, progression, liveops, and evidence records
should still come from the game-oriented packs; the Unreal pack owns the
Unreal implementation boundary.

Delivered engine-tooling record kinds include:

- `unreal.project`
- `unreal.plugin`
- `unreal.module`
- `unreal.target`
- `unreal.map`
- `unreal.blueprint`
- `unreal.data-asset`
- `unreal.gameplay-tag`
- `unreal.input-action`
- `unreal.scanner`
- `unreal.validation-runner`
- `unreal.readiness-dashboard`
- `unreal.agent-context-exporter`

Useful future record kinds include:

- `unreal.build-config`
- `unreal.world`
- `unreal.level`
- `unreal.blueprint-interface`
- `unreal.actor`
- `unreal.component`
- `unreal.primary-asset`
- `unreal.data-table`
- `unreal.curve-table`
- `unreal.material`
- `unreal.animation-blueprint`
- `unreal.enhanced-input-mapping`
- `unreal.game-feature`
- `unreal.gameplay-ability`
- `unreal.gameplay-effect`
- `unreal.save-game-schema`
- `unreal.asset-manager-rule`
- `unreal.cook-rule`
- `unreal.chunk`
- `unreal.localization-target`
- `unreal.platform-build-target`
- `unreal.shared-plugin-dependency`
- `unreal.editor-tool`

## Engine Evidence Traceability

Engine examples compose the engine packs with `verity.pack.evidence` so
implementation proof can target concrete engine records instead of only a broad
product scope.

Supported evidence reference rules include:

- `unity.validation-runner` `producesEvidence` `evidence.test`
- `godot.validation-runner` `producesEvidence` `evidence.test`
- `unreal.validation-runner` `producesEvidence` `evidence.test`
- `evidence.test` `proves` `unity.project`
- `evidence.test` `proves` `unity.scene`
- `evidence.test` `proves` `godot.project`
- `evidence.test` `proves` `godot.scene`
- `evidence.test` `proves` `unreal.project`
- `evidence.test` `proves` `unreal.map`
- `evidence.build` `proves` `unity.build-target`
- `evidence.build` `proves` `godot.export-preset`
- `evidence.build` `proves` `unreal.target`

For a skipped or blocked engine check, model the evidence record with
`result: "skipped"` or `result: "inconclusive"` and keep the normal `proves`
relationship to the engine record being checked. Do not introduce ad hoc
relationships such as `provesGap` in downstream workspaces.

## Product-Delivery Pack

Existing pack ID: `verity.pack.product-delivery`.

This pack should describe repositories that use VeritySpec as their
project-management and product-delivery source of truth. It should not replace
GitHub workflow objects; it should connect those objects to product-contract
records, readiness gates, evidence requirements, and generated reports.

This first built-in slice covers the downstream rebuild blocker after the
Unity, Godot, and Unreal engine packs: private spec-driven repositories for
engine toolkits and game projects need built-in vocabulary for proprietary
posture, GitHub-native project management, decision completeness,
implementation readiness, evidence states, release and distribution policy,
support, maintenance, operations, archive and decommission policy, scanners,
generators, editor surfaces, and agent-context export.

Delivered record kinds:

- `product.scope`
- `commercial.posture`
- `project-management.model`
- `decision.record`
- `readiness.profile`
- `evidence.requirement`
- `release.process`
- `operations.model`
- `support.policy`
- `maintenance.policy`
- `archive.policy`
- `decommission.policy`
- `scanner.capability`
- `generator.capability`
- `validation.runner`
- `editor.surface`
- `agent-context.exporter`

The first follow-on lifecycle slices now live in `verity.pack.mobile`,
`verity.pack.liveops`, `verity.pack.progression`, and `verity.pack.evidence`.
They capture mobile release lifecycle, privacy/store posture, SDK inventory,
monetization posture, soft-launch and launch-candidate records, liveops
configuration, remote config, rollback, analytics, support, save migration,
decommissioning, data deletion, archive handling, progression XP/level/unlock
contracts, and concrete implementation evidence without turning
product-delivery into a catch-all pack.

Future follow-on packs or product-delivery expansions should focus on
portfolio and dependency behavior rather than duplicating mobile, liveops,
progression, or evidence records.

## Implementation Acceptance Criteria

Implementation sprints for these packs and follow-on expansions should include:

- Built-in pack manifests that pass `verity pack validate`.
- Strict JSON Schemas for every new kind.
- Readiness gates where the record kind affects release or implementation
  readiness.
- Reference rules that prove the product-contract graph is coherent.
- Fixtures or examples for the affected Unity, Godot, Unreal, and
  spec-driven product-delivery workspaces.
- Example workspaces that pass `verity validate`, `verity lint --strict`,
  `verity readiness --strict`, and `verity graph`.
- Public docs that describe the packs as engine-tooling and product-management
  support, not commercial, legal, marketplace, or certification guarantees.
- Tests covering pack validation, example validation, strict linting,
  readiness checks, graph behavior, and generator behavior where relevant.

The first implementation sprint should choose a narrow vertical slice rather
than adding every listed record kind at once.
