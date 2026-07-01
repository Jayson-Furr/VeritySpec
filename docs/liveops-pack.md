# LiveOps Pack

`verity.pack.liveops` adds built-in vocabulary for live operations
configuration, remote config, rollback plans, analytics taxonomy, support
categories, save migration policy, decommissioning, data deletion posture, and
archive handling.

The pack is engine-neutral. Unity, Godot, and Unreal projects can all link to a
liveops config with the same `usesLiveOpsConfig` relationship when the product
uses live operations or remote configuration. Engine-specific liveops additions
should keep that parity or document why an equivalent does not apply.

This pack does not assert legal, privacy-law, platform-certification,
marketplace, app-store, live-service, support, or archival readiness. Those
claims require downstream review, policy, and evidence outside this built-in
vocabulary.

## Record Kinds

The pack contributes these record kinds:

- `liveops.config`
- `liveops.remote-config`
- `liveops.rollback-plan`
- `liveops.analytics-taxonomy`
- `liveops.support-category`
- `liveops.save-migration-policy`
- `liveops.decommission-plan`
- `liveops.data-deletion-policy`
- `liveops.archive-handling`

## Readiness

LiveOps readiness gates require owners, descriptions, operations metadata, and
graph links for records that affect release, maintenance, support, or
retirement review.

Examples:

- `liveops.config` records should link to remote config, rollback, analytics,
  support, save-migration, decommission, data-deletion, and archive records.
- `liveops.remote-config` records should define key prefixes, bounds policy,
  deployment policy, and rollback links.
- `liveops.analytics-taxonomy` records should list tracked event names and KPI
  references.
- `liveops.decommission-plan` records should link to data-deletion and archive
  handling records.
- `liveops.save-migration-policy` records should define schema version,
  migration posture, and rollback posture.

Run the executable example:

```bash
verity validate examples/liveops
verity lint examples/liveops --strict
verity readiness examples/liveops --strict
verity graph examples/liveops
verity generate schema-bundle examples/liveops --out build/liveops-schema-bundle.json
```

When liveops records are combined with product-delivery and mobile records,
generate a lifecycle readiness gap report:

```bash
verity generate lifecycle-readiness-report examples/lifecycle-readiness --out build/lifecycle-readiness-report.json
```

The report summarizes remote-config, rollback, support, save-migration,
decommission, data-deletion, and archive-review coverage without asserting
live-service, support, legal, privacy-law, marketplace, app-store,
platform-certification, or archival readiness.

## Reference Rules

The pack defines reference rules for:

- `product`, `game.product`, and `product.scope` to `liveops.config` with
  `hasLiveOpsConfig`
- `unity.project`, `godot.project`, and `unreal.project` to `liveops.config`
  with `usesLiveOpsConfig`
- `mobile.app-release` to `liveops.config` with `usesLiveOpsConfig`
- `liveops.config` to remote config, rollback plan, analytics taxonomy,
  support category, save migration policy, decommission plan, data deletion
  policy, and archive handling records
- `liveops.remote-config` to rollback plan records
- `liveops.decommission-plan` to data deletion and archive handling records

These rules let `verity validate` reject unknown or mismatched liveops edges
instead of treating operational lifecycle records as isolated JSON documents.

## Example

The executable example at
[`examples/liveops`](../examples/liveops/verityspec.json) models a mobile game
liveops slice with remote config bounds, rollback, analytics taxonomy, support
category, save migration policy, decommission planning, data deletion posture,
and archive handling.

The example is included in the workspace compatibility matrix and CI contract.
