# VeritySpec v0.76.0 Release Notes

VeritySpec v0.76.0 adds `verity generate decision-index` so
product-delivery workspaces can turn structured `decision.record` records into
reviewable ADR and governance indexes.

## Highlights

- Added `verity generate decision-index WORKSPACE` with JSON output.
- Added Markdown output for human-readable ADR and governance review.
- Summarized decisions by decision status, record lifecycle status, decision
  type, and owner.
- Included graph links, supersession metadata, references, and index-gap
  summaries for accepted decisions without `decidedAt`, proposed decisions,
  superseded decisions, and decisions with no graph links.
- Advertised the generator in `verity.pack.product-delivery` metadata and
  pack validation.
- Added CLI coverage, library coverage, golden JSON and Markdown fixtures,
  README updates, generator docs, ADR docs, product-delivery docs,
  fixture-refresh guidance, release checklist updates, changelog, and roadmap
  bookkeeping.

This release does not approve decisions, replace ADR prose, or make legal,
commercial, privacy, marketplace, support-SLA, platform-certification, or
implementation-readiness claims. The decision index is an executable reporting
artifact over product-delivery records.

## Installation

```bash
pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.76.0"
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
verity validate examples/product-delivery
verity lint examples/product-delivery --strict
verity readiness examples/product-delivery --strict
verity generate decision-index examples/product-delivery --out build/decision-index.json
verity generate decision-index examples/product-delivery --format markdown --out build/decision-index.md
python -m json.tool build/decision-index.json
python -m build
python -m twine check dist/*
```

The release workflow also builds distributions, checks them, smoke-tests the
wheel, uploads artifacts, and creates the GitHub release. After the tag
workflow completes, use the post-tag release verification checklist to record
release asset hashes, skipped PyPI state, downloaded wheel smoke results,
public GitHub tag install results, closed issue and milestone evidence, and
agent context refresh evidence.
