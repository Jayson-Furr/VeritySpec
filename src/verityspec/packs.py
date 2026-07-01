from __future__ import annotations

import json
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path
from typing import Any, Optional


PACK_ROOT = Path(__file__).resolve().parent / "packs"
PACK_ENTRY_POINT_GROUP = "verityspec.packs"


@dataclass(frozen=True)
class SchemaBinding:
    kind: str
    schema: dict[str, Any]
    path: Path
    pack_id: str


@dataclass(frozen=True)
class ReferenceRule:
    source_kind: str
    relationship: str
    target_kind: str
    pack_id: str

    def matches(self, source_kind: str, relationship: str, target_kind: str) -> bool:
        return (
            self.source_kind == source_kind
            and self.relationship == relationship
            and self.target_kind == target_kind
        )


@dataclass(frozen=True)
class Pack:
    id: str
    version: str
    name: str
    description: str
    path: Path
    source: str
    schemas: dict[str, SchemaBinding]
    readiness_gates: list[dict[str, Any]]
    generators: list[str]
    generator_metadata: list[dict[str, Any]]
    reference_rules: list[ReferenceRule]


@dataclass(frozen=True)
class PackRegistry:
    packs: dict[str, Pack]
    schemas: dict[str, SchemaBinding]
    reference_rules: list[ReferenceRule]

    def schema_for_kind(self, kind: str) -> Optional[SchemaBinding]:
        return self.schemas.get(kind)

    def allows_reference(self, source_kind: str, relationship: str, target_kind: str) -> bool:
        return any(
            rule.matches(source_kind, relationship, target_kind)
            for rule in self.reference_rules
        )

    @property
    def readiness_gates(self) -> list[dict[str, Any]]:
        gates: list[dict[str, Any]] = []
        for pack in self.packs.values():
            gates.extend(pack.readiness_gates)
        return gates

    @property
    def known_kinds(self) -> list[str]:
        return sorted(self.schemas)


def available_builtin_packs() -> dict[str, Path]:
    packs: dict[str, Path] = {}
    if not PACK_ROOT.exists():
        return packs
    for manifest_path in sorted(PACK_ROOT.glob("*/pack.json")):
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        pack_id = manifest.get("id")
        if isinstance(pack_id, str):
            packs[pack_id] = manifest_path.parent
    return packs


def installed_pack_entry_points() -> list[metadata.EntryPoint]:
    entry_points = metadata.entry_points()
    if hasattr(entry_points, "select"):
        return list(entry_points.select(group=PACK_ENTRY_POINT_GROUP))
    return list(entry_points.get(PACK_ENTRY_POINT_GROUP, []))


def normalize_pack_path(path: str | Path, base_path: Path | None = None) -> Path:
    candidate = Path(path)
    if not candidate.is_absolute() and base_path is not None:
        candidate = base_path / candidate
    candidate = candidate.resolve()
    if candidate.name == "pack.json":
        return candidate.parent
    return candidate


def resolve_installed_pack_entry_point(entry_point: metadata.EntryPoint) -> Path:
    try:
        loaded = entry_point.load()
        pack_path = loaded() if callable(loaded) else loaded
    except Exception as exc:  # pragma: no cover - exact import errors vary by package
        raise ValueError(
            f"Installed pack entry point '{entry_point.name}' could not be loaded."
        ) from exc

    if not isinstance(pack_path, (str, Path)):
        raise ValueError(
            f"Installed pack entry point '{entry_point.name}' must resolve to a pack path."
        )
    return normalize_pack_path(pack_path)


def available_installed_packs() -> dict[str, Path]:
    packs: dict[str, Path] = {}
    builtin_ids = set(available_builtin_packs())
    for entry_point in sorted(installed_pack_entry_points(), key=lambda item: item.name):
        pack_path = resolve_installed_pack_entry_point(entry_point)
        manifest_path = pack_path / "pack.json"
        if not manifest_path.exists():
            raise ValueError(
                f"Installed pack entry point '{entry_point.name}' does not resolve to pack.json: {pack_path}"
            )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        pack_id = manifest.get("id")
        if not isinstance(pack_id, str):
            raise ValueError(
                f"Installed pack manifest is missing string id: {manifest_path}"
            )
        if entry_point.name != pack_id:
            raise ValueError(
                f"Installed pack entry point '{entry_point.name}' must match manifest id '{pack_id}'."
            )
        if pack_id in builtin_ids:
            raise ValueError(f"Installed pack '{pack_id}' collides with a built-in pack id.")
        if pack_id in packs and packs[pack_id] != pack_path:
            raise ValueError(f"Installed pack '{pack_id}' is declared by multiple entry points.")
        packs[pack_id] = pack_path
    return packs


def generator_id(generator: Any) -> str | None:
    if isinstance(generator, str):
        return generator
    if isinstance(generator, dict) and isinstance(generator.get("id"), str):
        return generator["id"]
    return None


