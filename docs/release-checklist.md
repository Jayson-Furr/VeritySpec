# Release Checklist

Use this checklist for public releases.

## Before Tagging

- Confirm `CHANGELOG.md` has an entry for the release.
- Confirm the version in `pyproject.toml` and `src/verityspec/__init__.py`
  matches the intended tag.
- Confirm the README release badge, latest-release text, install tag,
  workspace package-version text, and release-notes link match the intended
  tag.
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
verity validate tests/fixtures/custom_pack_workspace
verity validate tests/fixtures/generator_maturity
verity generate security-report examples/security --out build/security-report.json
verity generate observability-report examples/observability --out build/observability-report.json
verity generate accessibility-report examples/accessibility --out build/accessibility-report.json
verity generate compliance-matrix examples/compliance --out build/compliance-matrix.json
verity generate schema-bundle examples/accessibility --out build/accessibility-schema-bundle.json
verity generate schema-bundle examples/compliance --out build/compliance-schema-bundle.json
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
VERSION=v0.21.0
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
