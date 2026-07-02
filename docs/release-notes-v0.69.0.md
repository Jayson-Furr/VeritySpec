# VeritySpec v0.69.0 Release Notes

VeritySpec v0.69.0 adds a post-tag release verification checklist so release
operators and AI agents can record public release evidence consistently after
the GitHub release workflow finishes.

## Highlights

- Added the public
  [post-tag release verification](post-tag-release-verification.md) checklist.
- Documented release workflow evidence after a `v*` tag push.
- Documented GitHub release asset verification, including wheel and source
  distribution hashes.
- Documented the expected skipped or absent PyPI publish job state when PyPI
  publishing has not been explicitly requested.
- Documented downloaded wheel and public GitHub tag install smoke tests.
- Documented issue closure, milestone closure, final repository state, and
  AI-agent context refresh evidence.
- Linked the checklist from README, release checklist, release-integrity, CI,
  and branching guidance.
- Added tests that keep the checklist discoverable and preserve the required
  evidence categories.
- Added release-integrity coverage for the checklist so its current tag setup
  command is updated during release prep.
- Rotated the next-20 roadmap queue after converting release automation
  guidance into sprint 146.

This release does not enable PyPI publishing, change the release workflow,
create a new runtime command, or change public version references outside the
normal release-prep surfaces.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.69.0"
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
wheel, uploads artifacts, and creates the GitHub release. After the tag
workflow completes, use the post-tag release verification checklist to record
release asset hashes, skipped PyPI state, downloaded wheel smoke results,
public GitHub tag install results, closed issue and milestone evidence, and
agent context refresh evidence.
