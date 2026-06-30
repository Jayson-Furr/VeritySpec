from __future__ import annotations

import json
from typing import Any

from .workspace import Workspace


SEVERITY_LEVELS = ("info", "warning", "error")
SEVERITY_RANK = {severity: index for index, severity in enumerate(SEVERITY_LEVELS)}
LOW_RISK_RECORD_FIELDS = {
    "description",
    "name",
    "notes",
    "summary",
    "tags",
}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def changed_fields(old_data: dict[str, Any], new_data: dict[str, Any]) -> list[str]:
    fields = []
    for field in sorted(set(old_data) | set(new_data)):
        if canonical_json(old_data.get(field)) != canonical_json(new_data.get(field)):
            fields.append(field)
    return fields


def severity_max(*severities: str) -> str:
    return max(severities, key=lambda severity: SEVERITY_RANK.get(severity, 0))


def change_entry(
    change_type: str,
    severity: str,
    breaking: bool,
    reasons: list[str],
    **extra: Any,
) -> dict[str, Any]:
    return {
        "type": change_type,
        "severity": severity,
        "breaking": breaking,
        "reasons": reasons,
        **extra,
    }


def schema_required_values(schema: Any) -> set[str]:
    if not isinstance(schema, dict):
        return set()
    required = schema.get("required")
    if not isinstance(required, list):
        return set()
    return {item for item in required if isinstance(item, str)}


def schema_properties(schema: Any) -> dict[str, Any]:
    if not isinstance(schema, dict):
        return {}
    properties = schema.get("properties")
    return properties if isinstance(properties, dict) else {}


def schema_enum_values(schema: Any) -> set[str]:
    if not isinstance(schema, dict):
        return set()
    enum = schema.get("enum")
    if not isinstance(enum, list):
        return set()
    return {canonical_json(item) for item in enum}


def schema_breaking_reasons(
    old_schema: Any,
    new_schema: Any,
    path: str = "jsonSchema",
) -> list[str]:
    reasons: list[str] = []
    if not isinstance(old_schema, dict) or not isinstance(new_schema, dict):
        return reasons

    old_type = old_schema.get("type")
    new_type = new_schema.get("type")
    if old_type != new_type and old_type is not None and new_type is not None:
        reasons.append(f"{path}.type changed from {old_type!r} to {new_type!r}.")

    removed_required = sorted(schema_required_values(old_schema) - schema_required_values(new_schema))
    for field in removed_required:
        reasons.append(f"{path}.required removed {field!r}.")

    old_properties = schema_properties(old_schema)
    new_properties = schema_properties(new_schema)
    for field in sorted(set(old_properties) - set(new_properties)):
        reasons.append(f"{path}.properties removed {field!r}.")

    removed_enum_values = sorted(schema_enum_values(old_schema) - schema_enum_values(new_schema))
    if removed_enum_values:
        reasons.append(f"{path}.enum removed {len(removed_enum_values)} value(s).")

    for field in sorted(set(old_properties) & set(new_properties)):
        reasons.extend(
            schema_breaking_reasons(
                old_properties[field],
                new_properties[field],
                f"{path}.properties.{field}",
            )
        )
    return reasons


def response_statuses(record: dict[str, Any]) -> set[str]:
    statuses: set[str] = set()
    responses = record.get("responses")
    if not isinstance(responses, list):
        return statuses
    for response in responses:
        if not isinstance(response, dict):
            continue
        status = response.get("statusCode")
        if isinstance(status, (str, int)):
            statuses.add(str(status))
    return statuses


def classify_record_change(record_id: str, old_data: dict[str, Any], new_data: dict[str, Any]) -> dict[str, Any]:
    fields = changed_fields(old_data, new_data)
    reasons: list[str] = []
    severity = "info" if set(fields) <= LOW_RISK_RECORD_FIELDS else "warning"
    breaking = False

    old_kind = old_data.get("kind")
    new_kind = new_data.get("kind")
    if old_kind != new_kind:
        severity = "error"
        breaking = True
        reasons.append(f"Record kind changed from {old_kind!r} to {new_kind!r}.")

    if new_data.get("status") == "removed" and old_data.get("status") != "removed":
        severity = "error"
        breaking = True
        reasons.append("Record status changed to removed.")
    elif new_data.get("status") == "deprecated" and old_data.get("status") != "deprecated":
        severity = severity_max(severity, "warning")
        reasons.append("Record status changed to deprecated.")

    if old_kind == "api.endpoint" and new_kind == "api.endpoint":
        if old_data.get("method") != new_data.get("method"):
            severity = "error"
            breaking = True
            reasons.append(
                f"API endpoint method changed from {old_data.get('method')!r} to {new_data.get('method')!r}."
            )
        if old_data.get("path") != new_data.get("path"):
            severity = "error"
            breaking = True
            reasons.append(
                f"API endpoint path changed from {old_data.get('path')!r} to {new_data.get('path')!r}."
            )
        removed_statuses = sorted(response_statuses(old_data) - response_statuses(new_data))
        if removed_statuses:
            severity = "error"
            breaking = True
            reasons.append(f"API endpoint responses removed status code(s): {', '.join(removed_statuses)}.")

    if old_kind == "schema.object" and new_kind == "schema.object":
        schema_reasons = schema_breaking_reasons(old_data.get("jsonSchema"), new_data.get("jsonSchema"))
        if schema_reasons:
            severity = "error"
            breaking = True
            reasons.extend(schema_reasons)

    if not reasons:
        reasons.append("Record fields changed.")

    return change_entry(
        "record.changed",
        severity,
        breaking,
        reasons,
        recordId=record_id,
        kind=new_kind if isinstance(new_kind, str) else old_kind,
        fields=fields,
    )


