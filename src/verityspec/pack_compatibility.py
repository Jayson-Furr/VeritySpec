from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .issues import Issue
from .packs import Pack, load_pack, load_pack_from_path, normalize_pack_path


def _canonical(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _canonical(value[key]) for key in sorted(value)}
    if isinstance(value, list):
        return [_canonical(item) for item in value]
    return value


def _sort_by_key(values: list[dict[str, Any]], keys: tuple[str, ...]) -> list[dict[str, Any]]:
    return sorted(
        values,
        key=lambda item: tuple(str(item.get(key, "")) for key in keys),
    )


def _manifest(path: Path) -> dict[str, Any]:
    return json.loads((path / "pack.json").read_text(encoding="utf-8"))


def _surface_summary(pack: Pack) -> dict[str, Any]:
    manifest = _manifest(pack.path)
    schema_declarations = _sort_by_key(
        [
            {
                "kind": item.get("kind"),
                "path": item.get("path"),
            }
            for item in manifest.get("schemas", [])
        ],
        ("kind", "path"),
    )
    readiness_gates = _sort_by_key(
        [_canonical(item) for item in manifest.get("readinessGates", [])],
        ("kind", "id"),
    )
    reference_rules = _sort_by_key(
        [_canonical(item) for item in manifest.get("referenceRules", [])],
        ("sourceKind", "relationship", "targetKind"),
    )
    generator_metadata = _sort_by_key(
        [_canonical(item) for item in pack.generator_metadata],
        ("id",),
    )
    return {
        "id": pack.id,
        "version": pack.version,
        "name": pack.name,
        "description": pack.description,
        "path": str(pack.path),
        "source": pack.source,
        "schemaDeclarations": schema_declarations,
        "readinessGates": readiness_gates,
        "referenceRules": reference_rules,
        "generatorMetadata": generator_metadata,
        "kinds": sorted(pack.schemas),
    }


def _schema_content(pack: Pack) -> dict[str, Any]:
    return {
        kind: _canonical(binding.schema)
        for kind, binding in sorted(pack.schemas.items())
    }


def _difference(surface: str, code: str, message: str, **details: Any) -> dict[str, Any]:
    difference = {
        "surface": surface,
        "code": code,
        "message": message,
    }
    difference.update(details)
    return difference


def compare_pack_mirror(pack_id: str, mirror_path: str | Path) -> tuple[dict[str, Any], list[Issue]]:
    differences: list[dict[str, Any]] = []
    issues: list[Issue] = []

    try:
        source_pack = load_pack(pack_id)
    except ValueError as exc:
        issue = Issue("error", "pack.unknown", str(exc))
        report = {
            "command": "pack.compare",
            "passed": False,
            "packId": pack_id,
            "mirrorPath": str(mirror_path),
            "summary": {"differences": 0},
            "differences": [],
            "issues": [issue.to_dict()],
        }
        return report, [issue]

    try:
        mirror_pack = load_pack_from_path(normalize_pack_path(mirror_path), source="mirror")
    except Exception as exc:
        issue = Issue(
            "error",
            "pack.mirror.invalid",
            f"Pack mirror could not be loaded: {exc}",
            str(mirror_path),
        )
        report = {
            "command": "pack.compare",
            "passed": False,
            "packId": pack_id,
            "source": _surface_summary(source_pack),
            "mirrorPath": str(mirror_path),
            "summary": {"differences": 0},
            "differences": [],
            "issues": [issue.to_dict()],
        }
        return report, [issue]

    source = _surface_summary(source_pack)
    mirror = _surface_summary(mirror_pack)

    if mirror_pack.id != pack_id:
        differences.append(
            _difference(
                "manifest",
                "id_mismatch",
                f"Mirror manifest id '{mirror_pack.id}' does not match source pack id '{pack_id}'.",
                sourceId=pack_id,
                mirrorId=mirror_pack.id,
            )
        )

    for field in ["version", "name", "description"]:
        if source[field] != mirror[field]:
            differences.append(
                _difference(
                    "manifest",
                    f"{field}_mismatch",
                    f"Mirror manifest field '{field}' differs from source pack.",
                    field=field,
                    sourceValue=source[field],
                    mirrorValue=mirror[field],
                )
            )

    for surface in [
        "schemaDeclarations",
        "readinessGates",
        "referenceRules",
        "generatorMetadata",
    ]:
        if source[surface] != mirror[surface]:
            differences.append(
                _difference(
                    surface,
                    "surface_mismatch",
                    f"Mirror {surface} differ from source pack.",
                    sourceValue=source[surface],
                    mirrorValue=mirror[surface],
                )
            )

    source_schemas = _schema_content(source_pack)
    mirror_schemas = _schema_content(mirror_pack)
    source_kinds = set(source_schemas)
    mirror_kinds = set(mirror_schemas)
    if source_kinds != mirror_kinds:
        differences.append(
            _difference(
                "schemas",
                "schema_inventory_mismatch",
                "Mirror schema kind inventory differs from source pack.",
                missingInMirror=sorted(source_kinds - mirror_kinds),
                extraInMirror=sorted(mirror_kinds - source_kinds),
            )
        )

    for kind in sorted(source_kinds & mirror_kinds):
        if source_schemas[kind] != mirror_schemas[kind]:
            differences.append(
                _difference(
                    "schemas",
                    "schema_content_mismatch",
                    f"Mirror schema content differs for kind '{kind}'.",
                    kind=kind,
                    sourcePath=str(source_pack.schemas[kind].path),
                    mirrorPath=str(mirror_pack.schemas[kind].path),
                )
            )

    for difference in differences:
        code = "pack.mirror.id_mismatch" if difference["code"] == "id_mismatch" else "pack.mirror.surface_mismatch"
        issues.append(
            Issue(
                "error",
                code,
                difference["message"],
                difference.get("mirrorPath") or str(mirror_pack.path),
            )
        )

    report = {
        "command": "pack.compare",
        "passed": not issues,
        "packId": pack_id,
        "source": source,
        "mirror": mirror,
        "summary": {
            "differences": len(differences),
            "schemas": len(source_pack.schemas),
            "readinessGates": len(source_pack.readiness_gates),
            "referenceRules": len(source_pack.reference_rules),
            "generators": len(source_pack.generator_metadata),
        },
        "differences": differences,
        "issues": [issue.to_dict() for issue in issues],
    }
    return report, issues


def pack_mirror_report_to_text(report: dict[str, Any]) -> str:
    lines = [
        "Pack mirror comparison passed."
        if report.get("passed")
        else "Pack mirror comparison failed.",
        f"Pack: {report.get('packId')}",
    ]
    source = report.get("source")
    if isinstance(source, dict):
        lines.append(f"Source: {source.get('source')} {source.get('path')}")
    mirror = report.get("mirror")
    if isinstance(mirror, dict):
        lines.append(f"Mirror: {mirror.get('path')}")
    elif report.get("mirrorPath"):
        lines.append(f"Mirror: {report.get('mirrorPath')}")

    summary = report.get("summary", {})
    if isinstance(summary, dict):
        lines.append(f"Differences: {summary.get('differences', 0)}")
    for difference in report.get("differences", []):
        lines.append(
            f"- {difference.get('surface')}: {difference.get('code')} - {difference.get('message')}"
        )
    return "\n".join(lines)
