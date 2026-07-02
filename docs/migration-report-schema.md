# Migration Report JSON Schema

VeritySpec publishes a machine-readable JSON Schema for workspace migration
reports at
[`docs/schemas/migration-report.schema.json`](schemas/migration-report.schema.json).

The schema describes reports emitted by:

```bash
verity migrate ./workspace --format json
verity migrate ./workspace --dry-run --format json
verity migrate ./workspace --report-out build/migration-report.json
```

This contract is intended for CI integrations, release review tooling,
workspace-format migration jobs, and downstream automation that need to inspect
workspace migration plans without relying on ad hoc field checks.

## Report Identity

Migration reports use:

```json
{
  "type": "verityspec_migration_report"
}
```

The `verity migrate --list --format json` capability report uses a different
type, `verityspec_migration_capabilities`, and is not covered by this schema.

PrismSpec importer reports are also separate. See
[PrismSpec Migration](prismspec-migration.md) for the historical importer
bridge and its `migration-report.json` fields.

## Stable Fields

Every migration report includes:

- `type`: report identity, always `verityspec_migration_report`.
- `source`: absolute workspace path or requested workspace path used for the
  migration.
- `targetVersion`: requested target workspace format version.
- `dryRun`: whether the report was produced without writing files.
- `changed`: whether the report contains planned/performed changes or a
  manifest repair.
- `blocked`: whether migration could not produce or run a migration path.
- `migrationPath`: ordered migration steps.
- `impactSummary`: workspace-format, record, pack, and generator impacts.
- `availableTargets`: reachable targets from the normalized source key.
- `changes`: manifest and record rewrite operations.
- `filesWritten`: files written by non-dry-run migrations.
- `manualFollowUp`: human follow-up items.

Successful non-blocked reports also include:

- `fromVersion`: source version value when available.
- `fromVersionKey`: normalized migration graph key, such as `legacy`,
  `v0.1.0`, or `v0.2.0`.
- `changeCount`: number of entries in `changes`.

Blocked reports may omit `fromVersion`, `fromVersionKey`, and `changeCount`
when the report is blocked before a workspace source version can be loaded or a
migration graph path can be resolved. Consumers should always check `blocked`
before assuming rewrite fields indicate a completed migration.

## Impact Summary

`impactSummary` is always an object with these categories:

```json
{
  "workspaceFormat": [],
  "records": [],
  "packs": [],
  "generators": []
}
```

These arrays aggregate the planned migration path and workspace-specific repair
changes. They are meant for CI summaries, pull request comments, and release
review. Additional future impact categories may be added without removing the
current four categories.

## Migration Path Steps

Each `migrationPath` item includes:

- `id`
- `fromVersion`
- `toVersion`
- `description`
- `impacts`

`impacts` uses the same category shape as `impactSummary`.

## Change Records

Each `changes` item includes:

- `path`: absolute file path affected by the migration.
- `action`: current values include `set`, `rename`, `remove`, `normalize`, and
  `upgrade`.
- `field`: manifest or record field affected by the change.
- `before`: JSON value before migration.
- `after`: JSON value after migration.
- `recordId`: optional record ID for record-level changes.

The schema permits additional fields so future migrations can add more precise
context without breaking existing consumers.

## Blocked Reports

Blocked migration reports keep the same report identity and summary fields.
They set:

```json
{
  "blocked": true,
  "changed": false
}
```

Common blocked cases include:

- unsupported target versions;
- future workspace versions that require a newer VeritySpec CLI;
- no available migration path from the source key to the requested target.

Consumers should treat `manualFollowUp` as the human-readable explanation and
should not write migrated files when `blocked` is true. The CLI returns a
non-zero exit code for blocked migration reports even when the JSON payload
itself validates against this schema.

## Compatibility Policy

The schema is additive. Existing documented fields should remain stable across
compatible VeritySpec releases. New optional fields or impact categories may be
added as migration behavior expands.

CI integrations should validate the report against the schema and then inspect
only the fields they need. For release gates, prefer explicit checks such as:

- fail when `blocked` is true;
- fail when `manualFollowUp` is non-empty;
- archive `impactSummary` in release evidence;
- require review when `changes` contains record-envelope rewrites.
