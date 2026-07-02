# Release Checklist

Use this checklist for public releases.

## Before Tagging

- Confirm `CHANGELOG.md` has an entry for the release.
- Confirm the version in `pyproject.toml` and `src/verityspec/__init__.py`
  matches the intended tag.
- Confirm the README release badge, latest-release text, install tag,
  workspace package-version text, and release-notes link match the intended
  tag.
- Confirm maintained downstream CI templates, including the monorepo template,
  profile-aware template, reference the intended release tag.
- Confirm `docs/pypi.md` GitHub fallback install tag matches the intended tag.
- Review [fixture refresh guidance](fixture-refresh.md) when release-version
  fixture updates or generator-output drift are part of the release.
- Confirm `tests/test_release_integrity.py` passes so package metadata,
  README release surfaces, release notes, downstream pins, release checklist
  examples, and evidence fixtures match the intended tag.
- Run local checks:

```bash
python -m pip install --upgrade build twine
python -m unittest discover -s tests -v
verity pack validate
verity pack doctor --format json > build/pack-doctor.json
verity pack compare verity.pack.unity --mirror tests/fixtures/official_extension_mirrors/verityspec-pack-unity/pack --format json > build/unity-pack-mirror.json
verity validate examples/basic
verity lint examples/basic --strict
verity readiness examples/basic --strict
verity validate examples/security
verity lint examples/security --strict
verity readiness examples/security --strict
verity validate examples/observability
verity lint examples/observability --strict
verity readiness examples/observability --strict
verity validate examples/accessibility
verity lint examples/accessibility --strict
verity readiness examples/accessibility --strict
verity validate examples/compliance
verity lint examples/compliance --strict
verity readiness examples/compliance --strict
verity validate examples/deployment
verity lint examples/deployment --strict
verity readiness examples/deployment --strict
verity validate examples/game-core
verity lint examples/game-core --strict
verity readiness examples/game-core --strict
verity validate examples/game-assets
verity lint examples/game-assets --strict
verity readiness examples/game-assets --strict
verity validate examples/unity
verity lint examples/unity --strict
verity readiness examples/unity --strict
verity graph examples/unity --format json > build/unity-graph.json
verity validate examples/godot
verity lint examples/godot --strict
verity readiness examples/godot --strict
verity graph examples/godot --format json > build/godot-graph.json
verity validate examples/unreal
verity lint examples/unreal --strict
verity readiness examples/unreal --strict
verity graph examples/unreal --format json > build/unreal-graph.json
verity validate examples/gameplay
verity lint examples/gameplay --strict
verity readiness examples/gameplay --strict
verity validate examples/content
verity lint examples/content --strict
verity readiness examples/content --strict
verity validate examples/economy
verity lint examples/economy --strict
verity readiness examples/economy --strict
verity validate examples/progression
verity lint examples/progression --strict
verity readiness examples/progression --strict
verity graph examples/progression --format json > build/progression-graph.json
verity validate examples/product-delivery
verity lint examples/product-delivery --strict
verity readiness examples/product-delivery --strict
verity graph examples/product-delivery --format json > build/product-delivery-graph.json
verity generate agent-context examples/product-delivery --record agent-context.exporter.implementation_bundle --format markdown --out build/agent-context.md
verity generate decision-index examples/product-delivery --out build/decision-index.json
verity generate decision-index examples/product-delivery --format markdown --out build/decision-index.md
verity validate examples/portfolio
verity lint examples/portfolio --strict
verity readiness examples/portfolio --strict
verity graph examples/portfolio --format json > build/portfolio-graph.json
verity validate examples/mobile
verity lint examples/mobile --strict
verity readiness examples/mobile --strict
verity graph examples/mobile --format json > build/mobile-graph.json
verity validate examples/liveops
verity lint examples/liveops --strict
verity readiness examples/liveops --strict
verity graph examples/liveops --format json > build/liveops-graph.json
verity validate examples/evidence
verity lint examples/evidence --strict
verity readiness examples/evidence --strict
verity graph examples/evidence --format json > build/evidence-graph.json
verity validate tests/fixtures/custom_pack_workspace
verity validate tests/fixtures/generator_maturity
verity validate tests/fixtures/cross_pack_coverage
verity lint tests/fixtures/cross_pack_coverage --strict
verity readiness tests/fixtures/cross_pack_coverage --strict
verity validate tests/fixtures/product_impact/baseline
verity lint tests/fixtures/product_impact/baseline --strict
verity readiness tests/fixtures/product_impact/baseline --strict
verity validate tests/fixtures/product_impact/current
verity lint tests/fixtures/product_impact/current --strict
verity readiness tests/fixtures/product_impact/current --strict
verity pack validate verity.pack.features --path docs/fixtures/pack-scaffold/packs/features
verity validate docs/fixtures/pack-scaffold/workspace
verity lint docs/fixtures/pack-scaffold/workspace --strict
verity readiness docs/fixtures/pack-scaffold/workspace --strict
verity generate security-report examples/security --out build/security-report.json
verity generate security-report examples/security --format markdown --out build/security-report.md
verity generate observability-report examples/observability --out build/observability-report.json
verity generate accessibility-report examples/accessibility --out build/accessibility-report.json
verity generate compliance-matrix examples/compliance --out build/compliance-matrix.json
verity generate deployment-report examples/deployment --out build/deployment-report.json
verity generate evidence-report examples/evidence --out build/evidence-report.json
verity generate lifecycle-readiness-report examples/lifecycle-readiness --out build/lifecycle-readiness-report.json
verity generate schema-bundle examples/game-core --out build/game-core-schema-bundle.json
verity generate schema-bundle examples/game-assets --out build/game-assets-schema-bundle.json
verity generate schema-bundle examples/unity --out build/unity-schema-bundle.json
verity generate schema-bundle examples/godot --out build/godot-schema-bundle.json
verity generate schema-bundle examples/unreal --out build/unreal-schema-bundle.json
verity generate schema-bundle examples/gameplay --out build/gameplay-schema-bundle.json
verity generate schema-bundle examples/content --out build/content-schema-bundle.json
verity generate schema-bundle examples/economy --out build/economy-schema-bundle.json
verity generate schema-bundle examples/progression --out build/progression-schema-bundle.json
verity generate schema-bundle examples/product-delivery --out build/product-delivery-schema-bundle.json
verity generate schema-bundle examples/portfolio --out build/portfolio-schema-bundle.json
verity generate schema-bundle examples/mobile --out build/mobile-schema-bundle.json
verity generate schema-bundle examples/liveops --out build/liveops-schema-bundle.json
verity generate schema-bundle examples/evidence --out build/evidence-schema-bundle.json
verity generate coverage-dashboard tests/fixtures/cross_pack_coverage --out build/coverage-dashboard.json
verity generate coverage-dashboard tests/fixtures/cross_pack_coverage --format markdown --out build/coverage-dashboard.md
verity generate pack-capability-index tests/fixtures/custom_pack_workspace --out build/pack-capability-index.json
verity generate schema-bundle docs/fixtures/pack-scaffold/workspace --out build/pack-scaffold-schema-bundle.json
verity generate pack-capability-index docs/fixtures/pack-scaffold/workspace --out build/pack-scaffold-capability-index.json
verity generate product-impact tests/fixtures/product_impact/baseline tests/fixtures/product_impact/current --out build/product-impact.json
verity generate agent-context examples/product-delivery --record agent-context.exporter.implementation_bundle --format markdown --out build/agent-context.md
verity generate decision-index examples/product-delivery --out build/decision-index.json
verity generate decision-index examples/product-delivery --format markdown --out build/decision-index.md
verity generate issue-code-catalog --out build/issue-code-catalog.json
verity generate issue-code-catalog --format markdown --out build/issue-code-catalog.md
verity generate schema-bundle examples/accessibility --out build/accessibility-schema-bundle.json
verity generate schema-bundle examples/compliance --out build/compliance-schema-bundle.json
verity generate schema-bundle examples/deployment --out build/deployment-schema-bundle.json
python -m json.tool build/unity-graph.json >/dev/null
python -m json.tool build/godot-graph.json >/dev/null
python -m json.tool build/unreal-graph.json >/dev/null
python -m json.tool build/product-delivery-graph.json >/dev/null
python -m json.tool build/portfolio-graph.json >/dev/null
python -m json.tool build/mobile-graph.json >/dev/null
python -m json.tool build/liveops-graph.json >/dev/null
python -m json.tool build/progression-graph.json >/dev/null
python -m json.tool build/evidence-graph.json >/dev/null
python -m json.tool build/evidence-report.json >/dev/null
python -m json.tool build/lifecycle-readiness-report.json >/dev/null
python -m json.tool build/decision-index.json >/dev/null
python -m json.tool build/issue-code-catalog.json >/dev/null
python -m build
twine check dist/*
```

