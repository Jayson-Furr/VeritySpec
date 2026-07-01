from __future__ import annotations

import copy
import json
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .versions import (
    CURRENT_SPEC_VERSION,
    SUPPORTED_SPEC_VERSIONS,
    classify_spec_version,
    normalize_spec_version,
)
from .workspace import DEFAULT_PACKS, DEFAULT_RECORD_GLOBS, Workspace, load_json, load_workspace


KIND_ALIASES = {
    "product": "product",
    "schema": "schema.object",
    "schema.object": "schema.object",
    "endpoint": "api.endpoint",
    "api.endpoint": "api.endpoint",
    "command": "cli.command",
    "cli.command": "cli.command",
    "event": "event.message",
    "event.message": "event.message",
    "telemetry_event": "event.message",
}

STATUS_ALIASES = {
    "approved": "ready",
    "active": "ready",
    "locked": "ready",
    "stable": "ready",
    "review": "review",
    "draft": "draft",
    "deprecated": "deprecated",
    "removed": "removed",
}

LEGACY_SOURCE_VERSION = "legacy"


@dataclass(frozen=True)
class MigrationStep:
    id: str
    from_version: str
    to_version: str
    description: str
    impacts: dict[str, list[str]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "fromVersion": self.from_version,
            "toVersion": self.to_version,
            "description": self.description,
            "impacts": clone_json(self.impacts),
        }


MIGRATION_STEPS = [
    MigrationStep(
        id="legacy-to-v0.1.0",
        from_version=LEGACY_SOURCE_VERSION,
        to_version="v0.1.0",
        description="Normalize legacy VeritySpec workspace and record shapes into v0.1.0.",
        impacts={
            "workspaceFormat": [
                "Renames legacy workspace version fields to specVersion.",
                "Adds missing workspace records globs when absent.",
            ],
            "records": [
                "Renames known legacy record type fields to kind.",
                "Renames displayName to name.",
                "Normalizes known legacy statuses to ready.",
                "Adds placeholder owner, name, status, or product version fields when required.",
            ],
            "packs": [
                "Adds the default built-in pack set when packs are missing.",
            ],
            "generators": [
                "Generator availability may change when default built-in packs are added.",
            ],
        },
    ),
    MigrationStep(
        id="v0.1.0-to-v0.2.0",
        from_version="v0.1.0",
        to_version="v0.2.0",
        description="Promote workspaces to v0.2.0 by making external pack paths explicit.",
        impacts={
            "workspaceFormat": [
                "Upgrades specVersion to v0.2.0.",
                "Adds explicit packPaths when absent or repairs invalid packPaths values.",
            ],
            "records": [],
            "packs": [
                "Makes local external pack paths explicit with packPaths.",
            ],
            "generators": [
                "External pack-provided generator availability becomes tied to explicit packPaths.",
            ],
        },
    ),
]

IMPACT_CATEGORIES = ("workspaceFormat", "records", "packs", "generators")


def empty_impact_summary() -> dict[str, list[str]]:
    return {category: [] for category in IMPACT_CATEGORIES}


def add_impact(summary: dict[str, list[str]], category: str, message: str) -> None:
    if category not in summary:
        summary[category] = []
    if message not in summary[category]:
        summary[category].append(message)


def summarize_migration_impacts(
    steps: list[MigrationStep],
    changes: list[dict[str, Any]] | None = None,
) -> dict[str, list[str]]:
    summary = empty_impact_summary()
    for step in steps:
        for category in IMPACT_CATEGORIES:
            for message in step.impacts.get(category, []):
                add_impact(summary, category, message)

    for change in changes or []:
        field = change.get("field")
        if field in {"specVersion", "version", "version -> specVersion", "workspace", "records", "packPaths"}:
            add_impact(
                summary,
                "workspaceFormat",
                "Workspace manifest fields are rewritten or repaired.",
            )
        if field in {"packs", "packPaths"}:
            add_impact(
                summary,
                "packs",
                "Resolved pack configuration is rewritten or repaired.",
            )
            add_impact(
                summary,
                "generators",
                "Generator availability may change when resolved packs or pack paths change.",
            )
        if "recordId" in change or field in {
            "type -> kind",
            "type",
            "displayName -> name",
            "displayName",
            "name",
            "status",
            "owner",
        }:
            add_impact(
                summary,
                "records",
                "Record envelope fields are rewritten or repaired.",
            )

    return summary


