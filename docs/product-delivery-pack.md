# Product Delivery Pack

`verity.pack.product-delivery` adds built-in vocabulary for repositories that
use VeritySpec as their product-contract source of truth while GitHub or another
tracker manages workflow execution.

The pack is intended for spec-driven product repositories, engine-tooling
repositories, and game repositories that need records for scope, posture,
project management, decisions, readiness, evidence, release process,
operations, support, maintenance, archive, decommissioning, scanners,
generators, validation runners, editor surfaces, and agent-context export.

It does not assert commercial, legal, privacy-law, marketplace, platform
certification, or app-store readiness. Those claims require downstream policy,
review, and evidence outside this built-in vocabulary.

## Record Kinds

The pack contributes these record kinds:

- `product.scope`
- `commercial.posture`
- `project-management.model`
- `decision.record`
- `readiness.profile`
- `evidence.requirement`
- `release.process`
- `operations.model`
- `support.policy`
- `maintenance.policy`
- `archive.policy`
- `decommission.policy`
- `scanner.capability`
- `generator.capability`
- `validation.runner`
- `editor.surface`
- `agent-context.exporter`

## Source-Of-Truth Model

The intended model is:

```text
GitHub manages workflow.
VeritySpec manages truth.
```

Typical workflow mappings:

- GitHub Issues track work, questions, defects, readiness gaps, and evidence
  requests.
- GitHub Projects provide planning boards, roadmap views, portfolio views, and
  execution dashboards.
- GitHub Milestones bound sprint, release, candidate, maintenance, or archive
  work.
- GitHub Actions enforce product-contract checks.
- Pull requests review implementation and spec changes.
- VeritySpec records define the product-contract truth that those workflow
  objects point back to.

## Readiness

Product-delivery readiness gates require ownership, descriptions, release or
operations metadata, and graph links for records that affect implementation or
release review.

Examples:

- `product.scope` records should link to posture, project-management,
  readiness, release, operations, support, maintenance, archive, and
  decommission records.
- `project-management.model` records should link to a `decision.record`.
- `readiness.profile` records should link to `evidence.requirement` records.
- `release.process` records should link to readiness and evidence records.
- `validation.runner` records should declare `scannerRefs` and graph links to
  `scanner.capability` records.
- `editor.surface` and `agent-context.exporter` records should link to the
  validation, scope, readiness, and generator records they expose or describe.

Run the executable example:

```bash
verity validate examples/product-delivery
verity lint examples/product-delivery --strict
verity readiness examples/product-delivery --strict
verity graph examples/product-delivery
verity generate schema-bundle examples/product-delivery --out build/product-delivery-schema-bundle.json
```

When product-delivery records are combined with mobile and liveops records,
generate a lifecycle readiness gap report:

```bash
verity generate lifecycle-readiness-report examples/lifecycle-readiness --out build/lifecycle-readiness-report.json
```

The report summarizes record coverage and gaps only. It does not make
commercial, legal, privacy-law, marketplace, app-store, platform-certification,
support, or archival readiness claims.

## Reference Rules

The pack defines reference rules for:

- `product` to `product.scope` with `hasProductScope`
- `product.scope` to posture, project-management, readiness, release,
  operations, support, maintenance, archive, and decommission records
- `project-management.model` to `decision.record`
- `readiness.profile` and `release.process` to evidence requirements
- `maintenance.policy` and `decommission.policy` to archive policy
- scanner, generator, validation-runner, editor-surface, and agent-context
  records to the product-delivery records they scan, run, expose, or describe

These rules let `verity validate` reject unknown or mismatched graph edges
instead of treating product-delivery records as isolated JSON documents.

## Example

The executable example at
[`examples/product-delivery`](../examples/product-delivery/verityspec.json)
models a spec-driven engine-tooling repository. It demonstrates:

- a product root linked to `product.scope`
- proprietary private-alpha posture without external readiness claims
- GitHub-native workflow mapped back to VeritySpec truth records
- readiness and evidence requirements
- release, operations, support, maintenance, archive, and decommission policy
- scanner, generator, validation-runner, editor-surface, and agent-context
  exporter capability records

The example is included in the workspace compatibility matrix and CI contract.
