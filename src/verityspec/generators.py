from __future__ import annotations

import json
import keyword
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from . import __version__
from .diffing import SEVERITY_LEVELS, diff_workspaces
from .explain import ISSUE_EXPLANATIONS
from .graph import build_graph
from .issues import Issue, issue_count
from .packs import Pack, PackRegistry, ReferenceRule, SchemaBinding
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


def generated_at_value(value: str | None = None) -> str:
    if value is None:
        return datetime.now(timezone.utc).isoformat()
    candidate = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        datetime.fromisoformat(candidate)
    except ValueError as exc:
        raise ValueError("--generated-at must be an ISO 8601 datetime.") from exc
    return value


def issue_code_category(code: str) -> str:
    return code.split(".", 1)[0] if "." in code else code


def generate_issue_code_catalog(generated_at: str | None = None) -> dict[str, Any]:
    issue_codes = [
        {
            "code": code,
            "category": issue_code_category(code),
            "title": explanation.get("title", ""),
            "severity": explanation.get("severity", ""),
            "description": explanation.get("description", ""),
            "resolution": explanation.get("resolution", ""),
        }
        for code, explanation in sorted(ISSUE_EXPLANATIONS.items(), key=lambda item: item[0])
    ]
    severity_counts = {
        severity: sum(1 for item in issue_codes if item["severity"] == severity)
        for severity in SEVERITY_LEVELS
        if any(item["severity"] == severity for item in issue_codes)
    }
    category_counts = {
        category: sum(1 for item in issue_codes if item["category"] == category)
        for category in sorted({item["category"] for item in issue_codes})
    }

    return {
        "type": "issue_code_catalog",
        "generatedAt": generated_at_value(generated_at),
        "verityVersion": __version__,
        "source": "verity explain",
        "summary": {
            "issueCodeCount": len(issue_codes),
            "severityCounts": severity_counts,
            "categoryCounts": category_counts,
            "categories": sorted(category_counts),
            "severities": sorted(
                severity_counts,
                key=lambda item: SEVERITY_LEVELS.index(item) if item in SEVERITY_LEVELS else 99,
            ),
        },
        "issueCodes": issue_codes,
    }


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


def sorted_strings(values: Any) -> list[str]:
    if not isinstance(values, list):
        return []
    return sorted(value for value in values if isinstance(value, str))


