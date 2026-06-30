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


PATH_PARAMETER_PATTERN = re.compile(r"\{([^{}]+)\}")
OPENAPI_PARAMETER_LOCATIONS = {"path", "query", "header", "cookie"}


def path_parameter_names(path: str) -> list[str]:
    names: list[str] = []
    for match in PATH_PARAMETER_PATTERN.finditer(path):
        name = match.group(1).strip()
        if name and name not in names:
            names.append(name)
    return names


def openapi_parameter_schema(value: Any, id_to_component: dict[str, str]) -> dict[str, Any]:
    if isinstance(value, dict) and value:
        return dict(value)
    if isinstance(value, str):
        ref = openapi_schema_ref(value, id_to_component)
        if ref:
            return ref
    return {"type": "string"}


def normalize_openapi_parameter(
    value: Any,
    id_to_component: dict[str, str],
) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    name = value.get("name")
    location = value.get("in")
    if not isinstance(name, str) or not name:
        return None
    if not isinstance(location, str) or location not in OPENAPI_PARAMETER_LOCATIONS:
        return None

    parameter: dict[str, Any] = {
        "name": name,
        "in": location,
        "required": True if location == "path" else bool(value.get("required", False)),
        "schema": openapi_parameter_schema(value.get("schema"), id_to_component),
    }
    description = value.get("description")
    if isinstance(description, str) and description:
        parameter["description"] = description
    return parameter


def openapi_parameters(record: Record, path: str, id_to_component: dict[str, str]) -> list[dict[str, Any]]:
    explicit_parameters: list[dict[str, Any]] = []
    seen_explicit: set[tuple[str, str]] = set()
    for item in record.data.get("parameters", []):
        parameter = normalize_openapi_parameter(item, id_to_component)
        if not parameter:
            continue
        key = (parameter["in"], parameter["name"])
        if key in seen_explicit:
            continue
        seen_explicit.add(key)
        explicit_parameters.append(parameter)

    explicit_by_key = {
        (parameter["in"], parameter["name"]): parameter
        for parameter in explicit_parameters
    }
    parameters: list[dict[str, Any]] = []
    emitted: set[tuple[str, str]] = set()

    for name in path_parameter_names(path):
        key = ("path", name)
        parameter = explicit_by_key.get(
            key,
            {
                "name": name,
                "in": "path",
                "required": True,
                "schema": {"type": "string"},
            },
        )
        parameter = {**parameter, "required": True}
        parameters.append(parameter)
        emitted.add(key)

    for parameter in explicit_parameters:
        key = (parameter["in"], parameter["name"])
        if key in emitted:
            continue
        parameters.append(parameter)
        emitted.add(key)

    return parameters


def schema_ref_name(ref: str) -> str | None:
    if ref.startswith("#/components/schemas/"):
        return ref.rsplit("/", 1)[-1]
    return None


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
            "description": product.data.get("description", "") if product else "",
        },
        "paths": {},
        "components": {
            "schemas": schemas,
        },
        "tags": [],
    }
    tag_names: set[str] = set()

    for record in workspace.records:
        if record.kind != "api.endpoint":
            continue
        method = record.data["method"].lower()
        path = record.data["path"]
        owner = record.data.get("owner", "default")
        if isinstance(owner, str) and owner not in tag_names:
            tag_names.add(owner)
            document["tags"].append({"name": owner})
        operation: dict[str, Any] = {
            "operationId": sanitize_identifier(record.id or record.data["name"]),
            "tags": [owner] if isinstance(owner, str) else [],
            "summary": record.data.get("summary", record.data["name"]),
            "description": record.data.get("description", ""),
            "deprecated": record.data.get("status") == "deprecated",
            "x-verity-id": record.id,
            "x-verity-owner": owner,
            "x-verity-status": record.data.get("status"),
        }
        parameters = openapi_parameters(record, path, id_to_component)
        if parameters:
            operation["parameters"] = parameters
        operation["responses"] = {}

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
            "description": product.data.get("description", "") if product else "",
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
            "messageId": sanitize_identifier(record.id or record.data["name"]),
            "name": record.data["name"],
            "title": record.data["name"],
            "summary": record.data.get("summary", record.data.get("description", "")),
            "description": record.data.get("description", ""),
            "payload": payload,
            "x-verity-id": record.id,
            "x-verity-owner": record.data.get("owner"),
            "x-verity-status": record.data.get("status"),
        }
        document["channels"][record.data["topic"]] = {
            "description": record.data.get("description", ""),
            "subscribe": {
                "operationId": sanitize_identifier(f"subscribe.{record.id or record.data['name']}"),
                "message": {
                    "$ref": f"#/components/messages/{message_name}",
                }
            }
        }

    return document


