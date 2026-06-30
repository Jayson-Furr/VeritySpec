# Security Pack

`verity.pack.security` adds executable security-control records without moving
security concepts into the VeritySpec core kernel.

## Record Kind

The first security kind is `security.control`.

Security controls describe a release-relevant security requirement, its risk
level, implementation coverage, verification evidence, and target records.

Required release fields include:

- `owner`
- `name`
- `description`
- `category`
- `objective`
- `coverage`
- `verification.method`
- `verification.evidence`
- at least one `references` item

Use explicit references to connect controls to product surfaces:

```json
{
  "id": "security.control.account_access",
  "kind": "security.control",
  "name": "Account Access Control",
  "status": "ready",
  "owner": "platform-security",
  "description": "Limits account profile access to authorized callers.",
  "category": "authorization",
  "controlType": "preventive",
  "riskLevel": "high",
  "objective": "Prevent unauthorized access to account profile data.",
  "coverage": "verified",
  "verification": {
    "method": "automated-test",
    "evidence": "tests/security/test_account_access.py::test_owner_or_support_required",
    "lastVerified": "2026-06-30"
  },
  "references": [
    {
      "type": "appliesTo",
      "target": "api.accounts.get"
    }
  ]
}
```

Product records can reference controls with `securedBy`.

## Critical Control Readiness

Critical controls are release-blocking when they are not verified. A
`security.control` record with `riskLevel: "critical"` must have:

- `coverage: "verified"`
- `verification.method` set to a value other than `not-verified`
- non-empty `verification.evidence`

If a critical control does not meet those conditions, readiness emits
`security.control.critical_unverified`. With `verity readiness --strict`, that
issue is an error.

## Commands

```bash
verity validate examples/security
verity lint examples/security --strict
verity readiness examples/security --strict
verity generate security-report examples/security --out build/security-report.json
```

## Security Report

`security-report` emits JSON with:

- workspace metadata
- total control count
- counts by `coverage`
- counts by `riskLevel`
- verified-control count
- critical unverified control IDs
- per-control target records from `appliesTo` references

The report is intended for CI, release review, and downstream dashboards.
