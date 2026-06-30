# Downstream CI

Downstream repositories can run VeritySpec as a product-contract gate.

## Maintained Templates

Copy one of the maintained templates into a downstream repository as
`.github/workflows/product-contract.yml`:

- `templates/github-actions/product-contract-reusable.yml`: calls the reusable
  VeritySpec workflow.
- `templates/github-actions/product-contract-with-local-packs.yml`: calls the
  reusable workflow with local external pack paths.
- `templates/github-actions/product-contract-direct.yml`: installs VeritySpec
  directly and runs the contract commands inline.

The templates are pinned to the current GitHub release tag so downstream
repositories get reproducible checks.

## Direct Install Workflow

```yaml
name: Product Contract

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  verity:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v7

      - name: Set up Python
        uses: actions/setup-python@v6
        with:
          python-version: "3.12"

      - name: Install VeritySpec
        run: pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.20.0"

      - name: Check product contract
        shell: bash
        run: |
          mkdir -p build
          verity --version
          verity validate .
          verity lint . --strict
          verity readiness . --strict
          verity doctor . --format json > build/verity-doctor.json
          verity generate validation-report . --out build/verity-validation-report.json
          python -m json.tool build/verity-doctor.json >/dev/null
          python -m json.tool build/verity-validation-report.json >/dev/null
```

After PyPI publishing is enabled, replace the install step with:

```bash
pip install verityspec
```

## Reusable Workflow

VeritySpec also exposes a reusable workflow:

```yaml
name: Product Contract

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  verity:
    uses: Jayson-Furr/VeritySpec/.github/workflows/product-contract.yml@v0.20.0
    with:
      workspace: .
```

For local external packs:

```yaml
jobs:
  verity:
    uses: Jayson-Furr/VeritySpec/.github/workflows/product-contract.yml@v0.20.0
    with:
      workspace: specs/product
      pack-paths: packs/features packs/security
```
