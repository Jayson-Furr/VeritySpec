# Cross-Workspace Dependencies

VeritySpec currently validates one workspace at a time. This note defines the
first design boundary for future cross-workspace dependencies before any
workspace schema, resolver, lockfile, or CLI behavior is implemented.

No schema changes are introduced by this design note. The first implementation
should stay local-only, readonly, and direct-dependency oriented so VeritySpec
can prove the model before adding Git, registry, remote, or transitive
dependency behavior.

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
`studio.library.shared_unity_runtime` workspace would contain actual records
for a studio's shared Unity runtime. A game workspace should depend on the
shared Unity runtime workspace, not on a copied set of library records or on
the pack itself.

## Phase 1 Boundary

The first implementation should support only:

- local path dependencies
- readonly dependencies
- direct dependencies
- explicit dependency aliases
- workspace ID and version checks
- exported-record visibility checks
- cross-workspace reference resolution
- deterministic lockfile generation
- dependency-aware validation and graph reporting

The first implementation should not support:

- remote registries
- Git authentication
- package publishing
- mutable writes into dependency workspaces
- transitive dependency override logic
- cyclic dependency policies beyond failing cycles
- partial dependency loading
- multi-registry resolution

That boundary keeps the first version executable and reviewable.

## Workspace Dependency Shape

A future workspace manifest could declare local dependencies with a
`dependencies` array:

```json
{
  "workspace": "studio.game.dream_extraction",
  "specVersion": "v0.3.0",
  "packs": [
    "verity.core",
    "verity.pack.game",
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

The exact future `specVersion` is intentionally not chosen here. Adding
`dependencies` is a workspace-format change and should ship with migration,
compatibility fixtures, release notes, and validation tests.

## Exported Records

Dependency workspaces need visibility rules. A consuming workspace should only
reference records that the dependency exports.

A future record could expose itself with fields such as:

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

Recommended visibility behavior:

- public exported records can be referenced from dependent workspaces
- internal records remain implementation details
- deprecated exported records resolve but warn, or fail under strict policy
- removed records fail when referenced

The first implementation should prefer explicit exported-record fields over
implicit public-by-default behavior. That keeps dependency workspaces from
accidentally committing to internal records as public contracts.

## Reference Forms

Authors need a readable reference form. Resolvers need a canonical form.

Friendly authoring form:

```text
sharedUnity::unity.package.save_system
```

Canonical resolved form:

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
- referenced record visibility/export state
- referenced record content hash or record-set hash

## Resolution Flow

A conservative resolver should:

1. Load the consuming workspace.
2. Load declared direct dependencies from local paths.
3. Confirm each dependency workspace ID matches the manifest declaration.
4. Confirm each dependency version satisfies the declared constraint.
5. Confirm aliases are unique and stable.
6. Build a local record index for the consuming workspace.
7. Build exported-record indexes for dependency workspaces.
8. Resolve local references against local records.
9. Resolve alias-qualified references against exported dependency records.
10. Normalize resolved references into canonical URIs for reports and lockfiles.
11. Fail cycles in the workspace-dependency graph.

The resolver should not silently fall back from an alias-qualified reference to
a local record with the same ID. That would make cross-workspace contracts
ambiguous.

## Lockfile Boundary

A dependency lockfile should make validation reproducible in CI.

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

Validation should be able to fail when:

- the lockfile is missing while strict dependency mode requires it
- the resolved workspace differs from the lockfile
- the record-set hash changed unexpectedly
- a dependency version no longer satisfies the workspace manifest
- a referenced exported record was removed or made internal

## Validation Goals

Future dependency-aware validation should check:

- declared dependency paths exist
- dependency workspaces load successfully
- dependency workspace IDs match declarations
- dependency versions satisfy constraints
- dependency aliases are unique
- dependency packs are compatible with the consuming workspace
- cross-workspace references resolve
- referenced records are exported
- deprecated dependency records are reported
- removed dependency records fail validation
- relationship rules allow the source kind, relationship, and target kind
- dependency cycles fail validation
- lockfile contents match resolved dependencies when lockfile checking is
  enabled

These checks should use normal VeritySpec issue codes so CI can fail with the
same product-contract workflow used for local records.

## Graph, Diff, And Impact

Dependency-aware graph output should distinguish local records from dependency
records. It should show which local records consume which exported dependency
records and which dependency workspace supplied each target.

Dependency-aware diff and product-impact reports should be able to answer:

- which local records changed
- which dependency records changed
- which local records consume changed dependency records
- whether a dependency update is breaking
- whether docs, generators, readiness gates, or release reviews need to rerun

This is the path from one-workspace validation to ecosystem-level contract
analysis.

## Future Commands

The first implementation can extend existing commands before adding a full
dependency command family:

```bash
verity validate ./workspace --include-dependencies
verity graph ./workspace --include-dependencies
verity diff old-workspace new-workspace --include-dependencies
verity readiness ./workspace --include-dependencies
```

A later command family could include:

```bash
verity deps list ./workspace
verity deps resolve ./workspace
verity deps lock ./workspace
verity deps update ./workspace
verity deps graph ./workspace
verity deps explain ./workspace sharedUnity::unity.package.save_system
```

The project should add these commands only when the resolver, lockfile, and
validation contract are stable enough to test.

## Transitional Pattern

Until first-class dependencies exist, users can model dependency checks through
integration workspaces that load records from multiple local workspaces:

```json
{
  "workspace": "studio.integration.dream_extraction_shared_runtime",
  "specVersion": "v0.2.0",
  "packs": [
    "verity.core",
    "verity.pack.game",
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
lockfiles. It should be treated as a bridge, not the final dependency model.

## First-Implementation Gate

Before implementation begins, the sprint should include:

- a GitHub issue and milestone for the exact first dependency scope
- workspace-format migration planning for a `dependencies` field
- JSON Schema changes and compatibility fixtures
- local dependency fixtures with positive and negative cases
- exported-record visibility tests
- alias-qualified reference-resolution tests
- lockfile generation and stale-lockfile tests
- validation issue-code documentation
- graph and diff smoke coverage
- README, changelog, roadmap, and release-note updates

If any of those pieces are not ready, the project should add narrower fixtures
or another design note before adding behavior.