def ts_literal(value: Any) -> str:
    return json.dumps(value)


def ts_property_name(value: str) -> str:
    if re.match(r"^[A-Za-z_$][A-Za-z0-9_$]*$", value):
        return value
    return json.dumps(value)


def ts_type(schema: dict[str, Any]) -> str:
    ref = schema.get("$ref")
    if isinstance(ref, str):
        return schema_ref_name(ref) or "unknown"
    enum = schema.get("enum")
    if isinstance(enum, list) and enum:
        return " | ".join(ts_literal(item) for item in enum)
    if "const" in schema:
        return ts_literal(schema["const"])
    schema_type = schema.get("type")
    if isinstance(schema_type, list):
        variants = [ts_type({**schema, "type": item}) for item in schema_type if item != "null"]
        if "null" in schema_type:
            variants.append("null")
        return " | ".join(dict.fromkeys(variants)) if variants else "unknown"
    if schema_type == "string":
        return "string"
    if schema_type in {"integer", "number"}:
        return "number"
    if schema_type == "boolean":
        return "boolean"
    if schema_type == "array":
        return f"{ts_type(schema.get('items', {}))}[]"
    if schema_type == "object":
        properties = schema.get("properties", {})
        if isinstance(properties, dict) and properties:
            required = set(schema.get("required", []))
            fields = []
            for prop_name, prop_schema in properties.items():
                optional = "" if prop_name in required else "?"
                fields.append(f"{ts_property_name(prop_name)}{optional}: {ts_type(prop_schema)}")
            return "{ " + "; ".join(fields) + " }"
        return "Record<string, unknown>"
    return "unknown"


def ts_doc(description: Any, indent: str = "") -> list[str]:
    if not isinstance(description, str) or not description.strip():
        return []
    clean = description.replace("*/", "* /").strip()
    return [f"{indent}/** {clean} */"]


