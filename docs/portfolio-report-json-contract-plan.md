# Portfolio Report JSON Contract Plan

This plan defines the first future JSON contract for portfolio reporting before
any `verity generate portfolio-report` runtime behavior is implemented. It
does not add schemas, commands, generators, readiness gates, or dependency
resolution behavior.

The plan builds on the
[portfolio-level validation foundation](portfolio-validation.md), the existing
single-workspace validation, lint, readiness, graph, product-impact, evidence,
lifecycle-readiness, and agent-context generator boundaries, and the
transitional integration-workspace pattern.

## Goal

The first portfolio report JSON contract should give maintainers and CI systems
a deterministic summary of a reviewed collection of related workspaces without
inventing a second validation engine.

The report should answer:

- Which workspaces are in the portfolio?
- Which packs and workspace formats are in use?
- Which workspaces pass validation, strict linting, strict readiness, and graph
  review?
- Which workspaces have evidence gaps or generated-artifact refresh needs?
- Which shared workspace or integration-workspace relationships need impact
  review?
- Which agent-context exports need refresh after spec changes?
- Which follow-up issues should be opened or reviewed by maintainers?

The future implementation should orchestrate existing VeritySpec checks and
preserve their original issue codes, severities, locations, record IDs, and
workspace paths.

## Planned Command Shape

A future implementation can use a command shape like:

```bash
verity generate portfolio-report PORTFOLIO --out build/portfolio-report.json
```

`PORTFOLIO` may be a portfolio workspace, a portfolio configuration fixture, or
a directory containing an explicit portfolio manifest. The first implementation
should fail on ambiguous scope instead of silently scanning unrelated
directories.

JSON should be the first supported output format. Markdown can follow after the
machine-readable contract stabilizes.

## Planned JSON Shape

The report should be deterministic and structured for CI consumption:

```json
{
  "type": "portfolio_report",
  "schemaVersion": "0.1.0",
  "generatedAt": "2026-01-02T03:04:05Z",
  "verityVersion": "0.82.0",
  "portfolio": {},
  "summary": {},
  "workspaces": [],
  "relationships": [],
  "impactWarnings": [],
  "evidenceGaps": [],
  "generatedArtifactRefreshNeeds": [],
  "agentContextRefreshNeeds": [],
  "followUpRecommendations": [],
  "claimBoundaries": []
}
```

The first implementation should include `--generated-at` support for stable
golden fixtures if the generator follows the existing report-generator
convention.

## Portfolio Object

The `portfolio` object should identify the portfolio scope:

- portfolio ID or inferred fixture name
- source path
- owner or owner records when declared
- portfolio record ID when a portfolio workspace provides one
- spec version and loaded pack IDs for the portfolio workspace when available
- explicit manifest path when the report is generated from a manifest
- reviewed workspace count

The report should not infer owner, readiness, legal posture, or commercial
posture when records do not declare them.

## Workspace Entries

Each `workspaces` entry should summarize one explicitly included workspace:

- workspace ID and display name when available
- workspace path and normalized relative path
- workspace type such as product, service, library, game, engine-toolkit,
  shared-library, integration, or portfolio
- owner records or owner strings when declared
- `specVersion`
- requested pack IDs and loaded pack IDs
- record counts by kind and by pack surface
- validation status
- lint status
- readiness status
- graph status
- generated-artifact refresh needs
- agent-context exporter records and refresh status
- evidence counts and evidence gaps

Status fields should be stable objects rather than free-form text. A status
object should be able to represent `passed`, `failed`, `not_run`, and
`not_applicable`, with issue counts and severity counts when applicable.

## Relationships

The `relationships` section should describe portfolio-level relationships that
are explicitly modeled in fixtures or workspaces:

- integration workspace links
- shared library or shared engine runtime links
- dependency aliases declared in transitional fixtures
- exported record references when loaded into the validation context
- unresolved or deferred dependency relationships

Until first-class cross-workspace dependencies exist, the report should label
dependency-aware results as transitional when they are proved only by
integration workspaces or combined local fixtures.

