# VeritySpec v0.16.0 Release Notes

VeritySpec v0.16.0 adds public contribution guidance for proposing packs and
schema changes while preserving the project's executable-contract standard.

## Highlights

- Expanded `CONTRIBUTING.md` with contribution flow, local setup, local
  checks, pack proposal expectations, schema change expectations, and pull
  request expectations.
- Added GitHub issue templates for pack proposals and schema changes.
- Updated the pull request template with issue, compatibility, verification,
  and bookkeeping prompts.
- Linked contribution guidance from README and pack documentation.
- Added tests that keep contribution guidance and issue templates present and
  aligned with public docs.
- Added `pack` and `schema` repository labels for targeted triage.
- Updated README, changelog, roadmap, release checklist, and downstream CI
  release pins.

## Compatibility

- Package version: `0.16.0`.
- Python: `3.9` through `3.12`.
- Workspace formats: `v0.1.0` and `v0.2.0`.
- Current workspace format: `v0.2.0`.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.16.0"
verity --version
```

PyPI publishing remains prepared but requires PyPI-side trusted publishing
setup before enabling `publish_pypi=true`.