def generate_typescript(workspace: Workspace) -> str:
    blocks: list[str] = []
    for record in schema_records(workspace):
        schema = record.data["jsonSchema"]
        name = schema_component_name(record.id or "")
        properties = schema.get("properties", {})
        required = set(schema.get("required", []))
        lines = ts_doc(record.data.get("description") or schema.get("description"))
        lines.append(f"export interface {name} {{")
        if isinstance(properties, dict):
            for prop_name, prop_schema in properties.items():
                lines.extend(ts_doc(prop_schema.get("description") if isinstance(prop_schema, dict) else None, "  "))
                optional = "" if prop_name in required else "?"
                lines.append(f"  {ts_property_name(prop_name)}{optional}: {ts_type(prop_schema)};")
        lines.append("}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks) + "\n"


def python_literal(value: Any) -> str:
    return repr(value)


def python_nested_model_name(parent_name: str, prop_name: str) -> str:
    return f"{parent_name}{pascal_case(prop_name)}"


def python_type(
    schema: dict[str, Any],
    context_name: str | None = None,
    model_blocks: list[str] | None = None,
    seen_models: set[str] | None = None,
) -> str:
    ref = schema.get("$ref")
    if isinstance(ref, str):
        return schema_ref_name(ref) or "Any"
    enum = schema.get("enum")
    if isinstance(enum, list) and enum:
        return "Literal[" + ", ".join(python_literal(item) for item in enum) + "]"
    if "const" in schema:
        return "Literal[" + python_literal(schema["const"]) + "]"
    schema_type = schema.get("type")
    if isinstance(schema_type, list):
        non_null = [item for item in schema_type if item != "null"]
        if len(non_null) == 1:
            inner_type = python_type(
                {**schema, "type": non_null[0]},
                context_name,
                model_blocks,
                seen_models,
            )
            return f"Optional[{inner_type}]"
    if schema_type == "string":
        return "str"
    if schema_type == "integer":
        return "int"
    if schema_type == "number":
        return "float"
    if schema_type == "boolean":
        return "bool"
    if schema_type == "array":
        item_context = f"{context_name}Item" if context_name else None
        item_type = python_type(schema.get("items", {}), item_context, model_blocks, seen_models)
        return f"list[{item_type}]"
    if schema_type == "object":
        properties = schema.get("properties", {})
        if (
            context_name
            and isinstance(properties, dict)
            and properties
            and model_blocks is not None
            and seen_models is not None
        ):
            append_python_model_block(context_name, schema, model_blocks, seen_models)
            return context_name
        return "dict[str, Any]"
    return "Any"


def python_field_name(name: str) -> str:
    snake_name = re.sub(r"(?<!^)(?=[A-Z])", "_", name)
    field = sanitize_identifier(snake_name).lower()
    if keyword.iskeyword(field):
        return f"{field}_"
    return field


def optional_python_type(type_name: str) -> str:
    if type_name.startswith("Optional[") or type_name == "Any":
        return type_name
    return f"Optional[{type_name}]"


def append_python_model_block(
    name: str,
    schema: dict[str, Any],
    model_blocks: list[str],
    seen_models: set[str],
) -> None:
    if name in seen_models:
        return
    seen_models.add(name)

    properties = schema.get("properties", {})
    required = set(schema.get("required", []))
    lines = ["@dataclass", f"class {name}:"]
    required_lines: list[str] = []
    optional_lines: list[str] = []
    if isinstance(properties, dict):
        for prop_name, prop_schema in properties.items():
            description = (
                prop_schema.get("description") if isinstance(prop_schema, dict) else None
            )
            context_name = python_nested_model_name(name, prop_name)
            field_type = python_type(prop_schema, context_name, model_blocks, seen_models)
            line = f"    {python_field_name(prop_name)}: {field_type}"
            if isinstance(description, str) and description:
                line = f"    # {description}\n{line}"
            if prop_name in required:
                required_lines.append(line)
            else:
                optional_line = line.replace(
                    f": {field_type}",
                    f": {optional_python_type(field_type)}",
                )
                optional_lines.append(f"{optional_line} = None")
    field_lines = required_lines + optional_lines
    if field_lines:
        lines.extend(field_lines)
    else:
        lines.append("    pass")
    model_blocks.append("\n".join(lines))


def generate_python_models(workspace: Workspace) -> str:
    blocks = [
        "from __future__ import annotations",
        "",
        "from dataclasses import dataclass",
        "from typing import Any, Literal, Optional",
        "",
    ]
    model_blocks: list[str] = []
    seen_models: set[str] = set()
    for record in schema_records(workspace):
        schema = record.data["jsonSchema"]
        name = schema_component_name(record.id or "")
        append_python_model_block(name, schema, model_blocks, seen_models)
    for block in model_blocks:
        blocks.append(block)
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


def count_by_field(records: list[Record], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        value = record.data.get(field)
        key = value if isinstance(value, str) and value else "unspecified"
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: item[0]))


def reference_targets(
    record: Record,
    records_by_id: dict[str, Record],
    relationship: str | None = None,
) -> list[dict[str, str]]:
    targets: list[dict[str, str]] = []
    for item in record.data.get("references", []):
        if not isinstance(item, dict):
            continue
        if relationship is not None and item.get("type") != relationship:
            continue
        target_id = item.get("target")
        if not isinstance(target_id, str) or not target_id:
            continue
        target = records_by_id.get(target_id)
        targets.append(
            {
                "id": target_id,
                "kind": target.kind if target and target.kind else "unknown",
                "name": target.data.get("name", "") if target else "",
            }
        )
    return targets


def security_control_targets(record: Record, records_by_id: dict[str, Record]) -> list[dict[str, str]]:
    return reference_targets(record, records_by_id, "appliesTo")


def is_security_control_verified(record: Record) -> bool:
    verification = record.data.get("verification")
    if not isinstance(verification, dict):
        return False
    return (
        record.data.get("coverage") == "verified"
        and verification.get("method") != "not-verified"
        and isinstance(verification.get("evidence"), str)
        and bool(verification.get("evidence", "").strip())
    )


def accessibility_claim_targets(record: Record, records_by_id: dict[str, Record]) -> list[dict[str, str]]:
    return reference_targets(record, records_by_id, "appliesTo")


