# CI

Recommended minimal CI:

```bash
verity pack validate
verity pack doctor --format json > build/pack-doctor.json
verity pack compare verity.pack.unity --mirror tests/fixtures/official_extension_mirrors/verityspec-pack-unity/pack --format json > build/unity-pack-mirror.json
verity validate examples/basic
verity lint examples/basic --strict
verity readiness examples/basic --strict
verity doctor examples/basic --fail-on warning
verity doctor examples/basic --report-out build/doctor-report.json
verity diff examples/basic examples/basic --format json > build/diff.json
verity migrate examples/basic --dry-run --format json > build/migration.json
verity generate validation-report examples/basic --out build/validation-report.json
verity generate lifecycle-readiness-report examples/lifecycle-readiness --out build/lifecycle-readiness-report.json
verity generate coverage-dashboard tests/fixtures/cross_pack_coverage --out build/coverage-dashboard.json
verity generate coverage-dashboard tests/fixtures/cross_pack_coverage --format markdown --out build/coverage-dashboard.md
verity generate pack-capability-index tests/fixtures/custom_pack_workspace --out build/pack-capability-index.json
verity generate product-impact tests/fixtures/product_impact/baseline tests/fixtures/product_impact/current --out build/product-impact.json
```

The migration report written to `build/migration.json` follows the
[Migration Report JSON Schema](migration-report-schema.md). Downstream CI can
validate it against
[`docs/schemas/migration-report.schema.json`](schemas/migration-report.schema.json)
before inspecting `blocked`, `impactSummary`, `changes`, `filesWritten`, or
`manualFollowUp`.

For repositories with multiple workspaces, run the contract checks for each
workspace and generate the artifacts that matter for that product surface.
Downstream GitHub Actions users can copy
`templates/github-actions/product-contract-monorepo.yml` to run the reusable
product-contract workflow once per workspace while sharing local pack paths.

Use product-contract profiles when a workspace has a known enforcement posture:

```bash
verity validate examples/basic --profile release
verity lint examples/basic --profile strict
verity readiness examples/basic --profile release
verity doctor examples/basic --profile public-api --format json
```

VeritySpec's own CI also executes safe local command examples from `README.md`.
Install and environment-setup snippets remain documentation-only, while local
`verity` examples are smoke-tested with temporary `build/` output paths so
public command snippets do not drift from the CLI.

After a public release tag is pushed, use the
[post-tag release verification](post-tag-release-verification.md) checklist to
record release workflow success, GitHub release asset hashes, skipped PyPI
publish evidence, downloaded wheel smoke checks, public GitHub tag install
smoke checks, and milestone closure evidence.

In GitHub Actions, pass `--github-annotations` to `verity validate`, `verity
lint`, or `verity readiness` to emit workflow annotations for product-contract
issues while preserving normal text or JSON stdout.

For workspaces that load `verity.pack.security`, include the security report:

```bash
verity validate examples/security
verity lint examples/security --strict
verity readiness examples/security --strict
verity generate security-report examples/security --out build/security-report.json
verity generate security-report examples/security --format markdown --out build/security-report.md
```

For workspaces that load `verity.pack.observability`, include the usual
contract checks and keep a schema bundle for downstream tooling:

```bash
verity validate examples/observability
verity lint examples/observability --strict
verity readiness examples/observability --strict
verity generate observability-report examples/observability --out build/observability-report.json
verity generate schema-bundle examples/observability --out build/observability-schema-bundle.json
```

For workspaces that load `verity.pack.accessibility`, include the usual
contract checks and keep a schema bundle for downstream tooling:

```bash
verity validate examples/accessibility
verity lint examples/accessibility --strict
verity readiness examples/accessibility --strict
verity generate accessibility-report examples/accessibility --out build/accessibility-report.json
verity generate schema-bundle examples/accessibility --out build/accessibility-schema-bundle.json
```

For workspaces that load `verity.pack.compliance`, include the usual contract
checks and keep a schema bundle for downstream tooling:

```bash
verity validate examples/compliance
verity lint examples/compliance --strict
verity readiness examples/compliance --strict
verity generate compliance-matrix examples/compliance --out build/compliance-matrix.json
verity generate schema-bundle examples/compliance --out build/compliance-schema-bundle.json
```

For workspaces that load `verity.pack.deployment`, include the usual contract
checks and keep a deployment report with linked release evidence for release
and operations review:

```bash
verity validate examples/deployment
verity lint examples/deployment --strict
verity readiness examples/deployment --strict
verity generate deployment-report examples/deployment --out build/deployment-report.json
verity generate deployment-report examples/deployment --format markdown --out build/deployment-report.md
verity generate schema-bundle examples/deployment --out build/deployment-schema-bundle.json
```

