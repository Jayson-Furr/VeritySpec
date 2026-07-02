# Godot Pack

`verity.pack.godot` adds built-in Godot game implementation and engine-tooling
records without moving generic game design, liveops, evidence, release, or
workspace dependency behavior into the core kernel.

The pack is meant for games made with Godot and for Godot-facing tooling
repositories. It connects `game.product` records to `godot.project` records
while leaving player fantasy, modes, loops, gameplay, content, economy,
liveops, and evidence to the game-oriented packs.

## Record Kinds

- `godot.project`: a Godot project contract with Godot version, project path,
  renderer, target platforms, autoload references, and links to addon,
  shared-library, scene, node, resource, script, input, and export records.
- `godot.addon`: a Godot addon contract with addon name, version, source,
  addon path, purpose, and capabilities.
- `godot.shared-library`: a reusable Godot library contract that groups addon
  records, exported capabilities, repository metadata, and supporting script
  references.
- `godot.scene`: a Godot scene contract with scene path, scene role, root node,
  load mode, export inclusion, and implementation references.
- `godot.node-contract`: a Godot node contract with node path, node type,
  node role, required signals, required groups, and implementation links.
- `godot.resource`: a Godot resource contract with resource path, resource
  type, purpose, import settings, and graph references.
- `godot.script`: a Godot script contract with script path, language, class
  name, purpose, and addon references.
- `godot.autoload`: a Godot autoload/singleton contract with script reference
  and load order.
- `godot.input-action`: a Godot input action contract with event types,
  device types, deadzone metadata, and handling script links.
- `godot.export-preset`: a Godot export preset contract with platform, output
  path, included scenes, and addon references.
- `godot.scanner`: a scanner contract for Godot project, addon, scene, script,
  and resource inspection.
- `godot.validation-runner`: a validation-runner contract that names the
  Godot checks it runs and the scanner records it uses.
- `godot.readiness-dashboard`: a readiness-dashboard contract for Godot
  project/tooling status summaries.
- `godot.agent-context-exporter`: an agent-context exporter contract for
  bounded Godot implementation handoff artifacts.

## Relationships

The pack declares reference relationships that connect:

- products and game products to `godot.project`
- Godot projects to addons, shared libraries, scenes, nodes, resources,
  scripts, autoloads, input actions, export presets, and tooling records
- scenes to addons, node contracts, resources, and scripts
- node contracts to scripts, resources, and input actions
- shared libraries to addons and exported scripts
- export presets to scenes and addons
- scanners, validation runners, dashboards, and agent-context exporters to the
  Godot records they inspect, run, report, or describe

This scope composes with `verity.pack.game-core`: game-core defines early game
product intent, modes, loops, and prototype scope; Godot records describe the
engine-specific implementation and tooling boundary for a game made with
Godot.

When the workspace also loads `verity.pack.evidence`, Godot validation runners
can use `producesEvidence` to point at `evidence.test` records. Test evidence
can directly prove `godot.project` and `godot.scene` records, and build
evidence can directly prove `godot.export-preset` records.

## Readiness

Strict readiness checks require each ready Godot record to have enough metadata
for implementation, export, validation, and agent handoff:

- Godot projects need a Godot version, project path, renderer, target platform,
  and graph links to implementation records.
- Addons need addon name, version, source, and purpose.
- Shared libraries need addon references, exported capabilities, and graph
  links.
- Scenes need scene path, scene role, root node, load mode, and graph links.
- Node contracts need node path, node type, node role, and graph links.
- Resources need resource path, resource type, purpose, and graph links.
- Scripts need script path, language, purpose, and graph links.
- Autoloads need singleton name, script reference, load order, and graph links.
- Input actions need action name, event types, device types, and graph links.
- Export presets need preset name, platform, output path, included scenes, and
  graph links.
- Scanners, validation runners, readiness dashboards, and agent-context
  exporters need command or output metadata plus graph links to the records
  they scan, run, report, or describe.

## Commands

```bash
verity validate examples/godot
verity lint examples/godot --strict
verity readiness examples/godot --strict
verity graph examples/godot
verity generate schema-bundle examples/godot --out build/godot-schema-bundle.json
```

The example workspace models the Dream Extraction game concept with one Godot
project, addon, shared library, prototype scene, node contract, resource,
script, autoload, input action, PC export preset, scanner, validation runner,
readiness dashboard, agent-context exporter, and evidence records for contract
validation plus PC development export proof.
