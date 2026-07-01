# VeritySpec v0.41.0 Release Notes

VeritySpec v0.41.0 adds the built-in Godot pack as the next engine-specific
game implementation and tooling surface.

## Highlights

- Added built-in `verity.pack.godot`.
- Added strict schemas for `godot.project`, `godot.addon`,
  `godot.shared-library`, `godot.scene`, `godot.node-contract`,
  `godot.resource`, `godot.script`, `godot.autoload`, `godot.input-action`,
  `godot.export-preset`, `godot.scanner`, `godot.validation-runner`,
  `godot.readiness-dashboard`, and `godot.agent-context-exporter`.
- Added Godot readiness gates and reference rules that connect game products
  to Godot projects, implementation records, export presets, scanners,
  validation runners, readiness dashboards, and agent-context exporters.
- Added executable `examples/godot` coverage for a game made with Godot that
  composes with `verity.pack.game-core` without moving generic game design
  into the engine pack.
- Added Godot graph checks, schema-bundle checks, cross-pack coverage
  dashboard coverage, compatibility manifest coverage, CI checks, docs, and
  AI-agent commands.
- Updated engine-pack planning so future Unreal work starts with an executable
  game workspace, not only engine-tooling repository coverage.

## Compatibility

- Package version: `0.41.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.
- No workspace format migration is required.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.41.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
