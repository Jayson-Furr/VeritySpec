# Unity Pack

`verity.pack.unity` adds built-in Unity implementation and engine-tooling
records without moving generic game design, liveops, evidence, release, or
workspace dependency behavior into the core kernel.

## Record Kinds

- `unity.project`: a Unity project contract with Unity version, project path,
  render pipeline, scripting backend, target platforms, assembly definitions,
  and references to package, shared-library, prefab, assembly, scene, and
  build-target records.
- `unity.package-dependency`: a Unity package dependency contract with package
  name, version requirement, source, purpose, and required capabilities.
- `unity.package`: a concrete Unity package contract with package name,
  version, source, package path, purpose, and package capabilities.
- `unity.shared-library`: a reusable Unity library contract that groups
  package records, exported capabilities, repository metadata, and supporting
  implementation references.
- `unity.prefab`: a prefab contract with prefab path, role, owning package or
  assembly references, and implementation links.
- `unity.asmdef`: a Unity assembly definition contract with assembly path,
  platform constraints, define constraints, and package references.
- `unity.scanner`: a scanner contract for Unity project/package/prefab/assembly
  inspection.
- `unity.validation-runner`: a validation-runner contract that names the
  Unity checks it runs and the scanner records it uses.
- `unity.readiness-dashboard`: a readiness-dashboard contract for Unity
  project/tooling status summaries.
- `unity.agent-context-exporter`: an agent-context exporter contract for
  bounded Unity implementation handoff artifacts.
- `unity.scene`: a Unity scene contract with scene path, role, load mode,
  build inclusion, and package references.
- `unity.build-target`: a Unity build target contract with platform, build
  configuration, output path, included scene IDs, scripting backend, and build
  references.

## Relationships

The pack declares these reference relationships:

- `product` `hasUnityProject` `unity.project`
- `game.product` `implementedBy` `unity.project`
- `unity.project` `usesPackage` `unity.package-dependency`
- `unity.project` `usesPackage` `unity.package`
- `unity.project` `usesSharedLibrary` `unity.shared-library`
- `unity.project` `containsScene` `unity.scene`
- `unity.project` `containsPrefab` `unity.prefab`
- `unity.project` `declaresAssembly` `unity.asmdef`
- `unity.project` `buildsFor` `unity.build-target`
- `unity.project` `scannedBy` `unity.scanner`
- `unity.project` `validatedBy` `unity.validation-runner`
- `unity.project` `reportsReadinessTo` `unity.readiness-dashboard`
- `unity.project` `exportsAgentContextWith` `unity.agent-context-exporter`
- `unity.package` `declaredByDependency` `unity.package-dependency`
- `unity.package` `providedByLibrary` `unity.shared-library`
- `unity.shared-library` `includesPackage` `unity.package`
- `unity.shared-library` `declaresAssembly` `unity.asmdef`
- `unity.scene` `usesPackage` `unity.package-dependency`
- `unity.scene` `usesPackage` `unity.package`
- `unity.scene` `usesPrefab` `unity.prefab`
- `unity.scene` `implementedByAssembly` `unity.asmdef`
- `unity.prefab` `usesPackage` `unity.package`
- `unity.prefab` `usesPackage` `unity.package-dependency`
- `unity.prefab` `implementedByAssembly` `unity.asmdef`
- `unity.asmdef` `usesPackage` `unity.package`
- `unity.asmdef` `usesPackage` `unity.package-dependency`
- `unity.build-target` `includesScene` `unity.scene`
- `unity.build-target` `usesPackage` `unity.package-dependency`
- `unity.build-target` `usesPackage` `unity.package`
- `unity.scanner` `scansProject` `unity.project`
- `unity.scanner` `scansPackage` `unity.package`
- `unity.scanner` `scansPrefab` `unity.prefab`
- `unity.scanner` `scansAssembly` `unity.asmdef`
- `unity.validation-runner` `runsScanner` `unity.scanner`
- `unity.validation-runner` `reportsTo` `unity.readiness-dashboard`
- `unity.readiness-dashboard` `tracksProject` `unity.project`
- `unity.readiness-dashboard` `tracksRunner` `unity.validation-runner`
- `unity.agent-context-exporter` `describesProject` `unity.project`
- `unity.agent-context-exporter` `includesDashboard` `unity.readiness-dashboard`
- `unity.agent-context-exporter` `includesRunner` `unity.validation-runner`
- `unity.agent-context-exporter` `includesScanner` `unity.scanner`

This scope composes with `verity.pack.game-core`: game-core defines early game
product intent, modes, loops, and prototype scope; Unity records describe the
engine-specific implementation and tooling boundary.

When the workspace also loads `verity.pack.evidence`, Unity validation runners
can use `producesEvidence` to point at `evidence.test` records. Test evidence
can directly prove `unity.project` and `unity.scene` records, and build
evidence can directly prove `unity.build-target` records.

## Readiness

Strict readiness checks require each ready Unity record to have enough metadata
for implementation and build handoff:

- Unity projects need a Unity version, project path, render pipeline, scripting
  backend, at least one target platform, and references to package,
  shared-library, prefab, assembly, scene, and build-target records.
- Package dependencies need package name, version requirement, source, and
  purpose.
- Packages need package name, version, source, and purpose.
- Shared libraries need package references, exported capabilities, and
  implementation references.
- Prefabs need a prefab path, role, and implementation references.
- Assembly definitions need assembly name, asmdef path, root namespace, and
  graph references.
- Scanners need scan scope, scanned record kinds, output format, and graph
  references.
- Validation runners need command metadata, scanner references, and graph
  references.
- Readiness dashboards need target audience, tracked record kinds, output
  format, and graph references.
- Agent-context exporters need export format, included record kinds, output
  path, and graph references.
- Scenes need scene path, role, load mode, and at least one supporting
  reference.
- Build targets need platform, build configuration, output path, at least one
  scene, and at least one supporting reference.

## Commands

```bash
verity validate examples/unity
verity lint examples/unity --strict
verity readiness examples/unity --strict
verity graph examples/unity
verity generate schema-bundle examples/unity --out build/unity-schema-bundle.json
```

The example workspace models the Dream Extraction game concept with one Unity
project, package dependency, package, shared library, assembly definition,
prefab, prototype scene, PC development build target, scanner, validation
runner, readiness dashboard, agent-context exporter, and evidence records for
contract validation plus PC development build proof.
