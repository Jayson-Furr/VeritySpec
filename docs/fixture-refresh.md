# Fixture Refresh Guide

Use this guide when generator behavior, example records, package-version
metadata, or release evidence intentionally changes committed fixtures.

The goal is to make fixture refreshes reviewable. Golden fixtures are not bulk
rewritten as a cleanup task; they change only when the output contract changes
or a release-version fixture must be updated.

## Scope

This guide covers:

- golden fixtures under `tests/golden`
- generator maturity fixtures under `tests/fixtures/generator_maturity`
- release-version fixture updates in `examples/evidence` and
  `tests/fixtures/cross_pack_coverage`
- deterministic timestamps for generated JSON report review
- intentional output drift review before committing fixture changes

No automatic fixture rewrite command is provided by this guide. Until one
exists, maintainers should regenerate outputs into `build/`, inspect the diff,
and then update only the committed fixture files that the tests prove are
stale.

## Timestamp Discipline

JSON report generators support `--generated-at` for deterministic timestamps.
Use the same timestamp as the golden tests unless the test fixture itself is
being intentionally changed:

```bash
GENERATED_AT=2026-01-02T03:04:05Z
```

The committed report fixtures normalize dynamic metadata such as
`generatedAt`, `verityVersion`, and absolute workspace paths to placeholders
where needed. Keep those placeholders when refreshing golden fixtures.

## Current Golden Fixtures

| Fixture | Regeneration command |
|---|---|
| `tests/golden/security_report/security_report.json` | `verity generate security-report examples/security --generated-at "$GENERATED_AT" --out build/security-report.json` |
| `tests/golden/security_report/security_report.md` | `verity generate security-report examples/security --format markdown --generated-at "$GENERATED_AT" --out build/security-report.md` |
| `tests/golden/observability/observability_report.json` | `verity generate observability-report examples/observability --generated-at "$GENERATED_AT" --out build/observability-report.json` |
| `tests/golden/observability/schema_bundle.json` | `verity generate schema-bundle examples/observability --out build/observability-schema-bundle.json` |
| `tests/golden/accessibility_report/accessibility_report.json` | `verity generate accessibility-report examples/accessibility --generated-at "$GENERATED_AT" --out build/accessibility-report.json` |
| `tests/golden/compliance_matrix/compliance_matrix.json` | `verity generate compliance-matrix examples/compliance --generated-at "$GENERATED_AT" --out build/compliance-matrix.json` |
| `tests/golden/deployment/deployment_report.json` | `verity generate deployment-report examples/deployment --generated-at "$GENERATED_AT" --out build/deployment-report.json` |
| `tests/golden/evidence_report/evidence_report.json` | `verity generate evidence-report examples/evidence --generated-at "$GENERATED_AT" --out build/evidence-report.json` |
| `tests/golden/lifecycle_readiness/lifecycle_readiness_report.json` | `verity generate lifecycle-readiness-report examples/lifecycle-readiness --generated-at "$GENERATED_AT" --out build/lifecycle-readiness-report.json` |
| `tests/golden/coverage_dashboard/coverage_dashboard.json` | `verity generate coverage-dashboard tests/fixtures/cross_pack_coverage --generated-at "$GENERATED_AT" --out build/coverage-dashboard.json` |
| `tests/golden/coverage_dashboard/coverage_dashboard.md` | `verity generate coverage-dashboard tests/fixtures/cross_pack_coverage --format markdown --generated-at "$GENERATED_AT" --out build/coverage-dashboard.md` |
| `tests/golden/pack_capability_index/pack_capability_index.json` | `verity generate pack-capability-index tests/fixtures/custom_pack_workspace --generated-at "$GENERATED_AT" --out build/pack-capability-index.json` |
| `tests/golden/product_impact/product_impact.json` | `verity generate product-impact tests/fixtures/product_impact/baseline tests/fixtures/product_impact/current --generated-at "$GENERATED_AT" --out build/product-impact.json` |
| `tests/golden/issue_code_catalog/issue_code_catalog.json` | `verity generate issue-code-catalog --generated-at "$GENERATED_AT" --out build/issue-code-catalog.json` |
| `tests/golden/generator_maturity/openapi.json` | `verity generate openapi tests/fixtures/generator_maturity --out build/generator-maturity-openapi.json` |
| `tests/golden/generator_maturity/typescript.ts` | `verity generate typescript tests/fixtures/generator_maturity --out build/generator-maturity.ts` |
| `tests/golden/generator_maturity/python_models.py` | `verity generate python-models tests/fixtures/generator_maturity --out build/generator-maturity.py` |

Use `python -m json.tool` on generated JSON outputs before reviewing them:

```bash
python -m json.tool build/security-report.json >/dev/null
python -m json.tool build/lifecycle-readiness-report.json >/dev/null
python -m json.tool build/coverage-dashboard.json >/dev/null
python -m json.tool build/issue-code-catalog.json >/dev/null
```

Markdown golden fixtures preserve normalized placeholder values for dynamic
fields such as `<generatedAt>`, `<verityVersion>`, and `<workspacePath>` when
tests compare committed output.

## Review Procedure

1. Run the generator into `build/` with `--generated-at` when the generator
   accepts it.
2. Validate JSON output with `python -m json.tool` where applicable.
3. Run the focused golden tests before editing committed fixtures.
4. Compare the generated output to the committed fixture and identify the
   intentional output drift.
5. Preserve placeholder values for dynamic fields such as `<generatedAt>`,
   `<verityVersion>`, and `<workspacePath>`.
6. Update only the fixture files that correspond to the intended behavior
   change.
7. Re-run the focused tests and the standard local checks before committing.

Useful focused tests:

```bash
PYTHONPATH=src:. python3 -m pytest tests/test_verityspec.py -k golden -q
PYTHONPATH=src:. python3 -m pytest tests/test_cli.py -k golden -q
PYTHONPATH=src:. python3 -m pytest tests/test_release_integrity.py -q
```

## Release-Version Fixture Updates

Release prep changes package-version fixtures even when generator behavior is
unchanged. During a release branch, update and verify:

- `examples/evidence/records/records.json`
- `tests/golden/evidence_report/evidence_report.json`
- `tests/fixtures/cross_pack_coverage/records/all.json`
- README release badge, latest-release text, install tag, package-version
  text, and release-notes link
- downstream CI pins and workflow release pins
- `docs/release-checklist.md`
- `docs/release-notes-vX.Y.Z.md`

`tests/test_release_integrity.py` is the release-version fixture authority.
If it fails, update the release surface it names instead of weakening the test.

## Maintainer Checklist

For every fixture refresh PR:

- Name the generator, example, or release-version reason for the fixture
  change.
- State whether the output drift is behavioral, structural, metadata-only, or
  release-version-only.
- Include the focused golden tests and standard local checks in the PR body.
- Note any generated outputs reviewed from `build/`.
- Avoid broad fixture churn outside the changed generator or release version.
- If this process becomes useful outside VeritySpec, propose a follow-up organization-patterns write-back.
