# Engine and Product-Delivery Pack Direction

This note captures future VeritySpec pack direction for engine-tooling
repositories and spec-driven product delivery. It is a planning document, not a
claim that the listed packs or records already exist.

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

These future packs should support engine-tooling repositories and spec-driven
product management without making commercial, legal, marketplace-readiness, or
certification claims.

## Unity Pack Expansion

Existing pack ID: `verity.pack.unity`.

The current Unity pack covers Unity implementation and engine-tooling records:
projects, package dependencies, packages, shared libraries, prefabs, assembly
definitions, scanners, validation runners, readiness dashboards,
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

Proposed pack ID: `verity.pack.godot`.

The Godot pack should describe Godot projects, addons, runtime contracts,
editor surfaces, validation tooling, agent handoff surfaces, and the
engine-specific contracts needed by games made with Godot. Generic game design,
gameplay, content, economy, progression, liveops, and evidence records should
still come from the game-oriented packs; the Godot pack should own the Godot
implementation boundary.

Useful future record kinds include:

- `godot.project`
- `godot.addon`
- `godot.shared-library`
- `godot.scene`
- `godot.node-contract`
- `godot.resource`
- `godot.script`
- `godot.autoload`
- `godot.signal`
- `godot.group`
- `godot.input-action`
- `godot.export-preset`
- `godot.gdextension`
- `godot.save-schema`
- `godot.localization`
- `godot.editor-panel`
- `godot.scanner`
- `godot.validation-runner`
- `godot.readiness-dashboard`
- `godot.agent-context-exporter`

## Unreal Pack

Proposed pack ID: `verity.pack.unreal`.

The Unreal pack should describe Unreal projects, plugins, modules, assets,
build targets, editor tools, validation tooling, agent handoff surfaces, and
the engine-specific contracts needed by games made with Unreal. Generic game
design, gameplay, content, economy, progression, liveops, and evidence records
should still come from the game-oriented packs; the Unreal pack should own the
Unreal implementation boundary.

Useful future record kinds include:

- `unreal.project`
- `unreal.plugin`
- `unreal.module`
- `unreal.target`
- `unreal.build-config`
- `unreal.map`
- `unreal.world`
- `unreal.level`
- `unreal.blueprint`
- `unreal.blueprint-interface`
- `unreal.actor`
- `unreal.component`
- `unreal.data-asset`
- `unreal.primary-asset`
- `unreal.data-table`
- `unreal.curve-table`
- `unreal.material`
- `unreal.animation-blueprint`
- `unreal.input-action`
- `unreal.enhanced-input-mapping`
- `unreal.game-feature`
- `unreal.gameplay-tag`
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
- `unreal.scanner`
- `unreal.validation-runner`
- `unreal.readiness-dashboard`
- `unreal.agent-context-exporter`

## Product-Delivery Pack

Proposed pack ID: `verity.pack.product-delivery`.

This pack should describe repositories that use VeritySpec as their
project-management and product-delivery source of truth. It should not replace
GitHub workflow objects; it should connect those objects to product-contract
records, readiness gates, evidence requirements, and generated reports.

Useful future record kinds include:

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

## Implementation Acceptance Criteria

Future implementation sprints for these packs should include:

- Built-in pack manifests that pass `verity pack validate`.
- Strict JSON Schemas for every new kind.
- Readiness gates where the record kind affects release or implementation
  readiness.
- Reference rules that prove the product-contract graph is coherent.
- Fixtures or examples for Unity, Godot, Unreal, and spec-driven product
  delivery workspaces.
- Example workspaces that pass `verity validate`, `verity lint --strict`,
  `verity readiness --strict`, and `verity graph`.
- Public docs that describe the packs as engine-tooling and product-management
  support, not commercial, legal, marketplace, or certification guarantees.
- Tests covering pack validation, example validation, strict linting,
  readiness checks, graph behavior, and generator behavior where relevant.

The first implementation sprint should choose a narrow vertical slice rather
than adding every listed record kind at once.
