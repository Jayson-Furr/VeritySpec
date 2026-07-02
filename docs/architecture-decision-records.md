# Architecture Decision Records

Architecture decision records capture important VeritySpec decisions that
should outlive the pull request discussion that introduced them.

Use an ADR when a change affects public contracts, pack architecture,
generator behavior, workspace format compatibility, migration policy, release
process, or AI-agent operating rules.

## When To Write An ADR

Write an ADR for decisions such as:

- Adding or separating official extension packs.
- Changing workspace format behavior.
- Adding a new generator family or stable output contract.
- Changing migration compatibility or rollback policy.
- Changing installed-pack discovery rules.
- Changing installed-pack compatibility metadata enforcement after the
  [installed-pack compatibility metadata](installed-pack-compatibility-metadata.md)
  design note.
- Changing AI-agent entry-point, branching, release, or CI fallback policy.
- Choosing a long-term architecture for cross-workspace dependencies.
- Changing the CLI command module architecture after the
  [CLI command module decomposition](cli-command-modules.md) design note.

Small bug fixes, docs corrections, and narrow schema additions usually do not
need an ADR unless they change public guarantees.

## Storage

Store accepted ADRs under a future `docs/adr/` directory using a stable numeric
prefix:

```text
docs/adr/0001-short-title.md
```

Until the first accepted ADR exists, use [adr-template.md](adr-template.md) as
the canonical template.

Product-delivery workspaces can also index structured `decision.record`
records without replacing ADR prose:

```bash
verity generate decision-index examples/product-delivery --out build/decision-index.json
verity generate decision-index examples/product-delivery --format markdown --out build/decision-index.md
```

The generated decision index summarizes decision status, owner, type, graph
links, and index gaps for review. It does not approve decisions, replace ADR
text, or make implementation-readiness, legal, commercial, privacy, platform,
marketplace, or support claims.

## Status Values

Use one of these statuses:

- `Proposed`: under discussion and not yet accepted.
- `Accepted`: current project direction.
- `Superseded`: replaced by a later ADR.
- `Rejected`: considered and intentionally not adopted.

An accepted ADR should link to the replacing ADR when it becomes superseded.

## Review Expectations

An ADR should explain:

- Context and problem statement.
- Decision and rationale.
- Alternatives considered.
- Consequences and tradeoffs.
- Compatibility and migration impact.
- Verification plan.
- Rollback or supersession criteria.

The ADR does not replace tests, docs, release notes, or roadmap updates. It
records why a direction was chosen so future maintainers and AI agents do not
re-litigate the same decision from partial context.

## Pull Request Use

When a PR includes an ADR:

- Link the ADR from the PR body.
- Include tests or documentation that enforce the public behavior introduced by
  the decision.
- Update `ROADMAP.md` when the ADR changes future sequencing.
- Update `AGENTS.md` only when the decision affects repository operating rules.