def is_accessibility_claim_verified(record: Record) -> bool:
    verification = record.data.get("verification")
    if not isinstance(verification, dict):
        return False
    return (
        record.data.get("coverage") == "verified"
        and verification.get("method") != "not-verified"
        and isinstance(verification.get("evidence"), str)
        and bool(verification.get("evidence", "").strip())
    )


def generate_security_report(workspace: Workspace) -> dict:
    controls = [record for record in workspace.records if record.kind == "security.control"]
    records_by_id = {record.id: record for record in workspace.records if record.id}
    control_entries: list[dict[str, Any]] = []
    verified_control_count = 0
    critical_unverified: list[str] = []

    for record in controls:
        verified = is_security_control_verified(record)
        if verified:
            verified_control_count += 1
        if record.data.get("riskLevel") == "critical" and not verified and record.id:
            critical_unverified.append(record.id)

        control_entries.append(
            {
                "id": record.id,
                "name": record.data.get("name"),
                "status": record.data.get("status"),
                "owner": record.data.get("owner"),
                "category": record.data.get("category"),
                "controlType": record.data.get("controlType"),
                "riskLevel": record.data.get("riskLevel"),
                "coverage": record.data.get("coverage"),
                "objective": record.data.get("objective"),
                "verified": verified,
                "verification": record.data.get("verification", {}),
                "targets": security_control_targets(record, records_by_id),
            }
        )

    return {
        "type": "security_report",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "verityVersion": __version__,
        "workspace": workspace.config.get("workspace", workspace.base_path.name),
        "workspacePath": str(workspace.base_path),
        "specVersion": workspace.config.get("specVersion"),
        "controlCount": len(controls),
        "summary": {
            "byCoverage": count_by_field(controls, "coverage"),
            "byRiskLevel": count_by_field(controls, "riskLevel"),
            "verifiedControls": verified_control_count,
            "criticalUnverified": critical_unverified,
        },
        "controls": control_entries,
    }


def generate_accessibility_report(workspace: Workspace) -> dict:
    claims = [record for record in workspace.records if record.kind == "accessibility.claim"]
    records_by_id = {record.id: record for record in workspace.records if record.id}
    claim_entries: list[dict[str, Any]] = []
    verified_claim_count = 0
    critical_unverified: list[str] = []
    claims_without_targets: list[str] = []
    missing_verification_dates: list[str] = []

    for record in claims:
        verified = is_accessibility_claim_verified(record)
        targets = accessibility_claim_targets(record, records_by_id)
        verification = record.data.get("verification", {})
        if verified:
            verified_claim_count += 1
        if record.data.get("impact") == "critical" and not verified and record.id:
            critical_unverified.append(record.id)
        if record.id and not targets:
            claims_without_targets.append(record.id)
        if record.id and (
            not isinstance(verification, dict)
            or not str(verification.get("lastVerified", "")).strip()
        ):
            missing_verification_dates.append(record.id)

        claim_entries.append(
            {
                "id": record.id,
                "name": record.data.get("name"),
                "status": record.data.get("status"),
                "owner": record.data.get("owner"),
                "standard": record.data.get("standard"),
                "criterion": record.data.get("criterion"),
                "level": record.data.get("level"),
                "userNeed": record.data.get("userNeed"),
                "surface": record.data.get("surface"),
                "impact": record.data.get("impact"),
                "coverage": record.data.get("coverage"),
                "verified": verified,
                "verification": verification if isinstance(verification, dict) else {},
                "assistiveTechnologies": record.data.get("assistiveTechnologies", []),
                "acceptanceCriteria": record.data.get("acceptanceCriteria", []),
                "targets": targets,
            }
        )

    missing_owners = [record.id for record in claims if record.id and owner_missing(record)]

    return {
        "type": "accessibility_report",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "verityVersion": __version__,
        "workspace": workspace.config.get("workspace", workspace.base_path.name),
        "workspacePath": str(workspace.base_path),
        "specVersion": workspace.config.get("specVersion"),
        "claimCount": len(claims),
        "summary": {
            "byOwner": count_by_field(claims, "owner"),
            "byStandard": count_by_field(claims, "standard"),
            "byLevel": count_by_field(claims, "level"),
            "byImpact": count_by_field(claims, "impact"),
            "byCoverage": count_by_field(claims, "coverage"),
            "verifiedClaims": verified_claim_count,
            "criticalUnverified": critical_unverified,
            "releaseGaps": {
                "criticalUnverified": critical_unverified,
                "claimsWithoutTargets": claims_without_targets,
                "missingOwners": missing_owners,
                "missingVerificationDates": missing_verification_dates,
            },
        },
        "claims": claim_entries,
    }


