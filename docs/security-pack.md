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

## Readiness Gates

The `security.control.release` readiness gate enforces the required fields and
references above, plus a `requireVerifiedForRisk` rule: security controls whose
`riskLevel` is `critical` must be **verified** before they pass release
readiness. A control is verified when `coverage` is `verified`,
`verification.method` is not `not-verified`, and `verification.evidence` is a
non-empty string.

Unverified critical controls fail `verity readiness --strict` with the
`readiness.unverified_critical` issue code instead of only appearing in the
generated security report. Lower-risk unverified controls still surface in the
security report but do not fail readiness.

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
