# CI

Recommended minimal CI:

```bash
verity pack validate
verity validate examples/basic
verity lint examples/basic --strict
verity readiness examples/basic --strict
verity doctor examples/basic --fail-on warning
verity doctor examples/basic --report-out build/doctor-report.json
verity diff examples/basic examples/basic --format json > build/diff.json
verity migrate examples/basic --dry-run --format json > build/migration.json
verity generate validation-report examples/basic --out build/validation-report.json
verity generate coverage-dashboard tests/fixtures/cross_pack_coverage --out build/coverage-dashboard.json
```

For repositories with multiple workspaces, run the contract checks for each
workspace and generate the artifacts that matter for that product surface.

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

In GitHub Actions, pass `--github-annotations` to `verity validate`, `verity
lint`, or `verity readiness` to emit workflow annotations for product-contract
issues while preserving normal text or JSON stdout.

For workspaces that load `verity.pack.security`, include the security report:

```bash
verity validate examples/security
verity lint examples/security --strict
verity readiness examples/security --strict
verity generate security-report examples/security --out build/security-report.json
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
checks and keep a deployment report for release and operations review:

```bash
verity validate examples/deployment
verity lint examples/deployment --strict
verity readiness examples/deployment --strict
verity generate deployment-report examples/deployment --out build/deployment-report.json
verity generate schema-bundle examples/deployment --out build/deployment-schema-bundle.json
```

For release-review workspaces that combine multiple product-surface packs,
generate a cross-pack coverage dashboard:

```bash
verity validate tests/fixtures/cross_pack_coverage
verity lint tests/fixtures/cross_pack_coverage --strict
verity readiness tests/fixtures/cross_pack_coverage --strict
verity generate coverage-dashboard tests/fixtures/cross_pack_coverage --out build/coverage-dashboard.json
```

For workspaces with local external packs:

```bash
verity pack validate verity.pack.features --path tests/fixtures/custom_pack
verity validate tests/fixtures/custom_pack_workspace
verity lint tests/fixtures/custom_pack_workspace --strict
verity readiness tests/fixtures/custom_pack_workspace --strict
verity generate schema-bundle tests/fixtures/custom_pack_workspace --out build/custom-schema-bundle.json
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
