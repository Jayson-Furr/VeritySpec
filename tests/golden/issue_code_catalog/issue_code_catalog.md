# VeritySpec Issue Code Catalog

- Generated: `<generatedAt>`
- VeritySpec: `<verityVersion>`
- Source: `verity explain`

> This catalog summarizes stable VeritySpec issue-code metadata for documentation sites, CI diagnostics, and agent workflows. The JSON output remains the machine-readable contract.

## Summary

| Metric | Count |
|---|---:|
| Issue codes | 63 |
| Categories | 14 |
| Severities | 2 |

## Severities

| Severity | Count |
|---|---:|
| warning | 16 |
| error | 47 |

## Categories

| Category | Count |
|---|---:|
| accessibility | 1 |
| compliance | 1 |
| dependency | 12 |
| deployment | 1 |
| graph | 2 |
| lint | 3 |
| pack | 19 |
| profile | 2 |
| readiness | 3 |
| record | 4 |
| reference | 4 |
| schema | 2 |
| security | 2 |
| workspace | 7 |

## Issue Codes

| Code | Category | Severity | Title | Description | Resolution |
|---|---|---|---|---|---|
| accessibility.claim.critical_unverified | accessibility | warning | Critical accessibility claim not verified | A critical accessibility claim is release-relevant but is not marked as verified. | Set coverage to verified and provide a verification method other than not-verified with evidence. |
| compliance.mapping.reviewed_unverified | compliance | warning | Reviewed compliance mapping not verified | A compliance mapping marked reviewed is missing verification evidence. | Use a verification method other than not-verified and provide evidence, or lower coverage until review is complete. |
| dependency.alias.duplicate | dependency | error | Duplicate workspace dependency alias | A workspace declares the same dependency alias more than once. | Give each dependency declaration a unique alias. |
| dependency.alias.unknown | dependency | error | Unknown workspace dependency alias | A reference uses an alias-qualified dependency target, but the workspace does not declare that dependency alias. | Declare the dependency alias in verityspec.json or update the reference target. |
| dependency.declaration.invalid | dependency | error | Invalid workspace dependency declaration | A workspace dependency declaration is missing required local dependency fields or uses an invalid shape. | Declare dependency id, alias, source, optional version, and readonly mode using the supported local dependency shape. |
| dependency.exports.invalid | dependency | error | Invalid dependency exports | A dependency workspace exports list is not an array of record ID strings. | Set exports to an array of record IDs that the dependency intentionally exposes to consumers. |
| dependency.id.mismatch | dependency | error | Workspace dependency ID mismatch | A declared dependency ID does not match the workspace loaded from the dependency source path. | Update the dependency id or source path so the declaration and loaded workspace agree. |
| dependency.load.failed | dependency | error | Workspace dependency failed to load | A declared local workspace dependency could not be parsed or loaded. | Fix the dependency workspace files or point source at a valid VeritySpec workspace. |
| dependency.mode.unsupported | dependency | error | Unsupported workspace dependency mode | A workspace dependency declares a mode other than readonly. | Set dependency mode to readonly for the local dependency prototype. |
| dependency.reference.missing | dependency | error | Missing workspace dependency reference target | A dependency-qualified reference points to a record ID that does not exist in the dependency workspace. | Create and export the target record in the dependency workspace or update the reference. |
| dependency.reference.not_exported | dependency | error | Workspace dependency reference not exported | A dependency-qualified reference points to a record that exists but is not exported by the dependency workspace. | Add the target record ID to the dependency workspace exports list or reference an exported record. |
| dependency.source.missing | dependency | error | Missing workspace dependency source | A local workspace dependency source path does not exist. | Create the dependency workspace at the source path or update the dependency declaration. |
| dependency.version.missing | dependency | error | Missing workspace dependency version | A dependency declaration includes a version constraint but the loaded dependency workspace has no version. | Add a version to the dependency workspace manifest or remove the version constraint. |
| dependency.version.unsatisfied | dependency | error | Workspace dependency version unsatisfied | A loaded dependency workspace version does not satisfy the consuming workspace dependency constraint. | Update the dependency source or version constraint so they agree. |
| deployment.target.production_release_controls_missing | deployment | warning | Production deployment controls missing | A production deployment target is missing required release approval, rollback, health-check, security, observability, compliance, or release evidence links. | Require release approval, declare a rollback plan, add a production healthCheckUrl, and link security controls, observability dashboards, compliance mappings, and release evidence records. |
| graph.cycle | graph | warning | Reference cycle | A directed reference path loops back to an earlier record. | Break the cycle by removing or changing one reference edge. |
| graph.orphan | graph | warning | Orphan record | A non-product, non-schema record has no incoming or outgoing graph references. | Reference the record from a product or another record, or remove it. |
| lint.description.missing | lint | warning | Missing description | A record should include a useful human-readable description. | Add a non-empty description field. |
| lint.owner.placeholder | lint | warning | Placeholder owner | The owner field uses a placeholder value. | Set owner to the team, person, or system responsible for the record. |
| lint.status.draft | lint | warning | Draft record | Draft records are not considered release-ready. | Move the record to review or ready once the contract is accepted. |
| pack.discovery.invalid | pack | error | Pack discovery failed | A local or installed pack source could not be resolved into a valid pack manifest. | Check local pack paths and installed `verityspec.packs` entry points, then rerun `verity pack list`. |
| pack.external.builtin_collision | pack | error | External pack shadows built-in pack | A local pack path declares a pack ID that is reserved by a built-in pack. | Use a distinct external pack ID. Built-in pack IDs cannot be shadowed by local pack paths. |
| pack.external.duplicate_id | pack | error | Duplicate external pack ID | Multiple local pack paths declare the same pack ID. | Remove the duplicate local path or ensure each external pack has a distinct ID. |
| pack.external.manifest_id_missing | pack | error | External pack manifest missing ID | A local pack manifest does not declare a string `id` field. | Add a string `id` field to the pack manifest. |
| pack.external.manifest_invalid | pack | error | External pack manifest invalid | A local pack manifest could not be parsed as a JSON object. | Fix the local pack's `pack.json` file and rerun `verity pack doctor`. |
| pack.external.missing_manifest | pack | error | External pack manifest missing | A local pack path does not contain a `pack.json` manifest. | Point the path at a pack directory or `pack.json` file. |
| pack.external.overrides_installed | pack | warning | External pack overrides installed pack | A local pack path supplies the same pack ID as an installed package entry point and takes precedence. | Confirm that the local override is intentional, or remove the local path to use the installed pack. |
| pack.external.path_invalid | pack | error | External pack path invalid | A local pack path could not be resolved. | Fix the local path or remove the invalid `packPaths`, `--pack-path`, or `verity pack --path` entry. |
| pack.installed.builtin_collision | pack | error | Installed pack shadows built-in pack | An installed pack entry point declares a pack ID that is reserved by a built-in pack. | Rename or uninstall the package. Built-in pack IDs cannot be shadowed by installed packs. |
| pack.installed.duplicate_id | pack | error | Duplicate installed pack ID | Multiple installed entry points declare the same pack ID. | Keep only one installed distribution for that pack ID, or make the duplicate package expose a distinct ID. |
| pack.installed.entry_point_load_failed | pack | error | Installed pack entry point failed | An installed `verityspec.packs` entry point could not be imported or called. | Fix or uninstall the package exposing the failing entry point, then rerun `verity pack doctor`. |
| pack.installed.entry_point_name_mismatch | pack | error | Installed pack entry point name mismatch | An installed entry-point name does not match the resolved pack manifest ID. | Update the package entry point name so it exactly matches the manifest `id`. |
| pack.installed.manifest_id_missing | pack | error | Installed pack manifest missing ID | An installed pack manifest does not declare a string `id` field. | Fix the installed package manifest so it declares a string `id`. |
| pack.installed.manifest_invalid | pack | error | Installed pack manifest invalid | An installed pack manifest could not be parsed as a JSON object. | Fix or uninstall the package exposing the invalid manifest. |
| pack.installed.missing_manifest | pack | error | Installed pack manifest missing | An installed pack entry point resolved to a path without a `pack.json` manifest. | Fix the entry point so it returns a pack directory or `pack.json` path. |
| pack.mirror.id_mismatch | pack | error | Pack mirror ID mismatch | An official-extension mirror pack declares a different manifest ID than the source pack being compared. | Preserve the existing pack ID in the mirror package. Packaging splits must not rename pack IDs or record kinds. |
| pack.mirror.invalid | pack | error | Pack mirror invalid | A pack mirror path could not be loaded as a pack directory or `pack.json` manifest. | Point `--mirror` at a valid pack directory or manifest and rerun `verity pack compare`. |
| pack.mirror.surface_mismatch | pack | error | Pack mirror surface mismatch | An official-extension mirror differs from the source pack in schemas, readiness gates, reference rules, generator metadata, or manifest fields. | Update the mirror fixture or package so its public pack contract matches the source pack, or document and migrate the intentional change before detaching the pack. |
| pack.unknown | pack | error | Unknown pack | The requested pack ID is not available. | Run `verity pack list` and use one of the listed pack IDs. |
| profile.required_pack | profile | error | Required profile pack missing | The selected product-contract profile requires a pack that is not loaded by the workspace. | Add the required pack to the workspace, or use a profile that matches the workspace scope. |
| profile.required_record_kind | profile | error | Required profile record kind missing | The selected product-contract profile requires at least one record of a specific kind. | Add the required record kind, or use a profile that matches the workspace scope. |
| readiness.min_items | readiness | warning | Readiness list too small | A readiness gate requires a list field to contain at least a minimum number of items. | Add the required items to the record. |
| readiness.required | readiness | warning | Readiness field missing | A readiness gate requires a field that is missing or empty. | Add the required field or adjust the relevant pack readiness gate. |
| readiness.validation_runner.scanner_refs_required | readiness | warning | Validation runner scanner references required | A scanner-backed engine validation runner is missing scanner references. | Add scannerRefs for scanner-backed runners, or use runnerType device-smoke when the runner validates a built artifact or device runtime directly. |
| record.id.duplicate | record | error | Duplicate record ID | Two records use the same ID. | Give each record a unique stable ID. |
| record.id.missing | record | error | Missing record ID | A record does not define a string ID. | Add an id field that matches the VeritySpec ID pattern. |
| record.kind.missing | record | error | Missing record kind | A record does not define a string kind. | Add a kind field declared by one of the loaded packs. |
| record.kind.unknown | record | error | Unknown record kind | A record uses a kind not declared by the loaded packs. | Load the pack that declares the kind or change the record kind. |
| reference.deprecated | reference | warning | Deprecated reference | A record references another record marked deprecated. | Move the reference to the replacement record or acknowledge it before release. |
| reference.disallowed | reference | error | Disallowed reference relationship | The source kind, relationship, and target kind combination is not allowed by loaded pack rules. | Use an allowed relationship or add a pack rule that explicitly permits it. |
| reference.missing | reference | error | Missing reference target | A reference points to a record ID that does not exist in the workspace. | Create the target record or update the reference target. |
| reference.removed | reference | error | Removed reference target | A record references another record marked removed. | Remove the reference or point it to an active replacement. |
| schema.unused | schema | warning | Unused schema | A schema record has no incoming references. | Reference the schema from a record or remove it. |
| schema.validation | schema | error | Schema validation failure | A record does not satisfy the JSON Schema for its kind. | Update the record to match its pack schema. |
| security.control.critical_unverified | security | warning | Critical security control not verified | A critical security control is release-relevant but is not marked as verified. | Set coverage to verified and provide a verification method other than not-verified with evidence. |
| security.control.evidence_stale | security | warning | Security verification evidence stale | A security control declares a review cadence, but its verification date is missing or older than that cadence. | Update verification.lastVerified after reviewing the evidence, or adjust verification.reviewCadenceDays to the accepted cadence. |
| workspace.dependencies.invalid | workspace | error | Invalid workspace dependencies | The workspace dependencies field is not an array. | Set dependencies to an array of local dependency declarations or remove the field. |
| workspace.packPaths.invalid | workspace | error | Invalid workspace pack paths | A v0.2.0 workspace declares packPaths, but it is not an array of strings. | Set packPaths to an array of local pack paths, or [] when no external packs are used. |
| workspace.packPaths.missing | workspace | error | Missing workspace pack paths | A v0.2.0 workspace must declare packPaths explicitly. | Run `verity migrate` or add `"packPaths": []` to verityspec.json. |
| workspace.version.future | workspace | error | Future workspace version | The workspace declares a specVersion newer than this VeritySpec CLI supports. | Install a newer VeritySpec CLI before validating or migrating the workspace. |
| workspace.version.invalid | workspace | error | Invalid workspace version | The workspace specVersion does not use vMAJOR.MINOR.PATCH format. | Set specVersion to a supported value such as v0.2.0. |
| workspace.version.missing | workspace | error | Missing workspace version | The workspace config does not declare a specVersion. | Run `verity migrate` or add a supported specVersion to verityspec.json. |
| workspace.version.unsupported | workspace | error | Unsupported workspace version | The workspace declares a version this VeritySpec CLI does not support. | Run `verity migrate` to produce a supported workspace version. |
