from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .issues import Issue, issue_count
from .packs import (
    PACK_ENTRY_POINT_GROUP,
    available_builtin_packs,
    installed_pack_entry_points,
    normalize_pack_path,
    resolve_installed_pack_entry_point,
)


def _entry_point_value(entry_point: Any) -> str | None:
    value = getattr(entry_point, "value", None)
    return str(value) if value is not None else None


def _entry_point_sort_key(entry_point: Any) -> tuple[str, str]:
    return (str(getattr(entry_point, "name", "")), _entry_point_value(entry_point) or "")


def _issue(
    issues: list[Issue],
    target_issues: list[dict[str, Any]],
    severity: str,
    code: str,
    message: str,
    location: str | None = None,
    record_id: str | None = None,
) -> None:
    issue = Issue(severity, code, message, location=location, record_id=record_id)
    issues.append(issue)
    target_issues.append(issue.to_dict())


def _read_manifest(
    manifest_path: Path,
    issues: list[Issue],
    target_issues: list[dict[str, Any]],
    source_code_prefix: str,
) -> dict[str, Any] | None:
    if not manifest_path.exists():
        _issue(
            issues,
            target_issues,
            "error",
            f"{source_code_prefix}.missing_manifest",
            f"Pack source does not contain pack.json: {manifest_path.parent}",
            str(manifest_path.parent),
        )
        return None
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        _issue(
            issues,
            target_issues,
            "error",
            f"{source_code_prefix}.manifest_invalid",
            f"Pack manifest could not be parsed: {exc}",
            str(manifest_path),
        )
        return None
    if not isinstance(manifest, dict):
        _issue(
            issues,
            target_issues,
            "error",
            f"{source_code_prefix}.manifest_invalid",
            "Pack manifest must be a JSON object.",
            str(manifest_path),
        )
        return None
    return manifest


def _pack_id_from_manifest(
    manifest: dict[str, Any],
    manifest_path: Path,
    issues: list[Issue],
    target_issues: list[dict[str, Any]],
    source_code_prefix: str,
) -> str | None:
    pack_id = manifest.get("id")
    if not isinstance(pack_id, str):
        _issue(
            issues,
            target_issues,
            "error",
            f"{source_code_prefix}.manifest_id_missing",
            f"Pack manifest is missing string id: {manifest_path}",
            str(manifest_path),
        )
        return None
    return pack_id


