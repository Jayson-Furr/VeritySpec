from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Callable


STATUS_MAP = {
    "approved": "ready",
    "locked": "ready",
    "review": "review",
    "draft": "draft",
    "deprecated": "deprecated",
    "removed": "removed",
}

BASE_FIELDS = {
    "id",
    "type",
    "specificationVersion",
    "displayName",
    "description",
    "status",
    "owner",
    "tags",
    "groupIds",
    "introducedIn",
    "deprecatedIn",
    "removedIn",
    "extensions",
}

RECOMMENDED_PACK_MAPPINGS = {
    "product": ["verity.core"],
    "endpoint": ["verity.core", "verity.pack.api"],
    "command": ["verity.core", "verity.pack.cli"],
    "telemetry_event": ["verity.core", "verity.pack.events"],
    "asset": ["future verity.pack.assets"],
    "control_type": ["future verity.pack.ui"],
    "profile_composition": ["verity.core with manual product/workspace modeling"],
    "user_flow": ["future verity.pack.ui"],
    "service_flow": ["future verity.pack.services"],
}


def verity_id(value: Any, fallback: str) -> str:
    raw = str(value or fallback).strip().lower()
    raw = re.sub(r"[^a-z0-9._-]+", ".", raw)
    raw = re.sub(r"[._-]+", ".", raw).strip(".-_")
    if not raw or not raw[0].isalpha():
        raw = f"imported.{raw or fallback}"
    return raw


def record_name(record: dict[str, Any]) -> str:
    return str(record.get("displayName") or record.get("id") or "Imported Record")


def record_description(record: dict[str, Any], fallback: str) -> str:
    return str(record.get("description") or fallback)


def record_status(record: dict[str, Any]) -> str:
    return STATUS_MAP.get(str(record.get("status")), "draft")


def record_owner(record: dict[str, Any]) -> str:
    owner = record.get("owner")
    return str(owner) if owner else "imported"


def unsupported_fields(record: dict[str, Any], supported: set[str]) -> list[str]:
    return sorted(set(record) - supported)


