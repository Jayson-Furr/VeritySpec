# VeritySpec v0.55.0 Release Notes

VeritySpec v0.55.0 adds governance foundations for future bounded
agent-context generation and durable architecture decisions.

## Highlights

- Added agent-context generation design guidance for future bounded handoff
  artifacts for humans, tools, and AI coding agents.
- Defined expected agent-context inputs, output sections, determinism rules,
  safety boundaries, and future command shape before implementing generator
  behavior.
- Added architecture decision record process documentation and a reusable ADR
  template for major pack, generator, migration, workspace-dependency, release,
  and AI-agent operating-rule decisions.
- Added executable documentation tests that keep `CODEX.md`, `CLAUDE.md`,
  `GEMINI.md`, and `CHATGPT.md` as thin pointers to `AGENTS.md`.
- Updated README, changelog, roadmap, and Next 20 planning for the Sprint 127
  governance work.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.55.0"
verity --version
```

PyPI publishing is prepared but not enabled yet. GitHub release installation
remains the canonical public install path for this release.

## Verification

Release verification should include:

```bash
python -m unittest discover -s tests -v
verity pack validate
verity validate examples/basic
verity lint examples/basic --strict
verity readiness examples/basic --strict
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release.