def is_compliance_mapping_verified(record: Record) -> bool:
    verification = record.data.get("verification")
    if not isinstance(verification, dict):
        return False
    return (
        verification.get("method") != "not-verified"
        and isinstance(verification.get("evidence"), str)
        and bool(verification.get("evidence", "").strip())
    )


def compliance_framework_name(record: Record) -> str:
    framework = record.data.get("framework")
    if isinstance(framework, dict):
        name = framework.get("name")
        if isinstance(name, str) and name:
            return name
    return "unspecified"


def compliance_requirement_key(record: Record) -> str:
    framework = record.data.get("framework")
    if not isinstance(framework, dict):
        return "unspecified"
    name = framework.get("name")
    requirement_id = framework.get("requirementId")
    if isinstance(name, str) and name and isinstance(requirement_id, str) and requirement_id:
        return f"{name}:{requirement_id}"
    if isinstance(requirement_id, str) and requirement_id:
        return requirement_id
    return "unspecified"


def count_compliance_field(records: list[Record], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        if field == "framework":
            key = compliance_framework_name(record)
        elif field == "requirement":
            key = compliance_requirement_key(record)
        else:
            value = record.data.get(field)
            key = value if isinstance(value, str) and value else "unspecified"
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: item[0]))


def compliance_target_summaries(
    record: Record,
    records_by_id: dict[str, Record],
) -> list[dict[str, Any]]:
    targets: list[dict[str, Any]] = []
    for item in record.data.get("references", []):
        if not isinstance(item, dict) or item.get("type") != "covers":
            continue
        target_id = item.get("target")
        if not isinstance(target_id, str) or not target_id:
            continue
        target = records_by_id.get(target_id)
        targets.append(
            {
                "id": target_id,
                "kind": target.kind if target and target.kind else "unknown",
                "name": target.data.get("name", "") if target else "",
                "owner": target.data.get("owner", "") if target else "",
                "status": target.data.get("status", "") if target else "",
            }
        )
    return targets


def compliance_security_evidence(record: Record) -> dict[str, Any]:
    return {
        "id": record.id,
        "name": record.data.get("name"),
        "owner": record.data.get("owner"),
        "riskLevel": record.data.get("riskLevel"),
        "coverage": record.data.get("coverage"),
        "verified": is_security_control_verified(record),
        "verification": record.data.get("verification", {}),
    }


def compliance_accessibility_evidence(record: Record) -> dict[str, Any]:
    return {
        "id": record.id,
        "name": record.data.get("name"),
        "owner": record.data.get("owner"),
        "standard": record.data.get("standard"),
        "criterion": record.data.get("criterion"),
        "level": record.data.get("level"),
        "impact": record.data.get("impact"),
        "coverage": record.data.get("coverage"),
        "verified": is_accessibility_claim_verified(record),
        "verification": record.data.get("verification", {}),
    }


def compliance_observability_evidence(
    record: Record,
    records_by_id: dict[str, Record],
) -> dict[str, Any]:
    evidence: dict[str, Any] = {
        "id": record.id,
        "kind": record.kind,
        "name": record.data.get("name"),
        "owner": record.data.get("owner"),
    }
    if record.kind == "observability.telemetry":
        evidence.update(
            {
                "signalName": record.data.get("signalName"),
                "emittedBy": record.data.get("emittedBy"),
                "payloadSchema": record.data.get("payloadSchema"),
            }
        )
    elif record.kind == "observability.metric":
        evidence.update(
            {
                "metricName": record.data.get("metricName"),
                "unit": record.data.get("unit"),
                "aggregation": record.data.get("aggregation"),
                "sources": reference_targets(record, records_by_id, "derivedFrom"),
            }
        )
    elif record.kind == "observability.dashboard":
        evidence.update(
            {
                "url": record.data.get("url"),
                "audience": record.data.get("audience"),
                "metrics": reference_targets(record, records_by_id, "displays"),
                "alerts": reference_targets(record, records_by_id, "tracks"),
            }
        )
    elif record.kind == "observability.alert":
        evidence.update(
            {
                "severity": record.data.get("severity"),
                "condition": record.data.get("condition"),
                "runbook": record.data.get("runbook"),
                "metrics": reference_targets(record, records_by_id, "firesOn"),
            }
        )
    return evidence


