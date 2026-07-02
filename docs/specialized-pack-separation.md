# Specialized Pack Separation Plan

VeritySpec should move toward a smaller core runtime plus official extension
pack packages, but separation must be staged. The current bundled packs are
part of the public package contract, so this plan defines the gates that must
exist before any specialized pack is removed from the `verityspec` wheel.

This is not an immediate removal plan. Existing bundled packs remain available
until the extension-pack path can preserve workspace behavior without manual
`packPaths`, record-kind churn, or unsupported migration work.

## Goals

- Keep the `verityspec` package focused on the contract engine: CLI,
  workspace loading, validation, readiness, graphing, diffing, migrations,
  generator dispatch, pack validation, and pack discovery.
- Let specialized domain packs become separately installable official packages
  once their contracts are stable enough.
- Preserve existing pack IDs and record kinds so workspaces do not need to
  rewrite product contracts just because packaging changes.
- Provide compatibility metadata, migration guidance, examples, tests, and
  rollback instructions before any package split becomes user-visible.
- Keep the current bundled-pack behavior as the fallback until official
  extension packages are proven in CI.

## Candidate Packages

The first separation candidates are domain-heavy packs whose schemas are useful
but not part of the core runtime itself.

| Official package | Pack IDs initially carried |
|---|---|
| `verityspec-pack-game` | `verity.pack.game-core`, `verity.pack.game-assets`, `verity.pack.gameplay`, `verity.pack.content`, `verity.pack.economy`, `verity.pack.progression` |
| `verityspec-pack-mobile` | `verity.pack.mobile` |
| `verityspec-pack-liveops` | `verity.pack.liveops` |
| `verityspec-pack-unity` | `verity.pack.unity` |
| `verityspec-pack-godot` | `verity.pack.godot` |
| `verityspec-pack-unreal` | `verity.pack.unreal` |

These are Python distribution names, not new pack IDs. The pack IDs should
remain stable so records keep the same `kind` values and workspace manifests
continue to list the same `packs`.

Broad and cross-cutting packs should remain close to the core until there is a
separate reason to split them:

- `verity.core`
- `verity.pack.api`
- `verity.pack.cli`
- `verity.pack.events`
- `verity.pack.security`
- `verity.pack.observability`
- `verity.pack.accessibility`
- `verity.pack.compliance`
- `verity.pack.deployment`
- `verity.pack.product-delivery`
- `verity.pack.evidence`

## Required Runtime Gates

Specialized packs cannot move out of the bundled wheel safely until these
runtime gates exist:

1. Installed-pack discovery through the `verityspec.packs` entry-point group.
2. Compatibility metadata that declares supported `verityspec` versions,
   workspace format versions, pack API level, and schema stability.
3. A registry policy for official extension packages.
4. A detach gate that allows a formerly bundled official pack ID to be supplied
   by an installed package without opening arbitrary built-in pack shadowing.
5. Deterministic parity tests proving bundled and installed package variants
   expose the same schemas, readiness gates, reference rules, generator
   metadata, examples, and golden outputs.
6. Migration and rollback guidance for existing workspaces.

Built-in pack IDs are reserved until an official detach gate exists. The
current collision protection is intentional; it prevents unrelated installed
packages from shadowing bundled packs.

## Compatibility Metadata

Future official extension packages should declare compatibility in their
manifest or package metadata before they can be detached from core. The exact
schema can evolve, but it should answer:

- Which `verityspec` package versions are supported?
- Which workspace format versions are supported?
- Which pack API level is required?
- Which pack IDs and record kinds are provided?
- Which generators, readiness gates, and reference rules are expected?
- Is the package bundled, mirrored, detached, deprecated, or removed?

The metadata should be machine-readable so `verity pack validate`, `verity
doctor`, CI templates, and future migration tooling can fail early when a
workspace installs an incompatible extension package.

The first proposed shape and lifecycle vocabulary are captured in
[Installed pack compatibility metadata](installed-pack-compatibility-metadata.md).
That design note is intentionally documentation-only until runtime diagnostics
and detach gates are implemented in later sprints.

## Migration Guidance

A packaging split should not force users to rename records or rewrite `kind`
values. The expected migration path is:

1. Keep existing workspaces using the same `packs` entries.
2. Add package-manager dependencies such as `verityspec-pack-unity` where a
   workspace needs detached engine coverage.
3. Run `verity pack doctor --format json` and `verity pack list --format json`
   to confirm pack discovery health and whether each pack is loaded from
   `built-in`, `installed`, or `external` source.
4. Run `verity validate`, `verity lint --strict`, `verity readiness --strict`,
   and generator checks before changing CI pins.
5. Use migration reports for any future manifest or compatibility-field
   changes.

The first detached package release should be additive from the user's point of
view. If an installed official package is missing or incompatible, the current
bundled pack should remain the safe fallback during the transition period.

## Rollback Criteria

Every separation sprint should include rollback instructions. A rollback is
required if any of these happen:

- installed extension packages fail to load by pack ID;
- schemas, readiness gates, reference rules, or generator metadata drift from
  the bundled pack without an explicit migration;
- example workspaces pass with bundled packs but fail with installed packs;
- downstream CI templates cannot install the required packages reproducibly;
- `verity pack validate` cannot explain the incompatibility clearly;
- users cannot return to the bundled pack without changing record IDs or
  record kinds.

Rollback should mean reverting to the bundled pack source, not rewriting
product contracts.

## Separation Phases

### Phase 0: Bundled Baseline

Current state. Specialized packs are bundled and validated with the core
package. This keeps public installs simple while schemas and examples mature.

### Phase 1: Compatibility Metadata

Add metadata to pack manifests or package metadata, then teach pack validation
and doctor diagnostics to report compatibility. This phase should not change
how workspaces load packs.

### Phase 2: Official Mirror Packages

Create official extension package candidates that contain the same pack
manifests, schemas, docs, examples, and tests as the bundled packs. CI should
compare bundled and installed variants, including `verity pack compare` checks
against official-extension mirror fixtures, but normal users should still
receive bundled packs by default.

### Phase 3: Detachable Official Packs

Enable a controlled official detach gate for selected pack IDs. This gate must
distinguish official extension packages from arbitrary built-in shadowing and
must keep local `packPaths` override behavior explicit.

### Phase 4: Documentation and CI Migration

Update README, pack docs, downstream CI templates, release notes, migration
guidance, and examples so users can choose bundled or installed package
sources deliberately.

### Phase 5: Bundled Deprecation Window

Only after installed packages are proven, document a bundled-pack deprecation
window. Deprecation should warn first, preserve rollback, and avoid removing
pack IDs until a later release with explicit migration evidence.

## Non-Goals

- Do not remove specialized bundled packs in the first separation sprint.
- Do not rename pack IDs or record kinds for packaging reasons.
- Do not make arbitrary installed packages shadow built-in pack IDs.
- Do not split packages without parity tests and migration guidance.
- Do not turn `verityspec` into an empty launcher package; the executable
  contract engine remains in core.

## Sprint Standard

A future sprint that actually detaches a pack must include:

- a GitHub issue and milestone naming the pack IDs and package names;
- compatibility metadata;
- installed-package fixture coverage;
- bundled-versus-installed parity tests;
- updated examples and documentation;
- downstream CI examples;
- changelog, roadmap, and release notes;
- rollback criteria and manual verification steps.

Until those gates exist, specialized packs remain bundled.