def diagnose_pack_discovery(
    external_pack_paths: list[str | Path] | None = None,
    base_path: Path | None = None,
) -> tuple[dict[str, Any], list[Issue]]:
    """Return non-throwing diagnostics for built-in, installed, and local packs."""

    issues: list[Issue] = []
    builtin = available_builtin_packs()
    builtin_ids = set(builtin)

    built_in_packs = [
        {"id": pack_id, "path": str(path)}
        for pack_id, path in sorted(builtin.items(), key=lambda item: item[0])
    ]

    installed_entries: list[dict[str, Any]] = []
    installed_by_id: dict[str, list[dict[str, Any]]] = {}
    for entry_point in sorted(installed_pack_entry_points(), key=_entry_point_sort_key):
        entry_issues: list[dict[str, Any]] = []
        entry = {
            "name": str(getattr(entry_point, "name", "")),
            "value": _entry_point_value(entry_point),
            "source": "installed",
            "status": "ok",
            "issues": entry_issues,
        }
        try:
            pack_path = resolve_installed_pack_entry_point(entry_point)
        except ValueError as exc:
            _issue(
                issues,
                entry_issues,
                "error",
                "pack.installed.entry_point_load_failed",
                str(exc),
                entry["name"],
            )
            entry["status"] = "error"
            installed_entries.append(entry)
            continue

        entry["path"] = str(pack_path)
        manifest_path = pack_path / "pack.json"
        manifest = _read_manifest(
            manifest_path,
            issues,
            entry_issues,
            "pack.installed",
        )
        if manifest is None:
            entry["status"] = "error"
            installed_entries.append(entry)
            continue

        pack_id = _pack_id_from_manifest(
            manifest,
            manifest_path,
            issues,
            entry_issues,
            "pack.installed",
        )
        if pack_id is None:
            entry["status"] = "error"
            installed_entries.append(entry)
            continue

        entry["packId"] = pack_id
        if entry["name"] != pack_id:
            _issue(
                issues,
                entry_issues,
                "error",
                "pack.installed.entry_point_name_mismatch",
                f"Installed pack entry point '{entry['name']}' must match manifest id '{pack_id}'.",
                str(manifest_path),
                pack_id,
            )
        if pack_id in builtin_ids:
            _issue(
                issues,
                entry_issues,
                "error",
                "pack.installed.builtin_collision",
                f"Installed pack '{pack_id}' collides with a built-in pack id.",
                str(manifest_path),
                pack_id,
            )
        entry["status"] = "error" if entry_issues else "ok"
        installed_entries.append(entry)
        installed_by_id.setdefault(pack_id, []).append(entry)

    for pack_id, entries in sorted(installed_by_id.items(), key=lambda item: item[0]):
        if len(entries) <= 1:
            continue
        message = (
            f"Installed pack '{pack_id}' is declared by multiple entry points: "
            + ", ".join(entry["name"] for entry in entries)
        )
        for entry in entries:
            _issue(
                issues,
                entry["issues"],
                "error",
                "pack.installed.duplicate_id",
                message,
                str(entry.get("path") or entry["name"]),
                pack_id,
            )
            entry["status"] = "error"

    external_entries: list[dict[str, Any]] = []
    external_by_id: dict[str, list[dict[str, Any]]] = {}
    for raw_path in external_pack_paths or []:
        entry_issues = []
        entry = {
            "input": str(raw_path),
            "source": "external",
            "status": "ok",
            "issues": entry_issues,
        }
        try:
            pack_path = normalize_pack_path(raw_path, base_path)
        except Exception as exc:
            _issue(
                issues,
                entry_issues,
                "error",
                "pack.external.path_invalid",
                f"External pack path could not be resolved: {exc}",
                str(raw_path),
            )
            entry["status"] = "error"
            external_entries.append(entry)
            continue

        entry["path"] = str(pack_path)
        manifest_path = pack_path / "pack.json"
        manifest = _read_manifest(
            manifest_path,
            issues,
            entry_issues,
            "pack.external",
        )
        if manifest is None:
            entry["status"] = "error"
            external_entries.append(entry)
            continue

        pack_id = _pack_id_from_manifest(
            manifest,
            manifest_path,
            issues,
            entry_issues,
            "pack.external",
        )
        if pack_id is None:
            entry["status"] = "error"
            external_entries.append(entry)
            continue

        entry["packId"] = pack_id
        if pack_id in builtin_ids:
            _issue(
                issues,
                entry_issues,
                "error",
                "pack.external.builtin_collision",
                f"External pack '{pack_id}' collides with a built-in pack id.",
                str(manifest_path),
                pack_id,
            )
        entry["status"] = "error" if entry_issues else "ok"
        external_entries.append(entry)
        external_by_id.setdefault(pack_id, []).append(entry)

    for pack_id, entries in sorted(external_by_id.items(), key=lambda item: item[0]):
        if len(entries) <= 1:
            continue
        message = (
            f"External pack '{pack_id}' is declared by multiple local paths: "
            + ", ".join(str(entry.get("path", entry["input"])) for entry in entries)
        )
        for entry in entries:
            _issue(
                issues,
                entry["issues"],
                "error",
                "pack.external.duplicate_id",
                message,
                str(entry.get("path") or entry["input"]),
                pack_id,
            )
            entry["status"] = "error"

    overrides: list[dict[str, Any]] = []
    valid_installed_by_id = {
        pack_id: [
            entry
            for entry in entries
            if entry.get("path") and not any(
                item.get("severity") == "error" for item in entry.get("issues", [])
            )
        ]
        for pack_id, entries in installed_by_id.items()
    }
    for pack_id, entries in sorted(external_by_id.items(), key=lambda item: item[0]):
        installed_entries_for_id = valid_installed_by_id.get(pack_id, [])
        if not installed_entries_for_id:
            continue
        for entry in entries:
            if any(item.get("severity") == "error" for item in entry.get("issues", [])):
                continue
            _issue(
                issues,
                entry["issues"],
                "warning",
                "pack.external.overrides_installed",
                (
                    f"External pack '{pack_id}' takes precedence over installed pack "
                    "entry points with the same id."
                ),
                str(entry.get("path") or entry["input"]),
                pack_id,
            )
            if entry["status"] == "ok":
                entry["status"] = "warning"
            overrides.append(
                {
                    "packId": pack_id,
                    "activeSource": "external",
                    "activePath": entry.get("path"),
                    "shadowedSource": "installed",
                    "shadowedEntryPoints": [
                        {
                            "name": installed_entry["name"],
                            "path": installed_entry.get("path"),
                        }
                        for installed_entry in installed_entries_for_id
                    ],
                    "reason": (
                        "Explicit local pack paths take precedence over installed packs "
                        "with the same id."
                    ),
                }
            )

    installed_pack_ids = sorted(
        pack_id
        for pack_id, entries in installed_by_id.items()
        if any(entry.get("path") for entry in entries)
    )
    external_pack_ids = sorted(
        pack_id
        for pack_id, entries in external_by_id.items()
        if any(entry.get("path") for entry in entries)
    )
    report = {
        "command": "pack.doctor",
        "passed": issue_count(issues, "error") == 0,
        "entryPointGroup": PACK_ENTRY_POINT_GROUP,
        "summary": {
            "errors": issue_count(issues, "error"),
            "warnings": issue_count(issues, "warning"),
            "issues": len(issues),
            "builtInPackCount": len(built_in_packs),
            "installedEntryPointCount": len(installed_entries),
            "installedPackCount": len(installed_pack_ids),
            "externalPathCount": len(external_pack_paths or []),
            "externalPackCount": len(external_pack_ids),
            "overrideCount": len(overrides),
        },
        "builtInPacks": built_in_packs,
        "installedEntryPoints": installed_entries,
        "externalPacks": external_entries,
        "overrides": overrides,
        "issues": [issue.to_dict() for issue in issues],
    }
    return report, issues


