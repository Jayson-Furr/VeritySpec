# VeritySpec v0.42.0 Release Notes

VeritySpec v0.42.0 adds the built-in Unreal pack as the next
engine-specific game implementation and tooling surface.

## Highlights

- Added built-in `verity.pack.unreal`.
- Added strict schemas for `unreal.project`, `unreal.plugin`,
  `unreal.module`, `unreal.target`, `unreal.map`, `unreal.blueprint`,
  `unreal.data-asset`, `unreal.gameplay-tag`, `unreal.input-action`,
  `unreal.scanner`, `unreal.validation-runner`,
  `unreal.readiness-dashboard`, and `unreal.agent-context-exporter`.
- Added Unreal readiness gates and reference rules that connect game products
  to Unreal projects, implementation records, scanners, validation runners,
  readiness dashboards, and agent-context exporters.
- Added executable `examples/unreal` coverage for a game made with Unreal that
  composes with `verity.pack.game-core` without moving generic game design
  into the engine pack.
- Added Unreal graph checks, schema-bundle checks, cross-pack coverage
  dashboard coverage, compatibility manifest coverage, CI checks, docs, and
  AI-agent commands.
- Updated the engine-pack roadmap so Unity, Godot, and Unreal now have narrow
  built-in engine implementation surfaces before broader portfolio reporting
  work begins.

## Compatibility

- Package version: `0.42.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.
- No workspace format migration is required.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.42.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