For workspaces that load `verity.pack.game-core`, include the usual contract
checks and keep a schema bundle for game design, prototype, and agent handoff
tooling:

```bash
verity validate examples/game-core
verity lint examples/game-core --strict
verity readiness examples/game-core --strict
verity generate schema-bundle examples/game-core --out build/game-core-schema-bundle.json
```

For workspaces that load `verity.pack.game-assets`, include the usual contract
checks and keep a schema bundle for creative-source, identity, concept-art, and
agent handoff tooling:

```bash
verity validate examples/game-assets
verity lint examples/game-assets --strict
verity readiness examples/game-assets --strict
verity generate schema-bundle examples/game-assets --out build/game-assets-schema-bundle.json
```

For workspaces that load `verity.pack.unity`, include the usual contract
checks, graph checks, and a schema bundle for Unity project, package,
shared-library, prefab, assembly, scanner, validation-runner, dashboard,
scene, build, and agent handoff tooling:

```bash
verity validate examples/unity
verity lint examples/unity --strict
verity readiness examples/unity --strict
verity graph examples/unity --format json > build/unity-graph.json
verity generate schema-bundle examples/unity --out build/unity-schema-bundle.json
```

For workspaces that load `verity.pack.godot`, include the usual contract
checks, graph checks, and a schema bundle for Godot project, addon,
shared-library, scene, node, resource, script, autoload, input, export,
scanner, validation-runner, dashboard, and agent handoff tooling:

```bash
verity validate examples/godot
verity lint examples/godot --strict
verity readiness examples/godot --strict
verity graph examples/godot --format json > build/godot-graph.json
verity generate schema-bundle examples/godot --out build/godot-schema-bundle.json
```

For workspaces that load `verity.pack.unreal`, include the usual contract
checks, graph checks, and a schema bundle for Unreal project, plugin, module,
target, map, Blueprint, data-asset, gameplay-tag, input-action, scanner,
validation-runner, dashboard, and agent handoff tooling:

```bash
verity validate examples/unreal
verity lint examples/unreal --strict
verity readiness examples/unreal --strict
verity graph examples/unreal --format json > build/unreal-graph.json
verity generate schema-bundle examples/unreal --out build/unreal-schema-bundle.json
```

For workspaces that load `verity.pack.gameplay`, include the usual contract
checks and keep a schema bundle for mechanic, ability, rule, encounter, and
agent handoff tooling:

```bash
verity validate examples/gameplay
verity lint examples/gameplay --strict
verity readiness examples/gameplay --strict
verity generate schema-bundle examples/gameplay --out build/gameplay-schema-bundle.json
```

For workspaces that load `verity.pack.content`, include the usual contract
checks and keep a schema bundle for content item, level, loot-table, manifest,
and agent handoff tooling:

```bash
verity validate examples/content
verity lint examples/content --strict
verity readiness examples/content --strict
verity generate schema-bundle examples/content --out build/content-schema-bundle.json
```

For workspaces that load `verity.pack.economy`, include the usual contract
checks and keep a schema bundle for currency, source, sink, reward, offer, and
agent handoff tooling:

```bash
verity validate examples/economy
verity lint examples/economy --strict
verity readiness examples/economy --strict
verity generate schema-bundle examples/economy --out build/economy-schema-bundle.json
```

For workspaces that load `verity.pack.product-delivery`, include the usual
contract checks, graph checks, and a schema bundle for product scope, project
management, readiness, evidence, release, operations, support, maintenance,
archive, decommission, scanner, generator, validation-runner, editor-surface,
and agent-context tooling:

```bash
verity validate examples/product-delivery
verity lint examples/product-delivery --strict
verity readiness examples/product-delivery --strict
verity graph examples/product-delivery --format json > build/product-delivery-graph.json
verity generate schema-bundle examples/product-delivery --out build/product-delivery-schema-bundle.json
```

For workspaces that load `verity.pack.mobile`, include the usual contract
checks, graph checks, and a schema bundle for app release, store listing,
privacy and data-safety posture, SDK inventory, monetization, entitlements,
soft-launch, launch-candidate, and compatibility review:

```bash
verity validate examples/mobile
verity lint examples/mobile --strict
verity readiness examples/mobile --strict
verity graph examples/mobile --format json > build/mobile-graph.json
verity generate schema-bundle examples/mobile --out build/mobile-schema-bundle.json
```

For workspaces that load `verity.pack.progression`, include the usual
contract checks, graph checks, and a schema bundle for XP models, levels,
unlocks, tracks, and gates:

```bash
verity validate examples/progression
verity lint examples/progression --strict
verity readiness examples/progression --strict
verity graph examples/progression --format json > build/progression-graph.json
verity generate schema-bundle examples/progression --out build/progression-schema-bundle.json
```