def normalize_generator_metadata(generators: Any) -> list[dict[str, Any]]:
    if not isinstance(generators, list):
        return []
    metadata: list[dict[str, Any]] = []
    for generator in generators:
        if isinstance(generator, str):
            metadata.append({"id": generator})
        elif isinstance(generator, dict):
            generator_id_value = generator_id(generator)
            if generator_id_value:
                metadata.append(dict(generator))
    return metadata


def normalize_generator_ids(generators: Any) -> list[str]:
    ids: list[str] = []
    for metadata in normalize_generator_metadata(generators):
        generator_id_value = metadata.get("id")
        if isinstance(generator_id_value, str):
            ids.append(generator_id_value)
    return ids


def available_external_packs(
    pack_paths: list[str | Path] | None = None,
    base_path: Path | None = None,
) -> dict[str, Path]:
    packs: dict[str, Path] = {}
    builtin_ids = set(available_builtin_packs())
    for raw_path in pack_paths or []:
        pack_path = normalize_pack_path(raw_path, base_path)
        manifest_path = pack_path / "pack.json"
        if not manifest_path.exists():
            raise ValueError(f"External pack path does not contain pack.json: {pack_path}")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        pack_id = manifest.get("id")
        if not isinstance(pack_id, str):
            raise ValueError(f"External pack manifest is missing string id: {manifest_path}")
        if pack_id in builtin_ids:
            raise ValueError(f"External pack '{pack_id}' collides with a built-in pack id.")
        if pack_id in packs and packs[pack_id] != pack_path:
            raise ValueError(f"External pack '{pack_id}' is declared by multiple paths.")
        packs[pack_id] = pack_path
    return packs


def load_pack_from_path(pack_path: str | Path, source: str = "external") -> Pack:
    pack_path = normalize_pack_path(pack_path)
    manifest = json.loads((pack_path / "pack.json").read_text(encoding="utf-8"))
    pack_id = manifest["id"]
    schemas: dict[str, SchemaBinding] = {}
    for schema_decl in manifest.get("schemas", []):
        kind = schema_decl.get("kind")
        rel_path = schema_decl.get("path")
        if not isinstance(kind, str) or not isinstance(rel_path, str):
            continue
        schema_path = pack_path / rel_path
        schema = json.loads(schema_path.read_text(encoding="utf-8")) if schema_path.exists() else {}
        schemas[kind] = SchemaBinding(kind=kind, schema=schema, path=schema_path, pack_id=pack_id)

    reference_rules: list[ReferenceRule] = []
    for rule in manifest.get("referenceRules", []):
        source_kind = rule.get("sourceKind")
        relationship = rule.get("relationship")
        target_kind = rule.get("targetKind")
        if not all(isinstance(value, str) for value in [source_kind, relationship, target_kind]):
            continue
        reference_rules.append(
            ReferenceRule(
                source_kind=source_kind,
                relationship=relationship,
                target_kind=target_kind,
                pack_id=pack_id,
            )
        )

    return Pack(
        id=manifest["id"],
        version=manifest.get("version", "0.0.0"),
        name=manifest.get("name", manifest["id"]),
        description=manifest.get("description", ""),
        path=pack_path,
        source=source,
        schemas=schemas,
        readiness_gates=manifest.get("readinessGates", []),
        generators=normalize_generator_ids(manifest.get("generators", [])),
        generator_metadata=normalize_generator_metadata(manifest.get("generators", [])),
        reference_rules=reference_rules,
    )


def load_pack(
    pack_id: str,
    external_pack_paths: list[str | Path] | None = None,
    base_path: Path | None = None,
) -> Pack:
    builtin = available_builtin_packs()
    external = available_external_packs(external_pack_paths, base_path)
    if pack_id in external:
        return load_pack_from_path(external[pack_id], source="external")
    if pack_id in builtin:
        return load_pack_from_path(builtin[pack_id], source="built-in")

    installed = available_installed_packs()
    if pack_id in installed:
        return load_pack_from_path(installed[pack_id], source="installed")

    available = ", ".join(sorted(set(builtin) | set(installed) | set(external))) or "none"
    raise ValueError(f"Unknown pack '{pack_id}'. Available packs: {available}")


def load_pack_registry(
    pack_ids: list[str],
    external_pack_paths: list[str | Path] | None = None,
    base_path: Path | None = None,
) -> PackRegistry:
    packs: dict[str, Pack] = {}
    schemas: dict[str, SchemaBinding] = {}
    reference_rules: list[ReferenceRule] = []
    external = available_external_packs(external_pack_paths, base_path)
    for pack_id in pack_ids:
        if pack_id in external:
            pack = load_pack_from_path(external[pack_id], source="external")
        else:
            pack = load_pack(pack_id, external_pack_paths, base_path)
        packs[pack.id] = pack
        reference_rules.extend(pack.reference_rules)
        for kind, binding in pack.schemas.items():
            if kind in schemas:
                raise ValueError(
                    f"Kind '{kind}' is declared by both {schemas[kind].pack_id} and {pack.id}"
                )
            schemas[kind] = binding
    return PackRegistry(packs=packs, schemas=schemas, reference_rules=reference_rules)
