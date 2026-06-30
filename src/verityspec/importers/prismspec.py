from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STATUS_MAP = {
    "approved": "ready",
    "locked": "ready",
    "review": "review",
    "draft": "draft",
    "deprecated": "deprecated",
    "removed": "removed",
}


def import_prismspec(source: str | Path, out: str | Path) -> dict[str, Any]:
    source_path = Path(source).resolve()
    out_path = Path(out).resolve()
    records_path = out_path / "records"
    records_path.mkdir(parents=True, exist_ok=True)

    converted: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    unsupported_fields: list[dict[str, str]] = []

    for catalog_path in sorted(source_path.rglob("*.catalog.json")):
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        for record in catalog.get("records", []):
            if not isinstance(record, dict):
                continue
            record_type = record.get("type")
            if record_type == "product":
                converted_record = {
                    "id": record.get("id"),
                    "kind": "product",
                    "name": record.get("displayName", record.get("id", "Imported Product")),
                    "description": record.get("description", "Imported from PrismSpec."),
                    "status": STATUS_MAP.get(record.get("status"), "draft"),
                    "owner": record.get("owner", "unknown"),
                    "version": record.get("introducedIn", "0.1.0"),
                    "references": [],
                }
                converted.append(converted_record)
                for field in sorted(set(record) - set(["id", "type", "displayName", "description", "status", "owner", "introducedIn"])):
                    unsupported_fields.append({"recordId": str(record.get("id")), "field": field})
            else:
                skipped.append(
                    {
                        "recordId": str(record.get("id", "")),
                        "type": str(record_type),
                        "reason": "No stable VeritySpec v0.1 mapping yet.",
                    }
                )

    workspace = {
        "workspace": out_path.name,
        "specVersion": "v0.1.0",
        "packs": ["verity.core"],
        "records": ["records/*.json"],
    }
    (out_path / "verityspec.json").write_text(json.dumps(workspace, indent=2) + "\n", encoding="utf-8")

    for record in converted:
        safe_id = str(record["id"]).replace("/", "_").replace(":", "_")
        (records_path / f"{safe_id}.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    report = {
        "source": str(source_path),
        "output": str(out_path),
        "convertedRecords": len(converted),
        "skippedRecords": skipped,
        "unsupportedFields": unsupported_fields,
        "manualFollowUp": [
            "Review placeholder owners.",
            "Map skipped PrismSpec record types to VeritySpec packs as those packs mature.",
            "Run `verity validate` and `verity readiness --strict` on the imported workspace.",
        ],
    }
    (out_path / "migration-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report

