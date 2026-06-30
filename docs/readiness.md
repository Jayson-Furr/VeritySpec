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

Gates can also include conditional rules for pack-specific release policy:

```json
{
  "id": "security.control.release",
  "kind": "security.control",
  "required": ["owner", "name", "coverage", "verification.method"],
  "rules": [
    {
      "id": "security.control.critical-verified",
      "code": "security.control.critical_unverified",
      "when": {
        "field": "riskLevel",
        "equals": "critical"
      },
      "must": [
        {
          "field": "coverage",
          "equals": "verified"
        },
        {
          "field": "verification.method",
          "notEquals": "not-verified"
        },
        {
          "field": "verification.evidence",
          "present": true
        }
      ],
      "message": "Critical security controls must be verified before release."
    }
  ]
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

Readiness issue locations point at the relevant field when possible, such as
`records/api.json:summary` for a missing required field or
`records/security.json:coverage` for a failed conditional rule.
