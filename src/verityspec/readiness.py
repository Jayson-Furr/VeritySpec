from __future__ import annotations

from typing import Any

from .issues import Issue, location_at
from .packs import PackRegistry
from .workspace import Workspace


def is_missing(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip() == ""
    return value is None or value == "" or value == [] or value == {}


def get_field(data: dict[str, Any], path: str) -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def condition_matches(data: dict[str, Any], condition: dict[str, Any]) -> bool:
    field = condition.get("field")
    if not isinstance(field, str):
        return False

    value = get_field(data, field)
    matched = True
    evaluated = False

    if "equals" in condition:
        matched = matched and value == condition["equals"]
        evaluated = True
    if "notEquals" in condition:
        matched = matched and value != condition["notEquals"]
        evaluated = True
    if "present" in condition:
        should_be_present = bool(condition["present"])
        presence_matches = not is_missing(value) if should_be_present else is_missing(value)
        matched = matched and presence_matches
        evaluated = True

    return evaluated and matched


def failed_rule_condition(record_data: dict[str, Any], rule: dict[str, Any]) -> dict[str, Any] | None:
    when = rule.get("when")
    if isinstance(when, dict) and not condition_matches(record_data, when):
        return None

    requirements = rule.get("must", [])
    if not isinstance(requirements, list):
        return None

    for requirement in requirements:
        if isinstance(requirement, dict) and not condition_matches(record_data, requirement):
            return requirement
    return None


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
        rules = gate.get("rules", [])
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
                            location_at(record.location, field),
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
                                location_at(record.location, str(field)),
                                record.id,
                            )
                        )
                    elif isinstance(minimum, int) and not isinstance(value, list):
                        issues.append(
                            Issue(
                                severity,
                                "readiness.min_items",
                                f"Readiness gate {gate_id} requires '{field}' to be a list.",
                                location_at(record.location, str(field)),
                                record.id,
                            )
                        )

            if isinstance(rules, list):
                for rule in rules:
                    if not isinstance(rule, dict):
                        continue
                    failed_condition = failed_rule_condition(record.data, rule)
                    if failed_condition is None:
                        continue
                    issues.append(
                        Issue(
                            severity,
                            str(rule.get("code", "readiness.rule")),
                            str(
                                rule.get(
                                    "message",
                                    f"Readiness gate {gate_id} rule failed.",
                                )
                            ),
                            location_at(record.location, failed_condition.get("field")),
                            record.id,
                        )
                    )

    return issues
