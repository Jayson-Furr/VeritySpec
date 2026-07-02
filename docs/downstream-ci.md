# Downstream CI

Downstream repositories can run VeritySpec as a product-contract gate.

## Maintained Templates

Copy one of the maintained templates into a downstream repository as
`.github/workflows/product-contract.yml`:

- `templates/github-actions/product-contract-reusable.yml`: calls the reusable
  VeritySpec workflow.
- `templates/github-actions/product-contract-with-local-packs.yml`: calls the
  reusable workflow with local external pack paths.
- `templates/github-actions/product-contract-monorepo.yml`: calls the reusable
  workflow once per workspace in a monorepo matrix, with shared local packs.
- `templates/github-actions/product-contract-profiles.yml`: calls the reusable
  workflow once per profile-specific workspace for release, regulated, public
  API, and internal-tool enforcement examples.
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
        run: pip install "verityspec @ git+https://github.com/Jason-Furr/verity-spec.git@v0.68.0"

      - name: Check product contract
        shell: bash
        run: |
          mkdir -p build
          annotation_args=()
          if verity validate --help | grep -q -- "--github-annotations"; then
            annotation_args+=(--github-annotations)
          fi

          verity --version
          verity validate . "${annotation_args[@]}"
          verity lint . --strict "${annotation_args[@]}"
          verity readiness . --strict "${annotation_args[@]}"
          verity doctor . --format json > build/verity-doctor.json
          verity generate validation-report . --out build/verity-validation-report.json
          python -m json.tool build/verity-doctor.json >/dev/null
          python -m json.tool build/verity-validation-report.json >/dev/null
```

After PyPI publishing is enabled, replace the install step with:

```bash
pip install verityspec
```

The annotation feature detection keeps the template compatible with older
installed releases while automatically enabling GitHub Actions annotations for
validation, lint, and readiness issues when the installed `verity` supports
`--github-annotations`.

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
    uses: Jason-Furr/verity-spec/.github/workflows/product-contract.yml@v0.68.0
    with:
      workspace: .
```

For local external packs:

```yaml
jobs:
  verity:
    uses: Jason-Furr/verity-spec/.github/workflows/product-contract.yml@v0.68.0
    with:
      workspace: specs/product
      pack-paths: packs/features packs/security
```

For an enforcement profile:

```yaml
jobs:
  verity:
    uses: Jason-Furr/verity-spec/.github/workflows/product-contract.yml@v0.68.0
    with:
      workspace: specs/product
      profile: release
```

The reusable workflow passes `profile` to `verity validate`, `verity lint`,
`verity readiness`, and `verity doctor`. If no profile is supplied, the
workflow keeps the existing strict product-contract behavior.

When using `profile: internal-tool`, set `strict: false` if warnings should
remain advisory:

```yaml
jobs:
  verity:
    uses: Jason-Furr/verity-spec/.github/workflows/product-contract.yml@v0.68.0
    with:
      workspace: specs/internal-tool
      profile: internal-tool
      strict: false
```

## Monorepo Workflow

For a monorepo with several VeritySpec workspaces and shared local packs, copy
`templates/github-actions/product-contract-monorepo.yml` and replace the matrix
entries with the downstream repository's workspace paths:

```yaml
name: Product Contract Monorepo

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  verity:
    name: ${{ matrix.workspace }}
    strategy:
      fail-fast: false
      matrix:
        include:
          - workspace: services/catalog/specs
            pack_paths: packs/shared packs/catalog
            strict: true
          - workspace: apps/admin/specs
            pack_paths: packs/shared packs/admin
            strict: true
          - workspace: packages/cli/specs
            pack_paths: packs/shared packs/cli
            strict: true
    uses: Jason-Furr/verity-spec/.github/workflows/product-contract.yml@v0.68.0
    with:
      workspace: ${{ matrix.workspace }}
      pack-paths: ${{ matrix.pack_paths }}
      strict: ${{ matrix.strict }}
```

Use `packs/shared` for pack contracts reused by multiple workspaces, and add
workspace-specific pack paths only where those product surfaces need them.

## Profile Matrix Workflow

For repositories that keep separate workspaces for different enforcement
postures, copy `templates/github-actions/product-contract-profiles.yml` and
replace the workspace paths:

```yaml
name: Product Contract Profiles

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  verity:
    name: ${{ matrix.name }}
    strategy:
      fail-fast: false
      matrix:
        include:
          - name: release
            workspace: specs/release
            profile: release
            strict: true
          - name: regulated
            workspace: specs/regulated
            profile: regulated
            strict: true
          - name: public-api
            workspace: specs/public-api
            profile: public-api
            strict: true
          - name: internal-tool
            workspace: specs/internal-tool
            profile: internal-tool
            strict: false
    uses: Jason-Furr/verity-spec/.github/workflows/product-contract.yml@v0.68.0
    with:
      workspace: ${{ matrix.workspace }}
      profile: ${{ matrix.profile }}
      strict: ${{ matrix.strict }}
```

Use `release` for normal shippable product-contract checks, `public-api` when
API contract coverage is required, `regulated` when governance pack coverage
is required, and `internal-tool` for early internal tooling where warnings
should guide work without failing the command.

These profiles are VeritySpec enforcement postures only. They do not prove
commercial, legal, privacy-law, marketplace, platform-certification,
app-store, store-review, pricing-approval, or support-SLA readiness.
