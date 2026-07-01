# Packs

VeritySpec grows through packs. A pack contributes record kinds, JSON Schemas,
readiness gates, reference rules, and generator support without expanding the
core kernel.

Built-in packs currently include:

- `verity.core`: products, reusable object schemas, schema bundles,
  cross-pack coverage dashboards, product-impact reports, and pack capability
  indexes.
- `verity.pack.api`: API endpoints and OpenAPI generation.
- `verity.pack.cli`: CLI commands and CLI reference generation.
- `verity.pack.events`: event messages and AsyncAPI generation.
- `verity.pack.security`: security controls and security report generation.
- `verity.pack.observability`: telemetry, metrics, dashboards, and alerts.
- `verity.pack.accessibility`: accessibility claims, checks, and evidence.
- `verity.pack.compliance`: compliance mappings and compliance matrix generation.
- `verity.pack.deployment`: deployment runtimes, targets, release policies,
  rollback plans, release evidence links, and deployment report generation.
- `verity.pack.game-core`: game product, mode, loop, and prototype-scope
  records for early game product-contract coverage.
- `verity.pack.game-assets`: GDD source, visual identity, identity image, and
  concept art records for creative-source game coverage.
- `verity.pack.unity`: Unity projects, package dependencies, packages,
  shared libraries, prefabs, assembly definitions, scanners, validation
  runners, readiness dashboards, agent-context exporters, scenes, and build
  targets for Unity game implementation and engine-tooling coverage.
- `verity.pack.godot`: Godot projects, addons, shared libraries, scenes,
  node contracts, resources, scripts, autoloads, input actions, export
  presets, scanners, validation runners, readiness dashboards, and
  agent-context exporters for Godot game implementation and engine-tooling
  coverage.
- `verity.pack.unreal`: Unreal projects, plugins, modules, targets, maps,
  Blueprints, data assets, gameplay tags, input actions, scanners, validation
  runners, readiness dashboards, and agent-context exporters for Unreal game
  implementation and engine-tooling coverage.
- `verity.pack.gameplay`: game mechanics, abilities, rules, and encounters for
  gameplay implementation handoff coverage.
- `verity.pack.content`: game content items, levels, loot tables, and content
  manifests for content implementation and release-review coverage.
- `verity.pack.economy`: currencies, sources, sinks, rewards, and offers for
  economy implementation and release-review coverage.
- `verity.pack.progression`: XP models, levels, unlocks, tracks, and gates for
  game progression implementation and readiness coverage.
- `verity.pack.product-delivery`: product scope, commercial posture,
  project-management model, decision, readiness profile, evidence requirement,
  release process, operations, support, maintenance, archive, decommission,
  scanner, generator, validation-runner, editor-surface, and agent-context
  exporter records for spec-driven product-delivery repositories.
- `verity.pack.mobile`: mobile app release, store listing, privacy policy,
  Apple privacy details, Google Play Data Safety, ATT consent, SDK inventory,
  monetization posture, entitlements, soft launches, launch candidates, and
  compatibility matrix records for mobile lifecycle coverage.
- `verity.pack.liveops`: live operations config, remote config, rollback,
  analytics taxonomy, support category, save migration, decommission, data
  deletion, and archive handling records for release, maintenance, and
  retirement coverage.
- `verity.pack.evidence`: test, CI, build, review, screenshot, video, QA,
  playtest, certification-checklist, and artifact evidence records plus an
  evidence report for implementation and release proof.

## Manifest

Each built-in pack has a `pack.json` manifest:

```json
{
  "id": "verity.pack.api",
  "version": "0.1.0",
  "name": "VeritySpec API Pack",
  "description": "API endpoint records and OpenAPI generation support.",
  "schemas": [
    {
      "kind": "api.endpoint",
      "path": "schemas/api-endpoint.schema.json"
    }
  ],
  "readinessGates": [],
  "referenceRules": [],
  "generators": [
    {
      "id": "openapi",
      "name": "OpenAPI",
      "description": "Emit an OpenAPI document from API endpoint and schema records.",
      "artifactType": "api-description",
      "outputFormats": ["json"],
      "recordKinds": ["api.endpoint"]
    }
  ]
}
```

The manifest contract is defined by
`src/verityspec/schemas/pack-manifest.schema.json`.

Generator declarations may use the legacy string form, such as
`"schema-bundle"`, or the structured metadata form shown above. `verity pack
list --format json` always emits both the normalized `generators` ID list and
`generatorMetadata` for machine clients.

## Pack Standard

Every pack should include:

