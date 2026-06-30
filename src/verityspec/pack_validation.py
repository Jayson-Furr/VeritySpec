from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, SchemaError

from .envelope import RECORD_ENVELOPE_REQUIRED
from .issues import Issue
from .packs import (
    Pack,
    PackRegistry,
    available_builtin_packs,
    available_external_packs,
    load_pack,
    load_pack_from_path,
    load_pack_registry,
)


KNOWN_GENERATORS = {
    "openapi",
    "asyncapi",
    "typescript",
    "python-models",
    "schema-bundle",
    "cli-reference",
    "validation-report",
}

PACK_MANIFEST_SCHEMA_PATH = Path(__file__).resolve().parent / "schemas" / "pack-manifest.schema.json"


def load_pack_manifest_schema() -> dict[str, Any]:
    return json.loads(PACK_MANIFEST_SCHEMA_PATH.read_text(encoding="utf-8"))


def pack_summary_from_pack(pack: Pack) -> dict[str, Any]:
    return {
        "id": pack.id,
        "version": pack.version,
        "name": pack.name,
        "description": pack.description,
        "path": str(pack.path),
        "kinds": sorted(pack.schemas),
        "readinessGates": [gate.get("id") for gate in pack.readiness_gates],
        "generators": pack.generators,
    }


def pack_summary(pack_id: str) -> dict[str, Any]:
    return pack_summary_from_pack(load_pack(pack_id))


def list_builtin_pack_summaries() -> list[dict[str, Any]]:
    return [pack_summary(pack_id) for pack_id in sorted(available_builtin_packs())]


def list_pack_summaries(
    external_pack_paths: list[str | Path] | None = None,
    base_path: Path | None = None,
) -> list[dict[str, Any]]:
    summaries = list_builtin_pack_summaries()
    external = available_external_packs(external_pack_paths, base_path)
    for pack_id in sorted(external):
        summaries.append(pack_summary_from_pack(load_pack_from_path(external[pack_id])))
    return summaries


def validate_pack_manifest(path: Path) -> list[Issue]:
    issues: list[Issue] = []
    manifest = json.loads(path.read_text(encoding="utf-8"))
    schema = load_pack_manifest_schema()
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
        error_path = ".".join(str(part) for part in error.path)
        location = f"{path}:{error_path}" if error_path else str(path)
        issues.append(Issue("error", "pack.manifest.schema", error.message, location))
    return issues


def validate_pack_schemas_for_pack(pack: Pack) -> list[Issue]:
    issues: list[Issue] = []
    for kind, binding in pack.schemas.items():
        schema = binding.schema
        try:
            Draft202012Validator.check_schema(schema)
        except SchemaError as exc:
            issues.append(
                Issue("error", "pack.schema.invalid", str(exc), str(binding.path))
            )

        type_property = schema.get("properties", {}).get("kind", {})
        if type_property.get("const") != kind:
            issues.append(
                Issue(
                    "error",
                    "pack.schema.kind_mismatch",
                    f"Schema kind '{kind}' must declare properties.kind.const '{kind}'.",
                    str(binding.path),
                )
            )

        if schema.get("additionalProperties") is not False:
            issues.append(
                Issue(
                    "error",
                    "pack.schema.not_strict",
                    f"Schema kind '{kind}' must set additionalProperties to false.",
                    str(binding.path),
                )
            )

        required = set(schema.get("required", []))
        properties = set(schema.get("properties", {}))
        for field in RECORD_ENVELOPE_REQUIRED:
            if field not in required:
                issues.append(
                    Issue(
                        "error",
                        "pack.schema.envelope_required_missing",
                        f"Schema kind '{kind}' must require envelope field '{field}'.",
                        str(binding.path),
                    )
                )
            if field not in properties:
                issues.append(
                    Issue(
                        "error",
                        "pack.schema.envelope_property_missing",
                        f"Schema kind '{kind}' must define envelope field '{field}'.",
                        str(binding.path),
                    )
                )
    return issues


