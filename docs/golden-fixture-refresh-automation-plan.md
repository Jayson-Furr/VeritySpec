# Golden Fixture Refresh Automation Plan

This plan defines the safety contract for future golden-fixture refresh
automation. It does not add CLI commands, schemas, generators, readiness gates,
or rewrite behavior in this planning sprint.

The current authority remains the [fixture refresh guide](fixture-refresh.md):
generate into `build/`, inspect output drift, preserve placeholders, update only
the intended committed fixtures, and run focused golden tests plus the standard
local checks before committing.

No automatic fixture rewrite command is provided by this plan.

## Goal

Future automation should make fixture refreshes easier to review without making
fixture churn easier to hide.

The plan uses generator allowlists so future refreshes stay explicit.

The first automation slice should provide a dry-run report, generator
allowlists, and explicit safety checks that answer:

- Which generator was run?
- Which workspace or input paths were used?
- Which committed golden fixtures would change?
- Which placeholders would be preserved?
- Which diffs are behavioral, structural, metadata-only, or
  release-version-only?
- Which rewrite requests are blocked by policy?
- Which maintainer approval gates still need to happen before committed
  fixtures change?

Automation should support the existing generator contracts in
[generators.md](generators.md), the release-version checks in
[release-integrity.md](release-integrity.md), the release workflow in
[release-checklist.md](release-checklist.md), and the golden tests under
`tests/golden`.

## Planned Command Shape

The future command shape is intentionally explicit and allowlist driven:

```bash
verity fixtures refresh \
  --dry-run \
  --generator security-report \
  --workspace examples/security \
  --golden tests/golden/security_report/security_report.json \
  --generated-at 2026-01-02T03:04:05Z \
  --out build/fixture-refresh-diff.json
```

The first implementation should require `--dry-run`. A later rewrite mode can
be considered only after the dry-run report has stable tests, fixture coverage,
and maintainer review.

Automation should not infer broad fixture ownership from a generator name. A
fixture refresh request should name the generator, workspace or input paths,
committed golden path, output format when needed, and deterministic timestamp
when the generator supports `--generated-at`.

## Planned JSON Shape

The dry-run output should be machine-readable so PRs and release reviews can
preserve evidence:

```json
{
  "type": "golden_fixture_refresh_plan",
  "schemaVersion": "0.1.0",
  "generatedAt": "2026-01-02T03:04:05Z",
  "verityVersion": "0.81.0",
  "mode": "dry_run",
  "allowlist": {
    "generators": [],
    "workspaces": [],
    "goldenPaths": []
  },
  "inputs": [],
  "generatedOutputs": [],
  "fixtureComparisons": [],
  "placeholderPreservation": [],
  "diffSummary": {},
  "approvalGates": [],
  "blockedRewrites": [],
  "claimBoundaries": []
}
```

### Allowlist

`allowlist` should record the exact generators, workspace paths, input paths,
and committed fixture paths approved for the dry run. The command should reject
requests that try to refresh every fixture, cross generator boundaries without
explicit entries, or write outside the repository fixture paths.

### Inputs

`inputs` should record the workspace or command input paths, generator ID,
format, `--generated-at` value, and target golden path. For generators such as
`product-impact` that take two workspace paths, the input entry should preserve
both baseline and current paths.

### Generated Outputs

`generatedOutputs` should record paths under `build/`, JSON parse status where
applicable, stdout or stderr summaries, generator exit status, and whether the
generator supports deterministic timestamps.

### Fixture Comparisons

`fixtureComparisons` should compare generated output with committed golden
fixtures after the same normalization used by existing tests. Each comparison
should classify the change as one of:

- `no_change`
- `behavioral`
- `structural`
- `metadata_only`
- `release_version_only`
- `blocked`

### Placeholder Preservation

`placeholderPreservation` should record dynamic fields that must stay
normalized in committed fixtures, including:

- `generatedAt`
- `verityVersion`
- absolute workspace paths
- platform-specific path separators
- release artifact hashes when they are intentionally represented by
  placeholders
- Markdown placeholders such as `<generatedAt>`, `<verityVersion>`, and
  `<workspacePath>`

The automation should fail the dry run if a generated output would replace a
known placeholder with local machine data, current timestamps, private paths, or
release evidence that has not been intentionally approved.

### Diff Summary

`diffSummary` should summarize changed file counts, changed JSON keys,
Markdown section changes, added or removed records, and whether the output
drift affects the public generator contract documented in `docs/generators.md`.

### Approval Gates

`approvalGates` should list the maintainer actions required before any fixture
change can be committed:

- dry-run report reviewed in the PR
- generator or release-version reason named
- focused golden tests run
- `tests/test_release_integrity.py` run when release-version fixtures change
- standard local checks run
- changed fixture paths match the allowlist
- placeholders preserved
- no unrelated generated output committed from `build/`

### Blocked Rewrites

`blockedRewrites` should record unsafe requests, including broad all-fixture refreshes,
missing allowlist entries, missing deterministic timestamp values,
attempts to rewrite unrelated fixtures, private path leakage, ignored
placeholder rules, and requests to bypass tests or approval gates.

### Claim Boundaries

`claimBoundaries` should state that fixture refresh automation only reviews
generated output drift. It does not prove external commercial, legal,
privacy-law, marketplace, app-store, platform-certification, pricing-approval,
support-SLA, security-certification, or production-readiness guarantees.

## Planned Fixture Families

The first implementation should include deterministic fixtures before any
rewrite mode exists:

| Fixture | Purpose |
|---|---|
| `tests/fixtures/fixture_refresh/basic-dry-run` | Single generator, single golden path, no rewrite |
| `tests/fixtures/fixture_refresh/placeholder-preservation` | Dynamic metadata stays normalized |
| `tests/fixtures/fixture_refresh/blocked-rewrite` | Unsafe rewrite request is reported and refused |
| `tests/fixtures/fixture_refresh/allowlist` | Multiple explicit allowlist entries without broad churn |

The implementation should also add at least one golden JSON fixture for the
dry-run report contract once the report schema is executable.

## Acceptance Gates For Implementation

A future implementation sprint should not ship until it includes:

- CLI and library tests for dry-run output.
- Fixture coverage for allowlists, placeholder preservation, blocked rewrites,
  and deterministic timestamp handling.
- Golden output for the dry-run report JSON contract.
- Documentation updates in `docs/fixture-refresh.md`,
  `docs/generators.md`, `docs/release-checklist.md`, and README.
- Release-integrity coverage when release-version fixtures are in scope.
- PR guidance that names reviewed generated files under `build/`.
- No default rewrite mode.
- There is no default rewrite mode.

## Non-Goals And Non-Claims

This plan does not:

- implement `verity fixtures refresh`
- bulk rewrite committed fixtures
- replace maintainer review
- bypass golden tests
- change generator output contracts
- change release-version fixture authority
- publish generated artifacts
- approve release readiness or production readiness

Fixture refresh automation should help maintainers review generated output
changes. It should not turn generated output into unchecked source-of-truth
updates.
