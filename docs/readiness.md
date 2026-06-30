# Readiness

Readiness gates are pack-declared checks for release-relevant completeness.

Example:

```json
{
  "id": "api.endpoint.release",
  "kind": "api.endpoint",
  "required": ["owner", "name", "method", "path", "summary", "responses"],
  "minItems": {
    "responses": 1
  }
}
```

Run readiness checks:

```bash
verity readiness examples/basic
verity readiness examples/basic --strict
verity readiness examples/basic --strict --format json
```

Readiness is intentionally separate from schema validation. A record can be
structurally valid but not ready for release.

## `requireVerifiedForRisk`

A gate can declare `requireVerifiedForRisk` with a list of `riskLevel` values
for which records must be verified. A record is verified when `coverage` is
`verified`, `verification.method` is not `not-verified`, and
`verification.evidence` is a non-empty string. The built-in
`security.control.release` gate uses this to fail critical unverified controls
with the `readiness.unverified_critical` issue code.

```json
{
  "id": "security.control.release",
  "kind": "security.control",
  "required": ["owner", "name", "description", "category", "objective", "coverage", "verification.method", "verification.evidence"],
  "minItems": {
    "references": 1
  },
  "requireVerifiedForRisk": ["critical"]
}
```