def supported_version_entries() -> list[dict[str, str]]:
    return [
        {
            "id": version.id,
            "status": version.status,
            "description": version.description,
        }
        for version in sorted(SUPPORTED_SPEC_VERSIONS.values(), key=lambda item: item.id)
    ]


def migration_capabilities() -> dict[str, Any]:
    return {
        "type": "verityspec_migration_capabilities",
        "currentVersion": CURRENT_SPEC_VERSION,
        "legacySource": LEGACY_SOURCE_VERSION,
        "supportedVersions": supported_version_entries(),
        "steps": [step.to_dict() for step in MIGRATION_STEPS],
    }


def impact_summary_to_text_lines(
    impact_summary: dict[str, Any],
    *,
    base_indent: str = "",
) -> list[str]:
    lines: list[str] = []
    has_impacts = False
    for category, label in [
        ("workspaceFormat", "Workspace format"),
        ("records", "Records"),
        ("packs", "Packs"),
        ("generators", "Generators"),
    ]:
        impacts = impact_summary.get(category, [])
        if not impacts:
            continue
        has_impacts = True
        lines.append(f"{base_indent}{label}:")
        lines.extend(f"{base_indent}  - {item}" for item in impacts)
    if not has_impacts:
        lines.append(f"{base_indent}none")
    return lines


def migration_capabilities_to_text(capabilities: dict[str, Any]) -> str:
    lines = [
        f"Current workspace version: {capabilities.get('currentVersion')}",
        "Supported versions:",
    ]
    for version in capabilities.get("supportedVersions", []):
        lines.append(f"  {version.get('id')} ({version.get('status')}): {version.get('description')}")
    lines.append("Migration steps:")
    for step in capabilities.get("steps", []):
        lines.append(
            f"  {step.get('fromVersion')} -> {step.get('toVersion')} ({step.get('id')}): "
            f"{step.get('description')}"
        )
        impacts = step.get("impacts")
        if isinstance(impacts, dict):
            lines.append("    Impacts:")
            lines.extend(impact_summary_to_text_lines(impacts, base_indent="      "))
    return "\n".join(lines)


def migration_source_key(source_version: object) -> str:
    normalized = normalize_spec_version(source_version)
    if normalized in SUPPORTED_SPEC_VERSIONS:
        return normalized
    return LEGACY_SOURCE_VERSION


def reachable_migration_targets(source_key: str) -> list[str]:
    targets: set[str] = set()
    queue: deque[str] = deque([source_key])
    visited: set[str] = {source_key}
    while queue:
        current = queue.popleft()
        for step in MIGRATION_STEPS:
            if step.from_version != current:
                continue
            targets.add(step.to_version)
            if step.to_version not in visited:
                visited.add(step.to_version)
                queue.append(step.to_version)
    return sorted(targets)


def plan_migration_path(source_key: str, target_version: str) -> list[MigrationStep] | None:
    if source_key == target_version:
        return []

    queue: deque[tuple[str, list[MigrationStep]]] = deque([(source_key, [])])
    visited: set[str] = {source_key}
    while queue:
        current, path = queue.popleft()
        for step in MIGRATION_STEPS:
            if step.from_version != current:
                continue
            next_path = path + [step]
            if step.to_version == target_version:
                return next_path
            if step.to_version not in visited:
                visited.add(step.to_version)
                queue.append((step.to_version, next_path))
    return None


def clone_json(value: Any) -> Any:
    return json.loads(json.dumps(value))