def map_product(record: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    converted = [
        {
            "id": verity_id(record.get("id"), "product.imported"),
            "kind": "product",
            "name": record_name(record),
            "description": record_description(record, "Imported PrismSpec product."),
            "status": record_status(record),
            "owner": record_owner(record),
            "version": str(record.get("introducedIn") or "0.1.0"),
            "references": [],
        }
    ]
    supported = BASE_FIELDS | {"productKind", "audiences"}
    notes = ["PrismSpec productKind/audiences are not first-class VeritySpec fields yet."]
    return converted, unsupported_fields(record, supported), notes


def map_endpoint(record: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    notes: list[str] = []
    responses = record.get("responses")
    if not isinstance(responses, list) or not responses:
        responses = [{"statusCode": 200, "description": "Imported default response; review manually."}]
        notes.append("Added default 200 response because PrismSpec record did not provide responses.")
    converted = [
        {
            "id": verity_id(record.get("id"), "api.imported"),
            "kind": "api.endpoint",
            "name": record_name(record),
            "description": record_description(record, "Imported PrismSpec endpoint."),
            "status": record_status(record),
            "owner": record_owner(record),
            "method": str(record.get("method") or "GET").upper(),
            "path": str(record.get("path") or "/imported"),
            "summary": record_name(record),
            "responses": responses,
        }
    ]
    supported = BASE_FIELDS | {"method", "path", "summary", "responses"}
    return converted, unsupported_fields(record, supported), notes


def map_command(record: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    notes = ["Added default exit codes because PrismSpec command records do not require them."]
    converted = [
        {
            "id": verity_id(record.get("id"), "cli.imported"),
            "kind": "cli.command",
            "name": record_name(record),
            "description": record_description(record, "Imported PrismSpec command."),
            "status": record_status(record),
            "owner": record_owner(record),
            "command": str(record.get("commandName") or record.get("command") or record.get("id") or "imported"),
            "options": [],
            "exitCodes": [
                {"code": 0, "description": "Imported success exit code; review manually."},
                {"code": 1, "description": "Imported failure exit code; review manually."},
            ],
        }
    ]
    supported = BASE_FIELDS | {"commandName", "command", "arguments", "options"}
    return converted, unsupported_fields(record, supported), notes


def map_telemetry_event(record: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    event_id = verity_id(record.get("id"), "event.imported")
    schema_id = verity_id(f"schema.{event_id}.payload", "schema.imported.payload")
    notes = ["Created generic payload schema because PrismSpec telemetry event did not provide a payload schema."]
    converted = [
        {
            "id": schema_id,
            "kind": "schema.object",
            "name": f"{record_name(record)} Payload",
            "description": "Generic imported telemetry payload schema.",
            "status": record_status(record),
            "owner": record_owner(record),
            "jsonSchema": {
                "type": "object",
                "additionalProperties": True,
                "properties": {},
            },
        },
        {
            "id": event_id,
            "kind": "event.message",
            "name": record_name(record),
            "description": record_description(record, "Imported PrismSpec telemetry event."),
            "status": record_status(record),
            "owner": record_owner(record),
            "topic": str(record.get("category") or event_id),
            "payloadSchema": schema_id,
        },
    ]
    supported = BASE_FIELDS | {"category", "privacyClass"}
    return converted, unsupported_fields(record, supported), notes


MAPPERS: dict[str, Callable[[dict[str, Any]], tuple[list[dict[str, Any]], list[str], list[str]]]] = {
    "product": map_product,
    "endpoint": map_endpoint,
    "command": map_command,
    "telemetry_event": map_telemetry_event,
}


def load_prismspec_records(source_path: Path) -> list[tuple[Path, dict[str, Any]]]:
    records: list[tuple[Path, dict[str, Any]]] = []
    for catalog_path in sorted(source_path.rglob("*.catalog.json")):
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        for record in catalog.get("records", []):
            if isinstance(record, dict):
                records.append((catalog_path, record))
    return records


def required_packs_for_records(records: list[dict[str, Any]]) -> list[str]:
    packs = {"verity.core"}
    kinds = {record.get("kind") for record in records}
    if "api.endpoint" in kinds:
        packs.add("verity.pack.api")
    if "cli.command" in kinds:
        packs.add("verity.pack.cli")
    if "event.message" in kinds:
        packs.add("verity.pack.events")
    return sorted(packs)


def write_records(records_path: Path, converted: list[dict[str, Any]]) -> None:
    for index, record in enumerate(converted, start=1):
        safe_id = verity_id(record.get("id"), f"record.{index}").replace(".", "-")
        (records_path / f"{safe_id}.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def import_prismspec(source: str | Path, out: str | Path) -> dict[str, Any]:
    source_path = Path(source).resolve()
    out_path = Path(out).resolve()
    records_path = out_path / "records"
    records_path.mkdir(parents=True, exist_ok=True)

    converted: list[dict[str, Any]] = []
    converted_records: list[dict[str, Any]] = []
    skipped_records: list[dict[str, str]] = []
    unsupported: list[dict[str, str]] = []
    defaults_applied: list[dict[str, Any]] = []
    deprecated_concepts: list[dict[str, str]] = []

    for catalog_path, record in load_prismspec_records(source_path):
        source_type = str(record.get("type") or "unknown")
        source_id = str(record.get("id") or "")
        mapper = MAPPERS.get(source_type)
        if mapper is None:
            skipped_records.append(
                {
                    "recordId": source_id,
                    "type": source_type,
                    "catalog": str(catalog_path.relative_to(source_path)),
                    "reason": "No stable VeritySpec v0.1 mapping exists for this PrismSpec concept.",
                }
            )
            if source_type in {"asset", "control_type", "profile_composition", "user_flow", "service_flow"}:
                deprecated_concepts.append(
                    {
                        "recordId": source_id,
                        "type": source_type,
                        "replacement": ", ".join(RECOMMENDED_PACK_MAPPINGS.get(source_type, [])),
                    }
                )
            continue

        mapped_records, unsupported_field_names, notes = mapper(record)
        converted.extend(mapped_records)
        for mapped in mapped_records:
            converted_records.append(
                {
                    "sourceId": source_id,
                    "sourceType": source_type,
                    "targetId": str(mapped.get("id")),
                    "targetKind": str(mapped.get("kind")),
                }
            )
        for field in unsupported_field_names:
            unsupported.append({"recordId": source_id, "type": source_type, "field": field})
        if notes:
            defaults_applied.append({"recordId": source_id, "type": source_type, "notes": notes})

    packs = required_packs_for_records(converted)
    workspace = {
        "workspace": out_path.name,
        "specVersion": "v0.1.0",
        "packs": packs,
        "records": ["records/*.json"],
    }
    (out_path / "verityspec.json").write_text(json.dumps(workspace, indent=2) + "\n", encoding="utf-8")
    write_records(records_path, converted)

    report = {
        "type": "prismspec_migration_report",
        "source": str(source_path),
        "output": str(out_path),
        "sourceFormat": "PrismSpec v1.0.0 catalogs",
        "targetFormat": "VeritySpec v0.1.0 workspace",
        "compatibility": "not_wire_compatible",
        "convertedRecordCount": len(converted_records),
        "skippedRecordCount": len(skipped_records),
        "unsupportedFieldCount": len(unsupported),
        "convertedRecords": converted_records,
        "skippedRecords": skipped_records,
        "unsupportedFields": unsupported,
        "defaultsApplied": defaults_applied,
        "missingReferences": [],
        "deprecatedConcepts": deprecated_concepts,
        "recommendedPackMappings": RECOMMENDED_PACK_MAPPINGS,
        "manualFollowUp": [
            "Review imported owners, statuses, and descriptions.",
            "Review every default response, exit code, and generated payload schema.",
            "Map skipped PrismSpec concepts to future VeritySpec packs or custom records.",
            "Run `verity validate`, `verity lint --strict`, and `verity readiness --strict` on the imported workspace.",
        ],
    }
    (out_path / "migration-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report
