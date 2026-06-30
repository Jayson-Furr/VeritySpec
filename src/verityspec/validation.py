from __future__ import annotations

from jsonschema import Draft202012Validator

from .envelope import RECORD_ENVELOPE_REQUIRED
from .issues import Issue, apply_strict, location_at
from .packs import PackRegistry
from .references import ReferenceEdge, extract_reference_edges
from .versions import validate_workspace_version
from .workspace import Record, Workspace


def validate_builtin_schema_envelope(registry: PackRegistry) -> list[Issue]:
    issues: list[Issue] = []
    for kind, binding in registry.schemas.items():
        required = set(binding.schema.get("required", []))
        properties = set(binding.schema.get("properties", {}))
        for field in RECORD_ENVELOPE_REQUIRED:
            if field not in required:
                issues.append(
                    Issue(
                        "error",
                        "schema.envelope.required_missing",
                        f"Schema for kind '{kind}' does not require envelope field '{field}'.",
                        str(binding.path),
                    )
                )
            if field not in properties:
                issues.append(
                    Issue(
                        "error",
                        "schema.envelope.property_missing",
                        f"Schema for kind '{kind}' does not define envelope field '{field}'.",
                        str(binding.path),
                    )
                )
    return issues


def find_cycles(adjacency: dict[str, list[str]]) -> list[list[str]]:
    cycles: list[list[str]] = []
    visited: set[str] = set()
    stack: list[str] = []
    in_stack: dict[str, int] = {}
    seen: set[tuple[str, ...]] = set()

    def normalize(cycle: list[str]) -> tuple[str, ...]:
        body = cycle[:-1]
        if not body:
            return tuple(cycle)
        rotations = [tuple(body[index:] + body[:index]) for index in range(len(body))]
        best = min(rotations)
        return best + (best[0],)

    def visit(node: str) -> None:
        visited.add(node)
        in_stack[node] = len(stack)
        stack.append(node)
        for target in adjacency.get(node, []):
            if target not in adjacency:
                continue
            if target not in visited:
                visit(target)
            elif target in in_stack:
                cycle = stack[in_stack[target] :] + [target]
                key = normalize(cycle)
                if key not in seen:
                    seen.add(key)
                    cycles.append(cycle)
        stack.pop()
        in_stack.pop(node, None)

    for node in sorted(adjacency):
        if node not in visited:
            visit(node)
    return cycles


def validate_reference_graph(
    workspace: Workspace,
    registry: PackRegistry,
    by_id: dict[str, Record],
    edges: list[tuple[Record, ReferenceEdge]],
) -> list[Issue]:
    issues: list[Issue] = []
    incoming: dict[str, set[str]] = {record_id: set() for record_id in by_id}
    outgoing: dict[str, set[str]] = {record_id: set() for record_id in by_id}
    adjacency: dict[str, list[str]] = {record_id: [] for record_id in by_id}

    for record, edge in edges:
        target = by_id.get(edge.target)
        if target is None:
            continue

        incoming[edge.target].add(edge.source)
        outgoing[edge.source].add(edge.target)
        adjacency[edge.source].append(edge.target)

        if record.kind and target.kind and not registry.allows_reference(
            record.kind, edge.relationship, target.kind
        ):
            issues.append(
                Issue(
                    "error",
                    "reference.disallowed",
                    (
                        f"Reference relationship '{edge.relationship}' is not allowed "
                        f"from kind '{record.kind}' to kind '{target.kind}'."
                    ),
                    location_at(record.location, edge.field),
                    record.id,
                )
            )

    for record in workspace.records:
        if not record.id or record.id not in by_id:
            continue
        if record.kind == "schema.object" and not incoming[record.id]:
            issues.append(
                Issue(
                    "warning",
                    "schema.unused",
                    "Schema record is not referenced by any record.",
                    record.location,
                    record.id,
                )
            )
        elif record.kind not in {"product", "schema.object"} and not incoming[record.id] and not outgoing[record.id]:
            issues.append(
                Issue(
                    "warning",
                    "graph.orphan",
                    "Record is not connected to the workspace reference graph.",
                    record.location,
                    record.id,
                )
            )

    for cycle in find_cycles(adjacency):
        issues.append(
            Issue(
                "warning",
                "graph.cycle",
                "Reference cycle detected: " + " -> ".join(cycle),
                by_id[cycle[0]].location if cycle and cycle[0] in by_id else None,
                cycle[0] if cycle else None,
            )
        )

    return issues


def validate_workspace(
    workspace: Workspace, registry: PackRegistry, strict: bool = False
) -> list[Issue]:
    issues: list[Issue] = validate_workspace_version(workspace)
    issues.extend(validate_builtin_schema_envelope(registry))
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
            issues.append(
                Issue(
                    "error",
                    "schema.validation",
                    error.message,
                    location_at(record.location, error.path),
                    record.id,
                )
            )

    by_id = {record.id: record for record in workspace.records if record.id}
    edges: list[tuple[Record, ReferenceEdge]] = []
    for record in workspace.records:
        for edge in extract_reference_edges(record):
            edges.append((record, edge))
            target = by_id.get(edge.target)
            if target is None:
                issues.append(
                    Issue(
                        "error",
                        "reference.missing",
                        f"Reference '{edge.target}' from {edge.field} does not resolve.",
                        location_at(record.location, edge.field),
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
                        location_at(record.location, edge.field),
                        record.id,
                    )
                )
            elif target_status == "deprecated":
                issues.append(
                    Issue(
                        "warning",
                        "reference.deprecated",
                        f"Reference '{edge.target}' points to a deprecated record.",
                        location_at(record.location, edge.field),
                        record.id,
                    )
                )

    issues.extend(validate_reference_graph(workspace, registry, by_id, edges))

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