def add_change(
    changes: list[dict[str, Any]],
    path: Path,
    action: str,
    field: str,
    before: Any,
    after: Any,
    record_id: str | None = None,
) -> None:
    change = {
        "path": str(path),
        "action": action,
        "field": field,
        "before": before,
        "after": after,
    }
    if record_id:
        change["recordId"] = record_id
    changes.append(change)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def migrate_workspace_config(
    workspace: Workspace,
    target_version: str,
    changes: list[dict[str, Any]],
) -> tuple[Path, dict[str, Any]]:
    config_path = workspace.config_path or workspace.base_path / "verityspec.json"
    config = copy.deepcopy(workspace.config if isinstance(workspace.config, dict) else {})

    if not isinstance(config.get("workspace"), str) or not config.get("workspace"):
        before = config.get("workspace")
        config["workspace"] = workspace.base_path.name
        add_change(changes, config_path, "set", "workspace", before, config["workspace"])

    legacy_version = config.get("version")
    if "specVersion" not in config and legacy_version is not None:
        normalized = normalize_spec_version(legacy_version) or target_version
        config["specVersion"] = normalized
        add_change(changes, config_path, "rename", "version -> specVersion", legacy_version, normalized)
        del config["version"]
        add_change(changes, config_path, "remove", "version", legacy_version, None)

    if "specVersion" not in config:
        config["specVersion"] = target_version
        add_change(changes, config_path, "set", "specVersion", None, target_version)
    else:
        normalized = normalize_spec_version(config.get("specVersion"))
        if normalized and normalized != config.get("specVersion"):
            before = config.get("specVersion")
            config["specVersion"] = normalized
            add_change(changes, config_path, "normalize", "specVersion", before, normalized)
        elif classify_spec_version(config.get("specVersion")) in {"invalid", "unsupported"}:
            before = config.get("specVersion")
            config["specVersion"] = target_version
            add_change(changes, config_path, "set", "specVersion", before, target_version)

    if not isinstance(config.get("packs"), list):
        before = config.get("packs")
        config["packs"] = DEFAULT_PACKS
        add_change(changes, config_path, "set", "packs", before, DEFAULT_PACKS)

    if not isinstance(config.get("records"), list):
        before = config.get("records")
        config["records"] = DEFAULT_RECORD_GLOBS
        add_change(changes, config_path, "set", "records", before, DEFAULT_RECORD_GLOBS)

    return config_path, config


def migrate_workspace_config_to_v0_2_0(
    config_path: Path,
    config: dict[str, Any],
    changes: list[dict[str, Any]],
) -> dict[str, Any]:
    migrated = copy.deepcopy(config)

    if migrated.get("specVersion") != "v0.2.0":
        before = migrated.get("specVersion")
        migrated["specVersion"] = "v0.2.0"
        add_change(changes, config_path, "upgrade", "specVersion", before, "v0.2.0")

    pack_paths = migrated.get("packPaths")
    if "packPaths" not in migrated:
        migrated["packPaths"] = []
        add_change(changes, config_path, "set", "packPaths", None, [])
    elif not isinstance(pack_paths, list) or not all(isinstance(item, str) for item in pack_paths):
        migrated["packPaths"] = []
        add_change(changes, config_path, "set", "packPaths", pack_paths, [])

    return migrated