- A valid `pack.json` manifest.
- At least one strict JSON Schema for a record kind.
- Schemas that require the shared record envelope: `id`, `kind`, `name`,
  `status`, and `owner`.
- Readiness gates for release-relevant records.
- Conditional readiness rules for pack-specific release policy where needed.
- Reference rules for relationships introduced by the pack.
- At least one useful generator or report when applicable.
- Tests and executable examples for expected behavior.

## Commands

```bash
verity pack list
verity pack list --format json
verity pack validate
verity pack validate verity.pack.api --format json
verity pack init verity.pack.features --out build/packs/features --kind feature.flag --force
```

`verity pack init` creates a local starter pack with:

- `pack.json`
- `schemas/<kind>.schema.json`
- one strict starter record schema
- one readiness gate for the starter kind
- one `product` to starter-kind reference rule using the `uses`
  relationship
- `schema-bundle` generator metadata

The built-in core pack also advertises `coverage-dashboard`,
`product-impact`, and `pack-capability-index` generator metadata because those
reports summarize cross-pack product-contract and pack-registry state while
remaining available to every workspace. `coverage-dashboard` advertises both
JSON and Markdown output: JSON is the machine-readable contract for CI and
downstream tooling, while Markdown is a derived internal release-review
artifact for maintainers.

The generated pack can be validated immediately:

```bash
verity pack validate verity.pack.features --path build/packs/features
```

It can also be loaded by a workspace immediately through `packPaths`. A sample
workspace should include the generated pack ID in `packs`, point `packPaths` at
the generated pack directory, and connect a `product` record to the generated
record kind with a `uses` reference.

The executable documentation fixture at
[`docs/fixtures/pack-scaffold`](fixtures/pack-scaffold/README.md) shows that
complete layout. It includes a generated `verity.pack.features` pack under
`packs/features` and a consuming workspace under `workspace`.

## External Packs

Workspaces can load local packs with `packPaths`:

```json
{
  "packs": ["verity.core", "verity.pack.features"],
  "packPaths": ["../custom_pack"]
}
```

`packPaths` entries may point to a pack directory or directly to `pack.json`.
Relative paths in workspace config resolve from the workspace root.

CLI flags can also provide local packs. CLI paths resolve from the current
working directory:

```bash
verity validate ./workspace --pack-path ./packs/features
verity readiness ./workspace --strict --pack-path ./packs/features
verity generate schema-bundle ./workspace --pack-path ./packs/features --out build/schema-bundle.json
verity generate pack-capability-index ./workspace --pack-path ./packs/features --out build/pack-capability-index.json
verity pack list --path ./packs/features
verity pack validate verity.pack.features --path ./packs/features
verity validate docs/fixtures/pack-scaffold/workspace
verity lint docs/fixtures/pack-scaffold/workspace --strict
verity readiness docs/fixtures/pack-scaffold/workspace --strict
```

External packs use the same manifest schema, strict JSON Schema checks, shared
record envelope requirements, readiness gate checks, reference rule checks, and
registry collision checks as built-in packs. External pack IDs cannot shadow
built-in pack IDs.

## Installed Packs

VeritySpec can also discover separately installed pack packages through the
Python package entry-point group `verityspec.packs`. This is the foundation for
future official extension pack packages.

An installed pack package should expose one entry point per pack ID:

```toml
[project.entry-points."verityspec.packs"]
"verity.pack.features" = "verity_pack_features:pack_path"
```

The loaded object may be a path-like value or a callable that returns a path to
a pack directory or `pack.json` file:

```python
from pathlib import Path


def pack_path() -> Path:
    return Path(__file__).resolve().parent / "pack"
```

The entry-point name must match the `id` field inside the pack manifest. For
example, the entry point named `verity.pack.features` must resolve to a
manifest with `"id": "verity.pack.features"`.

Installed packs participate in the same manifest validation, schema checks,
readiness-gate checks, reference-rule checks, workspace validation, and
generator metadata summaries as built-in and local external packs:

```bash
verity pack list
verity pack list --format json
verity pack validate verity.pack.features
verity validate ./workspace
```

Source precedence is intentionally conservative:

- Built-in pack IDs are reserved and cannot be shadowed by installed packs.
- Explicit local `packPaths`, `--pack-path`, and `verity pack --path` entries
  take precedence over an installed pack with the same ID.
- Installed packs are loaded by ID when a workspace lists the pack in `packs`
  and no explicit local path supplies that ID.

`verity pack list --format json` includes a `source` field so tools can
distinguish `built-in`, `installed`, and `external` packs.

## Long-Term Pack Distribution Goal

