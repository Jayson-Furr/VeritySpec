# Accessibility Pack

`verity.pack.accessibility` adds accessibility claim records without expanding
the core kernel.

## Record Kinds

- `accessibility.claim`: accessibility claim, standard or criterion, user need,
  impacted surface, coverage, verification method, and evidence.

## Relationships

The pack declares these reference relationships:

- `product` `accessibilityCoveredBy` `accessibility.claim`
- `accessibility.claim` `appliesTo` `product`
- `accessibility.claim` `appliesTo` `api.endpoint`
- `accessibility.claim` `appliesTo` `cli.command`
- `accessibility.claim` `appliesTo` `event.message`
- `accessibility.claim` `appliesTo` `schema.object`

## Readiness

Accessibility claims must include:

- owner, name, description
- standard, criterion, and level
- user need and affected surface
- impact and coverage
- verification method and evidence
- at least one reference to the product surface the claim applies to

Critical accessibility claims also emit
`accessibility.claim.critical_unverified` when they are not verified.

## Example

```bash
verity validate examples/accessibility
verity lint examples/accessibility --strict
verity readiness examples/accessibility --strict
verity generate accessibility-report examples/accessibility --out build/accessibility-report.json
verity generate schema-bundle examples/accessibility --out build/accessibility-schema-bundle.json
```

The example workspace connects a checkout product to a WCAG-style keyboard
operation claim with verification evidence.

## Report

`accessibility-report` emits JSON with:

- counts for accessibility claims
- ownership, standard, level, impact, and coverage summaries
- verified-claim count
- release gaps for critical unverified claims, claims without targets, missing
  owners, and missing verification dates
- detailed claim entries with verification evidence, acceptance criteria,
  assistive technologies, and connected targets
