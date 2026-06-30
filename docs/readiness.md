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

