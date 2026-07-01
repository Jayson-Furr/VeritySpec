# Cross-Workspace Dependencies

VeritySpec supports a first local-only workspace dependency prototype. A
workspace can declare direct local, readonly dependencies, reference exported
records from those dependency workspaces, and include exported dependency
records in graph output.

This is the first executable step toward a graph of workspaces and records. It
does not add remote registries, Git authentication, transitive dependency
policy, lockfiles, dependency update commands, or record-level visibility
fields yet.

## Goal

The goal is to let one VeritySpec workspace depend on another workspace without
copying its records into the consuming workspace.

This makes shared contracts explicit for systems such as:

- products that depend on shared SDK or library workspaces
- services that consume shared event-contract workspaces
- applications that use shared design-system or platform workspaces
- games that depend on a shared Unity runtime workspace
- portfolios that need impact analysis across many related workspaces

The long-term result should be a graph of workspaces and records, not only a
graph of records inside one workspace.

## Pack Versus Workspace

Do not confuse packs and workspaces.

A pack teaches VeritySpec vocabulary and behavior:

- record kinds
- JSON Schemas
- readiness gates
- reference rules
- generators or reports

A workspace contains product, service, game, library, or platform records that
use those packs.

For example, `verity.pack.unity` defines Unity implementation vocabulary such
as package dependency and scene record kinds. A
`studio.library.shared_unity_runtime` workspace contains actual records for a
studio's shared Unity runtime. A game workspace should depend on the shared
Unity runtime workspace, not on a copied set of library records or on the pack
itself.

## Current Prototype Boundary

The current implementation supports:

- local path dependencies
- readonly dependencies
- direct dependencies
- explicit dependency aliases
- workspace ID checks
- exact and caret version checks
- manifest-level exported-record checks
- alias-qualified cross-workspace reference resolution
- dependency-aware validation and graph reporting

The current implementation does not support:

- remote registries
- Git authentication
- package publishing
- mutable writes into dependency workspaces
- transitive dependency override logic
- cyclic dependency policies beyond the existing graph cycle checks
- partial dependency loading
- multi-registry resolution
- `verityspec.lock.json` generation or enforcement
- record-level `visibility` or `exports` fields

This boundary keeps the first version executable and reviewable while leaving
room for lockfiles, remote dependency sources, and package-level visibility
rules later.

## Workspace Dependency Shape

A consuming workspace declares local dependencies with a `dependencies` array:

```json
{
  "workspace": "studio.game.dream_extraction",
  "specVersion": "v0.2.0",
  "packs": [
    "verity.core",
    "verity.pack.unity"
  ],
  "packPaths": [],
  "dependencies": [
    {
      "id": "studio.library.shared_unity_runtime",
      "alias": "sharedUnity",
      "version": "^1.2.0",
      "source": "../../libraries/shared-unity-runtime",
      "mode": "readonly"
    }
  ],
  "records": [
    "records/**/*.json"
  ]
}
```

Dependency declarations use these fields:

- `id`: expected workspace ID in the dependency workspace manifest.
- `alias`: local reference prefix, such as `sharedUnity`.
- `source`: local filesystem path to the dependency workspace.
- `mode`: currently only `readonly` is supported.
- `version`: optional exact or caret version constraint checked against the
  dependency workspace manifest `version`.

## Exported Records

Dependency workspaces need visibility rules. The current prototype uses a
manifest-level `exports` array so existing strict record schemas do not need
record-field churn.

```json
{
  "workspace": "studio.library.shared_unity_runtime",
  "version": "1.2.4",
  "specVersion": "v0.2.0",
  "packs": [
    "verity.core",
    "verity.pack.unity"
  ],
  "packPaths": [],
  "exports": [
    "unity.package.save_system"
  ],
  "records": [
    "records/**/*.json"
  ]
}
```

Only exported records can be referenced from dependent workspaces. Deprecated
exported records resolve with the normal deprecated-reference warning. Removed
exported records fail through the normal removed-reference validation path.

Future record-level visibility could expose itself with fields such as:

```json
{
  "id": "unity.package.save_system",
  "kind": "unity.package",
  "name": "Save System",
  "status": "ready",
  "owner": "runtime",
  "visibility": "public",
  "exports": true
}
```

That future shape needs pack schema updates, compatibility fixtures, and
migration guidance before it replaces manifest-level exports.

## Reference Forms

Authors use alias-qualified references:

```text
sharedUnity::unity.package.save_system
```

The current prototype keeps that friendly form in records and graph output.
A future resolver can also emit canonical resolved URIs such as:

```text
verity://workspace/studio.library.shared_unity_runtime@1.2.4/record/unity.package.save_system
```

The resolver should preserve enough resolved metadata for validation,
lockfiles, graph output, diffing, and impact analysis:

- dependency alias
- dependency workspace ID
- resolved dependency version
- referenced record ID
- referenced record kind
- referenced record status
- referenced record export state
- referenced record content hash or record-set hash

## Resolution Flow

The current resolver:

1. Loads the consuming workspace.
2. Parses declared direct dependencies from local paths.
3. Confirms each dependency source path exists.
4. Loads each dependency workspace.
5. Confirms each dependency workspace ID matches the declaration.
6. Confirms each dependency version satisfies the optional constraint.
7. Confirms aliases are unique and stable.
8. Builds a local record index for the consuming workspace.
9. Builds dependency record indexes and manifest-level export sets.
10. Resolves local references against local records.
11. Resolves alias-qualified references against dependency records.
12. Fails when the dependency record is missing or not exported.
13. Applies normal removed, deprecated, and reference-rule checks to resolved
    dependency targets.

The resolver does not silently fall back from an alias-qualified reference to a
local record with the same ID. That keeps cross-workspace contracts
unambiguous.

## Validation Issue Codes

Dependency validation uses normal VeritySpec issue output:

- `workspace.dependencies.invalid`
- `dependency.declaration.invalid`
- `dependency.alias.duplicate`
- `dependency.alias.unknown`
- `dependency.mode.unsupported`
- `dependency.source.missing`
- `dependency.load.failed`
- `dependency.id.mismatch`
- `dependency.version.missing`
- `dependency.version.unsatisfied`
- `dependency.exports.invalid`
- `dependency.reference.missing`
- `dependency.reference.not_exported`

These codes are available through `verity explain` and the issue-code catalog.

## Graph Output

`verity graph --format json` includes exported dependency records as
alias-qualified dependency nodes. Dependency metadata is also included in a
top-level `dependencies` list.

```bash
verity graph tests/fixtures/workspace_dependencies/consumer --format json
```

Dependency nodes include fields such as:

- `workspaceRole: "dependency"`
- `dependencyAlias`
- `dependencyWorkspace`
- `dependencySource`
- `exported`

This lets downstream tools distinguish local records from dependency records
while still following reference edges such as:

```text
unity.project.dream_extraction -> sharedUnity::unity.package.save_system
```

## Current Smoke Fixture

The committed smoke fixture demonstrates one Unity game workspace consuming an
exported package from a shared Unity runtime workspace:

```bash
verity validate tests/fixtures/workspace_dependencies/consumer
verity lint tests/fixtures/workspace_dependencies/consumer --strict
verity readiness tests/fixtures/workspace_dependencies/consumer --strict
verity graph tests/fixtures/workspace_dependencies/consumer --format json
```

Negative fixtures cover non-exported records, missing dependency records,
unknown aliases, missing local sources, and workspace ID mismatches.

## Lockfile Boundary

A dependency lockfile should make validation reproducible in CI, but lockfile
generation and enforcement are future work.

Conceptual file:

```text
verityspec.lock.json
```

The lockfile should record what was actually resolved:

```json
{
  "dependencies": [
    {
      "id": "studio.library.shared_unity_runtime",
      "alias": "sharedUnity",
      "resolvedVersion": "1.2.4",
      "source": "../../libraries/shared-unity-runtime",
      "revision": "a13f9c2",
      "recordSetHash": "sha256:...",
      "packVersions": {
        "verity.pack.unity": "0.3.0"
      }
    }
  ]
}
```

The first lockfile implementation should be deterministic and local-path
oriented. It should not try to represent every future remote source shape.

Validation should eventually be able to fail when:

- the lockfile is missing while strict dependency mode requires it
- the resolved workspace differs from the lockfile
- the record-set hash changed unexpectedly
- a dependency version no longer satisfies the workspace manifest
- a referenced exported record was removed or made internal

## Future Work

Future dependency work should add behavior in small executable slices:

- dependency lockfile generation and stale-lockfile validation
- dependency-aware diff and product-impact reports
- dependency cycle policy across workspace boundaries
- canonical resolved URI output
- record-level visibility fields and migrations
- local dependency command family such as `verity deps list`, `verity deps
  resolve`, and `verity deps lock`
- remote registry or Git dependency sources only after local dependency
  semantics are stable

## Integration Workspaces

Integration workspaces still remain useful for combined validation contexts
where the user wants to load several local workspaces as one record graph:

```json
{
  "workspace": "studio.integration.dream_extraction_shared_runtime",
  "specVersion": "v0.2.0",
  "packs": [
    "verity.core",
    "verity.pack.unity"
  ],
  "packPaths": [],
  "records": [
    "../../games/dream-extraction/records/**/*.json",
    "../../libraries/shared-unity-runtime/records/**/*.json"
  ]
}
```

This pattern validates a combined record graph, but it does not model
dependency aliases, exported-record boundaries, version constraints, or
lockfiles. Treat integration workspaces as a bridge for aggregate validation,
not a replacement for workspace dependencies.
