from __future__ import annotations

from typing import Any

from .issues import Issue
from .packs import PackRegistry
from .workspace import Record, Workspace


def is_missing(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def get_field(data: dict[str, Any], path: str) -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def is_control_verified(record: Record) -> bool:
    """Return True when a record satisfies the standard verification envelope.

    A record is considered verified when its `coverage` is `verified`, its
    `verification.method` is not `not-verified`, and it carries non-empty
    `verification.evidence`. Packs that declare `requireVerifiedForRisk` gates
    rely on this predicate.
    """
    verification = record.data.get("verification")
    if not isinstance(verification, dict):
        return False
    return (
        record.data.get("coverage") == "verified"
        and verification.get("method") != "not-verified"
        and isinstance(verification.get("evidence"), str)
        and bool(verification.get("evidence", "").strip())
    )


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
        require_verified_for_risk = gate.get("requireVerifiedForRisk", [])
        if not isinstance(require_verified_for_risk, list):
            require_verified_for_risk = []
        risk_levels = {str(value) for value in require_verified_for_risk if isinstance(value, str)}
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

            if risk_levels and str(record.data.get("riskLevel")) in risk_levels:
                if not is_control_verified(record):
                    issues.append(
                        Issue(
                            severity,
                            "readiness.unverified_critical",
                            f"Readiness gate {gate_id} requires risk level "
                            f"'{record.data.get('riskLevel')}' controls to be verified.",
                            record.location,
                            record.id,
                        )
                    )

    return issues