def validate_pack_declarations_for_pack(pack: Pack) -> list[Issue]:
    issues: list[Issue] = []
    pack_path = pack.path
    manifest_path = pack.path / "pack.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    own_kinds = set(pack.schemas)

    for schema_decl in manifest.get("schemas", []):
        schema_path = pack_path / schema_decl.get("path", "")
        if not schema_path.exists():
            issues.append(
                Issue("error", "pack.schema.missing_file", f"Schema file does not exist: {schema_path}", str(manifest_path))
            )

    for gate in manifest.get("readinessGates", []):
        kind = gate.get("kind")
        if kind not in own_kinds:
            issues.append(
                Issue(
                    "error",
                    "pack.readiness.unknown_kind",
                    f"Readiness gate references kind '{kind}' not declared by this pack.",
                    str(manifest_path),
                )
            )

    for generator in manifest.get("generators", []):
        if generator not in KNOWN_GENERATORS:
            issues.append(
                Issue(
                    "error",
                    "pack.generator.unknown",
                    f"Unknown generator '{generator}'.",
                    str(manifest_path),
                )
            )

    return issues


def validate_pack_object(pack: Pack) -> list[Issue]:
    manifest_path = pack.path / "pack.json"
    issues = validate_pack_manifest(manifest_path)
    issues.extend(validate_pack_schemas_for_pack(pack))
    issues.extend(validate_pack_declarations_for_pack(pack))
    return issues


def validate_single_pack(
    pack_id: str,
    external_pack_paths: list[str | Path] | None = None,
    base_path: Path | None = None,
) -> list[Issue]:
    try:
        pack = load_pack(pack_id, external_pack_paths, base_path)
    except ValueError:
        return [Issue("error", "pack.unknown", f"Unknown pack '{pack_id}'.")]
    issues = validate_pack_object(pack)
    registry_ids = sorted(available_builtin_packs())
    if pack_id not in registry_ids:
        registry_ids.append(pack_id)
    try:
        registry = load_pack_registry(registry_ids, external_pack_paths, base_path)
        issues.extend(validate_pack_registry_semantics(registry))
    except ValueError as exc:
        issues.append(Issue("error", "pack.kind.collision", str(exc)))
    return issues


def validate_pack_registry_semantics(registry: PackRegistry) -> list[Issue]:
    issues: list[Issue] = []
    known_kinds = set(registry.schemas)

    for rule in registry.reference_rules:
        if rule.source_kind not in known_kinds:
            issues.append(
                Issue(
                    "error",
                    "pack.reference_rule.unknown_source_kind",
                    f"Reference rule source kind '{rule.source_kind}' is not declared by the loaded packs.",
                    record_id=rule.pack_id,
                )
            )
        if rule.target_kind not in known_kinds:
            issues.append(
                Issue(
                    "error",
                    "pack.reference_rule.unknown_target_kind",
                    f"Reference rule target kind '{rule.target_kind}' is not declared by the loaded packs.",
                    record_id=rule.pack_id,
                )
            )

    for pack in registry.packs.values():
        for gate in pack.readiness_gates:
            kind = gate.get("kind")
            if kind not in known_kinds:
                issues.append(
                    Issue(
                        "error",
                        "pack.readiness.registry_unknown_kind",
                        f"Readiness gate references kind '{kind}' not declared by the loaded packs.",
                        record_id=pack.id,
                    )
                )

    return issues


def validate_builtin_packs(pack_id: str | None = None) -> list[Issue]:
    return validate_packs(pack_id)


def validate_packs(
    pack_id: str | None = None,
    external_pack_paths: list[str | Path] | None = None,
    base_path: Path | None = None,
) -> list[Issue]:
    if pack_id:
        return validate_single_pack(pack_id, external_pack_paths, base_path)

    pack_ids = sorted(available_builtin_packs())
    try:
        external = available_external_packs(external_pack_paths, base_path)
    except ValueError as exc:
        return [Issue("error", "pack.path.invalid", str(exc))]
    pack_ids.extend(sorted(external))
    issues: list[Issue] = []
    for candidate in pack_ids:
        issues.extend(validate_single_pack(candidate, external_pack_paths, base_path))

    try:
        registry = load_pack_registry(pack_ids, external_pack_paths, base_path)
    except ValueError as exc:
        issues.append(Issue("error", "pack.kind.collision", str(exc)))
        return issues

    issues.extend(validate_pack_registry_semantics(registry))
    return issues