def compliance_evidence_groups(
    targets: list[dict[str, Any]],
    records_by_id: dict[str, Record],
) -> dict[str, list[dict[str, Any]]]:
    evidence: dict[str, list[dict[str, Any]]] = {
        "securityControls": [],
        "accessibilityClaims": [],
        "observabilitySignals": [],
        "otherTargets": [],
    }
    for target in targets:
        record_id = target.get("id")
        if not isinstance(record_id, str):
            continue
        record = records_by_id.get(record_id)
        if not record:
            evidence["otherTargets"].append(target)
            continue
        if record.kind == "security.control":
            evidence["securityControls"].append(compliance_security_evidence(record))
        elif record.kind == "accessibility.claim":
            evidence["accessibilityClaims"].append(compliance_accessibility_evidence(record))
        elif record.kind and record.kind.startswith("observability."):
            evidence["observabilitySignals"].append(
                compliance_observability_evidence(record, records_by_id)
            )
        else:
            evidence["otherTargets"].append(target)
    return evidence


def generate_compliance_matrix(workspace: Workspace) -> dict:
    mappings = [record for record in workspace.records if record.kind == "compliance.mapping"]
    records_by_id = {record.id: record for record in workspace.records if record.id}
    matrix: list[dict[str, Any]] = []
    verified_mapping_count = 0
    mappings_without_targets: list[str] = []
    mappings_without_evidence: list[str] = []
    reviewed_unverified: list[str] = []
    targets_without_owners: list[str] = []

    for record in mappings:
        verified = is_compliance_mapping_verified(record)
        if verified:
            verified_mapping_count += 1
        targets = compliance_target_summaries(record, records_by_id)
        verification = record.data.get("verification", {})
        evidence = verification.get("evidence") if isinstance(verification, dict) else None
        has_evidence = isinstance(evidence, str) and bool(evidence.strip())

        if record.id and not targets:
            mappings_without_targets.append(record.id)
        if record.id and not has_evidence:
            mappings_without_evidence.append(record.id)
        if record.id and record.data.get("coverage") == "reviewed" and not verified:
            reviewed_unverified.append(record.id)
        for target in targets:
            target_id = target.get("id")
            target_record = records_by_id.get(target_id) if isinstance(target_id, str) else None
            if isinstance(target_id, str) and (
                target_record is None or owner_missing(target_record)
            ):
                targets_without_owners.append(target_id)

        matrix.append(
            {
                "id": record.id,
                "name": record.data.get("name"),
                "status": record.data.get("status"),
                "owner": record.data.get("owner"),
                "framework": record.data.get("framework", {}),
                "requirement": compliance_requirement_key(record),
                "mappingType": record.data.get("mappingType"),
                "coverage": record.data.get("coverage"),
                "attestation": record.data.get("attestation"),
                "verified": verified,
                "verification": verification if isinstance(verification, dict) else {},
                "targets": targets,
                "evidence": compliance_evidence_groups(targets, records_by_id),
            }
        )

    missing_owners = [record.id for record in mappings if record.id and owner_missing(record)]

    return {
        "type": "compliance_matrix",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "verityVersion": __version__,
        "workspace": workspace.config.get("workspace", workspace.base_path.name),
        "workspacePath": str(workspace.base_path),
        "specVersion": workspace.config.get("specVersion"),
        "mappingCount": len(mappings),
        "summary": {
            "byOwner": count_by_field(mappings, "owner"),
            "byFramework": count_compliance_field(mappings, "framework"),
            "byRequirement": count_compliance_field(mappings, "requirement"),
            "byMappingType": count_by_field(mappings, "mappingType"),
            "byCoverage": count_by_field(mappings, "coverage"),
            "verifiedMappings": verified_mapping_count,
            "releaseGaps": {
                "mappingsWithoutTargets": mappings_without_targets,
                "mappingsWithoutEvidence": mappings_without_evidence,
                "reviewedUnverified": reviewed_unverified,
                "missingOwners": missing_owners,
                "targetsWithoutOwners": sorted(set(targets_without_owners)),
            },
        },
        "matrix": matrix,
    }


