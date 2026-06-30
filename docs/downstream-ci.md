# Downstream CI

Downstream repositories can run VeritySpec as a product-contract gate.

## Copy-Paste Workflow

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
        run: pip install "verityspec @ git+https://github.com/Jayson-Furr/VeritySpec.git@v0.6.0"

      - name: Check product contract
        run: |
          verity validate .
          verity lint . --strict
          verity readiness . --strict
          verity generate validation-report . --out build/verity-validation-report.json
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
    uses: Jayson-Furr/VeritySpec/.github/workflows/product-contract.yml@v0.6.0
    with:
      workspace: .
```

For local external packs:

```yaml
jobs:
  verity:
    uses: Jayson-Furr/VeritySpec/.github/workflows/product-contract.yml@v0.6.0
    with:
      workspace: specs/product
      pack-paths: packs/features packs/security
```
