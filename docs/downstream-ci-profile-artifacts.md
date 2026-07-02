# Downstream CI Profile Artifacts

Downstream repositories should preserve enough VeritySpec output to explain why
a product-contract check passed or failed. This guidance is for repositories
using release, regulated, public API, or internal-tool profiles in GitHub
Actions.

This document adds guidance only. It does not change the reusable workflow,
the CLI, report generators, or profile enforcement behavior.

## Goal

Profile artifacts should make CI review reproducible:

- validation, lint, readiness, and doctor output should be preserved
- graph output should be available for relationship review
- generated report artifacts should be kept with the profile that produced them
- failed runs should still upload available artifacts
- artifact names should identify the workspace, profile, run, and attempt
- private paths, secrets, tokens, customer data, and unpublished product data
  should not be uploaded accidentally

Artifact bundles are evidence of declared VeritySpec checks. They do not prove
external commercial, legal, privacy-law, marketplace, app-store,
platform-certification, pricing-approval, support-SLA, security-certification,
or production-readiness approval.

## Recommended Layout

Use one output directory per workspace and profile:

```text
build/verity-artifacts/
  release/
    validation.json
    lint.json
    readiness.json
    doctor.json
    graph.json
    validation-report.json
    evidence-report.json
  regulated/
    validation.json
    lint.json
    readiness.json
    doctor.json
    graph.json
    validation-report.json
    security-report.json
    accessibility-report.json
    compliance-matrix.json
    evidence-report.json
  public-api/
    validation.json
    lint.json
    readiness.json
    doctor.json
    graph.json
    validation-report.json
    openapi.json
    schema-bundle.json
  internal-tool/
    validation.json
    lint.json
    readiness.json
    doctor.json
    graph.json
    validation-report.json
```

For monorepos, include the workspace slug:

```text
build/verity-artifacts/services-catalog/release/
build/verity-artifacts/apps-admin/internal-tool/
```

## Common Commands

For each profile, preserve machine-readable command output:

```bash
WORKSPACE=specs/product
PROFILE=release
OUT_DIR=build/verity-artifacts/release
mkdir -p "$OUT_DIR"

verity validate "$WORKSPACE" --profile "$PROFILE" --format json > "$OUT_DIR/validation.json"
verity lint "$WORKSPACE" --profile "$PROFILE" --strict --format json > "$OUT_DIR/lint.json"
verity readiness "$WORKSPACE" --profile "$PROFILE" --strict --format json > "$OUT_DIR/readiness.json"
verity doctor "$WORKSPACE" --profile "$PROFILE" --format json > "$OUT_DIR/doctor.json"
verity graph "$WORKSPACE" --format json > "$OUT_DIR/graph.json"
verity generate validation-report "$WORKSPACE" --out "$OUT_DIR/validation-report.json"
```

For `internal-tool`, omit `--strict` if warnings should remain advisory:

```bash
PROFILE=internal-tool
verity lint "$WORKSPACE" --profile "$PROFILE" --format json > "$OUT_DIR/lint.json"
verity readiness "$WORKSPACE" --profile "$PROFILE" --format json > "$OUT_DIR/readiness.json"
```

Validate JSON artifacts before upload:

```bash
python -m json.tool "$OUT_DIR/validation.json" >/dev/null
python -m json.tool "$OUT_DIR/lint.json" >/dev/null
python -m json.tool "$OUT_DIR/readiness.json" >/dev/null
python -m json.tool "$OUT_DIR/doctor.json" >/dev/null
python -m json.tool "$OUT_DIR/graph.json" >/dev/null
python -m json.tool "$OUT_DIR/validation-report.json" >/dev/null
```

## Profile Bundles

### Release

Release artifacts should preserve the core gate:

- validation JSON
- lint JSON
- readiness JSON
- doctor JSON
- graph JSON
- validation report JSON
- evidence report JSON when `verity.pack.evidence` is loaded
- lifecycle-readiness report JSON when product-delivery, mobile, or liveops
  lifecycle surfaces are part of the release gate

Useful optional commands:

```bash
verity generate evidence-report "$WORKSPACE" --out "$OUT_DIR/evidence-report.json"
verity generate lifecycle-readiness-report "$WORKSPACE" --out "$OUT_DIR/lifecycle-readiness-report.json"
```

### Regulated

Regulated artifacts should preserve governance evidence for security,
accessibility, and compliance review:

- validation JSON
- lint JSON
- readiness JSON
- doctor JSON
- graph JSON
- validation report JSON
- security report JSON when `verity.pack.security` is loaded
- accessibility report JSON when `verity.pack.accessibility` is loaded
- compliance matrix JSON when `verity.pack.compliance` is loaded
- evidence report JSON when `verity.pack.evidence` is loaded

Useful optional commands:

