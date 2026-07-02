# Unreal Pack

`verity.pack.unreal` adds built-in Unreal game implementation and
engine-tooling records without moving generic game design, liveops, evidence,
release, or workspace dependency behavior into the core kernel.

The pack is meant for games made with Unreal and for Unreal-facing tooling
repositories. It connects `game.product` records to `unreal.project` records
while leaving player fantasy, modes, loops, gameplay, content, economy,
liveops, and evidence to the game-oriented packs.

## Record Kinds

- `unreal.project`: an Unreal project contract with engine version, project
  path, target platforms, and links to plugin, module, target, map, blueprint,
  data-asset, gameplay-tag, input-action, and tooling records.
- `unreal.plugin`: an Unreal plugin contract with plugin name, version,
  source, path, purpose, modules, and capabilities.
- `unreal.module`: an Unreal module contract with module name, type, path,
  loading phase, and dependency links.
- `unreal.target`: an Unreal build or editor target contract with target type,
  platform, configuration, maps, modules, and plugins.
- `unreal.map`: an Unreal map contract with map path, role, load mode, build
  inclusion, blueprints, and data assets.
- `unreal.blueprint`: an Unreal Blueprint contract with path, type, parent
  class, implementation purpose, module link, data assets, and input actions.
- `unreal.data-asset`: an Unreal data asset contract with asset path, type,
  primary asset type, purpose, and gameplay-tag links.
- `unreal.gameplay-tag`: an Unreal gameplay tag contract with tag name,
  domain, purpose, and consumer metadata.
- `unreal.input-action`: an Unreal input action contract with action name,
  value type, device types, mapping context, and handler metadata.
- `unreal.scanner`: a scanner contract for Unreal project, plugin, map,
  Blueprint, and data-asset inspection.
- `unreal.validation-runner`: a validation-runner contract that names the
  Unreal checks it runs and the scanner records it uses.
- `unreal.readiness-dashboard`: a readiness-dashboard contract for Unreal
  project/tooling status summaries.
- `unreal.agent-context-exporter`: an agent-context exporter contract for
  bounded Unreal implementation handoff artifacts.

## Relationships

The pack declares reference relationships that connect:

- products and game products to `unreal.project`
- Unreal projects to plugins, modules, targets, maps, Blueprints, data assets,
  gameplay tags, input actions, and tooling records
- plugins and targets to modules
- targets to maps and plugins
- maps to Blueprints and data assets
- Blueprints to modules, data assets, and input actions
- data assets to gameplay tags
- scanners, validation runners, dashboards, and agent-context exporters to the
  Unreal records they inspect, run, report, or describe

This scope composes with `verity.pack.game-core`: game-core defines early game
product intent, modes, loops, and prototype scope; Unreal records describe the
engine-specific implementation and tooling boundary for a game made with
Unreal.

When the workspace also loads `verity.pack.evidence`, Unreal validation
runners can use `producesEvidence` to point at `evidence.test` records. Test
evidence can directly prove `unreal.project` and `unreal.map` records, and
build evidence can directly prove `unreal.target` records.

## Readiness

Strict readiness checks require each ready Unreal record to have enough
metadata for implementation, target/build handoff, validation, and agent
handoff:

- Unreal projects need an engine version, project path, target platform, and
  graph links to implementation records.
- Plugins need plugin name, version, source, and purpose.
- Modules need module name, module type, module path, and graph links.
- Targets need target name, target type, platform, configuration, map refs, and
  graph links.
- Maps need map path, role, load mode, and graph links.
- Blueprints need path, type, purpose, and graph links.
- Data assets need asset path, asset type, purpose, and graph links.
- Gameplay tags need tag name, tag domain, and purpose.
- Input actions need action name, value type, and device types.
- Scanners, validation runners, readiness dashboards, and agent-context
  exporters need command or output metadata plus graph links to the records
  they scan, run, report, or describe.

## Commands

```bash
verity validate examples/unreal
verity lint examples/unreal --strict
verity readiness examples/unreal --strict
verity graph examples/unreal
verity generate schema-bundle examples/unreal --out build/unreal-schema-bundle.json
```

The example workspace models the Dream Extraction game concept with one Unreal
project, plugin, module, target, prototype map, Blueprint, data asset,
gameplay tag, input action, scanner, validation runner, readiness dashboard,
agent-context exporter, and evidence records for contract validation plus PC
development target proof.