Also smoke-test the built wheel locally before tagging:

```bash
python -m venv /tmp/verityspec-wheel
/tmp/verityspec-wheel/bin/python -m pip install --upgrade pip
/tmp/verityspec-wheel/bin/pip install dist/*.whl
/tmp/verityspec-wheel/bin/verity --version
/tmp/verityspec-wheel/bin/verity pack validate
/tmp/verityspec-wheel/bin/verity validate examples/basic
/tmp/verityspec-wheel/bin/verity validate examples/deployment
/tmp/verityspec-wheel/bin/verity validate examples/game-core
/tmp/verityspec-wheel/bin/verity validate examples/game-assets
/tmp/verityspec-wheel/bin/verity validate examples/unity
/tmp/verityspec-wheel/bin/verity validate examples/godot
/tmp/verityspec-wheel/bin/verity validate examples/unreal
/tmp/verityspec-wheel/bin/verity validate examples/gameplay
/tmp/verityspec-wheel/bin/verity validate examples/content
/tmp/verityspec-wheel/bin/verity validate examples/economy
/tmp/verityspec-wheel/bin/verity validate examples/progression
/tmp/verityspec-wheel/bin/verity validate examples/product-delivery
/tmp/verityspec-wheel/bin/verity generate agent-context examples/product-delivery --record agent-context.exporter.implementation_bundle --format markdown --out build/agent-context-wheel.md
/tmp/verityspec-wheel/bin/verity generate decision-index examples/product-delivery --out build/decision-index-wheel.json
/tmp/verityspec-wheel/bin/verity generate decision-index examples/product-delivery --format markdown --out build/decision-index-wheel.md
/tmp/verityspec-wheel/bin/verity validate examples/portfolio
/tmp/verityspec-wheel/bin/verity validate examples/mobile
/tmp/verityspec-wheel/bin/verity validate examples/liveops
/tmp/verityspec-wheel/bin/verity validate examples/evidence
```

