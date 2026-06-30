# PrismSpec Migration

VeritySpec includes a PrismSpec importer for bridging historical PrismSpec
v1.0.0 catalog folders into a VeritySpec workspace.

The importer is intentionally conservative. VeritySpec is not wire-compatible
with PrismSpec, so import produces a converted workspace plus a migration report
instead of pretending every concept maps cleanly.

```bash
verity import prismspec ../PrismSpec/v1.0.0 --out ./verity-workspace
verity validate ./verity-workspace
verity lint ./verity-workspace --strict
verity readiness ./verity-workspace --strict
```

## Output

The importer writes:

- `verityspec.json`
- `records/*.json`
- `migration-report.json`

The generated workspace includes the built-in packs needed by converted record
kinds. For example, imported endpoints add `verity.pack.api`, imported commands
add `verity.pack.cli`, and imported telemetry events add `verity.pack.events`.

## Report Fields

`migration-report.json` includes:

- `compatibility`: always `not_wire_compatible`
- `convertedRecordCount`
- `skippedRecordCount`
- `unsupportedFieldCount`
- `convertedRecords`
- `skippedRecords`
- `unsupportedFields`
- `defaultsApplied`
- `missingReferences`
- `deprecatedConcepts`
- `recommendedPackMappings`
- `manualFollowUp`

## Current Mappings

| PrismSpec type | VeritySpec output |
|---|---|
| `product` | `product` |
| `endpoint` | `api.endpoint` |
| `command` | `cli.command` |
| `telemetry_event` | `schema.object` plus `event.message` |

Endpoint records receive a default `200` response if PrismSpec did not provide
responses. Command records receive default success and failure exit codes.
Telemetry events receive a generic payload schema. These defaults are reported
in `defaultsApplied` and should be reviewed manually.

## Skipped Concepts

Some PrismSpec concepts are intentionally skipped until corresponding VeritySpec
packs exist or stabilize. The current report identifies recommended future pack
mappings for concepts such as assets, UI controls, profile compositions, user
flows, and service flows.

Skipped concepts are not data loss hidden by the tool. They are called out in
the report so teams can decide whether to model them manually, wait for a pack,
or build a custom pack.

## CI Usage

For repositories that keep PrismSpec fixtures or migration snapshots, add an
import smoke test:

```bash
verity import prismspec tests/fixtures/prismspec_sample --out build/prismspec-import
python -m json.tool build/prismspec-import/migration-report.json >/dev/null
verity validate build/prismspec-import --format json > build/prismspec-import-validation.json
python -m json.tool build/prismspec-import-validation.json >/dev/null
```

