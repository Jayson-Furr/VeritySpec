# VeritySpec v0.39.0 Release Notes

VeritySpec v0.39.0 adds the first built-in economy implementation pack:
`verity.pack.economy`.

## Highlights

- Added built-in `verity.pack.economy`.
- Added strict schemas for `economy.currency`, `economy.source`,
  `economy.sink`, `economy.reward`, and `economy.offer`.
- Added economy readiness gates for release-facing currency, source, sink,
  reward, and offer contracts.
- Added economy reference rules that connect game products, gameplay
  mechanics, content manifests, loot tables, currencies, sources, sinks,
  rewards, and offers.
- Added executable `examples/economy` using the Dream Extraction concept with
  game-core, gameplay, content, and economy records.
- Added economy support to cross-pack coverage dashboards, schema bundles,
  example compatibility fixtures, CI checks, release checks, and public
  documentation.
- Recorded the larger sprint policy: future sprint planning should group
  related work into cohesive bundles sized up to roughly one week of
  development effort.

## Compatibility

- Package version: `0.39.0`.
- Python support: `>=3.9`.
- Supported workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.
- No workspace format migration is required.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.39.0"
```

PyPI publishing remains prepared but disabled until the PyPI project and
trusted-publishing environment are explicitly configured.
