# Generators

Generators turn a valid workspace into implementation or documentation
artifacts.

```bash
verity generate openapi examples/api-service --out build/openapi.json
verity generate asyncapi examples/events --out build/asyncapi.json
verity generate cli-reference examples/cli-tool --out build/cli-reference.md
verity generate typescript examples/basic --out build/types.ts
verity generate python-models examples/basic --out build/models.py
verity generate schema-bundle examples/basic --out build/schema-bundle.json
verity generate validation-report examples/basic --out build/validation-report.json
```

Most generators run validation first and fail if the product contract has
errors. `validation-report` is special: it always writes the report, then exits
with the validation result.

