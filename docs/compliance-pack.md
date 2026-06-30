# Compliance Pack

`verity.pack.compliance` adds compliance-mapping records without turning
VeritySpec into a legal attestation system.

## Record Kind

The first compliance kind is `compliance.mapping`.

Compliance mappings connect product records, security controls, accessibility
claims, and observability signals to internal or external framework
requirements. They are designed for traceability, readiness review, and future
matrix generation.

Required release fields include:

- `owner`
- `name`
- `description`
- `framework.name`
- `framework.requirementId`
- `mappingType`
- `coverage`
- `attestation`
- `verification.method`
- `verification.evidence`
- at least one `references` item

`attestation` must be `false`. The pack tracks mapping evidence; it does not
claim audit, certification, legal, or regulatory compliance.

Use explicit references to connect mappings to product-contract records:

```json
{
  "id": "compliance.mapping.checkout_access_review",
  "kind": "compliance.mapping",
  "name": "Checkout Access Review Mapping",
  "status": "ready",
  "owner": "risk",
  "description": "Maps checkout access controls and evidence to an internal review requirement.",
  "framework": {
    "name": "internal-access-review",
    "version": "2026.1",
    "requirementId": "IAR-1",
    "requirementTitle": "Access and evidence review"
  },
  "mappingType": "control",
  "coverage": "reviewed",
  "attestation": false,
  "verification": {
    "method": "evidence-review",
    "evidence": "reviews/compliance/checkout-access-review.md",
    "lastVerified": "2026-06-30"
  },
  "references": [
    {
      "type": "covers",
      "target": "security.control.checkout_access"
    }
  ]
}
```

Product records can reference compliance mappings with `complianceMappedBy`.

## Reviewed Mapping Readiness

Reviewed mappings are release-blocking when they do not include real
verification evidence. A `compliance.mapping` record with
`coverage: "reviewed"` must have:

- `verification.method` set to a value other than `not-verified`
- non-empty `verification.evidence`

If a reviewed mapping does not meet those conditions, readiness emits
`compliance.mapping.reviewed_unverified`. With `verity readiness --strict`,
that issue is an error.

## Commands

```bash
verity validate examples/compliance
verity lint examples/compliance --strict
verity readiness examples/compliance --strict
verity generate compliance-matrix examples/compliance --out build/compliance-matrix.json
verity generate schema-bundle examples/compliance --out build/compliance-schema-bundle.json
```

## Current Scope

The compliance pack currently provides:

- strict `compliance.mapping` schema validation
- readiness gates and reviewed-mapping policy
- reference rules for products, APIs, CLIs, events, schemas, security controls,
  accessibility claims, and observability records
- compliance matrix generation
- schema-bundle generator support
- an executable example workspace

## Compliance Matrix

`compliance-matrix` emits JSON with:

- workspace and VeritySpec version metadata
- compliance-mapping count
- owner, framework, requirement, mapping type, and coverage summaries
- verified-mapping count
- release gaps for mappings without targets, mappings without evidence,
  reviewed-but-unverified mappings, missing mapping owners, and referenced
  targets without owners
- one row per compliance mapping with framework metadata, verification state,
  mapped targets, and grouped security, accessibility, and observability
  evidence
