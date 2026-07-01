# Agent-Context Generation Design

VeritySpec should eventually generate bounded implementation context for
humans, tools, and AI coding agents. This document defines the intended
contract before a production `verity generate agent-context` command exists.

The goal is not to make an agent infer product intent from scattered docs. The
goal is to let VeritySpec gather the relevant, validated records for a task and
emit a compact handoff artifact that keeps the product contract visible.

## Design Goals

- Keep the VeritySpec workspace as the source of truth.
- Give agents enough context to act without copying the whole repository into a
  prompt.
- Make constraints, readiness gates, evidence needs, and prohibited drift
  explicit.
- Preserve traceability from generated context back to record IDs and pack
  ownership.
- Keep output deterministic enough for review, tests, and CI comparisons.
- Support human review before generated context is used for implementation.

## Inputs

The future generator should start from a workspace plus either a requested
record, exporter record, or named target.

Useful input records include:

- Core product and schema records.
- Product-delivery `agent-context.exporter` records.
- Engine-specific exporter records such as `unity.agent-context-exporter`,
  `godot.agent-context-exporter`, and `unreal.agent-context-exporter`.
- Feature, API, CLI, event, gameplay, content, mobile, liveops, evidence, and
  deployment records linked through the graph.
- Readiness profiles and evidence requirements that apply to the requested
  target.

The generator should use the same workspace loading, pack loading, graph, and
validation behavior as the rest of the CLI. It should not invent records or
silently ignore validation errors.

## Output Sections

A generated agent-context artifact should include:

- Workspace identity, VeritySpec version, generation timestamp, and selected
  target.
- The requested task or implementation scope.
- Relevant records, grouped by kind and graph relationship.
- Contract constraints the agent must preserve.
- Readiness gates and evidence requirements that must pass after work.
- Generated artifacts that may need refresh.
- Files, directories, or external systems likely affected when known from
  records.
- Records that should not drift during the task.
- Known deprecated or removed records that must not be referenced.
- Verification commands expected before handoff or PR.

Markdown is the likely first human-facing format. JSON can follow once the
contract stabilizes enough for tools and CI integrations.

## Determinism

Agent context must be deterministic for the same workspace, target, pack set,
and generation timestamp. Output should sort records by stable IDs and should
include a future `--generated-at` option if timestamps are part of the artifact.

Deterministic output lets maintainers review generated context like any other
generated report and makes drift visible in pull requests.

## Safety Boundaries

The generator should be explicit about what it does not prove:

- It does not prove implementation correctness.
- It does not replace tests, readiness checks, or evidence records.
- It does not make legal, commercial, privacy, marketplace, or certification
  claims.
- It does not authorize agents to bypass repository process.
- It does not replace `AGENTS.md` as the canonical repository entry point.

The generated artifact should point agents back to `AGENTS.md` for repository
process, shell discipline, branching, PR, release, and bookkeeping rules.

## Future Command Shape

The eventual command could look like:

```bash
verity generate agent-context examples/product-delivery --record agent-context.exporter.coverage_agent_context --out build/agent-context.md
```

This sprint intentionally does not implement that command. The design note
exists so later implementation can be reviewed against a clear contract instead
of growing as an ad hoc prompt generator.

## Implementation Readiness Before Generator Work

Before implementation, VeritySpec should have:

- A stable output outline for Markdown.
- A sampled fixture workspace with representative graph links.
- Tests for target selection, deterministic ordering, and validation failure
  behavior.
- README and generator docs that avoid overstating agent autonomy.
- A plan for JSON output if downstream tools need machine-readable context.
