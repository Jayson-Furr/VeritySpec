# VeritySpec v0.18.0 Release Notes

VeritySpec v0.18.0 adds a roadmap governance generator so maintainers and AI
agents can inspect sprint and planning state through a machine-readable report.

## Highlights

- Added `verity generate roadmap-report` for JSON reports generated from
  `ROADMAP.md`.
- Included release milestone sections, sprint rows, active milestones, latest
  released milestone, completed sprint counts, and Next 20 planning points.
- Allowed the command to read either a repository directory containing
  `ROADMAP.md` or a direct roadmap file path.
- Added library and CLI coverage for the roadmap-report shape.
- Updated README, generator docs, changelog, roadmap, downstream CI pins, and
  release bookkeeping for `v0.18.0`.

## Compatibility

- Package version: `0.18.0`.
- Python: `3.9` through `3.12`.
- Workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.18.0"
verity --version
```

PyPI publishing remains prepared but disabled. Keep `publish_pypi=false` unless
the PyPI project and trusted-publishing setup have been verified and publishing
has been explicitly requested.