## Impact Warnings

`impactWarnings` should summarize changes or relationships that need review:

- shared workspace records used by multiple consumers
- deprecated or removed records referenced by consuming workspaces
- missing integration workspace coverage
- missing product-impact output for declared shared contracts
- records that affect generated docs, schemas, agent-context exports, or
  release-review artifacts

Impact warnings are review signals. They should not claim breaking-change
classification unless the future implementation uses the existing `verity diff`
or `product-impact` logic to support that claim.

## Evidence Gaps

`evidenceGaps` should summarize implementation and release proof gaps without
replacing the evidence pack or evidence-report generator:

- missing evidence records for declared evidence requirements
- failing or inconclusive evidence
- evidence records with missing subjects
- evidence records with missing artifact or URI fields
- workspace entries that declare readiness profiles without corresponding
  proof records

Evidence gaps should preserve the relevant workspace path, record ID, evidence
record ID, issue code when available, and severity.

## Generated Artifact Refresh Needs

`generatedArtifactRefreshNeeds` should identify artifacts that may need to be
regenerated after portfolio or workspace changes:

- validation reports
- doctor reports
- graph outputs
- schema bundles
- product-impact reports
- lifecycle-readiness reports
- evidence reports
- agent-context exports
- downstream CI evidence bundles

The report should describe refresh needs; it should not rewrite artifacts.
Fixture rewrite behavior belongs to separate golden-fixture refresh automation
work.

## Agent Context Refresh Needs

`agentContextRefreshNeeds` should identify agent-context exporter records that
need review after related records change:

- exporter record ID and kind
- workspace path
- included record kinds
- generated artifact path when declared
- selected graph-connected records
- stale or missing output indicators when detectable
- verification commands for regenerating or reviewing the context

The report should preserve the boundary that generated agent context does not
replace `AGENTS.md`, tests, readiness checks, evidence records, or human code
review.

## Follow-Up Recommendations

`followUpRecommendations` should be machine-readable enough for maintainers to
convert into GitHub issues:

- recommendation type
- workspace path
- record ID when applicable
- severity
- suggested title
- suggested body summary
- source issue codes or report sections
- whether the recommendation blocks release review

The first implementation should not create GitHub issues automatically. It
should only report recommendations.

## Planned Fixtures

The implementation sprint should add small deterministic fixtures before broad
portfolio scanning:

- `tests/fixtures/portfolio_report/basic`
- `tests/fixtures/portfolio_report/engine-portfolio`
- `tests/fixtures/portfolio_report/evidence-gaps`
- `tests/fixtures/portfolio_report/agent-context-refresh`

The fixtures should cover at least:

- a portfolio with two or more included workspaces
- one integration workspace proving a transitional shared relationship
- one workspace with validation, lint, readiness, and graph success
- one workspace with an intentional evidence gap
- one agent-context exporter refresh need
- one generated-artifact refresh need

The first implementation should include a golden JSON fixture and should keep
placeholder values for `generatedAt`, `verityVersion`, and absolute paths where
needed.

## Acceptance Gates For Implementation

The future implementation sprint should prove:

- `verity generate portfolio-report` writes deterministic JSON.
- The JSON validates with `python -m json.tool`.
- Invalid workspace inputs fail loudly and preserve underlying issue details.
- Included workspaces can be validated, linted, checked for readiness, and
  graphed through existing VeritySpec behavior.
- The generator does not require remote registries, Git authentication,
  transitive dependency policy, or dependency lockfiles.
- README, generator docs, fixture-refresh docs, changelog, roadmap, release
  checklist, and golden tests are updated with the shipped behavior.

## Non-Goals And Non-Claims

This planning sprint does not implement portfolio-report generation.

Portfolio reports should not make commercial, legal, privacy-law, marketplace,
platform-certification, app-store, store-review, pricing-approval,
support-SLA, security-certification, or production-readiness guarantees.

Portfolio reports can summarize declared product-contract posture and evidence
records. They do not prove external approval, platform acceptance, legal
compliance, revenue readiness, store approval, or operational support quality.