def summarize_changes(changes: list[dict[str, Any]]) -> dict[str, Any]:
    by_severity = {severity: 0 for severity in SEVERITY_LEVELS}
    for change in changes:
        severity = change.get("severity")
        if isinstance(severity, str) and severity in by_severity:
            by_severity[severity] += 1
    breaking_changes = [change for change in changes if change.get("breaking")]
    return {
        "totalChanges": len(changes),
        "breakingChanges": len(breaking_changes),
        "hasBreakingChanges": bool(breaking_changes),
        "bySeverity": by_severity,
    }


def diff_workspaces(old: Workspace, new: Workspace) -> dict:
    old_by_id = {record.id: record.data for record in old.records if record.id}
    new_by_id = {record.id: record.data for record in new.records if record.id}

    old_ids = set(old_by_id)
    new_ids = set(new_by_id)

    changed = []
    changes: list[dict[str, Any]] = []

    if old.config.get("specVersion") != new.config.get("specVersion"):
        changes.append(
            change_entry(
                "workspace.version.changed",
                "warning",
                False,
                ["Workspace spec version changed."],
                old=old.config.get("specVersion"),
                new=new.config.get("specVersion"),
            )
        )

    for pack_id in sorted(set(new.pack_ids) - set(old.pack_ids)):
        changes.append(
            change_entry(
                "pack.added",
                "info",
                False,
                ["Pack added to workspace."],
                packId=pack_id,
            )
        )
    for pack_id in sorted(set(old.pack_ids) - set(new.pack_ids)):
        changes.append(
            change_entry(
                "pack.removed",
                "error",
                True,
                ["Pack removed from workspace."],
                packId=pack_id,
            )
        )

    for record_id in sorted(new_ids - old_ids):
        data = new_by_id[record_id]
        changes.append(
            change_entry(
                "record.added",
                "info",
                False,
                ["Record added to workspace."],
                recordId=record_id,
                kind=data.get("kind"),
            )
        )
    for record_id in sorted(old_ids - new_ids):
        data = old_by_id[record_id]
        changes.append(
            change_entry(
                "record.removed",
                "error",
                True,
                ["Record removed from workspace."],
                recordId=record_id,
                kind=data.get("kind"),
            )
        )

    for record_id in sorted(old_ids & new_ids):
        if canonical_json(old_by_id[record_id]) != canonical_json(new_by_id[record_id]):
            changed.append(record_id)
            changes.append(classify_record_change(record_id, old_by_id[record_id], new_by_id[record_id]))

    return {
        "versions": {
            "old": old.config.get("specVersion"),
            "new": new.config.get("specVersion"),
            "changed": old.config.get("specVersion") != new.config.get("specVersion"),
        },
        "packs": {
            "added": sorted(set(new.pack_ids) - set(old.pack_ids)),
            "removed": sorted(set(old.pack_ids) - set(new.pack_ids)),
        },
        "added": sorted(new_ids - old_ids),
        "removed": sorted(old_ids - new_ids),
        "changed": changed,
        "summary": summarize_changes(changes),
        "changes": changes,
    }


def change_label(change: dict[str, Any]) -> str:
    identifier = change.get("recordId") or change.get("packId") or change.get("type")
    reasons = change.get("reasons")
    reason = reasons[0] if isinstance(reasons, list) and reasons else "Changed."
    return f"  [{change.get('severity')}] {change.get('type')} {identifier} - {reason}"


def diff_to_text(diff: dict) -> str:
    summary = diff.get("summary", {})
    changes = diff.get("changes", [])
    breaking_changes = [change for change in changes if change.get("breaking")]
    lines = [
        f"Spec version: {diff.get('versions', {}).get('old')} -> {diff.get('versions', {}).get('new')}",
        "Summary:",
        f"  Total changes: {summary.get('totalChanges', 0)}",
        f"  Breaking changes: {summary.get('breakingChanges', 0)}",
        "  Severity: "
        + ", ".join(
            f"{severity}={summary.get('bySeverity', {}).get(severity, 0)}"
            for severity in SEVERITY_LEVELS
        ),
        "Breaking changes:",
    ]
    if breaking_changes:
        lines.extend(change_label(change) for change in breaking_changes)
    else:
        lines.append("  None")
    lines.extend(
        [
            "Packs added:",
        ]
    )
    lines.extend(f"  {item}" for item in diff.get("packs", {}).get("added", []))
    lines.append("Packs removed:")
    lines.extend(f"  {item}" for item in diff.get("packs", {}).get("removed", []))
    lines.append("Added:")
    lines.extend(f"  {item}" for item in diff["added"])
    lines.append("Removed:")
    lines.extend(f"  {item}" for item in diff["removed"])
    lines.append("Changed:")
    lines.extend(f"  {item}" for item in diff["changed"])
    return "\n".join(lines)
