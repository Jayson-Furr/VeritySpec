# CLI Command Module Decomposition

VeritySpec's CLI is currently implemented in `src/verityspec/cli.py`. That file
is still workable, but the command surface is growing: workspace dependencies,
portfolio reports, lifecycle reports, agent-context generation, official
extension-pack tooling, and future dependency commands will add more parser and
handler logic.

This note defines the intended command module boundary before moving code. No runtime command movement is introduced by this design note. The current `verity` commands, arguments, exit codes, text output, JSON output, and GitHub Actions annotation behavior must remain compatible while the implementation is decomposed in later sprints.

## Goals

- Keep `verity` as the stable console command and `verityspec.cli:main` as the
  public entry point.
- Split command registration and handlers by command family before larger
  dependency, portfolio, lifecycle, and agent-context command families expand.
- Keep shared output, issue, profile, workspace-loading, and pack-loading
  helpers in one place so command modules do not drift.
- Preserve argparse for now; this is a module boundary plan, not a framework
  replacement.
- Make future command additions reviewable by domain instead of growing one
  central command hub indefinitely.

## Current Shape

`src/verityspec/cli.py` currently owns several responsibilities:

- top-level parser construction
- common argument helpers such as `--pack-path`, `--profile`, `--format`,
  `--strict`, and GitHub annotation flags
- command handlers for `init`, `validate`, `lint`, `readiness`, `doctor`,
  `explain`, `graph`, `diff`, `migrate`, `generate`, `import`, and `pack`
- text and JSON output helpers
- issue summary and exit-code policy
- starter workspace and pack scaffold helpers

That shape kept early development simple. The next growth phase needs clearer
module ownership so future command families can be added without making
unrelated behavior harder to review.

## Proposed Package Layout

Future decomposition should introduce a `verityspec.commands` package:

```text
src/verityspec/
  cli.py
  commands/
    __init__.py
    common.py
    init.py
    validate.py
    lint.py
    readiness.py
    doctor.py
    explain.py
    graph.py
    diff.py
    migrate.py
    generate.py
    import_.py
    pack.py
    deps.py
    portfolio.py
    agent_context.py
```

The exact file names can change when implementation starts, but the ownership
rule should stay stable: modules are organized around command families and
public command contracts, not around whichever helper function is convenient to
move first.

## Entry Point Contract

`src/verityspec/cli.py` should remain the public entry point. After
decomposition, it should be responsible for:

- defining the top-level `argparse.ArgumentParser`
- wiring `--version`
- calling `verityspec.commands.register_all(subparsers)`
- parsing arguments
- invoking the selected handler
- translating unexpected exceptions into `EXIT_INTERNAL_ERROR`

Command modules should not import `verityspec.cli`. Shared helpers should move
to `verityspec.commands.common` first so command modules can depend on common
behavior without creating import cycles.

## Command Registration Contract

Each command module should expose a registration function that accepts the
relevant argparse subparser object and attaches its handler:

```python
def register(subparsers):
    parser = subparsers.add_parser("validate", help="Validate a workspace.")
    parser.add_argument("workspace")
    parser.set_defaults(func=cmd_validate)
```

Nested command families, such as `verity pack`, should keep their subcommand
registration inside that family module. A future `verity deps` command should
follow the same pattern instead of adding special-case registration logic to
`cli.py`.

## Shared Helpers

Move shared helpers before moving command families. The first helper module
should include:

- exit-code constants
- `load_context`
- issue result and issue summary helpers
- GitHub annotation output helper
- common argparse helpers for `--pack-path`, `--profile`, `--format`,
  `--strict`, `--fail-on`, and `--generated-at`
- generated-output write helpers where command modules need a common wrapper

Command modules should keep domain-specific helper functions only when those
helpers are not reused elsewhere. For example, graph filtering helpers can stay
with `commands.graph`, while issue output helpers belong in `commands.common`.

## Suggested Migration Phases

1. Add this design note and tests. Do not move runtime code in the same sprint.
2. Introduce `verityspec.commands.common` and move shared helpers with focused
   tests that prove CLI output and exit codes are unchanged.
3. Move low-risk independent command families first: `explain`, `diff`,
   `graph`, and `pack`.
4. Move workspace contract commands next: `validate`, `lint`, `readiness`, and
   `doctor`.
5. Move `migrate`, `import`, and scaffold commands after their shared helper
   boundaries are clear.
6. Move `generate` last because it has the widest artifact surface and the most
   output-format behavior.
7. Add future `deps`, `portfolio`, and `agent_context` command families only
   after the registration contract has real module coverage.

Each phase should have a branch, issue, tests, README or docs updates where
needed, and normal PR/CI verification.

## Compatibility Guardrails

Future implementation must preserve:

- `verity --version`
- existing top-level command names and subcommand names
- current exit-code meanings: success, contract failure, usage error, and
  internal error
- text and JSON output contracts for existing commands
- stable issue-code payloads
- GitHub Actions annotation behavior
- README command smoke-test coverage
- downstream workflow examples
- release-integrity surfaces

The decomposition should not add Click, Typer, or another CLI framework unless
there is a separate design note or ADR explaining the migration, compatibility
plan, and rollback path.

## Test Expectations

Each movement phase should include focused tests that prove:

- parser registration still exposes the expected command names
- moved handlers return the same exit codes for representative success, usage
  error, and contract-failure cases
- JSON output remains parseable and keeps existing keys
- text output keeps documented human-facing phrases
- README command smoke tests still pass
- command modules do not import `verityspec.cli`

When moving a command family, prefer targeted tests around that family plus the
existing full CLI suite. Do not rely only on broad test discovery to prove a
public command stayed compatible.

## Non-Goals

This design note does not:

- move command implementations
- change public command names, arguments, output formats, or exit codes
- introduce a new CLI framework
- add dependency, portfolio, lifecycle, or agent-context commands
- change workspace schemas, pack schemas, readiness gates, or generator output
- detach specialized packs from the core package

## First Implementation Gate

The first implementation sprint after this design note should move only shared
helpers and one low-risk command family. It should include before/after CLI
behavior tests and should avoid mixing decomposition with feature work.

The expected first candidate is `verity explain` or `verity diff`, because each
has a small parser surface, deterministic output, and minimal workspace-loading
behavior.
