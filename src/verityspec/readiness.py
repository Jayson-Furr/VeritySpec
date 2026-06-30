from __future__ import annotations

from typing import Any

from .issues import Issue
from .packs import PackRegistry
from .workspace import Workspace


def is_missing(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def get_field(data: dict[str, Any], path: str) -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def evaluate_readiness(
    workspace: Workspace, registry: PackRegistry, strict: bool = False
) -> list[Issue]:
    severity = "error" if strict else "warning"
    issues: list[Issue] = []

    for gate in registry.readiness_gates:
        kind = gate.get("kind")
        if not isinstance(kind, str):
            continue
        required = [field for field in gate.get("required", []) if isinstance(field, str)]
        min_items = gate.get("minItems", {})
        gate_id = gate.get("id", "readiness.gate")

        for record in workspace.records:
            if record.kind != kind:
                continue

            for field in required:
                if is_missing(get_field(record.data, field)):
                    issues.append(
                        Issue(
                            severity,
                            "readiness.required",
                            f"Readiness gate {gate_id} requires '{field}'.",
                            record.location,
                            record.id,
                        )
                    )

            if isinstance(min_items, dict):
                for field, minimum in min_items.items():
                    value = get_field(record.data, str(field))
                    if isinstance(minimum, int) and isinstance(value, list) and len(value) < minimum:
                        issues.append(
                            Issue(
                                severity,
                                "readiness.min_items",
                                f"Readiness gate {gate_id} requires at least {minimum} item(s) in '{field}'.",
                                record.location,
                                record.id,
                            )
                        )
                    elif isinstance(minimum, int) and not isinstance(value, list):
                        issues.append(
                            Issue(
                                severity,
                                "readiness.min_items",
                                f"Readiness gate {gate_id} requires '{field}' to be a list.",
                                record.location,
                                record.id,
                            )
                        )

    return issues