```bash
verity generate security-report "$WORKSPACE" --out "$OUT_DIR/security-report.json"
verity generate accessibility-report "$WORKSPACE" --out "$OUT_DIR/accessibility-report.json"
verity generate compliance-matrix "$WORKSPACE" --out "$OUT_DIR/compliance-matrix.json"
verity generate evidence-report "$WORKSPACE" --out "$OUT_DIR/evidence-report.json"
```

### Public API

Public API artifacts should preserve the public contract surface:

- validation JSON
- lint JSON
- readiness JSON
- doctor JSON
- graph JSON
- validation report JSON
- OpenAPI JSON
- schema bundle JSON

Useful optional commands:

```bash
verity generate openapi "$WORKSPACE" --out "$OUT_DIR/openapi.json"
verity generate schema-bundle "$WORKSPACE" --out "$OUT_DIR/schema-bundle.json"
```

### Internal Tool

Internal-tool artifacts should preserve advisory output without making early
internal warnings disappear:

- validation JSON
- lint JSON without `--strict`
- readiness JSON without `--strict`
- doctor JSON
- graph JSON
- validation report JSON

Use the artifact review to decide whether warnings should become issue work,
not as evidence that the internal tool is production-ready.

## GitHub Actions Upload Example

When a workflow has a profile matrix, upload artifacts even when the contract
gate fails:

```yaml
- name: Generate VeritySpec artifact bundle
  if: always()
  shell: bash
  env:
    WORKSPACE: ${{ matrix.workspace }}
    PROFILE: ${{ matrix.profile }}
    STRICT: ${{ matrix.strict }}
  run: |
    safe_workspace="${WORKSPACE//\//-}"
    out_dir="build/verity-artifacts/${safe_workspace}/${PROFILE:-strict}"
    mkdir -p "$out_dir"

    strict_args=()
    if [ "$STRICT" = "true" ]; then
      strict_args+=(--strict)
    fi

    verity validate "$WORKSPACE" --profile "$PROFILE" --format json > "$out_dir/validation.json" || true
    verity lint "$WORKSPACE" --profile "$PROFILE" "${strict_args[@]}" --format json > "$out_dir/lint.json" || true
    verity readiness "$WORKSPACE" --profile "$PROFILE" "${strict_args[@]}" --format json > "$out_dir/readiness.json" || true
    verity doctor "$WORKSPACE" --profile "$PROFILE" --format json > "$out_dir/doctor.json" || true
    verity graph "$WORKSPACE" --format json > "$out_dir/graph.json" || true
    verity generate validation-report "$WORKSPACE" --out "$out_dir/validation-report.json" || true

- name: Upload VeritySpec artifact bundle
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: verity-${{ matrix.name }}-${{ github.run_id }}-${{ github.run_attempt }}
    path: build/verity-artifacts/**
    if-no-files-found: warn
    retention-days: 14
```

Keep enforcement and artifact generation as separate steps. The enforcement
step should decide pass/fail. The artifact step should collect whatever output
is available for review.

## Retention And Naming

Use artifact names that include:

- profile name
- workspace or matrix name
- GitHub run ID
- GitHub run attempt

Recommended retention:

- pull request runs: 7 to 14 days
- release-branch runs: 30 to 90 days
- regulated or audited releases: match the repository's evidence-retention
  policy

Long retention does not turn CI artifacts into legal, compliance, privacy, or
certification approval evidence. It only preserves the VeritySpec check output.

## Redaction And Privacy

Before uploading artifacts:

- keep secrets out of VeritySpec records
- avoid uploading generated files that include tokens, customer data, private
  URLs, unpublished commercial terms, or local machine paths
- prefer relative workspace paths in reports
- avoid broad `build/**` uploads when other tools write private output there
- use `build/verity-artifacts/**` for VeritySpec output

If a downstream repository handles sensitive data, add a repository-specific
redaction step before `actions/upload-artifact`.

## CI Fallback

If GitHub Actions cannot run because of billing, credits, quota, runner
availability, or another platform issue, run equivalent commands locally and
preserve the generated artifact directory as local evidence. Record the local
commands and artifact paths in the pull request or release notes.

The standard local fallback should include:

```bash
PYTHONPATH=src python3 -m verityspec validate "$WORKSPACE" --profile "$PROFILE" --format json > "$OUT_DIR/validation.json"
PYTHONPATH=src python3 -m verityspec lint "$WORKSPACE" --profile "$PROFILE" --format json > "$OUT_DIR/lint.json"
PYTHONPATH=src python3 -m verityspec readiness "$WORKSPACE" --profile "$PROFILE" --format json > "$OUT_DIR/readiness.json"
PYTHONPATH=src python3 -m verityspec doctor "$WORKSPACE" --profile "$PROFILE" --format json > "$OUT_DIR/doctor.json"
PYTHONPATH=src python3 -m verityspec graph "$WORKSPACE" --format json > "$OUT_DIR/graph.json"
```

## Organization Follow-Up

This guidance may be useful as a reusable organization pattern after it proves
itself in downstream repositories. If sibling repositories adopt this bundle
shape, propose a follow-up write-back to `Jason-Furr/organization-patterns`.