def pack_discovery_report_to_text(report: dict[str, Any]) -> str:
    summary = report.get("summary", {})
    lines = [
        "Pack diagnostics passed." if report.get("passed") else "Pack diagnostics failed.",
        f"Entry point group: {report.get('entryPointGroup')}",
        f"Built-in packs: {summary.get('builtInPackCount', 0)}",
        f"Installed entry points: {summary.get('installedEntryPointCount', 0)}",
        f"Installed packs: {summary.get('installedPackCount', 0)}",
        f"External pack paths: {summary.get('externalPathCount', 0)}",
        f"External packs: {summary.get('externalPackCount', 0)}",
        f"Overrides: {summary.get('overrideCount', 0)}",
    ]

    overrides = report.get("overrides", [])
    if overrides:
        lines.append("")
        lines.append("Local overrides:")
        for override in overrides:
            shadowed = ", ".join(
                item.get("name", "") for item in override.get("shadowedEntryPoints", [])
            )
            lines.append(
                f"- {override.get('packId')}: external {override.get('activePath')} "
                f"overrides installed {shadowed}"
            )

    issues = report.get("issues", [])
    if issues:
        lines.append("")
        lines.append("Issues:")
        for issue in issues:
            location = f" {issue['location']}" if issue.get("location") else ""
            record_id = f" {issue['recordId']}" if issue.get("recordId") else ""
            lines.append(
                f"- {issue['severity'].upper()} {issue['code']}{record_id}{location}: "
                f"{issue['message']}"
            )

    return "\n".join(lines)