def has_reference(record: Record, relationship: str) -> bool:
    return bool(reference_targets(record, {}, relationship))


def owner_missing(record: Record) -> bool:
    owner = record.data.get("owner")
    return owner in {"unknown", "todo", "tbd", ""}


def telemetry_metric_ids(metrics: list[Record]) -> set[str]:
    telemetry_ids: set[str] = set()
    for metric in metrics:
        for item in metric.data.get("references", []):
            if isinstance(item, dict) and item.get("type") == "derivedFrom":
                target = item.get("target")
                if isinstance(target, str) and target:
                    telemetry_ids.add(target)
    return telemetry_ids


def generate_observability_report(workspace: Workspace) -> dict:
    records_by_id = {record.id: record for record in workspace.records if record.id}
    telemetry = [record for record in workspace.records if record.kind == "observability.telemetry"]
    metrics = [record for record in workspace.records if record.kind == "observability.metric"]
    dashboards = [record for record in workspace.records if record.kind == "observability.dashboard"]
    alerts = [record for record in workspace.records if record.kind == "observability.alert"]
    observability_records = telemetry + metrics + dashboards + alerts

    telemetry_with_metrics = telemetry_metric_ids(metrics)
    telemetry_without_metrics = [
        record.id for record in telemetry if record.id and record.id not in telemetry_with_metrics
    ]
    metrics_without_telemetry = [
        record.id for record in metrics if record.id and not has_reference(record, "derivedFrom")
    ]
    dashboards_without_alerts = [
        record.id for record in dashboards if record.id and not has_reference(record, "tracks")
    ]
    alerts_without_runbooks = [
        record.id
        for record in alerts
        if record.id and not str(record.data.get("runbook", "")).strip()
    ]
    missing_owners = [record.id for record in observability_records if record.id and owner_missing(record)]

    return {
        "type": "observability_report",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "verityVersion": __version__,
        "workspace": workspace.config.get("workspace", workspace.base_path.name),
        "workspacePath": str(workspace.base_path),
        "specVersion": workspace.config.get("specVersion"),
        "signalCount": len(observability_records),
        "summary": {
            "telemetry": len(telemetry),
            "metrics": len(metrics),
            "dashboards": len(dashboards),
            "alerts": len(alerts),
            "byOwner": count_by_field(observability_records, "owner"),
            "alertsBySeverity": count_by_field(alerts, "severity"),
            "releaseGaps": {
                "telemetryWithoutMetrics": telemetry_without_metrics,
                "metricsWithoutTelemetry": metrics_without_telemetry,
                "dashboardsWithoutAlerts": dashboards_without_alerts,
                "alertsWithoutRunbooks": alerts_without_runbooks,
                "missingOwners": missing_owners,
            },
        },
        "telemetry": [
            {
                "id": record.id,
                "name": record.data.get("name"),
                "owner": record.data.get("owner"),
                "signalName": record.data.get("signalName"),
                "emittedBy": record.data.get("emittedBy"),
                "payloadSchema": record.data.get("payloadSchema"),
            }
            for record in telemetry
        ],
        "metrics": [
            {
                "id": record.id,
                "name": record.data.get("name"),
                "owner": record.data.get("owner"),
                "metricName": record.data.get("metricName"),
                "unit": record.data.get("unit"),
                "aggregation": record.data.get("aggregation"),
                "sources": reference_targets(record, records_by_id, "derivedFrom"),
            }
            for record in metrics
        ],
        "dashboards": [
            {
                "id": record.id,
                "name": record.data.get("name"),
                "owner": record.data.get("owner"),
                "url": record.data.get("url"),
                "audience": record.data.get("audience"),
                "metrics": reference_targets(record, records_by_id, "displays"),
                "alerts": reference_targets(record, records_by_id, "tracks"),
            }
            for record in dashboards
        ],
        "alerts": [
            {
                "id": record.id,
                "name": record.data.get("name"),
                "owner": record.data.get("owner"),
                "ownerTeam": record.data.get("ownerTeam"),
                "severity": record.data.get("severity"),
                "condition": record.data.get("condition"),
                "runbook": record.data.get("runbook"),
                "metrics": reference_targets(record, records_by_id, "firesOn"),
            }
            for record in alerts
        ],
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