VeritySpec's product direction is a small core runtime plus official extension
pack packages. The main `verityspec` package should remain responsible for the
contract engine: CLI commands, workspace loading, schema validation, semantic
validation, readiness checks, graphing, diffing, migrations, generator
dispatch, pack validation, and pack discovery.

Broad product-contract packs may stay bundled while their behavior is still
stabilizing. Specialized domain packs should eventually be eligible to move
into separately installable official packages once VeritySpec has stable
installed-pack discovery, compatibility metadata, migration guidance, and
fixtures proving separated packs behave the same as bundled packs. The staged
guardrails for that work are defined in
[Specialized pack separation plan](specialized-pack-separation.md).

The likely separation boundary is:

- Core or broadly useful packs remain close to `verityspec`: `verity.core`,
  `verity.pack.api`, `verity.pack.cli`, `verity.pack.events`,
  `verity.pack.security`, `verity.pack.observability`,
  `verity.pack.accessibility`, `verity.pack.compliance`,
  `verity.pack.deployment`, `verity.pack.product-delivery`, and
  `verity.pack.evidence`.
- Specialized extension-pack candidates include game, mobile, liveops, and
  engine packs: `verity.pack.game-core`, `verity.pack.game-assets`,
  `verity.pack.gameplay`, `verity.pack.content`, `verity.pack.economy`,
  `verity.pack.progression`, `verity.pack.mobile`, `verity.pack.liveops`,
  `verity.pack.unity`, `verity.pack.godot`, and `verity.pack.unreal`.

This is not an immediate removal plan. Existing bundled packs should remain
available until installed official extension packs can be discovered without
manual `packPaths`, validated with the same pack contract, versioned with
compatibility metadata, and migrated without breaking existing workspaces.

## Contributing Packs and Schema Changes

Public pack and schema proposals should start from
[Contributing](../CONTRIBUTING.md).

Use the `Pack proposal` issue template for new packs or major pack expansions.
Use the `Schema change` issue template for new fields, required-field changes,
enum changes, reference-shape changes, deprecations, removals, and breaking
schema behavior.

Maintainers should review public external pack proposals with the
[External pack maintainer review checklist](external-pack-review-checklist.md).

Pack proposals should define the product surface, record kinds, reference
rules, readiness gates, generator or report output, executable examples, tests,
and compatibility boundaries before implementation begins.

Schema changes should explain whether the change is additive, behavioral,
deprecated, or breaking, and should include before-and-after records, migration
impact, affected generators or readiness gates, and validation fixtures.

## Product Surface Pack Boundaries

Future GUI, desktop, engine, and additional game packs should follow the
boundary guidance in
[Product surface pack boundaries](product-surface-pack-boundaries.md) and
[Engine and product-delivery pack direction](engine-product-delivery-packs.md)
before their first schemas are added. Specialized pack extraction should also
follow the staged gates in
[Specialized pack separation plan](specialized-pack-separation.md). The first
narrow game, engine, product-delivery, mobile, and liveops scopes now live in
[`verity.pack.game-core`](game-core-pack.md) and
[`verity.pack.game-assets`](game-assets-pack.md), with Unity game
implementation and engine-tooling coverage in
[`verity.pack.unity`](unity-pack.md), Godot game implementation and
engine-tooling coverage in [`verity.pack.godot`](godot-pack.md), Unreal game
implementation and engine-tooling coverage in
[`verity.pack.unreal`](unreal-pack.md), gameplay coverage in
[`verity.pack.gameplay`](gameplay-pack.md), content coverage in
[`verity.pack.content`](content-pack.md), economy coverage in
[`verity.pack.economy`](economy-pack.md), progression coverage in
[`verity.pack.progression`](progression-pack.md), product-delivery coverage in
[`verity.pack.product-delivery`](product-delivery-pack.md), mobile lifecycle
coverage in [`verity.pack.mobile`](mobile-pack.md), liveops coverage in
[`verity.pack.liveops`](liveops-pack.md), and evidence coverage in
[`verity.pack.evidence`](evidence-pack.md).

That guidance keeps product-surface packs focused on their own domains and
prevents them from duplicating cross-cutting concerns owned by security,
accessibility, observability, compliance, release, evidence, deployment,
dependency, or portfolio packs.

Workspace dependencies are not packs. A pack defines vocabulary and behavior;
a workspace contains actual product, service, game, library, or platform
records. Future dependency behavior should follow the boundary guidance in
[Cross-workspace dependencies](cross-workspace-dependencies.md) before adding
manifest fields, lockfiles, or dependency-aware graph behavior.
