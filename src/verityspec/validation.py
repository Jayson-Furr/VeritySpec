from __future__ import annotations

from jsonschema import Draft202012Validator

from .issues import Issue, apply_strict
from .packs import PackRegistry
from .references import extract_reference_edges
from .workspace import Workspace


def validate_workspace(
    workspace: Workspace, registry: PackRegistry, strict: bool = False
) -> list[Issue]:
    issues: list[Issue] = []
    ids: dict[str, str] = {}

    for record in workspace.records:
        if not record.id:
            issues.append(Issue("error", "record.id.missing", "Record is missing string id.", record.location))
        elif record.id in ids:
            issues.append(
                Issue(
                    "error",
                    "record.id.duplicate",
                    f"Record id already declared at {ids[record.id]}.",
                    record.location,
                    record.id,
                )
            )
        else:
            ids[record.id] = record.location

        if not record.kind:
            issues.append(
                Issue("error", "record.kind.missing", "Record is missing string kind.", record.location, record.id)
            )
            continue

        binding = registry.schema_for_kind(record.kind)
        if not binding:
            issues.append(
                Issue(
                    "error",
                    "record.kind.unknown",
                    f"Unknown record kind '{record.kind}'.",
                    record.location,
                    record.id,
                )
            )
            continue

        validator = Draft202012Validator(binding.schema)
        for error in sorted(validator.iter_errors(record.data), key=lambda item: list(item.path)):
            path = ".".join(str(part) for part in error.path)
            location = f"{record.location}:{path}" if path else record.location
            issues.append(
                Issue("error", "schema.validation", error.message, location, record.id)
            )

    by_id = {record.id: record for record in workspace.records if record.id}
    for record in workspace.records:
        for edge in extract_reference_edges(record):
            target = by_id.get(edge.target)
            if target is None:
                issues.append(
                    Issue(
                        "error",
                        "reference.missing",
                        f"Reference '{edge.target}' from {edge.field} does not resolve.",
                        record.location,
                        record.id,
                    )
                )
                continue

            target_status = target.data.get("status")
            if target_status == "removed":
                issues.append(
                    Issue(
                        "error",
                        "reference.removed",
                        f"Reference '{edge.target}' points to a removed record.",
                        record.location,
                        record.id,
                    )
                )
            elif target_status == "deprecated":
                issues.append(
                    Issue(
                        "warning",
                        "reference.deprecated",
                        f"Reference '{edge.target}' points to a deprecated record.",
                        record.location,
                        record.id,
                    )
                )

    return apply_strict(issues) if strict else issues


def lint_workspace(workspace: Workspace, registry: PackRegistry, strict: bool = False) -> list[Issue]:
    issues = validate_workspace(workspace, registry, strict=False)

    for record in workspace.records:
        description = record.data.get("description")
        if not isinstance(description, str) or not description.strip():
            issues.append(
                Issue(
                    "warning",
                    "lint.description.missing",
                    "Record should include a non-empty description.",
                    record.location,
                    record.id,
                )
            )

        owner = record.data.get("owner")
        if owner in {"unknown", "todo", "tbd", ""}:
            issues.append(
                Issue(
                    "warning",
                    "lint.owner.placeholder",
                    "Record owner should not be a placeholder.",
                    record.location,
                    record.id,
                )
            )

        if record.data.get("status") == "draft":
            issues.append(
                Issue(
                    "warning",
                    "lint.status.draft",
                    "Draft records are not release-ready.",
                    record.location,
                    record.id,
                )
            )

    return apply_strict(issues) if strict else issues

