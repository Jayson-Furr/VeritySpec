# VeritySpec v0.43.0 Release Notes

VeritySpec v0.43.0 adds the built-in product-delivery pack as the first
spec-driven repository delivery surface.

## Highlights

- Added built-in `verity.pack.product-delivery`.
- Added strict schemas for `product.scope`, `commercial.posture`,
  `project-management.model`, `decision.record`, `readiness.profile`,
  `evidence.requirement`, `release.process`, `operations.model`,
  `support.policy`, `maintenance.policy`, `archive.policy`,
  `decommission.policy`, `scanner.capability`, `generator.capability`,
  `validation.runner`, `editor.surface`, and `agent-context.exporter`.
- Added product-delivery readiness gates and reference rules that connect
  product scope, commercial posture, project-management model, decisions,
  evidence, release process, operations, support, maintenance, archive,
  decommission, scanner, generator, validation-runner, editor-surface, and
  agent-context exporter records.
- Added executable `examples/product-delivery` coverage for a spec-driven
  product repository that follows the model: GitHub manages workflow;
  VeritySpec manages truth.
- Added product-delivery graph checks, schema-bundle checks,
  coverage-dashboard support, compatibility manifest coverage, CI checks,
  docs, release-checklist coverage, and AI-agent commands.
- Kept product-delivery claims scoped to product-contract vocabulary. This
  release does not assert legal, privacy-law, marketplace, app-store,
  platform-certification, or commercial-readiness guarantees.

## Compatibility

- Package version: `0.43.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.
- No workspace format migration is required.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.43.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