If `twine` is installed but the console script is not on `PATH`, run
`python -m twine check dist/*` and record that in the PR verification notes.

## Release PR

- Create a release-prep issue in the release milestone.
- Work from a `release/<version>` branch.
- Include the local release verification commands in the PR body.
- Wait for all GitHub Actions checks to pass before merging.
- After merge, verify local `main` and the `main` CI run before tagging.

## Tag

```bash
VERSION=v0.81.0
git tag -a "$VERSION" -m "VeritySpec $VERSION"
git push origin "$VERSION"
```

Pushing a `v*` tag runs the release workflow, builds the distributions, checks
them, smoke-tests the wheel, and creates a GitHub release with the artifacts.

After the release workflow finishes:

- Verify the GitHub release exists for the tag.
- Verify the wheel and source distribution are attached.
- Confirm PyPI publishing was not triggered unless explicitly requested.
- Close the release milestone.
- Refresh agent context from `AGENTS.md`, `git status`, and the latest commit
  before continuing with the next sprint.
- Record the full post-tag evidence with the
  [post-tag release verification](post-tag-release-verification.md) checklist.

## PyPI

PyPI publishing is prepared through GitHub Actions trusted publishing. Before
using it:

- Create the `verityspec` project on PyPI or claim the name.
- Configure PyPI trusted publishing for `Jason-Furr/verity-spec`.
- Confirm the GitHub `pypi` environment exists.
- Run the `Release` workflow manually with `publish_pypi=true`.
