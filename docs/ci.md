# CI

Recommended minimal CI:

```bash
verity pack validate
verity validate examples/basic
verity lint examples/basic --strict
verity readiness examples/basic --strict
verity doctor examples/basic --fail-on warning
verity generate validation-report examples/basic --out build/validation-report.json
```

For repositories with multiple workspaces, run the contract checks for each
workspace and generate the artifacts that matter for that product surface.

Broken examples can be checked by expecting a non-zero validation exit:

```bash
set +e
verity validate examples/broken --format json > build/broken-validation.json
exit_status=$?
set -e
test "$exit_status" -eq 1
```
