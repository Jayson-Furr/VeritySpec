# Unity Pack

`verity.pack.unity` adds the first built-in Unity implementation-surface
records without moving generic game design, liveops, evidence, release, or
workspace dependency behavior into the core kernel.

## Record Kinds

- `unity.project`: a Unity project contract with Unity version, project path,
  render pipeline, scripting backend, target platforms, assembly definitions,
  and references to package, scene, and build-target records.
- `unity.package-dependency`: a Unity package dependency contract with package
  name, version requirement, source, purpose, and required capabilities.
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
- `unity.project` `containsScene` `unity.scene`
- `unity.project` `buildsFor` `unity.build-target`
- `unity.scene` `usesPackage` `unity.package-dependency`
- `unity.build-target` `includesScene` `unity.scene`
- `unity.build-target` `usesPackage` `unity.package-dependency`

This scope composes with `verity.pack.game-core`: game-core defines early game
product intent, modes, loops, and prototype scope; Unity records describe the
first engine-specific implementation boundary.

## Readiness

Strict readiness checks require each ready Unity record to have enough metadata
for implementation and build handoff:

- Unity projects need a Unity version, project path, render pipeline, scripting
  backend, at least one target platform, and references to package, scene, and
  build-target records.
- Package dependencies need package name, version requirement, source, and
  purpose.
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
project, one Unity package dependency, one prototype scene, and one PC
development build target.
