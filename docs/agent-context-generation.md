# Agent-Context Generation

VeritySpec can generate bounded implementation context for humans, tools, and
AI coding agents. The first implementation is a Markdown handoff artifact
created by `verity generate agent-context` from product-delivery and engine
agent-context exporter records.

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

The current generator starts from a workspace plus a requested exporter record:

```bash
verity generate agent-context examples/product-delivery --record agent-context.exporter.implementation_bundle --format markdown --out build/agent-context.md
```

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

The Markdown artifact includes:

- Workspace identity, VeritySpec version, generation timestamp, and selected
  target.
- Target exporter metadata, including output path, included record kinds,
  privacy policy, and redaction policy.
- Relevant records selected from the exporter, declared included kinds, and
  graph-connected records.
- Graph links between selected records.
- Generated artifacts that may need refresh.
- Known deprecated or removed records that must not be referenced.
- Safety boundaries and process limits.
- Verification commands expected before handoff or PR.

Future versions can add richer Contract constraints, Readiness gates and
evidence requirements, prohibited drift sections, likely affected files, and
machine-readable JSON once the contract stabilizes enough for tools and CI
integrations.

Future Readiness gates and evidence requirements should remain grounded in
VeritySpec records rather than being inferred from prompt text.

## Determinism

Agent context must be deterministic for the same workspace, target, pack set,
and generation timestamp. Output sorts records and graph links by stable IDs
and supports `--generated-at` when fixture or CI review needs a fixed
timestamp.

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

## Command Shape

The command requires `--record` because an agent-context artifact must be
bounded by an explicit exporter record:

```bash
verity generate agent-context examples/product-delivery --record agent-context.exporter.implementation_bundle --format markdown --out build/agent-context.md
```

Supported target kinds are:

- `agent-context.exporter`
- `unity.agent-context-exporter`
- `godot.agent-context-exporter`
- `unreal.agent-context-exporter`

The generator uses the same workspace loading, pack loading, graph, and
validation behavior as the rest of the CLI. It does not invent records or
silently ignore validation errors.

## Future Work

Next maturity steps include:

- Richer sections for Contract constraints, Readiness gates and evidence
  requirements, prohibited drift, likely affected files, and implementation
  scope.
- JSON output for downstream tools once the Markdown contract is stable.
- Targeted generation from feature, release, portfolio, or lifecycle records
  when those records declare enough context to bound an implementation task.
- Additional examples for Unity, Godot, and Unreal exporter records.