For workspaces that load `verity.pack.liveops`, include the usual contract
checks, graph checks, and a schema bundle for remote config, rollback,
analytics taxonomy, support categories, save migration, decommissioning, data
deletion, and archive handling:

```bash
verity validate examples/liveops
verity lint examples/liveops --strict
verity readiness examples/liveops --strict
verity graph examples/liveops --format json > build/liveops-graph.json
verity generate schema-bundle examples/liveops --out build/liveops-schema-bundle.json
```

For workspaces that load `verity.pack.evidence`, include the usual contract
checks, graph checks, an evidence report, and a schema bundle for test, CI,
build, review, screenshot, video, QA, playtest, certification-checklist, and
artifact evidence:

```bash
verity validate examples/evidence
verity lint examples/evidence --strict
verity readiness examples/evidence --strict
verity graph examples/evidence --format json > build/evidence-graph.json
verity generate evidence-report examples/evidence --out build/evidence-report.json
verity generate evidence-report examples/evidence --format markdown --out build/evidence-report.md
verity generate schema-bundle examples/evidence --out build/evidence-schema-bundle.json
```

For release-review workspaces that combine multiple product-surface packs,
generate a cross-pack coverage dashboard. Keep the JSON output as the
machine-readable contract for CI and downstream tooling; use the Markdown
output as a human-readable internal release-review artifact. The Markdown
report does not make legal, commercial, privacy-law, platform-certification,
marketplace, app-store, store-review, pricing-approval, or support-SLA claims.

```bash
verity validate tests/fixtures/cross_pack_coverage
verity lint tests/fixtures/cross_pack_coverage --strict
verity readiness tests/fixtures/cross_pack_coverage --strict
verity generate coverage-dashboard tests/fixtures/cross_pack_coverage --out build/coverage-dashboard.json
verity generate coverage-dashboard tests/fixtures/cross_pack_coverage --format markdown --out build/coverage-dashboard.md
```

For product-delivery, mobile, and liveops lifecycle review workspaces,
generate a lifecycle readiness gap report. The report is a VeritySpec record
coverage and gap summary; it does not make commercial, legal, privacy-law,
marketplace, app-store, platform-certification, live-service, support, or
archival readiness claims.

```bash
verity validate examples/lifecycle-readiness
verity lint examples/lifecycle-readiness --strict
verity readiness examples/lifecycle-readiness --strict
verity generate lifecycle-readiness-report examples/lifecycle-readiness --out build/lifecycle-readiness-report.json
```

For release reviews that compare two workspace snapshots, generate a
product-impact report:

```bash
verity validate tests/fixtures/product_impact/current
verity lint tests/fixtures/product_impact/current --strict
verity readiness tests/fixtures/product_impact/current --strict
verity generate product-impact tests/fixtures/product_impact/baseline tests/fixtures/product_impact/current --out build/product-impact.json
```

For workspaces with local external packs:

```bash
verity pack validate verity.pack.features --path tests/fixtures/custom_pack
verity validate tests/fixtures/custom_pack_workspace
verity lint tests/fixtures/custom_pack_workspace --strict
verity readiness tests/fixtures/custom_pack_workspace --strict
verity generate schema-bundle tests/fixtures/custom_pack_workspace --out build/custom-schema-bundle.json
verity generate pack-capability-index tests/fixtures/custom_pack_workspace --out build/pack-capability-index.json
```

For future official extension-package mirrors, compare the mirror fixture
against the bundled source pack without loading the mirror into the active
registry:

```bash
verity pack compare verity.pack.unity --mirror tests/fixtures/official_extension_mirrors/verityspec-pack-unity/pack --format json > build/unity-pack-mirror.json
```

This verifies manifest identity, schema declarations, schema JSON content,
readiness gates, reference rules, and generator metadata while preserving the
current built-in pack collision guard.

For generated pack scaffold documentation fixtures:

```bash
verity pack validate verity.pack.features --path docs/fixtures/pack-scaffold/packs/features
verity validate docs/fixtures/pack-scaffold/workspace
verity lint docs/fixtures/pack-scaffold/workspace --strict
verity readiness docs/fixtures/pack-scaffold/workspace --strict
verity generate schema-bundle docs/fixtures/pack-scaffold/workspace --out build/pack-scaffold-schema-bundle.json
verity generate pack-capability-index docs/fixtures/pack-scaffold/workspace --out build/pack-scaffold-capability-index.json
```

For migration coverage, smoke test any committed PrismSpec fixtures:

```bash
verity import prismspec tests/fixtures/prismspec_sample --out build/prismspec-import
verity validate build/prismspec-import --format json > build/prismspec-import-validation.json
```

Broken examples can be checked by expecting a non-zero validation exit:

```bash
set +e
verity validate examples/broken --format json > build/broken-validation.json
exit_status=$?
set -e
test "$exit_status" -eq 1
```
