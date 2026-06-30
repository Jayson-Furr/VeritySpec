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
verity generate typescript tests/fixtures/generator_maturity --out build/generator-maturity.ts
verity generate python-models tests/fixtures/generator_maturity --out build/generator-maturity.py
```

Most generators run validation first and fail if the product contract has
errors. `validation-report` is special: it always writes the report, then exits
with the validation result.

Validation reports include:

- Generation timestamp
- VeritySpec CLI version
- Workspace path
- Loaded pack versions
- Known record kinds
- Issue summary and full issue list

## Current Guarantees

OpenAPI output includes:

- Product title, version, and description in `info`
- Component schemas from `schema.object` records
- Request and response schema references where records declare them
- Inferred path parameters from templated paths such as `/users/{userId}`
- Explicit endpoint parameters for path, query, header, and cookie locations
- Operation tags, VeritySpec IDs, owners, statuses, and deprecation metadata

AsyncAPI output includes:

- Product title, version, and description in `info`
- Component schemas and message components
- Message IDs, channel subscriptions, payload references, and VeritySpec metadata

TypeScript and Python model generators support:

- `$ref` values that point at `#/components/schemas/...`
- Arrays
- String, number, integer, boolean, and object types
- String and scalar enums
- Nullable fields
- Optional fields
- Inline nested object shapes for TypeScript
- Field descriptions in generated comments

OpenAPI, TypeScript, and Python output for `tests/fixtures/generator_maturity`
is covered by golden-file tests. Changes to those generators should update the
golden files only when the output contract intentionally changes.

Known limits:

- Python nested object fields currently emit `dict[str, Any]`.
- Generators do not yet emit client/server stubs.
