# External Pack Maintainer Review Checklist

This checklist is for maintainers reviewing public external pack proposals.
It turns the pack standard into a repeatable acceptance process without making
every proposal part of the core package.

External pack acceptance means the proposal is clear enough to build, test,
document, and support as a VeritySpec pack. It does not mean the pack is
bundled, official, detached from core, or guaranteed to be accepted into the
`verityspec` wheel.

## Review Inputs

Before review, the proposal should include:

- a GitHub issue using the `Pack proposal` template;
- a proposed pack ID that does not shadow built-in pack IDs;
- the product problem and product surface the pack makes executable;
- initial record kinds and ownership boundaries;
- reference rules introduced by the pack;
- readiness gates or conditional readiness rules;
- generator, report, or useful artifact expectations;
- executable example or fixture expectations;
- compatibility, versioning, migration, and deprecation notes.

If any of those inputs are missing, ask for proposal clarification before
accepting implementation work.

## Identity Gate

Maintainers should confirm:

- the pack ID follows the `verity.pack.<surface>` style;
- the pack ID is stable enough to appear in workspace manifests;
- the pack does not duplicate an existing built-in or proposed pack;
- the pack has a clear owner or maintainer group;
- the pack boundary is narrow enough to avoid becoming a broad static catalog;
- the proposal explains why the product surface belongs in a pack instead of
  the core runtime.

## Contract Gate

The pack contract should include:

- a valid `pack.json` manifest;
- strict JSON Schemas for each record kind;
- shared record envelope requirements: `id`, `kind`, `name`, `status`, and
  `owner`;
- required pack-specific fields with clear validation behavior;
- reference rules for relationships introduced by the pack;
- readiness gates for release-relevant records;
- generator metadata for every generator or report the pack advertises.

Maintainers should reject proposals that add mostly empty schema/catalog pairs
without executable checks, examples, or generated artifacts.

## Executability Gate

Accepted implementation work should prove the pack is executable:

- positive examples validate with `verity validate`;
- examples lint cleanly with `verity lint --strict`;
- examples pass `verity readiness --strict` when intended to be release-ready;
- graph behavior is covered when the pack adds references;
- generator or report output is tested when the pack advertises a generator;
- negative fixtures cover important validation, readiness, or reference-rule
  failures;
- `verity pack validate` passes for the pack manifest and schemas;
- `verity pack doctor --path <pack>` reports no discovery errors for the local
  pack path.

## Documentation Gate

Public documentation should explain:

- the pack's product surface and non-goals;
- each record kind's purpose;
- required relationships and readiness expectations;
- generator or report output, if any;
- example workspace commands;
- compatibility, migration, and deprecation posture;
- whether the pack is built-in, local external, installed, official mirror,
  detached, deprecated, or experimental.

The README and `docs/packs.md` should link public docs for accepted built-in
packs or official extension-pack candidates.

## Compatibility Gate

Before accepting a pack into a public release path, maintainers should check:

- supported VeritySpec package versions;
- supported workspace format versions;
- pack manifest schema compatibility;
- record-kind stability and deprecation posture;
- migration impact for existing examples or downstream workspaces;
- generator output stability and golden fixture needs;
- interaction with installed-pack discovery and local `packPaths`;
- built-in collision behavior and source precedence.

Specialized packs that may become official extension packages must also follow
the staged gates in the
[Specialized pack separation plan](specialized-pack-separation.md).

## PR Review Gate

Implementation pull requests should include:

- the issue or milestone link;
- local verification commands and results;
- tests for validation, lint, readiness, graph behavior, generators, and
  fixtures where relevant;
- docs, examples, README, changelog, and roadmap updates when public-facing;
- release-note coverage when behavior is shipped;
- migration or rollback notes for compatibility-sensitive changes.

If GitHub Actions is unavailable because of billing, credits, quota, runner
availability, or another platform issue, maintainers should require equivalent
local checks to be recorded in the PR before merging.

## Acceptance Outcomes

After review, mark the proposal as one of:

- `accepted`: ready for implementation in a scoped sprint;
- `needs-design`: useful direction, but the contract boundary or behavior is
  not clear enough;
- `needs-fixture`: needs examples, negative fixtures, or generated output
  expectations before implementation;
- `out-of-scope`: does not fit VeritySpec's pack model or current roadmap;
- `duplicate`: covered by an existing pack or active proposal;
- `deferred`: valid direction, but not a current release priority.

Accepted proposals should still move through a normal branch, PR, CI, and
release process. The checklist is a review gate, not a shortcut around the
repository operating loop.
