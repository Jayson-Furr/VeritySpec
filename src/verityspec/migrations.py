from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from .versions import (
    CURRENT_SPEC_VERSION,
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
    if normalized_target != CURRENT_SPEC_VERSION:
        return {
            "type": "verityspec_migration_report",
            "source": str(Path(path).resolve()),
            "targetVersion": target_version,
            "dryRun": dry_run,
            "changed": False,
            "blocked": True,
            "changes": [],
            "filesWritten": [],
            "manualFollowUp": [f"Target version '{target_version}' is not supported by this VeritySpec release."],
        }

    requested = Path(path).resolve()
    workspace = load_workspace(requested)
    source_version = workspace.config.get("specVersion") or workspace.config.get("version")
    source_classification = classify_spec_version(source_version)
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
            "manualFollowUp": [
                "This workspace declares a future specVersion. Install a newer VeritySpec CLI before migrating."
            ],
        }

    config_path, migrated_config = migrate_workspace_config(workspace, normalized_target, changes)
    record_paths = sorted({record.path for record in workspace.records})
    migrated_payloads: list[tuple[Path, Any]] = []
    for record_path in record_paths:
        record_changes_before = len(changes)
        migrated_payload, payload_changed = migrate_payload_records(record_path, changes)
        if payload_changed or len(changes) != record_changes_before:
            migrated_payloads.append((record_path, migrated_payload))

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
        "targetVersion": normalized_target,
        "dryRun": dry_run,
        "changed": bool(changes) or config_changed,
        "blocked": False,
        "changes": changes,
        "changeCount": len(changes),
        "filesWritten": files_written,
        "manualFollowUp": manual_follow_up,
    }


def migration_report_to_text(report: dict[str, Any]) -> str:
    lines = [
        f"Migration target: {report.get('targetVersion')}",
        f"Source: {report.get('source')}",
        f"Dry run: {str(report.get('dryRun', False)).lower()}",
    ]
    if report.get("blocked"):
        lines.append("Blocked: true")
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