def migrate_record_data(record: dict[str, Any], path: Path, changes: list[dict[str, Any]]) -> dict[str, Any]:
    data = copy.deepcopy(record)
    record_id = data.get("id") if isinstance(data.get("id"), str) else None

    source_type = data.get("type")
    if "kind" not in data and isinstance(source_type, str):
        target_kind = KIND_ALIASES.get(source_type)
        if target_kind:
            data["kind"] = target_kind
            add_change(changes, path, "rename", "type -> kind", source_type, target_kind, record_id)
            del data["type"]
            add_change(changes, path, "remove", "type", source_type, None, record_id)

    display_name = data.get("displayName")
    if "name" not in data and isinstance(display_name, str) and display_name:
        data["name"] = display_name
        add_change(changes, path, "rename", "displayName -> name", display_name, display_name, record_id)
    if "displayName" in data:
        before = data["displayName"]
        del data["displayName"]
        add_change(changes, path, "remove", "displayName", before, None, record_id)

    if "name" not in data or not isinstance(data.get("name"), str) or not data.get("name"):
        before = data.get("name")
        data["name"] = record_id or "Imported Record"
        add_change(changes, path, "set", "name", before, data["name"], record_id)

    status = data.get("status")
    if isinstance(status, str) and status in STATUS_ALIASES and STATUS_ALIASES[status] != status:
        data["status"] = STATUS_ALIASES[status]
        add_change(changes, path, "normalize", "status", status, data["status"], record_id)
    elif "status" not in data:
        data["status"] = "draft"
        add_change(changes, path, "set", "status", None, "draft", record_id)

    if "owner" not in data or not isinstance(data.get("owner"), str) or not data.get("owner"):
        before = data.get("owner")
        data["owner"] = "unknown"
        add_change(changes, path, "set", "owner", before, "unknown", record_id)

    if data.get("kind") == "product" and ("version" not in data or not data.get("version")):
        before = data.get("version")
        data["version"] = "0.1.0"
        add_change(changes, path, "set", "version", before, "0.1.0", record_id)

    return data


def migrate_payload_records(path: Path, changes: list[dict[str, Any]]) -> tuple[Any, bool]:
    payload = load_json(path)
    migrated = clone_json(payload)

    if isinstance(migrated, dict) and isinstance(migrated.get("records"), list):
        for index, item in enumerate(migrated["records"]):
            if isinstance(item, dict):
                migrated["records"][index] = migrate_record_data(item, path, changes)
    elif isinstance(migrated, list):
        for index, item in enumerate(migrated):
            if isinstance(item, dict):
                migrated[index] = migrate_record_data(item, path, changes)
    elif isinstance(migrated, dict):
        migrated = migrate_record_data(migrated, path, changes)

    return migrated, migrated != payload


