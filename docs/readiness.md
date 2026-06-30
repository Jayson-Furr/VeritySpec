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

Conditional rules support:

- `equals` for exact field matches
- `notEquals` for exact field mismatches
- `present` for required or forbidden field presence
- `dateWithinDays` for a fixed maximum age in days
- `dateWithinDaysField` for a maximum age read from another field

Security controls use `dateWithinDaysField` to compare
`verification.lastVerified` against `verification.reviewCadenceDays`.

Deployment targets use conditional readiness rules to require production
release controls. A `deployment.target` with `environment: "production"` must
require approval, declare a rollback plan, and expose a health-check URL.

Game-core records use readiness gates to keep early game contracts executable.
A `game.product` should link to mode, loop, and prototype-scope records before
strict readiness passes.

Game-assets records use readiness gates to keep creative-source contracts
traceable. A `game.visual-identity` should link to identity image and concept
art records before strict readiness passes.

Unity records use readiness gates to keep implementation contracts executable.
A `unity.project` should link to package, scene, and build-target records before
strict readiness passes.

Gameplay records use readiness gates to keep mechanics and encounters
implementation-ready. A `game.mechanic` should declare inputs, outputs, and
graph references before strict readiness passes.

Content records use readiness gates to keep item, level, loot-table, and
manifest contracts traceable. A `game.content-manifest` should include content
references and graph links before strict readiness passes.

Run readiness checks:

```bash
verity readiness examples/basic
verity readiness examples/basic --strict
verity readiness examples/basic --profile release
verity readiness examples/deployment --strict
verity readiness examples/game-core --strict
verity readiness examples/game-assets --strict
verity readiness examples/unity --strict
verity readiness examples/gameplay --strict
verity readiness examples/content --strict
verity readiness examples/basic --strict --format json
```

Readiness is intentionally separate from schema validation. A record can be
structurally valid but not ready for release.

Product-contract profiles can set the effective strictness for readiness. For
example, `--profile release`, `--profile strict`, `--profile regulated`, and
`--profile public-api` run readiness with strict enforcement, while
`--profile internal-tool` leaves warnings advisory.

Readiness issue locations point at the relevant field when possible, such as
`records/api.json:summary` for a missing required field or
`records/security.json:coverage` for a failed conditional rule.
