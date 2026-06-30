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
verity generate security-report examples/security --out build/security-report.json
verity generate observability-report examples/observability --out build/observability-report.json
verity generate accessibility-report examples/accessibility --out build/accessibility-report.json
verity generate schema-bundle examples/accessibility --out build/accessibility-schema-bundle.json
verity generate schema-bundle examples/compliance --out build/compliance-schema-bundle.json
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
- Issue summary and full issue list, including nested issue locations when
  available

Security reports include:

- Workspace and VeritySpec version metadata
- Security-control count
- Control counts by coverage and risk level
- Verified-control count
- Critical unverified control IDs
- Per-control owner, category, objective, verification evidence, and target records

Accessibility reports include:

- Workspace and VeritySpec version metadata
- Accessibility-claim count
- Claim counts by owner, standard, level, impact, and coverage
- Verified-claim count
- Release gaps for critical unverified claims, claims without targets, missing
  owners, and missing verification dates
- Per-claim owner, criterion, user need, surface, verification evidence,
  assistive technologies, acceptance criteria, and target records

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

Security report output includes:

- `security.control` records from workspaces that load `verity.pack.security`
- Verification status based on `coverage`, `verification.method`, and
  `verification.evidence`
- Target records from explicit `appliesTo` references

Accessibility report output includes:

- `accessibility.claim` records from workspaces that load
  `verity.pack.accessibility`
- Verification status based on `coverage`, `verification.method`, and
  `verification.evidence`
- Target records from explicit `appliesTo` references

TypeScript and Python model generators support:

- `$ref` values that point at `#/components/schemas/...`
- Arrays
- String, number, integer, boolean, and object types
- String and scalar enums
- Nullable fields
- Optional fields
- Inline nested object shapes for TypeScript
- Inline nested dataclasses for Python object properties
- Inline nested dataclasses for Python array item objects
- Field descriptions in generated comments

OpenAPI, TypeScript, and Python output for `tests/fixtures/generator_maturity`
is covered by golden-file tests. Changes to those generators should update the
golden files only when the output contract intentionally changes.

Known limits:

- Generators do not yet emit client/server stubs.
