from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .workspace import Record


REFERENCE_FIELD_NAMES = {
    "parent",
    "payloadSchema",
    "requestSchema",
    "responseSchema",
    "runtimeRef",
    "schema",
    "outputSchema",
}


@dataclass(frozen=True)
class ReferenceEdge:
    source: str
    target: str
    relationship: str
    field: str

    def to_dict(self) -> dict[str, str]:
        return {
            "source": self.source,
            "target": self.target,
            "relationship": self.relationship,
            "field": self.field,
        }


def extract_reference_edges(record: Record) -> list[ReferenceEdge]:
    if not record.id:
        return []
    edges: list[ReferenceEdge] = []

    def add(target: Any, relationship: str, field: str) -> None:
        if isinstance(target, str) and target:
            edges.append(
                ReferenceEdge(
                    source=record.id or "",
                    target=target,
                    relationship=relationship,
                    field=field,
                )
            )

    explicit = record.data.get("references")
    if isinstance(explicit, list):
        for index, item in enumerate(explicit):
            if isinstance(item, dict):
                relationship = item.get("type", "references")
                add(item.get("target"), str(relationship), f"references[{index}].target")

    def visit(value: Any, path: str) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                child_path = f"{path}.{key}" if path else key
                if key in REFERENCE_FIELD_NAMES and key != "schema":
                    add(child, key, child_path)
                elif key == "schema" and path.rsplit(".", 1)[-1].startswith("responses["):
                    add(child, "responseSchema", child_path)
                elif key != "jsonSchema":
                    visit(child, child_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, f"{path}[{index}]")

    visit(record.data, "")
    return edges