def migrate_workspace(
    path: str | Path,
    target_version: str = CURRENT_SPEC_VERSION,
    dry_run: bool = False,
) -> dict[str, Any]:
    normalized_target = normalize_spec_version(target_version)
    if normalized_target not in SUPPORTED_SPEC_VERSIONS:
        return {
            "type": "verityspec_migration_report",
            "source": str(Path(path).resolve()),
            "targetVersion": target_version,
            "dryRun": dry_run,
            "changed": False,
            "blocked": True,
            "changes": [],
            "filesWritten": [],
            "migrationPath": [],
            "impactSummary": empty_impact_summary(),
            "availableTargets": [],
            "manualFollowUp": [
                f"Target version '{target_version}' is not supported by this VeritySpec release.",
                f"Supported target versions: {', '.join(sorted(SUPPORTED_SPEC_VERSIONS))}.",
            ],
        }

    requested = Path(path).resolve()
    workspace = load_workspace(requested)
    declared_spec_version = workspace.config.get("specVersion")
    legacy_version = workspace.config.get("version")
    source_version = declared_spec_version if declared_spec_version is not None else legacy_version
    source_classification = classify_spec_version(declared_spec_version)
    source_key = migration_source_key(declared_spec_version)
    changes: list[dict[str, Any]] = []
    files_written: list[str] = []
    manual_follow_up: list[str] = []

    if source_classification == "future":
        return {
            "type": "verityspec_migration_report",
            "source": str(workspace.base_path),
            "fromVersion": source_version,
            "targetVersion": normalized_target,
            "dryRun": dry_run,
            "changed": False,
            "blocked": True,
            "changes": [],
            "filesWritten": [],
            "migrationPath": [],
            "impactSummary": empty_impact_summary(),
            "availableTargets": [],
            "manualFollowUp": [
                "This workspace declares a future specVersion. Install a newer VeritySpec CLI before migrating."
            ],
        }

    migration_path = plan_migration_path(source_key, normalized_target)
    available_targets = reachable_migration_targets(source_key)
    if migration_path is None:
        return {
            "type": "verityspec_migration_report",
            "source": str(workspace.base_path),
            "fromVersion": source_version,
            "fromVersionKey": source_key,
            "targetVersion": normalized_target,
            "dryRun": dry_run,
            "changed": False,
            "blocked": True,
            "changes": [],
            "filesWritten": [],
            "migrationPath": [],
            "impactSummary": empty_impact_summary(),
            "availableTargets": available_targets,
            "manualFollowUp": [
                f"No migration path is available from {source_key} to {normalized_target}."
            ],
        }

    config_path = workspace.config_path or workspace.base_path / "verityspec.json"
    migrated_config = copy.deepcopy(workspace.config if isinstance(workspace.config, dict) else {})
    migrated_payloads: list[tuple[Path, Any]] = []

    for step in migration_path:
        if step.id == "legacy-to-v0.1.0":
            config_path, migrated_config = migrate_workspace_config(workspace, step.to_version, changes)
            record_paths = sorted({record.path for record in workspace.records})
            for record_path in record_paths:
                record_changes_before = len(changes)
                migrated_payload, payload_changed = migrate_payload_records(record_path, changes)
                if payload_changed or len(changes) != record_changes_before:
                    migrated_payloads.append((record_path, migrated_payload))
        elif step.id == "v0.1.0-to-v0.2.0":
            migrated_config = migrate_workspace_config_to_v0_2_0(config_path, migrated_config, changes)

    if source_key == normalized_target and normalized_target == "v0.2.0":
        migrated_config = migrate_workspace_config_to_v0_2_0(config_path, migrated_config, changes)

    config_changed = workspace.config_path is None or migrated_config != workspace.config
    if not dry_run:
        if config_changed:
            write_json(config_path, migrated_config)
            files_written.append(str(config_path))
        for record_path, migrated_payload in migrated_payloads:
            write_json(record_path, migrated_payload)
            files_written.append(str(record_path))

    if any(change["field"] == "owner" and change["after"] == "unknown" for change in changes):
        manual_follow_up.append("Replace placeholder owner values introduced during migration.")
    if any(change["field"] == "status" and change["after"] == "draft" for change in changes):
        manual_follow_up.append("Review draft statuses introduced during migration.")

    return {
        "type": "verityspec_migration_report",
        "source": str(workspace.base_path),
        "fromVersion": source_version,
        "fromVersionKey": source_key,
        "targetVersion": normalized_target,
        "dryRun": dry_run,
        "changed": bool(changes) or config_changed,
        "blocked": False,
        "migrationPath": [step.to_dict() for step in migration_path],
        "impactSummary": summarize_migration_impacts(migration_path, changes),
        "availableTargets": available_targets,
        "changes": changes,
        "changeCount": len(changes),
        "filesWritten": files_written,
        "manualFollowUp": manual_follow_up,
    }


def migration_report_to_text(report: dict[str, Any]) -> str:
    lines = [
        f"Source version: {report.get('fromVersion') or report.get('fromVersionKey')}",
        f"Migration target: {report.get('targetVersion')}",
        f"Source: {report.get('source')}",
        f"Dry run: {str(report.get('dryRun', False)).lower()}",
    ]
    if report.get("blocked"):
        lines.append("Blocked: true")
    path = report.get("migrationPath", [])
    if path:
        lines.append("Migration path:")
        for step in path:
            lines.append(
                f"  {step.get('fromVersion')} -> {step.get('toVersion')} ({step.get('id')})"
            )
    else:
        lines.append("Migration path: none")
    impact_summary = report.get("impactSummary", {})
    if isinstance(impact_summary, dict):
        lines.append("Impact summary:")
        lines.extend(impact_summary_to_text_lines(impact_summary, base_indent="  "))
    lines.append(f"Changes: {report.get('changeCount', len(report.get('changes', [])))}")
    files = report.get("filesWritten", [])
    lines.append(f"Files written: {len(files)}")
    for path in files:
        lines.append(f"  {path}")
    follow_up = report.get("manualFollowUp", [])
    if follow_up:
        lines.append("Manual follow-up:")
        lines.extend(f"  {item}" for item in follow_up)
    return "\n".join(lines)