def sorted_mapping(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        return {}
    return {key: value[key] for key in sorted(value)}


def pack_source(pack: Pack) -> str:
    return pack.source


def schema_capability_summary(binding: SchemaBinding) -> dict[str, Any]:
    return {
        "kind": binding.kind,
        "packId": binding.pack_id,
        "path": str(binding.path),
    }


def readiness_gate_summary(gate: dict[str, Any], pack_id: str) -> dict[str, Any]:
    rules = [
        {
            "id": rule.get("id", ""),
            "code": rule.get("code", ""),
            "when": rule.get("when", {}),
            "must": rule.get("must", []),
            "message": rule.get("message", ""),
        }
        for rule in gate.get("rules", [])
        if isinstance(rule, dict)
    ]
    return {
        "id": gate.get("id", ""),
        "kind": gate.get("kind", ""),
        "packId": pack_id,
        "required": sorted_strings(gate.get("required", [])),
        "minItems": sorted_mapping(gate.get("minItems", {})),
        "ruleCount": len(rules),
        "rules": sorted(rules, key=lambda item: (str(item["id"]), str(item["code"]))),
    }


def reference_rule_summary(rule: ReferenceRule) -> dict[str, Any]:
    return {
        "sourceKind": rule.source_kind,
        "relationship": rule.relationship,
        "targetKind": rule.target_kind,
        "packId": rule.pack_id,
    }


def generator_metadata_summary(metadata: dict[str, Any], pack_id: str) -> dict[str, Any]:
    return {
        "id": metadata.get("id", ""),
        "packId": pack_id,
        "name": metadata.get("name", ""),
        "description": metadata.get("description", ""),
        "artifactType": metadata.get("artifactType", ""),
        "outputFormats": sorted_strings(metadata.get("outputFormats", [])),
        "recordKinds": sorted_strings(metadata.get("recordKinds", [])),
    }


def generator_capability_index(packs: list[Pack]) -> list[dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for pack in packs:
        for metadata in pack.generator_metadata:
            generator_id = metadata.get("id")
            if not isinstance(generator_id, str):
                continue
            entry = indexed.setdefault(
                generator_id,
                {
                    "id": generator_id,
                    "packIds": set(),
                    "declarationCount": 0,
                    "artifactTypes": set(),
                    "outputFormats": set(),
                    "recordKinds": set(),
                },
            )
            entry["packIds"].add(pack.id)
            entry["declarationCount"] += 1
            artifact_type = metadata.get("artifactType")
            if isinstance(artifact_type, str) and artifact_type:
                entry["artifactTypes"].add(artifact_type)
            for output_format in sorted_strings(metadata.get("outputFormats", [])):
                entry["outputFormats"].add(output_format)
            for record_kind in sorted_strings(metadata.get("recordKinds", [])):
                entry["recordKinds"].add(record_kind)

    return [
        {
            "id": generator_id,
            "packIds": sorted(entry["packIds"]),
            "declarationCount": entry["declarationCount"],
            "artifactTypes": sorted(entry["artifactTypes"]),
            "outputFormats": sorted(entry["outputFormats"]),
            "recordKinds": sorted(entry["recordKinds"]),
        }
        for generator_id, entry in sorted(indexed.items(), key=lambda item: item[0])
    ]


def generate_pack_capability_index(
    workspace: Workspace,
    registry: PackRegistry,
    generated_at: str | None = None,
) -> dict:
    packs = [pack for _, pack in sorted(registry.packs.items(), key=lambda item: item[0])]
    pack_sources = {pack.id: pack_source(pack) for pack in packs}
    readiness_gates = [
        readiness_gate_summary(gate, pack.id)
        for pack in packs
        for gate in pack.readiness_gates
    ]
    reference_rules = [
        reference_rule_summary(rule)
        for rule in sorted(
            registry.reference_rules,
            key=lambda item: (
                item.pack_id,
                item.source_kind,
                item.relationship,
                item.target_kind,
            ),
        )
    ]
    generators = generator_capability_index(packs)
    generator_declaration_count = sum(len(pack.generator_metadata) for pack in packs)
    conditional_rule_count = sum(
        len(gate.get("rules", []))
        for pack in packs
        for gate in pack.readiness_gates
        if isinstance(gate.get("rules", []), list)
    )

    return {
        "type": "pack_capability_index",
        "generatedAt": generated_at_value(generated_at),
        "verityVersion": __version__,
        "workspace": workspace.config.get("workspace", workspace.base_path.name),
        "workspacePath": str(workspace.base_path),
        "specVersion": workspace.config.get("specVersion"),
        "packs": workspace.pack_ids,
        "packPaths": workspace.pack_paths,
        "loadedPacks": [pack.id for pack in packs],
        "summary": {
            "packCount": len(packs),
            "builtInPackCount": sum(1 for source in pack_sources.values() if source == "built-in"),
            "installedPackCount": sum(1 for source in pack_sources.values() if source == "installed"),
            "externalPackCount": sum(1 for source in pack_sources.values() if source == "external"),
            "schemaCount": len(registry.schemas),
            "readinessGateCount": len(readiness_gates),
            "conditionalReadinessRuleCount": conditional_rule_count,
            "referenceRuleCount": len(reference_rules),
            "generatorCount": len(generators),
            "generatorDeclarationCount": generator_declaration_count,
            "recordKinds": registry.known_kinds,
            "generators": [generator["id"] for generator in generators],
        },
        "capabilities": {
            "schemas": [
                schema_capability_summary(binding)
                for _, binding in sorted(registry.schemas.items(), key=lambda item: item[0])
            ],
            "readinessGates": sorted(
                readiness_gates,
                key=lambda item: (str(item["packId"]), str(item["kind"]), str(item["id"])),
            ),
            "referenceRules": reference_rules,
            "generators": generators,
        },
        "packDetails": [
            {
                "id": pack.id,
                "version": pack.version,
                "name": pack.name,
                "description": pack.description,
                "source": pack_sources[pack.id],
                "path": str(pack.path),
                "schemaCount": len(pack.schemas),
                "readinessGateCount": len(pack.readiness_gates),
                "referenceRuleCount": len(pack.reference_rules),
                "generatorCount": len(pack.generator_metadata),
                "schemas": [
                    schema_capability_summary(binding)
                    for _, binding in sorted(pack.schemas.items(), key=lambda item: item[0])
                ],
                "readinessGates": [
                    readiness_gate_summary(gate, pack.id)
                    for gate in sorted(
                        pack.readiness_gates,
                        key=lambda item: (str(item.get("kind", "")), str(item.get("id", ""))),
                    )
                ],
                "referenceRules": [
                    reference_rule_summary(rule)
                    for rule in sorted(
                        pack.reference_rules,
                        key=lambda item: (
                            item.source_kind,
                            item.relationship,
                            item.target_kind,
                        ),
                    )
                ],
                "generators": [
                    generator_metadata_summary(metadata, pack.id)
                    for metadata in sorted(
                        pack.generator_metadata,
                        key=lambda item: str(item.get("id", "")),
                    )
                ],
            }
            for pack in packs
        ],
    }


def generate_validation_report(
    workspace: Workspace,
    registry: PackRegistry,
    issues: list[Issue],
    generated_at: str | None = None,
) -> dict:
    errors = issue_count(issues, "error")
    warnings = issue_count(issues, "warning")
    return {
        "type": "validation_report",
        "generatedAt": generated_at_value(generated_at),
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


SURFACE_DEFINITIONS: list[dict[str, Any]] = [
    {
        "id": "core",
        "name": "Core",
        "packId": "verity.core",
        "recordKinds": ["product", "schema.object"],
        "productRelationships": [],
    },
    {
        "id": "api",
        "name": "API",
        "packId": "verity.pack.api",
        "recordKinds": ["api.endpoint"],
        "productRelationships": ["exposes"],
    },
    {
        "id": "cli",
        "name": "CLI",
        "packId": "verity.pack.cli",
        "recordKinds": ["cli.command"],
        "productRelationships": ["ships"],
    },
    {
        "id": "events",
        "name": "Events",
        "packId": "verity.pack.events",
        "recordKinds": ["event.message"],
        "productRelationships": ["emits"],
    },
    {
        "id": "security",
        "name": "Security",
        "packId": "verity.pack.security",
        "recordKinds": ["security.control"],
        "productRelationships": ["securedBy"],
    },
    {
        "id": "accessibility",
        "name": "Accessibility",
        "packId": "verity.pack.accessibility",
        "recordKinds": ["accessibility.claim"],
        "productRelationships": ["accessibilityCoveredBy"],
    },
    {
        "id": "observability",
        "name": "Observability",
        "packId": "verity.pack.observability",
        "recordKinds": [
            "observability.telemetry",
            "observability.metric",
            "observability.dashboard",
            "observability.alert",
        ],
        "productRelationships": ["observes"],
    },
    {
        "id": "compliance",
        "name": "Compliance",
        "packId": "verity.pack.compliance",
        "recordKinds": ["compliance.mapping"],
        "productRelationships": ["complianceMappedBy"],
    },
    {
        "id": "deployment",
        "name": "Deployment",
        "packId": "verity.pack.deployment",
        "recordKinds": ["deployment.runtime", "deployment.target"],
        "productRelationships": ["deploysTo"],
    },
    {
        "id": "game-core",
        "name": "Game Core",
        "packId": "verity.pack.game-core",
        "recordKinds": [
            "game.product",
            "game.mode",
            "game.loop",
            "game.prototype-scope",
        ],
        "productRelationships": ["describes"],
    },
    {
        "id": "game-assets",
        "name": "Game Assets",
        "packId": "verity.pack.game-assets",
        "recordKinds": [
            "game.gdd-source",
            "game.visual-identity",
            "game.identity-image",
            "game.concept-art",
        ],
        "productRelationships": ["hasGameAssets"],
    },
    {
        "id": "unity",
        "name": "Unity",
        "packId": "verity.pack.unity",
        "recordKinds": [
            "unity.project",
            "unity.package-dependency",
            "unity.package",
            "unity.shared-library",
            "unity.prefab",
            "unity.asmdef",
            "unity.scanner",
            "unity.validation-runner",
            "unity.readiness-dashboard",
            "unity.agent-context-exporter",
            "unity.scene",
            "unity.build-target",
        ],
        "productRelationships": ["hasUnityProject"],
    },
    {
        "id": "godot",
        "name": "Godot",
        "packId": "verity.pack.godot",
        "recordKinds": [
            "godot.project",
            "godot.addon",
            "godot.shared-library",
            "godot.scene",
            "godot.node-contract",
            "godot.resource",
            "godot.script",
            "godot.autoload",
            "godot.input-action",
            "godot.export-preset",
            "godot.scanner",
            "godot.validation-runner",
            "godot.readiness-dashboard",
            "godot.agent-context-exporter",
        ],
        "productRelationships": ["hasGodotProject"],
    },
    {
        "id": "unreal",
        "name": "Unreal",
        "packId": "verity.pack.unreal",
        "recordKinds": [
            "unreal.project",
            "unreal.plugin",
            "unreal.module",
            "unreal.target",
            "unreal.map",
            "unreal.blueprint",
            "unreal.data-asset",
            "unreal.gameplay-tag",
            "unreal.input-action",
            "unreal.scanner",
            "unreal.validation-runner",
            "unreal.readiness-dashboard",
            "unreal.agent-context-exporter",
        ],
        "productRelationships": ["hasUnrealProject"],
    },
    {
        "id": "gameplay",
        "name": "Gameplay",
        "packId": "verity.pack.gameplay",
        "recordKinds": [
            "game.mechanic",
            "game.ability",
            "game.rule",
            "game.encounter",
        ],
        "productRelationships": ["hasGameplay"],
    },
    {
        "id": "content",
        "name": "Content",
        "packId": "verity.pack.content",
        "recordKinds": [
            "game.content-item",
            "game.level",
            "game.loot-table",
            "game.content-manifest",
        ],
        "productRelationships": ["hasContentManifest"],
    },
    {
        "id": "economy",
        "name": "Economy",
        "packId": "verity.pack.economy",
        "recordKinds": [
            "economy.currency",
            "economy.source",
            "economy.sink",
            "economy.reward",
            "economy.offer",
        ],
        "productRelationships": ["hasEconomy"],
    },
    {
        "id": "progression",
        "name": "Progression",
        "packId": "verity.pack.progression",
        "recordKinds": [
            "progression.xp-model",
            "progression.level",
            "progression.unlock",
            "progression.track",
            "progression.gate",
        ],
        "productRelationships": ["hasProgressionTrack"],
    },
    {
        "id": "product-delivery",
        "name": "Product Delivery",
        "packId": "verity.pack.product-delivery",
        "recordKinds": [
            "product.scope",
            "commercial.posture",
            "project-management.model",
            "decision.record",
            "readiness.profile",
            "evidence.requirement",
            "release.process",
            "operations.model",
            "support.policy",
            "maintenance.policy",
            "archive.policy",
            "decommission.policy",
            "scanner.capability",
            "generator.capability",
            "validation.runner",
            "editor.surface",
            "agent-context.exporter",
        ],
        "productRelationships": ["hasProductScope"],
    },
    {
        "id": "mobile",
        "name": "Mobile",
        "packId": "verity.pack.mobile",
        "recordKinds": [
            "mobile.app-release",
            "mobile.store-listing",
            "mobile.privacy-policy",
            "mobile.apple-privacy-details",
            "mobile.google-play-data-safety",
            "mobile.att-consent",
            "mobile.sdk-inventory",
            "mobile.monetization-posture",
            "mobile.entitlement",
            "mobile.soft-launch",
            "mobile.launch-candidate",
            "mobile.compatibility-matrix",
        ],
        "productRelationships": ["hasMobileRelease"],
    },
    {
        "id": "liveops",
        "name": "LiveOps",
        "packId": "verity.pack.liveops",
        "recordKinds": [
            "liveops.config",
            "liveops.remote-config",
            "liveops.rollback-plan",
            "liveops.analytics-taxonomy",
            "liveops.support-category",
            "liveops.save-migration-policy",
            "liveops.decommission-plan",
            "liveops.data-deletion-policy",
            "liveops.archive-handling",
        ],
        "productRelationships": ["hasLiveOpsConfig"],
    },
    {
        "id": "evidence",
        "name": "Evidence",
        "packId": "verity.pack.evidence",
        "recordKinds": [
            "evidence.test",
            "evidence.ci-run",
            "evidence.build",
            "evidence.review",
            "evidence.screenshot",
            "evidence.video",
            "evidence.qa",
            "evidence.playtest",
            "evidence.certification-checklist",
            "evidence.artifact",
        ],
        "productRelationships": ["hasEvidence"],
    },
]
PRODUCT_SURFACE_IDS = [surface["id"] for surface in SURFACE_DEFINITIONS if surface["id"] != "core"]


def coverage_record_summary(record: Record) -> dict[str, Any]:
    return {
        "id": record.id,
        "kind": record.kind,
        "name": record.data.get("name"),
        "status": record.data.get("status"),
        "owner": record.data.get("owner"),
    }


def coverage_reference_summary(
    product: Record,
    item: dict[str, Any],
    records_by_id: dict[str, Record],
) -> dict[str, Any]:
    target_id = item.get("target")
    target = records_by_id.get(target_id) if isinstance(target_id, str) else None
    return {
        "productId": product.id,
        "relationship": item.get("type"),
        "targetId": target_id,
        "targetKind": target.kind if target else "unknown",
        "targetName": target.data.get("name", "") if target else "",
    }


def generate_coverage_dashboard(workspace: Workspace, generated_at: str | None = None) -> dict:
    records_by_kind: dict[str, list[Record]] = {}
    for record in workspace.records:
        if record.kind:
            records_by_kind.setdefault(record.kind, []).append(record)
    records_by_id = {record.id: record for record in workspace.records if record.id}
    products = sorted(
        [record for record in workspace.records if record.kind == "product"],
        key=lambda record: record.id or "",
    )
    relationship_to_surface = {
        relationship: surface["id"]
        for surface in SURFACE_DEFINITIONS
        for relationship in surface["productRelationships"]
    }

    surface_entries: list[dict[str, Any]] = []
    for surface in SURFACE_DEFINITIONS:
        records = [
            record
            for kind in surface["recordKinds"]
            for record in records_by_kind.get(kind, [])
        ]
        product_references = []
        for product in products:
            for item in product.data.get("references", []):
                if not isinstance(item, dict):
                    continue
                if item.get("type") not in surface["productRelationships"]:
                    continue
                product_references.append(coverage_reference_summary(product, item, records_by_id))

        surface_entries.append(
            {
                "id": surface["id"],
                "name": surface["name"],
                "packId": surface["packId"],
                "packLoaded": surface["packId"] in workspace.pack_ids,
                "recordKinds": surface["recordKinds"],
                "productRelationships": surface["productRelationships"],
                "recordCount": len(records),
                "covered": bool(records),
                "records": [
                    coverage_record_summary(record)
                    for record in sorted(records, key=lambda item: item.id or "")
                ],
                "productReferences": sorted(
                    product_references,
                    key=lambda item: (
                        str(item.get("productId", "")),
                        str(item.get("relationship", "")),
                        str(item.get("targetId", "")),
                    ),
                ),
            }
        )

    product_entries: list[dict[str, Any]] = []
    products_without_surface_references: list[str] = []
    product_surface_gaps: list[dict[str, Any]] = []
    for product in products:
        refs_by_surface: dict[str, list[dict[str, Any]]] = {surface_id: [] for surface_id in PRODUCT_SURFACE_IDS}
        for item in product.data.get("references", []):
            if not isinstance(item, dict):
                continue
            relationship = item.get("type")
            surface_id = relationship_to_surface.get(relationship)
            if surface_id is None:
                continue
            refs_by_surface[surface_id].append(coverage_reference_summary(product, item, records_by_id))

        missing = [
            surface_id
            for surface_id in PRODUCT_SURFACE_IDS
            if not refs_by_surface[surface_id]
        ]
        if product.id and len(missing) == len(PRODUCT_SURFACE_IDS):
            products_without_surface_references.append(product.id)
        if product.id and missing:
            product_surface_gaps.append(
                {
                    "productId": product.id,
                    "missingSurfaces": missing,
                }
            )
        product_entries.append(
            {
                "id": product.id,
                "name": product.data.get("name"),
                "status": product.data.get("status"),
                "owner": product.data.get("owner"),
                "surfaceReferences": {
                    surface_id: refs_by_surface[surface_id]
                    for surface_id in PRODUCT_SURFACE_IDS
                },
                "missingSurfaces": missing,
            }
        )

    surface_records = {
        surface["id"]: sum(
            len(records_by_kind.get(kind, []))
            for kind in surface["recordKinds"]
        )
        for surface in SURFACE_DEFINITIONS
        if surface["id"] != "core"
    }
    covered_surface_ids = [
        surface_id for surface_id, count in surface_records.items() if count > 0
    ]
    missing_surface_records = [
        surface_id for surface_id, count in surface_records.items() if count == 0
    ]
    loaded_packs_without_surface_records = [
        surface["id"]
        for surface in SURFACE_DEFINITIONS
        if surface["id"] != "core"
        and surface["packId"] in workspace.pack_ids
        and surface_records[surface["id"]] == 0
    ]
    coverage_percent = (
        round((len(covered_surface_ids) / len(PRODUCT_SURFACE_IDS)) * 100, 2)
        if PRODUCT_SURFACE_IDS
        else 100.0
    )

    return {
        "type": "coverage_dashboard",
        "generatedAt": generated_at_value(generated_at),
        "verityVersion": __version__,
        "workspace": workspace.config.get("workspace", workspace.base_path.name),
        "workspacePath": str(workspace.base_path),
        "specVersion": workspace.config.get("specVersion"),
        "packs": workspace.pack_ids,
        "recordCount": len(workspace.records),
        "productCount": len(products),
        "summary": {
            "trackedSurfaces": len(PRODUCT_SURFACE_IDS),
            "loadedSurfacePacks": sum(
                1
                for surface in SURFACE_DEFINITIONS
                if surface["id"] != "core" and surface["packId"] in workspace.pack_ids
            ),
            "coveredSurfaces": len(covered_surface_ids),
            "coveragePercent": coverage_percent,
            "bySurface": dict(sorted(surface_records.items(), key=lambda item: item[0])),
            "byRecordKind": {
                kind: len(records)
                for kind, records in sorted(records_by_kind.items(), key=lambda item: item[0])
            },
            "releaseGaps": {
                "missingSurfaceRecords": missing_surface_records,
                "loadedPacksWithoutSurfaceRecords": loaded_packs_without_surface_records,
                "productsWithoutSurfaceReferences": products_without_surface_references,
                "productSurfaceGaps": product_surface_gaps,
            },
        },
        "surfaces": surface_entries,
        "products": product_entries,
    }


def workspace_report_summary(workspace: Workspace) -> dict[str, Any]:
    return {
        "workspace": workspace.config.get("workspace", workspace.base_path.name),
        "workspacePath": str(workspace.base_path),
        "specVersion": workspace.config.get("specVersion"),
        "packs": workspace.pack_ids,
        "recordCount": len(workspace.records),
    }


def impact_record_summary(record_id: str, data: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": record_id,
        "kind": data.get("kind"),
        "name": data.get("name"),
        "status": data.get("status"),
        "owner": data.get("owner"),
    }


def graph_reference_indexes(
    graph: dict[str, Any],
    records_by_id: dict[str, dict[str, Any]],
) -> tuple[dict[str, set[str]], dict[str, set[str]], list[dict[str, str]]]:
    downstream: dict[str, set[str]] = {}
    upstream: dict[str, set[str]] = {}
    missing: list[dict[str, str]] = []
    for edge in graph.get("edges", []):
        source = edge.get("source")
        target = edge.get("target")
        if not isinstance(source, str) or not isinstance(target, str):
            continue
        if source not in records_by_id:
            continue
        if target not in records_by_id:
            missing.append(
                {
                    "source": source,
                    "target": target,
                    "relationship": str(edge.get("relationship", "")),
                    "field": str(edge.get("field", "")),
                }
            )
            continue
        downstream.setdefault(source, set()).add(target)
        upstream.setdefault(target, set()).add(source)
    return downstream, upstream, sorted(
        missing,
        key=lambda item: (
            item["source"],
            item["relationship"],
            item["target"],
            item["field"],
        ),
    )


def reachable_record_ids(start: str, adjacency: dict[str, set[str]]) -> set[str]:
    seen: set[str] = set()
    pending = list(sorted(adjacency.get(start, set())))
    while pending:
        record_id = pending.pop(0)
        if record_id == start or record_id in seen:
            continue
        seen.add(record_id)
        for next_id in sorted(adjacency.get(record_id, set())):
            if next_id not in seen and next_id != start:
                pending.append(next_id)
    return seen


def impact_direction_summary(
    record_id: str,
    adjacency: dict[str, set[str]],
    records_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    direct_ids = sorted(adjacency.get(record_id, set()))
    all_ids = sorted(reachable_record_ids(record_id, adjacency))
    transitive_ids = sorted(set(all_ids) - set(direct_ids))
    return {
        "directRecordIds": direct_ids,
        "transitiveRecordIds": transitive_ids,
        "recordIds": all_ids,
        "records": [
            impact_record_summary(impacted_id, records_by_id[impacted_id])
            for impacted_id in all_ids
        ],
    }


def change_by_record(diff: dict[str, Any]) -> dict[str, dict[str, Any]]:
    changes: dict[str, dict[str, Any]] = {}
    for change in diff.get("changes", []):
        record_id = change.get("recordId")
        if isinstance(record_id, str):
            changes[record_id] = change
    return changes


def changed_record_ids(diff: dict[str, Any]) -> list[str]:
    record_ids: set[str] = set()
    for key in ["added", "removed", "changed"]:
        values = diff.get(key, [])
        if isinstance(values, list):
            record_ids.update(item for item in values if isinstance(item, str))
    return sorted(record_ids)


def graph_context_for_change(
    record_id: str,
    diff: dict[str, Any],
    old_context: dict[str, Any],
    new_context: dict[str, Any],
) -> tuple[str, dict[str, Any]]:
    if record_id in diff.get("removed", []):
        return "baseline", old_context
    return "current", new_context


def release_review_summary(
    diff: dict[str, Any],
    impacted_record_count: int,
    missing_reference_count: int,
) -> dict[str, Any]:
    changes = diff.get("changes", [])
    removed_count = len(diff.get("removed", []))
    breaking_count = diff.get("summary", {}).get("breakingChanges", 0)
    focus: list[str] = []
    if breaking_count:
        focus.append("breaking changes")
    if removed_count:
        focus.append("removed records")
    if impacted_record_count:
        focus.append("upstream and downstream impacted records")
    if missing_reference_count:
        focus.append("missing references")
    if not focus and changes:
        focus.append("changed records")

    risk_level = "low"
    if breaking_count or removed_count or missing_reference_count:
        risk_level = "high"
    elif impacted_record_count or changes:
        risk_level = "medium"

    return {
        "requiresReview": bool(changes or impacted_record_count or missing_reference_count),
        "riskLevel": risk_level,
        "focus": focus,
    }


def generate_product_impact_report(
    old_workspace: Workspace,
    new_workspace: Workspace,
    generated_at: str | None = None,
) -> dict:
    diff = diff_workspaces(old_workspace, new_workspace)
    old_records = {record.id: record.data for record in old_workspace.records if record.id}
    new_records = {record.id: record.data for record in new_workspace.records if record.id}
    old_graph = build_graph(old_workspace)
    new_graph = build_graph(new_workspace)
    old_downstream, old_upstream, old_missing = graph_reference_indexes(old_graph, old_records)
    new_downstream, new_upstream, new_missing = graph_reference_indexes(new_graph, new_records)
    old_context = {
        "records": old_records,
        "downstream": old_downstream,
        "upstream": old_upstream,
    }
    new_context = {
        "records": new_records,
        "downstream": new_downstream,
        "upstream": new_upstream,
    }

    changes = change_by_record(diff)
    impacted_records: dict[str, dict[str, Any]] = {}
    changed_entries: list[dict[str, Any]] = []
    upstream_total = 0
    downstream_total = 0

    for record_id in changed_record_ids(diff):
        graph_source, context = graph_context_for_change(record_id, diff, old_context, new_context)
        records = context["records"]
        data = records.get(record_id, {})
        change = changes.get(record_id, {})
        upstream = impact_direction_summary(record_id, context["upstream"], records)
        downstream = impact_direction_summary(record_id, context["downstream"], records)
        upstream_total += len(upstream["recordIds"])
        downstream_total += len(downstream["recordIds"])

        for direction, summary in [("upstream", upstream), ("downstream", downstream)]:
            for impacted_id in summary["recordIds"]:
                impacted_data = records[impacted_id]
                entry = impacted_records.setdefault(
                    impacted_id,
                    {
                        **impact_record_summary(impacted_id, impacted_data),
                        "directions": [],
                        "changedRecordIds": [],
                        "graphSources": [],
                    },
                )
                if direction not in entry["directions"]:
                    entry["directions"].append(direction)
                if record_id not in entry["changedRecordIds"]:
                    entry["changedRecordIds"].append(record_id)
                if graph_source not in entry["graphSources"]:
                    entry["graphSources"].append(graph_source)

        changed_entries.append(
            {
                **impact_record_summary(record_id, data),
                "changeType": change.get("type", "record.changed"),
                "severity": change.get("severity", "info"),
                "breaking": bool(change.get("breaking", False)),
                "fields": change.get("fields", []),
                "reasons": change.get("reasons", []),
                "graphSource": graph_source,
                "upstream": upstream,
                "downstream": downstream,
            }
        )

    normalized_impacted_records = []
    for record_id in sorted(impacted_records):
        entry = impacted_records[record_id]
        normalized_impacted_records.append(
            {
                **entry,
                "directions": sorted(entry["directions"]),
                "changedRecordIds": sorted(entry["changedRecordIds"]),
                "graphSources": sorted(entry["graphSources"]),
            }
        )

    missing_references = [
        {**item, "graphSource": "baseline"}
        for item in old_missing
    ] + [
        {**item, "graphSource": "current"}
        for item in new_missing
    ]
    missing_references = sorted(
        missing_references,
        key=lambda item: (
            item["graphSource"],
            item["source"],
            item["relationship"],
            item["target"],
            item["field"],
        ),
    )

    by_severity = {severity: 0 for severity in SEVERITY_LEVELS}
    for entry in changed_entries:
        severity = entry.get("severity")
        if isinstance(severity, str) and severity in by_severity:
            by_severity[severity] += 1

    return {
        "type": "product_impact_report",
        "generatedAt": generated_at_value(generated_at),
        "verityVersion": __version__,
        "oldWorkspace": workspace_report_summary(old_workspace),
        "newWorkspace": workspace_report_summary(new_workspace),
        "diff": diff,
        "summary": {
            "changedRecordCount": len(changed_entries),
            "impactedRecordCount": len(normalized_impacted_records),
            "upstreamImpactCount": upstream_total,
            "downstreamImpactCount": downstream_total,
            "missingReferenceCount": len(missing_references),
            "bySeverity": by_severity,
            "releaseReview": release_review_summary(
                diff,
                len(normalized_impacted_records),
                len(missing_references),
            ),
        },
        "changedRecords": changed_entries,
        "impactedRecords": normalized_impacted_records,
        "missingReferences": missing_references,
    }


ROADMAP_MILESTONE_PATTERN = re.compile(r"^## (v\d+\.\d+\.\d+)\s*$")
ROADMAP_SECTION_PATTERN = re.compile(r"^## .+")
ROADMAP_SPRINT_ROW_PATTERN = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")
ROADMAP_PLANNING_ITEM_PATTERN = re.compile(r"^(\d+)\.\s+(.*)")


def roadmap_path(path: str | Path) -> Path:
    candidate = Path(path)
    if candidate.is_dir():
        candidate = candidate / "ROADMAP.md"
    return candidate


def roadmap_status(lines: list[str]) -> str:
    for line in lines[:8]:
        text = line.strip().lower()
        if "milestone is active" in text or "milestone is focused on" in text:
            return "active"
        if "milestone is released" in text:
            return "released"
    return "unknown"


def parse_roadmap_sprints(lines: list[str]) -> list[dict[str, Any]]:
    sprints: list[dict[str, Any]] = []
    for line in lines:
        match = ROADMAP_SPRINT_ROW_PATTERN.match(line.strip())
        if not match:
            continue
        sprints.append(
            {
                "number": int(match.group(1)),
                "status": match.group(2).strip(),
                "focus": match.group(3).strip(),
            }
        )
    return sprints


def parse_roadmap_milestones(text: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    milestones: list[dict[str, Any]] = []
    index = 0
    while index < len(lines):
        match = ROADMAP_MILESTONE_PATTERN.match(lines[index])
        if not match:
            index += 1
            continue
        version = match.group(1)
        section_start = index + 1
        index += 1
        while index < len(lines) and not ROADMAP_MILESTONE_PATTERN.match(lines[index]):
            if lines[index].startswith("## Later Candidates") or lines[index].startswith("## Next 20"):
                break
            index += 1
        section_lines = lines[section_start:index]
        sprints = parse_roadmap_sprints(section_lines)
        completed = [sprint for sprint in sprints if sprint["status"].lower() == "complete"]
        in_progress = [sprint for sprint in sprints if sprint["status"].lower() == "in progress"]
        milestones.append(
            {
                "version": version,
                "status": roadmap_status(section_lines),
                "sprintCount": len(sprints),
                "completedSprintCount": len(completed),
                "inProgressSprintCount": len(in_progress),
                "sprints": sprints,
            }
        )
    return milestones


def parse_next_roadmap_points(text: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    points: list[dict[str, Any]] = []
    in_section = False
    current: dict[str, Any] | None = None
    for line in lines:
        if line.startswith("## Next 20 Roadmap Points"):
            in_section = True
            continue
        if in_section and ROADMAP_SECTION_PATTERN.match(line):
            break
        if not in_section:
            continue

        stripped = line.strip()
        match = ROADMAP_PLANNING_ITEM_PATTERN.match(stripped)
        if match:
            if current is not None:
                points.append(current)
            current = {"number": int(match.group(1)), "text": match.group(2).strip()}
            continue
        if current is not None and stripped:
            current["text"] = f"{current['text']} {stripped}".strip()

    if current is not None:
        points.append(current)
    return points


def generate_roadmap_report(path: str | Path, generated_at: str | None = None) -> dict:
    resolved_path = roadmap_path(path).resolve()
    text = resolved_path.read_text(encoding="utf-8")
    milestones = parse_roadmap_milestones(text)
    next_points = parse_next_roadmap_points(text)
    released = [milestone for milestone in milestones if milestone["status"] == "released"]
    active = [milestone for milestone in milestones if milestone["status"] == "active"]
    completed_sprints = sum(milestone["completedSprintCount"] for milestone in milestones)
    in_progress_sprints = sum(milestone["inProgressSprintCount"] for milestone in milestones)

    return {
        "type": "roadmap_report",
        "generatedAt": generated_at_value(generated_at),
        "verityVersion": __version__,
        "roadmapPath": str(resolved_path),
        "latestReleasedMilestone": released[-1]["version"] if released else None,
        "activeMilestones": [milestone["version"] for milestone in active],
        "summary": {
            "milestones": len(milestones),
            "releasedMilestones": len(released),
            "activeMilestones": len(active),
            "sprints": sum(milestone["sprintCount"] for milestone in milestones),
            "completedSprints": completed_sprints,
            "inProgressSprints": in_progress_sprints,
            "nextRoadmapPoints": len(next_points),
        },
        "milestones": milestones,
        "nextRoadmapPoints": next_points,
    }


def markdown_cell(value: Any) -> str:
    text = str(value) if value not in (None, "") else "none"
    return text.replace("|", "\\|")


def generate_roadmap_report_markdown(report: dict[str, Any]) -> str:
    summary = report.get("summary", {})
    milestones = report.get("milestones", [])
    next_points = report.get("nextRoadmapPoints", [])
    recent_milestones = milestones[-5:]
    active_milestones = report.get("activeMilestones", [])

    lines = [
        "# VeritySpec Roadmap Report",
        "",
        f"- Generated: `{report.get('generatedAt')}`",
        f"- VeritySpec: `{report.get('verityVersion')}`",
        f"- Roadmap: `{report.get('roadmapPath')}`",
        f"- Latest released milestone: `{report.get('latestReleasedMilestone') or 'none'}`",
        f"- Active milestones: `{', '.join(active_milestones) if active_milestones else 'none'}`",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|---|---:|",
    ]

    summary_rows = [
        ("Milestones", summary.get("milestones", 0)),
        ("Released milestones", summary.get("releasedMilestones", 0)),
        ("Active milestones", summary.get("activeMilestones", 0)),
        ("Sprints", summary.get("sprints", 0)),
        ("Completed sprints", summary.get("completedSprints", 0)),
        ("In-progress sprints", summary.get("inProgressSprints", 0)),
        ("Next roadmap points", summary.get("nextRoadmapPoints", 0)),
    ]
    for label, count in summary_rows:
        lines.append(f"| {markdown_cell(label)} | {markdown_cell(count)} |")

    lines.extend(
        [
            "",
            "## Recent Milestones",
            "",
            "| Milestone | Status | Sprints | Complete | In Progress |",
            "|---|---|---:|---:|---:|",
        ]
    )
    for milestone in recent_milestones:
        lines.append(
            "| "
            f"{markdown_cell(milestone.get('version'))} | "
            f"{markdown_cell(milestone.get('status'))} | "
            f"{markdown_cell(milestone.get('sprintCount', 0))} | "
            f"{markdown_cell(milestone.get('completedSprintCount', 0))} | "
            f"{markdown_cell(milestone.get('inProgressSprintCount', 0))} |"
        )

    lines.extend(["", "## Recent Sprint Rows", ""])
    for milestone in recent_milestones:
        sprints = milestone.get("sprints", [])
        if not sprints:
            continue
        lines.append(f"### {milestone.get('version')}")
        lines.append("")
        lines.append("| Sprint | Status | Focus |")
        lines.append("|---:|---|---|")
        for sprint in sprints:
            lines.append(
                "| "
                f"{markdown_cell(sprint.get('number'))} | "
                f"{markdown_cell(sprint.get('status'))} | "
                f"{markdown_cell(sprint.get('focus'))} |"
            )
        lines.append("")

    lines.extend(["## Next 20 Roadmap Points", ""])
    for point in next_points:
        lines.append(f"{point.get('number')}. {point.get('text')}")

    return "\n".join(lines).rstrip() + "\n"


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


EVIDENCE_KINDS = {
    "evidence.test",
    "evidence.ci-run",
    "evidence.build",
    "evidence.review",
    "evidence.screenshot",
    "evidence.video",
    "evidence.qa",
    "evidence.playtest",
    "evidence.certification-checklist",
    "evidence.artifact",
}
EVIDENCE_URI_FIELDS = [
    "evidenceUri",
    "runUrl",
    "artifactPath",
    "reviewUri",
    "imagePath",
    "videoPath",
    "reportPath",
    "checklistPath",
]
EVIDENCE_FAILING_VALUES = {"failure", "failing", "blocked", "changes-requested", "rejected"}
EVIDENCE_INCONCLUSIVE_VALUES = {
    "inconclusive",
    "skipped",
    "cancelled",
    "neutral",
    "timed-out",
    "deferred",
    "not-started",
    "in-progress",
    "mixed",
}


def evidence_status(record: Record) -> str:
    for field in ["result", "conclusion", "decision", "certificationStatus"]:
        value = record.data.get(field)
        if isinstance(value, str) and value:
            return value
    return record.data.get("status", "unspecified")


def evidence_uri(record: Record) -> str | None:
    for field in EVIDENCE_URI_FIELDS:
        value = record.data.get(field)
        if isinstance(value, str) and value.strip():
            return value
    return None


def evidence_subject(record: Record, records_by_id: dict[str, Record]) -> dict[str, Any]:
    subject_ref = record.data.get("subjectRef")
    subject = records_by_id.get(subject_ref) if isinstance(subject_ref, str) else None
    return {
        "id": subject_ref if isinstance(subject_ref, str) else "",
        "kind": subject.kind if subject and subject.kind else record.data.get("subjectKind", "unknown"),
        "name": subject.data.get("name", "") if subject else "",
        "resolved": subject is not None,
    }


def generate_evidence_report(workspace: Workspace, generated_at: str | None = None) -> dict:
    evidence_records = [record for record in workspace.records if record.kind in EVIDENCE_KINDS]
    records_by_id = {record.id: record for record in workspace.records if record.id}
    by_kind: dict[str, int] = {}
    for record in evidence_records:
        key = record.kind or "unspecified"
        by_kind[key] = by_kind.get(key, 0) + 1
    entries: list[dict[str, Any]] = []
    missing_subjects: list[str] = []
    missing_artifacts: list[str] = []
    failing_evidence: list[str] = []
    inconclusive_evidence: list[str] = []

    for record in sorted(evidence_records, key=lambda item: item.id or ""):
        status = evidence_status(record)
        subject = evidence_subject(record, records_by_id)
        uri = evidence_uri(record)
        if record.id and not subject["resolved"]:
            missing_subjects.append(record.id)
        if record.id and not uri:
            missing_artifacts.append(record.id)
        if record.id and status in EVIDENCE_FAILING_VALUES:
            failing_evidence.append(record.id)
        if record.id and status in EVIDENCE_INCONCLUSIVE_VALUES:
            inconclusive_evidence.append(record.id)

        entries.append(
            {
                "id": record.id,
                "kind": record.kind,
                "name": record.data.get("name"),
                "status": record.data.get("status"),
                "owner": record.data.get("owner"),
                "evidenceStatus": status,
                "subject": subject,
                "uri": uri,
                "references": record.data.get("references", []),
            }
        )

    return {
        "type": "evidence_report",
        "generatedAt": generated_at_value(generated_at),
        "verityVersion": __version__,
        "workspace": workspace.config.get("workspace", workspace.base_path.name),
        "workspacePath": str(workspace.base_path),
        "specVersion": workspace.config.get("specVersion"),
        "evidenceCount": len(evidence_records),
        "summary": {
            "byKind": dict(sorted(by_kind.items(), key=lambda item: item[0])),
            "byStatus": count_by_field(evidence_records, "status"),
            "byOwner": count_by_field(evidence_records, "owner"),
            "byEvidenceStatus": dict(
                sorted(
                    {
                        status: sum(
                            1 for record in evidence_records if evidence_status(record) == status
                        )
                        for status in {evidence_status(record) for record in evidence_records}
                    }.items(),
                    key=lambda item: item[0],
                )
            ),
            "releaseGaps": {
                "missingSubjects": sorted(missing_subjects),
                "missingArtifacts": sorted(missing_artifacts),
                "failingEvidence": sorted(failing_evidence),
                "inconclusiveEvidence": sorted(inconclusive_evidence),
            },
        },
        "evidence": entries,
    }


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


def verification_last_verified(record: Record) -> str:
    verification = record.data.get("verification")
    if not isinstance(verification, dict):
        return ""
    value = verification.get("lastVerified")
    return value.strip() if isinstance(value, str) else ""


def security_control_has_missing_verification_date(record: Record) -> bool:
    return verification_last_verified(record) == ""


def security_control_has_stale_evidence(record: Record) -> bool:
    verification = record.data.get("verification")
    if not isinstance(verification, dict):
        return False
    review_cadence_days = verification.get("reviewCadenceDays")
    if not isinstance(review_cadence_days, int) or review_cadence_days < 0:
        return False
    last_verified = verification_last_verified(record)
    if not last_verified:
        return False
    try:
        verified_at = date.fromisoformat(last_verified)
    except ValueError:
        return True
    age_days = (date.today() - verified_at).days
    return age_days < 0 or age_days > review_cadence_days


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


def generate_security_report(workspace: Workspace, generated_at: str | None = None) -> dict:
    controls = [record for record in workspace.records if record.kind == "security.control"]
    records_by_id = {record.id: record for record in workspace.records if record.id}
    control_entries: list[dict[str, Any]] = []
    verified_control_count = 0
    critical_unverified: list[str] = []
    stale_evidence: list[str] = []
    missing_verification_dates: list[str] = []

    for record in controls:
        verified = is_security_control_verified(record)
        if verified:
            verified_control_count += 1
        if record.data.get("riskLevel") == "critical" and not verified and record.id:
            critical_unverified.append(record.id)
        if record.id and security_control_has_stale_evidence(record):
            stale_evidence.append(record.id)
        if record.id and security_control_has_missing_verification_date(record):
            missing_verification_dates.append(record.id)

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
        "generatedAt": generated_at_value(generated_at),
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
            "releaseGaps": {
                "criticalUnverified": sorted(critical_unverified),
                "staleEvidence": sorted(stale_evidence),
                "missingVerificationDates": sorted(missing_verification_dates),
            },
        },
        "controls": control_entries,
    }


def generate_accessibility_report(workspace: Workspace, generated_at: str | None = None) -> dict:
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
        "generatedAt": generated_at_value(generated_at),
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


def generate_compliance_matrix(workspace: Workspace, generated_at: str | None = None) -> dict:
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
        "generatedAt": generated_at_value(generated_at),
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


def deployment_runtime_summary(record: Record | None) -> dict[str, Any]:
    if record is None:
        return {}
    return {
        "id": record.id,
        "name": record.data.get("name"),
        "owner": record.data.get("owner"),
        "runtimeType": record.data.get("runtimeType"),
        "runtimeName": record.data.get("runtimeName"),
        "version": record.data.get("version"),
        "artifactType": record.data.get("artifactType"),
    }


def generate_deployment_report(workspace: Workspace, generated_at: str | None = None) -> dict:
    runtimes = [record for record in workspace.records if record.kind == "deployment.runtime"]
    targets = [record for record in workspace.records if record.kind == "deployment.target"]
    records_by_id = {record.id: record for record in workspace.records if record.id}
    runtime_target_ids = {
        record.data.get("runtimeRef")
        for record in targets
        if isinstance(record.data.get("runtimeRef"), str)
    }
    target_entries: list[dict[str, Any]] = []
    targets_without_runtime: list[str] = []
    production_without_approval: list[str] = []
    production_without_health_checks: list[str] = []
    targets_without_rollback_plan: list[str] = []

    for record in targets:
        runtime_ref = record.data.get("runtimeRef")
        runtime = records_by_id.get(runtime_ref) if isinstance(runtime_ref, str) else None
        release_policy = record.data.get("releasePolicy", {})
        approval_required = (
            release_policy.get("approvalRequired")
            if isinstance(release_policy, dict)
            else None
        )
        is_production = record.data.get("environment") == "production"
        has_health_check = bool(str(record.data.get("healthCheckUrl", "")).strip())
        has_rollback_plan = bool(str(record.data.get("rollbackPlan", "")).strip())

        if record.id and runtime is None:
            targets_without_runtime.append(record.id)
        if record.id and is_production and approval_required is not True:
            production_without_approval.append(record.id)
        if record.id and is_production and not has_health_check:
            production_without_health_checks.append(record.id)
        if record.id and not has_rollback_plan:
            targets_without_rollback_plan.append(record.id)

        target_entries.append(
            {
                "id": record.id,
                "name": record.data.get("name"),
                "status": record.data.get("status"),
                "owner": record.data.get("owner"),
                "environment": record.data.get("environment"),
                "provider": record.data.get("provider"),
                "platform": record.data.get("platform"),
                "regions": record.data.get("regions", []),
                "url": record.data.get("url"),
                "healthCheckUrl": record.data.get("healthCheckUrl"),
                "runtime": deployment_runtime_summary(runtime),
                "releasePolicy": release_policy if isinstance(release_policy, dict) else {},
                "rollbackPlan": record.data.get("rollbackPlan"),
                "references": record.data.get("references", []),
            }
        )

    runtime_entries = [
        {
            "id": record.id,
            "name": record.data.get("name"),
            "status": record.data.get("status"),
            "owner": record.data.get("owner"),
            "runtimeType": record.data.get("runtimeType"),
            "runtimeName": record.data.get("runtimeName"),
            "version": record.data.get("version"),
            "artifactType": record.data.get("artifactType"),
            "language": record.data.get("language"),
            "entrypoint": record.data.get("entrypoint"),
            "dependencies": record.data.get("dependencies", []),
        }
        for record in runtimes
    ]
    runtimes_without_targets = [
        record.id
        for record in runtimes
        if record.id and record.id not in runtime_target_ids
    ]
    deployment_records = runtimes + targets
    missing_owners = [
        record.id for record in deployment_records if record.id and owner_missing(record)
    ]

    return {
        "type": "deployment_report",
        "generatedAt": generated_at_value(generated_at),
        "verityVersion": __version__,
        "workspace": workspace.config.get("workspace", workspace.base_path.name),
        "workspacePath": str(workspace.base_path),
        "specVersion": workspace.config.get("specVersion"),
        "targetCount": len(targets),
        "runtimeCount": len(runtimes),
        "summary": {
            "targets": len(targets),
            "runtimes": len(runtimes),
            "byEnvironment": count_by_field(targets, "environment"),
            "byProvider": count_by_field(targets, "provider"),
            "byPlatform": count_by_field(targets, "platform"),
            "runtimesByType": count_by_field(runtimes, "runtimeType"),
            "releaseGaps": {
                "targetsWithoutRuntime": targets_without_runtime,
                "runtimesWithoutTargets": runtimes_without_targets,
                "productionWithoutApproval": production_without_approval,
                "productionWithoutHealthChecks": production_without_health_checks,
                "targetsWithoutRollbackPlan": targets_without_rollback_plan,
                "missingOwners": missing_owners,
            },
        },
        "targets": target_entries,
        "runtimes": runtime_entries,
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


def generate_observability_report(workspace: Workspace, generated_at: str | None = None) -> dict:
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
        "generatedAt": generated_at_value(generated_at),
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
