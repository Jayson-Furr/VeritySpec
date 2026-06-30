# VeritySpec Sprint Roadmap

VeritySpec will mature through small, shippable sprints. Each sprint should
leave the repository in a releasable state with tests, examples, and CI checks
updated alongside code.

## Sprint 1: CLI Contract

Goal: make `verity` behave like a stable developer tool.

Deliverables:

- Add `verity --version`.
- Add `--format text|json` to `validate`, `lint`, and `readiness`.
- Define stable exit codes for success, validation failure, usage error, and internal error.
- Add CLI integration tests that execute the command surface.
- Add README examples for JSON output and CI usage.

Acceptance criteria:

- CLI output is scriptable.
- CI verifies command behavior, not only library behavior.
- Every documented command example works from a clean checkout.

## Sprint 2: Contract Semantics

Goal: make validation more semantic and graph-aware.

Deliverables:

- Formalize the shared record envelope.
- Add typed reference rules for allowed source and target kind relationships.
- Add validation report output as a first-class generated artifact.
- Add orphan, unused schema, cycle, deprecated-reference, and removed-reference checks.
- Add tests with intentionally broken workspaces.

Acceptance criteria:

- Broken contracts produce clear, stable issue codes.
- Graph-level failures can break CI.
- Validation reports can be saved and consumed by other tools.

## Sprint 3: Pack System

Goal: make packs independently validatable and ready for ecosystem growth.

Deliverables:

- Add `verity pack list`.
- Add `verity pack validate`.
- Define pack manifest schema.
- Validate pack schemas, readiness gates, declared generators, and kind collisions.
- Document the pack standard.

Acceptance criteria:

- Built-in packs validate independently.
- A future external pack author has a documented path.
- CI fails if pack manifests or schemas drift.

## Sprint 4: Examples and Documentation

Goal: make VeritySpec understandable from examples before reading internals.

Deliverables:

- Add `examples/api-service`.
- Add `examples/cli-tool`.
- Add `examples/events`.
- Add `examples/broken` for validation demos.
- Add docs for workspace format, record lifecycle, packs, readiness, generators, graph checks, and CI.

Acceptance criteria:

- All positive examples validate, lint, pass readiness, and generate expected artifacts.
- Broken examples fail with expected issue codes.
- Documentation is aligned with tested commands.

## Sprint 5: Release Automation

Goal: make public releases repeatable.

Deliverables:

- Add GitHub release workflow.
- Add package build checks.
- Prepare PyPI publishing for `verityspec`.
- Add changelog/release checklist.
- Add `v0.1.0` tag after release checks are stable.

Acceptance criteria:

- A release can be created from a clean tag.
- Built distributions install and expose `verity`.
- Release notes are generated from the repository state.

## Working Rule

No sprint is complete unless:

- Tests pass.
- CI passes.
- Documentation and examples match the implemented behavior.
- New behavior has at least one executable test or CLI smoke check.

