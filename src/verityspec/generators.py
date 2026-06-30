from __future__ import annotations

import json
import keyword
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import __version__
from .issues import Issue, issue_count
from .packs import PackRegistry
from .workspace import Record, Workspace


def write_generated(value: str | dict, out_path: str | None) -> str:
    if isinstance(value, dict):
        text = json.dumps(value, indent=2) + "\n"
    else:
        text = value
    if out_path:
        path = Path(out_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return text


def sanitize_identifier(value: str) -> str:
    text = re.sub(r"[^A-Za-z0-9_]+", "_", value).strip("_")
    if not text:
        return "Generated"
    if text[0].isdigit():
        text = f"_{text}"
    return text


def pascal_case(value: str) -> str:
    parts = re.split(r"[^A-Za-z0-9]+", value)
    text = "".join(part[:1].upper() + part[1:] for part in parts if part)
    return text or "Generated"


def schema_component_name(record_id: str) -> str:
    if record_id.startswith("schema."):
        record_id = record_id[len("schema.") :]
    return pascal_case(record_id)


def schema_records(workspace: Workspace) -> list[Record]:
    return [record for record in workspace.records if record.kind == "schema.object" and record.id]


def product_record(workspace: Workspace) -> Record | None:
    for record in workspace.records:
        if record.kind == "product":
            return record
    return None


def component_schemas(workspace: Workspace) -> tuple[dict[str, Any], dict[str, str]]:
    components: dict[str, Any] = {}
    id_to_component: dict[str, str] = {}
    for record in schema_records(workspace):
        name = schema_component_name(record.id or "")
        components[name] = record.data["jsonSchema"]
        id_to_component[record.id or ""] = name
    return components, id_to_component


def openapi_schema_ref(schema_id: str, id_to_component: dict[str, str]) -> dict[str, str]:
    name = id_to_component.get(schema_id)
    if not name:
        return {}
    return {"$ref": f"#/components/schemas/{name}"}


def generate_openapi(workspace: Workspace) -> dict:
    product = product_record(workspace)
    schemas, id_to_component = component_schemas(workspace)
    title = product.data.get("name") if product else workspace.config.get("workspace", "VeritySpec API")
    version = product.data.get("version", "0.1.0") if product else "0.1.0"

    document: dict[str, Any] = {
        "openapi": "3.1.0",
        "info": {
            "title": title,
            "version": version,
        },
        "paths": {},
        "components": {
            "schemas": schemas,
        },
    }

    for record in workspace.records:
        if record.kind != "api.endpoint":
            continue
        method = record.data["method"].lower()
        path = record.data["path"]
        operation: dict[str, Any] = {
            "operationId": sanitize_identifier(record.id or record.data["name"]),
            "summary": record.data.get("summary", record.data["name"]),
            "description": record.data.get("description", ""),
            "responses": {},
        }

        request_schema = record.data.get("requestSchema")
        if isinstance(request_schema, str):
            ref = openapi_schema_ref(request_schema, id_to_component)
            if ref:
                operation["requestBody"] = {
                    "required": True,
                    "content": {"application/json": {"schema": ref}},
                }

        for response in record.data.get("responses", []):
            status_code = str(response["statusCode"])
            response_entry: dict[str, Any] = {
                "description": response.get("description", ""),
            }
            response_schema = response.get("schema")
            if isinstance(response_schema, str):
                ref = openapi_schema_ref(response_schema, id_to_component)
                if ref:
                    response_entry["content"] = {"application/json": {"schema": ref}}
            operation["responses"][status_code] = response_entry

        document["paths"].setdefault(path, {})[method] = operation

    return document


def generate_asyncapi(workspace: Workspace) -> dict:
    product = product_record(workspace)
    schemas, id_to_component = component_schemas(workspace)
    title = product.data.get("name") if product else workspace.config.get("workspace", "VeritySpec Events")
    version = product.data.get("version", "0.1.0") if product else "0.1.0"

    document: dict[str, Any] = {
        "asyncapi": "2.6.0",
        "info": {
            "title": title,
            "version": version,
        },
        "channels": {},
        "components": {
            "schemas": schemas,
            "messages": {},
        },
    }

    for record in workspace.records:
        if record.kind != "event.message":
            continue
        message_name = pascal_case(record.id or record.data["name"])
        payload_schema = record.data.get("payloadSchema")
        payload = openapi_schema_ref(payload_schema, id_to_component) if isinstance(payload_schema, str) else {}
        document["components"]["messages"][message_name] = {
            "name": record.data["name"],
            "title": record.data["name"],
            "summary": record.data.get("summary", record.data.get("description", "")),
            "payload": payload,
        }
        document["channels"][record.data["topic"]] = {
            "subscribe": {
                "message": {
                    "$ref": f"#/components/messages/{message_name}",
                }
            }
        }

    return document


def ts_type(schema: dict[str, Any]) -> str:
    schema_type = schema.get("type")
    if isinstance(schema_type, list):
        non_null = [item for item in schema_type if item != "null"]
        if len(non_null) == 1:
            return f"{ts_type({**schema, 'type': non_null[0]})} | null"
    if schema_type == "string":
        return "string"
    if schema_type in {"integer", "number"}:
        return "number"
    if schema_type == "boolean":
        return "boolean"
    if schema_type == "array":
        return f"{ts_type(schema.get('items', {}))}[]"
    if schema_type == "object":
        return "Record<string, unknown>"
    return "unknown"


def generate_typescript(workspace: Workspace) -> str:
    blocks: list[str] = []
    for record in schema_records(workspace):
        schema = record.data["jsonSchema"]
        name = schema_component_name(record.id or "")
        properties = schema.get("properties", {})
        required = set(schema.get("required", []))
        lines = [f"export interface {name} {{"]
        if isinstance(properties, dict):
            for prop_name, prop_schema in properties.items():
                optional = "" if prop_name in required else "?"
                lines.append(f"  {prop_name}{optional}: {ts_type(prop_schema)};")
        lines.append("}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks) + "\n"


def python_type(schema: dict[str, Any]) -> str:
    schema_type = schema.get("type")
    if isinstance(schema_type, list):
        non_null = [item for item in schema_type if item != "null"]
        if len(non_null) == 1:
            return f"Optional[{python_type({**schema, 'type': non_null[0]})}]"
    if schema_type == "string":
        return "str"
    if schema_type == "integer":
        return "int"
    if schema_type == "number":
        return "float"
    if schema_type == "boolean":
        return "bool"
    if schema_type == "array":
        return f"list[{python_type(schema.get('items', {}))}]"
    if schema_type == "object":
        return "dict[str, Any]"
    return "Any"


def python_field_name(name: str) -> str:
    field = sanitize_identifier(name).lower()
    if keyword.iskeyword(field):
        return f"{field}_"
    return field


def generate_python_models(workspace: Workspace) -> str:
    blocks = [
        "from __future__ import annotations",
        "",
        "from dataclasses import dataclass",
        "from typing import Any, Optional",
        "",
    ]
    for record in schema_records(workspace):
        schema = record.data["jsonSchema"]
        name = schema_component_name(record.id or "")
        properties = schema.get("properties", {})
        required = set(schema.get("required", []))
        lines = ["@dataclass", f"class {name}:"]
        required_lines: list[str] = []
        optional_lines: list[str] = []
        if isinstance(properties, dict):
            for prop_name, prop_schema in properties.items():
                line = f"    {python_field_name(prop_name)}: {python_type(prop_schema)}"
                if prop_name in required:
                    required_lines.append(line)
                else:
                    optional_lines.append(f"{line} = None")
        field_lines = required_lines + optional_lines
        if field_lines:
            lines.extend(field_lines)
        else:
            lines.append("    pass")
        blocks.append("\n".join(lines))
        blocks.append("")
    return "\n".join(blocks)


def generate_schema_bundle(registry: PackRegistry) -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "VeritySpec Schema Bundle",
        "packs": sorted(registry.packs),
        "schemas": {
            kind: binding.schema
            for kind, binding in sorted(registry.schemas.items(), key=lambda item: item[0])
        },
    }


def generate_validation_report(
    workspace: Workspace, registry: PackRegistry, issues: list[Issue]
) -> dict:
    errors = issue_count(issues, "error")
    warnings = issue_count(issues, "warning")
    return {
        "type": "validation_report",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "verityVersion": __version__,
        "workspace": workspace.config.get("workspace", workspace.base_path.name),
        "workspacePath": str(workspace.base_path),
        "specVersion": workspace.config.get("specVersion"),
        "packs": workspace.pack_ids,
        "packVersions": {
            pack_id: pack.version
            for pack_id, pack in sorted(registry.packs.items(), key=lambda item: item[0])
        },
        "knownKinds": registry.known_kinds,
        "recordCount": len(workspace.records),
        "passed": errors == 0,
        "summary": {
            "errors": errors,
            "warnings": warnings,
            "issues": errors + warnings,
        },
        "issues": [issue.to_dict() for issue in issues],
    }


def generate_cli_reference(workspace: Workspace) -> str:
    lines = ["# CLI Reference", ""]
    commands = [record for record in workspace.records if record.kind == "cli.command"]
    for record in commands:
        lines.append(f"## `{record.data['command']}`")
        lines.append("")
        lines.append(record.data.get("description", record.data["name"]))
        lines.append("")
        options = record.data.get("options", [])
        if options:
            lines.append("| Option | Required | Description |")
            lines.append("|---|---:|---|")
            for option in options:
                lines.append(
                    f"| `{option['name']}` | {str(option.get('required', False)).lower()} | {option.get('description', '')} |"
                )
            lines.append("")
        exit_codes = record.data.get("exitCodes", [])
        if exit_codes:
            lines.append("| Exit code | Meaning |")
            lines.append("|---:|---|")
            for exit_code in exit_codes:
                lines.append(f"| {exit_code['code']} | {exit_code['description']} |")
            lines.append("")
    return "\n".join(lines)
