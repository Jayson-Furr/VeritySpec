# VeritySpec v0.74.0 Release Notes

VeritySpec v0.74.0 adds Markdown output for the issue-code catalog so stable
diagnostic metadata can be published for documentation sites, CI diagnostics,
and agent workflows without hand-converting the JSON catalog.

## Highlights

- Added `--format markdown` support for
  `verity generate issue-code-catalog`.
- Kept `issue-code-catalog` as a no-workspace generator and continued
  rejecting workspace paths.
- Preserved JSON as the machine-readable issue-code catalog contract.
- Added a Markdown renderer with release metadata, summary counts, severity
  and category tables, and issue-code rows.
- Added CLI coverage, library coverage, and a golden Markdown fixture.
- Updated README, generator docs, fixture-refresh docs, release checklist,
  changelog, and roadmap bookkeeping for the new output.

This release does not change stable issue codes, issue severity semantics, the
JSON issue-code catalog shape, or `verity explain` output. The Markdown output
is a human-readable publishing format layered on top of the existing catalog.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.74.0"
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
verity generate issue-code-catalog --out build/issue-code-catalog.json
verity generate issue-code-catalog --format markdown --out build/issue-code-catalog.md
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release. After the tag
workflow completes, use the post-tag release verification checklist to record
release asset hashes, skipped PyPI state, downloaded wheel smoke results,
public GitHub tag install results, closed issue and milestone evidence, and
agent context refresh evidence.
