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
  reference the intended release tag.
- Confirm `docs/pypi.md` GitHub fallback install tag matches the intended tag.
- Run local checks:

```bash
python -m pip install --upgrade build twine
python -m unittest discover -s tests -v
verity pack validate
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
verity validate examples/product-delivery
verity lint examples/product-delivery --strict
verity readiness examples/product-delivery --strict
verity graph examples/product-delivery --format json > build/product-delivery-graph.json
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
verity generate observability-report examples/observability --out build/observability-report.json
verity generate accessibility-report examples/accessibility --out build/accessibility-report.json
verity generate compliance-matrix examples/compliance --out build/compliance-matrix.json
verity generate deployment-report examples/deployment --out build/deployment-report.json
verity generate schema-bundle examples/game-core --out build/game-core-schema-bundle.json
verity generate schema-bundle examples/game-assets --out build/game-assets-schema-bundle.json
verity generate schema-bundle examples/unity --out build/unity-schema-bundle.json
verity generate schema-bundle examples/godot --out build/godot-schema-bundle.json
verity generate schema-bundle examples/unreal --out build/unreal-schema-bundle.json
verity generate schema-bundle examples/gameplay --out build/gameplay-schema-bundle.json
verity generate schema-bundle examples/content --out build/content-schema-bundle.json
verity generate schema-bundle examples/economy --out build/economy-schema-bundle.json
verity generate schema-bundle examples/product-delivery --out build/product-delivery-schema-bundle.json
verity generate coverage-dashboard tests/fixtures/cross_pack_coverage --out build/coverage-dashboard.json
verity generate pack-capability-index tests/fixtures/custom_pack_workspace --out build/pack-capability-index.json
verity generate schema-bundle docs/fixtures/pack-scaffold/workspace --out build/pack-scaffold-schema-bundle.json
verity generate pack-capability-index docs/fixtures/pack-scaffold/workspace --out build/pack-scaffold-capability-index.json
verity generate product-impact tests/fixtures/product_impact/baseline tests/fixtures/product_impact/current --out build/product-impact.json
verity generate schema-bundle examples/accessibility --out build/accessibility-schema-bundle.json
verity generate schema-bundle examples/compliance --out build/compliance-schema-bundle.json
verity generate schema-bundle examples/deployment --out build/deployment-schema-bundle.json
python -m json.tool build/unity-graph.json >/dev/null
python -m json.tool build/godot-graph.json >/dev/null
python -m json.tool build/unreal-graph.json >/dev/null
python -m json.tool build/product-delivery-graph.json >/dev/null
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
/tmp/verityspec-wheel/bin/verity validate examples/product-delivery
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
VERSION=v0.42.0
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

## PyPI

PyPI publishing is prepared through GitHub Actions trusted publishing. Before
using it:

- Create the `verityspec` project on PyPI or claim the name.
- Configure PyPI trusted publishing for `Jayson-Furr/VeritySpec`.
- Confirm the GitHub `pypi` environment exists.
- Run the `Release` workflow manually with `publish_pypi=true`.
