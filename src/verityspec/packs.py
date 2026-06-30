from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


PACK_ROOT = Path(__file__).resolve().parent / "packs"


@dataclass(frozen=True)
class SchemaBinding:
    kind: str
    schema: dict[str, Any]
    path: Path
    pack_id: str


@dataclass(frozen=True)
class Pack:
    id: str
    version: str
    name: str
    description: str
    schemas: dict[str, SchemaBinding]
    readiness_gates: list[dict[str, Any]]
    generators: list[str]


@dataclass(frozen=True)
class PackRegistry:
    packs: dict[str, Pack]
    schemas: dict[str, SchemaBinding]

    def schema_for_kind(self, kind: str) -> Optional[SchemaBinding]:
        return self.schemas.get(kind)

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


def load_pack(pack_id: str) -> Pack:
    builtin = available_builtin_packs()
    if pack_id not in builtin:
        available = ", ".join(sorted(builtin)) or "none"
        raise ValueError(f"Unknown pack '{pack_id}'. Available packs: {available}")

    pack_path = builtin[pack_id]
    manifest = json.loads((pack_path / "pack.json").read_text(encoding="utf-8"))
    schemas: dict[str, SchemaBinding] = {}
    for schema_decl in manifest.get("schemas", []):
        kind = schema_decl.get("kind")
        rel_path = schema_decl.get("path")
        if not isinstance(kind, str) or not isinstance(rel_path, str):
            continue
        schema_path = pack_path / rel_path
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schemas[kind] = SchemaBinding(kind=kind, schema=schema, path=schema_path, pack_id=pack_id)

    return Pack(
        id=manifest["id"],
        version=manifest.get("version", "0.0.0"),
        name=manifest.get("name", manifest["id"]),
        description=manifest.get("description", ""),
        schemas=schemas,
        readiness_gates=manifest.get("readinessGates", []),
        generators=manifest.get("generators", []),
    )


def load_pack_registry(pack_ids: list[str]) -> PackRegistry:
    packs: dict[str, Pack] = {}
    schemas: dict[str, SchemaBinding] = {}
    for pack_id in pack_ids:
        pack = load_pack(pack_id)
        packs[pack.id] = pack
        for kind, binding in pack.schemas.items():
            if kind in schemas:
                raise ValueError(
                    f"Kind '{kind}' is declared by both {schemas[kind].pack_id} and {pack.id}"
                )
            schemas[kind] = binding
    return PackRegistry(packs=packs, schemas=schemas)

